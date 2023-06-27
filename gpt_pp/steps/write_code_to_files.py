from ..ai import write_code
from ..file_utils import ValidationError, sanitize_input
from ..system import System
from ..ui import UI


def write_code_to_files(system: System):
    file_manager = system.file_manager
    current_paths = file_manager.files.keys()
    files = write_code(system)

    system.save_to_logs("parsed_file_diffs", files)

    UI.message("Writing code to file system")
    for file in files:
        try:
            path = sanitize_input(file[0])
            position = file[1]
            code = file[2]

            if path not in current_paths:
                file_manager.create(path, code)
            else:
                file_manager.update(path, code, position - 1)
            UI.success(path)

        except ValidationError as e:
            UI.fail(f"{path} - {str(e)}")
        except ValueError as e:
            UI.fail(f"{path} - {str(e)}")
        except Exception as e:
            UI.fail(f"{path} - {str(e)}")
