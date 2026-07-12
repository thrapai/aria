from pathlib import Path

import typer
from rich.console import Console

console = Console()

EXAMPLE = """version: "0.1"

name: hello

inputs:
  name:
    type: string
    required: true

steps:
  - id: write
    uses: file.write
    with:
      path: hello.txt
      content: "Hello {{ inputs.name }}"

outputs:
  file: "{{ steps.write.output.path }}"
"""


def init(force: bool = typer.Option(False, "--force", help="Overwrite workflow.yml")) -> None:
    path = Path("workflow.yml")
    if path.exists() and not force:
        console.print("[red]workflow.yml already exists. Use --force to overwrite.[/red]")
        raise typer.Exit(1)
    path.write_text(EXAMPLE, encoding="utf-8")
    console.print("[green]Created workflow.yml[/green]")
