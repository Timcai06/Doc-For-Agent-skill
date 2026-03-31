# Core Goals

## Top Rules (Read First)

- Rule 1: Product positioning: this repository is scoped for CLI coding-agent workflows, not a standalone end-user application.
- Rule 2: Repository adaptation scope: fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans.
- Rule 3: Retention value: prioritize repeatable `init -> refresh -> doctor` lifecycle checks so documentation stays governable, not a one-shot generator output.

## Confirmed Facts

- English | [简体中文](README.zh.md)
- This repository is currently best understood as a `skill/meta repository`.
- The core product is the reusable agent-documentation workflow, not only the generated files themselves.

## Constraints To Preserve

- Avoid drifting away from the repository's real code, scripts, and naming conventions.
- Prefer stable entrypoints and contracts over broad structural churn.
- Review mixed signals before collapsing the repository into a single simplistic mental model.

## Supporting Doc Synthesis (Product)

### Confirmed

- Product positioning: this repository is scoped for CLI coding-agent workflows, not a standalone end-user application.
- Repository adaptation scope: fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans.
- Retention value: prioritize repeatable `init -> refresh -> doctor` lifecycle checks so documentation stays governable, not a one-shot generator output.
- Positioning guardrail: describe `docagent` as an ongoing documentation system (`init/refresh/doctor/migrate`), not a one-shot markdown generator.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 (sources: `docs/landing-page.zh.md`)

### Conflicting

- No direct product conflicts were synthesized from supporting docs.

### Unresolved

- No unresolved product items were synthesized from supporting docs.

## Referenced Repository Docs

- `README.md`
- `docs/landing-page.md`
- `docs/landing-page.zh.md`
- `docs/maintainers.md`

## Open Questions

- Confirm the top-level success criteria and non-goals for this repository.
