from config import Models

from ..llm import get_llm
from ..system import System

code_prompt = """
Write the code that meets the instructions. 

Start by thinking about how you are going to implement the code. Document your thoughts.

Then write the code needed for each file. Please note that the code should be fully functional. No placeholders.
"""


def write_code(system: System) -> str:
    """Prompt an AI model to write the code to fulfill the instructions
    outlined in chat history. Return a list of tuples (path, position, code)
    representig the file path, position in the file and code block.
    """
    llm = get_llm(Models.CODE_MODEL)

    system.memory.add_user_message(code_prompt)
    code = llm(system.memory.get_messages())
    system.memory.add_ai_message(code.content)

    system.save_to_logs(
        "write_code",
        code_prompt,
        code.content,
    )

    return code
