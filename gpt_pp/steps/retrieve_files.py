from pathlib import Path
from typing import List

from ..system import System
from ..ui import UI


def _get_imported_file_paths(system: System) -> List[str]:
    """Generate imported file paths and filter the paths already
    added from the list.
    """
    seed_file = system.project.get_all_file_content()
    file_paths = system.ai.get_imported_file_paths(seed_file)

    return list(filter(system.project.already_added, file_paths or []))


def retrieve_files(system: System):
    """Retrieve all the file paths imported into the content stored in the
    FileManager. Add the paths to the FileManager or return early if no files
    or paths exist.
    """
    if system.project.num_files() == 0:
        # no file content
        return None

    file_paths = _get_imported_file_paths(system)

    if len(file_paths) == 0:
        # no imported file paths
        return None

    UI.message("Adding files to context")
    for path in file_paths:
        path = Path(path)
        success = system.project.add(path)
        if success:
            UI.success(str(path))
        else:
            UI.fail(str(path))
