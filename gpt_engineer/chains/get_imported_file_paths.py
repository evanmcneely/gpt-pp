import os
from langchain import PromptTemplate, LLMChain
from langchain.output_parsers import CommaSeparatedListOutputParser

from ..llm import get_llm
from config import Models

prompt = """
Determine the paths to all the files imported into the file below from the project root directory in the form of ./path/to/file . Return the result as a comma separated list of file paths. Don't return anything else, just the file paths

{file}
"""


def get_imported_file_paths(file: str):
    chain = LLMChain(
        llm=get_llm(Models.INTERPRETATION_MODEL),
        prompt=PromptTemplate.from_template(prompt),
        output_parser=CommaSeparatedListOutputParser(),
    )

    return chain.predict(file=file)
