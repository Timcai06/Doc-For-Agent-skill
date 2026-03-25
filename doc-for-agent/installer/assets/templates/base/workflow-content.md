{{FRONTMATTER}}# {{TITLE}}

{{DESCRIPTION}}

Use this workflow when the user wants to create or refresh an `AGENTS/` directory for a repository.

## Workflow

1. Inspect the repository root and infer the repo shape.
2. Run the generator in `refresh` mode first.
3. Prefer `--profile layered` when the repository is long-lived or phase-driven.
4. Use `--dry-run` or `--explain` when the repository shape is unclear.

## Commands

```bash
python3 {{SCRIPT_REL_PATH}} --root "<repo-root>" --mode refresh
```

```bash
python3 {{SCRIPT_REL_PATH}} --root "<repo-root>" --mode refresh --profile layered
```

## Installed For

- Platform: {{DISPLAY_NAME}}
- Adapter type: {{INSTALL_TYPE}}

## Post-Install

{{POST_INSTALL_NOTES}}
