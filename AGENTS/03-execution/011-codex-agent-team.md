# Codex App Agent Team Workflow

## Purpose

This file defines the recommended way to run a small agent team in Codex app using:

- one `main` integration window
- multiple `git worktree` execution windows
- explicit handoff and merge rules

It is optimized for repositories like this one where multiple agents can work in parallel, but someone still needs to protect `main`.

## Best Used For

- parallel feature and quality work
- installer/distribution work separated from generator-core work
- avoiding branch switching conflicts between Codex app windows
- creating a repeatable agent-team pattern that can later be productized into the skill itself

## Roles

### 1. Main Integrator

One Codex window stays on `main`.

Responsibilities:

- split work into branches
- create worktrees
- review each worker's change scope
- run final verification
- merge into `main`
- push the integrated result

This window should avoid doing large feature work directly.

### 2. Worker Windows

Each worker gets:

- one dedicated `git worktree`
- one dedicated branch
- one bounded problem area

Typical examples:

- `codex/product-distribution`
- `codex/skill-quality`
- `codex/docs-release`

Each worker should mostly stay inside its write scope.

## Directory Pattern

Recommended layout:

```text
/Users/tim/DocForAgent_skill                    -> main integrator window
/Users/tim/DocForAgent_skill-distribution       -> product/distribution worker
/Users/tim/DocForAgent_skill-quality            -> generation-quality worker
```

## Branch Pattern

Use a stable prefix:

- `codex/<task-name>`

Examples:

- `codex/product-distribution`
- `codex/skill-quality`
- `codex/release-surface`

Archive old experiment lines using:

- `archive/<old-topic>`

## Worktree Commands

Create worker trees from `main`:

```bash
git checkout main
git pull --ff-only

git worktree add ../DocForAgent_skill-distribution -b codex/product-distribution main
git worktree add ../DocForAgent_skill-quality -b codex/skill-quality main
```

List all worktrees:

```bash
git worktree list
```

Remove a finished worktree after merge:

```bash
git worktree remove ../DocForAgent_skill-distribution
git branch -d codex/product-distribution
```

## Window Contract

Each worker window should receive:

- a directory
- a branch
- a role
- a write boundary
- a definition of done
- a required handoff format

Recommended worker prompt structure:

1. where you are working
2. what files you should prefer to touch
3. what files you should avoid
4. what tests you must run
5. what git commands you should provide back to the user

## Write-Scope Rules

To reduce merge pain, each worker should have a preferred write scope.

Example split for this repository:

- `product-distribution`
  - `doc-for-agent/installer/`
  - `doc-for-agent/templates/`
  - `doc-for-agent/scripts/render_platform_adapter.py`
  - install/distribution sections in `README.md`

- `skill-quality`
  - `doc-for-agent/scripts/doc_for_agent_generator/`
  - `doc-for-agent/scripts/init_agents_docs.py`
  - `doc-for-agent/tests/fixtures/`
  - `doc-for-agent/tests/snapshots.json`
  - quality-related sections in `README.md`

If both windows need `README.md`, they should edit different sections whenever possible.

## Handoff Format

Each worker should report back in the same shape:

1. What changed
2. Why it changed
3. Tests run
4. Risks or follow-up ideas
5. Exact git commands for the human to run manually

Recommended git command block:

```bash
git add <files>
git commit -m "..."
git push -u origin <branch>
```

## Merge Order

Default merge order:

1. merge core capability / quality improvements first
2. merge outer product / distribution changes second

Why:

- distribution usually depends on the current engine behavior
- quality improvements often affect README, tests, and generator output
- letting the integrator merge core changes first reduces adapter drift

## Integrator Checklist

Before merging a worker branch into `main`, the integrator should:

1. fetch all remote branches
2. inspect branch-specific diff
3. confirm worker tests passed
4. merge one branch at a time
5. rerun repository-wide verification
6. push `main` only after integrated tests pass

Recommended verification for this repository:

```bash
python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
python3 doc-for-agent/tests/verify_generator_snapshots.py
```

## Why This Works In Codex App

`git worktree` solves branch isolation.
This workflow adds the missing team behavior:

- role separation
- explicit write scopes
- repeatable handoff structure
- one integration authority

That gets close to an "agent team" experience even though Codex app does not currently behave like an automatic swarm runtime.

## Next Productization Step

The next logical evolution for `doc-for-agent` is to turn this workflow into generated project guidance.

That likely means adding generated docs such as:

- `coordination.md`
- `handoff-template.md`
- `merge-checklist.md`
- or a profile specifically for multi-agent Codex work

For now, this file is the reference implementation for how the workflow should feel in practice.
