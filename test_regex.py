import re
from typing import List, Tuple


# def _codeblock_search(chat: str) -> re.Match:
#     regex = r"(\S+)(?:, (\d+))?\n\s*```[^\n]*\n(.+?)```"
#     return re.finditer(regex, chat, re.DOTALL)


# def _parse_chat(chat) -> List[Tuple[str, str]]:
#     matches = _codeblock_search(chat)

#     files = []
#     for match in matches:
#         # Strip the filename of any non-allowed characters and convert / to \
#         path = re.sub(r'[<>"|?*]', "", match.group(1))

#         position = int(match.group(2)) if match.group(2) else None

#         # Remove leading and trailing brackets
#         path = re.sub(r"^\[(.*)\]$", r"\1", path)

#         # Remove leading and trailing backticks
#         path = re.sub(r"^`(.*)`$", r"\1", path)

#         # Remove trailing ]
#         path = re.sub(r"\]$", "", path)

#         # Get the code
#         code = match.group(2)

#         # Add the file to the list
#         files.append((path, code, position))


#     # Return the files
#     return files


def _codeblock_search(chat: str):
    regex = r"(\S+)(?:, (\d+))?\n\s*```[^\n]*\n(.+?)```"
    return re.finditer(regex, chat, re.DOTALL)


def _parse_chat(chat: str):
    matches = _codeblock_search(chat)

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

    # Return the files
    return files


chat = """  
bla bla bla

./main.py, 5
```python
print("hello")
```

./index.py, 7
```python
print("goodbye")
```
"""

print(_parse_chat(chat))
