import json
from pathlib import Path

import typer
from rich.console import Console

from aria.core.errors import ARIAError
from aria.core.parser import load_workflow
from aria.core.runner import run_workflow

console = Console()


def run(path: Path, input: list[str] = typer.Option(None, "--input", help="key=value")) -> None:
    try:
        workflow = load_workflow(path)
        outputs = run_workflow(workflow, path, _parse_inputs(input or []))
    except ARIAError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    console.print(json.dumps(outputs, indent=2))


def _parse_inputs(values: list[str]) -> dict[str, str]:
    inputs = {}
    for value in values:
        if "=" not in value:
            raise ARIAError(f"Invalid input '{value}', expected key=value")
        key, val = value.split("=", 1)
        inputs[key] = val
    return inputs
