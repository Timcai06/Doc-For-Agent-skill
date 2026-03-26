# doc-for-agent Platform Guide

Use `docagent init --ai ...` to choose your platform entrypoint.

## Platform Matrix

| Platform | First command | Adapter type | Install target |
| --- | --- | --- | --- |
| Claude Code | `docagent init --ai claude --target <repo-root>` | skill (`SKILL.md`) | `.claude/skills/doc-for-agent/` |
| Codex | `docagent init --ai codex --target <repo-root>` | skill (`SKILL.md`) | `.codex/skills/doc-for-agent/` |
| CodeBuddy | `docagent init --ai codex --target <repo-root>` | skill (`SKILL.md`) | `.codex/skills/doc-for-agent/` |
| Continue | `docagent init --ai continue --target <repo-root>` | skill (`SKILL.md`) | `.continue/skills/doc-for-agent/` |
| GitHub Copilot | `docagent init --ai copilot --target <repo-root>` | prompt (`PROMPT.md`) | `.github/prompts/doc-for-agent/` |

## Multi-Agent Setup

```bash
docagent init --ai all --target <repo-root>
```

## Distribution Model

- Python package: canonical runtime and full CLI.
- npm package: thin Node launcher for Node-first users.
- Both paths converge to the same command surface: `docagent`.

## Next Command

After init:

```bash
docagent refresh --root <repo-root> --output-mode agent
```

See also:

- [Quickstart](quickstart.md)
- [Maintainer Guide](maintainers.md)
