from typing import Any, Protocol

from aria.core.context import ARIAContext


class Extension(Protocol):
    name: str

    def run(self, input: dict[str, Any], context: ARIAContext) -> dict[str, Any]: ...
