import re
from typing import List, Optional, Tuple

from ..file_utils import sanitize_path


def extract_file_operations(content: str) -> Optional[List[Tuple[str, str]]]:
    """Parse an AI models completion string into format represting the paths
    and operations of files, or None if the end sequence is found.
    """
    if content.strip(" \n").lower() == "no files need changes":
        return None

    lines = content.split("\n")
    output: List[Tuple[str, str]] = []
    for line in lines:
        path, operation = line.split(",")
        path = path.strip()
        operation = operation.strip().lower()
        output.append((path, operation))

    return output


def extract_code_block(code_block: str) -> str:
    """Parse the code block for the file content."""
    pattern = r"```(\w+)\s+(.*?)\s+```"
    match = re.search(pattern, code_block, re.DOTALL)
    if match:
        return match.group(2)
    else:
        return code_block


def extract_files(content: str) -> Optional[List[str]]:
    """Parse an AI models completion string into either a list of
    strings, split on the occurrence of a comma, or None if the
    end sequence 'nothing to import' is found.
    """
    if content.strip(" \n").lower() == "nothing to import":
        return None

    return [sanitize_path(p) for p in content.split(",")]
