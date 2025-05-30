# questions/managers.py
import random
from typing import List, Tuple # Import Tuple

from django.db import models
from .querysets import QuestionQuerySet 

class QuestionManager(models.Manager):
    """
    Custom Manager for the Question model.
    """
    
    def get_queryset(self) -> QuestionQuerySet:
        """
        Overrides the default `get_queryset` method to use QuestionQuerySet.
        """
        return QuestionQuerySet(self.model, using=self._db)
    
    def get_initial_questions(self, amount: int = 5) -> List[Tuple[str, str]]: # Return type is List of (string, string) tuples
        """
        Retrieves a random list of (TutorialTitle.title_id_slug, Question.question_id_slug) tuples.
        """
        # Fetching tuples of (TutorialTitle.title_id_slug, Question.question_id_slug)
        # This directly gives us a list of 2-element tuples.
        question_identifier_tuples = list(
            self.model.objects
            .select_related('tutorial_title') # Good for performance
            .values_list(
                'tutorial_title__title_id_slug', # First element of the tuple
                'question_id_slug'               # Second element of the tuple
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
        Retrieves a random list of unique tag names.
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
        # valid_tags = [tag for tag in tags if tag is not None] # Safeguard, though exclude should handle it
        # If exclude works as expected (it should for non-null names), this simplification is fine:
        return tags[:amount]
    
    
class TutorialTitleManager(models.Manager):
    """
    Custom Manager for the TutorialTitle model.
    """
    
    def get_initial_titles(self, amount: int = 6) -> List[str]:
        """
        Retrieves a random list of unique tutorial title names.
        """
        titles = list(
            self.model.objects
            .values_list('name', flat=True)
            .distinct()
            .exclude(name__isnull=True) 
        )
        
        if not titles:
            return []
            
        random.shuffle(titles)
        # valid_titles = [title for title in titles if title is not None] # Safeguard, though exclude should handle it
        # If exclude works as expected (it should for non-null names), this simplification is fine:
        return titles[:amount]