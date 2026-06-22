from pathlib import Path

import yaml
from pydantic import ValidationError

from aic.core.errors import WorkflowParseError, WorkflowValidationError
from aic.types.workflow import Workflow


def load_workflow(path: Path) -> Workflow:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise WorkflowParseError(f"Could not read workflow: {exc}") from exc
    except yaml.YAMLError as exc:
        raise WorkflowParseError(f"Invalid YAML: {exc}") from exc
    if not isinstance(raw, dict):
        raise WorkflowValidationError("Workflow must be a YAML object")
    try:
        return Workflow.model_validate(raw)
    except ValidationError as exc:
        raise WorkflowValidationError(str(exc)) from exc
