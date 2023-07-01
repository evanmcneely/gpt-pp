from typing import List, Optional, Tuple

from langchain import PromptTemplate
from langchain.schema import HumanMessage

from config import Models

from ..llm import get_llm
from ..system import System
from ..file_utils import sanitize_input


def _parse_output(content: str) -> Optional[List[Tuple[str, str]]]:
    """Parse an AI models completion string into format represting the paths
    and operations of files, or None if the end sequence is found.
    """
    if sanitize_input(content).lower() == "no files need changes":
        return None

    lines = content.split("\n")
    output: List[Tuple[str, str]] = []
    for line in lines:
        path, operation = line.split(",")
        path = path.strip()
        operation = operation.strip().lower()
        output.append((path, operation))

    return output


get_imports_template = """
Return a list of file paths matched with the operation ("create", "patch" or "delete") that should be applied to the file to implement the instructions.

Format the response like this:
PATH, OPERATION
PATH, OPERATION
PATH, OPERATION
... as many times as needed

PATH is the path to the file from the project directory, e.g. ./path/to/file.py
OPERATION is either "create" (file needs to be created), "patch" (file content needs to be updated), or "delete" (file needs to be deleted)

Example output:
./path/to/file.py, create
./anouther/file.py, patch
./last/file.py, delete


{chat_history}
"""


def get_files_that_require_changes(system: System) -> Optional[List[Tuple[str, str]]]:
    """Prompt an AI model for a list of files that need to be
    changed along with the operation (create, patch, delete).
    """
    prompt = PromptTemplate.from_template(get_imports_template).format(
        chat_history=system.memory.load_messages_as_string()
    )
    llm = get_llm(Models.INTERPRETATION_MODEL)

    result = llm([HumanMessage(content=prompt)])

    system.save_to_logs("get_files_that_require_changes", prompt, result.content)

    return _parse_output(result.content)
