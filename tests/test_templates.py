import pytest

from aic.core.context import AICContext
from aic.core.errors import TemplateRenderError
from aic.core.templates import render_value


def test_template_renders_inputs(tmp_path):
    context = AICContext(inputs={"name": "Thomas"}, run_dir=tmp_path)
    assert render_value("Hello {{ inputs.name }}", context) == "Hello Thomas"


def test_template_renders_prior_step_output(tmp_path):
    context = AICContext(inputs={}, run_dir=tmp_path, steps={"read": {"output": {"content": "hi"}}})
    assert render_value("{{ steps.read.output.content }}", context) == "hi"


def test_missing_template_variable_raises_clear_error(tmp_path):
    context = AICContext(inputs={}, run_dir=tmp_path)
    with pytest.raises(TemplateRenderError, match="Template render failed"):
        render_value("{{ inputs.name }}", context)
