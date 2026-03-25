# CLAUDE.md

This repository is a platformized skill repo for `doc-for-agent`.

## Source Of Truth

- `src/doc_for_agent/` contains the canonical generator logic, references, and reusable assets.
- `doc-for-agent/` is the Codex-facing adapter package kept for install compatibility.
- `.claude/skills/doc-for-agent/` is the Claude-facing skill adapter.

## Verify

```bash
python3 doc-for-agent/tests/verify_generator_snapshots.py
```

## Editing Rules

- Prefer editing files under `src/doc_for_agent/` first.
- Treat adapter folders as distribution surfaces unless a platform-specific change is required.
- If generator behavior changes, rerun the regression verifier.
