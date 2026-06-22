# file.read

Read a UTF-8 text file.

Input:

```yaml
path: input.txt
```

Output:

```json
{
  "content": "..."
}
```

Example:

```yaml
steps:
  - id: read
    uses: file.read
    with:
      path: input.txt
```
