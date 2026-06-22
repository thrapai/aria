# json.parse

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
    uses: json.parse
    with:
      text: "{{ inputs.text }}"
```
