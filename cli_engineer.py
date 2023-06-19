import json
from typing import Callable
import typer

from gpt_engineer.steps import initialize
from gpt_engineer.system import System
from gpt_engineer.ui import UI


app = typer.Typer()


def _save_to_logs(system: System, step: Callable, messages: list):
    system.logs[step.__name__] = json.dumps(messages)


STEPS = []


@app.command()
def setup(
    ignore_existing: bool = typer.Option(
        False,
        "-i",
        "--ignore",
        help="ignore existing project and file paths in the workspace directory if they exist",
    ),
    run_prefix: str = typer.Option(
        "",
        "-r",
        "--run-prefix",
        help="run prefix, if you want to run multiple variants of the same project and later compare them",
    ),
):
    try:
        system, file_manager = initialize(ignore_existing, run_prefix)

        # while True:
        for step in STEPS:
            messages = step(file_manager, system)
            _save_to_logs(system, step, messages)

    except Exception as e:
        UI.error(e.message)


if __name__ == "__main__":
    app()
