# questions/logic/views_logic.py
import logging
from typing import List, Dict, Any, Optional, Tuple, Union
from django.http import HttpRequest, HttpResponseForbidden
from django.template.response import TemplateResponse
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from ..models import Question

User = get_user_model()

logger = logging.getLogger(__name__)


def validate_htmx_request(request: HttpRequest) -> Optional[HttpResponseForbidden]:
    """
    Validates that the request is an HTMX request.

    Args:
        request: The HTTP request object

    Returns:
        HttpResponseForbidden if not HTMX request, None if valid
    """
    if not getattr(request, "htmx", False):
        logger.warning("Non-HTMX request received at HTMX endpoint.")
        return HttpResponseForbidden(b"This endpoint is for HTMX requests only.")
    return None


def parse_filter_parameters(request: HttpRequest) -> Tuple[List[str], List[str], List[str]]:
    """
    Extracts and parses filter parameters from GET request.

    Args:
        request: The HTTP request object

    Returns:
        Tuple of (title_id_slugs, difficulty_levels, tag_names) lists
    """
    # Extract raw parameters
    title_id_slugs_str = request.GET.get("title-id", None)
    difficulty_levels_str = request.GET.get("difficulty", None)
    tag_names_str = request.GET.get("tags", None)

    logger.debug(
        f"HTMX request received with params: title-id='{title_id_slugs_str}', "
        f"difficulty='{difficulty_levels_str}', tags='{tag_names_str}'"
    )

    # Parse title slugs
    title_id_slugs = []
    if title_id_slugs_str:
        title_id_slugs = [
            slug.strip()
            for slug in title_id_slugs_str.split(",")
            if slug.strip()
        ]

    # Parse difficulty levels
    difficulty_levels = []
    if difficulty_levels_str:
        difficulty_levels = [
            level.strip().lower()
            for level in difficulty_levels_str.split(",")
            if level.strip()
        ]

    # Parse tag names
    tag_names = []
    if tag_names_str:
        tag_names = [
            tag.strip() for tag in tag_names_str.split(",") if tag.strip()
        ]

    return title_id_slugs, difficulty_levels, tag_names


def get_filtered_questions(
    title_id_slugs: Optional[List[str]] = None,
    difficulty_levels: Optional[List[str]] = None,
    tag_names: Optional[List[str]] = None
) -> QuerySet[Question]:
    """
    Retrieves questions based on filter criteria with optimized queries.

    Args:
        title_id_slugs: List of tutorial title slugs to filter by
        difficulty_levels: List of difficulty levels to filter by
        tag_names: List of tag names to filter by

    Returns:
        Optimized QuerySet of filtered questions
    """
    questions_queryset = (
        Question.objects.get_queryset().get_interactive_quiz_questions(
            title_id_slugs=title_id_slugs if title_id_slugs else None,
            difficulty_levels=(
                difficulty_levels if difficulty_levels else None
            ),
            tag_names=tag_names if tag_names else None,
        )
    )

    # Optimize queries with select_related and prefetch_related
    questions_queryset = questions_queryset.select_related(
        "tutorial_title", "stats"
    )

    return questions_queryset


def calculate_question_set_stats(questions_queryset: QuerySet[Question]) -> Dict[str, Any]:
    """
    Calculates analytics statistics for a set of questions.

    Args:
        questions_queryset: QuerySet of questions to analyze

    Returns:
        Dictionary containing aggregated statistics
    """
    question_set_stats = {}
    if not questions_queryset.exists():
        return question_set_stats

    questions_with_stats = [
        q for q in questions_queryset
        if hasattr(q, "stats") and getattr(q, "stats", None) is not None
    ]
    total_questions = questions_queryset.count()
    questions_with_data = len(questions_with_stats)
    if questions_with_stats:
        success_rates = [
            float(q.stats.success_rate) for q in questions_with_stats
        ]
        avg_success_rate = sum(success_rates) / len(success_rates)
        question_set_stats = {
            "total_questions": total_questions,
            "questions_with_data": questions_with_data,
            "avg_success_rate": round(avg_success_rate, 1),
            "difficulty_rating": round(100 - avg_success_rate, 1),
            "data_coverage": round(
                (questions_with_data / total_questions) * 100, 1
            ),
            "min_success_rate": round(min(success_rates), 1),
            "max_success_rate": round(max(success_rates), 1),
        }
    else:
        question_set_stats = {
            "total_questions": total_questions,
            "questions_with_data": 0,
            "avg_success_rate": 0.0,
            "difficulty_rating": 0.0,
            "data_coverage": 0.0,
            "min_success_rate": 0.0,
            "max_success_rate": 0.0,
        }

    return question_set_stats


def build_question_context(
    questions_queryset: QuerySet[Question],
    question_set_stats: Dict[str, Any],
    error_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Builds the context dictionary for question templates.

    Args:
        questions_queryset: QuerySet of questions
        question_set_stats: Analytics statistics
        error_message: Optional error message

    Returns:
        Context dictionary for template rendering
    """
    return {
        "questions": questions_queryset,
        "question_set_stats": question_set_stats,
        "error_message": error_message,
        "has_questions": questions_queryset.exists(),
        "questions_count": questions_queryset.count(),
    }


def htmx_load_questions_logic(request: HttpRequest) -> Union[TemplateResponse, HttpResponseForbidden]:
    """
    Handles HTMX requests to dynamically load and filter quiz questions.

    Refactored version of the original htmx_load_questions view with improved
    separation of concerns and testability.

    Args:
        request: HTTP request object

    Returns:
        TemplateResponse with filtered questions and analytics
    """
    # 1. Validate HTMX request
    htmx_validation_error = validate_htmx_request(request)
    if htmx_validation_error:
        return htmx_validation_error

    template_name = "questions/partials/_question_list_htmx.html"

    try:
        # 2. Parse filter parameters
        title_id_slugs, difficulty_levels, tag_names = (
            parse_filter_parameters(request)
        )

        # 3. Get filtered questions
        questions_queryset = get_filtered_questions(
            title_id_slugs=title_id_slugs,
            difficulty_levels=difficulty_levels,
            tag_names=tag_names
        )

        # 4. Calculate analytics
        question_set_stats = calculate_question_set_stats(questions_queryset)

        # 5. Build context
        context = build_question_context(
            questions_queryset=questions_queryset,
            question_set_stats=question_set_stats
        )

        logger.debug(
            f"Successfully loaded {context['questions_count']} questions with "
            f"{question_set_stats.get('questions_with_data', 0)} having data"
        )

    except Exception as e:
        # Handle unexpected errors during processing
        logger.error(f"Error processing htmx_load_questions: {e}", exc_info=True)
        
        error_context = build_question_context(
            questions_queryset=Question.objects.none(),
            question_set_stats={},
            error_message=(
                "Sorry, an unexpected error occurred while trying to load "
                "questions. Please try again later or contact support if "
                "the issue persists."
            )
        )

        return TemplateResponse(request, template_name, error_context)

    return TemplateResponse(request, template_name, context)


def get_question_difficulty_distribution(
    questions_queryset: QuerySet[Question]
) -> Dict[str, int]:
    """
    Calculates the distribution of questions by difficulty level.

    Args:
        questions_queryset: QuerySet of questions to analyze

    Returns:
        Dictionary mapping difficulty levels to question counts
    """
    from django.db.models import Count

    difficulty_distribution = {}

    if questions_queryset.exists():
        distribution_data = questions_queryset.values('difficulty').annotate(
            count=Count('difficulty')
        ).order_by('difficulty')

        difficulty_distribution = {
            item['difficulty']: item['count']
            for item in distribution_data
        }

    return difficulty_distribution


def get_tutorial_distribution(
    questions_queryset: QuerySet[Question]
) -> Dict[str, int]:
    """
    Calculates the distribution of questions by tutorial.

    Args:
        questions_queryset: QuerySet of questions to analyze

    Returns:
        Dictionary mapping tutorial titles to question counts
    """
    from django.db.models import Count

    tutorial_distribution = {}

    if questions_queryset.exists():
        distribution_data = questions_queryset.values(
            'tutorial_title__title_id_slug',
            'tutorial_title__name'
        ).annotate(
            count=Count('tutorial_title')
        ).order_by('tutorial_title__title_id_slug')

        tutorial_distribution = {
            (item['tutorial_title__name'] or 
             item['tutorial_title__title_id_slug']): item['count']
            for item in distribution_data
        }

    return tutorial_distribution


# =================== QUESTIONS PAGE VIEW LOGIC ===================

def get_initial_data() -> Tuple[List[Tuple], List[str], List[str]]:
    """
    Retrieves initial data for the questions page.

    Returns:
        Tuple of (initial_questions_namespaced_ids, initial_tags, initial_title_ids)
    """
    from ..models import TutorialTitle
    try:
        initial_questions_namespaced_ids = Question.objects.get_initial_questions()
        initial_tags = Question.objects.get_initial_tags()
        initial_title_ids = TutorialTitle.objects.get_initial_titles()
        return initial_questions_namespaced_ids, initial_tags, initial_title_ids
    except Exception as e:
        logger.error(f"Error loading initial data: {e}", exc_info=True)
        return [], [], []


def generate_title_names(title_ids: List[str]) -> List[str]:
    """
    Generates readable names from title slugs.

    Args:
        title_ids: List of title ID slugs

    Returns:
        List of human-readable title names
    """
    from ..utils import generate_readable_name_from_slug
    title_names = []
    for title_id in title_ids:
        title_names.append(generate_readable_name_from_slug(title_id))
    return title_names


def get_initial_questions_optimized(
    initial_questions_namespaced_ids: List[Tuple]
) -> List[Question]:
    """
    Retrieves initial questions with optimized queries.

    Args:
        initial_questions_namespaced_ids: List of (tutorial_slug, question_slug) tuples

    Returns:
        List of Question objects with prefetched stats
    """
    from django.db import models
    if not initial_questions_namespaced_ids:
        return []

    # Build lookup conditions for all questions at once
    conditions = models.Q()
    for q_tuple in initial_questions_namespaced_ids:
        conditions |= models.Q(
            tutorial_title__title_id_slug=q_tuple[0],
            question_id_slug=q_tuple[1],
        )

    # Prefetch stats for better performance
    initial_questions = list(
        Question.objects.select_related("tutorial_title")
        .prefetch_related("stats")
        .filter(conditions)
    )
    return initial_questions


def get_tutorial_analytics(title_ids: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Calculates tutorial-level analytics for given tutorial IDs.

    Args:
        title_ids: List of tutorial ID slugs

    Returns:
        Dictionary mapping tutorial IDs to their analytics
    """
    from ..models import TutorialTitle
    tutorial_stats = {}

    try:
        for title_id in title_ids:
            try:
                tutorial = TutorialTitle.objects.get(title_id_slug=title_id)
                # Force creation of stats if they don't exist
                tutorial.update_tutorial_stats()

                if hasattr(tutorial, "stats"):
                    tutorial_stats[title_id] = {
                        "completion_rate": float(tutorial.stats.completion_rate),
                        "average_score": float(tutorial.stats.average_score),
                        "total_attempts": tutorial.stats.total_attempts,
                        "question_count": tutorial.questions.count(),
                    }
                else:
                    # Fallback for tutorials without stats
                    tutorial_stats[title_id] = {
                        "completion_rate": 0.0,
                        "average_score": 0.0,
                        "total_attempts": 0,
                        "question_count": tutorial.questions.count(),
                    }
            except TutorialTitle.DoesNotExist:
                logger.warning(f"Tutorial with slug '{title_id}' not found")
                continue
    except Exception as e:
        logger.error(f"Error loading tutorial stats: {e}", exc_info=True)
    return tutorial_stats


def get_platform_analytics() -> Dict[str, Any]:
    """
    Calculates platform-wide analytics.

    Returns:
        Dictionary containing platform statistics
    """
    platform_stats = {}
    try:
        from django.db.models import Count, Avg

        total_questions = Question.objects.count()
        questions_with_stats = Question.objects.filter(
            stats__isnull=False
        ).count()

        if questions_with_stats > 0:
            avg_success_rate = Question.objects.filter(
                stats__isnull=False
            ).aggregate(avg_rate=Avg("stats__success_rate"))["avg_rate"]

            platform_stats = {
                "total_questions": total_questions,
                "questions_with_data": questions_with_stats,
                "average_success_rate": round(
                    float(avg_success_rate or 0), 1
                ),
                "data_coverage": round(
                    (questions_with_stats / total_questions) * 100, 1
                ) if total_questions > 0 else 0,
            }
        else:
            platform_stats = {
                "total_questions": total_questions,
                "questions_with_data": 0,
                "average_success_rate": 0.0,
                "data_coverage": 0.0,
            }
    except Exception as e:
        logger.error(f"Error calculating platform stats: {e}", exc_info=True)
    return platform_stats


def questions_page_view_logic(request: HttpRequest) -> TemplateResponse:
    """
    Logic for rendering the interactive quiz page.

    Refactored version with improved separation of concerns and testability.

    Args:
        request: HTTP request object

    Returns:
        TemplateResponse with initial page data and analytics
    """
    # 1. Get initial data
    initial_questions_namespaced_ids, initial_tags, initial_title_ids = (
        get_initial_data()
    )

    # 2. Generate readable names
    initial_title_names = generate_title_names(initial_title_ids)

    # 3. Get initial questions with optimized queries
    initial_questions = get_initial_questions_optimized(
        initial_questions_namespaced_ids
    )

    # 4. Get tutorial analytics
    tutorial_stats = get_tutorial_analytics(initial_title_ids)

    # 5. Get platform analytics
    platform_stats = get_platform_analytics()

    # 6. Build context
    context = {
        "sidebar_header": None,
        "initial_questions": initial_questions,
        "initial_tags": initial_tags,
        "initial_title_ids": initial_title_ids,
        "initial_title_names": initial_title_names,
        "tutorial_stats": tutorial_stats,
        "platform_stats": platform_stats,
    }
    template_name = "questions/questions_page.html"
    return TemplateResponse(request, template_name, context)


# =================== QUIZ VIEW LOGIC ===================

def parse_quiz_parameters(request: HttpRequest) -> Tuple[List[str], List[str], List[str]]:
    """
    Parses quiz filter parameters from URL.

    Args:
        request: HTTP request object

    Returns:
        Tuple of (tag_names, title_id_slugs, difficulty_levels)
    """
    # Extract filter parameters from URL
    tags_param = request.GET.get("tags", "")
    titles_param = request.GET.get("titles", "")
    difficulty_param = request.GET.get("difficulty", "")

    # Parse parameters
    tag_names = (
        [tag.strip() for tag in tags_param.split(",") if tag.strip()]
        if tags_param
        else []
    )
    title_id_slugs = (
        [title.strip() for title in titles_param.split(",") if title.strip()]
        if titles_param
        else []
    )
    difficulty_levels = (
        [
            level.strip().lower()
            for level in difficulty_param.split(",")
            if level.strip()
        ]
        if difficulty_param
        else []
    )

    logger.debug(
        f"Quiz view params: tags={tag_names}, titles={title_id_slugs}, "
        f"difficulty={difficulty_levels}"
    )
    return tag_names, title_id_slugs, difficulty_levels


def get_quiz_questions_and_initial_data(
    title_id_slugs: List[str],
    difficulty_levels: List[str],
    tag_names: List[str]
) -> Tuple[QuerySet[Question], List[str], List[str], List[str]]:
    """
    Gets quiz questions and initial data for filter options.

    Args:
        title_id_slugs: List of tutorial title slugs to filter by
        difficulty_levels: List of difficulty levels to filter by
        tag_names: List of tag names to filter by

    Returns:
        Tuple of (quiz_questions, initial_tags, initial_title_ids, initial_title_names)
    """
    from ..models import TutorialTitle
    try:
        # Get quiz questions based on parameters
        quiz_questions = get_filtered_questions(
            title_id_slugs=title_id_slugs if title_id_slugs else None,
            difficulty_levels=difficulty_levels if difficulty_levels else None,
            tag_names=tag_names if tag_names else None,
        )

        # Get initial data for filter options (for display purposes)
        initial_tags = Question.objects.get_initial_tags()
        initial_title_ids = TutorialTitle.objects.get_initial_titles()
        initial_title_names = generate_title_names(initial_title_ids)
        return quiz_questions, initial_tags, initial_title_ids, initial_title_names
    except Exception as e:
        logger.error(f"Error loading quiz data: {e}", exc_info=True)
        return Question.objects.none(), [], [], []


def calculate_quiz_stats(quiz_questions: QuerySet[Question]) -> Dict[str, Any]:
    """
    Calculates statistics for the quiz question set.

    Args:
        quiz_questions: QuerySet of quiz questions

    Returns:
        Dictionary containing quiz statistics
    """
    quiz_stats = {}
    if quiz_questions.exists():
        total_questions = quiz_questions.count()
        questions_with_stats = quiz_questions.filter(
            stats__isnull=False
        ).count()

        if questions_with_stats > 0:
            avg_difficulty = (
                sum(
                    q.get_current_stats()["success_rate"]
                    for q in quiz_questions
                    if hasattr(q, "stats")
                )
                / questions_with_stats
            )

            quiz_stats = {
                "total_questions": total_questions,
                "questions_with_stats": questions_with_stats,
                "average_difficulty": round(100 - avg_difficulty, 1),
                "data_coverage": round(
                    (questions_with_stats / total_questions) * 100, 1
                ),
            }
        else:
            quiz_stats = {
                "total_questions": total_questions,
                "questions_with_stats": 0,
                "average_difficulty": 0.0,
                "data_coverage": 0.0,
            }
    return quiz_stats


def quiz_view_logic(request: HttpRequest) -> TemplateResponse:
    """
    Logic for rendering the dedicated quiz-taking interface.

    Refactored version with improved separation of concerns and testability.

    Args:
        request: HTTP request object

    Returns:
        TemplateResponse with quiz data and analytics
    """
    # 1. Parse quiz parameters
    tag_names, title_id_slugs, difficulty_levels = parse_quiz_parameters(
        request
    )

    # 2. Get quiz questions and initial data
    quiz_questions, initial_tags, initial_title_ids, initial_title_names = (
        get_quiz_questions_and_initial_data(
            title_id_slugs, difficulty_levels, tag_names
        )
    )

    # 3. Calculate quiz statistics
    quiz_stats = calculate_quiz_stats(quiz_questions)

    # 4. Build context
    context = {
        "quiz_questions": quiz_questions,
        "quiz_question_count": quiz_questions.count(),
        "selected_tags": tag_names,
        "selected_titles": title_id_slugs,
        "selected_difficulty": difficulty_levels,
        "initial_tags": initial_tags,
        "initial_title_ids": initial_title_ids,
        "initial_title_names": initial_title_names,
        "quiz_stats": quiz_stats,
    }

    template_name = "questions/quiz_interface.html"
    return TemplateResponse(request, template_name, context)


# =================== SEARCH VIEWS LOGIC ===================

def search_tutorial_titles_logic(request: HttpRequest) -> Union[TemplateResponse, HttpResponseForbidden]:
    """
    Logic for handling HTMX requests to search and filter tutorial titles.

    Refactored version with improved separation of concerns and testability.

    Args:
        request: HTTP request object

    Returns:
        TemplateResponse with matching tutorial title pills
    """
    from ..models import TutorialTitle
    
    # 1. Validate HTMX request
    htmx_validation_error = validate_htmx_request(request)
    if htmx_validation_error:
        return htmx_validation_error

    # 2. Get search query from GET parameters
    search_query = request.GET.get("q_search", "").strip()

    try:
        # 3. Use the manager's search method
        matching_titles = TutorialTitle.objects.search_titles(
            search_query, limit=15
        )

        context: Dict[str, Any] = {
            "tutorial_titles": matching_titles,
            "search_query": search_query,
        }

        logger.debug(
            f"Tutorial title search for '{search_query}' returned "
            f"{len(matching_titles)} results"
        )

    except Exception as e:
        logger.error(f"Error searching tutorial titles: {e}", exc_info=True)
        context = {
            "tutorial_titles": [],
            "search_query": search_query,
            "error_message": "An error occurred while searching tutorial titles.",
        }
    template_name = "questions/partials/pills/_tutorial_pills_container.html"
    return TemplateResponse(request, template_name, context)


def search_tag_names_logic(request: HttpRequest) -> Union[TemplateResponse, HttpResponseForbidden]:
    """
    Logic for handling HTMX requests to search and filter tag names.

    Refactored version with improved separation of concerns and testability.

    Args:
        request: HTTP request object

    Returns:
        TemplateResponse with matching tag name pills
    """
    # 1. Validate HTMX request
    htmx_validation_error = validate_htmx_request(request)
    if htmx_validation_error:
        return htmx_validation_error

    # 2. Get search query from GET parameters
    search_query = request.GET.get("q_tag_search", "").strip()

    try:
        # 3. Use the manager's search method
        matching_tags = Question.objects.search_tags(search_query, limit=15)

        context = {
            "tag_names": matching_tags,
            "search_query": search_query,
        }

        logger.debug(
            f"Tag name search for '{search_query}' returned "
            f"{len(matching_tags)} results"
        )

    except Exception as e:
        logger.error(f"Error searching tag names: {e}", exc_info=True)
        context = {
            "tag_names": [],
            "search_query": search_query,
            "error_message": "An error occurred while searching tag names.",
        }
    template_name = "questions/partials/pills/_tag_pills_container.html"
    return TemplateResponse(request, template_name, context)


# =================== ANSWER CHECKING LOGIC ===================

def validate_htmx_post_request(request: HttpRequest) -> Optional[HttpResponseForbidden]:
    """
    Validates that the request is an HTMX POST request.

    Args:
        request: The HTTP request object

    Returns:
        HttpResponseForbidden if invalid, None if valid
    """
    # Ensure this is an HTMX request
    if not getattr(request, "htmx", False):
        logger.warning("Non-HTMX request received at HTMX endpoint.")
        return HttpResponseForbidden(b"This endpoint is for HTMX requests only.")

    # Only accept POST requests
    if request.method != "POST":
        logger.warning(
            f"Invalid method {request.method} received at HTMX POST endpoint."
        )
        return HttpResponseForbidden(
            b"This endpoint only accepts POST requests."
        )

    return None


def get_question_by_pk(question_pk: int) -> Question:
    """
    Retrieves a question by primary key with optimized queries.

    Args:
        question_pk: Primary key of the question

    Returns:
        Question object with related data

    Raises:
        Question.DoesNotExist: If question not found
    """
    return Question.objects.select_related("tutorial_title").get(pk=question_pk)


def process_answer_submission(request: HttpRequest, question: Question, question_pk: int) -> Dict[str, Any]:
    """
    Processes the user's answer submission and returns result data.

    Args:
        request: HTTP request object
        question: Question object
        question_pk: Question primary key

    Returns:
        Dictionary containing answer processing results

    Raises:
        ValueError: If no answer submitted or invalid data
    """
    # Get submitted answer
    submitted_answer = (
        request.POST.get(f"answer_for_q{question_pk}", "").strip().lower()
    )

    if not submitted_answer:
        raise ValueError("Please select an answer before submitting.")

    # Get user and time data
    auth_user = request.user if request.user.is_authenticated else None
    time_spent = int(request.POST.get("time_spent_seconds", 0))

    # Use the new retrieve_answer method
    result = question.retrieve_answer(
        selected_answer=submitted_answer,
        user=auth_user if auth_user and auth_user.is_authenticated else None,
        time_spent_seconds=time_spent,
    )

    # Get answer texts for display
    answer_texts = {
        "a": question.answer_a,
        "b": question.answer_b,
        "c": question.answer_c,
        "d": question.answer_d,
    }

    submitted_answer_text = answer_texts.get(submitted_answer, "Unknown")
    correct_answer_text = answer_texts.get(
        question.correct_answer.lower(), "Unknown"
    )

    # Log the attempt
    logger.info(
        f"Answer attempt for question {question_pk}: "
        f"submitted={submitted_answer}, correct={question.correct_answer}, "
        f"is_correct={result['is_correct']}, attempt_id={result['attempt_id']}, "
        f"attempt_number={result['attempt_number']}"
    )

    return {
        "submitted_answer": submitted_answer,
        "submitted_answer_text": submitted_answer_text,
        "correct_answer_text": correct_answer_text,
        "is_correct": result["is_correct"],
        "attempt_number": result["attempt_number"],
        "question_stats": result["question_stats"],
    }


def build_answer_context(question: Question, answer_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Builds context for answer feedback templates.

    Args:
        question: Question object
        answer_data: Result data from answer processing

    Returns:
        Context dictionary for template rendering
    """
    return {
        "question": question,
        "submitted_answer": answer_data["submitted_answer"],
        "submitted_answer_text": answer_data["submitted_answer_text"],
        "correct_answer": question.correct_answer.lower(),
        "correct_answer_text": answer_data["correct_answer_text"],
        "is_correct": answer_data["is_correct"],
        "explanation": getattr(question, "explanation", None),
        "attempt_number": answer_data["attempt_number"],
        "question_stats": answer_data["question_stats"],
    }


def check_answer_logic(request: HttpRequest, question_pk: int) -> Union[TemplateResponse, HttpResponseForbidden]:
    """
    Logic for handling HTMX POST requests to check user's answer submission.

    Refactored version with improved separation of concerns and testability.

    Args:
        request: HTTP request object
        question_pk: Primary key of the question

    Returns:
        TemplateResponse with answer feedback
    """
    # 1. Validate HTMX POST request
    validation_error = validate_htmx_post_request(request)
    if validation_error:
        return validation_error

    try:
        # 2. Get the question
        question = get_question_by_pk(question_pk)

        # 3. Process answer submission
        try:
            answer_data = process_answer_submission(request, question, question_pk)
        except ValueError as e:
            context = {
                "question": question,
                "error_message": str(e),
            }
            return TemplateResponse(
                request,
                "questions/partials/question_block/_question_block_htmx.html",
                context,
            )

        # 4. Build context for feedback templates
        context = build_answer_context(question, answer_data)

        # 5. Choose template based on correctness
        if answer_data["is_correct"]:
            template_name = "questions/partials/feedback/_feedback_correct.html"
        else:
            template_name = "questions/partials/feedback/_feedback_incorrect.html"

        return TemplateResponse(request, template_name, context)

    except Question.DoesNotExist:
        logger.error(f"Question with pk {question_pk} not found")
        context = {
            "error_message": "Question not found.",
        }
        return TemplateResponse(
            request, "questions/partials/_question_list_htmx.html", context
        )

    except Exception as e:
        logger.error(
            f"Error checking answer for question {question_pk}: {e}",
            exc_info=True,
        )
        context = {
            "error_message": "An error occurred while checking your answer. Please try again.",
        }
        return TemplateResponse(
            request, "questions/partials/_question_list_htmx.html", context
        )


# =================== SINGLE QUESTION LOADING LOGIC ===================

def load_single_question_logic(request: HttpRequest, question_pk: int) -> Union[TemplateResponse, HttpResponseForbidden]:
    """
    Logic for handling HTMX GET requests to load a single question block.

    Used for the "Try Again" functionality to reload the original question.

    Args:
        request: HTTP request object
        question_pk: Primary key of the question

    Returns:
        TemplateResponse with single question block
    """
    # 1. Validate HTMX request
    htmx_validation_error = validate_htmx_request(request)
    if htmx_validation_error:
        return htmx_validation_error

    try:
        # 2. Get the question
        question = get_question_by_pk(question_pk)

        context = {
            "question": question,
        }

        logger.debug(f"Loading single question {question_pk} for retry")

        return TemplateResponse(
            request,
            "questions/partials/question_block/_question_block_htmx.html",
            context,
        )

    except Question.DoesNotExist:
        logger.error(f"Question with pk {question_pk} not found")
        context = {
            "error_message": "Question not found.",
        }
        return TemplateResponse(
            request, "questions/partials/_question_list_htmx.html", context
        )

    except Exception as e:
        logger.error(
            f"Error loading single question {question_pk}: {e}", exc_info=True
        )
        context = {
            "error_message": "An error occurred while loading the question. Please try again.",
        }
        return TemplateResponse(
            request, "questions/partials/_question_list_htmx.html", context
        )


# =================== SKIP QUESTION LOGIC ===================

def process_question_skip(question: Question, user: Optional[User]) -> Dict[str, Any]:
    """
    Processes a question skip and returns result data.

    Args:
        question: Question object to skip
        user: User who skipped (can be None for anonymous)

    Returns:
        Dictionary containing skip processing results
    """
    # Use the new model method to record the skip
    skip_result = question.record_skip(user=user)

    logger.info(
        f"Question {question.pk} skipped by user {user}. "
        f"Total skips: {skip_result['total_skips']}"
    )

    return {
        "skipped": True,
        "skip_count": skip_result['total_skips'],
        "question_stats": question.get_current_stats()
    }


def skip_question_logic(request: HttpRequest, question_pk: int) -> Union[TemplateResponse, HttpResponseForbidden]:
    """
    Logic for handling HTMX POST requests when users skip a question.

    Records the skip in analytics and provides appropriate feedback.

    Args:
        request: HTTP request object
        question_pk: Primary key of the question

    Returns:
        TemplateResponse with skip feedback
    """
    # 1. Validate HTMX POST request
    validation_error = validate_htmx_post_request(request)
    if validation_error:
        return validation_error

    try:
        # 2. Get the question
        question = get_question_by_pk(question_pk)

        # 3. Process the skip
        auth_user = request.user if request.user.is_authenticated else None
        skip_data = process_question_skip(question, auth_user if auth_user and auth_user.is_authenticated else None)

        # 4. Build context
        context = {
            "question": question,
            "skipped": skip_data["skipped"],
            "skip_count": skip_data["skip_count"],
            "question_stats": skip_data["question_stats"]
        }

        return TemplateResponse(
            request,
            "questions/partials/feedback/_feedback_skipped.html",
            context
        )

    except Question.DoesNotExist:
        logger.error(f"Question with pk {question_pk} not found")
        context = {
            "error_message": "Question not found.",
        }
        return TemplateResponse(
            request, "questions/partials/_question_list_htmx.html", context
        )

    except Exception as e:
        logger.error(
            f"Error skipping question {question_pk}: {e}",
            exc_info=True,
        )
        context = {
            "error_message": "An error occurred while skipping the question. Please try again.",
        }
        return TemplateResponse(
            request, "questions/partials/_question_list_htmx.html", context
        )