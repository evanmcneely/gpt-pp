from pathlib import Path
from typing import List, Optional

from ..ai import AI
from ..file_manager import FileManager
from ..system import System
from ..ui import UI

from ..file_utils import (  # isort:skip
    ValidationError,
    is_directory_empty,
    resolve_path,
    sanitize_input,
    validate_directory_path,
    validate_file_path,
)


def _check_if_project_is_valid(project: Path) -> bool:
    try:
        validate_directory_path(project)
        return True
    except ValidationError or FileNotFoundError:
        return False


def _get_project_from_input() -> Path:
    """Prompt the user to enter a path to a project directory. Validate
    the project path and repeat until a valid path is entered.
    """
    while True:
        project = UI.prompt(
            "Enter the relative path to the project directory you would like to work in"
        )
        project = sanitize_input(project)
        project = Path(project)

        try:
            abs_path = project.absolute()
            validate_directory_path(abs_path)
            break

        except ValidationError:
            UI.error(f"Invalid path: {project}")
        except FileNotFoundError:
            UI.error(f"Directory not found: {project}")

    return project


def _get_file_from_input(project: str) -> str:
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


def initialize(project_path: Path) -> System:
    """Initialize the System class that the application is
    dependent on and return it.
    """
    project_path_string = str(project_path)
    project_valid = _check_if_project_is_valid(project_path)

    if not project_valid:
        UI.message(f"{project_path_string} not valid")
        project_path = _get_project_from_input()

    directory_empty = is_directory_empty(project_path)

    if not directory_empty:
        file = _get_file_from_input(project_path_string)

    project = FileManager(str(project_path))
    project.add(file)  # type:ignore

    system = System(
        project=project,
        ai=AI(),
    )

    return system
