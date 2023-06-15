import json
import typer

from gpt_engineer.steps import STEPS
from gpt_engineer.db import DB
from config import init_app


app = typer.Typer()


def _save_logs(db: DB, step: function, messages: list):
    db[step.__name__] = json.dumps(messages)


@app.command()
def setup(
    project_path: str = typer.Argument(
        None, help="relative path to project directory from gpt-engineer"
    ),
    seed_file_path: str = typer.Option(
        None, "--f", help="path to the file from the root of the project directory"
    ),
    run_prefix: str = typer.Option(
        "",
        "--p",
        help="run prefix, if you want to run multiple variants of the same project and later compare them",
    ),
):
    dbs, file_manager = init_app(project_path, seed_file_path, run_prefix)

    while True:
        for step in STEPS:
            messages = step(file_manager, dbs)
            _save_logs(dbs.logs, step, messages)


if __name__ == "__main__":
    app()
