# questions/tests/functions/test_quiz_view.py

from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.template.response import TemplateResponse

from questions.views import quiz_view
from questions.models import Question, TutorialTitle


class TestQuizView(TestCase):
    """
    Tests for the quiz_view function.
    This view renders the dedicated quiz-taking interface with URL parameter support.
    """

    def setUp(self):
        """Set up test data and request factory."""
        self.factory = RequestFactory()

        # Create test data
        self.tutorial_title = TutorialTitle.objects.create(
            title_id_slug="python-basics", name="Python Basics"
        )

        self.question1 = Question.objects.create(
            tutorial_title=self.tutorial_title,
            question_id_slug="variables-question",
            question_text="What is a variable in Python?",
            answer_a="A storage location",
            answer_b="A function",
            answer_c="A class",
            answer_d="A module",
            correct_answer="a",
            difficulty="easy",
        )
        self.question1.tags.add("python", "variables")

        self.question2 = Question.objects.create(
            tutorial_title=self.tutorial_title,
            question_id_slug="loops-question",
            question_text="Which loop is best for iterating over lists?",
            answer_a="while loop",
            answer_b="for loop",
            answer_c="do-while loop",
            answer_d="repeat-until loop",
            correct_answer="b",
            difficulty="medium",
        )
        self.question2.tags.add("python", "loops")

    def test_quiz_view_without_parameters(self):
        """Test quiz view with no URL parameters."""
        request = self.factory.get("/quiz/")

        with (
            patch(
                "questions.views.Question.objects.get_queryset"
            ) as mock_get_queryset,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
        ):
            # Mock the queryset chain
            mock_queryset = MagicMock()
            mock_interactive_questions = MagicMock()
            mock_interactive_questions.count.return_value = 2
            mock_queryset.get_interactive_quiz_questions.return_value = (
                mock_interactive_questions
            )
            mock_get_queryset.return_value = mock_queryset

            mock_get_tags.return_value = ["python", "django", "web"]
            mock_get_titles.return_value = ["python-basics", "django-intro"]

            response = quiz_view(request)

            # Verify response
            self.assertIsInstance(response, TemplateResponse)
            self.assertEqual(
                response.template_name, "questions/quiz_interface.html"
            )

            # Check context data
            context = response.context_data
            self.assertEqual(context["quiz_question_count"], 2)
            self.assertEqual(context["selected_tags"], [])
            self.assertEqual(context["selected_titles"], [])
            self.assertEqual(context["selected_difficulty"], [])

            # Verify the queryset method was called with None parameters
            mock_queryset.get_interactive_quiz_questions.assert_called_once_with(
                title_id_slugs=None,
                difficulty_levels=None,
                tag_names=None,
            )

    def test_quiz_view_with_tag_parameters(self):
        """Test quiz view with tag parameters."""
        request = self.factory.get("/quiz/?tags=python,django")

        with (
            patch(
                "questions.views.Question.objects.get_queryset"
            ) as mock_get_queryset,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
        ):
            # Mock the queryset chain
            mock_queryset = MagicMock()
            mock_interactive_questions = MagicMock()
            mock_interactive_questions.count.return_value = 1
            mock_queryset.get_interactive_quiz_questions.return_value = (
                mock_interactive_questions
            )
            mock_get_queryset.return_value = mock_queryset

            mock_get_tags.return_value = ["python", "django", "web"]
            mock_get_titles.return_value = ["python-basics", "django-intro"]

            response = quiz_view(request)

            # Check context data
            context = response.context_data
            self.assertEqual(context["selected_tags"], ["python", "django"])
            self.assertEqual(context["quiz_question_count"], 1)

            # Verify the queryset method was called with correct tag parameters
            mock_queryset.get_interactive_quiz_questions.assert_called_once_with(
                title_id_slugs=None,
                difficulty_levels=None,
                tag_names=["python", "django"],
            )

    def test_quiz_view_with_title_parameters(self):
        """Test quiz view with title parameters."""
        request = self.factory.get("/quiz/?titles=python-basics,django-intro")

        with (
            patch(
                "questions.views.Question.objects.get_queryset"
            ) as mock_get_queryset,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
        ):
            # Mock the queryset chain
            mock_queryset = MagicMock()
            mock_interactive_questions = MagicMock()
            mock_interactive_questions.count.return_value = 3
            mock_queryset.get_interactive_quiz_questions.return_value = (
                mock_interactive_questions
            )
            mock_get_queryset.return_value = mock_queryset

            mock_get_tags.return_value = ["python", "django"]
            mock_get_titles.return_value = ["python-basics", "django-intro"]

            response = quiz_view(request)

            # Check context data
            context = response.context_data
            self.assertEqual(
                context["selected_titles"], ["python-basics", "django-intro"]
            )
            self.assertEqual(context["quiz_question_count"], 3)

            # Verify the queryset method was called with correct title parameters
            mock_queryset.get_interactive_quiz_questions.assert_called_once_with(
                title_id_slugs=["python-basics", "django-intro"],
                difficulty_levels=None,
                tag_names=None,
            )

    def test_quiz_view_with_difficulty_parameters(self):
        """Test quiz view with difficulty parameters."""
        request = self.factory.get("/quiz/?difficulty=easy,medium")

        with (
            patch(
                "questions.views.Question.objects.get_queryset"
            ) as mock_get_queryset,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
        ):
            # Mock the queryset chain
            mock_queryset = MagicMock()
            mock_interactive_questions = MagicMock()
            mock_interactive_questions.count.return_value = 5
            mock_queryset.get_interactive_quiz_questions.return_value = (
                mock_interactive_questions
            )
            mock_get_queryset.return_value = mock_queryset

            mock_get_tags.return_value = ["python", "django"]
            mock_get_titles.return_value = ["python-basics"]

            response = quiz_view(request)

            # Check context data
            context = response.context_data
            self.assertEqual(
                context["selected_difficulty"], ["easy", "medium"]
            )
            self.assertEqual(context["quiz_question_count"], 5)

            # Verify the queryset method was called with correct difficulty parameters
            mock_queryset.get_interactive_quiz_questions.assert_called_once_with(
                title_id_slugs=None,
                difficulty_levels=["easy", "medium"],
                tag_names=None,
            )

    def test_quiz_view_with_all_parameters(self):
        """Test quiz view with all parameter types."""
        request = self.factory.get(
            "/quiz/?tags=python,django&titles=python-basics&difficulty=easy,hard"
        )

        with (
            patch(
                "questions.views.Question.objects.get_queryset"
            ) as mock_get_queryset,
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
            # Mock the queryset chain
            mock_queryset = MagicMock()
            mock_interactive_questions = MagicMock()
            mock_interactive_questions.count.return_value = 2
            mock_queryset.get_interactive_quiz_questions.return_value = (
                mock_interactive_questions
            )
            mock_get_queryset.return_value = mock_queryset

            mock_get_tags.return_value = ["python", "django", "web"]
            mock_get_titles.return_value = ["python-basics", "django-intro"]
            mock_generate_name.side_effect = lambda slug: slug.replace(
                "-", " "
            ).title()

            response = quiz_view(request)

            # Check context data
            context = response.context_data
            self.assertEqual(context["selected_tags"], ["python", "django"])
            self.assertEqual(context["selected_titles"], ["python-basics"])
            self.assertEqual(context["selected_difficulty"], ["easy", "hard"])
            self.assertEqual(context["quiz_question_count"], 2)

            # Verify the queryset method was called with all parameters
            mock_queryset.get_interactive_quiz_questions.assert_called_once_with(
                title_id_slugs=["python-basics"],
                difficulty_levels=["easy", "hard"],
                tag_names=["python", "django"],
            )

    def test_quiz_view_with_empty_parameters(self):
        """Test quiz view with empty parameter values."""
        request = self.factory.get("/quiz/?tags=&titles=&difficulty=")

        with (
            patch(
                "questions.views.Question.objects.get_queryset"
            ) as mock_get_queryset,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
        ):
            # Mock the queryset chain
            mock_queryset = MagicMock()
            mock_interactive_questions = MagicMock()
            mock_interactive_questions.count.return_value = 0
            mock_queryset.get_interactive_quiz_questions.return_value = (
                mock_interactive_questions
            )
            mock_get_queryset.return_value = mock_queryset

            mock_get_tags.return_value = []
            mock_get_titles.return_value = []

            response = quiz_view(request)

            # Check context data - empty parameters should result in empty lists
            context = response.context_data
            self.assertEqual(context["selected_tags"], [])
            self.assertEqual(context["selected_titles"], [])
            self.assertEqual(context["selected_difficulty"], [])

            # Verify the queryset method was called with None parameters
            mock_queryset.get_interactive_quiz_questions.assert_called_once_with(
                title_id_slugs=None,
                difficulty_levels=None,
                tag_names=None,
            )

    def test_quiz_view_with_whitespace_parameters(self):
        """Test quiz view handles whitespace in parameters correctly."""
        request = self.factory.get(
            "/quiz/?tags= python , django &titles= python-basics "
        )

        with (
            patch(
                "questions.views.Question.objects.get_queryset"
            ) as mock_get_queryset,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
        ):
            # Mock the queryset chain
            mock_queryset = MagicMock()
            mock_interactive_questions = MagicMock()
            mock_interactive_questions.count.return_value = 1
            mock_queryset.get_interactive_quiz_questions.return_value = (
                mock_interactive_questions
            )
            mock_get_queryset.return_value = mock_queryset

            mock_get_tags.return_value = ["python", "django"]
            mock_get_titles.return_value = ["python-basics"]

            response = quiz_view(request)

            # Check that whitespace is properly stripped
            context = response.context_data
            self.assertEqual(context["selected_tags"], ["python", "django"])
            self.assertEqual(context["selected_titles"], ["python-basics"])

            # Verify the queryset method was called with trimmed parameters
            mock_queryset.get_interactive_quiz_questions.assert_called_once_with(
                title_id_slugs=["python-basics"],
                difficulty_levels=None,
                tag_names=["python", "django"],
            )

    @patch("questions.views.logger")
    def test_quiz_view_exception_handling(self, mock_logger):
        """Test that exceptions during quiz data loading are handled gracefully."""
        request = self.factory.get("/quiz/?tags=python")

        with (
            patch(
                "questions.views.Question.objects.get_queryset"
            ) as mock_get_queryset,
        ):
            # Trigger an exception during quiz question loading
            mock_get_queryset.side_effect = Exception(
                "Database connection error"
            )

            response = quiz_view(request)

            # Response should still be successful with fallback data
            self.assertIsInstance(response, TemplateResponse)
            context = response.context_data

            # Should have empty queryset and fallback values
            self.assertEqual(context["quiz_question_count"], 0)
            self.assertEqual(context["initial_tags"], [])
            self.assertEqual(context["initial_title_ids"], [])
            self.assertEqual(context["initial_title_names"], [])

            # Verify error was logged
            mock_logger.error.assert_called_once()

    def test_context_structure_completeness(self):
        """Test that all required context variables are present."""
        request = self.factory.get("/quiz/")

        with (
            patch(
                "questions.views.Question.objects.get_queryset"
            ) as mock_get_queryset,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
        ):
            # Mock the queryset chain
            mock_queryset = MagicMock()
            mock_interactive_questions = MagicMock()
            mock_interactive_questions.count.return_value = 0
            mock_queryset.get_interactive_quiz_questions.return_value = (
                mock_interactive_questions
            )
            mock_get_queryset.return_value = mock_queryset

            mock_get_tags.return_value = []
            mock_get_titles.return_value = []

            response = quiz_view(request)

            # Check all required context keys are present
            required_keys = {
                "quiz_questions",
                "quiz_question_count",
                "selected_tags",
                "selected_titles",
                "selected_difficulty",
                "initial_tags",
                "initial_title_ids",
                "initial_title_names",
            }

            self.assertTrue(
                required_keys.issubset(response.context_data.keys())
            )

    def test_template_name_is_correct(self):
        """Test that the correct template is used for quiz interface."""
        request = self.factory.get("/quiz/")

        with (
            patch(
                "questions.views.Question.objects.get_queryset"
            ) as mock_get_queryset,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
        ):
            # Mock the queryset chain
            mock_queryset = MagicMock()
            mock_interactive_questions = MagicMock()
            mock_interactive_questions.count.return_value = 0
            mock_queryset.get_interactive_quiz_questions.return_value = (
                mock_interactive_questions
            )
            mock_get_queryset.return_value = mock_queryset

            mock_get_tags.return_value = []
            mock_get_titles.return_value = []

            response = quiz_view(request)

            self.assertEqual(
                response.template_name, "questions/quiz_interface.html"
            )

    def test_parameter_parsing_edge_cases(self):
        """Test edge cases in parameter parsing."""
        # Test with commas but no actual values
        request = self.factory.get("/quiz/?tags=,,,&difficulty=,")

        with (
            patch(
                "questions.views.Question.objects.get_queryset"
            ) as mock_get_queryset,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
        ):
            # Mock the queryset chain
            mock_queryset = MagicMock()
            mock_interactive_questions = MagicMock()
            mock_interactive_questions.count.return_value = 0
            mock_queryset.get_interactive_quiz_questions.return_value = (
                mock_interactive_questions
            )
            mock_get_queryset.return_value = mock_queryset

            mock_get_tags.return_value = []
            mock_get_titles.return_value = []

            response = quiz_view(request)

            # Should result in empty lists, not lists with empty strings
            context = response.context_data
            self.assertEqual(context["selected_tags"], [])
            self.assertEqual(context["selected_difficulty"], [])

    def test_debug_logging_for_parameters(self):
        """Test that debug logging captures parameter information."""
        request = self.factory.get(
            "/quiz/?tags=python&titles=basics&difficulty=easy"
        )

        with (
            patch(
                "questions.views.Question.objects.get_queryset"
            ) as mock_get_queryset,
            patch(
                "questions.views.Question.objects.get_initial_tags"
            ) as mock_get_tags,
            patch(
                "questions.views.TutorialTitle.objects.get_initial_titles"
            ) as mock_get_titles,
            patch("questions.views.logger") as mock_logger,
        ):
            # Mock the queryset chain
            mock_queryset = MagicMock()
            mock_interactive_questions = MagicMock()
            mock_interactive_questions.count.return_value = 1
            mock_queryset.get_interactive_quiz_questions.return_value = (
                mock_interactive_questions
            )
            mock_get_queryset.return_value = mock_queryset

            mock_get_tags.return_value = ["python"]
            mock_get_titles.return_value = ["basics"]

            response = quiz_view(request)

            # Verify debug logging was called with parameter information
            mock_logger.debug.assert_called_once()
            debug_call_args = mock_logger.debug.call_args[0][0]
            self.assertIn("Quiz view params:", debug_call_args)
            self.assertIn("tags=['python']", debug_call_args)
            self.assertIn("titles=['basics']", debug_call_args)
            self.assertIn("difficulty=['easy']", debug_call_args)
