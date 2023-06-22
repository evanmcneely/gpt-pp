from typing import Any
from langchain import PromptTemplate

from ..system import System
from ..chains import get_imported_file_paths
from ..ui import UI


def retrieve_files(system: System, previous_step: Any):
    if not system.file_manager.seed_file_path:
        return None

    file_paths = get_imported_file_paths(system.file_manager.get_seed_file_content())

    for path in file_paths:
        try:
            system.file_manager.add(path)
            UI.success(path)
        except:
            # ignore failed files, they are usually library imports
            # UI.fail(path)
            pass

    return None
