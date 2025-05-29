# questions/views.py
import logging
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from .models import Question 

logger = logging.getLogger(__name__)

def htmx_load_questions(request: HttpRequest) -> HttpResponse:
    """
    View to load questions based on GET parameters, intended exclusively for HTMX requests.
    Returns an HTML fragment to be swapped into the page by HTMX.
    """
    # 1. Ensure this is an HTMX request
    if not getattr(request, 'htmx', False): # Check for request.htmx (provided by django-htmx)
        logger.warning("Non-HTMX request received at htmx_load_questions endpoint.")
        return HttpResponseForbidden(b"This endpoint is for HTMX requests only.")

    template_name = 'questions/partials/_question_list_htmx.html'
    context = {'questions': Question.objects.none(), 'error_message': None} # Default context

    try:
        # 2. Extract and process filter parameters from GET request
        title_id_slug = request.GET.get('title-id', None)
        difficulty_levels_str = request.GET.get('difficulty', None)
        tag_names_str = request.GET.get('tags', None)

        logger.debug(
            f"HTMX request received with params: title-id='{title_id_slug}', "
            f"difficulty='{difficulty_levels_str}', tags='{tag_names_str}'"
        )

        difficulty_levels = []
        if difficulty_levels_str:
            difficulty_levels = [level.strip().lower() for level in difficulty_levels_str.split(',') if level.strip()]

        tag_names = []
        if tag_names_str:
            tag_names = [tag.strip() for tag in tag_names_str.split(',') if tag.strip()]

        # 3. Call your querying logic
        questions_queryset = Question.objects.get_queryset().get_interactive_quiz_questions(
            title_id_slug=title_id_slug,
            difficulty_levels=difficulty_levels if difficulty_levels else None,
            tag_names=tag_names if tag_names else None
        )
        context['questions'] = questions_queryset

    except Exception as e:
        # 4. Handle unexpected errors during parameter processing or querying
        logger.error(f"Error processing htmx_load_questions: {e}", exc_info=True)
        context['error_message'] = (
            "Sorry, an unexpected error occurred while trying to load questions. "
            "Please try again later or contact support if the issue persists."
        )

    # 5. Render the HTML partial and return it
    return render(request, template_name, context)