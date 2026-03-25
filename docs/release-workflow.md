# Release Workflow

This repository now has enough packaging and automation to follow a lightweight release process.

## Version Source

- Canonical version: `src/doc_for_agent/version.py`
- Python package version is read from that file through `pyproject.toml`
- CLI user-facing version output also reads from that file

## Before Releasing

Run:

```bash
python3 doc-for-agent/tests/verify_generator_snapshots.py
python3 cli/docforagent.py doctor
python3 cli/docforagent.py sync
python3 -m build
```

Update:

- `CHANGELOG.md`
- any user-facing installation docs if commands changed

## Tagging

Recommended tag format:

```text
v0.1.0
```

## GitHub Release

The release workflow is designed to:

- run tests
- build Python distribution artifacts
- attach `dist/*` files to the GitHub Release when a `v*` tag is pushed

## Notes

- `cli/package.json` is currently informational and should be kept aligned with the Python version manually.
- If adapter templates change, run `python3 scripts/sync_platform_adapters.py` before tagging.
