# questions/tests/test_TutorialTitle.py
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from ..models import TutorialTitle, Question, QuestionAttempt, TutorialStats


User = get_user_model()


class TutorialTitleModelTest(TestCase):
    """Test cases for the TutorialTitle model."""

    def setUp(self):
        """Set up test data."""
        self.tutorial_data = {
            "title_id_slug": "python-basics",
            "name": "Python Basics Tutorial",
        }
        self.tutorial = TutorialTitle.objects.create(**self.tutorial_data)

    def test_tutorial_title_creation(self):
        """Test that TutorialTitle objects are created correctly."""
        self.assertEqual(self.tutorial.title_id_slug, "python-basics")
        self.assertEqual(self.tutorial.name, "Python Basics Tutorial")
        self.assertIsInstance(self.tutorial, TutorialTitle)

    def test_tutorial_title_creation_without_name(self):
        """Test TutorialTitle creation with only slug."""
        tutorial = TutorialTitle.objects.create(
            title_id_slug="django-advanced"
        )
        self.assertEqual(tutorial.title_id_slug, "django-advanced")
        self.assertEqual(tutorial.name, "")

    def test_title_id_slug_is_primary_key(self):
        """Test that title_id_slug serves as primary key."""
        self.assertEqual(self.tutorial.pk, "python-basics")

    def test_title_id_slug_unique_constraint(self):
        """Test that title_id_slug must be unique."""
        with self.assertRaises(Exception):
            TutorialTitle.objects.create(
                title_id_slug="python-basics", name="Duplicate Tutorial"
            )

    def test_str_method_with_name(self):
        """Test __str__ method when name is provided."""
        expected = "Python Basics Tutorial"
        self.assertEqual(str(self.tutorial), expected)

    def test_str_method_without_name(self):
        """Test __str__ method when name is empty."""
        tutorial = TutorialTitle.objects.create(
            title_id_slug="no-name-tutorial"
        )
        expected = "no-name-tutorial"
        self.assertEqual(str(tutorial), expected)

    def test_str_method_with_blank_name(self):
        """Test __str__ method when name is blank."""
        tutorial = TutorialTitle.objects.create(
            title_id_slug="blank-name-tutorial", name=""
        )
        expected = "blank-name-tutorial"
        self.assertEqual(str(tutorial), expected)

    def test_meta_verbose_names(self):
        """Test model meta verbose names."""
        self.assertEqual(TutorialTitle._meta.verbose_name, "Tutorial Title")
        self.assertEqual(
            TutorialTitle._meta.verbose_name_plural, "Tutorial Titles"
        )

    def test_help_text_attributes(self):
        """Test that help text is properly set."""
        title_slug_field = TutorialTitle._meta.get_field("title_id_slug")
        name_field = TutorialTitle._meta.get_field("name")

        self.assertEqual(
            title_slug_field.help_text,
            "The unique slug for the tutorial title",
        )
        self.assertEqual(
            name_field.help_text, "A human-readable name for the tutorial"
        )

    def test_field_constraints(self):
        """Test field constraints and properties."""
        title_slug_field = TutorialTitle._meta.get_field("title_id_slug")
        name_field = TutorialTitle._meta.get_field("name")

        # title_id_slug constraints
        self.assertEqual(title_slug_field.max_length, 100)
        self.assertTrue(title_slug_field.unique)
        self.assertTrue(title_slug_field.primary_key)

        # name field constraints
        self.assertEqual(name_field.max_length, 255)
        self.assertTrue(name_field.blank)

    def test_update_tutorial_stats_with_no_attempts(self):
        """Test update_tutorial_stats when no attempts exist."""
        self.tutorial.update_tutorial_stats()

        # Should create TutorialStats with default values
        self.assertTrue(hasattr(self.tutorial, "stats"))
        stats = self.tutorial.stats
        self.assertEqual(stats.total_attempts, 0)
        self.assertEqual(stats.total_completions, 0)
        self.assertEqual(stats.completion_rate, Decimal("0.00"))
        self.assertEqual(stats.average_score, Decimal("0.00"))

    def test_update_tutorial_stats_with_attempts(self):
        """Test update_tutorial_stats with existing attempts."""
        # Create a user and question
        user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        question = Question.objects.create(
            tutorial_title=self.tutorial,
            question_id_slug="test-question",
            question_text="Test question?",
            answer_a="Option A",
            answer_b="Option B",
            answer_c="Option C",
            answer_d="Option D",
            correct_answer="a",
        )

        # Create question attempts
        QuestionAttempt.objects.create(
            user=user, question=question, selected_answer="a", is_correct=True
        )
        QuestionAttempt.objects.create(
            user=user, question=question, selected_answer="b", is_correct=False
        )

        self.tutorial.update_tutorial_stats()

        stats = self.tutorial.stats
        self.assertEqual(stats.total_attempts, 1)  # One unique user
        self.assertGreater(stats.average_score, 0)

    def test_update_tutorial_stats_creates_stats_if_not_exists(self):
        """Test that update_tutorial_stats creates TutorialStats if it doesn't exist."""
        # Ensure no stats exist initially
        self.assertFalse(hasattr(self.tutorial, "stats"))

        self.tutorial.update_tutorial_stats()

        # Should now have stats
        self.assertTrue(hasattr(self.tutorial, "stats"))
        self.assertIsInstance(self.tutorial.stats, TutorialStats)

    def test_update_tutorial_stats_updates_existing_stats(self):
        """Test that update_tutorial_stats updates existing TutorialStats."""
        # Create initial stats
        initial_stats = TutorialStats.objects.create(
            tutorial_title=self.tutorial,
            total_attempts=5,
            average_score=Decimal("75.00"),
        )

        self.tutorial.update_tutorial_stats()

        # Stats should be updated
        updated_stats = TutorialStats.objects.get(tutorial_title=self.tutorial)
        self.assertEqual(updated_stats.id, initial_stats.id)  # Same object

    def test_update_tutorial_stats_with_multiple_users(self):
        """Test update_tutorial_stats with multiple users."""
        # Create users and questions
        user1 = User.objects.create_user(username="user1", password="pass1")
        user2 = User.objects.create_user(username="user2", password="pass2")

        question = Question.objects.create(
            tutorial_title=self.tutorial,
            question_id_slug="multi-user-question",
            question_text="Multi user question?",
            answer_a="A",
            answer_b="B",
            answer_c="C",
            answer_d="D",
            correct_answer="a",
        )

        # Create attempts for both users
        QuestionAttempt.objects.create(
            user=user1, question=question, selected_answer="a", is_correct=True
        )
        QuestionAttempt.objects.create(
            user=user2,
            question=question,
            selected_answer="b",
            is_correct=False,
        )

        self.tutorial.update_tutorial_stats()

        stats = self.tutorial.stats
        self.assertEqual(stats.total_attempts, 2)  # Two unique users

    def test_related_name_questions(self):
        """Test that the related_name 'questions' works correctly."""
        # Create some questions
        question1 = Question.objects.create(
            tutorial_title=self.tutorial,
            question_id_slug="related-question-1",
            question_text="Related question 1?",
            answer_a="A",
            answer_b="B",
            answer_c="C",
            answer_d="D",
            correct_answer="a",
        )
        question2 = Question.objects.create(
            tutorial_title=self.tutorial,
            question_id_slug="related-question-2",
            question_text="Related question 2?",
            answer_a="A",
            answer_b="B",
            answer_c="C",
            answer_d="D",
            correct_answer="b",
        )

        # Test related manager
        questions = self.tutorial.questions.all()
        self.assertEqual(questions.count(), 2)
        self.assertIn(question1, questions)
        self.assertIn(question2, questions)

    def test_tutorial_title_manager(self):
        """Test that custom TutorialTitleManager is properly assigned."""
        from ..managers import TutorialTitleManager

        self.assertIsInstance(TutorialTitle.objects, TutorialTitleManager)
