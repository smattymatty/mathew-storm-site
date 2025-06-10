# questions/tests/integration/test_templates.py

from django.test import TestCase, RequestFactory, override_settings
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template.response import TemplateResponse

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
class FeedbackTemplateTest(TestCase):
    """
    Tests for feedback template rendering and context.
    """

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.tutorial = TutorialTitle.objects.create(
            title_id_slug="template-test-tut", name="Template Test Tutorial"
        )

        cls.question = Question.objects.create(
            tutorial_title=cls.tutorial,
            question_id_slug="template-q",
            question_text="Test question for template?",
            answer_a="Option A",
            answer_b="Option B",
            answer_c="Option C",
            answer_d="Option D",
            correct_answer="b",
        )

    def test_correct_feedback_template_renders(self):
        """Test that correct feedback template renders with proper context."""
        context = {
            "question": self.question,
            "submitted_answer": "b",
            "submitted_answer_text": "Option B",
            "correct_answer": "b",
            "correct_answer_text": "Option B",
            "is_correct": True,
            "explanation": None,  # No explanation field in model
        }

        rendered = render_to_string(
            "questions/partials/feedback/_feedback_correct.html", context
        )

        # Check for success elements
        self.assertIn("Excellent! 🎉", rendered)
        self.assertIn("That's correct!", rendered)
        self.assertIn("Option B", rendered)
        self.assertIn("Try Again", rendered)
        self.assertIn("Continue Reading", rendered)
        self.assertIn(str(self.question.pk), rendered)

    def test_incorrect_feedback_template_renders(self):
        """Test that incorrect feedback template renders with proper context."""
        context = {
            "question": self.question,
            "submitted_answer": "c",
            "submitted_answer_text": "Option C",
            "correct_answer": "b",
            "correct_answer_text": "Option B",
            "is_correct": False,
            "explanation": None,  # No explanation field in model
        }

        rendered = render_to_string(
            "questions/partials/feedback/_feedback_incorrect.html", context
        )

        # Check for error elements
        self.assertIn("Not Quite Right 🤔", rendered)
        self.assertIn("Option C", rendered)  # Their wrong answer
        self.assertIn("Try Again", rendered)
        self.assertIn("Continue Reading", rendered)
        self.assertIn(str(self.question.pk), rendered)

    def test_feedback_template_without_explanation(self):
        """Test feedback templates work when explanation is None."""
        context = {
            "question": self.question,
            "submitted_answer": "a",
            "submitted_answer_text": "Option A",
            "correct_answer": "b",
            "correct_answer_text": "Option B",
            "is_correct": False,
            "explanation": None,
        }

        rendered = render_to_string(
            "questions/partials/feedback/_feedback_incorrect.html", context
        )

        # Should not contain explanation section when None
        # But should still contain other elements
        self.assertIn("Not Quite Right 🤔", rendered)
        self.assertIn("Option A", rendered)

    def test_question_block_template_renders(self):
        """Test that question block template renders correctly."""
        context = {"question": self.question}

        rendered = render_to_string(
            "questions/partials/question_block/_question_block_htmx.html",
            context,
        )

        # Check for question elements
        self.assertIn("Test question for template?", rendered)
        self.assertIn('type="radio"', rendered)
        self.assertIn("Submit Answer", rendered)
        self.assertIn(f'id="question-block-{self.question.pk}"', rendered)
        self.assertIn("Checking answer...", rendered)  # Loading indicator


class PillTemplateTest(TestCase):
    """
    Tests for pill template rendering.
    """

    def test_tutorial_pill_template_renders(self):
        """Test that tutorial pill template renders with correct data attributes."""
        context = {"tutorial_name": "Python Basics"}

        rendered = render_to_string(
            "questions/partials/pills/tutorial_name_pill.html", context
        )

        # Check for required attributes
        self.assertIn('data-pill-type="tutorial"', rendered)
        self.assertIn('data-pill-value="python-basics"', rendered)
        self.assertIn('data-pill-display="Python Basics"', rendered)
        self.assertIn("pill-selectable", rendered)
        self.assertIn("tutorial-name-pill", rendered)
        self.assertIn("Python Basics", rendered)

    def test_tag_pill_template_renders(self):
        """Test that tag pill template renders with correct data attributes."""
        context = {"tag_name": "Machine Learning"}

        rendered = render_to_string(
            "questions/partials/pills/tag_name_pill.html", context
        )

        # Check for required attributes
        self.assertIn('data-pill-type="tag"', rendered)
        self.assertIn('data-pill-value="machine-learning"', rendered)
        self.assertIn('data-pill-display="Machine Learning"', rendered)
        self.assertIn("pill-selectable", rendered)
        self.assertIn("tag-name-pill", rendered)
        self.assertIn("Machine Learning", rendered)

    def test_selected_filters_template_renders(self):
        """Test that selected filters template renders correctly."""
        rendered = render_to_string("questions/partials/selected_filters.html")

        # Check for container elements
        self.assertIn('id="selected-filters-container"', rendered)
        self.assertIn('id="selected-pills-list"', rendered)
        self.assertIn("Selected Filters", rendered)
        self.assertIn("No filters selected", rendered)
