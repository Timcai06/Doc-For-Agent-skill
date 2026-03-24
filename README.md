# Doc For Agent Skill

`doc-for-agent` is a reusable Codex skill for bootstrapping an `AGENTS/` documentation directory in a new or existing software repository.

It is designed for teams who want every project to start with a clean, agent-facing documentation structure so coding agents can work against consistent product, architecture, workflow, and terminology docs.

## What It Does

This skill creates or refreshes an `AGENTS/` directory with:

- `AGENTS/README.md`
- `AGENTS/product.md`
- `AGENTS/architecture.md`
- `AGENTS/frontend.md`
- `AGENTS/backend.md`
- `AGENTS/workflows.md`
- `AGENTS/glossary.md`

The generated files are prefilled from the actual repository structure, routes, scripts, and backend contract clues, then intended to be refined further where needed.

## Repository Layout

```text
DocForAgent_skill/
├── README.md
├── LICENSE
└── doc-for-agent/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── scripts/
    │   └── init_agents_docs.py
    └── references/
        └── agents-structure.md
```

## Install As a Codex Skill

If you already use Codex local skills, install this skill into `~/.codex/skills/`.

One approach is to symlink it:

```bash
ln -sfn /absolute/path/to/doc-for-agent /Users/$USER/.codex/skills/doc-for-agent
```

After installation, restart Codex so the skill is discovered in a new session.

## Install From GitHub

If you want to install this skill from the published repository, use the Codex skill installer against this repo path:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Timcai06/Doc-For-Agent-skill \
  --path doc-for-agent
```

After installation, restart Codex so the new skill is loaded in future sessions.

## Use

Ask Codex something like:

- `Create an AGENTS directory for this repository using doc-for-agent`
- `Use doc-for-agent to bootstrap agent docs for this project`
- `Refresh this repo's AGENTS docs based on the real codebase`

The skill's initializer script can also be run directly:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --mode refresh
```

Optional explicit project name:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --project-name "My Project" --mode refresh
```

Use `--mode init` if you want to be explicit about a brand new repository:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --mode init
```

## Design Goals

- Keep agent-facing docs lean
- Prefer real commands over generic prose
- Separate product, architecture, frontend, backend, workflows, and glossary concerns
- Make new projects easier to onboard for coding agents
- Scan the current codebase and prefill useful content instead of generating empty templates
- Support refreshing existing `AGENTS/` docs when the repository evolves

## Publishing

This repository is suitable for publishing on GitHub as a reusable skill source. Other users can install the skill from the repo path once the repository is public.
