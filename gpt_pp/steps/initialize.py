from pathlib import Path
from typing import Optional

from ..ai import AI
from ..file_manager import FileManager
from ..system import System
from ..ui import UI

from ..file_utils import (  # isort:skip
    is_directory_empty,
    resolve_path,
    sanitize_input,
    validate_directory_path,
    validate_file_path,
)


def _get_project_from_input() -> Path:
    """Prompt the user to enter a path to a project directory. Validate
    the project path and repeat until a valid path is entered.
    """
    while True:
        project = UI.prompt(
            "Enter the relative path to the project directory you would like to work in"
        )
        project = Path(sanitize_input(project))
        abs_path = resolve_path(project)

        valid = validate_directory_path(abs_path, warn=True)
        if valid:
            break

    return project


def _get_file_from_input(project: Path) -> Path:
    """Prompt the user to enter a path to a file within the project directory.
    Validate the file path and repeat until a valid path is entered.
    """
    while True:
        file = UI.prompt(
            "Enter the relative path to the file you would like to work in"
        )
        file = Path(sanitize_input(file))
        path = resolve_path(project, file)

        valid = validate_file_path(path, warn=True)
        if valid:
            break

    return file


def _finalize_project_path(project: Path) -> Path:
    abs_path = resolve_path(project)
    project_valid = validate_directory_path(abs_path, warn=True)
    if not project_valid:
        project = _get_project_from_input()

    return project


def _finalize_file_path(project: Path, file: Optional[Path]) -> Optional[Path]:
    directory_empty = is_directory_empty(project)

    if not directory_empty:
        if file:
            abs_path = resolve_path(project, file)
            success = validate_file_path(abs_path, warn=True)
            if not success:
                file = _get_file_from_input(project)
        else:
            file = _get_file_from_input(project)

    return file


def initialize(project_path: Path, file_path: Optional[Path]) -> System:
    """Initialize the System class that the application is
    dependent on and return it.
    """
    project_path = _finalize_project_path(project_path)
    project = FileManager(project_path)

    file_path = _finalize_file_path(project_path, file_path)
    if file_path:
        project.add(file_path)

    system = System(
        project=project,
        ai=AI(),
    )

    return system
