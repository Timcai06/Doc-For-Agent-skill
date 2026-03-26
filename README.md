# doc-for-agent

`doc-for-agent` is a product CLI for people who work inside coding-agent terminals such as Claude Code, Codex, CodeBuddy, Continue, and similar CLI-first agent workflows.

It helps a repository grow a documentation system that both humans and agents can use:

- `AGENTS/` for coding-agent execution, handoff, and repo guidance
- `docs/` for maintainers and teammates who need a durable project map

After install, every user starts from one global command surface: `docagent`.
Node and Python distributions both converge on the same product flow: `docagent init --ai ...`.

## Quick Start

### Install Once

Node users:

```bash
npm install -g doc-for-agent
```

Python users:

```bash
pipx install doc-for-agent
```

### Start In 30 Seconds

Pick your coding agent, then run one command:

```bash
docagent init --ai claude --target /path/to/repo
docagent init --ai codex --target /path/to/repo
docagent init --ai copilot --target /path/to/repo
docagent init --ai continue --target /path/to/repo
docagent init --ai all --target /path/to/repo
```

Then refresh the repository docs:

```bash
docagent refresh --root /path/to/repo --output-mode agent
```

If you do not want a global install:

```bash
npx -y doc-for-agent
```

That opens the same `docagent` product flow through the Node entrypoint.

## Choose Your Agent

Use the same product CLI, but start from the platform you actually use:

| If you use... | Start with... |
| --- | --- |
| Claude Code | `docagent init --ai claude --target /path/to/repo` |
| Codex | `docagent init --ai codex --target /path/to/repo` |
| Continue | `docagent init --ai continue --target /path/to/repo` |
| GitHub Copilot | `docagent init --ai copilot --target /path/to/repo` |
| Multiple assistants | `docagent init --ai all --target /path/to/repo` |

## What You Get

After `init` and `refresh`, the repository can gain:

- `AGENTS/` for coding-agent execution, repo guidance, handoff, and working rules
- `docs/` for maintainers who need overview, architecture, workflows, and glossary docs

This is especially useful when a repo has:

- no project docs yet
- thin or outdated docs
- scattered docs across `README`, `docs/`, `specs/`, `plan/`, or `notes/`
- old flat `AGENTS` that should be migrated into a better structure

## Who It Is For

`doc-for-agent` is built for repository owners who:

- use coding agents from a terminal or CLI workflow
- want a repeatable project-doc setup for Claude Code, Codex, CodeBuddy, Continue, Copilot, and similar tools
- need help when a repo has no docs, thin docs, messy docs, or old flat `AGENTS`
- want one CLI to install platform adapters and keep docs refreshed over time

## What It Does

At its core, `docagent` does two jobs:

1. Install the right assistant-facing adapter for your chosen platform.
2. Generate or refresh a documentation system for the target repository.

On the agent side, it creates or refreshes an `AGENTS/` directory with:

- `AGENTS/README.md`
- `AGENTS/product.md`
- `AGENTS/architecture.md`
- `AGENTS/frontend.md`
- `AGENTS/backend.md`
- `AGENTS/workflows.md`
- `AGENTS/glossary.md`

On the maintainer side, it can also generate a minimal `docs/` set:

- `docs/overview.md`
- `docs/architecture.md`
- `docs/workflows.md`
- `docs/glossary.md`

The generated files are prefilled from the actual repository structure, routes, scripts, backend contract clues, and supporting docs, then intended to be refined further where needed.

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
- it can now move toward a layered `AGENTS/` operating model instead of treating flat bootstrap output as the only long-term shape

Recent quality improvements also make output more directly usable:

- repo-type detection now treats `package.json` `bin` metadata as a first-class CLI signal
- repo-type detection now keeps strong app envelopes (`frontend + backend` / workspace) from being misclassified as CLI-only repos
- architecture docs now infer source-of-truth files based on repo type (workspace config, manifests, entrypoints, runtime roots)
- workflows prefer executable fallback guidance over placeholder TODO lines
- `--explain` now includes a suggested profile (`bootstrap` or `layered`), a copyable refresh command, and a source-of-truth quick list
- layered generation now synthesizes supporting docs into agent-facing `confirmed / conflicting / unresolved` guidance instead of only listing reference paths
- human docs generation now emits `overview/architecture/workflows/glossary` with the same synthesis model plus explicit provenance sections
- human docs now include maintainer-facing structure (audience, system map, operational notes, documentation gaps) so low-doc repos still get actionable baseline docs
- human docs now separate `confirmed / inferred / unresolved` signals and add a maintenance workflow + bootstrap backlog section so teams can keep docs alive after first generation
- human docs now express evidence as a natural `Knowledge Status` section and include explicit `Update Triggers`, reducing template feel while improving long-term maintainability

## Core Workflow

Most users only need three commands:

```bash
docagent init --ai codex|claude|continue|copilot|all --target /path/to/repo
docagent doctor --target /path/to/repo
docagent refresh --root /path/to/repo --output-mode agent|human|dual
```

That maps to a simple lifecycle:

- `init`: install the right platform adapter into the repository
- `doctor`: verify what is installed and where
- `refresh`: generate or update repository docs from the current codebase and existing docs

Use `generate` when you want more explicit control over mode, profile, and output shape.

## Why It Is Different

`doc-for-agent` is not just a platform installer.

It combines:

- platform setup for coding-agent tools
- repository analysis
- doc migration (`initialize / migrate / refresh`)
- dual output for both `AGENTS/` and maintainers' `docs/`

That means the product is useful both when a repo already has messy documentation and when a repo barely has any documentation at all.

## Maintainer Docs

If you want the repository internals rather than the product entry flow, use:

- [Quickstart](/Users/tim/DocForAgent_skill/docs/quickstart.md)
- [Platform Guide](/Users/tim/DocForAgent_skill/docs/platforms.md)
- [Maintainer Guide](/Users/tim/DocForAgent_skill/docs/maintainers.md)

## Install Paths

Use the path that matches how you normally work:

| User profile | Install path | Start command |
| --- | --- | --- |
| Node-first (global) | `npm install -g doc-for-agent` | `docagent init --ai all --target /path/to/repo` |
| Node-first (one-off) | `npx -y doc-for-agent` | `npx -y doc-for-agent init --ai all --target /path/to/repo` |
| Python-first (recommended) | `pipx install doc-for-agent` | `docagent init --ai all --target /path/to/repo` |
| Python-first (venv/system) | `python3 -m pip install doc-for-agent` | `docagent init --ai all --target /path/to/repo` |

Detailed guides:

- [Quickstart](/Users/tim/DocForAgent_skill/docs/quickstart.md)
- [Platform Guide](/Users/tim/DocForAgent_skill/docs/platforms.md)

## Platform Targets

| Platform | Adapter type | Install target |
| --- | --- | --- |
| Codex | skill (`SKILL.md`) | `.codex/skills/doc-for-agent/` |
| Claude Code | skill (`SKILL.md`) | `.claude/skills/doc-for-agent/` |
| Continue | skill (`SKILL.md`) | `.continue/skills/doc-for-agent/` |
| GitHub Copilot | prompt (`PROMPT.md`) | `.github/prompts/doc-for-agent/` |

## Product CLI v1

Primary commands:

```bash
docagent init --ai codex|claude|continue|copilot|all --target /path/to/repo
docagent doctor --target /path/to/repo
docagent refresh --root /path/to/repo --output-mode agent|human|dual
docagent generate --root /path/to/repo --mode refresh --output-mode human|agent|dual
docagent update --target /path/to/repo
docagent versions --target /path/to/repo
```

Utility command:

```bash
docagent quickstart --target /path/to/repo
```

Legacy compatibility commands are still available, but they are no longer the main path:

```bash
docagent install --platform codex --target /path/to/repo
docagent all --target /path/to/repo
```

## Packaging Model

The product is intentionally distributed through two user-facing paths:

- Python package: canonical runtime and full CLI
- npm package: thin Node launcher for Node-first users

Both converge on the same product command surface: `docagent`.

## Release Checklist

Before publishing to PyPI or npm:

```bash
python3 doc-for-agent/installer/sync_assets.py
python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
python3 doc-for-agent/tests/verify_generator_snapshots.py
python3 -m pip wheel . -w /tmp/docagent-wheel-check
npm pack --dry-run
```

Source checkout fallback (without package install) is still available:

```bash
python3 doc-for-agent/installer/docagent.py doctor --target /path/to/repo
```

## Advanced Use

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

The engine now also accepts `--mode migrate` and `--mode generate` so product-level CLIs can map user intents to stable engine actions without re-implementing internal wiring.

Preview the file plan without writing anything:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --mode refresh --dry-run
```

Generate the BDI-style layered topology for long-lived or phase-driven projects:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --mode refresh --profile layered
```

Generate human-oriented project docs only:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --mode refresh --output-mode human
```

Generate both AGENTS docs and human docs in one run:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --mode refresh --output-mode dual
```

Render the current platform adapter scaffold into a project-local assistant folder:

```bash
python3 doc-for-agent/scripts/render_platform_adapter.py --platform codex --target /path/to/repo
python3 doc-for-agent/scripts/render_platform_adapter.py --platform claude --target /path/to/repo
python3 doc-for-agent/scripts/render_platform_adapter.py --platform continue --target /path/to/repo
```

Force a repo type when auto-detection is ambiguous:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --mode refresh --repo-type cli-tool
```

Explain the classification signals and reasoning before writing:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --mode refresh --explain
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

## Blueprint

The current shipped output is still the lean flat profile, but the repository now also carries a next-step design reference for a more durable, BDI-inspired layered `AGENTS/` topology:

- `doc-for-agent/references/agent-doc-migration-blueprint.md`
- `doc-for-agent/references/layered-agents-blueprint.md`
- `doc-for-agent/references/multi-platform-distribution-blueprint.md`

That blueprint captures a likely future direction for the skill:

- keep the current bootstrap profile for fast onboarding
- add a layered profile for long-lived, phase-driven projects
- normalize messy or legacy agent docs into one canonical layered `AGENTS/` root
- introduce entry, execution, and memory docs as first-class agent primitives
- separate the engine from platform adapters so the product can ship beyond Codex

## Verify

Run the focused unit tests first:

```bash
python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
```

Then run the generator regression checks against the bundled fixtures:

```bash
python3 doc-for-agent/tests/verify_generator_snapshots.py
```

This now verifies representative `skill-meta`, `hybrid skill + CLI`, `backend service`, `web-app`, `cli-tool`, and `library-sdk` repository shapes and checks that `init` followed by `refresh` stays stable.

## Publishing

This repository now has the beginnings of a product distribution shape:

- the engine stays Python-first
- platform adapters are template-driven
- installs produce self-contained bundles
- the installer exposes a clear `doctor` / `install` surface

The next likely packaging step is a publishable Python entrypoint so `docagent` can be installed directly with `pipx` or `uv tool install`.
