# AGENTS Entry

## Purpose

- Define the reading order before an agent changes code or docs
- State the operating rules that should survive session resets
- Point future agents at the repository's canonical fact sources

## Reading Order

- ``01-product/001-core-goals.md``
- ``01-product/002-prd.md``
- ``02-architecture/004-tech-stack.md``
- ``01-product/003-app-flow.md``
- ``02-architecture/006-backend-structure.md``
- ``02-architecture/005-frontend-guidelines.md``
- ``02-architecture/007-architecture-compatibility.md``
- ``03-execution/008-implementation-plan.md``
- ``04-memory/009-progress.md``
- ``04-memory/010-lessons.md``

## Rules

- Read product and architecture docs before broad refactors.
- Refresh `AGENTS/` after meaningful repo-shape, workflow, or terminology changes.
- Prefer confirmed facts over speculative roadmap language.
- Protect hand-maintained notes with manual blocks when refresh safety matters.
- Keep the skill manifest, SKILL.md instructions, and generator behavior aligned.

## Current Operating Posture

- Keep the skill definition, generator behavior, and generated documentation in sync.

## Canonical Fact Sources

- `README.md`
- `docs/landing-page.md`
- `docs/landing-page.zh.md`
- `docs/maintainers.md`
