import json
from langchain import PromptTemplate

from ..llm import get_llm
from config import Models
from ..FileManager import FileManager
from ..system import System


template = """
Determine the paths to all the files imported into the file below from the project root directory. Return the result as a python list of strings. The result must be a valid JSON BLOB.

{file}
"""

prompt = PromptTemplate(
    input_variables=["file"],
    template=template,
)


def _get_file_paths_from_seed_file_path(seed_file: str):
    llm = get_llm(Models.INTERPRETATION_MODEL)
    result = llm.run(prompt.format(file=seed_file))
    return json.loads(result)


def retrieve_files(_: System, file_manager: FileManager):
    seed_file_path = FileManager.seed_file_path
    if not seed_file_path:
        return

    file_paths = _get_file_paths_from_seed_file_path(seed_file_path)

    print(file_paths)

    for path in file_paths:
        file_manager.add_file(path)
