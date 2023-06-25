from typing import Optional, Tuple

from ..system import System, DB
from ..FileManager import FileManager
from ..ChatMemory import ChatMemory
from ..ui import UI
from ..file_utils import (
    ValidationError,
    sanitize_input,
    resolve_path,
    is_directory_empty,
    validate_file_path,
    validate_directory_path,
)


def _get_project_from_workspace(workspace: DB) -> Optional[str]:
    try:
        project = sanitize_input(workspace["project"])
        if not project:
            return None

        abs_path = resolve_path(project)
        validate_directory_path(abs_path)

    except ValidationError:
        UI.error("Cannot use workspace project path")
        project = None
    except FileNotFoundError:
        project = None

    return project


def _get_file_from_workspace(workspace: DB, project: str) -> Optional[str]:
    try:
        file = sanitize_input(workspace["file"])
        if not file:
            return None

        abs_path = resolve_path(project, file)
        validate_file_path(abs_path)

    except ValidationError:
        UI.error("Cannot use workspace file path")
        file = None
    except FileNotFoundError:
        file = None

    return file


def _get_project_input() -> str:
    while True:
        project = UI.prompt(
            "Enter the relative path to the project directory you would like to work in"
        )
        project = sanitize_input(project)

        try:
            abs_path = resolve_path(project)
            validate_directory_path(abs_path)
            break

        except ValidationError:
            UI.error(f"Invalid path: {project}")
        except FileNotFoundError:
            UI.error(f"Directory not found: {project}")

    return project


def _get_file_input(project: str) -> str:
    while True:
        file = UI.prompt(
            "Enter the relative path to the file you would like to work in"
        )
        file = sanitize_input(file)
        try:
            path = resolve_path(project, file)
            validate_file_path(path)
            break
        except ValidationError:
            UI.error(f"Invalid path: {file}")
        except FileNotFoundError:
            UI.error(f"File not found: {file}")

    return file


def initialize(ignore_existing: bool):
    workspace = DB(resolve_path("workspace"))
    logs = DB(resolve_path("logs"))

    project: str = _get_project_from_workspace(workspace)
    if not project or ignore_existing:
        project = _get_project_input()
    else:
        UI.message(f"Using project {project}")

    empty_directory: bool = is_directory_empty(resolve_path(project))

    file = None
    if not empty_directory:
        file: str = _get_file_from_workspace(workspace, project)
        if not file or ignore_existing:
            file = _get_file_input(project)
        else:
            UI.message(f"Using file {file}")

    file_manager = FileManager(project)
    if file:
        file_manager.add(file)

    system = System(
        workspace=workspace,
        logs=logs,
        memory=ChatMemory(),
        file_manager=file_manager,
    )

    return system
