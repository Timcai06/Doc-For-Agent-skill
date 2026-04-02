# doc-for-agent Quickstart

Language: English | [简体中文](quickstart.zh.md)

This page is for first-time product users.

Use one mental model:

1. install
2. init
3. refresh
Think of it as two and a half steps: global install for agent visibility, repo-local init for repository workflow, then refresh when you want to write or update docs.

`refresh` supports `agent`, `human`, `dual`, and `quad` documentation outputs.
Mode map: `agent` -> `dfa-doc/AGENTS/`, `human` -> `dfa-doc/handbook/`, `dual` -> both, `quad` -> `dfa-doc/AGENTS/`, `dfa-doc/AGENTS.zh/`, `dfa-doc/handbook/`, `dfa-doc/handbook.zh/`.
Dual mode keeps `dfa-doc/handbook/` (human docs) and `dfa-doc/AGENTS/` (agent docs) paired in one refresh flow. Quad mode establishes the bilingual four-view directory contract.
That four-view contract describes the structure target, not a claim that every bilingual page is already fully polished.
This flow is not AGENTS-only; use `human` or `dual` when needed.

## Install
Step 1 (global install): make the skill visible to your coding agent.
Simple path (`uipro-cli` style): `npm install -g doc-for-agent@next` -> `docagent init --ai codex` / `docagent init --ai claudecode`.

Node:

```bash
npm install -g doc-for-agent@next
```

Python:

```bash
pipx install doc-for-agent
```

One-off Node start (no global install):

```bash
npx -y doc-for-agent init --ai all --target <repo-root>
```
This one-off command combines global install and repo-local init for temporary use. `refresh` still comes after it when you want docs generated or updated.

If you only need one platform, replace `all` with `claudecode`, `codex`, `continue`, or `copilot`.

## Init

Step 2 (repo-local init): enable the workflow in the target repository.

Use the short form when you only need agent discoverability:

```bash
docagent init --ai codex
docagent init --ai claudecode
```

Use the repo-local form when you also want to wire the current repository:

```bash
docagent init --ai <codex|claudecode|continue|copilot|all> --target <repo-root>
```

Common picks:

```bash
docagent init --ai all --target <repo-root>
docagent init --ai claudecode --target <repo-root>
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
docagent refresh --root <repo-root> --output-mode quad
```

## Verify

```bash
docagent doctor --target <repo-root>
docagent versions --target <repo-root>
```

See also:
Entry path reminder: `README.md` -> `docs/landing-page.md` -> `docs/quickstart.md` -> `docs/platforms.md`.
- [Landing Page Note](landing-page.md)
- [Platform Guide](platforms.md)
- [Maintainer Guide](maintainers.md)
