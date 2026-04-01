# Architecture Compatibility

## Top Rules (Read First)

- Rule 1: CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Rule 2: Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Rule 3: Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.

## Repo-Type Signals

- Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).

## Source Of Truth

- `README.md` for stated project goals, setup expectations, and user-facing examples
- `doc-for-agent/SKILL.md` for trigger conditions and maintainer workflow
- `doc-for-agent/agents/openai.yaml` for launcher/marketplace invocation metadata
- `doc-for-agent/scripts/` for generation behavior and repository scanning
- `doc-for-agent/references/` for documentation structure and writing constraints

## Supporting Doc Synthesis (Architecture)

### Confirmed

- CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.
- Conflict handling order: 1) check `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md`; 2) then edit adapter/config mappings.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 (sources: `docs/platforms.zh.md`)

### Conflicting

- No direct architecture conflicts were synthesized from supporting docs.

### Unresolved

- No unresolved architecture items were synthesized from supporting docs.

## Referenced Historical Docs

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`

## Compatibility Boundaries

- Prefer changing source code and configuration first, then refresh `AGENTS/` docs.
- Do not let generated docs drift away from the repository's actual entrypoints and workflows.
- Skill manifests, README examples, and generator output should describe the same capability surface.

## Conflicting Signals

- Skill markers dominate classification, but packaged tooling signals suggest this repository may also ship installable utilities.
