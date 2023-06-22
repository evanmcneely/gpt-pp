from typing import Any

from ..chains import follow_instructions
from ..system import System


def write_code(system: System, previous_step: Any):
    files = follow_instructions(system.memory.get_iteration_memory())
    print(files)

    return files
