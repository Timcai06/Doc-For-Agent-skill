# doc-for-agent

English | [简体中文](README.zh.md)

`doc-for-agent` is a unified CLI for CLI coding-agent users.

It is designed for Claude Code, Codex, CodeBuddy, Continue, Copilot, and similar terminal-first agent workflows.

The product path is short:

1. install
2. `init`
3. `refresh`

## 30-Second Start

Install once:

```bash
# Node users
npm install -g doc-for-agent

# Python users
pipx install doc-for-agent
```

Start in a repository:

```bash
docagent init --ai <claude|codex|continue|copilot|all> --target <repo-root>
docagent refresh --root <repo-root> --output-mode agent
```

Need a guided doc entry map? Run:

```bash
docagent quickstart --target <repo-root>
```

## Pick Your Agent

| If you use... | Run this first |
| --- | --- |
| Claude Code | `docagent init --ai claude --target <repo-root>` |
| Codex | `docagent init --ai codex --target <repo-root>` |
| CodeBuddy | `docagent init --ai codex --target <repo-root>` |
| Continue | `docagent init --ai continue --target <repo-root>` |
| GitHub Copilot | `docagent init --ai copilot --target <repo-root>` |
| Multiple agents | `docagent init --ai all --target <repo-root>` |

## Install Matrix

| User profile | Install path | Start command |
| --- | --- | --- |
| Node-first (global) | `npm install -g doc-for-agent` | `docagent init --ai all --target <repo-root>` |
| Node-first (one-off) | `npx -y doc-for-agent` | `npx -y doc-for-agent init --ai all --target <repo-root>` |
| Python-first (recommended) | `pipx install doc-for-agent` | `docagent init --ai all --target <repo-root>` |
| Python-first (venv/system) | `python3 -m pip install doc-for-agent` | `docagent init --ai all --target <repo-root>` |

## Product CLI v1

Primary flow commands:

```bash
docagent init --ai <claude|codex|continue|copilot|all> --target <repo-root>
docagent refresh --root <repo-root> --output-mode agent|human|dual
docagent doctor --target <repo-root>
```

Other primary commands:

```bash
docagent generate --root <repo-root> --mode refresh --output-mode agent|human|dual
docagent update --target <repo-root>
docagent versions --target <repo-root>
docagent quickstart --target <repo-root>
```

Legacy compatibility:

```bash
docagent install --platform codex --target <repo-root>
docagent all --target <repo-root>
```

## Docs

- [Quickstart (EN)](docs/quickstart.md) / [快速开始 (ZH)](docs/quickstart.zh.md) (start here)
- [Platform Guide (EN)](docs/platforms.md) / [平台指南 (ZH)](docs/platforms.zh.md) (choose `--ai`)
- [Maintainer Guide](docs/maintainers.md)
