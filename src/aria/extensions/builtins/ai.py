from typing import Any

from aria.core.context import ARIAContext
from aria.core.errors import ExtensionExecutionError
from aria.providers.ollama_provider import generate as generate_ollama
from aria.providers.openai_provider import generate as generate_openai


class AIGenerate:
    name = "ai.generate"

    def run(self, input: dict[str, Any], context: ARIAContext) -> dict[str, Any]:
        model = input["model"]
        provider_name, model_name = _split_model(model)
        provider = context.providers.get(provider_name)
        provider_type = provider.type if provider else provider_name
        if provider_type == "openai":
            text = generate_openai(model_name, input["prompt"], provider)
        elif provider_type == "ollama":
            text = generate_ollama(model_name, input["prompt"], provider)
        else:
            raise ExtensionExecutionError(f"Unsupported model provider: {provider_name}")
        return {"text": text, "model": model}


def _split_model(model: str) -> tuple[str, str]:
    if ":" not in model:
        raise ExtensionExecutionError(f"Model must use provider:model format: {model}")
    return model.split(":", 1)
