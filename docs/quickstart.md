# doc-for-agent Quickstart

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

One-off Node run:

```bash
npx -y doc-for-agent
```

## Init

Pick one:

```bash
docagent init --ai claude --target /path/to/repo
docagent init --ai codex --target /path/to/repo
docagent init --ai continue --target /path/to/repo
docagent init --ai copilot --target /path/to/repo
docagent init --ai all --target /path/to/repo
```

CodeBuddy users usually start with:

```bash
docagent init --ai codex --target /path/to/repo
```

## Refresh

Agent docs:

```bash
docagent refresh --root /path/to/repo --output-mode agent
```

Human docs:

```bash
docagent refresh --root /path/to/repo --output-mode human
```

Both:

```bash
docagent refresh --root /path/to/repo --output-mode dual
```

## Verify

```bash
docagent doctor --target /path/to/repo
docagent versions --target /path/to/repo
```

See also:

- [Platform Guide](platforms.md)
- [Maintainer Guide](maintainers.md)

