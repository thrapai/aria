# ai

AI generation extensions.

## ai.generate

Input:

```yaml
model: ollama:gemma3:4b
prompt: "Summarize: {{ inputs.text }}"
```

`model` must use `provider:model` format. The provider can be a built-in
provider name, such as `openai` or `ollama`, or a custom alias from the
workflow's `providers` block.

Supported provider types:

- `openai` - reads `OPENAI_API_KEY` by default, or `api_key_env` /
  `api_key_file` from the provider config. `base_url` is optional.
- `ollama` - uses `http://localhost:11434` by default. `base_url` is optional.

Output:

```json
{
  "text": "...",
  "model": "ollama:gemma3:4b"
}
```

Example:

```yaml
steps:
  - id: summarize
    uses: ai.generate
    with:
      model: ollama:gemma3:4b
      prompt: "Summarize: {{ inputs.text }}"
```
