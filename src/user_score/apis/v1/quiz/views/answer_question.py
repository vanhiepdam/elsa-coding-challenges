from django.db.models import QuerySet
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from core.models import QuizQuestion
from core.utils.api import CustomAPIViewSetMixin, QuizBasedAPIMixin
from user_score.apis.v1.quiz.serializers.answer_question import AnswerQuizQuestionSerializerV1


class QuizQuestionAPIV1(QuizBasedAPIMixin, CustomAPIViewSetMixin, GenericViewSet):
    def get_queryset(self) -> QuerySet:
        return QuizQuestion.objects.filter(quiz_id=self.quiz_uid)

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context["question_uid"] = self.get_object().id
        return context

    @action(
        detail=True,
        methods=["POST"],
        url_path="answer",
        url_name="answer",
        serializer_class=AnswerQuizQuestionSerializerV1,
    )
    def answer_question(self, request, *args, **kwargs):
        return self.perform_action(request)
