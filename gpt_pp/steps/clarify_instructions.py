from ..system import System
from ..ui import UI


def _is_end_sequence(sequence: str) -> bool:
    """Return True if the sequence is "nothing left to clarify."""
    return sequence.strip(' ."\n').lower() == "nothing left to clarify"


def _handle_ai_question(system: System) -> str:
    """Generate a response from an AI model and return the response."""
    chat_history = system.memory.load_messages_as_string()
    question: str = system.ai.generate_clarifying_question(chat_history=chat_history)
    system.memory.add_ai_message(question)
    return question


def _handle_user_response(system: System, ai: str) -> str:
    """Prompt the user to respond to the AI model and return the response."""
    user: str = UI.prompt(ai)
    system.memory.add_user_message(user)
    return user


def clarify_instructions(system: System):
    """Ask an AI model if they want to clarify anything about the instructions
    they are to perform. Prompt the user for clarification until the end
    sequence 'nothing left to clarify' is found.
    """
    ai = _handle_ai_question(system)

    while not _is_end_sequence(ai):
        _handle_user_response(system, ai)
        ai = _handle_ai_question(system)
