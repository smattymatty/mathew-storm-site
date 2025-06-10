# questions/tests/functions/test_htmx_search_tutorial_titles.py

from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.http import HttpResponseForbidden
from django.template.response import TemplateResponse

from questions.views import htmx_search_tutorial_titles
from questions.models import TutorialTitle


class TestHtmxSearchTutorialTitles(TestCase):
    """
    Tests for the htmx_search_tutorial_titles view function.
    """

    def setUp(self):
        """Set up test data and request factory."""
        self.factory = RequestFactory()

        # Create test data
        self.tutorial1 = TutorialTitle.objects.create(
            title_id_slug="first-tutorial", name="First Tutorial"
        )
        self.tutorial2 = TutorialTitle.objects.create(
            title_id_slug="second-tutorial", name="Second Tutorial"
        )

    def test_non_htmx_request_returns_forbidden(self):
        """Test that non-HTMX requests return HTTP 403 Forbidden."""
        request = self.factory.get("/htmx/search-tutorial-titles/")
        # Don't set request.htmx attribute to simulate non-HTMX request

        response = htmx_search_tutorial_titles(request)

        self.assertIsInstance(response, HttpResponseForbidden)
        self.assertEqual(
            response.content, b"This endpoint is for HTMX requests only."
        )

    @patch("questions.views.logger")
    def test_non_htmx_request_logs_warning(self, mock_logger):
        """Test that non-HTMX requests log a warning."""
        request = self.factory.get("/htmx/search-tutorial-titles/")

        htmx_search_tutorial_titles(request)

        mock_logger.warning.assert_called_once_with(
            "Non-HTMX request received at htmx_search_tutorial_titles endpoint."
        )

    def test_htmx_request_with_search_query(self):
        """Test HTMX request with search query."""
        request = self.factory.get(
            "/htmx/search-tutorial-titles/", {"q_search": "first"}
        )
        request.htmx = True

        with patch(
            "questions.views.TutorialTitle.objects.search_titles"
        ) as mock_search:
            mock_search.return_value = ["First Tutorial"]

            response = htmx_search_tutorial_titles(request)

            # Verify search method was called with correct parameters
            mock_search.assert_called_once_with("first", limit=15)

            # Check response
            self.assertIsInstance(response, TemplateResponse)
            self.assertEqual(
                response.template_name,
                "questions/partials/pills/_tutorial_pills_container.html",
            )
            self.assertEqual(
                response.context_data["tutorial_titles"], ["First Tutorial"]
            )
            self.assertEqual(response.context_data["search_query"], "first")

    def test_htmx_request_with_empty_search_query(self):
        """Test HTMX request with empty search query."""
        request = self.factory.get(
            "/htmx/search-tutorial-titles/", {"q_search": ""}
        )
        request.htmx = True

        with patch(
            "questions.views.TutorialTitle.objects.search_titles"
        ) as mock_search:
            mock_search.return_value = ["First Tutorial", "Second Tutorial"]

            response = htmx_search_tutorial_titles(request)

            # Empty query should be stripped to empty string
            mock_search.assert_called_once_with("", limit=15)

            self.assertEqual(response.context_data["search_query"], "")

    def test_htmx_request_with_whitespace_only_query(self):
        """Test HTMX request with whitespace-only search query."""
        request = self.factory.get(
            "/htmx/search-tutorial-titles/", {"q_search": "   "}
        )
        request.htmx = True

        with patch(
            "questions.views.TutorialTitle.objects.search_titles"
        ) as mock_search:
            mock_search.return_value = []

            response = htmx_search_tutorial_titles(request)

            # Whitespace should be stripped to empty string
            mock_search.assert_called_once_with("", limit=15)
            self.assertEqual(response.context_data["search_query"], "")

    def test_htmx_request_without_search_parameter(self):
        """Test HTMX request without q_search parameter."""
        request = self.factory.get("/htmx/search-tutorial-titles/")
        request.htmx = True

        with patch(
            "questions.views.TutorialTitle.objects.search_titles"
        ) as mock_search:
            mock_search.return_value = []

            response = htmx_search_tutorial_titles(request)

            # Missing parameter should default to empty string
            mock_search.assert_called_once_with("", limit=15)
            self.assertEqual(response.context_data["search_query"], "")

    @patch("questions.views.logger")
    def test_successful_search_logs_debug_message(self, mock_logger):
        """Test that successful searches log debug information."""
        request = self.factory.get(
            "/htmx/search-tutorial-titles/", {"q_search": "tutorial"}
        )
        request.htmx = True

        with patch(
            "questions.views.TutorialTitle.objects.search_titles"
        ) as mock_search:
            mock_search.return_value = ["First Tutorial", "Second Tutorial"]

            htmx_search_tutorial_titles(request)

            # Verify debug logging
            mock_logger.debug.assert_called_once_with(
                "Tutorial title search for 'tutorial' returned 2 results"
            )

    @patch("questions.views.logger")
    def test_search_exception_handling(self, mock_logger):
        """Test that search exceptions are handled gracefully."""
        request = self.factory.get(
            "/htmx/search-tutorial-titles/", {"q_search": "test"}
        )
        request.htmx = True

        with patch(
            "questions.views.TutorialTitle.objects.search_titles"
        ) as mock_search:
            mock_search.side_effect = Exception("Database error")

            response = htmx_search_tutorial_titles(request)

            # Check error handling
            self.assertIsInstance(response, TemplateResponse)
            context = response.context_data
            self.assertEqual(context["tutorial_titles"], [])
            self.assertEqual(context["search_query"], "test")
            self.assertEqual(
                context["error_message"],
                "An error occurred while searching tutorial titles.",
            )

            # Verify error logging
            mock_logger.error.assert_called_once()

    def test_context_data_structure(self):
        """Test that response context contains all required keys."""
        request = self.factory.get(
            "/htmx/search-tutorial-titles/", {"q_search": "test"}
        )
        request.htmx = True

        with patch(
            "questions.views.TutorialTitle.objects.search_titles"
        ) as mock_search:
            mock_search.return_value = ["Test Tutorial"]

            response = htmx_search_tutorial_titles(request)

            # Check required context keys
            required_keys = {"tutorial_titles", "search_query"}
            self.assertTrue(
                required_keys.issubset(response.context_data.keys())
            )

            # Verify no error_message in successful case
            self.assertNotIn("error_message", response.context_data)

    def test_search_query_case_sensitivity(self):
        """Test that search queries are passed as-is to the search method."""
        test_queries = ["TUTORIAL", "Tutorial", "tutorial", "TuToRiAl"]

        for query in test_queries:
            with self.subTest(query=query):
                request = self.factory.get(
                    "/htmx/search-tutorial-titles/", {"q_search": query}
                )
                request.htmx = True

                with patch(
                    "questions.views.TutorialTitle.objects.search_titles"
                ) as mock_search:
                    mock_search.return_value = []

                    response = htmx_search_tutorial_titles(request)

                    # Query should be passed as-is (case preserved)
                    mock_search.assert_called_once_with(query, limit=15)
                    self.assertEqual(
                        response.context_data["search_query"], query
                    )

    def test_search_limit_parameter(self):
        """Test that search limit is correctly set."""
        request = self.factory.get(
            "/htmx/search-tutorial-titles/", {"q_search": "test"}
        )
        request.htmx = True

        with patch(
            "questions.views.TutorialTitle.objects.search_titles"
        ) as mock_search:
            mock_search.return_value = []

            htmx_search_tutorial_titles(request)

            # Verify limit parameter
            mock_search.assert_called_once_with("test", limit=15)
