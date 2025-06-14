# questions/management/logic.py
import logging
from typing import List, Dict, Any
from pathlib import Path
from django.db import transaction, IntegrityError

from questions.models import TutorialTitle, Question
from .utils import load_json_data

logger = logging.getLogger(__name__)


def _create_or_update_question(
    q_data: Dict[str, Any],
    tutorial_title_instance: TutorialTitle,
    file_path_str: str,
) -> Dict[str, bool]:
    """Helper to create or update a single question."""
    question_id_slug = q_data.get("question-id")
    if not question_id_slug:
        logger.warning(
            f"Skipping question due to missing 'question-id' in {file_path_str}. Data: {q_data}"
        )
        return {"created": False, "updated": False, "skipped_malformed": True}

    defaults = {
        "question_text": q_data.get("question", ""),
        "answer_a": q_data.get("answer_a", ""),
        "answer_b": q_data.get("answer_b", ""),
        "answer_c": q_data.get("answer_c", ""),
        "answer_d": q_data.get("answer_d", ""),
        "correct_answer": str(
            q_data.get("correct_answer", "")
        ).lower(),  # Ensure lowercase
        "difficulty": str(
            q_data.get("difficulty", Question.Difficulty.EASY)
        ).lower(),  # Ensure lowercase
    }

    try:
        question, created = Question.objects.update_or_create(
            tutorial_title=tutorial_title_instance,
            question_id_slug=question_id_slug,
            defaults=defaults,
        )

        tags_list = q_data.get("tags", [])
        if isinstance(tags_list, list):
            question.tags.set(tags_list)  # set() clears old and adds new ones
        else:
            logger.warning(
                f"Tags data for question '{question_id_slug}' in '{file_path_str}' is not a list. Skipping tags update."
            )

        return {
            "created": created,
            "updated": not created,
            "skipped_malformed": False,
        }

    except IntegrityError as e:
        logger.error(
            f"IntegrityError for question '{question_id_slug}' in '{file_path_str}': {e}. Data: {defaults}"
        )
        return {
            "created": False,
            "updated": False,
            "skipped_malformed": True,
        }  # Count as malformed due to integrity
    except Exception as e:
        logger.error(
            f"Unexpected error creating/updating question '{question_id_slug}' in '{file_path_str}': {e}"
        )
        return {
            "created": False,
            "updated": False,
            "skipped_malformed": True,
        }  # Or a new 'failed' category


def process_single_json_file(file_path: Path, overall_stats: Dict) -> None:
    """Processes one JSON file and updates overall statistics."""
    logger.info(f"Processing file: {file_path}...")
    questions_data_list = load_json_data(file_path)

    if questions_data_list is None:  # Error during loading or invalid format
        overall_stats["files_skipped_error"] += 1
        overall_stats["skipped_files_list"].append(str(file_path))
        return

    overall_stats["files_processed"] += 1
    file_questions_created = 0
    file_questions_updated = 0
    file_questions_skipped = 0

    for q_data in questions_data_list:
        title_id_slug = q_data.get("title-id")
        if not title_id_slug:
            logger.warning(
                f"Skipping question entry due to missing 'title-id' in {file_path}. Data: {q_data}"
            )
            file_questions_skipped += 1
            continue

        try:
            # Use transaction for each question's related objects
            with transaction.atomic():
                tutorial_title_instance, tt_created = (
                    TutorialTitle.objects.get_or_create(
                        title_id_slug=title_id_slug,
                        defaults={
                            "name": q_data.get("title_name", title_id_slug)
                        },
                    )
                )
                if tt_created:
                    overall_stats["titles_created"] += 1
                    logger.debug(f"Created TutorialTitle: {title_id_slug}")

                result = _create_or_update_question(
                    q_data, tutorial_title_instance, str(file_path)
                )

                if result["created"]:
                    file_questions_created += 1
                elif result["updated"]:
                    file_questions_updated += 1
                elif result["skipped_malformed"]:
                    file_questions_skipped += 1

        except Exception as e:
            logger.error(
                f"Critical error processing an entry in {file_path} for title '{title_id_slug}': {e}"
            )
            file_questions_skipped += (
                1  # Count as skipped due to critical error
            )

    overall_stats["questions_created"] += file_questions_created
    overall_stats["questions_updated"] += file_questions_updated
    overall_stats["questions_skipped_malformed"] += file_questions_skipped
    logger.info(
        f"Finished processing {file_path}: {file_questions_created} created, {file_questions_updated} updated, {file_questions_skipped} skipped."
    )


def load_questions_from_json_files(
    json_file_paths: List[Path],
) -> Dict[str, Any]:
    """
    Main logic function to iterate through JSON files and load questions.
    """
    stats = {
        "total_files_found": len(json_file_paths),
        "files_processed": 0,
        "files_skipped_error": 0,  # Files that couldn't be read or had major format issues
        "skipped_files_list": [],
        "titles_created": 0,
        "questions_created": 0,
        "questions_updated": 0,
        "questions_skipped_malformed": 0,  # Questions skipped due to missing IDs or integrity errors
    }

    if not json_file_paths:
        logger.info("No JSON files provided to process.")
        return stats

    for file_path in json_file_paths:
        process_single_json_file(file_path, stats)

    return stats
