# questions/tests/test_commands.py

import json
import tempfile
# import shutil # Not strictly needed if TemporaryDirectory is used well
from pathlib import Path
from typing import Any # For _write_json_to_file type hint
from io import StringIO
import logging # Import logging

from django.core.management import call_command, CommandError
from django.test import TestCase, override_settings
from django.conf import settings

# Adjust the import path if your models are located elsewhere
from questions.models import TutorialTitle, Question
# from taggit.models import Tag # Uncomment if you need to query Tag model directly

logger = logging.getLogger(__name__) # Logger for this test module

# --- Sample JSON Data Structures for Tests ---
SAMPLE_DATA_SET_1 = [
    {
        "title-id": "tut01",
        "question-id": "q001-git-whatis",
        "question": "What is Git?",
        "answer_a": "A", "answer_b": "B", "answer_c": "C", "answer_d": "D",
        "correct_answer": "b", "difficulty": "easy", "tags": ["initial", "git"]
    },
    {
        "title-id": "tut01",
        "question-id": "q002-extra",
        "question": "Extra question?",
        "answer_a": "E", "answer_b": "F", "answer_c": "G", "answer_d": "H",
        "correct_answer": "e", "difficulty": "easy", "tags": ["extra", "git"]
    }
]

SAMPLE_DATA_SET_2_UPDATES_AND_NEW = [
    {
        "title-id": "tut01",
        "question-id": "q001-git-whatis",
        "question": "What is Git? (Updated Definition)",
        "answer_a": "A fruit", "answer_b": "A distributed version control system (DVCS)",
        "answer_c": "An AI model", "answer_d": "A browser plugin",
        "correct_answer": "b", "difficulty": "medium",
        "tags": ["git", "vcs", "basics", "updated"]
    },
    {
        "title-id": "tut01",
        "question-id": "q003-git-branch",
        "question": "What is a Git branch?",
        "answer_a": "A part of a tree", "answer_b": "A separate line of development",
        "answer_c": "A type of commit", "answer_d": "A merge strategy",
        "correct_answer": "b", "difficulty": "easy", "tags": ["git", "branching"]
    }
]

SAMPLE_DATA_SET_3_NEW_TITLE = [
    {
        "title-id": "tut02-advanced",
        "question-id": "q201-rebase-concept",
        "question": "Explain Git rebase.",
        "answer_a": "Modifying base settings", "answer_b": "Rewriting commit history for a linear sequence",
        "answer_c": "A type of fish", "answer_d": "A server configuration",
        "correct_answer": "b", "difficulty": "hard", "tags": ["git", "rebase", "advanced"]
    }
]

MALFORMED_JSON_STRING = "{'key': 'value',, 'invalid': true}"
EMPTY_JSON_LIST_STRING = "[]"
JSON_WITH_MISSING_IDS_DATA = [
    {"title-id": "tut03", "question": "No question ID here", "correct_answer": "a", "tags":[]},
    {"question-id": "q301", "question": "No title ID here", "correct_answer": "b", "tags":[]}
]
JSON_NOT_A_LIST_AT_ROOT = "{ \"error\": \"This is not a list of questions\" }"


class LoadQuestionsCommandTest(TestCase):
    def setUp(self):
        logger.info(f"LoadQuestionsCommandTest.setUp()")
        self.temp_dir_obj = tempfile.TemporaryDirectory(prefix="django_test_q_cmd_")
        self.temp_dir_path = Path(self.temp_dir_obj.name)
        logger.debug(f"--\tData: Created temporary directory: {self.temp_dir_path}")

        self.sub_dir = self.temp_dir_path / "subdir_for_tests"
        self.sub_dir.mkdir()
        logger.debug(f"--\tData: Created temporary subdirectory: {self.sub_dir}")

    def tearDown(self):
        logger.info(f"LoadQuestionsCommandTest.tearDown()")
        self.temp_dir_obj.cleanup()
        logger.debug(f"--\tAction: Cleaned up temporary directory: {self.temp_dir_path}")

    def _write_json_to_file(self, dir_path: Path, filename: str, data_content: Any) -> Path:
        file_path = dir_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            if isinstance(data_content, str):
                f.write(data_content)
            else:
                json.dump(data_content, f, indent=2)
        return file_path

    @override_settings(QUESTION_DATA_DIRECTORIES=None)
    def test_load_new_questions_successfully(self):
        logger.info(f"LoadQuestionsCommandTest.{self._testMethodName}()")
        logger.debug("--\tAction: Preparing files for initial load.")
        file1_path = self._write_json_to_file(self.temp_dir_path, "dataset1.json", SAMPLE_DATA_SET_1)
        file3_path = self._write_json_to_file(self.sub_dir, "dataset3_new_title.json", SAMPLE_DATA_SET_3_NEW_TITLE)
        logger.debug(f"--\tData: Created {file1_path} and {file3_path}.")

        with override_settings(QUESTION_DATA_DIRECTORIES=[str(self.temp_dir_path)]):
            out = StringIO()
            logger.debug("--\tAction: Calling 'load_questions' command.")
            call_command('load_questions', stdout=out)

        logger.debug("--\tAsserting: Database counts and specific object data after new load.")
        self.assertEqual(TutorialTitle.objects.count(), 2)
        self.assertEqual(Question.objects.count(), 3)

        title1 = TutorialTitle.objects.get(title_id_slug="tut01")
        self.assertEqual(title1.questions.count(), 2)
        # ... (other specific data assertions remain) ...

        output = out.getvalue()
        self.assertIn("Found 2 JSON file(s) to process", output)
        self.assertIn("Questions newly created: 3", output)
        self.assertIn("Questions updated: 0", output)
        self.assertIn("Tutorial Titles newly created: 2", output)
        logger.debug("--\tAsserted: Command output for successful new load.")

    @override_settings(QUESTION_DATA_DIRECTORIES=None)
    def test_update_one_and_add_one_isolated(self):
        logger.info(f"LoadQuestionsCommandTest.{self._testMethodName}()")

        logger.debug("--\tAction: Initial data load (Run 1).")
        self._write_json_to_file(self.temp_dir_path, "setup_data_for_update_test.json", SAMPLE_DATA_SET_1)
        with override_settings(QUESTION_DATA_DIRECTORIES=[str(self.temp_dir_path)]):
            call_command('load_questions', stdout=StringIO())
        logger.debug("--\tData: Initial data loaded. DB Question count: %s", Question.objects.count())
        self.assertEqual(Question.objects.count(), 2) # Initial verification

        logger.debug("--\tAction: Preparing for isolated update/add data load (Run 2).")
        update_specific_dir_obj = tempfile.TemporaryDirectory(prefix="update_only_")
        update_specific_dir_path = Path(update_specific_dir_obj.name)
        self._write_json_to_file(update_specific_dir_path, "updates_and_new_isolated.json", SAMPLE_DATA_SET_2_UPDATES_AND_NEW)
        logger.debug(f"--\tData: Created isolated update file in {update_specific_dir_path}.")
        
        out = StringIO()
        with override_settings(QUESTION_DATA_DIRECTORIES=[str(update_specific_dir_path)]):
            logger.debug("--\tAction: Calling 'load_questions' command for isolated update.")
            call_command('load_questions', stdout=out)
        
        output = out.getvalue()
        update_specific_dir_obj.cleanup()

        logger.debug("--\tAsserting: Database state after isolated update/add.")
        self.assertEqual(TutorialTitle.objects.count(), 1)
        self.assertEqual(Question.objects.count(), 3)
        q_git_after_update = Question.objects.get(tutorial_title__title_id_slug="tut01", question_id_slug="q001-git-whatis")
        self.assertEqual(q_git_after_update.question_text, "What is Git? (Updated Definition)")
        self.assertEqual(q_git_after_update.difficulty, "medium")
        self.assertSetEqual(set(q_git_after_update.tags.names()), {"git", "vcs", "basics", "updated"})

        q_new_branch = Question.objects.get(tutorial_title__title_id_slug="tut01", question_id_slug="q003-git-branch")
        self.assertEqual(q_new_branch.question_text, "What is a Git branch?")

        logger.debug("--\tAsserting: Command output for isolated update/add.")
        self.assertIn("Found 1 JSON file(s) to process", output)
        self.assertIn("Questions newly created: 1", output)
        self.assertIn("Questions updated: 1", output)
        self.assertIn("Tutorial Titles newly created: 0", output)

    @override_settings(QUESTION_DATA_DIRECTORIES=None)
    def test_no_json_files_found(self):
        logger.info(f"LoadQuestionsCommandTest.{self._testMethodName}()")
        logger.debug("--\tData: Testing with an empty directory.")
        with override_settings(QUESTION_DATA_DIRECTORIES=[str(self.temp_dir_path)]):
            out = StringIO()
            call_command('load_questions', stdout=out)
        logger.debug("--\tAsserting: 'No JSON files found' in output and DB is empty.")
        self.assertIn("No JSON files found", out.getvalue())
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(TutorialTitle.objects.count(), 0)

    @override_settings(QUESTION_DATA_DIRECTORIES=None)
    def test_empty_json_list_file(self):
        logger.info(f"LoadQuestionsCommandTest.{self._testMethodName}()")
        logger.debug("--\tData: Creating an empty JSON list file.")
        self._write_json_to_file(self.temp_dir_path, "empty.json", [])
        with override_settings(QUESTION_DATA_DIRECTORIES=[str(self.temp_dir_path)]):
            out = StringIO()
            call_command('load_questions', stdout=out)
        output = out.getvalue()
        logger.debug("--\tAsserting: Correct processing of empty JSON list file.")
        self.assertIn("Files processed successfully (read and parsed): 1", output)
        self.assertIn("Questions newly created: 0", output)
        self.assertIn("Questions updated: 0", output)
        self.assertEqual(Question.objects.count(), 0)

    @override_settings(QUESTION_DATA_DIRECTORIES=None)
    def test_malformed_json_file(self):
        logger.info(f"LoadQuestionsCommandTest.{self._testMethodName}()")
        logger.debug("--\tData: Creating a malformed JSON file.")
        malformed_file_path = self._write_json_to_file(self.temp_dir_path, "malformed.json", MALFORMED_JSON_STRING)
        with override_settings(QUESTION_DATA_DIRECTORIES=[str(self.temp_dir_path)]):
            out = StringIO()
            call_command('load_questions', stdout=out)
        output = out.getvalue()
        logger.debug("--\tAsserting: Correct handling of malformed JSON file.")
        self.assertIn("Files skipped due to loading/parsing errors: 1", output)
        self.assertIn(f"Skipped file: {str(malformed_file_path)}", output)
        self.assertEqual(Question.objects.count(), 0)

    @override_settings(QUESTION_DATA_DIRECTORIES=None)
    def test_json_file_not_a_list_at_root(self):
        logger.info(f"LoadQuestionsCommandTest.{self._testMethodName}()")
        logger.debug("--\tData: Creating a JSON file where root is not a list.")
        not_list_file_path = self._write_json_to_file(self.temp_dir_path, "not_a_list.json", JSON_NOT_A_LIST_AT_ROOT)
        with override_settings(QUESTION_DATA_DIRECTORIES=[str(self.temp_dir_path)]):
            out = StringIO()
            call_command('load_questions', stdout=out)
        output = out.getvalue()
        logger.debug("--\tAsserting: Correct handling of JSON file not being a list.")
        self.assertIn("Files skipped due to loading/parsing errors: 1", output)
        self.assertIn(f"Skipped file: {str(not_list_file_path)}", output)
        self.assertEqual(Question.objects.count(), 0)

    @override_settings(QUESTION_DATA_DIRECTORIES=None)
    def test_json_entries_missing_required_ids(self):
        logger.info(f"LoadQuestionsCommandTest.{self._testMethodName}()")
        logger.debug("--\tData: Creating JSON file with entries missing required IDs.")
        self._write_json_to_file(self.temp_dir_path, "missing_ids.json", JSON_WITH_MISSING_IDS_DATA)
        with override_settings(QUESTION_DATA_DIRECTORIES=[str(self.temp_dir_path)]):
            out = StringIO()
            call_command('load_questions', stdout=out)
        output = out.getvalue()
        logger.debug("--\tAsserting: Correct handling of entries with missing IDs.")
        self.assertIn("Individual questions skipped (e.g., missing IDs, integrity issues): 2", output)
        self.assertEqual(Question.objects.count(), 0)

    def test_command_error_if_setting_not_defined(self):
        logger.info(f"LoadQuestionsCommandTest.{self._testMethodName}()")
        logger.debug("--\tData: Testing command failure when QUESTION_DATA_DIRECTORIES is not defined.")
        with override_settings(QUESTION_DATA_DIRECTORIES=None):
            with self.assertRaises(CommandError) as cm:
                call_command('load_questions')
            self.assertIn("Setting QUESTION_DATA_DIRECTORIES is not defined", str(cm.exception))
        logger.debug("--\tAsserted: CommandError raised as expected.")

    @override_settings(QUESTION_DATA_DIRECTORIES=["/this/path/is/fake/and/very/unlikely_to_exist_kjhgf"])
    def test_non_existent_directory_in_setting(self):
        logger.info(f"LoadQuestionsCommandTest.{self._testMethodName}()")
        logger.debug("--\tData: Testing with a non-existent directory in settings.")
        out = StringIO()
        call_command('load_questions', stdout=out)
        output = out.getvalue()
        logger.debug("--\tAsserting: 'No JSON files found' for non-existent directory.")
        self.assertIn("No JSON files found", output)
        self.assertEqual(Question.objects.count(), 0)