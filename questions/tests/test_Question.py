# questions/tests/test_Question.py
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import transaction
from unittest.mock import patch

from ..models import Question, TutorialTitle, QuestionAttempt, QuestionStats


User = get_user_model()


class QuestionModelTest(TestCase):
    """Test cases for the Question model."""

    def setUp(self):
        """Set up test data."""
        self.tutorial = TutorialTitle.objects.create(
            title_id_slug="test-tutorial", name="Test Tutorial"
        )
        self.question_data = {
            "tutorial_title": self.tutorial,
            "question_id_slug": "test-question",
            "question_text": "What is the capital of France?",
            "answer_a": "London",
            "answer_b": "Berlin",
            "answer_c": "Paris",
            "answer_d": "Madrid",
            "correct_answer": "c",
            "difficulty": Question.Difficulty.EASY,
        }
        self.question = Question.objects.create(**self.question_data)
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )

    def test_question_creation(self):
        """Test that Question objects are created correctly."""
        self.assertEqual(self.question.tutorial_title, self.tutorial)
        self.assertEqual(self.question.question_id_slug, "test-question")
        self.assertEqual(
            self.question.question_text, "What is the capital of France?"
        )
        self.assertEqual(self.question.correct_answer, "c")
        self.assertEqual(self.question.difficulty, Question.Difficulty.EASY)

    def test_question_str_method(self):
        """Test Question __str__ method."""
        expected = (
            "test-tutorial | test-question | What is the capital of France?"
        )
        self.assertEqual(str(self.question), expected)

    def test_question_str_method_long_text(self):
        """Test __str__ method with long question text."""
        long_question = Question.objects.create(
            tutorial_title=self.tutorial,
            question_id_slug="long-question",
            question_text="This is a very long question text that exceeds 75 characters and should be truncated",
            answer_a="A",
            answer_b="B",
            answer_c="C",
            answer_d="D",
            correct_answer="a",
        )
        result = str(long_question)
        self.assertTrue(result.endswith("..."))
        self.assertEqual(len(result.split(" | ")[2]), 78)  # 75 + '...'

    def test_difficulty_choices(self):
        """Test that difficulty choices are properly defined."""
        expected_choices = [
            ("foundational", "Foundational"),
            ("easy", "Easy"),
            ("medium", "Medium"),
            ("hard", "Hard"),
            ("impossible", "Impossible"),
        ]
        self.assertEqual(Question.Difficulty.choices, expected_choices)

    def test_answer_choices(self):
        """Test that answer choices are properly defined."""
        expected_choices = [("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")]
        self.assertEqual(Question.AnswerChoice.choices, expected_choices)

    def test_unique_together_constraint(self):
        """Test that tutorial_title and question_id_slug must be unique together."""
        with self.assertRaises(Exception):
            Question.objects.create(
                tutorial_title=self.tutorial,
                question_id_slug="test-question",  # Same slug as existing
                question_text="Different question?",
                answer_a="A",
                answer_b="B",
                answer_c="C",
                answer_d="D",
                correct_answer="a",
            )

    def test_retrieve_answer_correct(self):
        """Test retrieve_answer method with correct answer."""
        result = self.question.retrieve_answer(
            selected_answer="c", user=self.user, time_spent_seconds=30
        )

        self.assertTrue(result["is_correct"])
        self.assertEqual(result["correct_answer"], "c")
        self.assertEqual(result["attempt_number"], 1)
        self.assertTrue(result["stats_updated"])
        self.assertIn("attempt_id", result)

    def test_retrieve_answer_incorrect(self):
        """Test retrieve_answer method with incorrect answer."""
        result = self.question.retrieve_answer(
            selected_answer="a", user=self.user, time_spent_seconds=45
        )

        self.assertFalse(result["is_correct"])
        self.assertEqual(result["correct_answer"], "c")
        self.assertEqual(result["attempt_number"], 1)

    def test_retrieve_answer_anonymous_user(self):
        """Test retrieve_answer method with anonymous user."""
        result = self.question.retrieve_answer(
            selected_answer="c", user=None, time_spent_seconds=20
        )

        self.assertTrue(result["is_correct"])
        self.assertEqual(result["attempt_number"], 1)

        # Check that attempt was created without user
        attempt = QuestionAttempt.objects.get(id=result["attempt_id"])
        self.assertIsNone(attempt.user)

    def test_retrieve_answer_invalid_choice(self):
        """Test retrieve_answer method with invalid answer choice."""
        with self.assertRaises(ValueError) as context:
            self.question.retrieve_answer(
                selected_answer="e",  # Invalid choice
                user=self.user,
            )

        self.assertIn("Invalid answer choice: e", str(context.exception))

    def test_retrieve_answer_attempt_numbering(self):
        """Test that attempt numbers increment correctly."""
        # First attempt
        result1 = self.question.retrieve_answer("a", user=self.user)
        self.assertEqual(result1["attempt_number"], 1)

        # Second attempt
        result2 = self.question.retrieve_answer("b", user=self.user)
        self.assertEqual(result2["attempt_number"], 2)

        # Third attempt
        result3 = self.question.retrieve_answer("c", user=self.user)
        self.assertEqual(result3["attempt_number"], 3)

    def test_retrieve_answer_case_insensitive(self):
        """Test that retrieve_answer handles case insensitive answers."""
        result = self.question.retrieve_answer(
            selected_answer="C",  # Uppercase
            user=self.user,
        )

        self.assertTrue(result["is_correct"])

        # Check that attempt was stored in lowercase
        attempt = QuestionAttempt.objects.get(id=result["attempt_id"])
        self.assertEqual(attempt.selected_answer, "c")

    def test_retrieve_answer_creates_attempt(self):
        """Test that retrieve_answer creates QuestionAttempt record."""
        initial_count = QuestionAttempt.objects.count()

        result = self.question.retrieve_answer(
            "c", user=self.user, time_spent_seconds=60
        )

        self.assertEqual(QuestionAttempt.objects.count(), initial_count + 1)

        attempt = QuestionAttempt.objects.get(id=result["attempt_id"])
        self.assertEqual(attempt.user, self.user)
        self.assertEqual(attempt.question, self.question)
        self.assertEqual(attempt.selected_answer, "c")
        self.assertTrue(attempt.is_correct)
        self.assertEqual(attempt.time_spent_seconds, 60)

    def test_retrieve_answer_updates_stats(self):
        """Test that retrieve_answer updates question stats."""
        # First attempt
        self.question.retrieve_answer("c", user=self.user)

        stats = self.question.stats
        self.assertEqual(stats.total_attempts, 1)
        self.assertEqual(stats.total_successes, 1)
        self.assertEqual(stats.total_failures, 0)
        self.assertEqual(stats.success_rate, Decimal("100.00"))

    def test_update_question_stats(self):
        """Test update_question_stats method."""
        # Create some attempts
        QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
            time_spent_seconds=30,
        )
        QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="a",
            is_correct=False,
            time_spent_seconds=45,
        )

        self.question.update_question_stats()

        stats = self.question.stats
        self.assertEqual(stats.total_attempts, 2)
        self.assertEqual(stats.total_successes, 1)
        self.assertEqual(stats.total_failures, 1)
        self.assertEqual(stats.success_rate, Decimal("50.00"))
        self.assertEqual(stats.average_time_seconds, 37)  # (30+45)/2

    def test_get_current_stats_with_existing_stats(self):
        """Test get_current_stats method when stats exist."""
        self.question.retrieve_answer(
            "c", user=self.user, time_spent_seconds=30
        )

        stats = self.question.get_current_stats()

        self.assertEqual(stats["total_attempts"], 1)
        self.assertEqual(stats["total_successes"], 1)
        self.assertEqual(stats["total_failures"], 0)
        self.assertEqual(stats["success_rate"], 100.0)
        self.assertEqual(stats["average_time_seconds"], 30)
        self.assertIn("difficulty_rating", stats)
        self.assertIn("last_updated", stats)

    def test_get_current_stats_without_stats(self):
        """Test get_current_stats method when no stats exist."""
        stats = self.question.get_current_stats()

        expected_defaults = {
            "total_attempts": 0,
            "total_successes": 0,
            "total_failures": 0,
            "success_rate": 0.0,
            "average_time_seconds": 0,
            "skip_count": 0,
            "difficulty_rating": "unknown",
            "last_updated": None,
        }

        for key, value in expected_defaults.items():
            self.assertEqual(stats[key], value)

    def test_get_calculated_difficulty(self):
        """Test get_calculated_difficulty method."""
        # Test various success rates
        test_cases = [
            (95, "very_easy"),
            (80, "easy"),
            (60, "medium"),
            (40, "hard"),
            (20, "very_hard"),
        ]

        for success_rate, expected_difficulty in test_cases:
            with self.subTest(success_rate=success_rate):
                # Create stats with specific success rate
                stats, _ = QuestionStats.objects.get_or_create(
                    question=self.question
                )
                stats.success_rate = Decimal(str(success_rate))
                stats.save()

                difficulty = self.question.get_calculated_difficulty()
                self.assertEqual(difficulty, expected_difficulty)

    def test_get_calculated_difficulty_no_stats(self):
        """Test get_calculated_difficulty when no stats exist."""
        difficulty = self.question.get_calculated_difficulty()
        self.assertEqual(difficulty, "unknown")

    def test_record_skip(self):
        """Test record_skip method."""
        result = self.question.record_skip(user=self.user)

        self.assertTrue(result["skip_recorded"])
        self.assertEqual(result["total_skips"], 1)

        # Check that stats were created/updated
        stats = self.question.stats
        self.assertEqual(stats.skip_count, 1)

    def test_record_skip_multiple_times(self):
        """Test record_skip method called multiple times."""
        self.question.record_skip(user=self.user)
        result = self.question.record_skip(user=self.user)

        self.assertEqual(result["total_skips"], 2)

        stats = self.question.stats
        self.assertEqual(stats.skip_count, 2)

    def test_record_skip_creates_stats_if_not_exists(self):
        """Test that record_skip creates stats if they don't exist."""
        self.assertFalse(hasattr(self.question, "stats"))

        self.question.record_skip()

        self.assertTrue(hasattr(self.question, "stats"))
        self.assertEqual(self.question.stats.skip_count, 1)

    def test_meta_ordering(self):
        """Test that Question model has correct ordering."""
        expected_ordering = [
            "tutorial_title__title_id_slug",
            "question_id_slug",
        ]
        self.assertEqual(Question._meta.ordering, expected_ordering)

    def test_meta_verbose_names(self):
        """Test Question model verbose names."""
        self.assertEqual(Question._meta.verbose_name, "Question")
        self.assertEqual(Question._meta.verbose_name_plural, "Questions")

    def test_field_help_texts(self):
        """Test that all fields have appropriate help text."""
        fields_with_help_text = [
            "tutorial_title",
            "question_id_slug",
            "question_text",
            "answer_a",
            "answer_b",
            "answer_c",
            "answer_d",
            "correct_answer",
            "difficulty",
            "tags",
        ]

        for field_name in fields_with_help_text:
            field = Question._meta.get_field(field_name)
            self.assertTrue(
                field.help_text, f"Field {field_name} should have help text"
            )

    @patch("questions.models.transaction.atomic")
    def test_retrieve_answer_uses_transaction(self, mock_atomic):
        """Test that retrieve_answer uses database transaction."""
        self.question.retrieve_answer("c", user=self.user)
        mock_atomic.assert_called_once()

    def test_question_manager(self):
        """Test that custom QuestionManager is properly assigned."""
        from ..managers import QuestionManager

        self.assertIsInstance(Question.objects, QuestionManager)

    def test_tags_field(self):
        """Test that tags field works correctly."""
        self.question.tags.add("python", "basics", "programming")

        tag_names = list(self.question.tags.names())
        self.assertIn("python", tag_names)
        self.assertIn("basics", tag_names)
        self.assertIn("programming", tag_names)

    def test_created_at_updated_at_fields(self):
        """Test that timestamp fields are set correctly."""
        self.assertIsNotNone(self.question.created_at)
        self.assertIsNotNone(self.question.updated_at)

        # Test that updated_at changes on save
        original_updated = self.question.updated_at
        self.question.question_text = "Updated question text"
        self.question.save()

        self.assertGreater(self.question.updated_at, original_updated)

    def test_retrieve_answer_returns_question_stats(self):
        """Test that retrieve_answer returns current question stats."""
        result = self.question.retrieve_answer("c", user=self.user)

        self.assertIn("question_stats", result)
        question_stats = result["question_stats"]

        self.assertEqual(question_stats["total_attempts"], 1)
        self.assertEqual(question_stats["total_successes"], 1)
        self.assertEqual(question_stats["success_rate"], 100.0)

    def test_multiple_questions_same_tutorial(self):
        """Test multiple questions can belong to same tutorial."""
        question2 = Question.objects.create(
            tutorial_title=self.tutorial,
            question_id_slug="second-question",
            question_text="What is 2+2?",
            answer_a="3",
            answer_b="4",
            answer_c="5",
            answer_d="6",
            correct_answer="b",
        )

        tutorial_questions = self.tutorial.questions.all()
        self.assertEqual(tutorial_questions.count(), 2)
        self.assertIn(self.question, tutorial_questions)
        self.assertIn(question2, tutorial_questions)

    def test_question_different_tutorials_same_slug(self):
        """Test questions with same slug can exist in different tutorials."""
        other_tutorial = TutorialTitle.objects.create(
            title_id_slug="other-tutorial", name="Other Tutorial"
        )

        other_question = Question.objects.create(
            tutorial_title=other_tutorial,
            question_id_slug="test-question",  # Same slug as self.question
            question_text="Different question text",
            answer_a="A",
            answer_b="B",
            answer_c="C",
            answer_d="D",
            correct_answer="a",
        )

        self.assertEqual(
            self.question.question_id_slug, other_question.question_id_slug
        )
        self.assertNotEqual(
            self.question.tutorial_title, other_question.tutorial_title
        )
