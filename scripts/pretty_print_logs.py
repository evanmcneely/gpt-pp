import json
import typer

from gpt_pp.file_utils import resolve_path
from gpt_pp.system import DB


app = typer.Typer()


@app.command()
def log(message):
    try:
        logs = DB(resolve_path("logs"))
        data = logs[message]
        data = json.loads(data)
        for item in data:
            print('\n*** new message ***\n')
            print(item)
    except FileNotFoundError:
        typer.echo(f"File not found: {message}")


if __name__ == "__main__":
    app()
