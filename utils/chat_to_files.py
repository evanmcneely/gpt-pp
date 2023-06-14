import re
from typing import List, Tuple


def _codeblock_search(chat: str) -> re.Match:
    regex = r"```(.*?)```"
    return re.finditer(regex, chat, re.DOTALL)


def parse_chat(chat) -> List[Tuple[str, str]]:
    matches = _codeblock_search(chat)

    files = []
    for match in matches:
        lines = match.group(1).split("\n")
        method, path = lines[0].split(" ")
        code = "\n".join(lines[1:])
        files.append((method, path, code))

    return files
