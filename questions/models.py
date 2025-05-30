# questions/models.py
from django.db import models
from taggit.managers import TaggableManager
from .managers import QuestionManager , TutorialTitleManager

class TutorialTitle(models.Model):
    title_id_slug = models.SlugField(
        max_length=100,
        unique=True,
        primary_key=True,
        help_text="The unique slug for the tutorial title (e.g., '01-first-contribution'). Corresponds to 'title-id' in the JSON."
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        help_text="A human-readable name for the tutorial (e.g., 'Your First Contribution'). Optional."
    )
    # -- Manager --
    objects: TutorialTitleManager = TutorialTitleManager() # Use your custom manager

    def __str__(self):
        """
        Returns the tutorial's name if set; otherwise, returns its unique slug identifier.
        """
        return self.name or self.title_id_slug

    class Meta:
        verbose_name = "Tutorial Title"
        verbose_name_plural = "Tutorial Titles"


class Question(models.Model):
    # --- Enums (Difficulty, AnswerChoice) ---
    class Difficulty(models.TextChoices):
        FOUNDATIONAL = "foundational", "Foundational"
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"
        IMPOSSIBLE = "impossible", "Impossible"

    class AnswerChoice(models.TextChoices):
        A = 'a', 'A'
        B = 'b', 'B'
        C = 'c', 'C'
        D = 'd', 'D'

    # --- Fields ---
    tutorial_title = models.ForeignKey(
        TutorialTitle,
        on_delete=models.CASCADE,
        related_name="questions",
        help_text="The tutorial this question belongs to."
    )
    question_id_slug = models.SlugField(
        max_length=255,
        help_text="A unique semantic slug for this question within its tutorial (e.g., 'git-basics-commit-definition')."
    )
    question_text = models.TextField(help_text="The main text of the question.")
    answer_a = models.CharField(max_length=500, help_text="Text for answer option A.")
    answer_b = models.CharField(max_length=500, help_text="Text for answer option B.")
    answer_c = models.CharField(max_length=500, help_text="Text for answer option C.")
    answer_d = models.CharField(max_length=500, help_text="Text for answer option D.")
    correct_answer = models.CharField(
        max_length=1,
        choices=AnswerChoice.choices,
        help_text="The letter (a, b, c, or d) corresponding to the correct answer."
    )
    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.EASY,
        help_text="The difficulty level of the question."
    )
    tags = TaggableManager(
        blank=True,
        help_text="A comma-separated list of tags. (Handled by django-taggit)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --- Manager ---
    objects: QuestionManager = QuestionManager() # Use your custom manager

    # --- Meta ---
    class Meta:
        unique_together = ('tutorial_title', 'question_id_slug')
        ordering = ['tutorial_title__title_id_slug', 'question_id_slug'] 
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    # --- Methods ---
    def __str__(self):
        display_text = (self.question_text[:75] + '...') if len(self.question_text) > 75 else self.question_text
        return f"{self.tutorial_title.title_id_slug} | {self.question_id_slug} | {display_text}"