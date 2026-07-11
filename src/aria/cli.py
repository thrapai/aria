import typer

from aria.commands.init import init
from aria.commands.run import run
from aria.commands.validate import validate

app = typer.Typer(no_args_is_help=True)
app.command()(init)
app.command()(validate)
app.command()(run)


if __name__ == "__main__":
    app()
