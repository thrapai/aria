from pathlib import Path

import typer
from rich.console import Console

from aria.core.errors import ARIAError
from aria.core.parser import load_workflow

console = Console()


def validate(path: Path) -> None:
    try:
        workflow = load_workflow(path)
    except ARIAError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    console.print(f"[green]Workflow '{workflow.name}' is valid.[/green]")
