from ..dbs import DBs
from ..utils import FileManager


def run_clarified(dbs: DBs, file_manager: FileManager):
    # get the messages from previous step
    messages = json.loads(dbs.logs[clarify.__name__])

    messages = [
        ai.fsystem(setup_sys_prompt(dbs)),
    ] + messages[1:]
    messages = ai.next(messages, dbs.identity["use_qa"])
    to_files(messages[-1]["content"], dbs.workspace)
    return messages
