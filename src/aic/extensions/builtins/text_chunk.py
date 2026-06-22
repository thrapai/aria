from typing import Any

from aic.core.context import AICContext
from aic.core.errors import ExtensionExecutionError


class TextChunk:
    name = "text.chunk"

    def run(self, input: dict[str, Any], context: AICContext) -> dict[str, Any]:
        text = input["text"]
        size = int(input.get("size", 4000))
        overlap = int(input.get("overlap", 0))
        if size <= 0:
            raise ExtensionExecutionError("size must be greater than 0")
        if overlap >= size:
            raise ExtensionExecutionError("overlap must be smaller than size")
        chunks = []
        step = size - overlap
        for start in range(0, len(text), step):
            chunks.append(text[start : start + size])
        return {"chunks": chunks}
