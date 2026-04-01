# 项目总体概览 (Project Overview)

## 项目定位与背景

- English | [简体中文](README.zh.md)
- 当前仓库形态： `skill/meta repository`。

## 核心护栏与顶层规则 (首读必看)

- Rule 1: Product positioning: this repository is scoped for CLI coding-agent workflows, not a standalone end-user application.
- Rule 2: Repository adaptation scope: fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans.
- Rule 3: Retention value: prioritize repeatable `init -> refresh -> doctor` lifecycle checks so documentation stays governable, not a one-shot generator output.

## 文档与维护契约

- This page is maintainer-facing source-of-truth for its domain; keep it synchronized with `AGENTS/` in dual mode and `human.zh/` as the human-view root.
- Update this page in the same PR as behavior changes; avoid narrative-only refreshes without command or contract changes.
- Record scope decisions as explicit rules and owners; move stale discussion text to decision backlog.

## 双重视图同步清单

- After edits, refresh in dual mode and verify both `AGENTS/` and `human.zh/` were updated in the same change set.
- If one side changed without the other, treat it as documentation drift and resolve before merge.
- When scope or audience changes, update project positioning and retention rules in both doc systems together.

## 结对刷新规则

- Refresh contract: run one refresh/generate action that updates paired views together; do not patch one locale/audience in isolation.
- Path contract: verify changed files include both `AGENTS*/` and `docs*/` counterparts when behavior changes affect shared source-of-truth.
- Quad-mode contract: when using `--output-mode quad`, validate all four roots (`AGENTS/`, `AGENTS.zh/`, `docs/`, `docs.zh/`) in the same review cycle.
- Product pairing rule: if `human.zh/overview.md` changes due to scope/value decisions, refresh paired product paths under both AGENTS roots.

## 双视图关联契约 (Rules)

- Pairing mode rule: in `dual`, human and agent docs are generated from one analysis pass and must be reviewed as one change set.
- Locale-output rule: human locale `zh` maps to `human.zh/`.
- Template rule: human template variant `paired-core` is part of the pairing contract and must remain consistent across paired docs.
- Path pair rule: `human.zh/overview.md` pairs with `AGENTS/01-product/001-core-goals.md` for agent-facing product rules and scope guardrails.
- Path pair rule: `human.zh/overview.md` pairs with `AGENTS/01-product/002-prd.md` for agent-facing user and outcome contract.
- Path pair rule: `human.zh/overview.md` pairs with `AGENTS/01-product/003-app-flow.md` for agent-facing flow and entry-surface notes.

## 结对智能体文档 (双重模式)

- `AGENTS/01-product/001-core-goals.md` for agent-facing product rules and scope guardrails.
- `AGENTS/01-product/002-prd.md` for agent-facing user and outcome contract.
- `AGENTS/01-product/003-app-flow.md` for agent-facing flow and entry-surface notes.

## 输出边界 (人类 vs 智能体)

- Use `human.zh/` for maintainer-facing policy and decisions; use `AGENTS/` for execution order, command wiring, and handoff runbooks.
- If a change affects both reader types, update both systems in one dual refresh cycle instead of patching only one side.
- Keep user/value framing in `human.zh/overview.md`; keep edit-time operating rules in `AGENTS/product.md` (or layered product docs).

## 双视图设计逻辑

- `human.zh/` and `AGENTS/` are two views generated from the same repository analysis and source-of-truth anchors.
- When the two views diverge, treat it as refresh drift rather than independent documentation authority.
- Product intent lives in `human.zh/overview.md`, while execution-facing preservation rules live in paired AGENTS product docs.

## 目标读者

- Repository maintainers responsible for day-to-day delivery and operational stability.
- Skill maintainers keeping manifests, prompts, and generator behavior aligned.

## 关键入口点

- `doc-for-agent/SKILL.md`
- `doc-for-agent/agents/openai.yaml`

## 提炼总结

- Sources analyzed: `4`
- Synthesized statements: `5` confirmed, `0` conflicting, `0` unresolved

## 知识健康度

### 已确认的基准主张

- Product positioning: this repository is scoped for CLI coding-agent workflows, not a standalone end-user application.
- Repository adaptation scope: fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans.
- Retention value: prioritize repeatable `init -> refresh -> doctor` lifecycle checks so documentation stays governable, not a one-shot generator output.
- Positioning guardrail: describe `docagent` as an ongoing documentation system (`init/refresh/doctor/migrate`), not a one-shot markdown generator.

### 辅助参考信号

- Project intent from README/code signals: English | [简体中文](README.zh.md)
- Repo type signal: `skill/meta repository` (Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).)

### 决策后台 (未决事项)

- 未从支持文档中检测到未决的产品内容项。

### 冲突监控清单

- 未从支持文档中检测到直接的产品冲突。

## 当前优先级事项

- 在 `docs/` 中记录最新决策，并确保在变更后同步更新 AGENTS 文档。

## 文档空白填补清单

- 未从支持文档中检测到明显的产品文档缺失。

## 文档刷新触发条件

- When new user-facing routes, commands, or APIs are added, update scope and audience notes.
- When priorities change in release planning, update the project overview and open decision list.

## 文档日常维护流

- Assign one maintainer owner for this document and update it in the same pull request as behavior changes.
- Review this document at least once per sprint or before each release cut.
- Update after roadmap, target user, or feature scope decisions.
- No major synthesis conflicts were detected; focus on keeping this page current with implementation changes.

## 冷启动阶段待办 (文档薄弱时)

- Supporting docs were found; continue consolidating them into this page and archive stale duplicates.

## 溯源证明 (依据文件)

- `README.md`
- `docs/landing-page.md`
- `docs/landing-page.zh.md`
- `docs/maintainers.md`
