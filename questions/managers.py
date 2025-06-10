# questions/managers.py
import random
from typing import List, Tuple # Import Tuple

from django.db import models
from django.db.models import QuerySet, Q
from .querysets import QuestionQuerySet

from .utils import generate_readable_name_from_slug

class QuestionManager(models.Manager):
    """
    Custom Manager for the Question model.
    """

    def get_queryset(self) -> QuestionQuerySet:
        """
        Returns a `QuestionQuerySet` for the associated model.
        """
        return QuestionQuerySet(self.model, using=self._db)

    def get_initial_questions(self, amount: int = 5) -> List[Tuple[str, str]]: # Return type is List of (string, string) tuples
        """
        Returns a randomized list of unique
        (tutorial title slug, question slug) tuples.

        Each tuple contains the slug of a tutorial title and the slug of a question.
        The list is shuffled and limited to the specified amount.
        Returns an empty list if no such pairs exist.

        Args:
            amount: The maximum number of tuples to return. Defaults to 5.

        Returns:
            A list of up to `amount` unique
            (tutorial title slug, question slug) tuples.
        """
        # Fetching tuples of
        # (TutorialTitle.title_id_slug, Question.question_id_slug)
        # This directly gives us a list of 2-element tuples.
        question_identifier_tuples = list(
            self.model.objects
            .select_related('tutorial_title')
            .values_list(
                'tutorial_title__title_id_slug',  # First element of the tuple
                'question_id_slug'                # Second element of the tuple
            )
            .distinct() # Ensures unique pairs
        )

        if not question_identifier_tuples:
            return []

        # Shuffle the list of (tutorial_title_slug, question_id_slug) tuples
        random.shuffle(question_identifier_tuples)

        return question_identifier_tuples[:amount]

    def get_initial_tags(self, amount: int = 9) -> List[str]:
        """
        Returns a randomized list of unique tag names associated with questions.

        Args:
            amount: The maximum number of tag names to return. Defaults to 9.

        Returns:
            A list of up to `amount` unique tag names, randomly ordered.
            Returns an empty list if no tags are found.
        """
        tags = list(
            self.model.objects
            .values_list('tags__name', flat=True)
            .distinct()
            .exclude(tags__name__isnull=True)
        )

        if not tags:
            return []

        random.shuffle(tags)
        return tags[:amount]

    def search_tags(self, query: str, limit: int = 20) -> List[str]:
        """
        Searches for tag names that contain the given query string
        (case-insensitive).

        Args:
            query: The search term to match against tag names
            limit: Maximum number of results to return. Defaults to 20.

        Returns:
            A list of tag names matching the search query,
            limited to `limit` results.
        """
        if not query or not query.strip():
            return self.get_initial_tags(limit)

        query = query.strip()
        tags = list(
            self.model.objects
            .filter(tags__name__icontains=query)
            .values_list('tags__name', flat=True)
            .distinct()
            .exclude(tags__name__isnull=True)
            .order_by('tags__name')[:limit]
        )

        return tags


class TutorialTitleManager(models.Manager):
    """
    Custom Manager for the TutorialTitle model.
    """

    def get_initial_titles(self, amount: int = 6) -> List[str]:
        """
        Returns a randomized list of unique tutorial title slugs,
        limited to the specified amount.

        Args:
            amount: The maximum number of tutorial title slugs to return.
                Defaults to 6.

        Returns:
            A list of up to `amount` unique tutorial title slugs,
            randomly ordered. Returns an empty list if no titles are found.
        """
        # Return title_id_slug values, not name values!
        title_slugs = list(
            self.model.objects
            .values_list('title_id_slug', flat=True)
            .distinct()
        )

        if not title_slugs:
            return []

        random.shuffle(title_slugs)
        return title_slugs[:amount]

    def search_titles(self, query: str, limit: int = 20) -> List[str]:
        """
        Searches for tutorial titles and returns readable names.

        Args:
            query: The search term to match against title names or slugs
            limit: Maximum number of results to return. Defaults to 20.

        Returns:
            A list of tutorial title readable names matching the search query,
            limited to `limit` results.
        """
        if not query or not query.strip():
            # Get initial slugs and convert them to readable names
            initial_slugs = self.get_initial_titles(limit)
            return [generate_readable_name_from_slug(slug) for slug in initial_slugs]

        query = query.strip()

        # Search both name and title_id_slug fields
        matching_titles = self.model.objects.filter(
            Q(name__icontains=query) | Q(title_id_slug__icontains=query)
        ).distinct().order_by('title_id_slug')[:limit]

        # Convert to readable names consistently
        result_names = []
        for title in matching_titles:
            if title.name:
                result_names.append(title.name)
            else:
                # Convert slug to readable name
                result_names.append(generate_readable_name_from_slug(title.title_id_slug))

        return result_names
