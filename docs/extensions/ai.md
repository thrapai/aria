# ai

AI generation extensions.

## ai.generate

Input:

```yaml
model: ollama:gemma3:4b
prompt: "Summarize: {{ inputs.text }}"
```

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
