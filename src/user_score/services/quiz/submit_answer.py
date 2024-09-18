import json
from dataclasses import dataclass

from django.db import OperationalError, transaction
from django.db.models import F
from kafka.errors import KafkaTimeoutError

from core.constants.queue import MessageType, QueueName
from core.models import QuizAnswer, QuizAnswerSubmission, QuizParticipant
from core.utils.cache import RedisLock
from core.utils.message_queue import KafkaProducer
from core.utils.retry import retry_on_connection_issue
from core.utils.service import BaseExecuteService


@dataclass(frozen=True)
class SubmitAnswerResult:
    is_correct: bool
    submission: QuizAnswerSubmission


class SubmitQuizQuestionAnswerService(BaseExecuteService):
    def __init__(self):
        super().__init__()
        self.answers = None

    def set_answers(self, answer_ids: list[int]) -> None:
        self.answers = QuizAnswer.objects.filter(
            id__in=answer_ids,
        ).only("id")

    def validate_answers(self, question_uid: int, answer_ids: list[int]) -> None:
        answer_ids = set(answer_ids)
        if not answer_ids:
            self.raise_validation_error("Answer IDs are required")

        if self.answers.filter(
            question_id=question_uid,
        ).count() != len(answer_ids):
            self.raise_validation_error("Invalid answer IDs")

    def validate_participant(self, quiz_uid: int, question_uid: int, participant_id: int) -> None:
        if not QuizParticipant.objects.filter(
            quiz_id=quiz_uid,
            id=participant_id,
        ).exists():
            self.raise_validation_error("Participant not found in the quiz")
        if QuizAnswerSubmission.objects.filter(
            question_id=question_uid,
            participant_id=participant_id,
        ).exists():
            self.raise_validation_error("Already answered")

    @staticmethod
    @retry_on_connection_issue(exceptions=(KafkaTimeoutError,))
    def send_update_leaderboard_message(quiz_uid: int) -> None:
        producer = KafkaProducer()
        message = producer.get_message_to_send(
            data=json.dumps(
                {
                    "quiz_uid": quiz_uid,
                }
            ),
            message_type=MessageType.LEADERBOARD_UPDATE,
        )
        producer.send(message, QueueName.LEADERBOARD.value)

    def handle_answer(self, question_uid: int, participant_id: int) -> SubmitAnswerResult:
        if set(
            QuizAnswer.objects.filter(
                question_id=question_uid,
                is_correct=True,
            ).values_list("id", flat=True)
        ) == set(self.answers.values_list("id", flat=True)):
            result = True
        else:
            result = False
        submission = QuizAnswerSubmission.objects.create(
            question_id=question_uid,
            participant_id=participant_id,
        )
        submission.answers.set(self.answers)
        return SubmitAnswerResult(is_correct=result, submission=submission)

    def update_participant_score(self, quiz_uid: int, participant_id: int) -> None:
        QuizParticipant.objects.filter(
            quiz_id=quiz_uid,
            id=participant_id,
        ).update(score=F("score") + 1)

    @retry_on_connection_issue(exceptions=(OperationalError,), wait_max=1000, retries=5)
    @transaction.atomic
    def submit(
        self,
        quiz_uid: int,
        question_uid: int,
        answer_ids: list[int],
        participant_id: int,
    ) -> SubmitAnswerResult:
        with RedisLock(f"submit_quiz_question_answer_{question_uid}_{participant_id}"):
            self.set_answers(answer_ids)
            self.validate_answers(question_uid=question_uid, answer_ids=answer_ids)
            self.validate_participant(
                quiz_uid=quiz_uid, question_uid=question_uid, participant_id=participant_id
            )
            result = self.handle_answer(question_uid=question_uid, participant_id=participant_id)
            if result.is_correct:
                self.update_participant_score(quiz_uid=quiz_uid, participant_id=participant_id)
                self.send_update_leaderboard_message(quiz_uid)
            return result
