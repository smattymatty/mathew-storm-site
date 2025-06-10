# questions/tests/integration/test_quiz_integration.py

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User

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
class QuizIntegrationTest(TestCase):
    """
    Integration tests for the complete quiz workflow including:
    - Question display
    - Answer submission
    - Feedback display
    - Navigation back to questions
    """

    @classmethod
    def setUpTestData(cls):
        """Set up test data for integration tests."""
        # Create a tutorial
        cls.tutorial = TutorialTitle.objects.create(
            title_id_slug="integration-test-tut",
            name="Integration Test Tutorial",
        )

        # Create test questions
        cls.question_easy = Question.objects.create(
            tutorial_title=cls.tutorial,
            question_id_slug="easy-q",
            question_text="What is 2 + 2?",
            answer_a="3",
            answer_b="4",
            answer_c="5",
            answer_d="6",
            correct_answer="b",
            difficulty="easy",
        )
        cls.question_easy.tags.add("arithmetic")

        cls.question_hard = Question.objects.create(
            tutorial_title=cls.tutorial,
            question_id_slug="hard-q",
            question_text="What is the capital of Mongolia?",
            answer_a="Ulaanbaatar",
            answer_b="Beijing",
            answer_c="Moscow",
            answer_d="Seoul",
            correct_answer="a",
            difficulty="hard",
        )
        cls.question_hard.tags.add("geography")

    def setUp(self):
        """Set up for each test."""
        self.client = Client()

    def test_quiz_page_loads_successfully(self):
        """Test that the main quiz page loads with initial questions."""
        response = self.client.get(reverse("questions:question_page"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Interactive Quiz")
        self.assertContains(response, "Quiz Options")
        self.assertContains(response, "Selected Filters")

    def test_correct_answer_submission_workflow(self):
        """Test the complete workflow for a correct answer submission."""
        # Step 1: Submit correct answer via HTMX
        response = self.client.post(
            reverse(
                "questions:htmx_check_answer", args=[self.question_easy.pk]
            ),
            data={f"answer_for_q{self.question_easy.pk}": "b"},
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)

        # Check that correct feedback template is used
        self.assertTemplateUsed(
            response, "questions/partials/feedback/_feedback_correct.html"
        )

        # Check response content contains success elements
        content = response.content.decode()
        self.assertIn("Excellent! 🎉", content)
        self.assertIn("That's correct!", content)
        self.assertIn("B", content)  # User's answer
        self.assertIn("Try Again", content)
        self.assertIn("Continue Reading", content)

    def test_incorrect_answer_submission_workflow(self):
        """Test the complete workflow for an incorrect answer submission."""
        # Step 1: Submit incorrect answer via HTMX
        response = self.client.post(
            reverse(
                "questions:htmx_check_answer", args=[self.question_easy.pk]
            ),
            data={f"answer_for_q{self.question_easy.pk}": "c"},
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)

        # Check that incorrect feedback template is used
        self.assertTemplateUsed(
            response, "questions/partials/feedback/_feedback_incorrect.html"
        )

        # Check response content contains error elements
        content = response.content.decode()
        self.assertIn("Not Quite Right 🤔", content)
        self.assertIn("C", content)  # User's wrong answer
        self.assertIn("Try Again", content)
        self.assertIn("Continue Reading", content)

    def test_try_again_functionality(self):
        """Test that 'Try Again' button reloads the original question."""
        # Step 1: Submit an answer to get feedback
        self.client.post(
            reverse(
                "questions:htmx_check_answer", args=[self.question_easy.pk]
            ),
            data={f"answer_for_q{self.question_easy.pk}": "c"},
            headers={"HX-Request": "true"},
        )

        # Step 2: Load the single question again (simulating "Try Again" click)
        response = self.client.get(
            reverse(
                "questions:htmx_load_single_question",
                args=[self.question_easy.pk],
            ),
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "questions/partials/question_block/_question_block_htmx.html",
        )

        # Check that the original question form is restored
        content = response.content.decode()
        self.assertIn("What is 2 + 2?", content)
        self.assertIn('type="radio"', content)
        self.assertIn("Submit Answer", content)

    def test_question_loading_with_difficulty_filter(self):
        """Test loading questions with difficulty filters."""
        response = self.client.get(
            reverse("questions:htmx_load_questions"),
            data={"difficulty": "easy"},
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # Should contain the easy question
        self.assertIn("What is 2 + 2?", content)
        # Should not contain the hard question
        self.assertNotIn("What is the capital of Mongolia?", content)

    def test_error_handling_for_invalid_question(self):
        """Test error handling when submitting answer for non-existent question."""
        invalid_question_pk = 99999
        response = self.client.post(
            reverse("questions:htmx_check_answer", args=[invalid_question_pk]),
            data={f"answer_for_q{invalid_question_pk}": "a"},
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Question not found", content)

    def test_empty_answer_submission(self):
        """Test submitting form without selecting an answer."""
        response = self.client.post(
            reverse(
                "questions:htmx_check_answer", args=[self.question_easy.pk]
            ),
            data={},  # No answer submitted
            headers={"HX-Request": "true"},
        )

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Please select an answer before submitting", content)
