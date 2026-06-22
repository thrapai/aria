from pathlib import Path
from typing import Any

from aic.core.context import AICContext
from aic.core.errors import ExtensionExecutionError


class FileRead:
    name = "file.read"

    def run(self, input: dict[str, Any], context: AICContext) -> dict[str, Any]:
        path = Path(input["path"])
        if not path.exists():
            raise ExtensionExecutionError(f"File not found: {path}")
        return {"content": path.read_text(encoding="utf-8")}
