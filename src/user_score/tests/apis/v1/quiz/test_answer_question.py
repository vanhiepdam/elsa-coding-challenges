# type: ignore
from unittest import mock

import pytest

from core.tests.factories.quiz import QuizAnswerSubmissionFactory, QuizFactory, QuizQuestionFactory
from user_score.services.quiz.submit_answer import SubmitAnswerResult

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def quiz():
    return QuizFactory()


@pytest.fixture
def quiz_question(quiz):
    return QuizQuestionFactory(quiz=quiz)


@mock.patch(
    "user_score.services.quiz.submit_answer.SubmitQuizQuestionAnswerService.submit",
)
def test_question_not_found(submit, api_client, quiz):
    # Arrange
    data = {
        "answer_ids": [],
        "participant_id": 123456789,
    }

    submit.side_effect = lambda *args, **kwargs: SubmitAnswerResult(
        is_correct=True, submission=QuizAnswerSubmissionFactory()
    )

    # Act
    response = api_client.post(
        f"/api/v1/quizzes/{quiz.uid}/questions/45678/answer", data=data, format="json"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["errors"][0]["code"] == "not_found"
    assert response.json()["errors"][0]["detail"] == "Not found."


@mock.patch(
    "user_score.services.quiz.submit_answer.SubmitQuizQuestionAnswerService.submit",
)
def test_answer_ids_empty(submit, api_client, quiz, quiz_question):
    # Arrange
    data = {
        "answer_ids": [],
        "participant_id": 123456789,
    }

    submit.side_effect = lambda *args, **kwargs: SubmitAnswerResult(
        is_correct=True, submission=QuizAnswerSubmissionFactory()
    )

    # Act
    response = api_client.post(
        f"/api/v1/quizzes/{quiz.uid}/questions/{quiz_question.id}/answer", data=data, format="json"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["errors"][0]["code"] == "min_length"
    assert response.json()["errors"][0]["detail"] == "Ensure this field has at least 1 elements."


@mock.patch(
    "user_score.services.quiz.submit_answer.SubmitQuizQuestionAnswerService.submit",
)
def test_success(submit, api_client, quiz, quiz_question):
    # Arrange
    answer = QuizAnswerSubmissionFactory(question=quiz_question)
    data = {
        "answer_ids": [answer.id],
        "participant_id": 123456789,
    }

    submit.side_effect = lambda *args, **kwargs: SubmitAnswerResult(
        is_correct=True, submission=QuizAnswerSubmissionFactory()
    )

    # Act
    response = api_client.post(
        f"/api/v1/quizzes/{quiz.uid}/questions/{quiz_question.id}/answer", data=data, format="json"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "is_correct": True,
    }
    submit.assert_called_once_with(
        quiz_uid=quiz.uid,
        question_uid=quiz_question.id,
        answer_ids=[answer.id],
        participant_id=123456789,
    )
