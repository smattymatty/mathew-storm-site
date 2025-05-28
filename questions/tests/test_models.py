import logging
from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from ..models import TutorialTitle, Question

logger = logging.getLogger(__name__) # This will be 'questions.tests.test_models'

class TutorialTitleModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass() # Good practice to call super
        logger.info(f"TutorialTitleModelTest.setUpClass()") # Formatter adds \n before
    
    def test_create_tutorial_title_with_name(self):
        logger.info(f"TutorialTitleModelTest.{self._testMethodName}()")
        title_slug_to_create = "01-first-contribution"
        title_name_to_create = "Your First Contribution"
        logger.debug(f"--\tData: Creating TutorialTitle with slug='{title_slug_to_create}', name='{title_name_to_create}'")
        
        title = TutorialTitle.objects.create(
            title_id_slug=title_slug_to_create,
            name=title_name_to_create
        )
        self.assertEqual(title.title_id_slug, title_slug_to_create)
        self.assertEqual(title.name, title_name_to_create)
        self.assertEqual(str(title), title_name_to_create)
        logger.debug(f"--\tAsserted: Creation and __str__ for slug='{title_slug_to_create}' successful.")

    def test_create_tutorial_title_slug_only(self):
        logger.info(f"TutorialTitleModelTest.{self._testMethodName}()")
        title_slug_to_create = "02-next-steps"
        logger.debug(f"--\tData: Creating TutorialTitle with slug='{title_slug_to_create}' (name blank).")

        title = TutorialTitle.objects.create(title_id_slug=title_slug_to_create)
        self.assertEqual(title.title_id_slug, title_slug_to_create)
        self.assertEqual(title.name, "") # Blank is True
        self.assertEqual(str(title), title_slug_to_create)
        logger.debug(f"--\tAsserted: Creation with blank name and __str__ for slug='{title_slug_to_create}' successful.")

    def test_tutorial_title_id_slug_is_primary_key_and_unique(self):
        logger.info(f"TutorialTitleModelTest.{self._testMethodName}()")
        unique_slug = "unique-slug-test-for-title" # Made slug more specific
        logger.debug(f"--\tData: Testing uniqueness with slug='{unique_slug}'.")
        
        TutorialTitle.objects.create(title_id_slug=unique_slug)
        with self.assertRaises(IntegrityError):
            TutorialTitle.objects.create(title_id_slug=unique_slug)
        logger.debug(f"--\tAsserted: IntegrityError raised for duplicate slug='{unique_slug}'.")


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Note: setUpTestData doesn't call super()
        logger.info(f"QuestionModelTest.setUpTestData()")
        # Using a more unique slug here to avoid potential clashes if tests run in certain orders
        # without perfect DB isolation between TestCase classes.
        cls.tutorial_title_slug = "qmt-01-first-contribution" 
        cls.tutorial_title = TutorialTitle.objects.create(
            title_id_slug=cls.tutorial_title_slug,
            name="Test First Contribution Title for Questions"
        )
        logger.debug(f"--\tData: Created TutorialTitle with slug='{cls.tutorial_title_slug}'.")

    def test_create_question_successfully(self):
        logger.info(f"QuestionModelTest.{self._testMethodName}()")
        question_slug = "git-basics-commit-definition"
        question_text_start = "In Git, what is a 'Commit'?"
        logger.debug(f"--\tData: Creating Question slug='{question_slug}', text starting: '{question_text_start[:30]}...'")
        
        question_data = {
            "tutorial_title": self.tutorial_title,
            "question_id_slug": question_slug,
            "question_text": question_text_start,
            "answer_a": "A command to connect to GitHub",
            "answer_b": "A saved snapshot of your changes",
            "answer_c": "A type of project license",
            "answer_d": "A discussion thread about a bug",
            "correct_answer": Question.AnswerChoice.B,
            "difficulty": Question.Difficulty.EASY,
        }
        question = Question.objects.create(**question_data)
        tags_to_add = ["git", "commit", "basics"]
        question.tags.add(*tags_to_add)
        logger.debug(f"--\tData: Added tags: {', '.join(tags_to_add)} to question '{question_slug}'.")

        self.assertEqual(question.tutorial_title, self.tutorial_title)
        self.assertEqual(question.question_id_slug, question_slug)
        # ... other assertions
        self.assertEqual(question.tags.count(), 3)
        logger.debug(f"--\tAsserted: Successful creation and tagging for question '{question_slug}'.")

    def test_question_unique_together_constraint(self):
        logger.info(f"QuestionModelTest.{self._testMethodName}()")
        unique_q_slug = "unique-q-slug" # This slug is unique for this test method
        logger.debug(f"--\tData: Testing unique_together: title='{self.tutorial_title.title_id_slug}', question_slug='{unique_q_slug}'.")

        Question.objects.create(
            tutorial_title=self.tutorial_title,
            question_id_slug=unique_q_slug,
            question_text="Test Question 1",
            answer_a="A", answer_b="B", answer_c="C", answer_d="D",
            correct_answer=Question.AnswerChoice.A,
            difficulty=Question.Difficulty.EASY
        )
        with self.assertRaises(IntegrityError):
            Question.objects.create(
                tutorial_title=self.tutorial_title, 
                question_id_slug=unique_q_slug, # Same slug under same title
                question_text="Test Question 2 - Duplicate Slug",
                answer_a="A", answer_b="B", answer_c="C", answer_d="D",
                correct_answer=Question.AnswerChoice.A,
                difficulty=Question.Difficulty.EASY
            )
        logger.debug(f"--\tAsserted: IntegrityError for duplicate question slug='{unique_q_slug}'.")

    def test_question_default_difficulty(self):
        logger.info(f"QuestionModelTest.{self._testMethodName}()")
        question_slug = "default-difficulty-test"
        logger.debug(f"--\tData: Testing default difficulty for question slug='{question_slug}'.")

        question = Question.objects.create(
            tutorial_title=self.tutorial_title,
            question_id_slug=question_slug,
            question_text="What's the default difficulty?",
            answer_a="A", answer_b="B", answer_c="C", answer_d="D",
            correct_answer=Question.AnswerChoice.A
        )
        self.assertEqual(question.difficulty, Question.Difficulty.EASY)
        logger.debug(f"--\tAsserted: Default difficulty is '{Question.Difficulty.EASY}'.")

    def test_question_invalid_difficulty_choice(self):
        logger.info(f"QuestionModelTest.{self._testMethodName}()")
        invalid_difficulty = "super_easy"
        logger.debug(f"--\tData: Testing invalid difficulty choice: '{invalid_difficulty}'.")
        
        question = Question(
            tutorial_title=self.tutorial_title,
            question_id_slug="invalid-difficulty-test",
            question_text="Test invalid difficulty.",
            answer_a="A", answer_b="B", answer_c="C", answer_d="D",
            correct_answer=Question.AnswerChoice.A,
            difficulty=invalid_difficulty 
        )
        with self.assertRaises(ValidationError):
            question.full_clean()
        logger.debug(f"--\tAsserted: ValidationError for invalid difficulty '{invalid_difficulty}'.")

    def test_question_invalid_correct_answer_choice(self):
        logger.info(f"QuestionModelTest.{self._testMethodName}()")
        invalid_answer = 'e'
        logger.debug(f"--\tData: Testing invalid correct_answer choice: '{invalid_answer}'.")

        question = Question(
            tutorial_title=self.tutorial_title,
            question_id_slug="invalid-answer-test",
            question_text="Test invalid answer choice.",
            answer_a="A", answer_b="B", answer_c="C", answer_d="D",
            correct_answer=invalid_answer,
            difficulty=Question.Difficulty.EASY
        )
        with self.assertRaises(ValidationError):
            question.full_clean()
        logger.debug(f"--\tAsserted: ValidationError for invalid correct_answer '{invalid_answer}'.")

    def test_question_can_be_created_without_tags(self):
        logger.info(f"QuestionModelTest.{self._testMethodName}()")
        question_slug = "no-tags-test"
        logger.debug(f"--\tData: Creating question slug='{question_slug}' without tags.")

        question = Question.objects.create(
            tutorial_title=self.tutorial_title,
            question_id_slug=question_slug,
            question_text="This question has no tags.",
            answer_a="A", answer_b="B", answer_c="C", answer_d="D",
            correct_answer=Question.AnswerChoice.D,
            difficulty=Question.Difficulty.MEDIUM
        )
        self.assertEqual(question.tags.count(), 0)
        logger.debug(f"--\tAsserted: Question '{question_slug}' created with 0 tags.")

    def test_question_tag_operations(self):
        logger.info(f"QuestionModelTest.{self._testMethodName}()")
        question_slug = "tag-ops-test"
        initial_tags = ["python", "django", "testing"]
        set_tags = ["git", "github"]
        logger.debug(f"--\tData: For q_slug='{question_slug}', initial_tags={initial_tags}, then set_tags={set_tags}.")

        question = Question.objects.create(
            tutorial_title=self.tutorial_title,
            question_id_slug=question_slug,
            question_text="Testing tag operations.",
            answer_a="A", answer_b="B", answer_c="C", answer_d="D",
            correct_answer=Question.AnswerChoice.A
        )
        
        question.tags.add(*initial_tags)
        logger.debug(f"--\tAction: Added tags {initial_tags}.")
        self.assertEqual(question.tags.count(), 3)
        
        question.tags.add("django") # Add existing
        logger.debug(f"--\tAction: Added existing tag 'django'.")
        self.assertEqual(question.tags.count(), 3)
        
        question.tags.remove("testing")
        logger.debug(f"--\tAction: Removed tag 'testing'.")
        self.assertEqual(question.tags.count(), 2)
        
        question.tags.set(set_tags, clear=True)
        logger.debug(f"--\tAction: Set tags to {set_tags}.")
        self.assertEqual(question.tags.count(), 2)
        self.assertTrue(question.tags.filter(name="git").exists())
        
        question.tags.clear()
        logger.debug(f"--\tAction: Cleared all tags.")
        self.assertEqual(question.tags.count(), 0)
        logger.debug(f"--\tAsserted: Tag operations for '{question_slug}' successful.")