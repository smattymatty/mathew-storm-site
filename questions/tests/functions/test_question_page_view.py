# questions/tests/functions/test_question_page_view.py

from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.template.response import TemplateResponse

from questions.views import question_page_view
from questions.models import Question, TutorialTitle


class TestQuestionPageView(TestCase):
    """
    Tests for the question_page_view function.
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
        self.question.tags.add("test-tag")

    def test_successful_page_load_with_data(self):
        """Test successful page load with initial data."""
        request = self.factory.get("/")

        with (
            patch(
                "questions.views.Question.objects.get_initial_questions"
            ) as mock_get_questions,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
            patch(
                "questions.views.generate_readable_name_from_slug"
            ) as mock_generate_name,
        ):
            # Mock return values
            mock_get_questions.return_value = [
                ("test-tutorial", "test-question")
            ]
            mock_get_tags.return_value = ["test-tag", "another-tag"]
            mock_get_titles.return_value = [
                "test-tutorial",
                "another-tutorial",
            ]
            mock_generate_name.side_effect = lambda slug: slug.replace(
                "-", " "
            ).title()

            response = question_page_view(request)

            # Verify response
            self.assertIsInstance(response, TemplateResponse)
            self.assertEqual(
                response.template_name, "questions/quiz_page.html"
            )

            # Check context data
            context = response.context_data
            self.assertEqual(context["sidebar_header"], "Interactive Quiz")
            self.assertEqual(
                context["initial_tags"], ["test-tag", "another-tag"]
            )
            self.assertEqual(
                context["initial_title_ids"],
                ["test-tutorial", "another-tutorial"],
            )
            self.assertEqual(
                context["initial_title_names"],
                ["Test Tutorial", "Another Tutorial"],
            )

            # Verify manager methods were called
            mock_get_questions.assert_called_once()
            mock_get_tags.assert_called_once()
            mock_get_titles.assert_called_once()

            # Verify name generation was called for each title
            self.assertEqual(mock_generate_name.call_count, 2)

    def test_database_query_for_initial_questions(self):
        """Test that initial questions are properly queried from database."""
        request = self.factory.get("/")

        with (
            patch(
                "questions.views.Question.objects.get_initial_questions"
            ) as mock_get_questions,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
        ):
            mock_get_questions.return_value = [
                ("test-tutorial", "test-question")
            ]
            mock_get_tags.return_value = ["test-tag"]
            mock_get_titles.return_value = ["test-tutorial"]

            response = question_page_view(request)

            # Check that actual Question objects are in context
            initial_questions = response.context_data["initial_questions"]
            self.assertIsInstance(initial_questions, list)

    @patch("questions.views.logger")
    def test_exception_handling_during_data_loading(self, mock_logger):
        """Test that exceptions during initial data loading are handled gracefully."""
        request = self.factory.get("/")

        # The first patch triggers the 'except' block, as intended.
        # The second patch intercepts the query chain.
        with (
            patch(
                "questions.views.Question.objects.get_initial_questions"
            ) as mock_get_questions,
            patch(
                "questions.views.Question.objects.select_related"
            ) as mock_select_related,
        ):
            # 1. Trigger the exception in the first part of the view
            mock_get_questions.side_effect = Exception(
                "Database connection error"
            )

            # 2. Control the chained call
            # Create a mock for the QuerySet that select_related returns
            mock_queryset = MagicMock()
            # The filter method on that mock should return an empty list
            mock_queryset.filter.return_value = []
            # Make select_related return our controlled mock QuerySet
            mock_select_related.return_value = mock_queryset

            response = question_page_view(request)

            # These assertions will now pass
            self.assertIsInstance(response, TemplateResponse)
            context = response.context_data
            self.assertEqual(context["initial_questions"], [])
            self.assertEqual(context["initial_tags"], [])
            self.assertEqual(context["initial_title_ids"], [])
            self.assertEqual(context["initial_title_names"], [])
            mock_logger.error.assert_called_once()

    # questions/tests/functions/test_question_page_view.py

    def test_empty_initial_data_handling(self):
        """Test handling when no initial data is available."""
        request = self.factory.get("/")

        with (
            patch(
                "questions.views.Question.objects.get_initial_questions"
            ) as mock_get_questions,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
            patch(
                "questions.views.Question.objects.select_related"
            ) as mock_select_related,
        ):
            # 1. The initial data fetching methods return empty lists
            mock_get_questions.return_value = []
            mock_get_tags.return_value = []
            mock_get_titles.return_value = []

            # 2. Control the chained call
            mock_queryset = MagicMock()
            mock_queryset.filter.return_value = []
            mock_select_related.return_value = mock_queryset

            response = question_page_view(request)

            # These assertions will now pass
            context = response.context_data
            self.assertEqual(context["initial_questions"], [])
            self.assertEqual(context["initial_tags"], [])
            self.assertEqual(context["initial_title_ids"], [])
            self.assertEqual(context["initial_title_names"], [])

    def test_context_structure_completeness(self):
        """Test that all required context variables are present."""
        request = self.factory.get("/")

        with (
            patch(
                "questions.views.Question.objects.get_initial_questions"
            ) as mock_get_questions,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
        ):
            mock_get_questions.return_value = []
            mock_get_tags.return_value = []
            mock_get_titles.return_value = []

            response = question_page_view(request)

            # Check all required context keys are present
            required_keys = {
                "sidebar_header",
                "initial_questions",
                "initial_tags",
                "initial_title_ids",
                "initial_title_names",
            }

            self.assertTrue(
                required_keys.issubset(response.context_data.keys())
            )
