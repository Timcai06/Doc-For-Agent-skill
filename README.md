# doc-for-agent

`doc-for-agent` is a product CLI for bootstrapping and maintaining repository documentation for coding agents.

After install, users start from one global command surface: `docagent`.
Node and Python distributions both converge on the same product flow (`docagent init --ai ...`).

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

## Repository Layout

```text
DocForAgent_skill/
├── README.md
├── LICENSE
├── pyproject.toml
├── setup.py
├── MANIFEST.in
├── package.json
├── .gitignore
└── doc-for-agent/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── scripts/
    │   ├── init_agents_docs.py
    │   ├── render_platform_adapter.py
    │   └── doc_for_agent_generator/
    │       ├── analysis.py
    │       ├── builders.py
    │       ├── markdown.py
    │       ├── models.py
    │       └── utils.py
    ├── installer/
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── docagent.py
    │   ├── sync_assets.py
    │   ├── node/
    │   │   └── docagent.js
    │   └── assets/
    │       ├── scripts/
    │       ├── templates/
    │       ├── references/
    │       └── agents/
    ├── templates/
    │   ├── base/
    │   │   ├── skill-content.md
    │   │   └── workflow-content.md
    │   ├── product.json
    │   └── platforms/
    │       ├── claude.json
    │       ├── codex.json
    │       ├── continue.json
    │       └── copilot.json
    ├── tests/
    │   ├── fixtures/
    │   │   ├── backend_service/
    │   │   ├── cli_tool/
    │   │   ├── hybrid_skill_cli/
    │   │   ├── library_sdk/
    │   │   ├── skill_meta/
    │   │   └── web_app/
    │   ├── unit/
    │   │   ├── test_classification.py
    │   │   ├── test_dry_run.py
    │   │   └── test_markdown.py
    │   ├── snapshots.json
    │   └── verify_generator_snapshots.py
    └── references/
        ├── agent-doc-migration-blueprint.md
        ├── agents-structure.md
        ├── layered-agents-blueprint.md
        └── multi-platform-distribution-blueprint.md
```

Current structure on `main` is intentionally simple:

- `doc-for-agent/` is the source of truth for the reusable Codex skill.
- `doc-for-agent/agents/openai.yaml` is the manifest shipped with installed adapters.
- `doc-for-agent/scripts/doc_for_agent_generator/` contains the modular generator core for analysis, content building, merge logic, and shared models.
- `doc-for-agent/installer/docagent.py` is the product CLI entrypoint (`docagent`) for install, doctor, update, and generation flows.
- `doc-for-agent/installer/node/docagent.js` is the npm/npx thin wrapper for Node-first installation paths.
- `doc-for-agent/installer/assets/` is the packaged runtime bundle used when `docagent` is installed from wheel/sdist.
- `doc-for-agent/installer/sync_assets.py` syncs source-of-truth runtime files into `installer/assets/` before packaging/release.
- `doc-for-agent/templates/product.json` carries product metadata used by the installer and install receipts.
- `doc-for-agent/templates/platforms/*.json` defines the platform-specific install surface for Codex, Claude Code, Continue, and Copilot.
- `doc-for-agent/tests/fixtures/` contains eight representative sample repositories used by the snapshot regression test.
- `doc-for-agent/tests/unit/` contains focused unit tests for classification, markdown merge behavior, dry-run behavior, platform adapters, and installer CLI behavior.
- Root `AGENTS/`, `dist/`, and `*.egg-info` outputs are local/generated artifacts and are ignored.
- `src/doc_for_agent/` is currently treated as a local packaging experiment on `main`, not the canonical implementation tree.

Two structure notes are worth keeping explicit:

- root packaging files such as `pyproject.toml`, `setup.py`, and `MANIFEST.in` belong to the product-distribution layer, not the AGENTS-generation engine itself
- `doc-for-agent/installer/assets/` is a packaged runtime mirror for installed `docagent` builds; day-to-day source changes should still start from `scripts/`, `templates/`, `references/`, and `agents/`

This keeps the default branch easier to reason about before splitting work across multiple `git worktree` directories.

## Install With the Product CLI

`docagent` is the single product CLI. Install from either ecosystem, then use the same command surface.

Recommended path by user type:

- Node users: start with `npx -y doc-for-agent` (one-off) or `npm install -g doc-for-agent` (global).
- Python users: start with `pipx install doc-for-agent`, then fallback to `python3 -m pip install doc-for-agent`.

### Install Matrix

| User profile | Install path | Product first run |
| --- | --- | --- |
| Node-first (one-off) | `npx -y doc-for-agent` | `npx -y doc-for-agent init --ai all --target /path/to/repo` |
| Node-first (global) | `npm install -g doc-for-agent` | `docagent init --ai all --target /path/to/repo` |
| Python-first (recommended) | `pipx install doc-for-agent` | `docagent init --ai all --target /path/to/repo` |
| Python-first (venv/system) | `python3 -m pip install doc-for-agent` | `docagent init --ai all --target /path/to/repo` |

### Product Quick Start

```bash
docagent init --ai all --target /path/to/repo
docagent doctor --target /path/to/repo
docagent versions --target /path/to/repo
```

Single-platform onboarding:

```bash
docagent init --ai codex --target /path/to/repo
docagent init --ai claude --target /path/to/repo
docagent init --ai continue --target /path/to/repo
docagent init --ai copilot --target /path/to/repo
```

### Unified Command Surface

Primary product entry:

```bash
docagent init --ai codex|claude|continue|copilot|all --target /path/to/repo
```

Operations:

```bash
docagent doctor --target /path/to/repo
docagent versions --target /path/to/repo
docagent update --target /path/to/repo
docagent refresh --root /path/to/repo
docagent generate --root /path/to/repo --mode refresh
docagent quickstart --target /path/to/repo
docagent --version
```

Backward compatibility is preserved:

```bash
docagent install --platform codex --target /path/to/repo
docagent all --target /path/to/repo
```

### Python vs Node Distribution

Each install writes a self-contained bundle under the platform's hidden folder:

- Codex: `.codex/skills/doc-for-agent/`
- Claude Code: `.claude/skills/doc-for-agent/`
- Continue: `.continue/skills/doc-for-agent/`
- Copilot: `.github/prompts/doc-for-agent/`

The installed bundle includes:

- the rendered `SKILL.md`
- generator scripts
- platform templates
- references
- agent manifests
- the installer itself
- an `INSTALLATION.json` receipt with platform and version metadata

The current product metadata lives in `doc-for-agent/templates/product.json`, so the installer and the installed bundle share one version source.

Distribution relation:

- Python package (`pipx` / `pip`) ships the core runtime bundle and full CLI.
- npm package (`npm` / `npx`) is a thin wrapper that forwards to the bundled Python `docagent`.
- Core engine logic stays in Python; Node is an adoption entrypoint, not a forked implementation.
- Node and Python users see one shared product story: `docagent init --ai ...` first, then doctor/version/update/refresh.

### Platform Matrix

| Platform | Adapter type | Install target |
| --- | --- | --- |
| Codex | skill (`SKILL.md`) | `.codex/skills/doc-for-agent/` |
| Claude Code | skill (`SKILL.md`) | `.claude/skills/doc-for-agent/` |
| Continue | skill (`SKILL.md`) | `.continue/skills/doc-for-agent/` |
| GitHub Copilot | prompt (`PROMPT.md`) | `.github/prompts/doc-for-agent/` |

### Release Prep

Before publishing to PyPI/npm, run:

```bash
python3 doc-for-agent/installer/sync_assets.py
python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
python3 doc-for-agent/tests/verify_generator_snapshots.py
python3 -m pip wheel . -w /tmp/docagent-wheel-check
npm pack --dry-run
```

Recommended install flow:

```bash
docagent doctor --target /path/to/repo
docagent all --target /path/to/repo
docagent versions --target /path/to/repo
docagent update --target /path/to/repo
```

Source checkout fallback (without package install) is still available:

```bash
python3 doc-for-agent/installer/docagent.py doctor --target /path/to/repo
```

When updating source files under `scripts/`, `templates/`, `references/`, or `agents/`, sync the packaged runtime bundle with:

```bash
python3 doc-for-agent/installer/sync_assets.py
```

## Install As a Codex Skill

If you already use Codex local skills and want a manual install into `~/.codex/skills/`, symlinking still works:

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
