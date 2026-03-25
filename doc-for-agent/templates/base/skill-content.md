{{FRONTMATTER}}# {{TITLE}}

{{DESCRIPTION}}

Use this skill when the user wants to initialize or refresh an `AGENTS/` directory for a repository so future coding agents can work from a stable project-specific documentation layer.

## When To Use

- Create an `AGENTS/` directory for a new repository
- Refresh existing agent docs against the latest codebase
- Bootstrap agent-facing docs before multi-agent or multi-worktree work
- Generate a layered entry/execution/memory topology for long-lived projects

## Core Commands

Initialize or refresh the lean profile:

```bash
python3 {{SCRIPT_REL_PATH}} --root "<repo-root>" --mode refresh
```

Prefer the layered profile for long-lived or phase-driven repositories:

```bash
python3 {{SCRIPT_REL_PATH}} --root "<repo-root>" --mode refresh --profile layered
```

Preview changes without writing files:

```bash
python3 {{SCRIPT_REL_PATH}} --root "<repo-root>" --mode refresh --dry-run
```

Explain classification reasoning before writing:

```bash
python3 {{SCRIPT_REL_PATH}} --root "<repo-root>" --mode refresh --explain
```

Force a repo type when auto-detection is ambiguous:

```bash
python3 {{SCRIPT_REL_PATH}} --root "<repo-root>" --mode refresh --repo-type cli-tool
```

## Notes

- The engine scans the real repository before generating docs.
- `bootstrap` is the safer default profile.
- `layered` is better for projects with explicit phases, execution plans, and durable memory files.
- Manual blocks wrapped in `<!-- doc-for-agent:manual-start -->` and `<!-- doc-for-agent:manual-end -->` are preserved during refresh.

## Installed For

- Platform: {{DISPLAY_NAME}}
- Adapter type: {{INSTALL_TYPE}}

## Post-Install

{{POST_INSTALL_NOTES}}
