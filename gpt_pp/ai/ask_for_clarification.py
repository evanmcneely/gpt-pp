from halo import Halo
from langchain import PromptTemplate
from langchain.schema import HumanMessage

from config import Models

from ..llm import get_llm
from ..system import System

clarification_template = """
Respond with a single question that you would need to ask to gain more clarity about how to follow the most recent instructions or feedback. Return just the question. If everything is clear, return the string "nothing left to clarify". You have been trusted to make assumptions, not every small detail needs to be clarified.

Chat History: 
{chat_history}
"""


@Halo(text="Thinking", spinner="dots")
def ask_for_clarification(system: System) -> str:
    """Prompt an AI model for a clarifying question about the
    instructions and file content.
    """
    prompt = PromptTemplate.from_template(clarification_template).format(
        chat_history=system.memory.load_messages_as_string()
    )
    llm = get_llm(Models.CONVERSATION_MODEL)

    result = llm([HumanMessage(content=prompt)])
    system.save_to_logs("ask_for_clarification", [prompt, result.content])

    return result.content
