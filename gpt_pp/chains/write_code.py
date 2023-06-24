from halo import Halo
import re
from typing import List, Tuple

from langchain import PromptTemplate, LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import StreamingStdOutCallbackHandler

from ..llm import get_llm
from ..file_utils import sanitize_path
from config import Models

first_prompt = """
Write the code that meets the instruction requirements.

Start by thinking about how you are going to implement the code. Document your thoughts.

Then write the code needed for each file. Please note that the code should be fully functional. No placeholders.

Instructions:
{chat_history}

"""

second_prompt = """
Format the code into the following structure. The code should be fully functional. No placeholders and no examples.

Each file must strictly follow a markdown code block format, where the following tokens must be replaced such that
- FILEPATH (string): is the file path from the projects root directory including the file extension (start file paths with './')
- LANG (string): is the markup code block language for the code's language
- POSITION (integer): is the position in the file the code is to be inserted.
- CODE (string): is the code

FILEPATH, POSITION
```LANG
CODE
```

Example 1:
/main.py, 1
```python
print("hello world")
```

Example 2:
/src/components/MyComponent.tsx, 7
```tsx
const MyComponent = () => (
    <div>Hello World</div>
)
````

Here is the code that we need to format
{the_code}

"""


def _codeblock_search(chat: str):
    regex = r"(\S+)(?:, (\d+))?\n\s*```[^\n]*\n(.+?)```"
    return re.finditer(regex, chat, re.DOTALL)


def _parse_chat(chat: str):
    matches = _codeblock_search(chat)

    files = []
    for match in matches:
        path = sanitize_path(re.sub(r'[<>"|?*]', "", match.group(1)))
        position = int(match.group(2)) if match.group(2) else 0
        code = match.group(3)

        files.append((path, position, code))

    return files


@Halo(text="Generating code", spinner="dots")
def write_code(memory: str):
    write = LLMChain(
        llm=get_llm(Models.CODE_MODEL),
        prompt=PromptTemplate(input_variables=["chat_history"], template=first_prompt),
    )

    format = LLMChain(
        llm=get_llm(Models.CODE_MODEL),
        prompt=PromptTemplate(input_variables=["the_code"], template=second_prompt),
    )

    chain = SimpleSequentialChain(chains=[write, format])

    result = chain.run(memory)

    return _parse_chat(result)
