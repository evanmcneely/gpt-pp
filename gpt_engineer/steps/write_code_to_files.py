from ..chains import write_code
from ..system import System
from ..ui import UI


def write_code_to_files(system: System):
    files = write_code(system.memory.load_messages())

    UI.message("Writing code to file system")
    for file in files:
        try:
            path = file[0]
            code = file[1]
            system.file_manager.update(path, code, 0)
            UI.success(path)
        except:
            UI.fail(path)
            pass

    return files
