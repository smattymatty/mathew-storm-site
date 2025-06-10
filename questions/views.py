# questions/views.py
import logging
from typing import List, Dict, Any

from django.db import models
from django.template.response import TemplateResponse
from django.http import HttpRequest, HttpResponseForbidden
from .models import Question, TutorialTitle

from .utils import generate_readable_name_from_slug

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
    # 1. Ensure this is an HTMX request
    if not getattr(request, "htmx", False):
        # Check for request.htmx (provided by django-htmx)
        logger.warning(
            "Non-HTMX request received at htmx_load_questions endpoint."
        )
        return HttpResponseForbidden(
            b"This endpoint is for HTMX requests only."
        )

    template_name = "questions/partials/_question_list_htmx.html"
    context = {
        "questions": Question.objects.none(),  # To be populated by the view
        "error_message": None,
    }

    try:
        # 2. Extract and process filter parameters from GET request
        title_id_slug = request.GET.get("title-id", None)
        difficulty_levels_str: str = request.GET.get("difficulty", None)
        tag_names_str = request.GET.get("tags", None)

        logger.debug(
            f"HTMX request received with params: title-id='{title_id_slug}', "
            f"difficulty='{difficulty_levels_str}', tags='{tag_names_str}'"
        )

        difficulty_levels = []
        if difficulty_levels_str:
            difficulty_levels = [
                level.strip().lower()
                for level in difficulty_levels_str.split(",")
                if level.strip()
            ]

        tag_names = []
        if tag_names_str:
            tag_names = [
                tag.strip() for tag in tag_names_str.split(",") if tag.strip()
            ]

        # 3. Call your querying logic
        questions_queryset = (
            Question.objects.get_queryset().get_interactive_quiz_questions(
                title_id_slug=title_id_slug,
                difficulty_levels=difficulty_levels
                if difficulty_levels
                else None,
                tag_names=tag_names if tag_names else None,
            )
        )
        context["questions"] = questions_queryset

    except Exception as e:
        # 4. Handle unexpected errors during parameter processing or querying
        logger.error(
            f"Error processing htmx_load_questions: {e}", exc_info=True
        )
        context["error_message"] = (
            "Sorry, an unexpected error occurred while trying to load questions. "
            "Please try again later or contact support if the issue persists."
        )

    # 5. Render the HTML partial and return it
    return TemplateResponse(request, template_name, context)


def question_page_view(request: HttpRequest) -> TemplateResponse:
    """
    Renders the interactive quiz page with initial questions, tags, and tutorial titles.

    The view prepares and passes to the template the initial set of quiz questions, available tags, tutorial title slugs, and their human-readable names for display in the sidebar and main content.
    """
    try:  # to get the initial data
        initial_questions_namespaced_ids = (
            Question.objects.get_initial_questions()
        )
        initial_tags = Question.objects.get_initial_tags()
        initial_title_ids = TutorialTitle.objects.get_initial_titles()
    except Exception as e:
        logger.error(f"Error loading initial data: {e}", exc_info=True)
        # Provide fallback values or redirect to error page
        initial_questions_namespaced_ids = []
        initial_tags = []
        initial_title_ids = []

    initial_title_names = []

    for title_id in initial_title_ids:
        initial_title_names.append(generate_readable_name_from_slug(title_id))

    initial_questions: List[Question] = []

    # Build lookup conditions for all questions at once
    conditions = models.Q()
    for q_tuple in initial_questions_namespaced_ids:
        conditions |= models.Q(
            tutorial_title__title_id_slug=q_tuple[0],
            question_id_slug=q_tuple[1],
        )

    initial_questions = list(
        Question.objects.select_related("tutorial_title").filter(conditions)
    )

    context = {
        "sidebar_header": "Interactive Quiz",
        "initial_questions": initial_questions,
        "initial_tags": initial_tags,
        "initial_title_ids": initial_title_ids,
        "initial_title_names": initial_title_names,
    }
    template_name = "questions/quiz_page.html"
    return TemplateResponse(request, template_name, context)


def htmx_search_tutorial_titles(request: HttpRequest) -> TemplateResponse:
    """
    Handles HTMX requests to search and filter tutorial titles based on user input.

    Processes the search query from GET parameters and returns an HTML fragment
    containing matching tutorial title pills for partial page updates.
    """
    # Ensure this is an HTMX request
    if not getattr(request, "htmx", False):
        logger.warning(
            "Non-HTMX request received at htmx_search_tutorial_titles endpoint."
        )
        return HttpResponseForbidden(
            b"This endpoint is for HTMX requests only."
        )

    # Get search query from GET parameters
    search_query = request.GET.get("q_search", "").strip()

    try:
        # Use the manager's search method
        matching_titles = TutorialTitle.objects.search_titles(
            search_query, limit=15
        )

        context: Dict[str, Any] = {
            "tutorial_titles": matching_titles,
            "search_query": search_query,
        }

        logger.debug(
            f"Tutorial title search for '{search_query}' returned {len(matching_titles)} results"
        )

    except Exception as e:
        logger.error(f"Error searching tutorial titles: {e}", exc_info=True)
        context = {
            "tutorial_titles": [],
            "search_query": search_query,
            "error_message": "An error occurred while searching tutorial titles.",
        }
    template_name = "questions/partials/pills/_tutorial_pills_container.html"
    return TemplateResponse(
        request,
        template_name,
        context,
    )


def htmx_search_tag_names(request: HttpRequest) -> TemplateResponse:
    """
    Handles HTMX requests to search and filter tag names based on user input.

    Processes the search query from GET parameters and returns an HTML fragment
    containing matching tag name pills for partial page updates.
    """
    # Ensure this is an HTMX request
    if not getattr(request, "htmx", False):
        logger.warning(
            "Non-HTMX request received at htmx_search_tag_names endpoint."
        )
        return HttpResponseForbidden(
            b"This endpoint is for HTMX requests only."
        )

    # Get search query from GET parameters
    search_query = request.GET.get("q_tag_search", "").strip()

    try:
        # Use the manager's search method
        matching_tags = Question.objects.search_tags(search_query, limit=15)

        context = {
            "tag_names": matching_tags,
            "search_query": search_query,
        }

        logger.debug(
            f"Tag name search for '{search_query}' returned {len(matching_tags)} results"
        )

    except Exception as e:
        logger.error(f"Error searching tag names: {e}", exc_info=True)
        context = {
            "tag_names": [],
            "search_query": search_query,
            "error_message": "An error occurred while searching tag names.",
        }
    template_name = "questions/partials/pills/_tag_pills_container.html"
    return TemplateResponse(
        request,
        template_name,
        context,
    )
