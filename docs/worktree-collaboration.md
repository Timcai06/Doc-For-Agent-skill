# Worktree Collaboration Rules

This document defines the default collaboration model for `doc-for-agent`.

## Default Topology

- `main` is the integrator branch and product-control surface.
- `codex/skill-quality` is the primary execution branch for output quality and documentation-engine work.
- `codex/product-distribution` is the secondary execution branch for entrypoint, install, and product-surface work.

## Role Boundaries

### `main`

`main` is responsible for:

- product judgment
- task splitting
- merge order
- full verification
- final integration and push

`main` should avoid doing large feature implementation unless the work is explicitly product-strategy or integration-specific.

### `codex/skill-quality`

This branch is the primary branch.

It is responsible for:

- synthesis quality
- human / agent / dual output behavior
- refresh / generate retention quality
- dogfooding output usefulness
- fixtures, snapshots, and engine-facing tests

It should avoid:

- npm/package entrypoint work
- README landing-page rewrites unless the change is tightly coupled to output semantics

### `codex/product-distribution`

This branch is the secondary branch.

It is responsible for:

- `docagent` entry experience
- README / quickstart / platform-guide consistency
- installer wording and first-run UX
- lightweight packaging and launcher polish

It should avoid:

- deep generator logic
- broad output-model redesign
- repo-analysis expansion unless a CLI wiring change strictly requires it

## Work Allocation Rule

Default allocation is:

- roughly 70% effort on `codex/skill-quality`
- roughly 30% effort on `codex/product-distribution`

That ratio should hold whenever product entry is already good enough and output retention remains the main differentiator.

## Merge Rule

Default merge order:

1. `codex/skill-quality`
2. `codex/product-distribution`

Reason:

- product-surface work should land on top of the latest output behavior, not the other way around

## When To Open A New Branch / Worktree

Do **not** open a third long-lived worktree by default.

Open an additional branch/worktree only when one of these is true:

- a strategy/documentation initiative becomes a real delivery track with files, tests, or launch assets of its own
- a risky architecture experiment needs isolation from both current worker branches
- a release/launch track begins to conflict with both quality work and distribution work

If the extra work does not yet have a concrete output surface, keep it on `main` as product/integration planning instead of spawning a new long-lived branch.

## Worker Handoff Format

Every worker should return:

- what changed
- why it was designed that way
- tests run
- remaining risks / next steps
- exact `git add`, `git commit`, and `git push` commands for the user to run manually

## Decision Rule

When there is tension between:

- more features
- better output quality
- lower entry friction

prefer, in order:

1. better output quality
2. lower entry friction
3. more features

This repository should optimize for retention value before breadth.
