from typing import Any

from aic.core.context import AICContext
from aic.core.errors import ExtensionExecutionError


class DoclingConvert:
    name = "docling.convert"

    def run(self, input: dict[str, Any], context: AICContext) -> dict[str, Any]:
        try:
            from docling.document_converter import DocumentConverter
        except ImportError as exc:
            raise ExtensionExecutionError("docling.convert requires the docling package") from exc

        try:
            result = DocumentConverter().convert(input["path"])
            text = result.document.export_to_markdown()
        except Exception as exc:
            raise ExtensionExecutionError(f"Docling conversion failed: {exc}") from exc
        return {"text": text}
