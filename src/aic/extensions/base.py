from typing import Any, Protocol

from aic.core.context import AICContext


class Extension(Protocol):
    name: str

    def run(self, input: dict[str, Any], context: AICContext) -> dict[str, Any]: ...
