---
name: doc-for-agent
description: Generate and maintain a dual documentation system for a repository. Use this when the user wants agent-facing docs in `AGENTS/`, human-facing docs in `docs/`, or both together in one refreshable flow grounded in the current codebase and repository docs.
---
# doc-for-agent

Use this skill when the user wants to initialize or refresh repository documentation so future coding agents and human maintainers can work against a stable, project-specific documentation baseline.

## What This Skill Produces

This skill can generate:

- `AGENTS/` for agent-facing execution docs
- `docs/` for human-facing reference docs
- or both together as a paired dual-doc system

Typical agent-facing files include:

- `AGENTS/product.md`
- `AGENTS/architecture.md`
- `AGENTS/frontend.md`
- `AGENTS/backend.md`
- `AGENTS/workflows.md`
- `AGENTS/glossary.md`
- `AGENTS/README.md`

Typical human-facing files include:

- `docs/overview.md`
- `docs/architecture.md`
- `docs/workflows.md`
- `docs/glossary.md`

The generated docs are prefilled from the real repository structure. They are not generic placeholders only.
The goal is not prettier markdown. The goal is a refreshable documentation baseline with lower ambiguity for both humans and agents.

## When To Use

Trigger this skill when the user asks to:

- create an `AGENTS` directory
- create a `docs/` directory from the current codebase
- bootstrap coding-agent docs for a new project
- bootstrap human-facing project docs for a repo with weak or messy docs
- generate reusable project docs for future agent work
- generate paired human + agent docs
- standardize dual docs across repos
- refresh or rewrite an existing documentation baseline from the latest codebase

Do not use this skill for normal feature work unless the user explicitly wants repository documentation.

## Workflow

### Step 1: Inspect the repository root

Before generating files, quickly inspect:

- top-level folders
- frontend/backend or app/server structure
- package manager / Python / framework hints

Use that to infer:

- project name
- repository type
- likely product purpose
- likely frontend stack
- likely backend stack

### Step 2: Generate or refresh the documentation baseline

For agent docs only, run:

```bash
python3 /Users/tim/DocForAgent_skill/doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --mode refresh --output-mode agent
```

For human docs only, run:

```bash
python3 /Users/tim/DocForAgent_skill/doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --mode refresh --output-mode human
```

For both together, prefer:

```bash
python3 /Users/tim/DocForAgent_skill/doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --mode refresh --output-mode dual
```

If the user gives a project name, also pass:

```bash
python3 /Users/tim/DocForAgent_skill/doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --project-name "<name>" --mode refresh --output-mode dual
```

If the repository is long-lived, phase-driven, or the user explicitly wants an entry/execution/memory layout, prefer:

```bash
python3 /Users/tim/DocForAgent_skill/doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --mode refresh --profile layered --output-mode dual
```

### Step 3: Let the script prefill from the actual codebase

The script will scan and prefill from:

- repository README
- repository type signals such as skill markers, CLI entrypoints, package shape, and frontend/backend structure
- frontend routes
- frontend package scripts
- backend endpoints
- storage behavior
- result contract fields
- canonical terminology hints
- existing `AGENTS/` section content when running in `refresh` mode
- existing `docs/` content when running in human or dual mode

### Step 4: Review and tighten the generated docs

After generation, review the docs and tighten the parts the script cannot infer well:

- product purpose and target users
- domain-specific constraints
- ownership boundaries
- any project-specific naming rules
- any manual sections you want to preserve long term; `refresh` now keeps useful existing section bodies where possible
- any sections still marked as facts vs. inferences vs. open questions
- any hand-maintained blocks wrapped with `<!-- doc-for-agent:manual-start -->` and `<!-- doc-for-agent:manual-end -->`

### Step 5: Keep it lean

These docs are for project execution and maintenance, not marketing.

Prefer:

- confirmed facts over confident guesses
- constraints
- real commands
- route structure
- response contract notes
- naming conventions
- file ownership hints
- task-oriented handoff guidance
- paired human/agent views when the user wants a durable baseline

Avoid:

- long narrative prose
- duplicated README content
- aspirational future-state plans unless the user explicitly wants them
- treating the skill as AGENTS-only when the user clearly wants human or dual docs

## Reference

For the intended file purposes and writing style, see:

- `references/agents-structure.md`
