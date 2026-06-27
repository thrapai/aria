# docling

Document conversion extensions.

## docling.convert

Convert a document file to Markdown or JSON with Docling.

Install:

```bash
uv sync --extra docling
```

Input:

```yaml
path: report.pdf
format: markdown
```

Output:

```json
{
  "format": "markdown",
  "content": "# Document text...",
  "text": "# Document text..."
}
```

For JSON output:

```yaml
path: report.pdf
format: json
```

Example:

```yaml
steps:
  - id: extract
    uses: docling.convert
    with:
      path: "{{ inputs.path }}"
      format: markdown
```
