from typing import Optional, Tuple

from ..system import System, DB
from ..FileManager import FileManager
from ..ChatMemory import ChatMemory
from ..ui import UI
from ..utils import (
    resolve_path,
    validate_file_path,
    validate_directory_path,
    sanitize_input,
)


def _get_project_from_workspace(workspace: DB) -> Optional[Tuple[str, bool]]:
    project = None
    created = False

    try:
        project = workspace["project"]
        project = sanitize_input(project)
        if not project:
            return (None, None)
        path = resolve_path(project)
        created = validate_directory_path(path)
    except ValueError as e:
        UI.error(e)
    except Exception:
        pass
    # TODO: specific error messaging

    return project, created


def _get_file_from_workspace(workspace: DB, project: str) -> Optional[str]:
    file = None
    try:
        file = workspace["file"]
        file = sanitize_input(file)
        if not file:
            return None
        path = resolve_path(project, file)
        validate_file_path(path)
    except ValueError as e:
        UI.error(e)
    except Exception:
        pass
    # TODO: specific error messaging

    return file


def _get_project_input() -> str:
    created = False
    while True:
        project = UI.prompt(
            "Enter the relative path to the project directory you would like to work in"
        )
        project = sanitize_input(project)
        try:
            path = resolve_path(project)
            created = validate_directory_path(path)
            break
        except ValueError as e:
            UI.error(e)
            pass

    return project, created


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
        except ValueError as e:
            UI.error(e)

    return file


def initialize(ignore_existing: bool):
    workspace = DB(resolve_path("workspace"))
    logs = DB(resolve_path("logs"))

    project, created = _get_project_from_workspace(workspace)
    if not project or ignore_existing:
        project, created = _get_project_input()
    else:
        UI.message(f"Using project {project}")

    file = None
    if not created:
        file: str = _get_file_from_workspace(workspace, project)
        if not file or ignore_existing:
            file = _get_file_input(project)
        else:
            UI.message(f"Using file {file}")

    file_manager = FileManager(project)
    if file:
        file_manager.add(file, seed=True)

    system = System(
        workspace=workspace,
        logs=logs,
        memory=ChatMemory(),
        file_manager=file_manager,
    )

    return system
