from typing import Iterable, Optional

import click
import typer
from click import Context

from . import __version__
from .platform.main import app as platform_app


class OrderedCommands(click.Group):
    def list_commands(self, ctx: Context) -> Iterable[str]:
        return self.commands.keys()


app = typer.Typer(cls=OrderedCommands)
app.add_typer(platform_app, name="platform")

state = {"verbose": False}


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def callback(
    verbose: bool = False,
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback
    ),
):
    """
    The datagrep CLI.
    """
    if verbose:
        state["verbose"] = True
