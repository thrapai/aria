from rich.console import Console

from aria import __version__

console = Console()


def version() -> None:
    console.print(f"thrapai-aria {__version__}")
