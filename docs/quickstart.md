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
docagent init --ai <claude|codex|continue|copilot|all> --target <repo-root>
docagent init --ai claude --target <repo-root>
docagent init --ai codex --target <repo-root>
docagent init --ai continue --target <repo-root>
docagent init --ai copilot --target <repo-root>
docagent init --ai all --target <repo-root>
```

CodeBuddy users usually start with:

```bash
docagent init --ai codex --target <repo-root>
```

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
