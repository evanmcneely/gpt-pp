from typing import Optional
from halo import Halo

from langchain import PromptTemplate, LLMChain

from ..llm import get_llm
from config import Models
from ..file_utils import sanitize_input


def _parse_output(content: str) -> Optional[str]:
    if sanitize_input(content).lower() == "nothing to import":
        return None

    return content.split(",")


prompt = """
Determine the paths to all the files imported into the files below from the project root directory in the form of ./path/to/file with the correct file extension. Return the result as a comma separated list of file paths. Don't return anything else, just the file paths. If there are no imported files return the string 'nothing to import'

{file}
"""


@Halo(text="Loading relative files", spinner="dots")
def get_imported_file_paths(file: str):
    chain = LLMChain(
        llm=get_llm(Models.INTERPRETATION_MODEL),
        prompt=PromptTemplate.from_template(prompt),
    )

    result = chain.predict(file=file)

    return _parse_output(result)
