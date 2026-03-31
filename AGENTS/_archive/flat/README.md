# AGENTS

## Best Used For

- Fast onboarding when a new coding agent enters this repository
- Multi-agent work where terminology, workflow, and ownership boundaries need to stay aligned
- Refreshing repo-specific context after the codebase structure changes

## Dual Documentation System

- `AGENTS/` is the agent-facing rule/runbook layer for execution and handoff.
- `docs/` is the human-facing system context layer for maintainers and onboarding.
- Prefer `--output-mode dual` so both layers stay synchronized after refresh.

## Repository Classification

- Detected repo type: `skill/meta repository`

## Files

- `product.md`: why this repository exists and what agents should preserve
- `architecture.md`: repository shape, source-of-truth files, and handoff boundaries
- `frontend.md`: UI/client context for frontend-facing repos, or agent-facing interface notes otherwise
- `backend.md`: service/runtime contract notes or implementation/runtime entrypoints
- `workflows.md`: setup, execution, verification, and refresh commands
- `glossary.md`: canonical names, labels, and terminology that should stay stable
