import json

import typer

from gpt_pp.steps import (build_initial_prompt, clarify_instructions,
                          initialize, provide_feedback, retrieve_files,
                          write_code_to_files)
from gpt_pp.system import System
from gpt_pp.ui import UI

app = typer.Typer()


@app.command()
def setup(
    ignore_existing: bool = typer.Option(
        False,
        "--no-workspace",
        help="ignore existing project/file paths and prompts in the workspace directory if they exist",
    ),
    run_name: str = typer.Option(
        "",
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
        system: System = initialize(ignore_existing, run_name)

        if not ignore_imports:
            retrieve_files(system)
        build_initial_prompt(system, ignore_existing)

        while True:
            clarify_instructions(system)
            write_code_to_files(system)
            system.save_to_logs("iteration", system.memory.load_messages_as_string())
            provide_feedback(system)

    except Exception as e:
        UI.error(e)


if __name__ == "__main__":
    app()
