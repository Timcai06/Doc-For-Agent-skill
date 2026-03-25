# Maintainer Workflow

This is the shortest safe loop for working on the productized repository.

## Daily Development

1. Edit canonical files under `src/doc_for_agent/`.
2. Regenerate adapters:

```bash
python3 scripts/sync_platform_adapters.py
```

3. Run product checks:

```bash
python3 scripts/verify_product_metadata.py
python3 doc-for-agent/tests/verify_generator_snapshots.py
python3 cli/docforagent.py doctor
```

4. If packaging changed, also run:

```bash
python3 -m build --no-isolation
```

## Before Opening A PR

- confirm adapter outputs are synced
- confirm changelog is updated when the user-facing product changes
- confirm README and CLI docs still match actual commands

## Before Tagging A Release

- update `src/doc_for_agent/version.py`
- update `cli/package.json`
- update `CHANGELOG.md`
- rerun the full verification loop

## Branching

Recommended branch prefixes:

- `codex/feature-*`
- `codex/fix-*`
- `codex/release-*`
