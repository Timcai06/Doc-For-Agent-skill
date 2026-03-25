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
    │   └── docagent.py
    ├── templates/
    │   ├── base/
    │   │   ├── skill-content.md
    │   │   └── workflow-content.md
    │   └── platforms/
    │       ├── claude.json
    │       ├── codex.json
    │       └── continue.json
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
        ├── agents-structure.md
        ├── layered-agents-blueprint.md
        └── multi-platform-distribution-blueprint.md
```

Current structure on `main` is intentionally simple:

- `doc-for-agent/` is the source of truth for the reusable Codex skill.
- `doc-for-agent/agents/openai.yaml` is the manifest shipped with installed adapters.
- `doc-for-agent/scripts/doc_for_agent_generator/` contains the modular generator core for analysis, content building, merge logic, and shared models.
- `doc-for-agent/installer/docagent.py` is the minimal Python installer CLI for repo-local adapter installs.
- `doc-for-agent/templates/platforms/*.json` defines the platform-specific install surface for Codex, Claude Code, and Continue.
- `doc-for-agent/tests/fixtures/` contains six representative sample repositories used by the snapshot regression test.
- `doc-for-agent/tests/unit/` contains focused unit tests for classification, markdown merge behavior, and CLI dry-run behavior.
- Root `AGENTS/`, `dist/`, and `*.egg-info` outputs are local/generated artifacts and are ignored.
- `src/doc_for_agent/` is currently treated as a local packaging experiment on `main`, not the canonical implementation tree.

This keeps the default branch easier to reason about before splitting work across multiple `git worktree` directories.

## Install With the Product CLI

The new minimal installer CLI gives `doc-for-agent` a cleaner distribution surface for repo-local assistant installs:

```bash
python3 doc-for-agent/installer/docagent.py doctor --target /path/to/repo
python3 doc-for-agent/installer/docagent.py install --platform codex --target /path/to/repo
python3 doc-for-agent/installer/docagent.py install --platform claude --target /path/to/repo
python3 doc-for-agent/installer/docagent.py install --platform continue --target /path/to/repo
```

Use `--platform all` to install every supported adapter in one pass:

```bash
python3 doc-for-agent/installer/docagent.py install --platform all --target /path/to/repo
```

Each install writes a self-contained bundle under the platform's hidden folder:

- Codex: `.codex/skills/doc-for-agent/`
- Claude Code: `.claude/skills/doc-for-agent/`
- Continue: `.continue/skills/doc-for-agent/`

The installed bundle includes the rendered `SKILL.md`, generator scripts, templates, references, agent manifests, and the installer itself.

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

Preview the file plan without writing anything:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --mode refresh --dry-run
```

Generate the BDI-style layered topology for long-lived or phase-driven projects:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/repo --mode refresh --profile layered
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

- `doc-for-agent/references/layered-agents-blueprint.md`
- `doc-for-agent/references/multi-platform-distribution-blueprint.md`

That blueprint captures a likely future direction for the skill:

- keep the current bootstrap profile for fast onboarding
- add a layered profile for long-lived, phase-driven projects
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
