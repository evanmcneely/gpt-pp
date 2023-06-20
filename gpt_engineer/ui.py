import typer


class UI:
    def error(message: str):
        typer.secho(message, fg=typer.colors.RED)

    def prompt(message: str) -> str:
        return typer.prompt(message)

    def success(message: str):
        prefix = typer.style("✔ ", fg=typer.colors.GREEN, bold=True)
        typer.echo(prefix + message)

    def fail(message: str):
        prefix = typer.style("✘ ", fg=typer.colors.RED, bold=True)
        typer.echo(prefix + message)

    def message(message: str):
        typer.echo(message)
