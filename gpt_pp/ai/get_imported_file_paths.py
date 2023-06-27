from typing import List, Optional

from halo import Halo
from langchain import PromptTemplate
from langchain.schema import HumanMessage

from config import Models

from ..file_utils import sanitize_input
from ..llm import get_llm
from ..system import System


def _parse_output(content: str) -> Optional[List[str]]:
    """Parse an AI models completion string into either a list of
    strings, split on the occurrence of a comma, or None if the
    end sequence 'nothing to import' is found.
    """
    if sanitize_input(content).lower() == "nothing to import":
        return None

    return content.split(",")


get_imports_prompt = """
Determine the paths to all the files imported into the files below from the project root directory in the form of ./path/to/file with the correct file extension. Return the result as a comma separated list of file paths. Don't return anything else, just the file paths. If there are no imported files return the string 'nothing to import'

{file}
"""


@Halo(text="Loading relative files", spinner="dots")
def get_imported_file_paths(system: System, file: str) -> Optional[List[str]]:
    """Prompt an AI model for a list of imported files given the content of a file.
    Return a list of the imported file paths or None if there are no imported files.
    """
    prompt = PromptTemplate.from_template(get_imports_prompt).format(file=file)
    llm = get_llm(Models.INTERPRETATION_MODEL)

    result = llm([HumanMessage(content=prompt)])

    system.save_to_logs("get_imported_file_paths", [prompt, result.content])

    return _parse_output(result.content)
