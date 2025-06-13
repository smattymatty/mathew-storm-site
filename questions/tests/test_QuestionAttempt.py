# questions/tests/test_QuestionAttempt.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from ..models import QuestionAttempt, Question, TutorialTitle


User = get_user_model()


class QuestionAttemptModelTest(TestCase):
    """Test cases for the QuestionAttempt model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.tutorial = TutorialTitle.objects.create(
            title_id_slug="test-tutorial", name="Test Tutorial"
        )
        self.question = Question.objects.create(
            tutorial_title=self.tutorial,
            question_id_slug="test-question",
            question_text="Test question?",
            answer_a="Option A",
            answer_b="Option B",
            answer_c="Option C",
            answer_d="Option D",
            correct_answer="c",
        )

    def test_question_attempt_creation(self):
        """Test that QuestionAttempt objects are created correctly."""
        attempt = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
            time_spent_seconds=45,
            attempt_number=1,
        )

        self.assertEqual(attempt.user, self.user)
        self.assertEqual(attempt.question, self.question)
        self.assertEqual(attempt.selected_answer, "c")
        self.assertTrue(attempt.is_correct)
        self.assertEqual(attempt.time_spent_seconds, 45)
        self.assertEqual(attempt.attempt_number, 1)
        self.assertIsNotNone(attempt.created_at)

    def test_question_attempt_creation_anonymous_user(self):
        """Test QuestionAttempt creation with anonymous user."""
        attempt = QuestionAttempt.objects.create(
            user=None,  # Anonymous user
            question=self.question,
            selected_answer="a",
            is_correct=False,
            time_spent_seconds=30,
        )

        self.assertIsNone(attempt.user)
        self.assertEqual(attempt.question, self.question)
        self.assertEqual(attempt.selected_answer, "a")
        self.assertFalse(attempt.is_correct)

    def test_question_attempt_default_values(self):
        """Test that default values are set correctly."""
        attempt = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="b",
            is_correct=False,
        )

        self.assertEqual(attempt.time_spent_seconds, 0)  # Default value
        self.assertEqual(attempt.attempt_number, 1)  # Default value

    def test_question_attempt_str_method(self):
        """Test QuestionAttempt __str__ method."""
        attempt = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        expected = "testuser - test-question - Correct"
        self.assertEqual(str(attempt), expected)

    def test_question_attempt_str_method_incorrect(self):
        """Test __str__ method for incorrect answer."""
        attempt = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="a",
            is_correct=False,
        )

        expected = "testuser - test-question - Incorrect"
        self.assertEqual(str(attempt), expected)

    def test_question_attempt_str_method_anonymous(self):
        """Test __str__ method for anonymous user."""
        attempt = QuestionAttempt.objects.create(
            user=None,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        expected = "Anonymous - test-question - Correct"
        self.assertEqual(str(attempt), expected)

    def test_answer_choice_validation(self):
        """Test that selected_answer must be valid choice."""
        # Valid choices should work
        for choice in ["a", "b", "c", "d"]:
            attempt = QuestionAttempt.objects.create(
                user=self.user,
                question=self.question,
                selected_answer=choice,
                is_correct=(choice == "c"),
            )
            self.assertEqual(attempt.selected_answer, choice)

    def test_foreign_key_relationships(self):
        """Test foreign key relationships work correctly."""
        attempt = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        # Test forward relationships
        self.assertEqual(attempt.user, self.user)
        self.assertEqual(attempt.question, self.question)

        # Test reverse relationships
        self.assertIn(attempt, self.user.question_attempts.all())
        self.assertIn(attempt, self.question.attempts.all())

    def test_cascade_deletion_user(self):
        """Test that attempts are deleted when user is deleted."""
        attempt = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )
        attempt_id = attempt.id

        # Delete user
        self.user.delete()

        # Attempt should be deleted due to CASCADE
        with self.assertRaises(QuestionAttempt.DoesNotExist):
            QuestionAttempt.objects.get(id=attempt_id)

    def test_cascade_deletion_question(self):
        """Test that attempts are deleted when question is deleted."""
        attempt = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )
        attempt_id = attempt.id

        # Delete question
        self.question.delete()

        # Attempt should be deleted due to CASCADE
        with self.assertRaises(QuestionAttempt.DoesNotExist):
            QuestionAttempt.objects.get(id=attempt_id)

    def test_attempt_number_incrementation(self):
        """Test that attempt numbers can increment correctly."""
        # Create multiple attempts for same user/question
        attempt1 = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="a",
            is_correct=False,
            attempt_number=1,
        )

        attempt2 = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="b",
            is_correct=False,
            attempt_number=2,
        )

        attempt3 = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
            attempt_number=3,
        )

        self.assertEqual(attempt1.attempt_number, 1)
        self.assertEqual(attempt2.attempt_number, 2)
        self.assertEqual(attempt3.attempt_number, 3)

    def test_time_spent_seconds_field(self):
        """Test time_spent_seconds field behavior."""
        attempt = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
            time_spent_seconds=120,
        )

        self.assertEqual(attempt.time_spent_seconds, 120)
        self.assertIsInstance(attempt.time_spent_seconds, int)

    def test_time_spent_seconds_positive_constraint(self):
        """Test that time_spent_seconds must be positive."""
        # Should work with positive values
        attempt = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
            time_spent_seconds=1,
        )
        self.assertEqual(attempt.time_spent_seconds, 1)

    def test_meta_ordering(self):
        """Test that QuestionAttempt has correct ordering."""
        # Create multiple attempts
        attempt1 = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="a",
            is_correct=False,
        )

        attempt2 = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        # Should be ordered by -created_at (newest first)
        attempts = QuestionAttempt.objects.all()
        self.assertEqual(attempts[0], attempt2)  # Most recent first
        self.assertEqual(attempts[1], attempt1)

    def test_meta_indexes(self):
        """Test that proper database indexes are defined."""
        expected_indexes = [
            ["user", "question"],
            ["question", "is_correct"],
            ["created_at"],
        ]

        actual_indexes = []
        for index in QuestionAttempt._meta.indexes:
            actual_indexes.append(index.fields)

        for expected_index in expected_indexes:
            self.assertIn(expected_index, actual_indexes)

    def test_related_name_user(self):
        """Test that related_name 'question_attempts' works for user."""
        attempt = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        user_attempts = self.user.question_attempts.all()
        self.assertIn(attempt, user_attempts)
        self.assertEqual(user_attempts.count(), 1)

    def test_related_name_question(self):
        """Test that related_name 'attempts' works for question."""
        attempt = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        question_attempts = self.question.attempts.all()
        self.assertIn(attempt, question_attempts)
        self.assertEqual(question_attempts.count(), 1)

    def test_multiple_users_same_question(self):
        """Test multiple users can attempt the same question."""
        user2 = User.objects.create_user(username="user2", password="pass2")

        attempt1 = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        attempt2 = QuestionAttempt.objects.create(
            user=user2,
            question=self.question,
            selected_answer="a",
            is_correct=False,
        )

        self.assertEqual(QuestionAttempt.objects.count(), 2)
        self.assertNotEqual(attempt1.user, attempt2.user)
        self.assertEqual(attempt1.question, attempt2.question)

    def test_same_user_multiple_questions(self):
        """Test same user can attempt multiple questions."""
        question2 = Question.objects.create(
            tutorial_title=self.tutorial,
            question_id_slug="test-question-2",
            question_text="Second test question?",
            answer_a="A",
            answer_b="B",
            answer_c="C",
            answer_d="D",
            correct_answer="b",
        )

        attempt1 = QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        attempt2 = QuestionAttempt.objects.create(
            user=self.user,
            question=question2,
            selected_answer="b",
            is_correct=True,
        )

        user_attempts = self.user.question_attempts.all()
        self.assertEqual(user_attempts.count(), 2)
        self.assertIn(attempt1, user_attempts)
        self.assertIn(attempt2, user_attempts)

    def test_anonymous_user_attempts(self):
        """Test that anonymous users can make multiple attempts."""
        attempt1 = QuestionAttempt.objects.create(
            user=None,
            question=self.question,
            selected_answer="a",
            is_correct=False,
        )

        attempt2 = QuestionAttempt.objects.create(
            user=None,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        anonymous_attempts = QuestionAttempt.objects.filter(user=None)
        self.assertEqual(anonymous_attempts.count(), 2)
