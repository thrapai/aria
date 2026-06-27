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

        format_ = input.get("format", "markdown")
        if format_ not in {"markdown", "json"}:
            raise ExtensionExecutionError(f"Unsupported docling.convert format: {format_}")
        try:
            result = DocumentConverter().convert(input["path"])
            if format_ == "markdown":
                content = result.document.export_to_markdown()
                return {"format": format_, "content": content, "text": content}
            return {"format": format_, "content": result.document.export_to_dict()}
        except ExtensionExecutionError:
            raise
        except Exception as exc:
            raise ExtensionExecutionError(f"Docling conversion failed: {exc}") from exc
