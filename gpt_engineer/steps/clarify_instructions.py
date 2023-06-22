from ..system import System
from ..ui import UI
from ..chains import ask_for_clarification


def _is_end_sequence(sequence: str) -> bool:
    return sequence.strip(' ."\n').lower() == "nothing left to clarify"


def _handle_ai_message(system: System) -> str:
    ai: str = ask_for_clarification(system.memory.load_messages())
    system.memory.add_ai_message(ai)
    return ai


def _handle_user_message(system: System, ai: str) -> str:
    user: str = UI.prompt(ai)
    system.memory.add_user_message(user)
    return user


def clarify_instructions(system: System):
    """Ask the user if they want to clarify anything and save the results to the workspace"""

    ai = _handle_ai_message(system)

    while not _is_end_sequence(ai):
        _handle_user_message(system, ai)
        ai = _handle_ai_message(system)
