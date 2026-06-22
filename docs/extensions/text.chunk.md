# text.chunk

Split text into character chunks.

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
    uses: text.chunk
    with:
      text: "{{ inputs.text }}"
      size: 4000
      overlap: 0
```
