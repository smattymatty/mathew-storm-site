# questions/management/commands/load_questions.py
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# Relative imports to sibling modules in the 'management' package
from ..utils import find_json_files
from ..logic import load_questions_from_json_files

logger = logging.getLogger(__name__) # Gets a logger named 'questions.management.commands.load_questions'

class Command(BaseCommand):
    help = 'Loads question data from JSON files specified in settings.QUESTION_DATA_DIRECTORIES into the database.'

    # Example of how to add arguments if needed later
    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         '--source',
    #         type=str,
    #         help='Specify a single JSON file or directory to process, overriding settings.',
    #     )
    #     parser.add_argument(
    #         '--dry-run',
    #         action='store_true',
    #         help="Run the command without actually saving to the database to see what would happen.",
    #     )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting question loading process..."))

        # Get folder paths from settings
        data_directories = getattr(settings, 'QUESTION_DATA_DIRECTORIES', None)
        if not data_directories or not isinstance(data_directories, list):
            raise CommandError(
                "Setting QUESTION_DATA_DIRECTORIES is not defined or is not a list in your settings.py. "
                "Please define it as a list of directory or file paths."
            )
        logger.info(f"Using QUESTION_DATA_DIRECTORIES: {data_directories}")

        # Find JSON files
        self.stdout.write("Searching for JSON files...")
        json_files_to_process = find_json_files(data_directories)

        if not json_files_to_process:
            self.stdout.write(self.style.WARNING("No JSON files found in the specified directories."))
            return

        self.stdout.write(f"Found {len(json_files_to_process)} JSON file(s) to process:")
        for f_path in json_files_to_process:
            self.stdout.write(f"  - {f_path}")

        # Process files using logic module
        self.stdout.write("Processing files and loading data into database...")
        stats = load_questions_from_json_files(json_files_to_process)

        # Output statistics
        self.stdout.write(self.style.SUCCESS("\n--- Import Process Summary ---"))
        self.stdout.write(f"Total JSON files found by scanner: {stats['total_files_found']}")
        self.stdout.write(f"Files processed successfully (read and parsed): {stats['files_processed']}")
        
        if stats['files_skipped_error'] > 0:
            self.stdout.write(self.style.WARNING(
                f"Files skipped due to loading/parsing errors: {stats['files_skipped_error']}"
            ))
            for skipped_f in stats['skipped_files_list']:
                self.stdout.write(self.style.WARNING(f"  - Skipped file: {skipped_f}"))

        self.stdout.write(f"Tutorial Titles newly created: {stats['titles_created']}")
        self.stdout.write(f"Questions newly created: {stats['questions_created']}")
        self.stdout.write(f"Questions updated: {stats['questions_updated']}")

        if stats['questions_skipped_malformed'] > 0:
            self.stdout.write(self.style.WARNING(
                f"Individual questions skipped (e.g., missing IDs, integrity issues): {stats['questions_skipped_malformed']}"
            ))
        
        self.stdout.write(self.style.SUCCESS("Question loading process finished."))