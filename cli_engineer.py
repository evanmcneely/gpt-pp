from typing import List, Callable
import typer

from gpt_engineer.system import System
from gpt_engineer.ui import UI
from gpt_engineer.steps import (
    initialize,
    retrieve_files,
    clarify_instructions,
    write_code_to_files,
    build_initial_prompt,
)


app = typer.Typer()


STEPS = [
    retrieve_files,
    build_initial_prompt,
    clarify_instructions,
    write_code_to_files,
]


def _run_steps(system: System, steps: List[Callable]):
    for step in steps:
        step(system)


@app.command()
def setup(
    ignore_existing: bool = typer.Option(
        False,
        "-i",
        help="ignore existing project/file paths and prompts in the workspace directory if they exist",
    ),
):
    try:
        system: System = initialize(ignore_existing)

        while True:
            _run_steps(system, STEPS)
            # TODO: summarize memory

    except Exception as e:
        UI.error(e)


if __name__ == "__main__":
    app()
