# 系统架构与边界 Compatibility

## 核心护栏与顶层规则 (首读必看)

- 第一原则： CLI 交互边界： keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- 第二原则： 真相源边界： on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- 第三原则： 分发结构： keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.

## Repo-Type Signals

- Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).

## Source Of Truth

- `README.md` for stated project goals, setup expectations, and user-facing examples
- `doc-for-agent/SKILL.md` for trigger conditions and maintainer workflow
- `doc-for-agent/agents/openai.yaml` for launcher/marketplace invocation metadata
- `doc-for-agent/scripts/` for generation behavior and repository scanning
- `doc-for-agent/references/` for documentation structure and writing constraints

## 辅助参考文档提炼 (Architecture)

### 已确认的基准主张

- CLI 交互边界： keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- 真相源边界： on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- 分发结构： keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.
- Conflict handling order: 1) check `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md`; 2) then edit adapter/config mappings.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 

### 待清理的矛盾点

- 未检测到直接的架构冲突 .

### 悬而未决的问题

- 未检测到未决的架构项 .

## Referenced Architecture Docs

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`

## Compatibility Boundaries

- Prefer changing source code and configuration first, then refresh `AGENTS/` docs.
- Do not let generated docs drift away from the repository's actual entrypoints and workflows.
- Skill manifests, README examples, and generator output should describe the same capability surface.

## Conflicting Signals

- Skill markers dominate classification, but packaged tooling signals suggest this repository may also ship installable utilities.
