import re
from typing import List, Tuple

from halo import Halo

from config import Models

from ..file_utils import sanitize_path
from ..llm import get_llm
from ..system import System

code_prompt = """
Write the code that meets the instruction requirements.

Start by thinking about how you are going to implement the code. Document your thoughts.

Then write the code needed for each file. Please note that the code should be fully functional. No placeholders.
"""

diff_prompt = """
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
./main.py, 1
```python
print("hello world")
```

Example 2:
./src/components/MyComponent.tsx, 7
```tsx
const MyComponent = () => (
    <div>Hello World</div>
)
````
"""


def _codeblock_search(chat: str):
    """Apply a regex on a chat string and return the matches."""
    regex = r"(\S+)(?:, (\d+))?\n\s*```[^\n]*\n(.+?)```"
    return re.finditer(regex, chat, re.DOTALL)


def _parse_chat(chat: str) -> List[Tuple[str, int, str]]:
    """Parse an AI models completion string into a list of 
    touples (path, position, code).
    """
    matches = _codeblock_search(chat)

    files = []
    for match in matches:
        path = sanitize_path(re.sub(r'[<>"|?*]', "", match.group(1)))
        position = int(match.group(2)) if match.group(2) else 1
        code = match.group(3)

        files.append((path, position, code))

    return files


@Halo(text="Generating code", spinner="dots")
def write_code(system: System) -> List[Tuple[str, int, str]]:
    """Prompt an AI model to write the code to fulfill the instructions
    outlined in chat history. Return a list of tuples (path, position, code)
    representig the file path, position in the file and code block.
    """
    llm = get_llm(Models.CODE_MODEL)

    system.memory.add_user_message(code_prompt)
    code = llm(system.memory.get_messages())
    system.memory.add_ai_message(code.content)

    system.memory.add_user_message(diff_prompt)
    result = llm(system.memory.get_messages())
    system.memory.add_ai_message(result.content)

    system.save_to_logs(
        "write_code", [code_prompt, code.content, diff_prompt, result.content]
    )

    return _parse_chat(result.content)
