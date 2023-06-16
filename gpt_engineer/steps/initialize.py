import os
import pathlib

from .system import System, DB
from .FileManager import FileManager


def _validate_directory(path: str):
    if not os.path.exists(path):
        raise ValueError("Project path is required")


def _validate_file_path(path: list[str]):
    for p in path:
        if not os.path.exists(p):
            raise ValueError("File path is required")


def _sanitize_line(input: str) -> str:
    return input.strip()


def _sanitize_input(input: str) -> list[str]:
    return [_sanitize_line(x) for x in input.split("\n")]


def _get_project_from_workspace(system: System) -> str:
    return system.workspace["projects"]


def _get_file_paths_from_workspace(system: System) -> list[str]:
    return system.workspace["files"]


def _add_files_to_project(file_manager: FileManager, files: list[str]):
    for file in files:
        file_manager.add_file(file, seed=True)


def inititialize(ignore_existing: bool, run_prefix: str):
    system = System(
        logs=DB(pathlib.Path(__file__).parent / (run_prefix + "logs")),
        preferences=DB(pathlib.Path(__file__).parent / "preferences"),
        workspace=DB(pathlib.Path(__file__).parent / "workspace"),
    )

    project = _get_project_from_workspace(system)
    files = _get_file_paths_from_workspace(system)

    if len(project) == 0 or ignore_existing:
        project = print(
            "Enter the relative path to the project directory you would like to work in"
        )
        project = _sanitize_input(project)[0]

    if len(files) == 0 or ignore_existing:
        files = print(
            "Enter the paths to the files in project you would like to work with (new line for each file path)"
        )
        files = _sanitize_input(files)

    _validate_directory(project)
    _validate_file_path(files)

    file_manager = FileManager(project)
    _add_files_to_project(file_manager, files)

    return system, file_manager
