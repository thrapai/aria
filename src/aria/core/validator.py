from pathlib import Path

from aria.core.parser import load_workflow
from aria.types.workflow import Workflow


def validate_workflow(path: Path) -> Workflow:
    return load_workflow(path)
