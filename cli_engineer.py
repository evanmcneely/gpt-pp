import typer

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
    ignore_workspace: bool = typer.Option(
        False,
        "--no-workspace",
        help="ignore existing project/file paths and prompts in the workspace directory if they exist",  # noqa
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
        system = initialize(ignore_workspace, run_name)

        if not ignore_imports:
            retrieve_files(system)
        build_initial_prompt(system, ignore_workspace)

        while True:
            clarify_instructions(system)
            write_code_to_files(system)
            provide_feedback(system)

    except Exception as e:
        UI.error(str(e))


if __name__ == "__main__":
    app()
