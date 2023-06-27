import typer


class UI:
    @staticmethod
    def error(message: str):
        """Display an error message to the user  in red."""
        typer.secho(message, fg=typer.colors.RED)
    
    @staticmethod
    def prompt(message: str) -> str:
        """Prompt the user for input and return the input."""
        message = typer.style(message + ": ", fg=typer.colors.BLUE)
        return input(message)
    
    @staticmethod
    def success(message: str):
        """Display a success message to the user in green."""
        prefix = typer.style("   ", fg=typer.colors.GREEN, bold=True)
        typer.echo(prefix + message)

    @staticmethod
    def fail(message: str):
        """Display a failure message to the user in red."""
        prefix = typer.style("   ", fg=typer.colors.RED, bold=True)
        typer.echo(prefix + message)
    
    @staticmethod
    def message(message: str):
        """Display a message to the user."""
        typer.echo(message)
