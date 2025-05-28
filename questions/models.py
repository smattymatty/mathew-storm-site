from django.db import models
from taggit.managers import TaggableManager # Import TaggableManager

class TutorialTitle(models.Model):
    """
    Represents the source or context of a set of questions,
    e.g., a specific tutorial document.
    """
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

    def __str__(self):
        return self.name or self.title_id_slug

    class Meta:
        verbose_name = "Tutorial Title"
        verbose_name_plural = "Tutorial Titles"


class Question(models.Model):
    """
    Represents a single quiz question.
    """

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

    # Foreign Key to the tutorial/content source
    tutorial_title = models.ForeignKey(
        TutorialTitle,
        on_delete=models.CASCADE,
        related_name="questions",
        help_text="The tutorial this question belongs to."
    )

    # Corresponds to 'question-id' from JSON, unique within a tutorial_title
    question_id_slug = models.SlugField(
        max_length=255,
        help_text="A unique semantic slug for this question within its tutorial (e.g., 'git-basics-commit-definition')."
    )

    question_text = models.TextField(help_text="The main text of the question.")

    # Answer options
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

    # Replaced ManyToManyField with TaggableManager from django-taggit
    tags = TaggableManager(
        blank=True,
        help_text="A comma-separated list of tags. (Handled by django-taggit)"
    )

    # Timestamps (optional but good practice)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensures question_id_slug is unique for each tutorial_title
        unique_together = ('tutorial_title', 'question_id_slug')
        ordering = ['tutorial_title', 'question_id_slug'] # Default ordering
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        # Truncate question text for display if too long
        display_text = (self.question_text[:75] + '...') if len(self.question_text) > 75 else self.question_text
        return f"{self.tutorial_title.title_id_slug} | {self.question_id_slug} | {display_text}"