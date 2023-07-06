from ..file_utils import ValidationError, sanitize_input
from ..system import System
from ..ui import UI


def retrieve_files(system: System):
    """Retrieve all the file paths imported into the content stored in the
    FileManager. Add the paths to the FileManager or return early if no files
    or paths exist.
    """
    files_loaded = system.project.num_files()
    if files_loaded == 0:
        return None

    seed_file = system.project.get_all_file_content()
    file_paths = system.ai.get_imported_file_paths(seed_file)
    if not file_paths:
        return None

    UI.message("Adding files to context")
    for path in file_paths:
        try:
            path = sanitize_input(path)
            system.project.add(path)
            UI.success(path)
        except ValidationError as e:
            UI.fail(f"{path} - {str(e)}")
        except FileNotFoundError as e:
            UI.fail(f"{path} - no such file exists")
