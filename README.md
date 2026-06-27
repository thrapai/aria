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
- Built-in extensions: `ai.generate`, `file.read`, `file.write`, `utils.json.parse`, `utils.text.chunk`, `docling.convert`
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

For document conversion support:

```bash
uv sync --extra docling
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

Steps can loop over a list with `for_each`; each item is available as `item`, and the step output becomes a list:

```yaml
steps:
  - id: summarize_chunks
    uses: ai.generate
    for_each: "{{ steps.chunks.output.chunks }}"
    with:
      model: openai:gpt-4.1-mini
      prompt: "Summarize this section:\n\n{{ item }}"
```

## Examples

```bash
uv run aic validate examples/hello.yml
uv run aic run examples/hello.yml --input name=Thomas

uv run aic run examples/json_parse.yml --input 'text={"name":"Thomas"}'
uv run --extra docling aic run examples/summarize_document.yml --input path=report.pdf
```

## Providers

`ai.generate` uses `provider:model`.

### Ollama

Start Ollama and pull a model:

```bash
ollama pull gemma3:4b
```

Run the PDF summary example:

```bash
uv run --extra docling aic run examples/summarize_document.yml --input path=report.pdf
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

Extensions are grouped by namespace:

- `ai.*`: AI generation. `ai.generate` returns text today; other output types can fit under the same namespace later.
- `file.*`: plain file IO.
- `utils.*`: generic data utilities.
- `docling.*`: document conversion, including PDF/DOCX to Markdown or JSON.

| Extension | Input | Output |
| --- | --- | --- |
| `file.read` | `path` | `content` |
| `file.write` | `path`, `content` | `path`, `bytes` |
| `utils.json.parse` | `text` | `value` |
| `utils.text.chunk` | `text`, `size`, `overlap`, `delimiter` | `chunks` |
| `ai.generate` | `model`, `prompt` | `text`, `model` |
| `docling.convert` | `path`, `format` | `format`, `content`, `text` |

Each extension has a short example in `docs/extensions/`.

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
