# docling.convert

Convert a document file to Markdown text with Docling.

Install:

```bash
uv sync --extra docling
```

Input:

```yaml
path: report.pdf
```

Output:

```json
{
  "text": "# Document text..."
}
```

Example:

```yaml
steps:
  - id: extract
    uses: docling.convert
    with:
      path: "{{ inputs.path }}"
```
