from typing import Any

from ..system import System
from ..ui import UI
from ..chains import ask_for_clarification
from ..chains.ask_for_clarification import format_initial_prompt


def _get_prompt_from_workspace(system: System) -> str:
    prompt = None
    try:
        prompt = system.workspace["prompt"]
    except Exception:
        pass
    # TODO: specific error messaging

    return prompt


def _get_prompt_from_input() -> str:
    prompt = UI.prompt("Enter the instruction prompt that you want to execute")

    return prompt


def _build_initial_prompt(system: System) -> str:
    prompt: str = _get_prompt_from_workspace(system)
    if not prompt:
        prompt = _get_prompt_from_input()

    file_content: str = system.file_manager.get_all_file_content()

    return format_initial_prompt(prompt, file_content)


def _is_end_sequence(sequence: str) -> bool:
    return sequence.strip(' ."\n').lower() == "nothing left to clarify"


def clarify_instructions(system: System, previous_step: Any):
    """Ask the user if they want to clarify anything and save the results to the workspace"""
    user: str = _build_initial_prompt(system)
    ai: str = ask_for_clarification(system.memory.current_iteration, user)
    system.memory.save(user, ai)

    while not _is_end_sequence(ai):
        user: str = UI.prompt(ai)
        ai: str = ask_for_clarification(system.memory.get_iteration_memory(), user)
        system.memory.save(user, ai)

    return None
