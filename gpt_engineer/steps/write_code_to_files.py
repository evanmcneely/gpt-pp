from ..chains import write_code
from ..system import System


def write_code_to_files(system: System):
    files = write_code(system.memory.load_messages())
    print(files)

    for file in files:
        system.file_manager.add(file)

    return files
