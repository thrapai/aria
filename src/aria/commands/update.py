from typing import Literal

import typer
from rich.console import Console

console = Console()

PACKAGE_NAME = "thrapai-aria"
UPDATE_COMMANDS: dict[str, str] = {
    "pipx": f"pipx upgrade {PACKAGE_NAME}",
    "pip": f"python -m pip install -U {PACKAGE_NAME}",
    "uv": f"uv tool upgrade {PACKAGE_NAME}",
}


def update(
    method: Literal["pipx", "pip", "uv"] | None = typer.Option(None, "--method", "-m", help="Upgrade method"),
) -> None:
    if method is None:
        console.print("Choose an upgrade method:")
        for name, command in UPDATE_COMMANDS.items():
            console.print(f"{name}: {command}")
        return
    console.print(UPDATE_COMMANDS[method])
