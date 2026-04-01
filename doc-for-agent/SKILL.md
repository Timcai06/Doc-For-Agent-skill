---
name: "doc-for-agent"
description: "Repository documentation skill package for coding agents"
---
# doc-for-agent

Use this skill when a coding agent needs to understand, initialize, refresh, or audit a repository documentation system for both agents and human maintainers.

This package is not just a standalone CLI. The product has two layers:

- `doc-for-agent` is the **skill package** that agents discover and load.
- `docagent` is the **workflow adapter** that installs the skill, wires a repository, and runs `init / refresh / doctor`.

## When To Use

- A repository needs a stable agent-facing and maintainer-facing documentation baseline.
- The user wants repository docs that can be refreshed after code, workflow, or terminology changes.
- The repository has drift between README, manifests, commands, and actual implementation.
- Multi-agent or long-lived work needs shared contracts instead of one-off markdown summaries.

## Product Model

### 1. Repository Analysis

- Inspect the real repository structure first.
- Classify the repository shape from code, manifests, routes, commands, and supporting docs.
- Prefer repository facts over narrative assumptions.

### 2. Documentation System Refresh

- Build or refresh the paired documentation system from repository facts.
- Output roots:
  - `AGENTS/`
  - `AGENTS.zh/`
  - `docs/`
  - `docs.zh/`
- Treat four-view output as a **structure contract**. Do not assume bilingual content quality is already complete.

### 3. Consistency Audit

- Check that install paths, commands, platform names, and documentation roots stay aligned.
- Treat disagreement between views as sync drift.
- Prefer one coherent refresh cycle over one-sided manual patching.

## Execution Model

### Skill Layer

- Use `SKILL.md`, `references/`, `templates/`, and `scripts/` progressively.
- Start from the workflow in this file.
- Load extra references only when the current task needs them.

### Workflow Adapter Layer

- Install / wire repository workflow with `docagent`.
- Current primary distribution path:

```bash
npm install -g doc-for-agent@next
```

- Current first-class init paths:

```bash
docagent init --ai codex
docagent init --ai claudecode
```

- Current repository refresh path:

```bash
docagent refresh --root . --output-mode quad
```

## Working Rules

1. Analyze the repository before describing it.
2. Treat `codex` and `claudecode` as first-class platform targets.
3. Keep `continue` and `copilot` as compatibility targets, not equal discoverability claims.
4. Do not describe `docagent` as the product itself; it is the skill distribution and repo workflow adapter.
5. Do not claim `AGENTS.zh/` or `docs.zh/` are fully polished translations unless the generated content actually proves it.
6. Keep installation facts, commands, and directory names exact.

## Verification Gate

Before considering the task complete, verify:

1. Commands match the real CLI surface.
2. Platform names match the current product contract (`codex`, `claudecode`, `continue`, `copilot`).
3. Output roots match the current four-view structure.
4. Chinese views do not contain large untranslated English rule blocks.

## Common Commands

- Install the npm-distributed skill package:
  - `npm install -g doc-for-agent@next`
- Initialize a repository for Codex:
  - `docagent init --ai codex`
- Initialize a repository for Claude Code:
  - `docagent init --ai claudecode`
- Refresh all four roots:
  - `docagent refresh --root . --output-mode quad`
- Check install / wiring status:
  - `docagent doctor --target .`
- Inspect current version state:
  - `docagent versions --target .`
