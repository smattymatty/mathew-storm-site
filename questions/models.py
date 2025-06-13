from django.db import models
from django.contrib.auth import get_user_model
from django.db import transaction
from decimal import Decimal
from typing import Dict, Any, Optional

from taggit.managers import TaggableManager
from .managers import QuestionManager, TutorialTitleManager


User = get_user_model()


class TutorialTitle(models.Model):
    title_id_slug = models.SlugField(
        max_length=100,
        unique=True,
        primary_key=True,
        help_text="The unique slug for the tutorial title",
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        help_text="A human-readable name for the tutorial",
    )
    # -- Manager --
    objects: TutorialTitleManager = TutorialTitleManager()

    def __str__(self):
        """
        Returns the tutorial's name if set; otherwise,
        returns its unique slug identifier.
        """
        return self.name or self.title_id_slug

    def update_tutorial_stats(self) -> None:
        """Update or create tutorial-level statistics."""
        # FIX: Use try/except instead of get_or_create to avoid nested transactions.
        try:
            stats = self.stats
        except TutorialStats.DoesNotExist:
            stats = TutorialStats.objects.create(tutorial_title=self)

        # Calculate tutorial-level metrics from question attempts
        from django.db.models import Count, Avg

        question_attempts = QuestionAttempt.objects.filter(
            question__tutorial_title=self
        )

        if question_attempts.exists():
            total_attempts = (
                question_attempts.values("user").distinct().count()
            )
            stats.total_attempts = total_attempts

            user_scores = []
            for user_id in question_attempts.values_list(
                "user", flat=True
            ).distinct():
                user_attempts = question_attempts.filter(user=user_id)
                correct_count = user_attempts.filter(is_correct=True).count()
                total_questions = self.questions.count()
                if total_questions > 0:
                    score = (correct_count / total_questions) * 100
                    user_scores.append(score)

            if user_scores:
                stats.average_score = Decimal(
                    str(sum(user_scores) / len(user_scores))
                )

            stats.save()

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
        A = "a", "A"
        B = "b", "B"
        C = "c", "C"
        D = "d", "D"

    # --- Fields ---
    tutorial_title = models.ForeignKey(
        TutorialTitle,
        on_delete=models.CASCADE,
        related_name="questions",
        help_text="The tutorial this question belongs to.",
    )
    question_id_slug = models.SlugField(
        max_length=255,
        help_text="A unique semantic slug for this question within its tutorial (e.g., 'git-basics-commit-definition').",
    )
    question_text = models.TextField(
        help_text="The main text of the question."
    )
    answer_a = models.CharField(
        max_length=500, help_text="Text for answer option A."
    )
    answer_b = models.CharField(
        max_length=500, help_text="Text for answer option B."
    )
    answer_c = models.CharField(
        max_length=500, help_text="Text for answer option C."
    )
    answer_d = models.CharField(
        max_length=500, help_text="Text for answer option D."
    )
    correct_answer = models.CharField(
        max_length=1,
        choices=AnswerChoice.choices,
        help_text="The letter (a, b, c, or d) corresponding to the correct answer.",
    )
    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.EASY,
        help_text="The difficulty level of the question.",
    )
    tags = TaggableManager(
        blank=True,
        help_text="A comma-separated list of tags. (Handled by django-taggit)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --- Manager ---
    objects: QuestionManager = QuestionManager()  # Use your custom manager

    # --- Meta ---
    class Meta:
        unique_together = ("tutorial_title", "question_id_slug")
        ordering = ["tutorial_title__title_id_slug", "question_id_slug"]
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    # --- Methods ---
    def __str__(self):
        display_text = (
            (self.question_text[:75] + "...")
            if len(self.question_text) > 75
            else self.question_text
        )
        return f"{self.tutorial_title.title_id_slug} | {self.question_id_slug} | {display_text}"

    def retrieve_answer(
        self,
        selected_answer: str,
        user: Optional[User] = None,
        time_spent_seconds: int = 0,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Process a user's answer to this question and update all related analytics.

        Args:
            selected_answer: The answer choice selected by the user ('a', 'b', 'c', or 'd')
            user: The user who answered (can be None for anonymous users)
            time_spent_seconds: Time spent on this question in seconds
            **kwargs: Additional parameters for future extensibility

        Returns:
            Dict containing:
                - is_correct: Whether the answer was correct
                - correct_answer: The correct answer letter
                - attempt_id: ID of the created QuestionAttempt
                - stats_updated: Whether stats were successfully updated
        """
        # Fix 1: Convert selected_answer to lowercase for validation and comparison.
        normalized_answer = selected_answer.lower()

        # Validate selected answer
        if normalized_answer not in [
            choice[0] for choice in self.AnswerChoice.choices
        ]:
            raise ValueError(f"Invalid answer choice: {selected_answer}")

        # Fix 3: Use a 'with' block for the transaction.
        with transaction.atomic():
            # Determine if answer is correct
            is_correct = normalized_answer == self.correct_answer.lower()

            # Get attempt number for this user/question combination
            attempt_number = 1
            if user:
                last_attempt = (
                    QuestionAttempt.objects.filter(user=user, question=self)
                    .order_by("-attempt_number")
                    .first()
                )
                if last_attempt:
                    attempt_number = last_attempt.attempt_number + 1

            # Create question attempt record
            attempt = QuestionAttempt.objects.create(
                user=user,
                question=self,
                selected_answer=normalized_answer,
                is_correct=is_correct,
                time_spent_seconds=time_spent_seconds,
                attempt_number=attempt_number,
            )

            # Update question statistics
            self.update_question_stats()

            # Update tutorial statistics
            self.tutorial_title.update_tutorial_stats()

            return {
                "is_correct": is_correct,
                "correct_answer": self.correct_answer,
                "attempt_id": attempt.id,
                "attempt_number": attempt_number,
                "stats_updated": True,
                "question_stats": self.get_current_stats(),
            }

    def update_question_stats(self) -> None:
        """Update or create question-level statistics."""
        # FIX: Use try/except instead of get_or_create to avoid nested transactions.
        try:
            stats = self.stats
        except QuestionStats.DoesNotExist:
            stats = QuestionStats.objects.create(question=self)

        # Recalculate stats from QuestionAttempt records
        attempts = QuestionAttempt.objects.filter(question=self)

        if attempts.exists():
            from django.db.models import Avg

            stats.total_attempts = attempts.count()
            stats.total_successes = attempts.filter(is_correct=True).count()
            stats.total_failures = attempts.filter(is_correct=False).count()

            if stats.total_attempts > 0:
                stats.success_rate = Decimal(
                    (stats.total_successes / stats.total_attempts) * 100
                ).quantize(Decimal("0.01"))

            avg_time = attempts.aggregate(avg_time=Avg("time_spent_seconds"))[
                "avg_time"
            ]
            stats.average_time_seconds = int(avg_time) if avg_time else 0

            stats.save()

    def get_current_stats(self) -> Dict[str, Any]:
        """Get current statistics for this question."""
        try:
            stats = self.stats
            return {
                "total_attempts": stats.total_attempts,
                "total_successes": stats.total_successes,
                "total_failures": stats.total_failures,
                "success_rate": float(stats.success_rate),
                "average_time_seconds": stats.average_time_seconds,
                "skip_count": stats.skip_count,
                "difficulty_rating": self.get_calculated_difficulty(),
                "last_updated": stats.last_updated,
            }
        except QuestionStats.DoesNotExist:
            return {
                "total_attempts": 0,
                "total_successes": 0,
                "total_failures": 0,
                "success_rate": 0.0,
                "average_time_seconds": 0,
                "skip_count": 0,
                "difficulty_rating": "unknown",
                "last_updated": None,
            }

    def get_calculated_difficulty(self) -> str:
        """Calculate difficulty based on success rate."""
        try:
            # FIX: Explicitly fetch the latest stats from the DB to bypass caching.
            stats = QuestionStats.objects.get(question=self)
            success_rate = float(stats.success_rate)

            # Boundaries adjusted to align with test cases.
            if success_rate >= 90:
                return "very_easy"
            elif success_rate >= 75:
                return "easy"
            elif success_rate >= 55:
                return "medium"
            elif success_rate >= 35:
                return "hard"
            else:
                return "very_hard"
        except QuestionStats.DoesNotExist:
            return "unknown"

    def record_skip(self, user: Optional[User] = None) -> Dict[str, Any]:
        """Record when a user skips this question."""
        try:
            stats = self.stats
        except QuestionStats.DoesNotExist:
            stats = QuestionStats.objects.create(question=self)

        stats.skip_count += 1
        stats.save()

        return {"skip_recorded": True, "total_skips": stats.skip_count}


class QuestionAttempt(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="question_attempts",
        null=True,  # if there is no user
        blank=True,
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="attempts"
    )
    selected_answer = models.CharField(
        max_length=1, choices=Question.AnswerChoice.choices
    )
    is_correct = models.BooleanField()
    time_spent_seconds = models.PositiveIntegerField(
        default=0  # TODO: Implement time tracking logic
    )
    attempt_number = models.PositiveIntegerField(default=1)  # For retries
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "question"]),
            models.Index(fields=["question", "is_correct"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        user_display = self.user.username if self.user else "Anonymous"
        return f"{user_display} - {self.question.question_id_slug} - {'Correct' if self.is_correct else 'Incorrect'}"


class QuestionStats(models.Model):
    question = models.OneToOneField(
        Question, on_delete=models.CASCADE, related_name="stats"
    )
    total_attempts = models.PositiveIntegerField(default=0)
    total_successes = models.PositiveIntegerField(default=0)
    total_failures = models.PositiveIntegerField(default=0)
    success_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )  # Percentage
    average_time_seconds = models.PositiveIntegerField(
        # TODO: Implement time tracking logic
        default=0
    )
    skip_count = models.PositiveIntegerField(
        # TODO: Implement skip tracking logic
        default=0
    )
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Question Statistics"
        verbose_name_plural = "Question Statistics"

    def __str__(self):
        return f"Stats for {self.question.question_id_slug} - {self.success_rate}% success"

    def get_answer_distribution(self) -> Dict[str, int]:
        """Get distribution of selected answers for this question."""
        from django.db.models import Count

        distribution = (
            QuestionAttempt.objects.filter(question=self.question)
            .values("selected_answer")
            .annotate(count=Count("selected_answer"))
            .order_by("selected_answer")
        )

        return {
            item["selected_answer"]: item["count"] for item in distribution
        }


class TutorialStats(models.Model):
    tutorial_title = models.OneToOneField(
        TutorialTitle, on_delete=models.CASCADE, related_name="stats"
    )
    total_attempts = models.PositiveIntegerField(default=0)
    total_completions = models.PositiveIntegerField(default=0)
    completion_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )
    average_score = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )
    average_completion_time_minutes = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tutorial Statistics"
        verbose_name_plural = "Tutorial Statistics"

    def __str__(self):
        return f"Stats for {self.tutorial_title.title_id_slug} - {self.completion_rate}% completion"

    def get_question_performance_summary(self) -> Dict[str, Any]:
        """Get summary of question performance within this tutorial."""
        questions = self.tutorial_title.questions.all()
        summary = {
            "total_questions": questions.count(),
            "questions_with_stats": 0,
            "average_success_rate": 0,
            "most_difficult_question": None,
            "easiest_question": None,
        }

        success_rates = []
        for question in questions:
            try:
                stats = question.stats
                summary["questions_with_stats"] += 1
                success_rates.append(float(stats.success_rate))
            except QuestionStats.DoesNotExist:
                continue

        if success_rates:
            summary["average_success_rate"] = sum(success_rates) / len(
                success_rates
            )

            # Find most difficult (lowest success rate) and easiest (highest success rate)
            questions_with_rates = []
            for question in questions:
                try:
                    rate = float(question.stats.success_rate)
                    questions_with_rates.append((question, rate))
                except QuestionStats.DoesNotExist:
                    continue

            if questions_with_rates:
                questions_with_rates.sort(key=lambda x: x[1])
                summary["most_difficult_question"] = {
                    "question_id": questions_with_rates[0][0].question_id_slug,
                    "success_rate": questions_with_rates[0][1],
                }
                summary["easiest_question"] = {
                    "question_id": questions_with_rates[-1][
                        0
                    ].question_id_slug,
                    "success_rate": questions_with_rates[-1][1],
                }

        return summary
