# questions/management/utils.py
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

def find_json_files(base_folder_paths: List[Path]) -> List[Path]:
    """
    Finds all .json files recursively within the given list of base folder paths.
    Also accepts individual file paths in the list.
    Returns a sorted list of unique Path objects.
    """
    json_files_set = set()
    for base_path_str in base_folder_paths:
        base_path = Path(base_path_str) # Ensure it's a Path object
        if base_path.is_dir():
            for file_path in base_path.rglob('*.json'):
                json_files_set.add(file_path.resolve())
        elif base_path.is_file() and base_path.suffix.lower() == '.json':
            json_files_set.add(base_path.resolve())
        else:
            logger.warning(f"Path specified in settings is neither a directory nor a JSON file: {base_path}")
    return sorted(list(json_files_set))

def load_json_data(file_path: Path) -> Optional[List[Dict[str, Any]]]:
    """
    Loads and parses JSON data from a file.
    Assumes the JSON file contains a list of question objects.
    Returns None if there's an error.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                logger.error(f"Invalid JSON format in {file_path}: Expected a list of questions, got {type(data)}.")
                return None
            return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading {file_path}: {e}")
        return None