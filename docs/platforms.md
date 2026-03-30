# doc-for-agent Platform Guide

Language: English | [简体中文](platforms.zh.md)

Use `docagent init --ai ...` to choose your platform entrypoint.
Entry path step: this page follows `README.md` -> `docs/landing-page.md` -> `docs/quickstart.md`.
Two-step model: global install makes the skill visible; repo-local init enables this repository workflow.
For temporary Node use, `npx -y doc-for-agent init ...` combines both steps.

## Platform Matrix

| Platform | First command |
| --- | --- |
| Claude Code | `docagent init --ai claudecode` |
| Codex | `docagent init --ai codex` |
| CodeBuddy | `docagent init --ai codex --target <repo-root>` |
| Continue | `docagent init --ai continue --target <repo-root>` |
| GitHub Copilot | `docagent init --ai copilot --target <repo-root>` |

`init` handles platform-specific adapter files automatically. You only need to select `--ai`.
After init, use `refresh --output-mode agent|human|dual|quad` based on the docs audience.
Mode map: `agent` -> `AGENTS/`, `human` -> `docs/`, `dual` -> both, `quad` -> `AGENTS/`, `AGENTS.zh/`, `docs/`, `docs.zh/`.
Dual mode keeps `docs/` (human docs) and `AGENTS/` (agent docs) paired in one refresh flow.
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

Optional modes: `--output-mode human`, `--output-mode dual`, or `--output-mode quad`.

See also:

- [Landing Page Note](landing-page.md)
- [Quickstart](quickstart.md)
- [Maintainer Guide](maintainers.md)
