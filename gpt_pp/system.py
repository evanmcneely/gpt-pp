from dataclasses import dataclass

from gpt_pp.ai import AI
from gpt_pp.file_manager import FileManager


# dataclass for all dbs:
@dataclass
class System:
    project: FileManager
    ai: AI
