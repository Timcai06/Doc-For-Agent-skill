# Doc For Agent Skill

`doc-for-agent` is a reusable Codex skill for bootstrapping an `AGENTS/` documentation directory in a new or existing software repository.

It is designed for teams who want every project to start with a clean, agent-facing documentation structure so coding agents can work against consistent product, architecture, workflow, and terminology docs.

This repository is now organized as a platformized skill repo:

- `src/doc_for_agent/` is the source of truth
- `doc-for-agent/` is the Codex adapter package
- `.claude/skills/doc-for-agent/` is the Claude adapter scaffold
- `.cursor/skills/doc-for-agent/`, `.continue/skills/doc-for-agent/`, and `.windsurf/skills/doc-for-agent/` are additional skill adapters
- `scripts/sync_platform_adapters.py` syncs shared source files into adapters

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

When run in `refresh` mode, the generator now merges by section and tries to preserve useful existing manual content instead of blindly overwriting whole files.
For long-lived notes, you can explicitly protect a block inside any section with:

```md
<!-- doc-for-agent:manual-start -->
Your hand-maintained notes here.
<!-- doc-for-agent:manual-end -->
```

The refresh step will carry those manual blocks forward.

The generator is now more agent-first in three important ways:

- it classifies the repository shape before choosing how to describe it
- it distinguishes confirmed facts from agent-facing inferences and open questions
- it writes docs toward agent execution and handoff, not just human-oriented project summaries

## Repository Layout

```text
DocForAgent_skill/
├── README.md
├── LICENSE
├── CLAUDE.md
├── src/
│   └── doc_for_agent/
│       ├── scripts/
│       ├── references/
│       └── assets/
├── doc-for-agent/
│   ├── SKILL.md
│   ├── agents/
│   ├── scripts/
│   └── references/
├── .claude/
│   └── skills/
│       └── doc-for-agent/
├── scripts/
│   └── sync_platform_adapters.py
├── docs/
└── cli/
```

## Install As a Codex Skill

If you already use Codex local skills, install this skill into `~/.codex/skills/`.

One approach is to symlink it:

```bash
ln -sfn /absolute/path/to/doc-for-agent /Users/$USER/.codex/skills/doc-for-agent
```

After installation, restart Codex so the skill is discovered in a new session.

You can also use the bundled CLI installer:

```bash
python3 cli/docforagent.py init --ai codex
```

## Install From GitHub

If you want to install this skill from the published repository, use the Codex skill installer against this repo path:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Timcai06/Doc-For-Agent-skill \
  --path doc-for-agent
```

After installation, restart Codex so the new skill is loaded in future sessions.

## Install For Claude-Style Skills

From the target project directory:

```bash
python3 /absolute/path/to/DocForAgent_skill/cli/docforagent.py init --ai claude
```

This installs the Claude adapter into:

```text
.claude/skills/doc-for-agent
```

## CLI

The minimal distribution CLI currently supports:

```bash
python3 cli/docforagent.py init --ai codex
python3 cli/docforagent.py init --ai claude
python3 cli/docforagent.py init --ai cursor
python3 cli/docforagent.py init --ai continue
python3 cli/docforagent.py init --ai windsurf
python3 cli/docforagent.py init --ai all
python3 cli/docforagent.py sync
python3 cli/docforagent.py doctor
```

You can also install the CLI as a Python package:

```bash
pipx install /absolute/path/to/DocForAgent_skill
docforagent doctor
```

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
- Classify repository type before applying documentation structure
- Distinguish confirmed facts, inferences, and open questions for safer agent consumption
- Make new projects easier to onboard for coding agents
- Scan the current codebase and prefill useful content instead of generating empty templates
- Support refreshing existing `AGENTS/` docs when the repository evolves

## Verify

Run the generator regression checks against the bundled fixtures:

```bash
python3 doc-for-agent/tests/verify_generator_snapshots.py
```

This verifies representative `skill-meta`, `web-app`, `cli-tool`, and `library-sdk` repository shapes and checks that `init` followed by `refresh` stays stable.

Sync the source-of-truth files into platform adapters after changing shared generator logic:

```bash
python3 scripts/sync_platform_adapters.py
```

## Publishing

This repository is suitable for publishing on GitHub as a reusable skill source. Other users can install the skill from the repo path once the repository is public.
