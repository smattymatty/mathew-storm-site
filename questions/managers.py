# questions/managers.py
from django.db import models
from .querysets import QuestionQuerySet #

class QuestionManager(models.Manager):
    """
    Custom Manager for the Question model.
    
    This manager is configured to use the custom `QuestionQuerySet`.
    As a result, all methods defined on `QuestionQuerySet` (such as
    `get_interactive_quiz_questions`) become directly available on
    `Question.objects` (or whatever name this manager is assigned to)
    and on any querysets derived from it.
    """
    
    def get_queryset(self) -> QuestionQuerySet:
        """
        Overrides the default `get_queryset` method.
        
        This is the key integration point. It ensures that any queryset
        originating from this manager is an instance of our custom
        `QuestionQuerySet`, thereby granting access to all its specialized
        querying methods.
        """
        # Instructs the manager to use your custom QuerySet for all default
        # queryset operations (like .all(), .filter(), etc.).
        return QuestionQuerySet(self.model, using=self._db)

