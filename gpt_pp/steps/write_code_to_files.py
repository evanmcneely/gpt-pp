from typing import List, Optional, Tuple

from halo import Halo

from ..ai.templates import generate_all_code
from ..system import System
from ..ui import UI


class file_operations:
    DELETE = "delete"
    PATCH = "patch"
    CREATE = "create"


@Halo(text="Generating code", spinner="dots")
def _get_code(system: System) -> Optional[List[Tuple[str, str]]]:
    memory = system.memory
    ai = system.ai

    memory.add_user_message(generate_all_code)
    code = ai.generate_code(memory.get_messages())

    memory.add_ai_message(code)
    files = ai.get_change_operations(memory.load_messages_as_string())

    return files


def _patch_file(system: System, path: str):
    chat = system.memory.load_messages_as_string()
    diff = system.ai.generate_diff(chat)
    system.project.apply_patch(path, diff)


def _create_file(system: System, path: str):
    chat = system.memory.load_messages_as_string()
    content = system.ai.generate_file_content(chat, path)
    if content:
        system.project.create(path, content)


@Halo(text="Updating files", spinner="dots")
def _write_to_file_system(
    system: System, changes: List[Tuple[str, str]]
) -> List[Tuple[str, bool, Optional[str]]]:
    change_status = []

    for file in changes:
        try:
            path = file[0]
            operation = file[1]

            if operation == file_operations.DELETE:
                system.project.delete(path)
            elif operation == file_operations.PATCH:
                _patch_file(system, path)
            elif operation == file_operations.CREATE:
                _create_file(system, path)
            else:
                raise Exception("Failed to generate file content")

            change_status.append((path, True, None))

        except Exception as e:
            change_status.append((path, False, str(e)))  # type: ignore

    return change_status


def write_code_to_files(system: System):
    """Generate code to implement the instructions in chat history and write
    those changes to the file system.
    """
    required_changes = _get_code(system)
    if not required_changes:
        return None
    change_status = _write_to_file_system(system, required_changes)

    for path, status, message in change_status:
        if status:
            UI.success(path)
        else:
            UI.fail(f"{path} - {message}")
