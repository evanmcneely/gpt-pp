import os

from ..system import System, DB
from ..FileManager import FileManager


def _resolve_path(path: str) -> str:
    return os.path.join(os.getcwd(), path)


def _validate_directory(path: str) -> bool:
    resolved_path = _resolve_path(path)
    if os.path.isfile(resolved_path):
        raise ValueError(f"{path} is a file, not a directory")
    if not os.path.isdir(resolved_path):
        os.makedirs(resolved_path)
        return False
    return True


def _validate_file_path(paths: list[str]):
    if not paths:
        raise ValueError("No file paths provided")
    for path in paths:
        resolved_path = _resolve_path(path)
        if os.path.isdir(resolved_path):
            raise ValueError(f"{path} is a directory, not a file")
        _, extension = os.path.splitext(path)
        if extension.lower() in [".jpg", ".jpeg", ".png", ".svg"]:
            continue
        if not os.path.isfile(resolved_path):
            raise ValueError(f"{path} does not exist or is not a file")


def _sanitize_line(input: str) -> str:
    return input.strip()


def _sanitize_input(input: str) -> list[str]:
    return [_sanitize_line(x) for x in input.split(" ")]


def _get_project_from_workspace(system: System) -> str:
    return system.workspace["project"]


def _get_file_paths_from_workspace(system: System) -> list[str]:
    return system.workspace["files"]


def _add_files_to_project(file_manager: FileManager, files: list[str]):
    for file in files:
        file_manager.add_file(file, seed=True)


def _get_project_input() -> str:
    project = input(
        "Enter the relative path to the project directory you would like to work in\n"
    )
    return _sanitize_line(project)


def _get_file_paths_input() -> list[str]:
    file_paths = input(
        "Enter the paths to the files in project you would like to work with (new line for each file path)\n"
    )
    return _sanitize_input(file_paths)


def initialize(ignore_existing: bool, run_prefix: str):
    system = System(
        logs=DB(_resolve_path(run_prefix + "logs")),
        preferences=DB(_resolve_path("preferences")),
        workspace=DB(_resolve_path("workspace")),
    )

    project: str = _get_project_input()
    files: list[str] = _get_file_paths_input()

    # TODO:
    # input validation
    # get projects/files from workspace

    file_manager = FileManager(project)
    _add_files_to_project(file_manager, files)

    return system, file_manager
