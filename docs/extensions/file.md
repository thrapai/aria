# file

Read and write UTF-8 text files.

## file.read

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

## file.write

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
