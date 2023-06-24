from ..chains import write_code
from ..system import System
from ..ui import UI
from ..file_utils import sanitize_input, ValidationError


def write_code_to_files(system: System):
    file_manager = system.file_manager
    current_paths = file_manager.files.keys()
    files, explanation = write_code(system.memory.load_messages())

    UI.message("Writing code to file system")
    for file in files:
        try:
            path = sanitize_input(file[0])
            position = sanitize_input(file[1])
            code = file[2]
            print(path, position)
            print(code)

            if path not in current_paths:
                print("creating file")
                file_manager.create(path, code)

            else:
                print("updating file")
                file_manager.update(path, code, position - 1)

            UI.success(path)
        except ValidationError as e:
            UI.fail(f"{path} - {str(e)}")
        except ValueError as e:
            UI.fail(f"{path} - {str(e)}")
        except Exception as e:
            UI.fail(f"{path} - unknown reason")

    # UI.message(explanation)
