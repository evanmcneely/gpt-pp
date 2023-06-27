from ..ai import get_imported_file_paths
from ..file_utils import sanitize_input
from ..system import System
from ..ui import UI


def retrieve_files(system: System):
    file_content = system.file_manager.get_all_file_content()
    if not file_content:
        return None

    file_paths = get_imported_file_paths(system, file_content)
    if not file_paths:
        return None

    UI.message("Adding files to context")
    for path in file_paths:
        try:
            path = sanitize_input(path)
            system.file_manager.add(path)
            UI.success(path)
        except ValueError as e:
            UI.fail(f"{path} - {str(e)}")
            pass
