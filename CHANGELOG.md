# Changelog

All notable changes to this project should be documented in this file.

The format is inspired by Keep a Changelog and this project uses semantic versioning as a practical release guide.

## [0.1.0] - 2026-03-25

### Added

- agent-first AGENTS generator with repository-type detection
- fixture-based regression verification for generated AGENTS docs
- explicit manual preservation blocks for refresh workflows
- platformized repository structure with shared source-of-truth under `src/doc_for_agent/`
- multi-platform adapters for Codex, Claude, Cursor, Continue, and Windsurf
- installer CLI with `init`, `sync`, `doctor`, `targets`, and version output
- Python packaging for `pipx`-style installation
- template/config-driven platform adapter generation
