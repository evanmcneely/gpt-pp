import os
from typing import Optional

from ..system import System, DB
from ..FileManager import FileManager
from ..ui import UI
from ..utils import (
    resolve_path,
    validate_file_path,
    validate_directory_path,
    create_directory,
)


def _resolve_path(path: str) -> str:
    return os.path.join(os.getcwd(), path)


# def _validate_directory(path: str) -> bool:
#     resolved_path = _resolve_path(path)
#     if os.path.isfile(resolved_path):
#         raise ValueError(f"{path} is a file, not a directory")
#     if not os.path.isdir(resolved_path):
#         os.makedirs(resolved_path)
#         return False
#     return True


# def _validate_file_path(paths: list[str]):
#     if not paths:
#         raise ValueError("No file paths provided")
#     for path in paths:
#         resolved_path = _resolve_path(path)
#         if os.path.isdir(resolved_path):
#             raise ValueError(f"{path} is a directory, not a file")
#         _, extension = os.path.splitext(path)
#         if extension.lower() in [".jpg", ".jpeg", ".png", ".svg"]:
#             continue
#         if not os.path.isfile(resolved_path):
#             raise ValueError(f"{path} does not exist or is not a file")


def _sanitize_input(input: str) -> str:
    return input.strip()


def _get_project_from_workspace(system: System) -> Optional[str]:
    project = None
    try:
        project = system.workspace["project"]
    except KeyError:
        pass
    return _sanitize_input(project)


def _get_file_from_workspace(system: System) -> Optional[str]:
    file = None
    try:
        file = system.workspace["file"]
    except KeyError:
        pass
    return _sanitize_input(file)


def _get_project_input() -> str:
    while True:
        project = UI.prompt(
            "Enter the relative path to the project directory you would like to work in\n"
        )
        project = _sanitize_input(project)
        try:
            validate_directory_path(project)
            break
        except ValueError as e:
            UI.error(e.message)

    return project


def _get_file_input() -> str:
    while True:
        file = UI.prompt(
            "Enter the relative path to the file you would like to work in\n"
        )
        file = _sanitize_input(file)
        try:
            validate_file_path(file)
            break
        except ValueError as e:
            UI.error(e.message)

    return file


def initialize(ignore_existing: bool, run_prefix: str):
    system = System(
        logs=DB(_resolve_path(run_prefix + "logs")),
        preferences=DB(_resolve_path("preferences")),
        workspace=DB(_resolve_path("workspace")),
    )

    project: str = _get_project_from_workspace(system)
    file: str = _get_file_from_workspace(system)

    if not project or ignore_existing:
        project = _get_project_input()

    if not file or ignore_existing:
        file = _get_file_input()

    file_manager = FileManager.from_seed_file(project, file)

    return system, file_manager
