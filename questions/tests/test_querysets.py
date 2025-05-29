# questions/tests/test_querysets.py
import logging
from django.test import TestCase
from ..models import TutorialTitle, Question

logger = logging.getLogger(__name__)

class QuestionQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        logger.info("Setting up test data for QuestionQuerySetTest...")
        # Create Tutorial Titles
        cls.title1 = TutorialTitle.objects.create(title_id_slug="tut-01", name="Tutorial One")
        logger.debug(f"--\tData: Created TutorialTitle slug='{cls.title1.title_id_slug}'.")
        cls.title2 = TutorialTitle.objects.create(title_id_slug="tut-02", name="Tutorial Two")
        logger.debug(f"--\tData: Created TutorialTitle slug='{cls.title2.title_id_slug}'.")

        # Create Questions with various attributes
        cls.q1 = Question.objects.create(
            tutorial_title=cls.title1, question_id_slug="q1", question_text="Q1 Text (Easy, git, python)",
            answer_a="A", answer_b="B", answer_c="C", answer_d="D", correct_answer="a",
            difficulty=Question.Difficulty.EASY
        )
        cls.q1.tags.add("git", "python")
        logger.debug(f"--\tData: Created Question slug='{cls.q1.question_id_slug}' (Title: {cls.title1.title_id_slug}, Diff: Easy, Tags: git, python).")

        cls.q2 = Question.objects.create(
            tutorial_title=cls.title1, question_id_slug="q2", question_text="Q2 Text (Medium, django)",
            answer_a="A", answer_b="B", answer_c="C", answer_d="D", correct_answer="b",
            difficulty=Question.Difficulty.MEDIUM
        )
        cls.q2.tags.add("django")
        logger.debug(f"--\tData: Created Question slug='{cls.q2.question_id_slug}' (Title: {cls.title1.title_id_slug}, Diff: Medium, Tags: django).")

        cls.q3 = Question.objects.create(
            tutorial_title=cls.title2, question_id_slug="q3", question_text="Q3 Text (Easy, git)",
            answer_a="A", answer_b="B", answer_c="C", answer_d="D", correct_answer="c",
            difficulty=Question.Difficulty.EASY
        )
        cls.q3.tags.add("git")
        logger.debug(f"--\tData: Created Question slug='{cls.q3.question_id_slug}' (Title: {cls.title2.title_id_slug}, Diff: Easy, Tags: git).")
        
        cls.q4 = Question.objects.create(
            tutorial_title=cls.title2, question_id_slug="q4", question_text="Q4 Text (Hard, No Tags)",
            answer_a="A", answer_b="B", answer_c="C", answer_d="D", correct_answer="d",
            difficulty=Question.Difficulty.HARD
        )
        logger.debug(f"--\tData: Created Question slug='{cls.q4.question_id_slug}' (Title: {cls.title2.title_id_slug}, Diff: Hard, No Tags).")

        # Question 5 (Title 2, Medium, Tag: unique-edge-tag) for edge case testing
        cls.q5 = Question.objects.create(
            tutorial_title=cls.title2, question_id_slug="q5-edge", question_text="Q5 Edge Text (Medium, unique-edge-tag)",
            answer_a="A", answer_b="B", answer_c="C", answer_d="D", correct_answer="a",
            difficulty=Question.Difficulty.MEDIUM 
        )
        cls.q5.tags.add("unique-edge-tag")
        logger.debug(f"--\tData: Created Question slug='{cls.q5.question_id_slug}' (Title: {cls.title2.title_id_slug}, Diff: Medium, Tags: unique-edge-tag).")
        logger.info("Test data setup complete for QuestionQuerySetTest. Total questions: 5.")

    # --- Existing Tests (Ensure counts are updated from 4 to 5 where applicable) ---

    def test_get_interactive_no_filters(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        logger.debug("--\tAction: Calling get_interactive_quiz_questions with no filters.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions()
        
        expected_count = 5 # UPDATED from 4
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} (all questions).")
        self.assertEqual(qs.count(), expected_count)
        
        expected_order = [self.q1, self.q2, self.q3, self.q4, self.q5] # UPDATED to include q5
        logger.debug(f"--\tAsserting: Correct order of questions: {[q.question_id_slug for q in expected_order]}.")
        self.assertListEqual(list(qs), expected_order)
        logger.debug(f"--\tAsserted: All questions returned in default order.")

    def test_filter_by_title_id_slug(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        test_title_slug = "tut-01"
        logger.debug(f"--\tAction: Calling get_interactive_quiz_questions with title_id_slug='{test_title_slug}'.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(title_id_slug=test_title_slug)
        
        expected_count = 2
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} for title_id_slug='{test_title_slug}'.")
        self.assertEqual(qs.count(), expected_count)
        logger.debug(f"--\tAsserting: Question '{self.q1.question_id_slug}' is in the queryset.")
        self.assertIn(self.q1, qs)
        logger.debug(f"--\tAsserting: Question '{self.q2.question_id_slug}' is in the queryset.")
        self.assertIn(self.q2, qs)
        logger.debug(f"--\tAsserted: Correct questions returned for title_id_slug='{test_title_slug}'.")

    def test_filter_by_difficulty_levels_single(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        test_difficulty = [Question.Difficulty.EASY]
        logger.debug(f"--\tAction: Calling get_interactive_quiz_questions with difficulty_levels={test_difficulty}.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(difficulty_levels=test_difficulty)
        
        expected_count = 2 
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} for difficulty_levels={test_difficulty}.")
        self.assertEqual(qs.count(), expected_count)
        logger.debug(f"--\tAsserting: Question '{self.q1.question_id_slug}' (Easy) is in the queryset.")
        self.assertIn(self.q1, qs)
        logger.debug(f"--\tAsserting: Question '{self.q3.question_id_slug}' (Easy) is in the queryset.")
        self.assertIn(self.q3, qs)
        logger.debug(f"--\tAsserted: Correct questions returned for single difficulty.")

    def test_filter_by_difficulty_levels_multiple(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        # q1 (Easy), q2 (Medium), q3 (Easy), q5 (Medium)
        test_difficulties = [Question.Difficulty.EASY, Question.Difficulty.MEDIUM]
        logger.debug(f"--\tAction: Calling get_interactive_quiz_questions with difficulty_levels={test_difficulties}.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(difficulty_levels=test_difficulties)
        
        expected_count = 4 # UPDATED q1, q2, q3, q5
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} for difficulty_levels={test_difficulties}.")
        self.assertEqual(qs.count(), expected_count)
        self.assertIn(self.q1, qs)
        self.assertIn(self.q2, qs)
        self.assertIn(self.q3, qs)
        self.assertIn(self.q5, qs)
        logger.debug(f"--\tAsserted: Correct questions returned for multiple difficulties.")
        
    def test_filter_by_difficulty_levels_empty_list(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        test_difficulties = []
        logger.debug(f"--\tAction: Calling get_interactive_quiz_questions with empty difficulty_levels list.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(difficulty_levels=test_difficulties)
        
        expected_count = 5 # UPDATED from 4
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} (all questions) when difficulty_levels is empty.")
        self.assertEqual(qs.count(), expected_count)
        logger.debug(f"--\tAsserted: Empty difficulty list correctly ignored.")

    def test_filter_by_tag_names_single(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        test_tags = ["python"]
        logger.debug(f"--\tAction: Calling get_interactive_quiz_questions with tag_names={test_tags}.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(tag_names=test_tags)
        
        expected_count = 1
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} for tag_names={test_tags}.")
        self.assertEqual(qs.count(), expected_count)
        logger.debug(f"--\tAsserting: Question '{self.q1.question_id_slug}' (Tags: git, python) is in the queryset.")
        self.assertIn(self.q1, qs)
        logger.debug(f"--\tAsserted: Correct questions returned for single tag.")

    def test_filter_by_tag_names_multiple(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        test_tags = ["git", "django"] # q1 (git), q2 (django), q3 (git)
        logger.debug(f"--\tAction: Calling get_interactive_quiz_questions with tag_names={test_tags}.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(tag_names=test_tags)
        
        expected_count = 3
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} for tag_names={test_tags}.")
        self.assertEqual(qs.count(), expected_count)
        self.assertIn(self.q1, qs)
        self.assertIn(self.q2, qs)
        self.assertIn(self.q3, qs)
        logger.debug(f"--\tAsserted: Correct questions returned for multiple tags (OR logic).")
        
    def test_filter_by_tag_names_empty_list(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        test_tags = []
        logger.debug(f"--\tAction: Calling get_interactive_quiz_questions with empty tag_names list.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(tag_names=test_tags)
        
        expected_count = 5 # UPDATED from 4
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} (all questions) when tag_names is empty.")
        self.assertEqual(qs.count(), expected_count)
        logger.debug(f"--\tAsserted: Empty tag list correctly ignored.")

    def test_combined_filters_title_and_difficulty(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        test_title_slug = "tut-01"
        test_difficulty = [Question.Difficulty.EASY]
        logger.debug(f"--\tAction: Calling with title_id_slug='{test_title_slug}' AND difficulty_levels={test_difficulty}.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(
            title_id_slug=test_title_slug, 
            difficulty_levels=test_difficulty
        )
        
        expected_count = 1
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} for combined title and difficulty.")
        self.assertEqual(qs.count(), expected_count)
        logger.debug(f"--\tAsserting: Question '{self.q1.question_id_slug}' is the expected result.")
        self.assertIn(self.q1, qs)
        logger.debug(f"--\tAsserted: Correct questions returned for combined title and difficulty.")

    def test_combined_filters_title_difficulty_tags(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        test_title_slug = "tut-01"
        test_difficulty = [Question.Difficulty.EASY]
        test_tags = ["git"]
        logger.debug(f"--\tAction: Calling with title_id_slug='{test_title_slug}', difficulty_levels={test_difficulty}, AND tag_names={test_tags}.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(
            title_id_slug=test_title_slug, 
            difficulty_levels=test_difficulty,
            tag_names=test_tags
        )
        
        expected_count = 1
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} for combined title, difficulty, and tags.")
        self.assertEqual(qs.count(), expected_count)
        logger.debug(f"--\tAsserting: Question '{self.q1.question_id_slug}' is the expected result.")
        self.assertIn(self.q1, qs)
        logger.debug(f"--\tAsserted: Correct questions returned for combined title, difficulty, and tags.")

    def test_eager_loading(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        test_title_slug = "tut-01" 
        logger.debug(f"--\tAction: Calling get_interactive_quiz_questions for title_id_slug='{test_title_slug}' to test eager loading.")
        
        expected_queries = 2 
        with self.assertNumQueries(expected_queries):
            logger.debug(f"--\tPerforming query and accessing related fields within assertNumQueries({expected_queries}).")
            qs = Question.objects.get_queryset().get_interactive_quiz_questions(title_id_slug=test_title_slug)
            for q_instance in qs:
                _ = q_instance.tutorial_title.name 
                _ = list(q_instance.tags.all()) 
        logger.debug(f"--\tAsserted: Eager loading performed within {expected_queries} queries.")

    # --- New Edge Case Tests ---

    def test_edge_non_existent_title_id_slug(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        test_title_slug = "non-existent-title"
        logger.debug(f"--\tAction: Calling get_interactive_quiz_questions with non-existent title_id_slug='{test_title_slug}'.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(title_id_slug=test_title_slug)
        
        expected_count = 0
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} for non-existent title.")
        self.assertEqual(qs.count(), expected_count)
        logger.debug(f"--\tAsserted: Empty queryset for non-existent title_id_slug.")

    def test_edge_valid_title_non_matching_difficulty(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        test_title_slug = "tut-01" # Title 1 has Easy (q1) and Medium (q2)
        test_difficulty = [Question.Difficulty.HARD] # Hard difficulty only exists for Title 2 (q4)
        logger.debug(f"--\tAction: Calling with title_id_slug='{test_title_slug}' and non-matching difficulty_levels={test_difficulty}.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(
            title_id_slug=test_title_slug,
            difficulty_levels=test_difficulty
        )
        
        expected_count = 0
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} for title with non-matching difficulty.")
        self.assertEqual(qs.count(), expected_count)
        logger.debug(f"--\tAsserted: Empty queryset for title with non-matching difficulty.")

    def test_edge_valid_title_non_matching_tag(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        test_title_slug = "tut-01" # q1 (git, python), q2 (django)
        test_tag = ["unique-edge-tag"] # This tag is only on q5 (tut-02)
        logger.debug(f"--\tAction: Calling with title_id_slug='{test_title_slug}' and non-matching tag_names={test_tag}.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(
            title_id_slug=test_title_slug,
            tag_names=test_tag
        )
        
        expected_count = 0
        logger.debug(f"--\tAsserting: Queryset count is {expected_count} for title with non-matching tag.")
        self.assertEqual(qs.count(), expected_count)
        logger.debug(f"--\tAsserted: Empty queryset for title with non-matching tag.")

    def test_edge_difficulty_levels_with_invalid_string(self):
        logger.info(f"QuestionQuerySetTest.{self._testMethodName}()")
        # q1 (Easy), q3 (Easy)
        test_difficulties = [Question.Difficulty.EASY, "super-duper-hard-does-not-exist"] # Invalid difficulty string
        logger.debug(f"--\tAction: Calling with difficulty_levels containing a non-existent string: {test_difficulties}.")
        qs = Question.objects.get_queryset().get_interactive_quiz_questions(difficulty_levels=test_difficulties)
        
        expected_count = 2 # Only 'easy' questions should match
        logger.debug(f"--\tAsserting: Queryset count is {expected_count}, ignoring invalid difficulty string.")
        self.assertEqual(qs.count(), expected_count)
        self.assertIn(self.q1, qs)
        self.assertIn(self.q3, qs)
        logger.debug(f"--\tAsserted: Correctly filtered by valid difficulties, ignoring invalid string.")