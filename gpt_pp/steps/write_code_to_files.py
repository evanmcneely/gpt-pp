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
    ai = system.ai

    ai.add_user_message(generate_all_code)
    code = ai.generate_code()

    ai.add_ai_message(code)
    files = ai.get_change_operations()

    return files


def _patch_file(system: System, path: str):
    diff = system.ai.generate_diff(path)
    system.project.apply_patch(path, diff)


def _create_file(system: System, path: str):
    content = system.ai.generate_file_content(path)
    if content:
        system.project.create(path, content)


@Halo(text="Updating files", spinner="dots")
def _write_to_file_system(
    system: System, changes: List[Tuple[str, str]]
) -> List[Tuple[str, bool]]:
    change_status = []

    for file in changes:
        path = file[0]
        operation = file[1]

        success = False
        if operation == file_operations.DELETE:
            system.project.delete(path)
            success = True
        elif operation == file_operations.PATCH:
            success = _patch_file(system, path)
        elif operation == file_operations.CREATE:
            success = _create_file(system, path)

        change_status.append((path, success))

    return change_status


def write_code_to_files(system: System):
    """Generate code to implement the instructions in chat history and write
    those changes to the file system.
    """
    required_changes = _get_code(system)
    if not required_changes:
        return None
    change_status = _write_to_file_system(system, required_changes)

    for path, status in change_status:
        if status:
            UI.success(path)
        else:
            UI.fail(path)
