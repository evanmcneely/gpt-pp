from dataclasses import dataclass
import os
from pathlib import Path


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
    logs: DB
    preferences: DB
