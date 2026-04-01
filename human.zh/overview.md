# 项目治理总体概览

## 项目定位与背景

- English | [简体中文](README.zh.md)
- 当前仓库形态： `Skill Meta`。

## 顶层护栏与核心规则 (首读必看)

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

- 结对模式规则：在 `dual` 模式下，人和机器的文档同源生成，必须作为一个完整的变更集进行评审。
- 语言输出规则：人类视图语言 `zh` 映射至目录 `human.zh/`。
- 模板规则：人类视图模板变体 `paired-core` 是结对契约的一部分，在配对文档间必须保持一致。
- Path pair rule: `human.zh/overview.md` pairs with `AGENTS/01-product/001-core-goals.md` for agent-facing product rules and scope guardrails.
- Path pair rule: `human.zh/overview.md` pairs with `AGENTS/01-product/002-prd.md` for agent-facing user and outcome contract.
- Path pair rule: `human.zh/overview.md` pairs with `AGENTS/01-product/003-app-flow.md` for agent-facing flow and entry-surface notes.

## 结对智能体文档 (双重模式)

- `AGENTS/01-product/001-core-goals.md` for agent-facing product rules and scope guardrails.
- `AGENTS/01-product/002-prd.md` for agent-facing user and outcome contract.
- `AGENTS/01-product/003-app-flow.md` for agent-facing flow and entry-surface notes.

## 文档输出边界 (人类与智能体)

- 使用 `human.zh/` 记录面向维护者的政策与决策；使用 `AGENTS/` 记录执行顺序、命令编排和运行手册。
- 如果一项变更同时影响两类受众，应在同一个同步周期内更新两套系统，而非仅单独修补一侧。
- 在 `human.zh/overview.md` 中保留用户/价值框架；在 `AGENTS/product.md` (或分层产品文档) 中保留运行规则。

## 双视图设计逻辑

- `human.zh/` 与 `AGENTS/` 是基于同一份仓库分析和事实锚点生成的两套视图。
- 当两套视图出现分歧时，应将其视为“同步漂移”，而非独立的文档权威。
- 产品意图记录在 `human.zh/overview.md` 中，而面向执行的规则保留在配对的 AGENTS 文档中。

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
- Repo type signal: `Skill Meta` (Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).)

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

## Preserved Notes

- 核心目标与管治准则
  - Preserved from previous manual edits.
  - **技能定义对齐**：将 `doc-for-agent` 的技能清单 (Skill Manifests)、生成行为与生成的文档事实维持高频同步。
  - **事实基准策略**：优先采用 `README.md` 和 `README.zh.md` 的核心表述作为全仓库文档治理的基准。
  - **治理闭环**：通过 `init -> refresh -> doctor` 实现可预测的、针对 Coding Agent 的文档刷新周期。
- 系统认知 (System Context)
  - Preserved from previous manual edits.
  - **识别仓库分类**：`skill/meta repository` (技能元仓库，识别可信度：中等)。
  - **核心定位**：本仓库通过统一的 `docagent` 命令界面，支持 Codex、Claude、Copilot 等多路径智能体工作流。
  - **治理方案**：采用 `layered` (分层索引) 对待仓库背景，通过 Quard-View 同时兼顾人类与智能体的多维度需求。
- 辅助文档提炼与事实对齐
  - Preserved from previous manual edits.
  ### 已确认的内容

  - **产品界限**：定位于 CLI 智能体深度协同，而非简单的静态页面生成。
  - **系统入口一致性**：保持 `docagent` 作为各工作流的物理入口，并支持 `npm install -g doc-for-agent@next` 一键部署。

  ### 潜在冲突项

  - **无**：当前未在支撑事实中检测到直接的系统级冲突项。

  ### 未决事项

  - **受众人群细化**：进一步明确下游集成方对于生成的物理物理目录及其命名的精确预期。
- 核心参考库 (References)
  - Preserved from previous manual edits.
  - [`README.md`](../README.md)
  - [`README.zh.md`](../README.zh.md)
  - [`docs/landing-page.zh.md`](../docs/landing-page.zh.md)
