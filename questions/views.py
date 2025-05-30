# questions/views.py
import logging
from typing import List
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from .models import Question, TutorialTitle

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
    context = {
        'questions': Question.objects.none(), # To be populated by the view
        'error_message': None,
        } 

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


def question_page_view(request: HttpRequest) -> HttpResponse:
    """
    Renders the main interactive quiz page.
    """
    initial_questions_namespaced_ids = Question.objects.get_initial_questions()
    initial_tags = Question.objects.get_initial_tags()
    
    initial_title_ids = TutorialTitle.objects.get_initial_titles()
    initial_title_names = []
    
    for title_id in initial_title_ids:
        initial_title_names.append(_generate_readable_name_from_slug(title_id))
    
    print(f"titles ids : {initial_title_ids}")
    print(f"titles names : {initial_title_names}")
    initial_questions: List[Question] = []
    
    for q_tuple in initial_questions_namespaced_ids:
        question = Question.objects.get(
            tutorial_title__title_id_slug=q_tuple[0],
            question_id_slug=q_tuple[1]
            )
        initial_questions.append(question)
    
    context = {
        'sidebar_header': 'Interactive Quiz',
        'initial_questions': initial_questions,
        'initial_tags': initial_tags,
        'initial_title_ids': initial_title_ids,
        'initial_title_names': initial_title_names,
        
    } 
    return render(request, 'questions/quiz_page.html', context)

# TODO: move this to a utils file
def _generate_readable_name_from_slug(title_id_slug: str) -> str:
        """
        Helper method to generate a human-readable name from the title_id_slug.
        Example: '01-first-contribution' -> '01 First Contribution'
        """
        if not title_id_slug:
            return ""
        
        parts = title_id_slug.split('-')
        # Capitalize each part. For "01", .capitalize() keeps it "01".
        # For "first", .capitalize() makes it "First".
        processed_parts = [part.capitalize() for part in parts]
        return " ".join(processed_parts)