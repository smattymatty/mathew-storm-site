# questions/querysets.py
from django.db import models
from django.db.models import Q
from typing import List, Optional

class QuestionQuerySet(models.QuerySet):
    """Custom QuerySet for the Question model."""
    def get_interactive_quiz_questions(
        self,
        title_id_slug: Optional[str] = None,
        difficulty_levels: Optional[List[str]] = None,
        tag_names: Optional[List[str]] = None,
    ) -> models.QuerySet:
        """
        Fetches Question objects based on optional filter criteria.
        If a filter list (difficulty_levels, tag_names) is invalid or empty, that specific filter is ignored.
        If no filters are provided at all, returns all questions matching other criteria (or all questions if no other criteria).
        """
        queryset = self # Start with all questions in the current queryset from the manager

        if title_id_slug:
            queryset = queryset.filter(tutorial_title__title_id_slug=title_id_slug) # Filter by the slug of the related tutorial title

        # Handle difficulty level filtering
        if difficulty_levels is not None: # Check if difficulty_levels parameter was provided (even if it's an empty list)
            if isinstance(difficulty_levels, list) and difficulty_levels: # Proceed only if it's a non-empty list
                difficulty_query = Q() # Initialize an empty Q object for OR conditions
                for level in difficulty_levels:
                    difficulty_query |= Q(difficulty=level) # Add each difficulty level as an OR condition
                queryset = queryset.filter(difficulty_query)
            # If difficulty_levels is None, an empty list, or not a list, this specific filter is effectively skipped.

        # Handle tag name filtering
        if tag_names is not None: # Check if tag_names parameter was provided
            if isinstance(tag_names, list) and tag_names: # Proceed only if it's a non-empty list
                # Filter for questions that have any of the tags in the list.
                # distinct() is used because a question might match multiple tags from the list, preventing duplicates in results.
                queryset = queryset.filter(tags__name__in=tag_names).distinct()
            # If tag_names is None, an empty list, or not a list, this specific filter is effectively skipped.
        
        # Eager load related data that will be frequently accessed to reduce database queries.
        queryset = queryset.select_related('tutorial_title') # Optimizes ForeignKey access (tutorial_title is a ForeignKey).
        queryset = queryset.prefetch_related('tags') # Optimizes ManyToManyField access (tags from django-taggit).

        # Default ordering to ensure consistent results, especially important for pagination or stable UIs.
        queryset = queryset.order_by('tutorial_title__title_id_slug', 'question_id_slug')

        return queryset