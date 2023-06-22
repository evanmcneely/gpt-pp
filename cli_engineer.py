import json
import typer

from gpt_engineer.system import System
from gpt_engineer.ui import UI
from gpt_engineer.steps import (
    initialize,
    retrieve_files,
    clarify_instructions,
    write_code_to_files,
    build_initial_prompt,
    provide_feedback,
)


app = typer.Typer()


def _save_to_logs(system: System, messages: str, run_name: str):
    system.logs[run_name] = json.dumps(messages)


@app.command()
def setup(
    ignore_existing: bool = typer.Option(
        False,
        "-i",
        help="ignore existing project/file paths and prompts in the workspace directory if they exist",
    ),
    run_name: str = typer.Option(
        "default",
        "-r",
        help="name of the log file",
    ),
):
    try:
        system: System = initialize(ignore_existing)

        retrieve_files(system)
        build_initial_prompt(system)

        while True:
            clarify_instructions(system)
            write_code_to_files(system)
            _save_to_logs(system, system.memory.load_messages(), run_name)
            provide_feedback(system)

    except Exception as e:
        UI.error(e)


if __name__ == "__main__":
    app()
