<h1 align="center">ARIA</h1>

<p align="center">
  Automation Runtime for Intelligent Actions.
</p>

<p align="center">
  <img src="docs/logo.png" alt="ARIA logo" width="160">
</p>

<p align="center">
  <a href="https://github.com/thrapai/aria/actions/workflows/ci.yml"><img alt="Tests" src="https://github.com/thrapai/aria/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://codecov.io/gh/thrapai/aria"><img alt="Coverage" src="https://codecov.io/gh/thrapai/aria/branch/main/graph/badge.svg"></a>
  <a href="https://pypi.org/project/thrapai-aria/"><img alt="PyPI" src="https://img.shields.io/pypi/v/thrapai-aria.svg"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
</p>

Build AI-powered workflows with ARIA.

Your workflows are source-controlled, CI-friendly, and live in YAML files. Define them, run them locally, and inspect every result from saved run artifacts.

## Why ARIA?

- Source-controlled workflows: prompts, steps, inputs, and providers live in YAML.
- Full step transparency: see every intermediate result, not just the final answer.
- Extensible runtime: add your own extension when a built-in step is not enough.
- Provider flexibility: OpenAI and local Ollama today, with more providers to come.
- Small runtime: no hosted service, web UI, marketplace, or agent framework.

## Install

With the install script:

```bash
curl -fsSL https://raw.githubusercontent.com/thrapai/aria/master/install.sh | bash
```

With optional docling support:

```bash
curl -fsSL https://raw.githubusercontent.com/thrapai/aria/master/install.sh | ARIA_PACKAGE='thrapai-aria[docling]' bash
```

With `pipx`:

```bash
pipx install thrapai-aria
```

For docling support:

```bash
pipx install "thrapai-aria[docling]"
```

## Quickstart

Create a workflow:

```bash
aria init
```

Run it:

```bash
ollama pull gemma3:4b
aria run workflow.yml --input path=notes.txt
```

ARIA prints final outputs as JSON and writes run artifacts under `.aria/runs/<timestamp>/`.

## Workflow

```yaml
version: "1"
name: summarize_file

providers:
  ollama:
    type: ollama
    base_url: http://localhost:11434

inputs:
  path:
    type: file
    required: true

steps:
  - id: read
    uses: file.read
    with:
      path: "{{ inputs.path }}"

  - id: summarize
    uses: ai.generate
    with:
      model: ollama:gemma3:4b
      prompt: |
        Summarize this file in five concise bullet points:

        {{ steps.read.output.content }}

  - id: save
    uses: file.write
    with:
      path: summary.txt
      content: "{{ steps.summarize.output.text }}"

outputs:
  summary: "{{ steps.summarize.output.text }}"
  summary_file: "{{ steps.save.output.path }}"
```

Templates can read workflow inputs and previous step outputs:

```jinja2
{{ inputs.path }}
{{ steps.read.output.content }}
```

## Built-In Extensions

- `ai.generate`
- `file.read`
- `file.write`
- `utils.json.parse`
- `utils.text.chunk`
- `docling.convert` - _optional_

Extension examples live in `docs/extensions/`.

## Providers

ARIA currently supports `openai` and `ollama` provider types. A provider entry is an
alias that can be used in `ai.generate` model strings as `provider:model`.

### OpenAI

```bash
export OPENAI_API_KEY="..."
```

```yaml
providers:
  openai:
    type: openai
    api_key_env: OPENAI_API_KEY
    # Optional:
    # api_key_file: .openai-key
    # base_url: https://api.openai.com/v1
```

If no `providers.openai` entry is configured, `openai:<model>` still works and
reads `OPENAI_API_KEY` from the environment.

### Ollama

```bash
ollama pull gemma3:4b
```

```yaml
providers:
  ollama:
    type: ollama
    base_url: http://localhost:11434
```

If no `providers.ollama` entry is configured, `ollama:<model>` still works and
uses `http://localhost:11434`.

Provider names may be custom aliases when the entry declares a supported `type`:

```yaml
providers:
  local:
    type: ollama
    base_url: http://localhost:11434

steps:
  - id: summarize
    uses: ai.generate
    with:
      model: local:gemma3:4b
      prompt: "Summarize: {{ inputs.text }}"
```

Use providers as `provider:model`, for example `openai:gpt-4.1-mini`,
`ollama:gemma3:4b`, or `local:gemma3:4b`.

## Development

```bash
uv sync --extra dev
uv run --extra dev python -m pytest
uv run --extra dev ruff check
uv run --extra dev ruff format --check
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution and release notes.

## License

MIT
