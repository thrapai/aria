from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aria.types.workflow import ProviderSpec


@dataclass
class ARIAContext:
    inputs: dict[str, Any]
    run_dir: Path
    providers: dict[str, ProviderSpec] = field(default_factory=dict)
    steps: dict[str, dict[str, Any]] = field(default_factory=dict)
    item: Any = None

    def template_data(self) -> dict[str, Any]:
        data = {"inputs": self.inputs, "steps": self.steps}
        if self.item is not None:
            data["item"] = self.item
        return data
