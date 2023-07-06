from typing import Optional

from ..system import System
from ..ui import UI


def _format_initial_prompt(prompt: str, file_content: str) -> str:
    """Format the instructions and file content into a prompt."""
    return f"""{prompt}

    {file_content}
    """


def _get_prompt_from_workspace(system: System) -> Optional[str]:
    """Get the prompt instructions from the workspace directory and return it."""
    prompt = None
    try:
        prompt = system.workspace["prompt"]
        if not prompt.strip():
            return None
    except Exception:
        pass
        # TODO: specific error messaging

    return prompt


def _get_prompt_from_input() -> str:
    """Get the prompt instructions from the user and return it."""
    prompt = UI.prompt("Enter the instruction prompt that you want to execute")

    return prompt


def build_initial_prompt(system: System, ignore_workspace: bool):
    """Build the initial prompt from the workspace directory or user input."""
    prompt = _get_prompt_from_workspace(system)
    if not prompt or ignore_workspace:
        prompt = _get_prompt_from_input()

    file_content = system.project.get_all_file_content()

    initial_prompt = _format_initial_prompt(prompt, file_content)

    system.memory.add_user_message(initial_prompt)
