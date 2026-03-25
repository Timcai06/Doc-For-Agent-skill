# Manual Preservation Example

Use explicit preservation blocks inside any generated AGENTS section:

```md
<!-- doc-for-agent:manual-start -->
- Human-maintained note that should survive refresh.
<!-- doc-for-agent:manual-end -->
```

The generator keeps these blocks when `--mode refresh` is used.
