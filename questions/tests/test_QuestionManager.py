import random
from unittest.mock import patch
from django.test import TestCase
from questions.models import Question, TutorialTitle


class QuestionManagerTest(TestCase):
    """
    Tests for the QuestionManager custom manager.
    """

    @classmethod
    def setUpTestData(cls):
        """Set up data for the entire test class."""
        cls.tutorial1 = TutorialTitle.objects.create(
            title_id_slug="django-basics", name="Django Basics"
        )
        cls.tutorial2 = TutorialTitle.objects.create(
            title_id_slug="python-advanced", name="Python Advanced"
        )

        # Create questions
        cls.q1 = Question.objects.create(
            tutorial_title=cls.tutorial1,
            question_id_slug="q1",
            question_text="What is a model?",
        )
        cls.q1.tags.add("django", "models")

        cls.q2 = Question.objects.create(
            tutorial_title=cls.tutorial2,
            question_id_slug="q2",
            question_text="What are decorators?",
        )
        cls.q2.tags.add("python", "advanced")

        cls.q3 = Question.objects.create(
            tutorial_title=cls.tutorial2,
            question_id_slug="q3",
            question_text="What is GIL?",
        )
        cls.q3.tags.add("python", "performance")

    def test_get_queryset_returns_question_queryset(self):
        """Test that get_queryset returns an instance of QuestionQuerySet."""
        from ..querysets import QuestionQuerySet

        self.assertIsInstance(
            Question.objects.get_queryset(), QuestionQuerySet
        )

    def test_get_initial_questions_returns_tuples(self):
        """Test that get_initial_questions returns a list of (str, str) tuples."""
        questions = Question.objects.get_initial_questions(amount=3)
        self.assertEqual(len(questions), 3)
        self.assertIsInstance(questions, list)
        # Check that all expected tuples are in the results
        expected_tuples = {
            ("django-basics", "q1"),
            ("python-advanced", "q2"),
            ("python-advanced", "q3"),
        }
        actual_tuples = set(questions)
        self.assertEqual(actual_tuples, expected_tuples)

    @patch("random.shuffle")
    def test_get_initial_questions_shuffles_results(self, mock_shuffle):
        """Test that get_initial_questions calls random.shuffle."""
        Question.objects.get_initial_questions()
        mock_shuffle.assert_called_once()

    def test_get_initial_questions_handles_no_questions(self):
        """Test it returns an empty list when no questions exist."""
        Question.objects.all().delete()
        self.assertEqual(Question.objects.get_initial_questions(), [])

    def test_get_initial_tags(self):
        """Test that get_initial_tags returns a list of unique tags."""
        tags = Question.objects.get_initial_tags(amount=5)
        self.assertIsInstance(tags, list)
        self.assertEqual(len(tags), 5)
        # Check that expected tags are present
        self.assertIn("django", tags)
        self.assertIn("python", tags)

    def test_search_tags_with_query(self):
        """Test that search_tags returns tags matching a query."""
        results = Question.objects.search_tags("py")
        self.assertEqual(results, ["python"])

    def test_search_tags_case_insensitive(self):
        """Test that search is case-insensitive."""
        results = Question.objects.search_tags("DJANGO")
        self.assertEqual(results, ["django"])

    def test_search_tags_with_empty_query_calls_get_initial_tags(self):
        """Test that an empty search query falls back to get_initial_tags."""
        with patch(
            "questions.models.QuestionManager.get_initial_tags"
        ) as mock_get_initial:
            mock_get_initial.return_value = ["initial"]
            # Test with empty string
            results = Question.objects.search_tags("", limit=10)
            mock_get_initial.assert_called_once_with(10)
            self.assertEqual(results, ["initial"])
