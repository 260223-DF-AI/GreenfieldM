import csv
import logging
from typing import List, Dict, Any
from exceptions import FileProcessingError

logger = logging.getLogger(__name__)

def read_with_encoding(filepath: str, encoding: str) -> List[Dict[str, Any]]:
    """
    Helper function to read a CSV file with a specific encoding.
    
    Returns: List of dictionaries (one per row)
    Raises: Empty if reading fails
    """
    with open(filepath, "r", encoding=encoding, newline="") as f:
        first = f.read(1)
        if first == "":
            return []
        f.seek(0)
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return []
        return [row for row in reader]

def read_csv_file(filepath):
    """
    Read a CSV file and return a list of dictionaries.
    
    Should handle:
    - FileNotFoundError
    - UnicodeDecodeError (try utf-8, then latin-1)
    - Empty files
    
    Returns: List of dictionaries (one per row)
    Raises: FileProcessingError with descriptive message
    """
    try:
        return read_with_encoding(filepath, "utf-8")
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise FileProcessingError(f"File not found: {filepath}")
    except UnicodeDecodeError:
        logger.warning(f"UnicodeDecodeError for utf-8, trying latin-1 for file: {filepath}")
        try:
            return read_with_encoding(filepath, "latin-1")
        except UnicodeDecodeError:
            logger.error(f"UnicodeDecodeError for latin-1 as well for file: {filepath}")
            raise FileProcessingError(f"Cannot decode file: {filepath} with utf-8 or latin-1")
    except Exception as e:
        logger.error(f"An unexpected error occurred while reading the file: {e}")
        raise FileProcessingError(f"An unexpected error occurred while reading the file: {e}")
    