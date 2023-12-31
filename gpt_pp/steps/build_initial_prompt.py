from ..system import System
from ..ui import UI


def _format_initial_prompt(prompt: str, file_content: str) -> str:
    """Format the instructions and file content into a prompt."""
    return f"""{prompt}

    {file_content}
    """


def _get_prompt_from_input() -> str:
    """Get the prompt instructions from the user and return it."""
    return UI.prompt("Enter the instruction prompt that you want to execute")


def build_initial_prompt(system: System):
    """Build the initial prompt from the workspace directory or user input."""
    prompt = _get_prompt_from_input()
    file_content = system.project.get_all_file_content()
    initial_prompt = _format_initial_prompt(prompt, file_content)
    system.ai.add_user_message(initial_prompt)
