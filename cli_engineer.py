import json
import typer

from gpt_pp.system import System
from gpt_pp.ui import UI
from gpt_pp.steps import (
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
        "--no-workspace",
        help="ignore existing project/file paths and prompts in the workspace directory if they exist",
    ),
    run_name: str = typer.Option(
        "default",
        "--log-prefix",
        help="name of the log file",
    ),
    ignore_imports: bool = typer.Option(
        False,
        "--no-imports",
        help="do not load any files from file imports into context",
    ),
):
    try:
        system: System = initialize(ignore_existing)

        if not ignore_imports:
            retrieve_files(system)
        build_initial_prompt(system, ignore_existing)

        while True:
            clarify_instructions(system)
            write_code_to_files(system)
            _save_to_logs(system, system.memory.load_messages(), run_name)
            provide_feedback(system)

    except Exception as e:
        UI.error(e)


if __name__ == "__main__":
    app()
