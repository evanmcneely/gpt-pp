from typing import Any, List, Optional, Tuple, Union

from halo import Halo
from langchain import LLMChain, PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationChain
from langchain.chat_models.base import BaseChatModel
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory, BaseMessage, HumanMessage

import gpt_pp.ai.parsers as parsers
from config import VERBOSE, Models
from gpt_pp.ai import templates
from gpt_pp.ai.llm import get_llm

PromptType = Union[List[BaseMessage], str]
ListOfChangesType = Optional[List[Tuple[str, str]]]


class AI(BaseChatMessageHistory):
    code_llm: BaseChatModel
    interpret_llm: BaseChatModel
    converse_llm: BaseChatModel

    def __init__(self):
        self.code_llm = get_llm(Models.CODE_MODEL)
        self.interpret_llm = get_llm(Models.INTERPRETATION_MODEL)
        self.converse_llm = get_llm(Models.CONVERSATION_MODEL)

    @staticmethod
    def _run(model: BaseChatModel, prompt: PromptTemplate, **kwargs: Any) -> str:
        chain = LLMChain(llm=model, prompt=prompt, verbose=VERBOSE)
        result = chain.predict(**kwargs)
        return result

    @Halo(text="Retrieving relevant files", spinner="dots")
    def get_imported_file_paths(self, file: str) -> Optional[List[str]]:
        prompt = PromptTemplate.from_template(templates.file_imports)
        completion = self._run(self.interpret_llm, prompt, file=file)
        return parsers.extract_files(completion)

    def get_change_operations(self) -> ListOfChangesType:
        history = self.load_messages_as_string()
        prompt = PromptTemplate.from_template(templates.files_requiring_changes)
        completion = self._run(self.interpret_llm, prompt, chat_history=history)
        return parsers.extract_file_operations(completion)

    @Halo(text="Thinking", spinner="dots")
    def generate_clarifying_question(self) -> str:
        history = self.load_messages_as_string()
        prompt = PromptTemplate.from_template(templates.clarify)
        completion = self._run(self.converse_llm, prompt, chat_history=history)
        return completion

    def generate_code(self) -> str:
        history = self.load_messages_as_string()
        completion = self._run(self.code_llm, history)
        return completion

    def generate_diff(self, file_path: str) -> str:
        history = self.load_messages_as_string()
        prompt = PromptTemplate.from_template(templates.diff)
        completion = self._run(
            self.code_llm, prompt, chat_history=history, file_path=file_path
        )
        return completion

    def generate_file_content(self, file_path: str) -> Optional[str]:
        history = self.load_messages_as_string()
        prompt = PromptTemplate.from_template(templates.file_content)
        completion = self._run(
            self.code_llm, prompt, chat_history=history, file_path=file_path
        )
        return parsers.extract_code_block(completion)

    def get_chat(self, files: str) -> ConversationChain:
        llm = get_llm(
            Models.CODE_MODEL,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
        memory = ConversationBufferMemory()
        memory.save_context({"input": files}, {"output": "Ask a question."})

        return ConversationChain(
            llm=llm,
            verbose=VERBOSE,
            memory=memory,
        )

    def load_messages_as_string(self) -> str:
        """Convert chat messages to a string and return it."""
        messages: List[BaseMessage] = self.messages
        history: str = ""

        for message in messages:
            if message.type == "system":
                history += "System: " + message.content + "\n"
            elif message.type == "human":
                history += "Human: " + message.content + "\n"
            elif message.type == "ai":
                history += "AI Assistant: " + message.content + "\n"

        return history

    def clear(self):
        self.messages = []
