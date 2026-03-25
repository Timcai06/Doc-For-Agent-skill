# Source Of Truth

This repository intentionally separates canonical content from platform distribution surfaces.

## Canonical Editing Targets

Edit these first:

- `src/doc_for_agent/scripts/`
- `src/doc_for_agent/references/`
- `src/doc_for_agent/assets/`
- `src/doc_for_agent/templates/`
- `src/doc_for_agent/platforms/configs/`
- `src/doc_for_agent/platforms/codex/agents/openai.yaml`
- `src/doc_for_agent/version.py`

## Generated Or Synced Surfaces

These paths should usually be treated as outputs, not primary editing locations:

- `doc-for-agent/`
- `.claude/skills/doc-for-agent/`
- `.cursor/skills/doc-for-agent/`
- `.continue/skills/doc-for-agent/`
- `.windsurf/skills/doc-for-agent/`

## Workflow

After modifying canonical files, run:

```bash
python3 scripts/sync_platform_adapters.py
```

Then verify:

```bash
python3 doc-for-agent/tests/verify_generator_snapshots.py
python3 cli/docforagent.py doctor
```

## Exceptions

You may edit an adapter directly only when:

- the change is intentionally platform-specific
- the change cannot be represented in the shared templates/configs yet

If that happens, follow up by deciding whether the change should move back into the shared source-of-truth layer.
