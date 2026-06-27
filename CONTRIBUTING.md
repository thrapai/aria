# Contributing

Thanks for helping improve ARIA. Keep changes small, tested, and easy to review.

The most useful contributions are new or improved extensions that let ARIA work with more tools, file types, providers, and workflow capabilities.

## Development

```bash
uv sync --extra dev
uv run --extra dev python -m pytest
uv run --extra dev ruff check
uv run --extra dev ruff format --check
```

For document conversion work:

```bash
uv sync --extra dev --extra docling
```

## Pull Requests

- Open an issue first for large behavior changes.
- Add or update tests for runtime behavior.
- Keep README changes focused on user-facing behavior.
- Do not commit run artifacts, coverage output, or built distributions.
