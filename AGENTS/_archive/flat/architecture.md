# Architecture

## Best Used For

- Building a quick mental model of repository boundaries before editing
- Deciding which files are canonical versus generated
- Handing work between agents without losing context

## Confirmed Facts

- Repository root: `/Users/tim/DocForAgent_skill`.
- Detected repo type: `skill-meta`.
- Classification confidence: `high`.
- Skill definition entrypoint: `doc-for-agent/SKILL.md`.
- Agent manifest files are present for marketplace or launcher integration.

## Repo-Type Signals

- Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).

## Secondary Traits

- No secondary traits were detected automatically.

## Conflicting Signals

- No major conflicting signals were detected automatically.

## Source Of Truth For Agents

- `doc-for-agent/SKILL.md` for trigger conditions and operator workflow
- `doc-for-agent/scripts/` for generation behavior and repository scanning
- `doc-for-agent/references/` for output structure and style constraints

## Handoff Boundaries

- Prompt/instruction changes should stay aligned with generator behavior so agents are not told to do something the script cannot support.
- Generated `AGENTS/` docs are downstream artifacts; review the generator and references before hand-editing broad structure.

## Open Questions

- No open architecture questions recorded.
