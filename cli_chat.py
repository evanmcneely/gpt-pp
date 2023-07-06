import typer

from gpt_pp.steps import initialize, retrieve_files
from gpt_pp.ui import UI

app = typer.Typer()


@app.command()
def setup(
    ignore_workspace: bool = typer.Option(
        False,
        "--no-workspace",
        help="ignore existing project/file paths and prompts in the workspace directory if they exist",  # noqa
    ),
    ignore_imports: bool = typer.Option(
        False,
        "--no-imports",
        help="do not load any files from file imports into context",
    ),
):
    try:
        system = initialize(ignore_workspace)

        if not ignore_imports:
            retrieve_files(system)

        files = system.project.get_all_file_content()
        chat = system.ai.get_chat(files)

        while True:
            question = UI.prompt("Query")
            if question.strip().lower() == "exit":
                break

            chat.predict(input=question)

    except Exception as e:
        UI.error(str(e))


if __name__ == "__main__":
    app()
