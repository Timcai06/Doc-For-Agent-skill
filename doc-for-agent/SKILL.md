---
name: "doc-for-agent"
description: "Generate and maintain a refreshable documentation system for coding agents and human maintainers. Use this when the user wants agent-facing docs in `AGENTS/`, human-facing docs in `docs/`, or a four-view layout across English and Chinese."
---
# doc-for-agent

`doc-for-agent` is a repository documentation bootstrapper for CLI coding-agent workflows.

Use this skill when the user wants to initialize or refresh repository docs so future coding agents and human maintainers can work from a stable, project-specific documentation baseline.

## When To Use

- Create or refresh `AGENTS/` for agent-facing execution docs
- Create or refresh `docs/` for human-facing reference docs
- Generate `dual` output when the repository needs paired human/agent views
- Generate `quad` output when the repository needs four persistent views:
  - `AGENTS/`
  - `AGENTS.zh/`
  - `docs/`
  - `docs.zh/`
- Bootstrap repository docs before multi-agent or multi-worktree work

## Core Commands

Install once, then make the skill visible to the agent:

```bash
npm install -g doc-for-agent@next
docagent init --ai codex
```

Claude Code uses the same product entry:

```bash
docagent init --ai claudecode
```

Refresh agent docs only:

```bash
python3 /Users/tim/DocForAgent_skill/doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --mode refresh --output-mode agent
```

Refresh human docs only:

```bash
python3 /Users/tim/DocForAgent_skill/doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --mode refresh --output-mode human
```

Refresh paired human + agent docs:

```bash
python3 /Users/tim/DocForAgent_skill/doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --mode refresh --output-mode dual
```

Refresh all four views:

```bash
python3 /Users/tim/DocForAgent_skill/doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --mode refresh --output-mode quad
```

Prefer the layered profile for long-lived repositories:

```bash
python3 /Users/tim/DocForAgent_skill/doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --mode refresh --profile layered --output-mode dual
```

## Notes

- The engine scans the real repository before generating docs.
- `agent`, `human`, `dual`, and `quad` are audience/layout choices, not repository-type choices.
- `quad` establishes the directory contract for bilingual output; it does not yet promise translated content quality.
- Manual blocks wrapped in `<!-- doc-for-agent:manual-start -->` and `<!-- doc-for-agent:manual-end -->` are preserved during refresh.
- `docagent init --ai <platform>` is the product entry for global agent discoverability.
- Add `--target <repo-root>` when you want repo-local workflow wiring in the same command.

## Installed For

- Platform: Codex
- Adapter type: skill

## Post-Install

- Use `docagent init --ai codex` or `docagent init --ai claudecode` as the recommended product entry.
- Restart Codex so the new skill is discovered in a fresh session.
- Use repo-local wiring when you want a repository to carry its own assistant wrapper and refresh workflow.
