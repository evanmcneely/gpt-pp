import json
from typing import Callable
import typer

from gpt_engineer.steps import initialize
from gpt_engineer.system import System


app = typer.Typer()


def _save_to_logs(system: System, step: Callable, messages: list):
    system.logs[step.__name__] = json.dumps(messages)


STEPS = []


@app.command()
def setup(
    ignore_existing: bool = typer.Option(
        False,
        "--i",
        help="ignore existing project and file paths",
    ),
    run_prefix: str = typer.Option(
        "",
        "--p",
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
        print(f"\033[31mError: {str(e)}\033[0m")


if __name__ == "__main__":
    app()
