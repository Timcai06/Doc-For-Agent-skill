# doc-for-agent

Use this skill when the user wants to initialize or refresh an `AGENTS/` directory for a repository so future coding agents can work against a stable, project-specific documentation structure.

This `doc-for-agent/` folder is the Codex adapter package. Shared logic is maintained under `src/doc_for_agent/` and synced here for distribution compatibility.

## What This Skill Produces

This skill generates a pragmatic `AGENTS/` directory with these files:

- `AGENTS/product.md`
- `AGENTS/architecture.md`
- `AGENTS/frontend.md`
- `AGENTS/backend.md`
- `AGENTS/workflows.md`
- `AGENTS/glossary.md`
- `AGENTS/README.md`

The generated docs are prefilled from the real repository structure. They are not generic placeholders only.
They should help future agents act with lower ambiguity, not just read a prettier summary.

## When To Use

Trigger this skill when the user asks to:

- create an `AGENTS` directory
- bootstrap coding-agent docs for a new project
- generate reusable project docs for future agent work
- standardize agent-facing docs across repos
- refresh or rewrite an existing `AGENTS/` directory from the latest codebase

Do not use this skill for normal feature work unless the user explicitly wants agent documentation.

## Workflow

### Step 1: Inspect the repository root

Before generating files, quickly inspect:

- top-level folders
- frontend/backend or app/server structure
- package manager / Python / framework hints

Use that to infer:

- project name
- repository type
- likely product purpose
- likely frontend stack
- likely backend stack

### Step 2: Generate or refresh the AGENTS directory

Run:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --mode refresh
```

If the user gives a project name, also pass:

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root "<repo-root>" --project-name "<name>" --mode refresh
```

### Step 3: Let the script prefill from the actual codebase

The script will scan and prefill from:

- repository README
- repository type signals such as skill markers, CLI entrypoints, package shape, and frontend/backend structure
- frontend routes
- frontend package scripts
- backend endpoints
- storage behavior
- result contract fields
- canonical terminology hints
- existing `AGENTS/` section content when running in `refresh` mode

### Step 4: Review and tighten the generated docs

After generation, review the docs and tighten the parts the script cannot infer well:

- product purpose and target users
- domain-specific constraints
- ownership boundaries
- any project-specific naming rules
- any manual sections you want to preserve long term; `refresh` now keeps useful existing section bodies where possible
- any sections still marked as facts vs. inferences vs. open questions
- any hand-maintained blocks wrapped with `<!-- doc-for-agent:manual-start -->` and `<!-- doc-for-agent:manual-end -->`

### Step 5: Keep it lean

These docs are for coding agents, not human marketing docs.

Prefer:

- confirmed facts over confident guesses
- constraints
- real commands
- route structure
- response contract notes
- naming conventions
- file ownership hints
- task-oriented handoff guidance

Avoid:

- long narrative prose
- duplicated README content
- aspirational future-state plans unless the user explicitly wants them

## Reference

For the intended file purposes and writing style, see:

- `references/agents-structure.md`
