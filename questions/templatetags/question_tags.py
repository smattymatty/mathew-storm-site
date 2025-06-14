# questions/templatetags/question_tags.py
"""
Custom template tags for the questions app.
"""

from typing import Dict
from pathlib import Path
from django import template
from django.conf import settings
from ..models import Question

register = template.Library()


@register.simple_tag
def question_tut_url(question: Question) -> str:
    """
    Generate the URL to the tutorial content for a question.

    Usage: {% question_tut_url question %}

    Args:
        question: The Question object

    Returns:
        str: The URL path to the tutorial content
    """
    return _get_tutorial_url(question)


@register.simple_tag
def question_tut_name(question: Question) -> str:
    """
    Get a human-readable name for the tutorial.

    Usage: {% question_tut_name question %}

    Args:
        question: The Question object

    Returns:
        str: The display name for the tutorial
    """
    return _get_tutorial_display_name(question)


def _get_tutorial_series_mapping() -> Dict[str, str]:
    """
    Dynamically generate tutorial series mapping by scanning the tutorials_content directory.

    Returns:
        Dict[str, str]: Mapping of tutorial slugs to their full paths
    """
    mapping = {}

    try:
        # Get the tutorials content directory
        tutorials_content_dir = Path(settings.BASE_DIR) / "tutorials_content"

        if tutorials_content_dir.exists():
            # Scan for tutorial series directories
            for series_dir in tutorials_content_dir.iterdir():
                if series_dir.is_dir() and not series_dir.name.startswith("."):
                    series_name = series_dir.name

                    # Scan for tutorial files in this series
                    for tutorial_file in series_dir.iterdir():
                        if tutorial_file.suffix == ".md":
                            # Extract the tutorial slug from the filename
                            tutorial_filename = tutorial_file.stem

                            # Remove number prefix if present (e.g., "01-" from "01-creating-a-project-base")
                            if (
                                "-" in tutorial_filename
                                and len(tutorial_filename.split("-")) > 1
                            ):
                                first_part = tutorial_filename.split("-")[0]
                                if first_part.isdigit():
                                    tutorial_slug = "-".join(
                                        tutorial_filename.split("-")[1:]
                                    )
                                else:
                                    tutorial_slug = tutorial_filename
                            else:
                                tutorial_slug = tutorial_filename

                            # Map the slug to the full path
                            mapping[tutorial_slug] = (
                                f"{series_name}/{tutorial_filename}"
                            )
    except Exception:
        # If dynamic mapping fails, return empty dict and fall back to static mapping
        pass

    return mapping


def _get_tutorial_url(question: Question) -> str:
    """
    Generate the URL to the tutorial content for this question.
    """
    tutorial_slug = question.tutorial_title.title_id_slug

    # Try dynamic mapping first
    mapping = _get_tutorial_series_mapping()
    tutorial_path = mapping.get(tutorial_slug)

    if tutorial_path:
        return f"/tuts/{tutorial_path}/"

    # Fallback: Static mapping for known tutorials
    tutorial_series_mapping = {
        "01-creating-a-project-base": "django-webdev-fundamentals/01-creating-a-project-base",
        "02-models-and-admin-interface": "django-webdev-fundamentals/02-models-and-admin-interface",
        "03-forms": "django-webdev-fundamentals/03-forms",
        "01-first-contribution": "git-for-beginners/01-first-contribution",
    }

    tutorial_path = tutorial_series_mapping.get(
        tutorial_slug, f"unknown/{tutorial_slug}"
    )
    return f"/tuts/{tutorial_path}/"


def _get_tutorial_display_name(question: Question) -> str:
    """
    Get a human-readable name for the tutorial.
    """
    # Use the tutorial title name if available, otherwise format the slug
    if question.tutorial_title.name:
        return question.tutorial_title.name

    # Format the slug to be more readable
    formatted_name = question.tutorial_title.title_id_slug.replace(
        "-", " "
    ).title()
    return formatted_name


@register.simple_tag
def debug_tutorial_mapping() -> Dict[str, str]:
    """
    Debug template tag to show the current tutorial mapping.

    Usage: {% debug_tutorial_mapping %}

    Returns:
        Dict[str, str]: The current tutorial mapping
    """
    return _get_tutorial_series_mapping()


@register.filter
def format_tutorial_name(value: str) -> str:
    """
    Format a tutorial slug into a readable name.

    Usage: {{ tutorial_slug|format_tutorial_name }}
    """
    return value.replace("-", " ").title()
