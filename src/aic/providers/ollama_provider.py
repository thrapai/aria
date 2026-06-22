import json
from typing import Any
from urllib import error, request

from aic.core.errors import ExtensionExecutionError
from aic.types.workflow import ProviderSpec


def generate(model: str, prompt: str, provider: ProviderSpec | None = None) -> str:
    base_url = (provider.base_url if provider and provider.base_url else "http://localhost:11434").rstrip("/")
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    try:
        req = request.Request(
            f"{base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=120) as response:
            data: dict[str, Any] = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace").strip()
        raise ExtensionExecutionError(f"Ollama request failed: {exc.code} {body or exc.reason}") from exc
    except Exception as exc:
        raise ExtensionExecutionError(f"Ollama request failed: {exc}") from exc
    return str(data.get("response", ""))
