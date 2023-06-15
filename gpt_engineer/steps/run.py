from ..FileManager import FileManager
from ..db import DBs


def run(dbs: DBs, file_manager: FileManager):
    """Run the AI on the main prompt and save the results"""
    messages = ai.start(setup_sys_prompt(dbs), dbs.input["main_prompt"])
    to_files(messages[-1]["content"], dbs.workspace)
    return messages
