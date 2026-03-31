<!-- @Agent: This is an automatically generated structural skeleton in English. Please translate the entire content below into professional Chinese (zh-CN) immediately, while preserving all markdown formatting, file names, and code blocks. -->

## Source Of Truth

- `README.md` for stated project goals, setup expectations, and user-facing examples
- `doc-for-agent/SKILL.md` for trigger conditions and maintainer workflow
- `doc-for-agent/agents/openai.yaml` for launcher/marketplace invocation metadata
- `doc-for-agent/scripts/` for generation behavior and repository scanning
- `doc-for-agent/references/` for documentation structure and writing constraints

## 核心护栏与顶层规则 (首读必看)

- 第一要则： CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- 第二要则： Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- 第三要则： Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.

## 文档与执行层契约

- This page is maintainer-facing source-of-truth for its domain; keep it synchronized with `AGENTS/` in dual mode and `human.zh/` as the human-view root.
- Update this page in the same PR as behavior changes; avoid narrative-only refreshes without command or contract changes.
- Resolve source-of-truth conflicts before editing CLI, adapter, or build-path behavior.

## 双重视图对齐检查清单

- After edits, refresh in dual mode and verify both `AGENTS/` and `human.zh/` were updated in the same change set.
- If one side changed without the other, treat it as documentation drift and resolve before merge.
- When source-of-truth files move, update references in both doc systems before adjusting adapter/build-path rules.

## Quad模式下的同步规则

- Refresh contract: run one refresh/generate action that updates paired views together; do not patch one locale/audience in isolation.
- Path contract: verify changed files include both `AGENTS*/` and `docs*/` counterparts when behavior changes affect shared source-of-truth.
- Quad-mode contract: when using `--output-mode quad`, validate all four roots (`AGENTS/`, `AGENTS.zh/`, `docs/`, `docs.zh/`) in the same review cycle.
- Architecture pairing rule: if `human.zh/architecture.md` changes due to boundary/source-of-truth updates, refresh paired architecture paths under both AGENTS roots.

## 双向绑定契约 (执行规则)

- Pairing mode rule: in `dual`, human and agent docs are generated from one analysis pass and must be reviewed as one change set.
- Locale-output rule: human locale `zh` maps to `human.zh/`.
- Template rule: human template variant `paired-core` is part of the pairing contract and must remain consistent across paired docs.
- Path pair rule: `human.zh/architecture.md` pairs with `AGENTS/02-architecture/004-tech-stack.md` for stack facts and platform anchors.
- Path pair rule: `human.zh/architecture.md` pairs with `AGENTS/02-architecture/007-architecture-compatibility.md` for source-of-truth and compatibility rules.

## 结对的 Agent 文档 (双向模式)

- `AGENTS/02-architecture/004-tech-stack.md` for stack facts and platform anchors.
- `AGENTS/02-architecture/007-architecture-compatibility.md` for source-of-truth and compatibility rules.

## 边界定义：人读区 vs 机读区

- Use `human.zh/` for maintainer-facing policy and decisions; use `AGENTS/` for execution order, command wiring, and handoff runbooks.
- If a change affects both reader types, update both systems in one dual refresh cycle instead of patching only one side.
- Keep architecture rationale in `human.zh/architecture.md`; keep CLI/build/source-of-truth guardrails in `AGENTS/architecture.md` (or layered architecture docs).

## 双重视图设计逻辑

- `human.zh/` and `AGENTS/` are two views generated from the same repository analysis and source-of-truth anchors.
- When the two views diverge, treat it as refresh drift rather than independent documentation authority.
- Architecture rationale lives in `human.zh/architecture.md`, while operational boundaries for agents live in paired AGENTS architecture docs.

## Detected Signals

- Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).

## System Map

- No system map details were detected automatically.

## 全局上下文信息提炼

- 已扫描分析底层信源数量：`3`
- 成功提炼主张：`5` 条确认, `0` 条矛盾, `0` 条未决

## 仓库知识体系健康度

### 100% 确凿基准规则库

- CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.
- Conflict handling order: 1) check `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md`; 2) then edit adapter/config mappings.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。

### 高价值辅助参考信号

- No additional derived architecture signals were detected from repository structure.

### 尚未决策的高风险清单

- No unresolved architecture items were synthesized from supporting docs.

### 矛盾与冲突预警监控

- No direct architecture conflicts were synthesized from supporting docs.

## Stability Boundaries

- Treat source-of-truth files as canonical when supporting docs disagree.
- Refresh both `docs/` and `AGENTS/` after architecture-impacting changes.

## 文档刷新触发条件

- When source-of-truth files, service boundaries, or runtime dependencies change, update this page.
- When integration contracts change (routes/endpoints/storage), refresh architecture notes in the same PR.

## 文档日常维护流

- Assign one maintainer owner for this document and update it in the same pull request as behavior changes.
- Review this document at least once per sprint or before each release cut.
- Update after boundary, dependency, or interface contract changes.
- No major synthesis conflicts were detected; focus on keeping this page current with implementation changes.

## 冷启动阶段待办 (When Docs Are Thin)

- Supporting docs were found; continue consolidating them into this page and archive stale duplicates.

## 溯源证明

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`
