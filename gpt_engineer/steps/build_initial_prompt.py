from ..system import System
from ..ui import UI


def _format_initial_prompt(prompt: str, file_content: str) -> str:
    return f"""
    Instructions: {prompt}

    {file_content}
    """


def _get_prompt_from_workspace(system: System) -> str:
    prompt = None
    try:
        prompt = system.workspace["prompt"]
        print(prompt)
        if not prompt.strip():
            return None
    except Exception:
        pass
    # TODO: specific error messaging

    return prompt


def _get_prompt_from_input() -> str:
    prompt = UI.prompt("Enter the instruction prompt that you want to execute")

    return prompt


def build_initial_prompt(system: System):
    prompt: str = _get_prompt_from_workspace(system)
    if not prompt:
        prompt = _get_prompt_from_input()

    file_content: str = system.file_manager.get_all_file_content()

    initial_prompt = _format_initial_prompt(prompt, file_content)

    system.memory.add_user_message(initial_prompt)
