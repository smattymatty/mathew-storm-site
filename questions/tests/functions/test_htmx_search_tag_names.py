from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.http import HttpResponse, HttpResponseForbidden

from questions.views import htmx_search_tag_names
from questions.models import Question, TutorialTitle


class TestHtmxSearchTagNames(TestCase):
    """
    Tests for the htmx_search_tag_names view function.
    """

    def setUp(self):
        """Set up test data and request factory."""
        self.factory = RequestFactory()

        # Create test data
        self.tutorial_title = TutorialTitle.objects.create(
            title_id_slug="test-tutorial", name="Test Tutorial"
        )

        self.question = Question.objects.create(
            tutorial_title=self.tutorial_title,
            question_id_slug="test-question",
            question_text="What is a test?",
            answer_a="Option A",
            answer_b="Option B",
            answer_c="Option C",
            answer_d="Option D",
            correct_answer="a",
            difficulty="easy",
        )
        self.question.tags.add("python", "django", "testing")

    def test_non_htmx_request_returns_forbidden(self):
        """Test that non-HTMX requests return HTTP 403 Forbidden."""
        request = self.factory.get("/htmx/search-tag-names/")
        # Don't set request.htmx attribute to simulate non-HTMX request

        response = htmx_search_tag_names(request)

        self.assertIsInstance(response, HttpResponseForbidden)
        self.assertEqual(
            response.content, b"This endpoint is for HTMX requests only."
        )

    @patch("questions.views.logger")
    def test_non_htmx_request_logs_warning(self, mock_logger):
        """Test that non-HTMX requests log a warning."""
        request = self.factory.get("/htmx/search-tag-names/")

        htmx_search_tag_names(request)

        mock_logger.warning.assert_called_once_with(
            "Non-HTMX request received at htmx_search_tag_names endpoint."
        )

    def test_htmx_request_with_search_query(self):
        """Test HTMX request with search query."""
        request = self.factory.get(
            "/htmx/search-tag-names/", {"q_tag_search": "python"}
        )
        request.htmx = True

        with patch(
            "questions.views.Question.objects.search_tags"
        ) as mock_search:
            mock_search.return_value = ["python", "python-advanced"]

            response = htmx_search_tag_names(request)

            # Verify search method was called with correct parameters
            mock_search.assert_called_once_with("python", limit=15)

            # Check response
            self.assertIsInstance(
                response, HttpResponse
            )  # Correction: render() returns HttpResponse
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.context_data["tag_names"],
                ["python", "python-advanced"],
            )
            self.assertEqual(response.context_data["search_query"], "python")

    def test_htmx_request_with_empty_search_query(self):
        """Test HTMX request with empty search query."""
        request = self.factory.get(
            "/htmx/search-tag-names/", {"q_tag_search": ""}
        )
        request.htmx = True

        with patch(
            "questions.views.Question.objects.search_tags"
        ) as mock_search:
            mock_search.return_value = ["python", "django", "testing"]

            response = htmx_search_tag_names(request)

            # Empty query should be stripped to empty string
            mock_search.assert_called_once_with("", limit=15)
            self.assertEqual(response.context_data["search_query"], "")
            self.assertEqual(response.status_code, 200)

    def test_htmx_request_with_whitespace_only_query(self):
        """Test HTMX request with whitespace-only search query."""
        request = self.factory.get(
            "/htmx/search-tag-names/", {"q_tag_search": "   "}
        )
        request.htmx = True

        with patch(
            "questions.views.Question.objects.search_tags"
        ) as mock_search:
            mock_search.return_value = []

            response = htmx_search_tag_names(request)

            # Whitespace should be stripped to empty string
            mock_search.assert_called_once_with("", limit=15)
            self.assertEqual(response.context_data["search_query"], "")

    def test_htmx_request_without_search_parameter(self):
        """Test HTMX request without q_tag_search parameter."""
        request = self.factory.get("/htmx/search-tag-names/")
        request.htmx = True

        with patch(
            "questions.views.Question.objects.search_tags"
        ) as mock_search:
            mock_search.return_value = []

            response = htmx_search_tag_names(request)

            # Missing parameter should default to empty string
            mock_search.assert_called_once_with("", limit=15)
            self.assertEqual(response.context_data["search_query"], "")

    @patch("questions.views.logger")
    def test_successful_search_logs_debug_message(self, mock_logger):
        """Test that successful searches log debug information."""
        request = self.factory.get(
            "/htmx/search-tag-names/", {"q_tag_search": "django"}
        )
        request.htmx = True

        with patch(
            "questions.views.Question.objects.search_tags"
        ) as mock_search:
            # Simulate the search returning one result
            mock_search.return_value = ["django"]

            htmx_search_tag_names(request)

            # Verify the debug message includes the query and result count
            mock_logger.debug.assert_called_once_with(
                "Tag name search for 'django' returned 1 results"
            )

    @patch("questions.views.logger")
    def test_exception_during_search_is_handled_gracefully(self, mock_logger):
        """Test that an exception during the search is handled gracefully."""
        request = self.factory.get(
            "/htmx/search-tag-names/", {"q_tag_search": "fail"}
        )
        request.htmx = True

        with patch(
            "questions.views.Question.objects.search_tags"
        ) as mock_search:
            # Simulate a database error
            mock_search.side_effect = Exception("Database is offline")

            response = htmx_search_tag_names(request)

            # Verify the error was logged
            mock_logger.error.assert_called_once()

            # Check that the response is still successful but with an error message
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context_data["tag_names"], [])
            self.assertEqual(
                response.context_data["error_message"],
                "An error occurred while searching tag names.",
            )
