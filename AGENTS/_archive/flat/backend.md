# Backend

## Best Used For

- Runtime, script, and service behavior changes
- Checking stable contracts before changing generated outputs
- Verifying where operational logic actually lives

## Confirmed Facts

- Generation or support scripts are present and act as the runtime behavior of this skill.

## Inferences For Agents

- The most important backend-like surface is the generator script and any install/runtime commands that mutate repository docs.

## Runtime Entry Points

- `doc-for-agent/scripts/init_agents_docs.py`

## Main Services / Endpoints

- No API endpoints were detected automatically.

## Stable Contract Fields

- No stable result-contract fields were detected automatically.

## Storage / Output Rules

- No storage or persistence rules were detected automatically.

## Open Questions

- Confirm which runtime entrypoints agents should read before changing behavior.
- Confirm whether there are outputs or contracts that downstream tools depend on and must not drift.
