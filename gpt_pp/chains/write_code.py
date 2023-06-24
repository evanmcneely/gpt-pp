from halo import Halo
import re
from typing import List, Tuple

from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import StreamingStdOutCallbackHandler

from ..llm import get_llm
from config import Models

template = """
Write the code that meets the instruction requirements. Follow these instructions to do it.

First, think about how you are going to implement the code. Document your thoughts.

Then you will output the content for each file. Each file must strictly follow a markdown code block format, where the following tokens must be replaced such that
- FILEPATH is the file path in the projects root directory including the file extension (start file paths with '/')
- LANG is the markup code block language for the code's language
- POSITION is the position in the file the code is to be inserted.
- CODE is the code

FILEPATH, POSITION
```LANG
CODE
```

Please note that the code should be fully functional. No placeholders.


Chat history:
{chat_history}

Remember to follow the markdown code block format.

Begin
"""


def _codeblock_search(chat: str):
    regex = r"(\S+)(?:, (\d+))?\n\s*```[^\n]*\n(.+?)```"
    return re.finditer(regex, chat, re.DOTALL)


def _parse_chat(chat: str):
    matches = _codeblock_search(chat)
    print(chat)

    files = []
    for match in matches:
        # Strip the filename of any non-allowed characters and convert / to \
        path = re.sub(r'[<>"|?*]', "", match.group(1))
        position = int(match.group(2)) if match.group(2) else None
        # Remove leading and trailing brackets
        path = re.sub(r"^\[(.*)\]$", r"\1", path)

        # Remove leading and trailing backticks
        path = re.sub(r"^`(.*)`$", r"\1", path)

        # Remove trailing ]
        path = re.sub(r"\]$", "", path)

        # Get the code
        code = match.group(3)

        # Add the file to the list
        files.append((path, position, code))

    # Get all the text before the first ``` block
    explanation = chat.split("```")[0]

    # Return the files
    return files, explanation


@Halo(text="Generating code", spinner="dots")
def write_code(memory: str):
    chain = LLMChain(
        llm=get_llm(Models.CODE_MODEL),
        prompt=PromptTemplate.from_template(template),
    )

    result = chain.predict(chat_history=memory)

    return _parse_chat(result)
