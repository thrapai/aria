import json
from typing import Any

from aic.core.context import AICContext
from aic.core.errors import ExtensionExecutionError


class JsonParse:
    name = "json.parse"

    def run(self, input: dict[str, Any], context: AICContext) -> dict[str, Any]:
        try:
            return {"value": json.loads(input["text"])}
        except json.JSONDecodeError as exc:
            raise ExtensionExecutionError(f"Invalid JSON: {exc}") from exc
