---
name: "doc-for-agent"
description: "Repository documentation skill package for coding agents"
---
# doc-for-agent

Use this skill when a coding agent needs to inspect a repository, establish or refresh its documentation system, or audit drift between code, commands, manifests, and generated docs.

This product has two layers:

- `doc-for-agent` is the skill package that agents discover and load.
- `docagent` is the workflow adapter that installs the skill, wires a repository, and runs `init / refresh / doctor / versions`.

## Trigger Conditions

Use this skill when one or more of these are true:

- The repository needs stable agent-facing and maintainer-facing documentation.
- The user wants docs that can be refreshed after code, workflow, or terminology changes.
- README, manifests, commands, and implementation appear to disagree.
- The work involves multiple agents or long-lived maintenance and needs a reusable memory layer instead of one-off summaries.

Do not use this skill as a generic markdown writer when the user only wants ad hoc prose unrelated to repository structure.

## Quick Workflow

1. Inspect the repository before describing it.
2. Identify repository shape from code, manifests, commands, routes, and supporting docs.
3. Refresh or audit the paired documentation system.
4. Verify install facts, platform names, and output roots against the current product contract.

If the task is repository-local workflow setup, use:

```bash
docagent init --ai codex
docagent init --ai claudecode
```

If the task is four-view refresh, use:

```bash
docagent refresh --root . --output-mode quad
```

If the task is installation or wiring verification, use:

```bash
docagent doctor --target .
docagent versions --target .
```

## Product Contract

### First-Class Platforms

- `codex`
- `claudecode`

Treat `continue` and `copilot` as compatibility targets, not equal discoverability claims.

### Output Roots

- `dfa-doc/AGENTS/`
- `dfa-doc/AGENTS.zh/`
- `dfa-doc/handbook/`
- `dfa-doc/handbook.zh/`

Treat four-view output as a structure contract. Do not claim the Chinese views are fully polished translations unless the generated content proves it.

### Memory Model

- `AGENTS/` and `AGENTS.zh/` are the long-lived agent memory layer.
- `handbook/` and `handbook.zh/` are maintainer-facing companion views.
- Refresh should maintain a coherent memory system, not create one-off markdown artifacts.

## Progressive Loading

Start with this file. Load deeper resources only when the task needs them.

- Read `references/agents-structure.md` when deciding page responsibilities and output structure.
- Read `references/layered-agents-blueprint.md` when working on layered output semantics or page layout.
- Read `references/multi-platform-distribution-blueprint.md` when changing install paths, platform claims, or packaging/distribution behavior.
- Read scripts under `scripts/` only when adjusting generator behavior or repository analysis.
- Read templates under `templates/` only when changing rendered output or adapter copy.

Do not bulk-load references when a narrower file is enough.

## Working Rules

1. Analyze the repository before describing it.
2. Prefer repository facts over narrative assumptions.
3. Keep install facts, commands, platform names, and directory roots exact.
4. Do not describe `docagent` as the product itself; it is the skill distribution and repository workflow adapter.
5. Treat disagreement between generated views as sync drift.
6. Prefer one coherent refresh cycle over one-sided manual patching.
7. When a repository already has hand-maintained user docs, do not treat them as generated output roots unless the product contract explicitly says so.

## Verification Gate

Before considering the task complete, verify:

1. Commands match the real CLI surface.
2. Platform names match the current contract: `codex`, `claudecode`, `continue`, `copilot`.
3. Output roots match the `dfa-doc/` four-view structure.
4. `AGENTS.zh` and `handbook.zh` do not contain large untranslated English rule blocks.
5. Generated memory pages still reflect real repository entrypoints, boundaries, and command order.

## Installation Facts

Current primary distribution path:

```bash
npm install -g doc-for-agent
```

Current first-class init paths:

```bash
docagent init --ai codex
docagent init --ai claudecode
```

Current four-view refresh path:

```bash
docagent refresh --root . --output-mode quad
```
