from aic.core.errors import ExtensionNotFoundError
from aic.extensions.base import Extension
from aic.extensions.builtins.ai import AIGenerate
from aic.extensions.builtins.docling import DoclingConvert
from aic.extensions.builtins.file import FileRead, FileWrite
from aic.extensions.builtins.utils import JsonParse, TextChunk


class Registry:
    def __init__(self) -> None:
        self._extensions: dict[str, Extension] = {}

    def register(self, extension: Extension) -> None:
        self._extensions[extension.name] = extension

    def get(self, name: str) -> Extension:
        try:
            return self._extensions[name]
        except KeyError as exc:
            raise ExtensionNotFoundError(f"Extension not found: {name}") from exc

    def has(self, name: str) -> bool:
        return name in self._extensions


def default_registry() -> Registry:
    registry = Registry()
    for extension in (FileRead(), FileWrite(), JsonParse(), TextChunk(), AIGenerate(), DoclingConvert()):
        registry.register(extension)
    return registry
