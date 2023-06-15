from ..utils import FileManager
from ..db import DBs


def clarify(dbs: DBs, file_manager: FileManager):
    """Ask the user if they want to clarify anything and save the results to the workspace"""
    # get input

    while True:
        messages = ai.next(messages, user)

        if messages[-1]["content"].strip().lower() == "no":
            break

        print()
        user = input('(answer in text, or "q" to move on)\n')
        print()

        if not user or user == "q":
            break

        user += (
            "\n\n"
            "Is anything else unclear? If yes, only answer in the form:\n"
            "{remaining unclear areas} remaining questions.\n"
            "{Next question}\n"
            'If everything is sufficiently clear, only answer "no".'
        )

    print()
    return messages
