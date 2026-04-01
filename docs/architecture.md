# Architecture

## Source Of Truth

- `README.md` for stated project goals, setup expectations, and user-facing examples
- `doc-for-agent/SKILL.md` for trigger conditions and maintainer workflow
- `doc-for-agent/agents/openai.yaml` for launcher/marketplace invocation metadata
- `doc-for-agent/scripts/` for generation behavior and repository scanning
- `doc-for-agent/references/` for documentation structure and writing constraints

## Top Rules (Read First)

- Rule 1: CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Rule 2: Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Rule 3: Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.

## Document Contract

- This page is maintainer-facing source-of-truth for its domain; keep it synchronized with `AGENTS/` in dual mode and `docs/` as the human-view root.
- Update this page in the same PR as behavior changes; avoid narrative-only refreshes without command or contract changes.
- Resolve source-of-truth conflicts before editing CLI, adapter, or build-path behavior.

## Dual Sync Checklist

- After edits, refresh in dual mode and verify both `AGENTS/` and `docs/` were updated in the same change set.
- If one side changed without the other, treat it as documentation drift and resolve before merge.
- When source-of-truth files move, update references in both doc systems before adjusting adapter/build-path rules.

## Paired Refresh Rules

- Refresh contract: run one refresh/generate action that updates paired views together; do not patch one locale/audience in isolation.
- Path contract: verify changed files include both `AGENTS*/` and `docs*/` counterparts when behavior changes affect shared source-of-truth.
- Quad-mode contract: when using `--output-mode quad`, validate all four roots (`AGENTS/`, `AGENTS.zh/`, `docs/`, `docs.zh/`) in the same review cycle.
- Architecture pairing rule: if `docs/architecture.md` changes due to boundary/source-of-truth updates, refresh paired architecture paths under both AGENTS roots.

## Dual Pairing Contract (Rules)

- Pairing mode rule: in `dual`, human and agent docs are generated from one analysis pass and must be reviewed as one change set.
- Locale-output rule: human locale `en` maps to `docs/`.
- Template rule: human template variant `paired-core` is part of the pairing contract and must remain consistent across paired docs.
- Path pair rule: `docs/architecture.md` pairs with `AGENTS/02-architecture/004-tech-stack.md` for stack facts and platform anchors.
- Path pair rule: `docs/architecture.md` pairs with `AGENTS/02-architecture/007-architecture-compatibility.md` for source-of-truth and compatibility rules.

## Paired Agent Docs (Dual Mode)

- `AGENTS/02-architecture/004-tech-stack.md` for stack facts and platform anchors.
- `AGENTS/02-architecture/007-architecture-compatibility.md` for source-of-truth and compatibility rules.

## Output Boundary (Human vs Agent)

- Use `docs/` for maintainer-facing policy and decisions; use `AGENTS/` for execution order, command wiring, and handoff runbooks.
- If a change affects both reader types, update both systems in one dual refresh cycle instead of patching only one side.
- Keep architecture rationale in `docs/architecture.md`; keep CLI/build/source-of-truth guardrails in `AGENTS/architecture.md` (or layered architecture docs).

## Dual View Rationale

- `docs/` and `AGENTS/` are two views generated from the same repository analysis and source-of-truth anchors.
- When the two views diverge, treat it as refresh drift rather than independent documentation authority.
- Architecture rationale lives in `docs/architecture.md`, while operational boundaries for agents live in paired AGENTS architecture docs.

## Detected Signals

- Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).

## System Map

- No system map details were detected automatically.

## Synthesis Summary

- Sources analyzed: `3`
- Synthesized statements: `5` confirmed, `0` conflicting, `0` unresolved

## Knowledge Status

### Confirmed Rules

- CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.
- Conflict handling order: 1) check `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md`; 2) then edit adapter/config mappings.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。

### Supporting Signals

- No additional derived product signals were detected from repository structure.

### Decision Backlog

- No unresolved architecture items were synthesized from supporting docs.

### Conflict Watchlist

- No direct architecture conflicts were synthesized from supporting docs.

## Stability Boundaries

- Treat source-of-truth files as canonical when supporting docs disagree.
- Refresh both `docs/` and `AGENTS/` after architecture-impacting changes.

## Update Triggers

- When source-of-truth files, service boundaries, or runtime dependencies change, update this page.
- When integration contracts change (routes/endpoints/storage), refresh architecture notes in the same PR.

## Maintenance Workflow

- Assign one maintainer owner for this document and update it in the same pull request as behavior changes.
- Review this document at least once per sprint or before each release cut.
- Update after boundary, dependency, or interface contract changes.
- No major synthesis conflicts were detected; focus on keeping this page current with implementation changes.

## Bootstrap Backlog (When Docs Are Thin)

- Supporting docs were found; continue consolidating them into this page and archive stale duplicates.

## Provenance

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`
