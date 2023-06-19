import os
from typing import Optional

from ..system import System, DB
from ..FileManager import FileManager
from ..ui import UI
from ..utils import resolve_path, validate_file_path, validate_directory_path


def _resolve_path(path: str) -> str:
    return os.path.join(os.getcwd(), path)


def _sanitize_input(input: str) -> str:
    return input.split("\n")[0].strip(" ")


def _get_project_from_workspace(system: System) -> Optional[str]:
    project = None
    created = False

    try:
        project = system.workspace["project"]
        path = resolve_path(project)
        created = validate_directory_path(path)
    except ValueError as e:
        UI.error(e)
    except Exception:
        pass
    # TODO: specific error messaging

    if not project:
        return None

    return _sanitize_input(project), created


def _get_file_from_workspace(system: System, project: str) -> Optional[str]:
    file = None
    try:
        file = system.workspace["file"]
        path = resolve_path(project, file)
        validate_file_path(path)
    except ValueError as e:
        UI.error(e)
    except Exception:
        pass
    # TODO: specific error messaging

    if not file:
        return None

    return _sanitize_input(file)


def _get_project_input() -> str:
    created = False
    while True:
        project = UI.prompt(
            "Enter the relative path to the project directory you would like to work in"
        )
        project = _sanitize_input(project)
        path = resolve_path(project)
        try:
            created = validate_directory_path(path)
            break
        except ValueError as e:
            UI.error(e)

    return project, created


def _get_file_input(project: str) -> str:
    while True:
        file = UI.prompt(
            "Enter the relative path to the file you would like to work in"
        )
        file = _sanitize_input(file)
        try:
            path = resolve_path(project, file)
            validate_file_path(path)
            break
        except ValueError as e:
            UI.error(e)

    return file


def initialize(ignore_existing: bool, run_prefix: str):
    system = System(
        logs=DB(_resolve_path(run_prefix + "logs")),
        preferences=DB(_resolve_path("preferences")),
        workspace=DB(_resolve_path("workspace")),
    )

    project, created = _get_project_from_workspace(system)
    if not project or ignore_existing:
        project, created = _get_project_input()

    file = None
    if not created:
        file: str = _get_file_from_workspace(system, project)
        if not file or ignore_existing:
            file = _get_file_input(project)

    print(project, created, file)

    file_manager = FileManager(project)
    if file:
        file_manager.add(file)

    return system, file_manager
