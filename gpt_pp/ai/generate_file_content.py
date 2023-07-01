import re
from typing import Optional

from langchain import PromptTemplate
from langchain.schema import HumanMessage

from config import Models

from ..llm import get_llm
from ..system import System

def _parse_code_block(code_block: str) -> Optional[str]:
    """Parse the code block for the file content."""
    pattern = r"```(\w+)\s+(.*?)\s+```"
    match = re.search(pattern, code_block, re.DOTALL)
    if match:
        return match.group(2)
    else:
        return None

get_content_template = """
{chat_history}
---
Given this chat conversation, generate the exact file content that should be pasted into the file at path "{file_path}". 
Return only the code block for this file. The code should be fully functional.
Ensure to implement all code, if you are unsure, write a plausible implementation.

Code for file {file_path}:
"""


def generate_file_content(system: System, path: str) -> Optional[str]:
    """Prompt an AI model for the file content to paste into the file at path."""
    prompt = PromptTemplate.from_template(get_content_template).format(
        chat_history=system.memory.load_messages_as_string(), file_path=path
    )
    llm = get_llm(Models.CODE_MODEL)

    result = llm([HumanMessage(content=prompt)])
    system.save_to_logs("generate_file_content", prompt, result.content)
    
    return _parse_code_block(result.content)
