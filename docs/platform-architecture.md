# Platform Architecture

This repository is organized in layers so one skill can be distributed across multiple agent environments.

## Layers

- `src/doc_for_agent/`
  - Source of truth for generator code, references, and reusable assets.
- `doc-for-agent/`
  - Codex adapter package. Keeps the traditional install path and delegates execution to `src/`.
- `.claude/skills/doc-for-agent/`
  - Claude adapter package. Carries Claude-facing skill metadata.
- `cli/`
  - Reserved distribution layer for a future installer or sync tooling.
- `docs/`
  - Human-facing maintenance and architecture notes.

## Current Status

- Codex adapter: implemented
- Claude adapter: scaffolded
- Shared source-of-truth layer: implemented
- CLI installer layer: scaffolded, not implemented yet

## Design Goal

Keep one canonical implementation while making platform-specific packaging explicit and low-risk.
