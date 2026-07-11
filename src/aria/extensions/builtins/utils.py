import json
from typing import Any

from aria.core.context import ARIAContext
from aria.core.errors import ExtensionExecutionError


class JsonParse:
    name = "utils.json.parse"

    def run(self, input: dict[str, Any], context: ARIAContext) -> dict[str, Any]:
        try:
            return {"value": json.loads(input["text"])}
        except json.JSONDecodeError as exc:
            raise ExtensionExecutionError(f"Invalid JSON: {exc}") from exc


class TextChunk:
    name = "utils.text.chunk"

    def run(self, input: dict[str, Any], context: ARIAContext) -> dict[str, Any]:
        text = input["text"]
        delimiter = input.get("delimiter")
        raw_size = input.get("size")
        if delimiter is not None:
            chunks = _split_on_delimiter(text, str(delimiter))
            if raw_size is None:
                return {"chunks": chunks}
            size = _size(raw_size)
            return {"chunks": _pack_chunks(chunks, size)}

        size = _size(raw_size or 4000)
        overlap = int(input.get("overlap", 0))
        if overlap >= size:
            raise ExtensionExecutionError("overlap must be smaller than size")
        chunks = []
        step = size - overlap
        for start in range(0, len(text), step):
            chunks.append(text[start : start + size])
        return {"chunks": chunks}


def _size(value: Any) -> int:
    size = int(value)
    if size <= 0:
        raise ExtensionExecutionError("size must be greater than 0")
    return size


def _split_on_delimiter(text: str, delimiter: str) -> list[str]:
    if delimiter == "":
        raise ExtensionExecutionError("delimiter must not be empty")
    parts = text.split(delimiter)
    return [part if index == 0 else delimiter + part for index, part in enumerate(parts) if part]


def _pack_chunks(chunks: list[str], size: int) -> list[str]:
    packed = []
    current = ""
    for chunk in chunks:
        if len(chunk) > size:
            if current:
                packed.append(current)
                current = ""
            packed.extend(chunk[start : start + size] for start in range(0, len(chunk), size))
        elif not current:
            current = chunk
        elif len(current) + len(chunk) <= size:
            current += chunk
        else:
            packed.append(current)
            current = chunk
    if current:
        packed.append(current)
    return packed
