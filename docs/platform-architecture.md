# Platform Architecture

This repository is organized in layers so one skill can be distributed across multiple agent environments.

## Layers

- `src/doc_for_agent/`
  - Source of truth for generator code, references, and reusable assets.
- `doc-for-agent/`
  - Codex adapter package generated from source-of-truth assets and synced for distribution compatibility.
- `.claude/skills/doc-for-agent/`
  - Claude adapter package generated from shared platform templates and sync outputs.
- `.cursor/skills/doc-for-agent/`
  - Cursor adapter package generated from shared platform templates and sync outputs.
- `.continue/skills/doc-for-agent/`
  - Continue adapter package generated from shared platform templates and sync outputs.
- `.windsurf/skills/doc-for-agent/`
  - Windsurf adapter package generated from shared platform templates and sync outputs.
- `cli/`
  - Distribution entrypoint for installer and maintenance commands.
- `docs/`
  - Human-facing maintenance and architecture notes.

## Current Status

- Codex adapter: implemented
- Claude adapter: implemented
- Cursor adapter: implemented
- Continue adapter: implemented
- Windsurf adapter: implemented
- Shared source-of-truth layer: implemented
- CLI installer layer: implemented
- Config-driven platform adapter generation: implemented
- Python package distribution: implemented

## Design Goal

Keep one canonical implementation while making platform-specific packaging explicit and low-risk.

## Core Rule

If a change affects generator logic, shared references, or adapter wording:

1. Edit `src/doc_for_agent/` first.
2. Regenerate adapters with `python3 scripts/sync_platform_adapters.py`.
3. Run verification before committing.
