from rest_framework import status
from rest_framework.response import Response


class CustomAPIViewSetMixin:
    def perform_action(self, request, status_code=status.HTTP_200_OK):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(data=serializer.to_representation(instance), status=status_code)


class QuizBasedAPIMixin:
    @property
    def quiz_uid(self):
        return self.kwargs["quiz_uid"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["quiz_uid"] = self.quiz_uid
        return context
