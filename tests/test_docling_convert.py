import sys
import types

import pytest

from aic.core.errors import ExtensionExecutionError
from aic.extensions.builtins.docling import DoclingConvert


def _stub_docling(monkeypatch):
    class FakeDocument:
        def export_to_markdown(self):
            return "# Title"

        def export_to_dict(self):
            return {"title": "Title"}

    class FakeConverter:
        def convert(self, path):
            return types.SimpleNamespace(document=FakeDocument())

    converter_module = types.ModuleType("docling.document_converter")
    converter_module.DocumentConverter = FakeConverter

    monkeypatch.setitem(sys.modules, "docling", types.ModuleType("docling"))
    monkeypatch.setitem(sys.modules, "docling.document_converter", converter_module)


def test_docling_convert_returns_markdown_or_json(monkeypatch):
    _stub_docling(monkeypatch)

    assert DoclingConvert().run({"path": "report.pdf"}, None) == {
        "format": "markdown",
        "content": "# Title",
        "text": "# Title",
    }
    assert DoclingConvert().run({"path": "report.pdf", "format": "json"}, None) == {
        "format": "json",
        "content": {"title": "Title"},
    }


def test_docling_convert_rejects_unknown_format(monkeypatch):
    _stub_docling(monkeypatch)

    with pytest.raises(ExtensionExecutionError, match="Unsupported docling.convert format: html"):
        DoclingConvert().run({"path": "report.pdf", "format": "html"}, None)
