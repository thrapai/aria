# file.write

Write UTF-8 text to a file.

Input:

```yaml
path: output.txt
content: "Hello {{ inputs.name }}"
```

Output:

```json
{
  "path": "output.txt",
  "bytes": 12
}
```

Example:

```yaml
steps:
  - id: write
    uses: file.write
    with:
      path: hello.txt
      content: "Hello {{ inputs.name }}"
```
