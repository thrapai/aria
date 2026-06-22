from pathlib import Path

import typer
from rich.console import Console

from aic.core.errors import AICError
from aic.core.parser import load_workflow

console = Console()


def validate(path: Path) -> None:
    try:
        workflow = load_workflow(path)
    except AICError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    console.print(f"[green]Workflow '{workflow.name}' is valid.[/green]")
