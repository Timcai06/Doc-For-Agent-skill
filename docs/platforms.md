# doc-for-agent Platform Guide

Language: English | [简体中文](platforms.zh.md)

Use `docagent init --ai ...` to choose your platform entrypoint.

## Platform Matrix

| Platform | First command |
| --- | --- |
| Claude Code | `docagent init --ai claude --target <repo-root>` |
| Codex | `docagent init --ai codex --target <repo-root>` |
| CodeBuddy | `docagent init --ai codex --target <repo-root>` |
| Continue | `docagent init --ai continue --target <repo-root>` |
| GitHub Copilot | `docagent init --ai copilot --target <repo-root>` |

`init` handles platform-specific adapter files automatically. You only need to select `--ai`.
After init, use `refresh --output-mode agent|human|dual` based on the docs audience.
Mode map: `agent` -> `AGENTS/`, `human` -> `docs/`, `dual` -> both.
Platform selection is separate from doc audience: this is not AGENTS-only.

## Multi-Agent Setup

```bash
docagent init --ai all --target <repo-root>
```

## Distribution Model

- Python package: canonical runtime and full CLI.
- npm package: thin Node launcher for Node-first users.
- Both paths converge to the same command surface: `docagent`.

## Next Command

Default:

```bash
docagent refresh --root <repo-root> --output-mode agent
```

Optional modes: `--output-mode human` or `--output-mode dual`.

See also:

- [Landing Page Note](landing-page.md)
- [Quickstart](quickstart.md)
- [Maintainer Guide](maintainers.md)
