from langchain import PromptTemplate

from ..FileManager import FileManager
from ..system import System
from ..chains import get_imported_file_paths
from ..ui import UI


def retrieve_files(file_manager: FileManager, _: System):
    if not file_manager.seed_file_path:
        return None

    file_paths = get_imported_file_paths(file_manager.get_seed_file_content())

    for path in file_paths:
        try:
            file_manager.add(path)
            UI.success(path)
        except:
            UI.fail(path)

    return file_paths
