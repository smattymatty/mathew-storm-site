# Question QuerySet

The `Question` model provides a custom manager, `QuestionManager`, which inherits from Django's `models.Manager`.

`get_queryset()` is the primary method that returns a `QuestionQuerySet` instance, which is a subclass of Django's `models.QuerySet`.

`QuestionQuerySet` provides a custom `get_interactive_quiz_questions()` method that is designed to fetch questions for interactive quizzes or filtered displays.

## Using the `Question` QuerySet for Interactive Quizzes

The `Question` model provides a custom manager method, `get_interactive_quiz_questions`, designed to flexibly fetch questions. This method is the primary way to retrieve questions for dynamic quizzes or filtered displays.

**Method Signature:**

```python
Question.objects.get_queryset().get_interactive_quiz_questions(
    title_id_slug: Optional[str] = None,
    difficulty_levels: Optional[List[str]] = None,
    tag_names: Optional[List[str]] = None
) -> models.QuerySet
```

---

### Purpose

Retrieves a Django `QuerySet` of `Question` instances based on the provided optional filter criteria. It includes database query optimizations for efficiently accessing related `TutorialTitle` and `Tag` data.

---

### Parameters

* **`title_id_slug: Optional[str]`** (Default: `None`)
  * Filters questions belonging to a specific `TutorialTitle` using its unique slug (e.g., ``"01-first-contribution"``).

* **`difficulty_levels: Optional[List[str]]`** (Default: `None`)
  * Filters questions by one or more difficulty levels.
  * If multiple levels are provided (e.g., `["easy", "medium"]`), questions matching *any* of the specified difficulties are returned (OR logic).
  * Valid difficulty strings correspond to `Question.Difficulty.choices` (e.g., `"foundational"`, `"easy"`, `"medium"`, `"hard"`, `"impossible"`).
  * If this parameter is `None`, or an empty list, or not a valid list, the difficulty filter is ignored.

* **`tag_names: Optional[List[str]]`** (Default: `None`)
  * Filters questions associated with *any* of the provided tag names (e.g., `["git", "python"]`).
  * Tag matching is typically case-sensitive.
  * If this parameter is `None`, or an empty list, or not a valid list, the tag filter is ignored.

---

### Return Value

* A Django `QuerySet` containing `Question` model instances that match all applied filters.
* The queryset is optimized with `select_related('tutorial_title')` and `prefetch_related('tags')` to reduce database queries when accessing these related fields on the retrieved questions.

---

### Behavior Notes

* **No Filters Provided:** If all filter parameters (`title_id_slug`, `difficulty_levels`, `tag_names`) are `None` or result in no actual filtering (e.g., empty lists are passed), the method returns all `Question` instances.
* **Empty/Invalid Filter Lists:** As noted above, if `difficulty_levels` or `tag_names` is an empty list or an invalid type, that specific filter criterion is skipped, and other active filters will still apply.
* **Default Ordering:** Results are ordered by `tutorial_title__title_id_slug` first, then by `question_id_slug` within each title group.

---

### Example Usage

1. **Get all questions for a specific tutorial:**
    `qs = Question.objects.get_interactive_quiz_questions(title_id_slug="tut-01")`

2. **Get all 'easy' questions:**
    `qs = Question.objects.get_interactive_quiz_questions(difficulty_levels=["easy"])`

3. **Get all 'easy' OR 'medium' questions for a specific tutorial:**

    ```python
    qs = Question.objects.get_interactive_quiz_questions(
        title_id_slug="tut-01",
        difficulty_levels=["easy", "medium"]
    )
    ```

4. **Get all questions tagged with 'git' OR 'python':**
    `qs = Question.objects.get_interactive_quiz_questions(tag_names=["git", "python"])`

5. **Get all 'hard' questions for 'tut-02' that are tagged 'advanced':**

    ```python
    qs = Question.objects.get_interactive_quiz_questions(
        title_id_slug="tut-02",
        difficulty_levels=["hard"],
        tag_names=["advanced"]
    )
    ```

6. **Get all questions (if no specific filters are needed):**
    `all_questions = Question.objects.get_interactive_quiz_questions()`
