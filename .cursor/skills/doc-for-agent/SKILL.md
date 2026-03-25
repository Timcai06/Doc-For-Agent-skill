---
name: doc-for-agent
description: Generate and refresh an AGENTS directory for a repository so coding agents can work from stable, project-specific context instead of rediscovering the codebase every time.
---
# doc-for-agent

Use this skill when the user asks to create, standardize, or refresh `AGENTS/` docs for a repository.

## Best Used For

- bootstrapping agent-facing project docs
- refreshing stale AGENTS docs after codebase changes
- giving multiple agents one shared project map

## Run

```bash
python3 .cursor/skills/doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --mode refresh
```
