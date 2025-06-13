# questions/tests/test_TutorialStats.py
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import (
    TutorialStats,
    TutorialTitle,
    Question,
    QuestionAttempt,
    QuestionStats,
)


User = get_user_model()


class TutorialStatsModelTest(TestCase):
    """Test cases for the TutorialStats model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.tutorial = TutorialTitle.objects.create(
            title_id_slug="test-tutorial", name="Test Tutorial"
        )
        self.questions = []
        for i in range(3):
            question = Question.objects.create(
                tutorial_title=self.tutorial,
                question_id_slug=f"test-question-{i}",
                question_text=f"Test question {i}?",
                answer_a="Option A",
                answer_b="Option B",
                answer_c="Option C",
                answer_d="Option D",
                correct_answer="c",
            )
            self.questions.append(question)

    def test_tutorial_stats_creation(self):
        """Test that TutorialStats objects are created correctly."""
        stats = TutorialStats.objects.create(
            tutorial_title=self.tutorial,
            total_attempts=50,
            total_completions=35,
            completion_rate=Decimal("70.00"),
            average_score=Decimal("82.50"),
            average_completion_time_minutes=25,
        )

        self.assertEqual(stats.tutorial_title, self.tutorial)
        self.assertEqual(stats.total_attempts, 50)
        self.assertEqual(stats.total_completions, 35)
        self.assertEqual(stats.completion_rate, Decimal("70.00"))
        self.assertEqual(stats.average_score, Decimal("82.50"))
        self.assertEqual(stats.average_completion_time_minutes, 25)
        self.assertIsNotNone(stats.last_updated)

    def test_tutorial_stats_default_values(self):
        """Test that default values are set correctly."""
        stats = TutorialStats.objects.create(tutorial_title=self.tutorial)

        self.assertEqual(stats.total_attempts, 0)
        self.assertEqual(stats.total_completions, 0)
        self.assertEqual(stats.completion_rate, Decimal("0.00"))
        self.assertEqual(stats.average_score, Decimal("0.00"))
        self.assertEqual(stats.average_completion_time_minutes, 0)

    def test_tutorial_stats_str_method(self):
        """Test TutorialStats __str__ method."""
        stats = TutorialStats.objects.create(
            tutorial_title=self.tutorial, completion_rate=Decimal("75.25")
        )

        expected = "Stats for test-tutorial - 75.25% completion"
        self.assertEqual(str(stats), expected)

    def test_one_to_one_relationship(self):
        """Test that TutorialStats has OneToOne relationship with TutorialTitle."""
        stats = TutorialStats.objects.create(tutorial_title=self.tutorial)

        # Test forward relationship
        self.assertEqual(stats.tutorial_title, self.tutorial)

        # Test reverse relationship
        self.assertEqual(self.tutorial.stats, stats)

    def test_one_to_one_uniqueness(self):
        """Test that only one TutorialStats can exist per TutorialTitle."""
        TutorialStats.objects.create(tutorial_title=self.tutorial)

        # Attempting to create another should raise an error
        with self.assertRaises(Exception):
            TutorialStats.objects.create(tutorial_title=self.tutorial)

    def test_cascade_deletion(self):
        """Test that stats are deleted when tutorial is deleted."""
        stats = TutorialStats.objects.create(tutorial_title=self.tutorial)
        stats_id = stats.id

        # Delete tutorial
        self.tutorial.delete()

        # Stats should be deleted due to CASCADE
        with self.assertRaises(TutorialStats.DoesNotExist):
            TutorialStats.objects.get(id=stats_id)

    def test_decimal_field_precision(self):
        """Test that decimal fields maintain proper precision."""
        stats = TutorialStats.objects.create(
            tutorial_title=self.tutorial,
            completion_rate=Decimal("85.67"),
            average_score=Decimal("92.34"),
        )

        self.assertEqual(stats.completion_rate, Decimal("85.67"))
        self.assertEqual(stats.average_score, Decimal("92.34"))

        # Check decimal precision
        self.assertEqual(stats.completion_rate.as_tuple().exponent, -2)
        self.assertEqual(stats.average_score.as_tuple().exponent, -2)

    def test_field_constraints(self):
        """Test field constraints and properties."""
        # Test decimal fields
        completion_rate_field = TutorialStats._meta.get_field(
            "completion_rate"
        )
        average_score_field = TutorialStats._meta.get_field("average_score")

        self.assertEqual(completion_rate_field.max_digits, 5)
        self.assertEqual(completion_rate_field.decimal_places, 2)
        self.assertEqual(average_score_field.max_digits, 5)
        self.assertEqual(average_score_field.decimal_places, 2)

        # Test positive integer fields
        positive_fields = [
            "total_attempts",
            "total_completions",
            "average_completion_time_minutes",
        ]

        for field_name in positive_fields:
            field = TutorialStats._meta.get_field(field_name)
            self.assertEqual(field.__class__.__name__, "PositiveIntegerField")

    def test_auto_now_last_updated(self):
        """Test that last_updated field uses auto_now."""
        field = TutorialStats._meta.get_field("last_updated")
        self.assertTrue(field.auto_now)

    def test_meta_verbose_names(self):
        """Test model meta verbose names."""
        self.assertEqual(
            TutorialStats._meta.verbose_name, "Tutorial Statistics"
        )
        self.assertEqual(
            TutorialStats._meta.verbose_name_plural, "Tutorial Statistics"
        )

    def test_get_question_performance_summary_empty(self):
        """Test get_question_performance_summary with no stats."""
        stats = TutorialStats.objects.create(tutorial_title=self.tutorial)

        summary = stats.get_question_performance_summary()

        expected = {
            "total_questions": 3,  # We created 3 questions in setUp
            "questions_with_stats": 0,
            "average_success_rate": 0,
            "most_difficult_question": None,
            "easiest_question": None,
        }

        self.assertEqual(summary, expected)

    def test_get_question_performance_summary_with_stats(self):
        """Test get_question_performance_summary with question stats."""
        stats = TutorialStats.objects.create(tutorial_title=self.tutorial)

        # Create stats for questions with different success rates
        success_rates = [Decimal("90.00"), Decimal("60.00"), Decimal("75.00")]

        for i, rate in enumerate(success_rates):
            QuestionStats.objects.create(
                question=self.questions[i],
                total_attempts=10,
                total_successes=int(rate / 10),
                success_rate=rate,
            )

        summary = stats.get_question_performance_summary()

        self.assertEqual(summary["total_questions"], 3)
        self.assertEqual(summary["questions_with_stats"], 3)
        self.assertEqual(summary["average_success_rate"], 75.0)  # (90+60+75)/3

        # Most difficult should be the one with lowest success rate
        self.assertEqual(
            summary["most_difficult_question"]["question_id"],
            "test-question-1",
        )
        self.assertEqual(
            summary["most_difficult_question"]["success_rate"], 60.0
        )

        # Easiest should be the one with highest success rate
        self.assertEqual(
            summary["easiest_question"]["question_id"], "test-question-0"
        )
        self.assertEqual(summary["easiest_question"]["success_rate"], 90.0)

    def test_get_question_performance_summary_partial_stats(self):
        """Test get_question_performance_summary with partial stats."""
        stats = TutorialStats.objects.create(tutorial_title=self.tutorial)

        # Create stats for only 2 out of 3 questions
        QuestionStats.objects.create(
            question=self.questions[0], success_rate=Decimal("80.00")
        )
        QuestionStats.objects.create(
            question=self.questions[1], success_rate=Decimal("70.00")
        )

        summary = stats.get_question_performance_summary()

        self.assertEqual(summary["total_questions"], 3)
        self.assertEqual(summary["questions_with_stats"], 2)
        self.assertEqual(summary["average_success_rate"], 75.0)  # (80+70)/2

    def test_get_question_performance_summary_single_question(self):
        """Test get_question_performance_summary with single question."""
        # Create a tutorial with only one question
        single_tutorial = TutorialTitle.objects.create(
            title_id_slug="single-question-tutorial",
            name="Single Question Tutorial",
        )

        single_question = Question.objects.create(
            tutorial_title=single_tutorial,
            question_id_slug="single-question",
            question_text="Only question?",
            answer_a="A",
            answer_b="B",
            answer_c="C",
            answer_d="D",
            correct_answer="a",
        )

        QuestionStats.objects.create(
            question=single_question, success_rate=Decimal("65.00")
        )

        stats = TutorialStats.objects.create(tutorial_title=single_tutorial)
        summary = stats.get_question_performance_summary()

        self.assertEqual(summary["total_questions"], 1)
        self.assertEqual(summary["questions_with_stats"], 1)
        self.assertEqual(summary["average_success_rate"], 65.0)

        # Both most difficult and easiest should be the same question
        self.assertEqual(
            summary["most_difficult_question"]["question_id"],
            "single-question",
        )
        self.assertEqual(
            summary["easiest_question"]["question_id"], "single-question"
        )

    def test_completion_rate_calculation(self):
        """Test completion rate calculation logic."""
        stats = TutorialStats.objects.create(
            tutorial_title=self.tutorial,
            total_attempts=100,
            total_completions=75,
        )

        # Manual calculation
        expected_rate = (75 / 100) * 100
        stats.completion_rate = Decimal(str(expected_rate))
        stats.save()

        self.assertEqual(stats.completion_rate, Decimal("75.00"))

    def test_average_score_boundaries(self):
        """Test average_score with boundary values."""
        boundary_scores = [
            Decimal("0.00"),  # Minimum
            Decimal("100.00"),  # Maximum
            Decimal("50.00"),  # Middle
            Decimal("99.99"),  # Almost perfect
            Decimal("0.01"),  # Almost zero
        ]

        for score in boundary_scores:
            with self.subTest(score=score):
                stats = TutorialStats.objects.create(
                    tutorial_title=self.tutorial, average_score=score
                )
                self.assertEqual(stats.average_score, score)
                stats.delete()  # Clean up for next test

    def test_large_time_values(self):
        """Test handling of large completion time values."""
        stats = TutorialStats.objects.create(
            tutorial_title=self.tutorial,
            average_completion_time_minutes=999999,  # Very large value
        )

        self.assertEqual(stats.average_completion_time_minutes, 999999)

    def test_stats_update_functionality(self):
        """Test updating TutorialStats values."""
        stats = TutorialStats.objects.create(
            tutorial_title=self.tutorial,
            total_attempts=10,
            total_completions=8,
            completion_rate=Decimal("80.00"),
            average_score=Decimal("75.00"),
        )

        # Update values
        stats.total_attempts = 20
        stats.total_completions = 16
        stats.completion_rate = Decimal(
            "80.00"
        )  # Still 80% but with more data
        stats.average_score = Decimal("78.50")
        stats.average_completion_time_minutes = 30
        stats.save()

        # Verify updates
        updated_stats = TutorialStats.objects.get(tutorial_title=self.tutorial)
        self.assertEqual(updated_stats.total_attempts, 20)
        self.assertEqual(updated_stats.total_completions, 16)
        self.assertEqual(updated_stats.completion_rate, Decimal("80.00"))
        self.assertEqual(updated_stats.average_score, Decimal("78.50"))
        self.assertEqual(updated_stats.average_completion_time_minutes, 30)

    def test_zero_attempts_edge_case(self):
        """Test handling of zero attempts scenario."""
        stats = TutorialStats.objects.create(
            tutorial_title=self.tutorial,
            total_attempts=0,
            total_completions=0,
            completion_rate=Decimal("0.00"),
            average_score=Decimal("0.00"),
        )

        # Should handle division by zero gracefully
        summary = stats.get_question_performance_summary()
        self.assertEqual(summary["total_questions"], 3)
        self.assertEqual(summary["average_success_rate"], 0)

    def test_stats_with_real_attempts_integration(self):
        """Test TutorialStats with actual QuestionAttempt data."""
        stats = TutorialStats.objects.create(tutorial_title=self.tutorial)

        # Create real attempts
        user2 = User.objects.create_user(username="user2", password="pass2")

        # User 1: 2/3 correct
        QuestionAttempt.objects.create(
            user=self.user,
            question=self.questions[0],
            selected_answer="c",
            is_correct=True,
        )
        QuestionAttempt.objects.create(
            user=self.user,
            question=self.questions[1],
            selected_answer="c",
            is_correct=True,
        )
        QuestionAttempt.objects.create(
            user=self.user,
            question=self.questions[2],
            selected_answer="a",
            is_correct=False,
        )

        # User 2: 1/3 correct
        QuestionAttempt.objects.create(
            user=user2,
            question=self.questions[0],
            selected_answer="c",
            is_correct=True,
        )
        QuestionAttempt.objects.create(
            user=user2,
            question=self.questions[1],
            selected_answer="a",
            is_correct=False,
        )
        QuestionAttempt.objects.create(
            user=user2,
            question=self.questions[2],
            selected_answer="b",
            is_correct=False,
        )

        # Update question stats based on attempts
        for question in self.questions:
            question.update_question_stats()

        # Now test the summary
        summary = stats.get_question_performance_summary()
        self.assertEqual(summary["questions_with_stats"], 3)
        self.assertGreater(summary["average_success_rate"], 0)

    def test_related_name_stats(self):
        """Test that the related_name 'stats' works correctly."""
        stats = TutorialStats.objects.create(tutorial_title=self.tutorial)

        # Access through related name
        tutorial_stats = self.tutorial.stats
        self.assertEqual(tutorial_stats, stats)
