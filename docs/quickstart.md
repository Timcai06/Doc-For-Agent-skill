# doc-for-agent Quickstart

`doc-for-agent` is designed for CLI coding-agent workflows.

The normal flow is:

1. install the product CLI
2. choose your assistant
3. refresh repository docs

## Fastest Start

Node users:

```bash
npm install -g doc-for-agent
docagent init --ai codex --target /path/to/repo
docagent refresh --root /path/to/repo --output-mode agent
```

Python users:

```bash
pipx install doc-for-agent
docagent init --ai claude --target /path/to/repo
docagent refresh --root /path/to/repo --output-mode agent
```

## One-Off Start

If you do not want a global install:

```bash
npx -y doc-for-agent
npx -y doc-for-agent init --ai all --target /path/to/repo
```

## Common Flows

Install all supported assistant adapters:

```bash
docagent init --ai all --target /path/to/repo
```

Verify install state:

```bash
docagent doctor --target /path/to/repo
```

Refresh agent docs only:

```bash
docagent refresh --root /path/to/repo --output-mode agent
```

Generate human docs only:

```bash
docagent generate --root /path/to/repo --mode refresh --output-mode human
```

Generate both human and agent docs:

```bash
docagent refresh --root /path/to/repo --output-mode dual
```
