from typing import Any

from jinja2 import StrictUndefined, TemplateError, Undefined
from jinja2.nativetypes import NativeEnvironment
from jinja2.sandbox import SandboxedEnvironment

from aic.core.context import AICContext
from aic.core.errors import TemplateRenderError

string_env = SandboxedEnvironment(undefined=StrictUndefined)
native_env = NativeEnvironment(undefined=StrictUndefined)


def render_value(value: Any, context: AICContext, native: bool = False) -> Any:
    try:
        if isinstance(value, str):
            rendered = (native_env if native else string_env).from_string(value).render(context.template_data())
            if isinstance(rendered, Undefined):
                raise TemplateRenderError(f"Template render failed: {rendered._undefined_message}")
            return rendered
        if isinstance(value, dict):
            return {key: render_value(val, context, native) for key, val in value.items()}
        if isinstance(value, list):
            return [render_value(item, context, native) for item in value]
        return value
    except TemplateError as exc:
        raise TemplateRenderError(f"Template render failed: {exc}") from exc
