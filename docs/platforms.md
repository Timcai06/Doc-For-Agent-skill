# doc-for-agent Platform Guide

Language: English | [简体中文](platforms.zh.md)

Use `docagent init --ai ...` to choose your platform entrypoint.
`docagent` is the distribution + workflow adapter for this repository memory skill package.
Entry path step: this page follows `README.md` -> `docs/landing-page.md` -> `docs/quickstart.md`.
Two-step model: global install makes the skill visible; repo-local init enables this repository workflow.
`refresh` is the half-step after init: run it when you want to write or update agent docs, human docs, or both.
For temporary Node use, `npx -y doc-for-agent init ...` combines both setup steps. `refresh` still remains separate.
Use `--target <repo-root>` only when wiring a specific repository from outside it.
Simple path (`uipro-cli` style): `npm install -g doc-for-agent` -> `docagent init --ai codex` / `docagent init --ai claudecode`.

## Platform Matrix

| Platform tier | First command |
| --- | --- |
| First-class: Claude Code | `docagent init --ai claudecode` |
| First-class: Codex | `docagent init --ai codex` |
| Compatibility: Continue | `docagent init --ai continue --target <repo-root>` |
| Compatibility: GitHub Copilot | `docagent init --ai copilot --target <repo-root>` |

`init` handles platform-specific adapter files automatically. You only need to select `--ai`.
After init, use `refresh --output-mode agent|human|dual|quad` based on the docs audience.
Mode map: `agent` -> `dfa-doc/AGENTS/`, `human` -> `dfa-doc/handbook/`, `dual` -> both, `quad` -> `dfa-doc/AGENTS/`, `dfa-doc/AGENTS.zh/`, `dfa-doc/handbook/`, `dfa-doc/handbook.zh/`.
Dual mode keeps `dfa-doc/handbook/` (human docs) and `dfa-doc/AGENTS/` (agent docs) paired in one refresh flow.
The four-view layout is a structure capability, not a claim that every bilingual view is already complete.
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
