# Frontend

## Best Used For

- Agent-facing interface context and user entrypoint discovery
- Checking which screens, prompts, or interaction surfaces must stay consistent

## Confirmed Facts

- Agent-facing interface manifests are present.
- Primary user interaction likely happens through an AI assistant invoking this skill rather than a browser UI.

## Inferences For Agents

- The closest thing to a frontend here is the installation and invocation surface exposed through skill manifests and prompts.

## Routes Or Interaction Entry Points

- No browser routes were detected automatically.

## Key Components Or Interface Files

- No component inventory was detected automatically.

## Agent Manifests / Prompt Surfaces

- `doc-for-agent/agents/openai.yaml`

## Open Questions

- Confirm the primary interaction surface agents should preserve: browser UI, CLI UX, or skill prompt surface.
- Confirm any labels, command names, or invocation phrases that must remain stable for users.
