# questions/views.py
import logging

from django.template.response import TemplateResponse
from django.http import HttpRequest

from .logic.views_logic import (
    htmx_load_questions_logic,
    questions_page_view_logic,
    quiz_view_logic,
    search_tutorial_titles_logic,
    search_tag_names_logic,
    check_answer_logic,
    load_single_question_logic,
    skip_question_logic
)

logger = logging.getLogger(__name__)


def htmx_load_questions(request: HttpRequest) -> TemplateResponse:
    """
    Handles HTMX requests to dynamically load and
    filter quiz questions based on GET parameters.

    Processes filter parameters for tutorial title,
    difficulty levels, and tags from the request,
    retrieves matching questions, and returns an
    HTML fragment for partial page updates. If the
    request is not an HTMX request, returns
    HTTP 403 Forbidden. On error, provides a user-friendly
    error message in the rendered fragment.
    """
    return htmx_load_questions_logic(request)


def questions_page_view(request: HttpRequest) -> TemplateResponse:
    """
    Renders the interactive quiz page with initial questions and tutorials.

    The view prepares and passes to the template the initial set of questions,
    available tags, tutorial title slugs, and their human-readable names.
    """
    return questions_page_view_logic(request)


def quiz_view(request: HttpRequest) -> TemplateResponse:
    """
    Renders the dedicated quiz-taking interface.

    Processes URL parameters to configure the quiz based on selected filters
    from the questions page. Supports parameters: tags, titles, difficulty.
    """
    return quiz_view_logic(request)


def htmx_search_tutorial_titles(request: HttpRequest) -> TemplateResponse:
    """
    Handles HTMX requests to search and filter tutorial titles.

    Processes the search query from GET parameters and returns an HTML fragment
    containing matching tutorial title pills for partial page updates.
    """
    return search_tutorial_titles_logic(request)


def htmx_search_tag_names(request: HttpRequest) -> TemplateResponse:
    """
    Handles HTMX requests to search and filter tag names.

    Processes the search query from GET parameters and returns an HTML fragment
    containing matching tag name pills for partial page updates.
    """
    return search_tag_names_logic(request)


def htmx_check_answer(
    request: HttpRequest, question_pk: int
) -> TemplateResponse:
    """
    Handles HTMX POST requests to check user's answer submission.

    Validates the submitted answer against the correct answer and returns
    appropriate feedback HTML fragment.
    """
    return check_answer_logic(request, question_pk)


def htmx_load_single_question(
    request: HttpRequest, question_pk: int
) -> TemplateResponse:
    """
    Handles HTMX GET requests to load a single question block.

    Used for the "Try Again" functionality to reload the original question.
    """
    return load_single_question_logic(request, question_pk)


def htmx_skip_question(
    request: HttpRequest, question_pk: int
) -> TemplateResponse:
    """
    Handles HTMX POST requests when users skip a question.
    Records the skip in analytics and provides appropriate feedback.
    """
    return skip_question_logic(request, question_pk)
