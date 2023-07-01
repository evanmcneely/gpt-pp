from langchain import PromptTemplate
from langchain.schema import HumanMessage

from config import Models

from ..llm import get_llm
from ..system import System


get_diff_template = """
Generate the universal diff that would need to be applied the file at path "{file_path}" to create the changes outlined in the chat history below.

{chat_history}
"""


def generate_diff(system: System, path: str) -> str:
    """Prompt an AI model for the file content to paste into the file at path."""
    prompt = PromptTemplate.from_template(get_diff_template).format(
        chat_history=system.memory.load_messages_as_string(), file_path=path
    )
    llm = get_llm(Models.CODE_MODEL)

    result = llm([HumanMessage(content=prompt)])
    system.save_to_logs("generate_diff", prompt, result.content)

    return result.content.strip("\n ")
