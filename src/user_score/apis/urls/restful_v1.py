from rest_framework.routers import DefaultRouter

from user_score.apis.v1.quiz.views.answer_question import QuizQuestionAPIV1

router = DefaultRouter(trailing_slash=False)

router.register(
    r"^quizzes/(?P<quiz_uid>[a-zA-Z0-9]+)/questions",
    QuizQuestionAPIV1,
    basename="quiz-question-v1",
)


urlpatterns = router.urls
