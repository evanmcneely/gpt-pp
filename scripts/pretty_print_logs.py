import typer
from rich.console import Console

from gpt_pp.file_utils import resolve_path
from gpt_pp.system import DB

console = Console()


app = typer.Typer()


@app.command()
def log(message):
    try:
        logs = DB(resolve_path("logs"))
        data = logs[message]
        console.log(data)
    except FileNotFoundError:
        typer.echo(f"File not found: {message}")


if __name__ == "__main__":
    app()
