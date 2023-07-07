from pathlib import Path
from typing import List, Optional

import typer
from typing_extensions import Annotated

from gpt_pp.steps import initialize, retrieve_files
from gpt_pp.ui import UI

app = typer.Typer()


def _is_exit(input: str):
    if input.lower().strip() == "exit":
        return True
    return False


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
    #     typer.Argument(
    #         help="File paths from the project root directory",
    #     ),
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

        file_content = system.project.get_all_file_content()
        chat = system.ai.get_chat(file_content)

        while True:
            question = UI.prompt("\n\nQuery")
            if _is_exit(question):
                break

            print()  # linebreak
            chat.predict(input=question)

    except Exception as e:
        UI.error(str(e))


if __name__ == "__main__":
    app()
