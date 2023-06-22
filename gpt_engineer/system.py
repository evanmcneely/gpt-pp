import os
from dataclasses import dataclass
from pathlib import Path

from .FileManager import FileManager
from .ChatMemory import ChatMemory


class DB:
    def __init__(self, path):
        self.path = Path(path).absolute()
        os.makedirs(self.path, exist_ok=True)

    def __getitem__(self, key):
        with open(self.path / key) as f:
            return f.read()

    def __setitem__(self, key, val):
        with open(self.path / key, "w") as f:
            f.write(val)


# dataclass for all dbs:
@dataclass
class System:
    workspace: DB
    memory: ChatMemory
    file_manager: FileManager
