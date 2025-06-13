# questions/tests/test_QuestionStats.py
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import QuestionStats, Question, TutorialTitle, QuestionAttempt


User = get_user_model()


class QuestionStatsModelTest(TestCase):
    """Test cases for the QuestionStats model."""

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

    def test_question_stats_creation(self):
        """Test that QuestionStats objects are created correctly."""
        stats = QuestionStats.objects.create(
            question=self.question,
            total_attempts=10,
            total_successes=7,
            total_failures=3,
            success_rate=Decimal("70.00"),
            average_time_seconds=45,
            skip_count=2,
        )

        self.assertEqual(stats.question, self.question)
        self.assertEqual(stats.total_attempts, 10)
        self.assertEqual(stats.total_successes, 7)
        self.assertEqual(stats.total_failures, 3)
        self.assertEqual(stats.success_rate, Decimal("70.00"))
        self.assertEqual(stats.average_time_seconds, 45)
        self.assertEqual(stats.skip_count, 2)
        self.assertIsNotNone(stats.last_updated)

    def test_question_stats_default_values(self):
        """Test that default values are set correctly."""
        stats = QuestionStats.objects.create(question=self.question)

        self.assertEqual(stats.total_attempts, 0)
        self.assertEqual(stats.total_successes, 0)
        self.assertEqual(stats.total_failures, 0)
        self.assertEqual(stats.success_rate, Decimal("0.00"))
        self.assertEqual(stats.average_time_seconds, 0)
        self.assertEqual(stats.skip_count, 0)

    def test_question_stats_str_method(self):
        """Test QuestionStats __str__ method."""
        stats = QuestionStats.objects.create(
            question=self.question, success_rate=Decimal("85.50")
        )

        expected = "Stats for test-question - 85.50% success"
        self.assertEqual(str(stats), expected)

    def test_one_to_one_relationship(self):
        """Test that QuestionStats has OneToOne relationship with Question."""
        stats = QuestionStats.objects.create(question=self.question)

        # Test forward relationship
        self.assertEqual(stats.question, self.question)

        # Test reverse relationship
        self.assertEqual(self.question.stats, stats)

    def test_one_to_one_uniqueness(self):
        """Test that only one QuestionStats can exist per Question."""
        QuestionStats.objects.create(question=self.question)

        # Attempting to create another should raise an error
        with self.assertRaises(Exception):
            QuestionStats.objects.create(question=self.question)

    def test_cascade_deletion(self):
        """Test that stats are deleted when question is deleted."""
        stats = QuestionStats.objects.create(question=self.question)
        stats_id = stats.id

        # Delete question
        self.question.delete()

        # Stats should be deleted due to CASCADE
        with self.assertRaises(QuestionStats.DoesNotExist):
            QuestionStats.objects.get(id=stats_id)

    def test_success_rate_decimal_precision(self):
        """Test that success_rate maintains proper decimal precision."""
        stats = QuestionStats.objects.create(
            question=self.question, success_rate=Decimal("75.55")
        )

        self.assertEqual(stats.success_rate, Decimal("75.55"))
        self.assertEqual(
            stats.success_rate.as_tuple().exponent, -2
        )  # 2 decimal places

    def test_success_rate_field_constraints(self):
        """Test success_rate field constraints."""
        field = QuestionStats._meta.get_field("success_rate")

        self.assertEqual(field.max_digits, 5)
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(field.default, Decimal("0.00"))

    def test_positive_integer_fields(self):
        """Test that count fields are PositiveIntegerField."""
        positive_fields = [
            "total_attempts",
            "total_successes",
            "total_failures",
            "average_time_seconds",
            "skip_count",
        ]

        for field_name in positive_fields:
            field = QuestionStats._meta.get_field(field_name)
            self.assertEqual(field.__class__.__name__, "PositiveIntegerField")

    def test_auto_now_last_updated(self):
        """Test that last_updated field uses auto_now."""
        field = QuestionStats._meta.get_field("last_updated")
        self.assertTrue(field.auto_now)

    def test_meta_verbose_names(self):
        """Test model meta verbose names."""
        self.assertEqual(
            QuestionStats._meta.verbose_name, "Question Statistics"
        )
        self.assertEqual(
            QuestionStats._meta.verbose_name_plural, "Question Statistics"
        )

    def test_get_answer_distribution_empty(self):
        """Test get_answer_distribution when no attempts exist."""
        stats = QuestionStats.objects.create(question=self.question)

        distribution = stats.get_answer_distribution()

        self.assertEqual(distribution, {})

    def test_get_answer_distribution_with_attempts(self):
        """Test get_answer_distribution with actual attempts."""
        stats = QuestionStats.objects.create(question=self.question)

        # Create various attempts
        attempts_data = [
            ("a", False),
            ("a", False),
            ("b", False),
            ("c", True),
            ("c", True),
            ("c", True),
            ("d", False),
        ]

        for answer, is_correct in attempts_data:
            QuestionAttempt.objects.create(
                user=self.user,
                question=self.question,
                selected_answer=answer,
                is_correct=is_correct,
            )

        distribution = stats.get_answer_distribution()

        expected = {"a": 2, "b": 1, "c": 3, "d": 1}
        self.assertEqual(distribution, expected)

    def test_get_answer_distribution_single_answer(self):
        """Test get_answer_distribution with only one type of answer."""
        stats = QuestionStats.objects.create(question=self.question)

        # Create attempts all with same answer
        for _ in range(5):
            QuestionAttempt.objects.create(
                user=self.user,
                question=self.question,
                selected_answer="c",
                is_correct=True,
            )

        distribution = stats.get_answer_distribution()

        expected = {"c": 5}
        self.assertEqual(distribution, expected)

    def test_get_answer_distribution_multiple_users(self):
        """Test get_answer_distribution with multiple users."""
        user2 = User.objects.create_user(username="user2", password="pass2")
        stats = QuestionStats.objects.create(question=self.question)

        # User 1 attempts
        QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="a",
            is_correct=False,
        )
        QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        # User 2 attempts
        QuestionAttempt.objects.create(
            user=user2,
            question=self.question,
            selected_answer="b",
            is_correct=False,
        )
        QuestionAttempt.objects.create(
            user=user2,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        distribution = stats.get_answer_distribution()

        expected = {"a": 1, "b": 1, "c": 2}
        self.assertEqual(distribution, expected)

    def test_get_answer_distribution_anonymous_users(self):
        """Test get_answer_distribution includes anonymous user attempts."""
        stats = QuestionStats.objects.create(question=self.question)

        # Anonymous attempts
        QuestionAttempt.objects.create(
            user=None,
            question=self.question,
            selected_answer="a",
            is_correct=False,
        )
        QuestionAttempt.objects.create(
            user=None,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        # Authenticated user attempt
        QuestionAttempt.objects.create(
            user=self.user,
            question=self.question,
            selected_answer="c",
            is_correct=True,
        )

        distribution = stats.get_answer_distribution()

        expected = {"a": 1, "c": 2}
        self.assertEqual(distribution, expected)

    def test_stats_calculation_consistency(self):
        """Test that manual calculations match stored values."""
        stats = QuestionStats.objects.create(
            question=self.question,
            total_attempts=20,
            total_successes=15,
            total_failures=5,
        )

        # Verify calculations
        self.assertEqual(
            stats.total_attempts, stats.total_successes + stats.total_failures
        )

        calculated_success_rate = (
            stats.total_successes / stats.total_attempts
        ) * 100
        expected_success_rate = Decimal("75.00")

        # Update with calculated rate
        stats.success_rate = expected_success_rate
        stats.save()

        self.assertEqual(stats.success_rate, expected_success_rate)

    def test_large_numbers_handling(self):
        """Test that stats can handle large numbers."""
        stats = QuestionStats.objects.create(
            question=self.question,
            total_attempts=999999,
            total_successes=500000,
            total_failures=499999,
            success_rate=Decimal("50.00"),
            average_time_seconds=86400,  # 24 hours in seconds
            skip_count=100000,
        )

        self.assertEqual(stats.total_attempts, 999999)
        self.assertEqual(stats.average_time_seconds, 86400)
        self.assertEqual(stats.skip_count, 100000)

    def test_success_rate_edge_cases(self):
        """Test success_rate with edge case values."""
        edge_cases = [
            Decimal("0.00"),  # 0%
            Decimal("100.00"),  # 100%
            Decimal("50.00"),  # 50%
            Decimal("33.33"),  # 1/3
            Decimal("66.67"),  # 2/3
            Decimal("99.99"),  # Almost 100%
            Decimal("0.01"),  # Almost 0%
        ]

        for rate in edge_cases:
            with self.subTest(rate=rate):
                stats = QuestionStats.objects.create(
                    question=self.question, success_rate=rate
                )
                self.assertEqual(stats.success_rate, rate)
                stats.delete()  # Clean up for next test

    def test_related_name_stats(self):
        """Test that the related_name 'stats' works correctly."""
        stats = QuestionStats.objects.create(question=self.question)

        # Access through related name
        question_stats = self.question.stats
        self.assertEqual(question_stats, stats)

    def test_question_stats_updates(self):
        """Test updating QuestionStats values."""
        stats = QuestionStats.objects.create(
            question=self.question,
            total_attempts=5,
            success_rate=Decimal("60.00"),
        )

        # Update values
        stats.total_attempts = 10
        stats.success_rate = Decimal("70.00")
        stats.save()

        # Verify updates
        updated_stats = QuestionStats.objects.get(question=self.question)
        self.assertEqual(updated_stats.total_attempts, 10)
        self.assertEqual(updated_stats.success_rate, Decimal("70.00"))
