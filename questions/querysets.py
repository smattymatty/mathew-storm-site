# questions/querysets.py
from django.db import models
from django.db.models import Q
from typing import List, Optional


class QuestionQuerySet(models.QuerySet):
    """Custom QuerySet for the Question model."""

    def get_interactive_quiz_questions(
        self,
        title_id_slugs: Optional[List[str]] = None,
        difficulty_levels: Optional[List[str]] = None,
        tag_names: Optional[List[str]] = None,
    ) -> models.QuerySet:
        """
        Fetches Question objects based on optional filter criteria.
        If a filter list is invalid or empty, that specific filter is ignored.
        If no filters are provided at all, returns all questions.
        """
        queryset = self

        # Handle title filtering - support multiple titles with OR logic
        if title_id_slugs is not None:
            if isinstance(title_id_slugs, list) and title_id_slugs:
                queryset = queryset.filter(
                    tutorial_title__title_id_slug__in=title_id_slugs
                )

        # Handle difficulty level filtering (existing logic is correct)
        if difficulty_levels is not None:
            if isinstance(difficulty_levels, list) and difficulty_levels:
                difficulty_query = Q()
                for level in difficulty_levels:
                    difficulty_query |= Q(difficulty=level)
                queryset = queryset.filter(difficulty_query)

        # Handle tag name filtering (existing logic is correct)
        if tag_names is not None:
            if isinstance(tag_names, list) and tag_names:
                queryset = queryset.filter(tags__name__in=tag_names).distinct()

        # Eager load related data
        queryset = queryset.select_related("tutorial_title")
        queryset = queryset.prefetch_related("tags")

        # Default ordering
        queryset = queryset.order_by(
            "tutorial_title__title_id_slug", "question_id_slug"
        )

        return queryset
