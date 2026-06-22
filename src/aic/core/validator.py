from pathlib import Path

from aic.core.parser import load_workflow
from aic.types.workflow import Workflow


def validate_workflow(path: Path) -> Workflow:
    return load_workflow(path)
