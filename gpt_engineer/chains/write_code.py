import re
from typing import List, Tuple
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import StreamingStdOutCallbackHandler

from ..llm import get_llm
from config import Models

template = """
Write the code needed to implement the instructions and clarifications in the chat history below. Start by thinking about what the code should do what files you might need to create, update or delete. It is important to think before writing code. Then output the content of each file following the syntax below. Make sure that files contain all imports, types etc. The code should be fully functional. Make sure that code in different files are compatible with each other.

File syntax:
Follow this syntax when writing the code. The first line, following the three ` is the action to take, either "create", "update" or "delete". Following the action is the path of the file from the projects root directory.

example "create"
```create file.py/ts/html
[ADD YOUR CODE HERE]
```

example "update"
```update file.py/ts/html
[ADD YOUR CODE HERE]
```

example "delete"
```delete file.py/ts/html
```

Chat history:
{chat_history}

Begin
"""


def _codeblock_search(chat: str) -> re.Match:
    regex = r"```(.*?)```"
    return re.finditer(regex, chat, re.DOTALL)


def _parse_chat(chat) -> List[Tuple[str, str]]:
    matches = _codeblock_search(chat)

    files = []
    for match in matches:
        lines = match.group(1).split("\n")
        method, path = lines[0].split(" ")
        code = "\n".join(lines[1:])
        files.append((method, path, code))

    return files


def write_code(memory: str):
    chain = LLMChain(
        llm=get_llm(Models.CODE_MODEL),
        prompt=PromptTemplate.from_template(template),
    )

    result = chain.predict(chat_history=memory)
    print(result)
    return _parse_chat(result)
