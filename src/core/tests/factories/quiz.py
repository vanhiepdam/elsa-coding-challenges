import factory
from django.db.models.signals import post_save
from factory.django import DjangoModelFactory

from core.models import Quiz, QuizAnswer, QuizAnswerSubmission, QuizParticipant, QuizQuestion
from core.models.base import generate_snow_flake_id


@factory.django.mute_signals(post_save)
class QuizFactory(DjangoModelFactory):
    class Meta:
        model = Quiz
        django_get_or_create = ("uid",)

    uid = factory.LazyAttribute(lambda _: str(generate_snow_flake_id()))


@factory.django.mute_signals(post_save)
class QuizParticipantFactory(DjangoModelFactory):
    class Meta:
        model = QuizParticipant

    quiz = factory.SubFactory(QuizFactory)
    user_name = factory.Faker("name")


@factory.django.mute_signals(post_save)
class QuizQuestionFactory(DjangoModelFactory):
    class Meta:
        model = QuizQuestion

    quiz = factory.SubFactory(QuizFactory)
    content = factory.Faker("sentence")
    order = factory.Faker("random_int", min=0, max=100)


@factory.django.mute_signals(post_save)
class QuizAnswerFactory(DjangoModelFactory):
    class Meta:
        model = QuizAnswer

    question = factory.SubFactory(QuizQuestionFactory)
    content = factory.Faker("sentence")
    is_correct = factory.Faker("boolean")


@factory.django.mute_signals(post_save)
class QuizAnswerSubmissionFactory(DjangoModelFactory):
    class Meta:
        model = QuizAnswerSubmission

    question = factory.SubFactory(QuizQuestionFactory)
    participant = factory.SubFactory(QuizParticipantFactory)

    @factory.post_generation
    def answers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.answers.add(*extracted)
