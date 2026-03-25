# Platform Targets

This repository currently generates and distributes adapters for five targets.

## Supported Targets

- `codex`
  - Install path: `~/.codex/skills/doc-for-agent`
  - Adapter root in repo: `doc-for-agent/`
- `claude`
  - Install path: `.claude/skills/doc-for-agent`
  - Adapter root in repo: `.claude/skills/doc-for-agent/`
- `cursor`
  - Install path: `.cursor/skills/doc-for-agent`
  - Adapter root in repo: `.cursor/skills/doc-for-agent/`
- `continue`
  - Install path: `.continue/skills/doc-for-agent`
  - Adapter root in repo: `.continue/skills/doc-for-agent/`
- `windsurf`
  - Install path: `.windsurf/skills/doc-for-agent`
  - Adapter root in repo: `.windsurf/skills/doc-for-agent/`

## Shared Inputs

Each target is generated from:

- `src/doc_for_agent/templates/platform_skill.md`
- `src/doc_for_agent/templates/bodies/*.md`
- `src/doc_for_agent/platforms/configs/*.json`
- shared generator and reference files under `src/doc_for_agent/`

## Maintainer Guidance

- Prefer changing the config/template system instead of hand-editing multiple target folders.
- If a new target is added, update:
  - platform configs
  - installer target lists
  - sync script copy map
  - CLI docs
  - release and CI verification if needed
