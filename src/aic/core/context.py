from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aic.types.workflow import ProviderSpec


@dataclass
class AICContext:
    inputs: dict[str, Any]
    run_dir: Path
    providers: dict[str, ProviderSpec] = field(default_factory=dict)
    steps: dict[str, dict[str, Any]] = field(default_factory=dict)

    def template_data(self) -> dict[str, Any]:
        return {"inputs": self.inputs, "steps": self.steps}
