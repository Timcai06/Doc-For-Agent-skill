# doc-for-agent Quickstart

Language: English | [简体中文](quickstart.zh.md)

This page is for first-time users of the repository memory system.
`docagent` is the distribution + workflow adapter command for this skill package.

Use one mental model:

1. install
2. init
3. refresh
Think of it as two and a half steps: global install for agent visibility, repo-local init for repository workflow, then refresh when you want to write or update docs.

`refresh` supports `agent`, `human`, `dual`, and `quad` documentation outputs.
Mode map: `agent` -> `dfa-doc/AGENTS/`, `human` -> `dfa-doc/handbook/`, `dual` -> both, `quad` -> `dfa-doc/AGENTS/`, `dfa-doc/AGENTS.zh/`, `dfa-doc/handbook/`, `dfa-doc/handbook.zh/`.
`dfa-doc/AGENTS/` + `dfa-doc/AGENTS.zh/` are the long-term agent memory layer.
`dfa-doc/handbook/` + `dfa-doc/handbook.zh/` are maintainer-facing views.
Dual mode keeps memory layer and handbook views paired in one refresh flow. Quad mode establishes the bilingual four-view directory contract.
That four-view contract describes the structure target, not a claim that every bilingual page is already fully polished.
This flow is not AGENTS-only; use `human` or `dual` when needed.

## Install
Step 1 (global install): make the skill visible to your coding agent.
Simple path (`uipro-cli` style): `npm install -g doc-for-agent` -> `docagent init --ai codex` / `docagent init --ai claudecode`.

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
This one-off command combines global install and repo-local init for temporary use. `refresh` still comes after it when you want docs generated or updated.

If you only need one platform, replace `all` with:
- first-class: `codex` or `claudecode`
- compatibility: `continue` or `copilot`

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

First-class platforms are `codex` and `claudecode`; `continue` and `copilot` are compatibility targets.

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
