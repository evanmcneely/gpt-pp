from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory

from ..llm import get_llm
from config import Models


def format_initial_prompt(prompt: str, file_content: str) -> str:
    return f"""
    Instructions: {prompt}

    {file_content}
    """


template = """
Respond with a single question that you would need to ask to gain more clarity about how to follow the instructions. Provided is a history of your past interactions with the user. If there are no more clarifications required return the string "nothing left to clarify".

Chat History: 
{chat_history}
human: {user_message}

Question:
"""


def ask_for_clarification(memory: ConversationBufferMemory, user_message: str):
    chain = LLMChain(
        llm=get_llm(Models.CONVERSATION_MODEL),
        prompt=PromptTemplate.from_template(template),
        memory=memory,
    )

    question = chain.predict(user_message=user_message)
    return question
