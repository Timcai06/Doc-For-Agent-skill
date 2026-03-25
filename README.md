# Doc For Agent

`doc-for-agent` is a platformized skill for generating and refreshing an `AGENTS/` directory so coding agents can start from stable, repo-specific context instead of rediscovering a codebase from scratch.

It is built for teams using multiple agents across real repositories and wanting a shared, refreshable layer for product context, architecture notes, workflows, and canonical terminology.

## Why It Exists

Without an `AGENTS/` layer, every new agent has to re-infer:

- what kind of repository this is
- which files are canonical
- how to run or verify it
- which names and terms should stay stable
- what still needs human confirmation

`doc-for-agent` turns that repeated discovery work into a reusable project asset.

## What It Generates

The generator creates or refreshes:

- `AGENTS/README.md`
- `AGENTS/product.md`
- `AGENTS/architecture.md`
- `AGENTS/frontend.md`
- `AGENTS/backend.md`
- `AGENTS/workflows.md`
- `AGENTS/glossary.md`

The output is agent-first:

- repository type is classified before docs are written
- sections separate confirmed facts, inferences, and open questions
- refresh supports explicit manual preservation blocks
- docs are optimized for action and handoff, not just human prose

## Before / After

Before:

- a new agent explores the repo from scratch
- terminology and workflows drift between agents
- refreshes are manual and inconsistent

After:

- agents get a shared project map on entry
- core docs stay aligned with the real repo shape
- long-lived notes can survive refresh with manual markers

Manual preservation syntax:

```md
<!-- doc-for-agent:manual-start -->
Your hand-maintained notes here.
<!-- doc-for-agent:manual-end -->
```

## Quick Start

### Codex

```bash
python3 cli/docforagent.py init --ai codex
```

Default install path:

```text
~/.codex/skills/doc-for-agent
```

### Claude / Cursor / Continue / Windsurf

From the target project directory:

```bash
python3 /absolute/path/to/DocForAgent_skill/cli/docforagent.py init --ai claude
python3 /absolute/path/to/DocForAgent_skill/cli/docforagent.py init --ai cursor
python3 /absolute/path/to/DocForAgent_skill/cli/docforagent.py init --ai continue
python3 /absolute/path/to/DocForAgent_skill/cli/docforagent.py init --ai windsurf
```

### pipx

```bash
pipx install /absolute/path/to/DocForAgent_skill
docforagent doctor
```

## Supported Platforms

- Codex
- Claude-style local skills
- Cursor
- Continue
- Windsurf

The current repository is organized so one shared source of truth can feed multiple platform adapters.

## Product Layout

```text
DocForAgent_skill/
├── src/doc_for_agent/                # source of truth
├── doc-for-agent/                    # Codex adapter
├── .claude/skills/doc-for-agent/     # Claude adapter
├── .cursor/skills/doc-for-agent/     # Cursor adapter
├── .continue/skills/doc-for-agent/   # Continue adapter
├── .windsurf/skills/doc-for-agent/   # Windsurf adapter
├── cli/                              # installer CLI
├── scripts/                          # sync/build helpers
├── docs/                             # maintenance and release docs
└── .github/workflows/                # CI and release automation
```

Key rule:

- `src/doc_for_agent/` is the source of truth
- platform folders are generated or synchronized distribution surfaces

## CLI

Core commands:

```bash
python3 cli/docforagent.py init --ai codex
python3 cli/docforagent.py init --ai claude
python3 cli/docforagent.py init --ai cursor
python3 cli/docforagent.py init --ai continue
python3 cli/docforagent.py init --ai windsurf
python3 cli/docforagent.py init --ai all
python3 cli/docforagent.py sync
python3 cli/docforagent.py doctor
python3 cli/docforagent.py targets
python3 cli/docforagent.py --version
```

What they do:

- `init`: installs a platform adapter into a target environment
- `sync`: regenerates and syncs adapters from the source of truth
- `doctor`: checks repository integrity for packaging and installs
- `targets`: shows supported install targets and default paths

## Use It In Practice

Ask your agent something like:

- `Create an AGENTS directory for this repository using doc-for-agent`
- `Refresh this repo's AGENTS docs based on the real codebase`
- `Bootstrap agent-facing docs for this project`

You can also run the generator directly:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --mode refresh
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --project-name "My Project" --mode refresh
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --mode init
```

## Verification

Regression checks:

```bash
python3 doc-for-agent/tests/verify_generator_snapshots.py
```

Adapter regeneration:

```bash
python3 scripts/sync_platform_adapters.py
```

CLI health:

```bash
python3 cli/docforagent.py doctor
```

## Release Readiness

This repository now includes:

- centralized versioning
- changelog tracking
- CI verification
- release workflow automation
- buildable Python distribution artifacts

See:

- [CHANGELOG.md](/Users/tim/DocForAgent_skill/CHANGELOG.md)
- [release-workflow.md](/Users/tim/DocForAgent_skill/docs/release-workflow.md)
- [platform-architecture.md](/Users/tim/DocForAgent_skill/docs/platform-architecture.md)

## Design Goals

- keep agent-facing docs lean and executable
- classify repository shape before writing docs
- preserve high-signal human knowledge across refreshes
- support multi-agent handoff and shared terminology
- make packaging and installation explicit across platforms
