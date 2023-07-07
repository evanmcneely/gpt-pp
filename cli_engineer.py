from pathlib import Path
from typing import List, Optional

import typer
from typing_extensions import Annotated

from gpt_pp.ui import UI

from gpt_pp.steps import (  # isort:skip
    build_initial_prompt,
    clarify_instructions,
    initialize,
    provide_feedback,
    retrieve_files,
    write_code_to_files,
)

app = typer.Typer()


@app.command()
def setup(
    project: Annotated[
        Path,
        typer.Argument(
            help="Path to the project directory to work with",
            exists=True,
            file_okay=False,
            dir_okay=True,
            writable=True,
            readable=True,
            resolve_path=False,
        ),
    ],
    # files: Annotated[
    #     Optional[List[Path]],
    #     typer.Argument(help="File paths from the project root directory"),
    # ] = None,
    imports: Annotated[
        bool,
        typer.Option(
            help="Load any relevant files into context",
        ),
    ] = True,
):
    try:
        system = initialize(str(project))

        if imports:
            retrieve_files(system)
        build_initial_prompt(system)

        while True:
            clarify_instructions(system)
            write_code_to_files(system)
            provide_feedback(system)

    except Exception as e:
        UI.error(str(e))


if __name__ == "__main__":
    app()
