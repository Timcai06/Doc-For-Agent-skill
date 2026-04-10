# App Flow

## Surfaces Detected

- Agent manifest surface: `doc-for-agent/agents/openai.yaml`

## Guidance

- Treat the first visible or invoked surface as part of the product contract.
- Keep user-facing names aligned across README examples, manifests, routes, and commands.
- Treat install, invocation, and prompt surfaces as the equivalent of a frontend contract.

## Supporting Doc Synthesis (Flow)

### Confirmed

- Product positioning: this repository is scoped for CLI coding-agent workflows, not a standalone end-user application.
- Repository adaptation scope: fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans.
- Retention value: prioritize repeatable `init -> refresh -> doctor` lifecycle checks so documentation stays governable, not a one-shot generator output.
- Positioning guardrail: describe `docagent` as an ongoing documentation system (`init/refresh/doctor/migrate`), not a one-shot markdown generator.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent -> docagent init --ai codex / docagent init --ai claudecode。 (sources: `docs/landing-page.zh.md`)

### Conflicting

- No direct flow conflicts were synthesized from supporting docs.

### Unresolved

- No unresolved flow items were synthesized from supporting docs.
