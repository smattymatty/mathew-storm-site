# questions/tests/integration/test_quiz_edge_cases.py

from unittest.mock import patch, Mock
from django.test import TestCase, RequestFactory, override_settings
from django.http import HttpResponseForbidden

from questions.views import htmx_check_answer, htmx_load_single_question
from questions.models import Question, TutorialTitle


@override_settings(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
            "OPTIONS": {
                "timeout": 20,
            },
        }
    }
)
class QuizEdgeCaseTest(TestCase):
    """
    Tests for edge cases and error conditions in quiz functionality.
    """

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.tutorial = TutorialTitle.objects.create(
            title_id_slug="edge-case-tut", name="Edge Case Tutorial"
        )

        cls.question = Question.objects.create(
            tutorial_title=cls.tutorial,
            question_id_slug="edge-q",
            question_text="Edge case question?",
            answer_a="A",
            answer_b="B",
            answer_c="C",
            answer_d="D",
            correct_answer="a",
        )

    def setUp(self):
        """Set up for each test."""
        self.factory = RequestFactory()

    def test_case_insensitive_answer_checking(self):
        """Test that answer checking is case insensitive."""
        # Test uppercase submission
        request = self.factory.post(
            f"/htmx/check-answer/{self.question.pk}/",
            {f"answer_for_q{self.question.pk}": "A"},  # Uppercase
        )
        request.htmx = True

        response = htmx_check_answer(request, question_pk=self.question.pk)
        self.assertTrue(response.context_data["is_correct"])

        # Test lowercase submission
        request = self.factory.post(
            f"/htmx/check-answer/{self.question.pk}/",
            {f"answer_for_q{self.question.pk}": "a"},  # Lowercase
        )
        request.htmx = True

        response = htmx_check_answer(request, question_pk=self.question.pk)
        self.assertTrue(response.context_data["is_correct"])

    def test_whitespace_handling_in_answers(self):
        """Test that leading/trailing whitespace in answers is handled."""
        request = self.factory.post(
            f"/htmx/check-answer/{self.question.pk}/",
            {f"answer_for_q{self.question.pk}": "  a  "},  # With whitespace
        )
        request.htmx = True

        response = htmx_check_answer(request, question_pk=self.question.pk)
        self.assertTrue(response.context_data["is_correct"])

    def test_invalid_answer_choice_handling(self):
        """Test handling of invalid answer choices (not a, b, c, d)."""
        request = self.factory.post(
            f"/htmx/check-answer/{self.question.pk}/",
            {f"answer_for_q{self.question.pk}": "z"},  # Invalid choice
        )
        request.htmx = True

        response = htmx_check_answer(request, question_pk=self.question.pk)
        self.assertFalse(response.context_data["is_correct"])
        self.assertEqual(
            response.context_data["submitted_answer_text"], "Unknown"
        )

    @patch("questions.views.logger")
    def test_database_error_handling(self, mock_logger):
        """Test handling of database errors during question retrieval."""
        with patch(
            "questions.models.Question.objects.select_related"
        ) as mock_query:
            mock_query.side_effect = Exception("Database connection error")

            request = self.factory.post(
                f"/htmx/check-answer/{self.question.pk}/",
                {f"answer_for_q{self.question.pk}": "a"},
            )
            request.htmx = True

            response = htmx_check_answer(request, question_pk=self.question.pk)

            # Should log the error
            mock_logger.error.assert_called()
            # Should return error template (which is _question_list_htmx.html)
            self.assertEqual(
                response.template_name,
                "questions/partials/_question_list_htmx.html",
            )

    def test_concurrent_request_handling(self):
        """Test that concurrent requests don't interfere with each other."""
        # Simulate multiple simultaneous requests
        requests = []
        for i in range(5):
            request = self.factory.post(
                f"/htmx/check-answer/{self.question.pk}/",
                {f"answer_for_q{self.question.pk}": "a"},
            )
            request.htmx = True
            requests.append(request)

        # Process all requests
        responses = [
            htmx_check_answer(req, question_pk=self.question.pk)
            for req in requests
        ]

        # All should succeed
        for response in responses:
            self.assertTrue(response.context_data["is_correct"])
            self.assertEqual(response.status_code, 200)

    def test_malformed_post_data(self):
        """Test handling of malformed POST data."""
        # Test with completely wrong field name
        request = self.factory.post(
            f"/htmx/check-answer/{self.question.pk}/",
            {"wrong_field_name": "a"},
        )
        request.htmx = True

        response = htmx_check_answer(request, question_pk=self.question.pk)
        self.assertIn(
            "Please select an answer", response.context_data["error_message"]
        )
