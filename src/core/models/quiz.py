from django.db import models

from core.constants.quiz import USERNAME_LENGTH
from core.models.base import SnowFlakeIDModel, TimestampModel


class Quiz(TimestampModel):
    uid = models.CharField(max_length=50, unique=True, primary_key=True)


class QuizParticipant(TimestampModel):
    quiz = models.ForeignKey(
        "core.Quiz",
        related_name="participants",
        on_delete=models.PROTECT,
    )
    user_name = models.CharField(max_length=USERNAME_LENGTH)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = (("quiz", "user_name"),)
        indexes = [
            models.Index("quiz_id", "score", name="idx_quiz_score"),
            models.Index("user_name", "score", name="idx_user_name_score"),
        ]


class QuizQuestion(SnowFlakeIDModel, TimestampModel):
    quiz = models.ForeignKey(
        "core.Quiz",
        related_name="questions",
        on_delete=models.PROTECT,
    )
    content = models.CharField(max_length=500)
    order = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (("quiz", "order"),)
        indexes = [
            models.Index("quiz", "order", name="idx_quiz_order_unique"),
        ]


class QuizAnswer(SnowFlakeIDModel, TimestampModel):
    question = models.ForeignKey(
        "core.QuizQuestion",
        related_name="answers",
        on_delete=models.CASCADE,
    )
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = (("id", "is_correct"),)


class QuizAnswerSubmission(SnowFlakeIDModel, TimestampModel):
    question = models.ForeignKey(
        "core.QuizQuestion",
        related_name="submitted_answers",
        on_delete=models.PROTECT,
    )
    answers = models.ManyToManyField(
        "core.QuizAnswer",
        related_name="submissions",
        blank=False,
    )
    user_name = models.CharField(max_length=USERNAME_LENGTH)

    class Meta:
        unique_together = (("question", "user_name"),)


__all__ = [
    "Quiz",
    "QuizParticipant",
    "QuizQuestion",
    "QuizAnswer",
    "QuizAnswerSubmission",
]
