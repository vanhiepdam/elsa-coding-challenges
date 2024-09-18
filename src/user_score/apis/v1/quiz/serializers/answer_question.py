from rest_framework import serializers

from user_score.services.quiz.submit_answer import (
    SubmitAnswerResult,
    SubmitQuizQuestionAnswerService,
)


class AnswerQuizQuestionSerializerV1(serializers.Serializer):
    answer_ids = serializers.ListField(child=serializers.IntegerField(), min_length=1)
    participant_id = serializers.IntegerField()

    def create(self, validated_data: dict) -> SubmitAnswerResult:
        result = SubmitQuizQuestionAnswerService().submit(
            quiz_uid=self.context["quiz_uid"],
            question_uid=self.context["question_uid"],
            answer_ids=validated_data["answer_ids"],
            participant_id=validated_data["participant_id"],
        )
        return result

    def to_representation(self, instance: SubmitAnswerResult) -> dict:
        return {
            "is_correct": instance.is_correct,
        }
