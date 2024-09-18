# Generated by Django 5.1.1 on 2024-09-18 03:08

import core.utils.database
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Quiz",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "uid",
                    models.CharField(
                        max_length=50, primary_key=True, serialize=False, unique=True
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="QuizAnswer",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        default=core.utils.database.generate_snow_flake_id,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("content", models.CharField(max_length=255)),
                ("is_correct", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="QuizQuestion",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        default=core.utils.database.generate_snow_flake_id,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("content", models.CharField(max_length=500)),
                ("order", models.PositiveSmallIntegerField()),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="questions",
                        to="core.quiz",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuizAnswerSubmission",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        default=core.utils.database.generate_snow_flake_id,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user_name", models.CharField(max_length=100)),
                (
                    "answers",
                    models.ManyToManyField(
                        related_name="submissions", to="core.quizanswer"
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="submitted_answers",
                        to="core.quizquestion",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="quizanswer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to="core.quizquestion",
            ),
        ),
        migrations.CreateModel(
            name="QuizParticipant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user_name", models.CharField(max_length=100)),
                ("score", models.IntegerField(default=0)),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="participants",
                        to="core.quiz",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        models.F("quiz_id"), models.F("score"), name="idx_quiz_score"
                    ),
                    models.Index(
                        models.F("user_name"),
                        models.F("score"),
                        name="idx_user_name_score",
                    ),
                ],
                "unique_together": {("quiz", "user_name")},
            },
        ),
        migrations.AddIndex(
            model_name="quizquestion",
            index=models.Index(
                models.F("quiz"), models.F("order"), name="idx_quiz_order_unique"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="quizquestion",
            unique_together={("quiz", "order")},
        ),
        migrations.AlterUniqueTogether(
            name="quizanswersubmission",
            unique_together={("question", "user_name")},
        ),
        migrations.AlterUniqueTogether(
            name="quizanswer",
            unique_together={("id", "is_correct")},
        ),
    ]
