# 项目总体概览

## 项目定位与愿景

- [English](README.md) | 简体中文
- 当前仓库形态： `技能/元数据类仓库`.

## 核心护栏与顶层规则 (首读必看)

- 第一原则： 产品定位： 本代码库专注于 CLI 编程智能体工作流，而非独立的终端用户应用.
- 第二原则： 仓库适配范围： 适用于需要持续刷新和治理工作流的仓库，而非一次性的文档扫描.
- 第三原则： 留存价值： 优先保障可重复的 `init -> refresh -> doctor` 生命周期的可治理性 确保文档持续可控，而非一次性生成后的“僵尸”文档.

## 文档与执行层契约

- 本页面是该领域面向维护者的真相源; 保持其在双重模式下与 `AGENTS/` 的同步 and `human.zh/` 作为人类视角的根目录.
- 在代码行为变更的同一个 PR 中同步更新此页面; 避免在没有命令或契约更改的情况下进行纯叙述性的刷新.
- 将范围决策记录为明确的规则和负责人; 将过时的讨论文本移至决策后台.

## 双重视图对齐检查清单

- After edits, refresh in dual mode and verify both `AGENTS/` and `human.zh/` were updated in the same change set.
- If one side changed without the other, treat it as documentation drift and resolve before merge.
- When scope or audience changes, update project positioning and retention rules in both doc systems together.

## Quad模式下的同步规则

- Refresh contract: run one refresh/generate action that updates paired views together; do not patch one locale/audience in isolation.
- Path contract: verify changed files include both `AGENTS*/` and `docs*/` counterparts when behavior changes affect shared source-of-truth.
- Quad-mode contract: when using `--output-mode quad`, validate all four roots (`AGENTS/`, `AGENTS.zh/`, `docs/`, `docs.zh/`) in the same review cycle.
- Product pairing rule: if `human.zh/overview.md` changes due to scope/value decisions, refresh paired product paths under both AGENTS roots.

## 双视图强制对齐契约

- Pairing mode rule: in `dual`, human and agent docs are generated from one analysis pass and must be reviewed as one change set.
- Locale-output rule: 中文语言包 `zh` 映射至 `human.zh/` 目录.
- Template rule: human template variant `paired-core` is part of the pairing contract and must remain consistent across paired docs.
- 路径对齐规则：`human.zh/overview.md` 与 `AGENTS/01-product/001-core-goals.md` 结对，用于 agent-facing product rules and scope guardrails.
- 路径对齐规则：`human.zh/overview.md` 与 `AGENTS/01-product/002-prd.md` 结对，用于 agent-facing user and outcome contract.
- 路径对齐规则：`human.zh/overview.md` 与 `AGENTS/01-product/003-app-flow.md` 结对，用于 agent-facing flow and entry-surface notes.

## Paired Agent Docs (Dual Mode)

- `AGENTS/01-product/001-core-goals.md` 智能体侧的产品规则与范围护栏.
- `AGENTS/01-product/002-prd.md` 智能体侧的用户与交付契约.
- `AGENTS/01-product/003-app-flow.md` 智能体侧的流程与入口说明.

## 边界定义：人读区 vs 机读区

- Use `human.zh/` for maintainer-facing policy and decisions; use `AGENTS/` for execution order, command wiring, and handoff runbooks.
- If a change affects both reader types, update both systems in one dual refresh cycle instead of patching only one side.
- Keep user/value framing in `human.zh/overview.md`; keep edit-time operating rules in `AGENTS/product.md` (or layered product docs).

## 双向视图设计逻辑

- `human.zh/` and `AGENTS/` are two views generated from the same repository analysis and source-of-truth anchors.
- When the two views diverge, treat it as refresh drift rather than independent documentation authority.
- Product intent lives in `human.zh/overview.md`, while execution-facing preservation rules live in paired AGENTS product docs.

## 目标读者与受众

- 负责日常交付和运营稳定的仓库维护者 以及运营稳定性.
- 负责保持清单、提示词与生成器行为一致的技能维护者.

## 关键入口点

- `doc-for-agent/SKILL.md`
- `doc-for-agent/agents/openai.yaml`

## 全局上下文提炼

- 已分析信源数量：`4`
- 成功提炼结论：`5` 条确认，`0` 条矛盾，`0` 条未决

## 仓库知识健康度

### 核心确立的规则库

- 产品定位： 本代码库专注于 CLI 编程智能体工作流，而非独立的终端用户应用.
- 仓库适配范围： 适用于需要持续刷新和治理工作流的仓库，而非一次性的文档扫描.
- 留存价值： 优先保障可重复的 `init -> refresh -> doctor` 生命周期的可治理性 确保文档持续可控，而非一次性生成后的“僵尸”文档.
- 定位护栏： 将 `docagent` 描述为一个持续运作的文档系统 (`init/refresh/doctor/migrate`), 而非一次性生成的 Markdown 工具.

### 高价值辅助参考信号

- Project intent from README/code signals: [English](README.md) | 简体中文
- Repo type signal: `技能/元数据类仓库` (Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).)

### 尚未决策的高风险清单

- 未检测到未决的项目内容项 .

### 矛盾与冲突预警监控

- 未检测到直接的项目内容冲突 .

## 当前任务优先级

- Capture latest decisions in `docs/` and keep AGENTS synchronized after changes.

## 待填补的文档空白

- 未检测到明显的产品文档空白 .

## 文档刷新触发条件

- When new user-facing routes, commands, or APIs are added, update scope and audience notes.
- When priorities change in release planning, update the project overview and open decision list.

## 文档日常维护流

- 为此文档分配一名维护责任人 and update it in the same pull request as behavior changes.
- 每个 Sprint 至少评审一次此文档 or before each release cut.
- Update after roadmap, target user, or feature scope decisions.
- 未检测到严重的规则提炼冲突; focus on keeping this page current with implementation changes.

## 冷启动阶段待办 (When Docs Are Thin)

- Supporting docs were found; continue consolidating them into this page and archive stale duplicates.

## 溯源证明

- `README.md`
- `docs/landing-page.md`
- `docs/landing-page.zh.md`
- `docs/maintainers.md`
