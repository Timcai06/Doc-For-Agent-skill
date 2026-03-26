# doc-for-agent Maintainer Guide

This page is for contributors and maintainers, not first-time product users.

## Repository Layout

```text
DocForAgent_skill/
├── README.md
├── LICENSE
├── pyproject.toml
├── setup.py
├── MANIFEST.in
├── package.json
├── .gitignore
└── doc-for-agent/
    ├── SKILL.md
    ├── agents/
    ├── scripts/
    ├── installer/
    ├── templates/
    ├── tests/
    └── references/
```

## Main Structure Notes

- `doc-for-agent/` is the source of truth for the reusable skill and documentation engine
- `doc-for-agent/scripts/doc_for_agent_generator/` contains the modular analysis/build/merge engine
- `doc-for-agent/installer/docagent.py` is the canonical product CLI entrypoint
- `doc-for-agent/installer/node/docagent.js` is the npm/npx thin launcher
- `doc-for-agent/installer/assets/` is the packaged runtime mirror used in installed distributions
- `doc-for-agent/templates/platforms/*.json` defines platform-specific install surfaces
- `doc-for-agent/tests/fixtures/` and `doc-for-agent/tests/unit/` protect engine and CLI behavior

## Packaging Notes

- root packaging files such as `pyproject.toml`, `setup.py`, and `MANIFEST.in` belong to the product-distribution layer
- `installer/assets/` is useful for packaged installs, but it is also a maintenance hotspot
- source edits should normally begin from `scripts/`, `templates/`, `references/`, and `agents/`, then be mirrored into packaged assets through the sync flow

## Codex Skill Install

If you want a manual local Codex skill install:

```bash
ln -sfn /absolute/path/to/doc-for-agent /Users/$USER/.codex/skills/doc-for-agent
```

Restart Codex so the skill is discovered in a new session.

## GitHub Skill Install

If you want to install this skill from the published repository through the Codex skill installer:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Timcai06/Doc-For-Agent-skill \
  --path doc-for-agent
```

Restart Codex so the new skill is loaded in future sessions.

## Release Prep

Before publishing to PyPI or npm:

```bash
python3 doc-for-agent/installer/sync_assets.py
python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
python3 doc-for-agent/tests/verify_generator_snapshots.py
python3 -m pip wheel . -w /tmp/docagent-wheel-check
npm pack --dry-run
```
