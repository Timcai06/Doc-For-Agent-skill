# doc-for-agent Quickstart

Language: English | [简体中文](quickstart.zh.md)

This page is for first-time product users.

Use one mental model:

1. install
2. init
3. refresh

## Install

Node:

```bash
npm install -g doc-for-agent
```

Python:

```bash
pipx install doc-for-agent
```

One-off Node start (no global install):

```bash
npx -y doc-for-agent init --ai all --target <repo-root>
```

If you only need one platform, replace `all` with `claude`, `codex`, `continue`, or `copilot`.

## Init

Use one command shape:

```bash
docagent init --ai <claude|codex|continue|copilot|all> --target <repo-root>
```

Common picks:

```bash
docagent init --ai all --target <repo-root>
docagent init --ai claude --target <repo-root>
docagent init --ai codex --target <repo-root>
```

CodeBuddy users usually start with `--ai codex`.

## Refresh

Agent docs:

```bash
docagent refresh --root <repo-root> --output-mode agent
```

Human docs:

```bash
docagent refresh --root <repo-root> --output-mode human
```

Both:

```bash
docagent refresh --root <repo-root> --output-mode dual
```

## Verify

```bash
docagent doctor --target <repo-root>
docagent versions --target <repo-root>
```

See also:

- [Platform Guide](platforms.md)
- [Maintainer Guide](maintainers.md)
