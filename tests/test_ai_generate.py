from aic.core.context import AICContext
from aic.extensions.builtins import ai
from aic.extensions.builtins.ai import AIGenerate
from aic.types.workflow import ProviderSpec


def test_ai_generate_routes_ollama(monkeypatch, tmp_path):
    monkeypatch.setattr(ai, "generate_ollama", lambda model, prompt, provider: f"{model}: {prompt}")
    context = AICContext(
        inputs={},
        run_dir=tmp_path,
        providers={"local": ProviderSpec(type="ollama", base_url="http://localhost:11434")},
    )

    output = AIGenerate().run({"model": "local:llama3.2", "prompt": "hello"}, context)

    assert output["text"] == "llama3.2: hello"
    assert output["model"] == "local:llama3.2"
