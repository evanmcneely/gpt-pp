# import json
from typing import Any, Callable
import typer

from gpt_engineer.system import System
from gpt_engineer.ui import UI
from gpt_engineer.steps import (
    initialize,
    retrieve_files,
    clarify_instructions,
    write_code,
)


app = typer.Typer()


# def _save_to_logs(system: System, step: Callable, messages: list):
#     system.logs[step.__name__] = json.dumps(messages)


STEPS = [
    retrieve_files,
    clarify_instructions,
    # write_code
]


def _run_steps(system: System, steps: list[Callable]):
    result = None
    for step in steps:
        result = step(system, result)
        # TODO: save to logs
        system.memory.clear_step()


@app.command()
def setup(
    ignore_existing: bool = typer.Option(
        False,
        "-i",
        "--ignore",
        help="ignore existing project/file paths and prompts in the workspace directory if they exist",
    ),
    run_prefix: str = typer.Option(
        "",
        "-r",
        "--run-prefix",
        help="run prefix, if you want to run multiple variants of the same project and later compare them",
    ),
):
    try:
        system: System = initialize(ignore_existing, run_prefix)

        while True:
            _run_steps(system, STEPS)

            system.memory.clear_iteration()

    except Exception as e:
        UI.error(e.message)


if __name__ == "__main__":
    app()
