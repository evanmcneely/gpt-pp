from ..ai import get_imported_file_paths
from ..file_utils import ValidationError, sanitize_input
from ..system import System
from ..ui import UI


def retrieve_files(system: System):
    """Retrieve all the file paths imported into the content stored in the
    FileManager. Add the paths to the FileManager or return early if no files
    or paths exist.
    """

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
        except ValidationError as e:
            UI.fail(f"{path} - {str(e)}")
            pass
