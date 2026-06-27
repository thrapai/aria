# utils

Generic data utilities.

## utils.json.parse

Parse JSON text.

Input:

```yaml
text: '{"name":"Thomas"}'
```

Output:

```json
{
  "value": {
    "name": "Thomas"
  }
}
```

Example:

```yaml
steps:
  - id: parse
    uses: utils.json.parse
    with:
      text: "{{ inputs.text }}"
```

## utils.text.chunk

Split text by size, delimiter, or delimiter chunks packed up to a size.

Input:

```yaml
text: "abcdef"
size: 3
overlap: 1
```

Output:

```json
{
  "chunks": ["abc", "cde", "ef"]
}
```

Example:

```yaml
steps:
  - id: chunks
    uses: utils.text.chunk
    with:
      text: "{{ inputs.text }}"
      size: 4000
      overlap: 0
```

Delimiter example:

```yaml
steps:
  - id: chunks
    uses: utils.text.chunk
    with:
      text: "{{ steps.extract.output.content }}"
      delimiter: "\n## "
      size: 4000
```

With both `delimiter` and `size`, chunks are split on the delimiter first, then packed together up to `size`.
If one delimiter chunk is larger than `size`, it is split into raw `size` character chunks.
