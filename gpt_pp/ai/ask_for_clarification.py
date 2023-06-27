from halo import Halo
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage

from config import Models

from ..llm import get_llm
from ..system import System


def format_initial_prompt(prompt: str, file_content: str) -> str:
    return f"""
    Instructions: {prompt}

    {file_content}
    """


clarification_prompt = """
Respond with a single question that you would need to ask to gain more clarity about how to follow the most recent instructions or feedback. Return just the question. If everything is clear, return the string "nothing left to clarify". You have been trusted to make assumptions, not every small detail needs to be clarified.

Chat History: 
{chat_history}
"""


@Halo(text="Thinking", spinner="dots")
def ask_for_clarification(system: System):
    prompt = PromptTemplate.from_template(clarification_prompt).format(
        chat_history=system.memory.load_messages_as_string()
    )
    llm = get_llm(Models.CONVERSATION_MODEL)

    result = llm([HumanMessage(content=prompt)])
    system.save_to_logs("ask_for_clarification", [prompt, result.content])

    return result.content
