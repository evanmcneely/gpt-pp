from typing import List, Optional, Tuple

from halo import Halo

from ..file_utils import ValidationError
from ..system import System
from ..ui import UI

from ..ai import (  # isort:skip
    generate_diff,
    generate_file_content,
    get_files_that_require_changes,
    write_code,
)


class file_operations:
    DELETE = "delete"
    PATCH = "patch"
    CREATE = "create"


@Halo(text="Generating code", spinner="dots")
def _get_code_and_file_changes(system: System) -> Optional[List[Tuple[str, str]]]:
    write_code(system)
    files = get_files_that_require_changes(system)
    return files


@Halo(text="Write to file system", spinner="dots")
def _write_to_file_system(
    system: System, changes: List[Tuple[str, str]]
) -> List[Tuple[str, bool, Optional[str]]]:
    change_status = []
    file_manager = system.file_manager

    for file in changes:
        try:
            path = file[0]
            operation = file[1]

            if operation == file_operations.DELETE:
                file_manager.delete(path)
            elif operation == file_operations.PATCH:
                diff = generate_diff(system, path)
                file_manager.apply_patch(path, diff)
            elif operation == file_operations.CREATE:
                content = generate_file_content(system, path)
                if content:
                    file_manager.add(path, content)
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
    required_changes = _get_code_and_file_changes(system)
    if not required_changes:
        return
    change_status = _write_to_file_system(system, required_changes)

    for path, status, message in change_status:
        if status:
            UI.success(path)
        else:
            UI.fail(f"{path} - {message}")

    system.save_to_logs("write_code_to_files", *change_status)
