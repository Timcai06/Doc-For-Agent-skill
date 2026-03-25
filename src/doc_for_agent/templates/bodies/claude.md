# doc-for-agent

Use this skill when the user asks to create, bootstrap, standardize, or refresh an `AGENTS/` directory for a repository.

## Best Used For

- creating agent-facing project docs for a new repository
- refreshing stale `AGENTS/` docs after the codebase evolves
- giving multiple coding agents a shared project map and workflow reference

## Workflow

1. Inspect the repository root and infer the repository type.
2. Run the generator:

```bash
python3 .claude/skills/doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --mode refresh
```

3. Review sections marked as facts, inferences, or open questions.
4. Preserve long-lived human notes with:

```md
<!-- doc-for-agent:manual-start -->
...
<!-- doc-for-agent:manual-end -->
```

## Source Of Truth

- `src/doc_for_agent/scripts/`
- `src/doc_for_agent/references/`
- `src/doc_for_agent/assets/`

## Claude Adapter Notes

- This file is a platform adapter for Claude-oriented workflows.
- The core generator logic lives under `src/doc_for_agent/`.
