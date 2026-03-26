# doc-for-agent

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
docagent init --ai <claude|codex|continue|copilot|all> --target /path/to/repo
docagent refresh --root /path/to/repo --output-mode agent
```

## Pick Your Agent

| If you use... | Run this first |
| --- | --- |
| Claude Code | `docagent init --ai claude --target /path/to/repo` |
| Codex | `docagent init --ai codex --target /path/to/repo` |
| CodeBuddy | `docagent init --ai codex --target /path/to/repo` |
| Continue | `docagent init --ai continue --target /path/to/repo` |
| GitHub Copilot | `docagent init --ai copilot --target /path/to/repo` |
| Multiple agents | `docagent init --ai all --target /path/to/repo` |

## Install Matrix

| User profile | Install path | Start command |
| --- | --- | --- |
| Node-first (global) | `npm install -g doc-for-agent` | `docagent init --ai all --target /path/to/repo` |
| Node-first (one-off) | `npx -y doc-for-agent` | `npx -y doc-for-agent init --ai all --target /path/to/repo` |
| Python-first (recommended) | `pipx install doc-for-agent` | `docagent init --ai all --target /path/to/repo` |
| Python-first (venv/system) | `python3 -m pip install doc-for-agent` | `docagent init --ai all --target /path/to/repo` |

## Product CLI v1

Primary commands:

```bash
docagent init --ai <claude|codex|continue|copilot|all> --target /path/to/repo
docagent doctor --target /path/to/repo
docagent refresh --root /path/to/repo --output-mode agent|human|dual
docagent generate --root /path/to/repo --mode refresh --output-mode agent|human|dual
docagent update --target /path/to/repo
docagent versions --target /path/to/repo
```

Utility command:

```bash
docagent quickstart --target /path/to/repo
```

Legacy compatibility:

```bash
docagent install --platform codex --target /path/to/repo
docagent all --target /path/to/repo
```

## Docs

- [Quickstart](docs/quickstart.md)
- [Platform Guide](docs/platforms.md)
- [Maintainer Guide](docs/maintainers.md)
