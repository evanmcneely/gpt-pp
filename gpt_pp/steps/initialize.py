from typing import Optional, Tuple

from ..chat_memory import ChatMemory
from ..file_manager import FileManager
from ..file_utils import (ValidationError, is_directory_empty, resolve_path,
                          sanitize_input, validate_directory_path,
                          validate_file_path)
from ..system import DB, System
from ..ui import UI


def _get_project_from_workspace(workspace: DB) -> Optional[str]:
    """Get the project path from the workspace directory, validate the 
    path and return it. Return none if an error occurs while retrieving the
    file or validating the path.
    """
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
        UI.error(f"Directory not found: {project}")
        project = None

    return project


def _get_file_from_workspace(workspace: DB, project: str) -> Optional[str]:
    """Get the file path from the workspace directory, validate the
    path and return it. Return none if an error occurs while retrieving the
    file or validating the path.
    """
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
        UI.error(f"File not found: {file}")
        file = None

    return file


def _get_project_input() -> str:
    """Prompt the user to enter a path to a project directory. Validate
    the project path and repeat until a valid path is entered.
    """
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
    """Prompt the user to enter a path to a file within the project directory. 
    Validate the file path and repeat until a valid path is entered.
    """
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
    """Initialize the System class that the application is 
    dependent on and return it.
    """
    workspace = DB(resolve_path("workspace"))
    logs = DB(resolve_path("logs"))

    project = _get_project_from_workspace(workspace)
    if not project or ignore_existing:
        project = _get_project_input()
    else:
        UI.message(f"Using project {project}")

    empty_directory: bool = is_directory_empty(resolve_path(project))

    file = None
    if not empty_directory:
        file = _get_file_from_workspace(workspace, project)
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
