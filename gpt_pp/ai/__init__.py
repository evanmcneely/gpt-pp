from typing import Any, List, Optional, Tuple, Union

from halo import Halo
from langchain import PromptTemplate
from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseMessage, HumanMessage

import gpt_pp.ai.parsers as parsers
from config import Models
from gpt_pp.ai import templates
from gpt_pp.ai.llm import get_llm

PromptType = Union[List[BaseMessage], str]
ListOfChangesType = Optional[List[Tuple[str, str]]]


class AI:
    code_llm: BaseChatModel
    interpret_llm: BaseChatModel
    converse_llm: BaseChatModel

    def __init__(self):
        self.code_llm = get_llm(Models.CODE_MODEL)
        self.interpret_llm = get_llm(Models.INTERPRETATION_MODEL)
        self.converse_llm = get_llm(Models.CONVERSATION_MODEL)

    @staticmethod
    def _get_prompt_from_template(template: str, **kwargs: Any) -> str:
        prompt_template = PromptTemplate.from_template(template)
        return prompt_template.format(**kwargs)

    @staticmethod
    def _wrap_prompt(prompt: PromptType) -> List[BaseMessage]:
        if isinstance(prompt, str):
            return [HumanMessage(content=prompt)]
        else:
            return prompt

    def _generate(self, prompt: PromptType) -> str:
        prompt = self._wrap_prompt(prompt)
        return self.code_llm(prompt).content

    def _interpret(self, prompt: PromptType) -> str:
        prompt = self._wrap_prompt(prompt)
        return self.interpret_llm(prompt).content

    def _converse(self, prompt: PromptType) -> str:
        prompt = self._wrap_prompt(prompt)
        return self.converse_llm(prompt).content

    @Halo(text="Retrieving relevant files", spinner="dots")
    def get_imported_file_paths(self, file: str) -> Optional[List[str]]:
        prompt = self._get_prompt_from_template(templates.file_imports, file=file)
        completion = self._interpret(prompt)
        return parsers.extract_files(completion)

    def get_change_operations(self, history: str) -> ListOfChangesType:
        prompt = self._get_prompt_from_template(
            templates.files_requiring_changes, chat_history=history
        )
        completion = self._interpret(prompt)
        return parsers.extract_file_operations(completion)

    @Halo(text="Thinking", spinner="dots")
    def generate_clarifying_question(self, chat_history: str) -> str:
        prompt = self._get_prompt_from_template(
            templates.clarify, chat_history=chat_history
        )
        completion = self._converse(prompt)
        return completion

    def generate_code(self, memory: PromptType) -> str:
        return self._generate(memory)

    def generate_diff(self, chat_history: str) -> str:
        prompt = self._get_prompt_from_template(
            templates.diff, chat_history=chat_history
        )
        completion = self._generate(prompt)  # type: ignore
        return completion

    def generate_file_content(self, chat_history: str, file_path: str) -> Optional[str]:
        prompt = self._get_prompt_from_template(
            templates.file_content, chat_history=chat_history, file_path=file_path
        )
        completion = self._generate(prompt)  # type: ignore
        return parsers.extract_code_block(completion)
