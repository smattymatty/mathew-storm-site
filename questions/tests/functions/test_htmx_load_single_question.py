from unittest.mock import patch
from django.test import TestCase, RequestFactory
from django.http import HttpResponseForbidden
from django.template.response import TemplateResponse

from questions.views import htmx_load_single_question
from questions.models import Question, TutorialTitle


class TestHtmxLoadSingleQuestion(TestCase):
    """
    Tests for the htmx_load_single_question view function.
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
        )

    def setUp(self):
        """Set up the request factory for each test."""
        self.factory = RequestFactory()

    def test_non_htmx_request_returns_forbidden(self):
        """Test that non-HTMX requests are forbidden."""
        request = self.factory.get(
            f"/htmx/load-single-question/{self.question.pk}/"
        )
        response = htmx_load_single_question(
            request, question_pk=self.question.pk
        )
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_successful_question_load(self):
        """Test that a question is loaded successfully via an HTMX GET request."""
        request = self.factory.get(
            f"/htmx/load-single-question/{self.question.pk}/"
        )
        request.htmx = True

        response = htmx_load_single_question(
            request, question_pk=self.question.pk
        )

        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            "questions/partials/question_block/_question_block_htmx.html",
        )
        # Check that the correct question is in the context
        self.assertEqual(response.context_data["question"], self.question)

    @patch("questions.views.logger")
    def test_question_not_found(self, mock_logger):
        """Test behavior when the requested question pk does not exist."""
        non_existent_pk = self.question.pk + 99
        request = self.factory.get(
            f"/htmx/load-single-question/{non_existent_pk}/"
        )
        request.htmx = True

        response = htmx_load_single_question(
            request, question_pk=non_existent_pk
        )

        self.assertEqual(
            response.context_data["error_message"], "Question not found."
        )
        mock_logger.error.assert_called_with(
            f"Question with pk {non_existent_pk} not found"
        )

    @patch("questions.views.logger")
    @patch("questions.views.Question.objects.select_related")
    def test_general_exception_handling(
        self, mock_select_related, mock_logger
    ):
        """Test that general exceptions are caught and handled."""
        # Make the chained .get() call raise an exception
        mock_select_related.return_value.get.side_effect = Exception(
            "A generic server error."
        )

        request = self.factory.get(
            f"/htmx/load-single-question/{self.question.pk}/"
        )
        request.htmx = True

        response = htmx_load_single_question(
            request, question_pk=self.question.pk
        )

        # Now the context will be correctly populated by the exception handler
        self.assertEqual(
            response.context_data["error_message"],
            "An error occurred while loading the question. Please try again.",
        )
        self.assertTrue(mock_logger.error.called)
