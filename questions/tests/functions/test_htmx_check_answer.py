from unittest.mock import patch
from django.test import TestCase, RequestFactory
from django.http import HttpResponseForbidden
from django.template.response import TemplateResponse

from questions.views import htmx_check_answer
from questions.models import Question, TutorialTitle


class TestHtmxCheckAnswer(TestCase):
    """
    Tests for the htmx_check_answer view function.
    """

    @classmethod
    def setUpTestData(cls):
        """Set up a single question for all tests in this class."""
        tutorial = TutorialTitle.objects.create(
            title_id_slug="test-tut", name="Test Tutorial"
        )
        cls.question = Question.objects.create(
            tutorial_title=tutorial,
            question_id_slug="q1",
            question_text="What is 1+1?",
            answer_a="1",
            answer_b="2",
            answer_c="3",
            answer_d="4",
            correct_answer="b",  # The correct answer is 'b'
        )

    def setUp(self):
        """Set up the request factory for each test."""
        self.factory = RequestFactory()

    def test_non_htmx_request_returns_forbidden(self):
        """Test that non-HTMX requests are forbidden."""
        request = self.factory.post(f"/htmx/check-answer/{self.question.pk}/")
        response = htmx_check_answer(request, question_pk=self.question.pk)
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_get_request_returns_forbidden(self):
        """Test that non-POST requests are forbidden."""
        request = self.factory.get(f"/htmx/check-answer/{self.question.pk}/")
        request.htmx = True
        response = htmx_check_answer(request, question_pk=self.question.pk)
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_correct_answer_submission(self):
        """Test that a correct answer submission returns the correct feedback."""
        post_data = {f"answer_for_q{self.question.pk}": "b"}
        request = self.factory.post(
            f"/htmx/check-answer/{self.question.pk}/", post_data
        )
        request.htmx = True

        response = htmx_check_answer(request, question_pk=self.question.pk)

        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            "questions/partials/feedback/_feedback_correct.html",
        )
        self.assertTrue(response.context_data["is_correct"])

    def test_incorrect_answer_submission(self):
        """Test that an incorrect answer submission returns the incorrect feedback."""
        post_data = {f"answer_for_q{self.question.pk}": "c"}
        request = self.factory.post(
            f"/htmx/check-answer/{self.question.pk}/", post_data
        )
        request.htmx = True

        response = htmx_check_answer(request, question_pk=self.question.pk)

        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            "questions/partials/feedback/_feedback_incorrect.html",
        )
        self.assertFalse(response.context_data["is_correct"])

    def test_no_answer_submitted(self):
        """Test that submitting with no answer returns an error message."""
        request = self.factory.post(
            f"/htmx/check-answer/{self.question.pk}/", {}
        )
        request.htmx = True

        response = htmx_check_answer(request, question_pk=self.question.pk)
        self.assertEqual(
            response.context_data["error_message"],
            "Please select an answer before submitting.",
        )
        self.assertEqual(
            response.template_name,
            "questions/partials/question_block/_question_block_htmx.html",
        )

    @patch("questions.views.logger")
    def test_question_not_found(self, mock_logger):
        """Test behavior when the requested question does not exist."""
        non_existent_pk = self.question.pk + 99
        request = self.factory.post(
            f"/htmx/check-answer/{non_existent_pk}/", {}
        )
        request.htmx = True

        response = htmx_check_answer(request, question_pk=non_existent_pk)

        self.assertEqual(
            response.context_data["error_message"], "Question not found."
        )
        mock_logger.error.assert_called_with(
            f"Question with pk {non_existent_pk} not found"
        )
