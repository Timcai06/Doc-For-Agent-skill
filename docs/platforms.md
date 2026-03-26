# doc-for-agent Platform Guide

Use `docagent init --ai ...` as the primary setup command.

## Supported Platforms

| Platform | Adapter type | Install target |
| --- | --- | --- |
| Codex | skill (`SKILL.md`) | `.codex/skills/doc-for-agent/` |
| Claude Code | skill (`SKILL.md`) | `.claude/skills/doc-for-agent/` |
| Continue | skill (`SKILL.md`) | `.continue/skills/doc-for-agent/` |
| GitHub Copilot | prompt (`PROMPT.md`) | `.github/prompts/doc-for-agent/` |

## Start Commands

```bash
docagent init --ai codex --target /path/to/repo
docagent init --ai claude --target /path/to/repo
docagent init --ai continue --target /path/to/repo
docagent init --ai copilot --target /path/to/repo
docagent init --ai all --target /path/to/repo
```

## Packaging Model

`doc-for-agent` currently uses one product story across two ecosystems:

- Python package: canonical runtime and full CLI
- npm package: thin Node launcher for Node-first users

Both paths converge on:

```bash
docagent init --ai ...
docagent doctor ...
docagent refresh ...
```

## Installed Bundle

Each install writes a self-contained bundle under the platform's hidden folder.

That bundle includes:

- the rendered skill or prompt entry file
- generator scripts
- references
- platform templates
- manifests
- an installation receipt with version metadata
