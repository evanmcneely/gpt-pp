from ..system import System
from ..chains import get_imported_file_paths
from ..ui import UI


def _sanitize_input(input: str) -> str:
    return input.strip(" ")


def retrieve_files(system: System):
    file_content = system.file_manager.get_all_file_content()
    file_paths = get_imported_file_paths(file_content)

    UI.message("Adding files to context")
    for path in file_paths:
        try:
            path = _sanitize_input(path)
            system.file_manager.add(path)
            UI.success(path)
        except:
            UI.fail(path)
            pass
