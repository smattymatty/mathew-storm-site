# questions/tests/test_performance.py

import time
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from questions.models import Question, TutorialTitle


@override_settings(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
            "OPTIONS": {
                "timeout": 20,
            },
        }
    }
)
class QuizPerformanceTest(TestCase):
    """
    Performance tests for quiz functionality.
    """

    @classmethod
    def setUpTestData(cls):
        """Set up test data for performance testing."""
        cls.tutorial = TutorialTitle.objects.create(
            title_id_slug="perf-test-tut", name="Performance Test Tutorial"
        )

        # Create multiple questions for load testing
        cls.questions = []
        for i in range(20):  # Reduced number to avoid timeout
            question = Question.objects.create(
                tutorial_title=cls.tutorial,
                question_id_slug=f"perf-q-{i}",
                question_text=f"Performance test question {i}?",
                answer_a=f"Option A {i}",
                answer_b=f"Option B {i}",
                answer_c=f"Option C {i}",
                answer_d=f"Option D {i}",
                correct_answer="b",
                difficulty="easy",
            )
            cls.questions.append(question)

    def setUp(self):
        """Set up for each test."""
        self.client = Client()

    def test_question_loading_performance(self):
        """Test that question loading performs within acceptable limits."""
        start_time = time.time()

        response = self.client.get(
            reverse("questions:htmx_load_questions"),
            headers={"HX-Request": "true"},
        )

        end_time = time.time()
        load_time = end_time - start_time

        self.assertEqual(response.status_code, 200)
        # Should load within 5 seconds even with 20 questions
        self.assertLess(
            load_time,
            5.0,
            f"Question loading took {load_time:.2f} seconds, expected < 5.0",
        )

    def test_answer_checking_performance(self):
        """Test that answer checking performs quickly."""
        question = self.questions[0]

        start_time = time.time()

        response = self.client.post(
            reverse("questions:htmx_check_answer", args=[question.pk]),
            data={f"answer_for_q{question.pk}": "b"},
            headers={"HX-Request": "true"},
        )

        end_time = time.time()
        check_time = end_time - start_time

        self.assertEqual(response.status_code, 200)
        # Answer checking should be very fast
        self.assertLess(
            check_time,
            2.0,
            f"Answer checking took {check_time:.2f} seconds, expected < 2.0",
        )

    @override_settings(DEBUG=False)
    def test_template_rendering_efficiency(self):
        """Test that template rendering is efficient."""
        question = self.questions[0]

        # Warm up
        self.client.post(
            reverse("questions:htmx_check_answer", args=[question.pk]),
            data={f"answer_for_q{question.pk}": "b"},
            headers={"HX-Request": "true"},
        )

        # Measure multiple renders
        start_time = time.time()

        for _ in range(10):  # Reduced iterations
            self.client.post(
                reverse("questions:htmx_check_answer", args=[question.pk]),
                data={f"answer_for_q{question.pk}": "b"},
                headers={"HX-Request": "true"},
            )

        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / 10

        # Each render should be reasonably fast
        self.assertLess(
            avg_time,
            1.0,
            f"Average render time was {avg_time:.3f} seconds, expected < 1.0",
        )
