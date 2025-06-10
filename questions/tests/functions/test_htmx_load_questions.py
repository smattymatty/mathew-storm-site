# questions/tests/functions/test_htmx_load_questions.py

from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.http import HttpResponseForbidden
from django.template.response import TemplateResponse

from questions.views import htmx_load_questions
from questions.models import Question, TutorialTitle


class TestHtmxLoadQuestions(TestCase):
    """
    Tests for the htmx_load_questions view function.
    """

    def setUp(self):
        """Set up test data and request factory."""
        self.factory = RequestFactory()

        # Create test data
        self.tutorial_title = TutorialTitle.objects.create(
            title_id_slug='test-tutorial',
            name='Test Tutorial'
        )

        self.question = Question.objects.create(
            tutorial_title=self.tutorial_title,
            question_id_slug='test-question',
            question_text='What is a test?',
            answer_a='Option A',
            answer_b='Option B',
            answer_c='Option C',
            answer_d='Option D',
            correct_answer='a',
            difficulty='easy'
        )
        self.question.tags.add('test-tag', 'another-tag')

    def test_non_htmx_request_returns_forbidden(self):
        """Test that non-HTMX requests return HTTP 403 Forbidden."""
        request = self.factory.get('/htmx/load-questions/')
        # Don't set request.htmx attribute to simulate non-HTMX request

        response = htmx_load_questions(request)

        self.assertIsInstance(response, HttpResponseForbidden)
        self.assertEqual(response.content, b"This endpoint is for HTMX requests only.")

    @patch('questions.views.logger')
    def test_non_htmx_request_logs_warning(self, mock_logger):
        """Test that non-HTMX requests log a warning."""
        request = self.factory.get('/htmx/load-questions/')

        htmx_load_questions(request)

        mock_logger.warning.assert_called_once_with(
            "Non-HTMX request received at htmx_load_questions endpoint."
        )

    def test_htmx_request_without_parameters_returns_all_questions(self):
        """Test HTMX request without filter parameters returns questions."""
        request = self.factory.get('/htmx/load-questions/')
        request.htmx = True  # Mock HTMX request

        with patch('questions.views.Question.objects.get_queryset') as mock_queryset:
            mock_quiz_questions = MagicMock()
            mock_queryset.return_value.get_interactive_quiz_questions.return_value = mock_quiz_questions

            response = htmx_load_questions(request)

            # Verify queryset method was called with correct parameters
            mock_queryset.return_value.get_interactive_quiz_questions.assert_called_once_with(
                title_id_slug=None,
                difficulty_levels=None,
                tag_names=None
            )

            # Check response
            self.assertIsInstance(response, TemplateResponse)
            self.assertEqual(response.template_name, 'questions/partials/_question_list_htmx.html')
            self.assertEqual(response.context_data['questions'], mock_quiz_questions)
            self.assertIsNone(response.context_data['error_message'])

    def test_htmx_request_with_difficulty_parameter(self):
        """Test HTMX request with difficulty filter."""
        request = self.factory.get('/htmx/load-questions/', {'difficulty': 'easy,medium'})
        request.htmx = True

        with patch('questions.views.Question.objects.get_queryset') as mock_queryset:
            mock_quiz_questions = MagicMock()
            mock_queryset.return_value.get_interactive_quiz_questions.return_value = mock_quiz_questions

            response = htmx_load_questions(request)

            # Verify difficulty levels were processed correctly
            mock_queryset.return_value.get_interactive_quiz_questions.assert_called_once_with(
                title_id_slug=None,
                difficulty_levels=['easy', 'medium'],
                tag_names=None
            )

    def test_htmx_request_with_tags_parameter(self):
        """Test HTMX request with tags filter."""
        request = self.factory.get('/htmx/load-questions/', {'tags': 'python,django'})
        request.htmx = True

        with patch('questions.views.Question.objects.get_queryset') as mock_queryset:
            mock_quiz_questions = MagicMock()
            mock_queryset.return_value.get_interactive_quiz_questions.return_value = mock_quiz_questions

            response = htmx_load_questions(request)

            # Verify tags were processed correctly
            mock_queryset.return_value.get_interactive_quiz_questions.assert_called_once_with(
                title_id_slug=None,
                difficulty_levels=None,
                tag_names=['python', 'django']
            )

    def test_htmx_request_with_title_id_parameter(self):
        """Test HTMX request with title-id filter."""
        request = self.factory.get('/htmx/load-questions/', {'title-id': 'test-tutorial'})
        request.htmx = True

        with patch('questions.views.Question.objects.get_queryset') as mock_queryset:
            mock_quiz_questions = MagicMock()
            mock_queryset.return_value.get_interactive_quiz_questions.return_value = mock_quiz_questions

            response = htmx_load_questions(request)

            # Verify title ID was processed correctly
            mock_queryset.return_value.get_interactive_quiz_questions.assert_called_once_with(
                title_id_slug='test-tutorial',
                difficulty_levels=None,
                tag_names=None
            )

    @patch('questions.views.logger')
    def test_htmx_request_with_exception_returns_error(self, mock_logger):
        """Test that exceptions are handled gracefully and return error message."""
        request = self.factory.get('/htmx/load-questions/')
        request.htmx = True

        with patch('questions.views.Question.objects.get_queryset') as mock_queryset:
            mock_queryset.return_value.get_interactive_quiz_questions.side_effect = Exception("Database error")

            response = htmx_load_questions(request)

            # Check error handling
            self.assertIsInstance(response, TemplateResponse)
            self.assertEqual(response.context_data['error_message'],
                           "Sorry, an unexpected error occurred while trying to load questions. "
                           "Please try again later or contact support if the issue persists.")

            # Verify logging
            mock_logger.error.assert_called_once()

    @patch('questions.views.logger')
    def test_debug_logging_with_parameters(self, mock_logger):
        """Test that debug logging works correctly with parameters."""
        request = self.factory.get('/htmx/load-questions/', {
            'title-id': 'test-tutorial',
            'difficulty': 'easy',
            'tags': 'python'
        })
        request.htmx = True

        with patch('questions.views.Question.objects.get_queryset') as mock_queryset:
            mock_quiz_questions = MagicMock()
            mock_queryset.return_value.get_interactive_quiz_questions.return_value = mock_quiz_questions

            htmx_load_questions(request)

            # Verify debug logging
            mock_logger.debug.assert_called_once_with(
                "HTMX request received with params: title-id='test-tutorial', "
                "difficulty='easy', tags='python'"
            )

    def test_empty_difficulty_and_tags_parameters(self):
        """Test handling of empty difficulty and tags parameters."""
        request = self.factory.get('/htmx/load-questions/', {
            'difficulty': '',
            'tags': '   ',  # Whitespace only
        })
        request.htmx = True

        with patch('questions.views.Question.objects.get_queryset') as mock_queryset:
            mock_quiz_questions = MagicMock()
            mock_queryset.return_value.get_interactive_quiz_questions.return_value = mock_quiz_questions

            response = htmx_load_questions(request)

            # Empty parameters should be treated as None
            mock_queryset.return_value.get_interactive_quiz_questions.assert_called_once_with(
                title_id_slug=None,
                difficulty_levels=None,
                tag_names=None
            )
