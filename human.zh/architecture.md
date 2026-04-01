# Architecture

## Source Of Truth

- `README.md` for stated project goals, setup expectations, and user-facing examples
- `doc-for-agent/SKILL.md` for trigger conditions and maintainer workflow
- `doc-for-agent/agents/openai.yaml` for launcher/marketplace invocation metadata
- `doc-for-agent/scripts/` for generation behavior and repository scanning
- `doc-for-agent/references/` for documentation structure and writing constraints

## Top Rules (Read First)

- Rule 1: CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Rule 2: Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Rule 3: Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.

## Document Contract

- This page is maintainer-facing source-of-truth for its domain; keep it synchronized with `AGENTS/` in dual mode and `human.zh/` as the human-view root.
- Update this page in the same PR as behavior changes; avoid narrative-only refreshes without command or contract changes.
- Resolve source-of-truth conflicts before editing CLI, adapter, or build-path behavior.

## Dual Sync Checklist

- After edits, refresh in dual mode and verify both `AGENTS/` and `human.zh/` were updated in the same change set.
- If one side changed without the other, treat it as documentation drift and resolve before merge.
- When source-of-truth files move, update references in both doc systems before adjusting adapter/build-path rules.

## Paired Refresh Rules

- Refresh contract: run one refresh/generate action that updates paired views together; do not patch one locale/audience in isolation.
- Path contract: verify changed files include both `AGENTS*/` and `docs*/` counterparts when behavior changes affect shared source-of-truth.
- Quad-mode contract: when using `--output-mode quad`, validate all four roots (`AGENTS/`, `AGENTS.zh/`, `docs/`, `docs.zh/`) in the same review cycle.
- Architecture pairing rule: if `human.zh/architecture.md` changes due to boundary/source-of-truth updates, refresh paired architecture paths under both AGENTS roots.

## Dual Pairing Contract (Rules)

- Pairing mode rule: in `dual`, human and agent docs are generated from one analysis pass and must be reviewed as one change set.
- Locale-output rule: human locale `zh` maps to `human.zh/`.
- Template rule: human template variant `paired-core` is part of the pairing contract and must remain consistent across paired docs.
- Path pair rule: `human.zh/architecture.md` pairs with `AGENTS/02-architecture/004-tech-stack.md` for stack facts and platform anchors.
- Path pair rule: `human.zh/architecture.md` pairs with `AGENTS/02-architecture/007-architecture-compatibility.md` for source-of-truth and compatibility rules.

## Paired Agent Docs (Dual Mode)

- `AGENTS/02-architecture/004-tech-stack.md` for stack facts and platform anchors.
- `AGENTS/02-architecture/007-architecture-compatibility.md` for source-of-truth and compatibility rules.

## Output Boundary (Human vs Agent)

- Use `human.zh/` for maintainer-facing policy and decisions; use `AGENTS/` for execution order, command wiring, and handoff runbooks.
- If a change affects both reader types, update both systems in one dual refresh cycle instead of patching only one side.
- Keep architecture rationale in `human.zh/architecture.md`; keep CLI/build/source-of-truth guardrails in `AGENTS/architecture.md` (or layered architecture docs).

## Dual View Rationale

- `human.zh/` and `AGENTS/` are two views generated from the same repository analysis and source-of-truth anchors.
- When the two views diverge, treat it as refresh drift rather than independent documentation authority.
- Architecture rationale lives in `human.zh/architecture.md`, while operational boundaries for agents live in paired AGENTS architecture docs.

## Detected Signals

- Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).

## System Map

- No system map details were detected automatically.

## Synthesis Summary

- Sources analyzed: `3`
- Synthesized statements: `5` confirmed, `0` conflicting, `0` unresolved

## Knowledge Status

### Confirmed Rules

- CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.
- Conflict handling order: 1) check `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md`; 2) then edit adapter/config mappings.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。

### Supporting Signals

- No additional derived architecture signals were detected from repository structure.

### Decision Backlog

- No unresolved architecture items were synthesized from supporting docs.

### Conflict Watchlist

- No direct architecture conflicts were synthesized from supporting docs.

## Stability Boundaries

- Treat source-of-truth files as canonical when supporting docs disagree.
- Refresh both `docs/` and `AGENTS/` after architecture-impacting changes.

## Update Triggers

- When source-of-truth files, service boundaries, or runtime dependencies change, update this page.
- When integration contracts change (routes/endpoints/storage), refresh architecture notes in the same PR.

## Maintenance Workflow

- Assign one maintainer owner for this document and update it in the same pull request as behavior changes.
- Review this document at least once per sprint or before each release cut.
- Update after boundary, dependency, or interface contract changes.
- No major synthesis conflicts were detected; focus on keeping this page current with implementation changes.

## Bootstrap Backlog (When Docs Are Thin)

- Supporting docs were found; continue consolidating them into this page and archive stale duplicates.

## Provenance

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`

## Preserved Notes

- 核心护栏与顶层规则 (首读必看)
  - Preserved from previous manual edits.
  - 第一原则： CLI 交互边界： keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
  - 第二原则： 真相源边界： on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
  - 第三原则： 分发结构： keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.
- 文档与执行层契约
  - Preserved from previous manual edits.
  - 本页面是该领域面向维护者的真相源; 保持其在双重模式下与 `AGENTS/` 的同步 and `human.zh/` 作为人类视角的根目录.
  - 在代码行为变更的同一个 PR 中同步更新此页面; 避免在没有命令或契约更改的情况下进行纯叙述性的刷新.
  - Resolve source-of-truth conflicts before editing CLI, adapter, or build-path behavior.
- 双重视图对齐检查清单
  - Preserved from previous manual edits.
  - After edits, refresh in dual mode and verify both `AGENTS/` and `human.zh/` were updated in the same change set.
  - If one side changed without the other, treat it as documentation drift and resolve before merge.
  - When source-of-truth files move, update references in both doc systems before adjusting adapter/build-path rules.
- Quad模式下的同步规则
  - Preserved from previous manual edits.
  - Refresh contract: run one refresh/generate action that updates paired views together; do not patch one locale/audience in isolation.
  - Path contract: verify changed files include both `AGENTS*/` and `docs*/` counterparts when behavior changes affect shared source-of-truth.
  - Quad-mode contract: when using `--output-mode quad`, validate all four roots (`AGENTS/`, `AGENTS.zh/`, `docs/`, `docs.zh/`) in the same review cycle.
  - Architecture pairing rule: if `human.zh/architecture.md` changes due to boundary/source-of-truth updates, refresh paired architecture paths under both AGENTS roots.
- 双视图强制对齐契约
  - Preserved from previous manual edits.
  - Pairing mode rule: in `dual`, human and agent docs are generated from one analysis pass and must be reviewed as one change set.
  - Locale-output rule: 中文语言包 `zh` 映射至 `human.zh/` 目录.
  - Template rule: human template variant `paired-core` is part of the pairing contract and must remain consistent across paired docs.
  - 路径对齐规则：`human.zh/architecture.md` 与 `AGENTS/02-architecture/004-tech-stack.md` 结对，用于 stack facts and platform anchors.
  - 路径对齐规则：`human.zh/architecture.md` 与 `AGENTS/02-architecture/007-architecture-compatibility.md` 结对，用于 source-of-truth and compatibility rules.
- 边界定义：人读区 vs 机读区
  - Preserved from previous manual edits.
  - Use `human.zh/` for maintainer-facing policy and decisions; use `AGENTS/` for execution order, command wiring, and handoff runbooks.
  - If a change affects both reader types, update both systems in one dual refresh cycle instead of patching only one side.
  - Keep architecture rationale in `human.zh/architecture.md`; keep CLI/build/source-of-truth guardrails in `AGENTS/architecture.md` (or layered architecture docs).
- 双向视图设计逻辑
  - Preserved from previous manual edits.
  - `human.zh/` and `AGENTS/` are two views generated from the same repository analysis and source-of-truth anchors.
  - When the two views diverge, treat it as refresh drift rather than independent documentation authority.
  - 架构设计逻辑存放于 `human.zh/architecture.md`, 而针对智能体的运行边界规则存放于配套的 AGENTS 架构文档中.
- 全局上下文提炼
  - Preserved from previous manual edits.
  - 已分析信源数量：`3`
  - 成功提炼结论：`5` 条确认，`0` 条矛盾，`0` 条未决
- 仓库知识健康度
  - Preserved from previous manual edits.
  ### 核心确立的规则库

  - CLI 交互边界： keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
  - 真相源边界： on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
  - 分发结构： keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.
  - Conflict handling order: 1) check `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md`; 2) then edit adapter/config mappings.
  - 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。

  ### 高价值辅助参考信号

  - No additional derived architecture signals were detected from repository structure.

  ### 尚未决策的高风险清单

  - 未检测到未决的架构项 .

  ### 矛盾与冲突预警监控

  - 未检测到直接的架构冲突 .
- 文档刷新触发条件
  - Preserved from previous manual edits.
  - When source-of-truth files, service boundaries, or runtime dependencies change, update this page.
  - When integration contracts change (routes/endpoints/storage), refresh architecture notes in the same PR.
- 文档日常维护流
  - Preserved from previous manual edits.
  - 为此文档分配一名维护责任人 and update it in the same pull request as behavior changes.
  - 每个 Sprint 至少评审一次此文档 or before each release cut.
  - Update after boundary, dependency, or interface contract changes.
  - 未检测到严重的规则提炼冲突; focus on keeping this page current with implementation changes.
- 冷启动阶段待办 (When Docs Are Thin)
  - Preserved from previous manual edits.
  - Supporting docs were found; continue consolidating them into this page and archive stale duplicates.
- 溯源证明
  - Preserved from previous manual edits.
  - `README.md`
  - `docs/platforms.md`
  - `docs/platforms.zh.md`
