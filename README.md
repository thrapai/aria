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
  <a href="https://pypi.org/project/aria/"><img alt="PyPI" src="https://img.shields.io/pypi/v/aria.svg"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
</p>

Build AI-powered workflows with ARIA.

Your workflows are source-controlled, CI-friendly, and live in YAML files. Define them, run them locally, and inspect every result from saved run artifacts.

```bash
aria init
aria validate workflow.yml
aria run workflow.yml --input name=Thomas
```

## Why ARIA?

- Source-controlled workflows: prompts, steps, inputs, and providers live in YAML.
- Full step transparency: see every intermediate result, not just the final answer.
- Extensible runtime: add your own extension when a built-in step is not enough.
- Provider flexibility: OpenAI and local Ollama today, with more providers to come.
- Small runtime: no hosted service, web UI, marketplace, or agent framework.

## Install

With the install script:

```bash
curl -fsSL https://raw.githubusercontent.com/thrapai/aria/main/install.sh | bash
```

With `pipx`:

```bash
pipx install aria
```

With `pip`:

```bash
pip install aria
```

For docling support:

```bash
pipx install "aria[docling]"
```

## Quickstart

Create a workflow:

```bash
aria init
```

Run it:

```bash
aria run workflow.yml --input name=Thomas
```

ARIA prints final outputs as JSON and writes run artifacts under `.aria/runs/<timestamp>/`.

## Workflow

```yaml
version: "0.1"
name: hello

inputs:
  name:
    type: string
    required: true

steps:
  - id: write
    uses: file.write
    with:
      path: hello.txt
      content: "Hello {{ inputs.name }}"

outputs:
  file: "{{ steps.write.output.path }}"
```

Templates can read workflow inputs and previous step outputs:

```jinja2
{{ inputs.name }}
{{ steps.write.output.path }}
```

Steps can loop over a list with `for_each`; each `item` gets its own step run and the output becomes a list.

## Built-In Extensions

- `ai.generate`
- `file.read`
- `file.write`
- `utils.json.parse`
- `utils.text.chunk`
- `docling.convert` - _optional_

Extension examples live in `docs/extensions/`.

## Providers

### OpenAI

```bash
export OPENAI_API_KEY="..."
```

```yaml
providers:
  openai:
    type: openai
    api_key_env: OPENAI_API_KEY
```

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

Use providers as `provider:model`, for example `openai:gpt-4.1-mini` or `ollama:gemma3:4b`.

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
