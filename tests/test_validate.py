import pytest
from pydantic import ValidationError

from aic.types.workflow import Workflow


def test_valid_workflow_passes_validation():
    workflow = Workflow.model_validate(
        {"version": "0.1", "name": "hello", "steps": [{"id": "one", "uses": "file.write"}]}
    )
    assert workflow.name == "hello"


def test_duplicate_step_ids_fail_validation():
    with pytest.raises(ValidationError, match="step IDs must be unique"):
        Workflow.model_validate(
            {
                "version": "0.1",
                "name": "bad",
                "steps": [{"id": "one", "uses": "file.write"}, {"id": "one", "uses": "file.read"}],
            }
        )


def test_provider_config_passes_validation():
    workflow = Workflow.model_validate(
        {
            "version": "0.1",
            "name": "ai",
            "providers": {
                "ollama": {"type": "ollama", "base_url": "http://localhost:11434"},
                "openai": {"type": "openai", "api_key_env": "OPENAI_API_KEY", "api_key_file": ".secret"},
            },
            "steps": [{"id": "ask", "uses": "ai.generate"}],
        }
    )
    assert workflow.providers["ollama"].type == "ollama"
