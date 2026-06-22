# AIC

AIC is a Python CLI runtime for AI workflows as code. Define a workflow in YAML, run it locally, and inspect the artifacts written for each run.

```bash
aic init
aic validate workflow.yml
aic run workflow.yml --input name=Thomas
```

## Features

- YAML workflow parsing and validation
- Sequential step execution
- Jinja templates for inputs and prior step outputs
- Local run artifacts under `.aic/runs/`
- Built-in extensions: `file.read`, `file.write`, `json.parse`, `text.chunk`, `ai.generate`
- AI providers: OpenAI and Ollama

## Scope

AIC is a local CLI runtime. It does not include a web UI, hosted service, auth, marketplace, DAG execution, or agent framework.

## Install

With uv:

```bash
uv sync --extra dev
uv run aic --help
```

With pip:

```bash
pip install -e ".[dev]"
python -m aic.cli --help
```

## Quickstart

Create a starter workflow:

```bash
uv run aic init
```

Validate it:

```bash
uv run aic validate workflow.yml
```

Run it:

```bash
uv run aic run workflow.yml --input name=Thomas
```

The final outputs print as JSON, and run artifacts are written under `.aic/runs/<timestamp>/`.

## Workflow Example

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

## Examples

```bash
uv run aic validate examples/hello.yml
uv run aic run examples/hello.yml --input name=Thomas

uv run aic run examples/json_parse.yml --input 'text={"name":"Thomas"}'
```

## Providers

`ai.generate` uses `provider:model`.

### Ollama

Start Ollama and pull a model:

```bash
ollama pull llama3.2
```

Run the example:

```bash
uv run aic run examples/ollama_summarize.yml --input "text=AIC runs local YAML workflows."
```

Workflow config:

```yaml
providers:
  ollama:
    type: ollama
    base_url: http://localhost:11434

steps:
  - id: summarize
    uses: ai.generate
    with:
      model: ollama:gemma3:4b
      prompt: "Summarize: {{ inputs.text }}"
```

### OpenAI

Use an environment variable:

```bash
export OPENAI_API_KEY="..."
uv run aic run examples/summarize_text.yml --input "text=AIC runs AI workflows as code."
```

Workflow config:

```yaml
providers:
  openai:
    type: openai
    api_key_env: OPENAI_API_KEY
```

You can also use `api_key_file`; if both are set, the environment variable wins.

## Built-In Extensions

| Extension | Input | Output |
| --- | --- | --- |
| `file.read` | `path` | `content` |
| `file.write` | `path`, `content` | `path`, `bytes` |
| `json.parse` | `text` | `value` |
| `text.chunk` | `text`, `size`, `overlap` | `chunks` |
| `ai.generate` | `model`, `prompt` | `text`, `model` |

## Run Artifacts

Each run creates a directory like:

```text
.aic/runs/2026-06-22T18-30-00/
  workflow.yml
  inputs.json
  steps/
    write.input.json
    write.output.json
  outputs.json
  metadata.json
```

For `ai.generate`, AIC also writes `steps/<step-id>.prompt.txt`.

## Development

```bash
uv sync --extra dev
uv run --extra dev pytest
uv run --extra dev ruff check
uv run --extra dev ruff format --check
uv run --extra dev pre-commit install
```

Without uv:

```bash
pip install -e ".[dev]"
pytest
pre-commit install
```
