import os
from pathlib import Path

from aria.types.workflow import ProviderSpec

from aria.core.errors import ExtensionExecutionError


def generate(model: str, prompt: str, provider: ProviderSpec | None = None) -> str:
    api_key = _secret(provider) or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ExtensionExecutionError("OpenAI API key is required for ai.generate")
    try:
        from openai import OpenAI

        kwargs = {"api_key": api_key}
        if provider and provider.base_url:
            kwargs["base_url"] = provider.base_url
        response = OpenAI(**kwargs).responses.create(model=model, input=prompt)
        return response.output_text
    except Exception as exc:
        raise ExtensionExecutionError(f"OpenAI request failed: {exc}") from exc


def _secret(provider: ProviderSpec | None) -> str | None:
    if not provider:
        return None
    if provider.api_key_env and os.getenv(provider.api_key_env):
        return os.getenv(provider.api_key_env)
    if provider.api_key_file:
        try:
            return Path(provider.api_key_file).read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise ExtensionExecutionError(f"Could not read API key file: {exc}") from exc
    return None
