# type: ignore

import pytest
from rest_framework.exceptions import ValidationError

from core.tests.factories.quiz import (
    QuizAnswerFactory,
    QuizAnswerSubmissionFactory,
    QuizFactory,
    QuizParticipantFactory,
    QuizQuestionFactory,
)
from user_score.services.quiz.submit_answer import SubmitQuizQuestionAnswerService

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def quiz():
    return QuizFactory()


@pytest.fixture
def quiz_question(quiz):
    return QuizQuestionFactory(quiz=quiz)


def test_answers_empty():
    # Act
    with pytest.raises(ValidationError) as ex:
        SubmitQuizQuestionAnswerService().validate_answers(question_uid=1, answer_ids=[])

    # Assert
    assert ex.value.detail[0] == "Answer IDs are required"


def test_invalid_answer_ids__answer_not_in_db(quiz, quiz_question):
    # Arrange
    answer_1 = QuizAnswerFactory(question=quiz_question)

    # Act
    with pytest.raises(ValidationError) as ex:
        service = SubmitQuizQuestionAnswerService()
        service.set_answers(answer_ids=[answer_1.id, 2])
        service.validate_answers(question_uid=quiz_question.id, answer_ids=[answer_1.id, 2])

    # Assert
    assert ex.value.detail[0] == "Invalid answer IDs"


def test_invalid_answer_ids__answer_belongs_to_other_question(quiz, quiz_question):
    # Arrange
    answer_1 = QuizAnswerFactory(question=quiz_question)
    wrong_answer = QuizAnswerFactory()

    # Act
    with pytest.raises(ValidationError) as ex:
        service = SubmitQuizQuestionAnswerService()
        service.set_answers(answer_ids=[answer_1.id, wrong_answer.id])
        service.validate_answers(
            question_uid=quiz_question.id, answer_ids=[answer_1.id, wrong_answer.id]
        )

    # Assert
    assert ex.value.detail[0] == "Invalid answer IDs"


def test_participant_not_found(quiz, quiz_question):
    # Act
    with pytest.raises(ValidationError) as ex:
        SubmitQuizQuestionAnswerService().validate_participant(
            quiz_uid=quiz.uid, question_uid=quiz_question.id, participant_id=123456789
        )

    # Assert
    assert ex.value.detail[0] == "Participant not found in the quiz"


def test_participant_already_submit_answer_for_the_question(quiz, quiz_question):
    # Arrange
    participant = QuizParticipantFactory(quiz=quiz)
    QuizAnswerSubmissionFactory(
        question=quiz_question,
        participant=participant,
        answers=[QuizAnswerFactory(question=quiz_question)],
    )

    # Act
    with pytest.raises(ValidationError) as ex:
        SubmitQuizQuestionAnswerService().validate_participant(
            quiz_uid=quiz.uid, question_uid=quiz_question.id, participant_id=participant.id
        )

    # Assert
    assert ex.value.detail[0] == "Already answered"


def test_handle_answer__incorrect_answer(quiz, quiz_question):
    # Arrange
    answer_2 = QuizAnswerFactory(question=quiz_question, is_correct=False)
    participant = QuizParticipantFactory(quiz=quiz)

    # Arrange noise data
    QuizAnswerFactory(question=quiz_question, is_correct=True)

    # Act
    service = SubmitQuizQuestionAnswerService()
    result = service.submit(
        quiz_uid=quiz.uid,
        question_uid=quiz_question.id,
        answer_ids=[answer_2.id],
        participant_id=participant.id,
    )

    # Assert
    assert result.is_correct is False
    assert result.submission.question_id == quiz_question.id
    assert result.submission.participant_id == participant.id
    assert result.submission.answers.count() == 1


def test_handle_answer__not_enough_correct_answer(quiz, quiz_question):
    # Arrange
    answer_1 = QuizAnswerFactory(question=quiz_question, is_correct=False)
    participant = QuizParticipantFactory(quiz=quiz)

    # Arrange noise data
    QuizAnswerFactory(question=quiz_question, is_correct=False)
    QuizAnswerFactory(question=quiz_question, is_correct=True)

    # Act
    service = SubmitQuizQuestionAnswerService()
    result = service.submit(
        quiz_uid=quiz.uid,
        question_uid=quiz_question.id,
        answer_ids=[answer_1.id],
        participant_id=participant.id,
    )

    # Assert
    assert result.is_correct is False
    assert result.submission.question_id == quiz_question.id
    assert result.submission.participant_id == participant.id
    assert result.submission.answers.count() == 1


def test_handle_answer__correct_answer_multiple_answer(quiz, quiz_question):
    # Arrange
    answer_1 = QuizAnswerFactory(question=quiz_question, is_correct=True)
    answer_2 = QuizAnswerFactory(question=quiz_question, is_correct=True)
    participant = QuizParticipantFactory(quiz=quiz)

    # Arrange noise data
    QuizAnswerFactory(question=quiz_question, is_correct=False)

    # Act
    service = SubmitQuizQuestionAnswerService()
    result = service.submit(
        quiz_uid=quiz.uid,
        question_uid=quiz_question.id,
        answer_ids=[answer_1.id, answer_2.id],
        participant_id=participant.id,
    )

    # Assert
    participant.refresh_from_db()
    assert result.is_correct is True
    assert result.submission.question_id == quiz_question.id
    assert result.submission.participant_id == participant.id
    assert result.submission.answers.count() == 2
    assert participant.score == 1


def test_handle_answer__correct_answer_single_answer(quiz, quiz_question):
    # Arrange
    answer_1 = QuizAnswerFactory(question=quiz_question, is_correct=True)
    participant = QuizParticipantFactory(quiz=quiz, score=2)

    # Arrange noise data
    QuizAnswerFactory(question=quiz_question, is_correct=False)

    # Act
    service = SubmitQuizQuestionAnswerService()
    result = service.submit(
        quiz_uid=quiz.uid,
        question_uid=quiz_question.id,
        answer_ids=[answer_1.id],
        participant_id=participant.id,
    )

    # Assert
    participant.refresh_from_db()
    assert result.is_correct is True
    assert result.submission.question_id == quiz_question.id
    assert result.submission.participant_id == participant.id
    assert result.submission.answers.count() == 1
    assert participant.score == 3
