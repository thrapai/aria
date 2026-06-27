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


class FileWrite:
    name = "file.write"

    def run(self, input: dict[str, Any], context: AICContext) -> dict[str, Any]:
        path = Path(input["path"])
        content = str(input.get("content", ""))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return {"path": str(path), "bytes": len(content.encode("utf-8"))}
