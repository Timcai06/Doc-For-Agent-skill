# 架构设计与技术决策

## 事实来源 (Source of Truth)

- `README.md` for stated project goals, setup expectations, and user-facing examples
- `doc-for-agent/SKILL.md` for trigger conditions and maintainer workflow
- `doc-for-agent/agents/openai.yaml` for launcher/marketplace invocation metadata
- `doc-for-agent/scripts/` for generation behavior and repository scanning
- `doc-for-agent/references/` for documentation structure and writing constraints

## 顶层护栏与核心规则 (首读必看)

- Rule 1: CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Rule 2: Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Rule 3: Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.

## 文档与维护契约

- This page is maintainer-facing source-of-truth for its domain; keep it synchronized with `AGENTS/` in dual mode and `human.zh/` as the human-view root.
- Update this page in the same PR as behavior changes; avoid narrative-only refreshes without command or contract changes.
- Resolve source-of-truth conflicts before editing CLI, adapter, or build-path behavior.

## 双重视图同步清单

- After edits, refresh in dual mode and verify both `AGENTS/` and `human.zh/` were updated in the same change set.
- If one side changed without the other, treat it as documentation drift and resolve before merge.
- When source-of-truth files move, update references in both doc systems before adjusting adapter/build-path rules.

## 结对刷新规则

- Refresh contract: run one refresh/generate action that updates paired views together; do not patch one locale/audience in isolation.
- Path contract: verify changed files include both `AGENTS*/` and `docs*/` counterparts when behavior changes affect shared source-of-truth.
- Quad-mode contract: when using `--output-mode quad`, validate all four roots (`AGENTS/`, `AGENTS.zh/`, `docs/`, `docs.zh/`) in the same review cycle.
- Architecture pairing rule: if `human.zh/architecture.md` changes due to boundary/source-of-truth updates, refresh paired architecture paths under both AGENTS roots.

## 双视图关联契约 (Rules)

- 结对模式规则：在 `dual` 模式下，人和机器的文档同源生成，必须作为一个完整的变更集进行评审。
- 语言输出规则：人类视图语言 `zh` 映射至目录 `human.zh/`。
- 模板规则：人类视图模板变体 `paired-core` 是结对契约的一部分，在配对文档间必须保持一致。
- Path pair rule: `human.zh/architecture.md` pairs with `AGENTS/02-architecture/004-tech-stack.md` for stack facts and platform anchors.
- Path pair rule: `human.zh/architecture.md` pairs with `AGENTS/02-architecture/007-architecture-compatibility.md` for source-of-truth and compatibility rules.

## 结对智能体文档 (双重模式)

- `AGENTS/02-architecture/004-tech-stack.md` for stack facts and platform anchors.
- `AGENTS/02-architecture/007-architecture-compatibility.md` for source-of-truth and compatibility rules.

## 文档输出边界 (人类与智能体)

- 使用 `human.zh/` 记录面向维护者的政策与决策；使用 `AGENTS/` 记录执行顺序、命令编排和运行手册。
- 如果一项变更同时影响两类受众，应在同一个同步周期内更新两套系统，而非仅单独修补一侧。
- 在 `human.zh/architecture.md` 中保留架构理由；在 `AGENTS/architecture.md` (或分层架构文档) 中保留 CLI/构建/事实来源护栏。

## 双视图设计逻辑

- `human.zh/` 与 `AGENTS/` 是基于同一份仓库分析和事实锚点生成的两套视图。
- 当两套视图出现分歧时，应将其视为“同步漂移”，而非独立的文档权威。
- 架构理由记录在 `human.zh/architecture.md` 中，而面向 Agent 的操作边界保留在配对的 AGENTS 文档中。

## 检测到的技术信号

- Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).

## 系统版图映射

- 未自动检测到系统版图细节。

## 提炼总结

- Sources analyzed: `3`
- Synthesized statements: `5` confirmed, `0` conflicting, `0` unresolved

## 知识健康度

### 已确认的基准主张

- CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.
- Conflict handling order: 1) check `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md`; 2) then edit adapter/config mappings.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。

### 辅助参考信号

- 未从代码仓库结构中检测到额外的衍生产品信号。

### 决策后台 (未决事项)

- 未从支持文档中检测到未决的架构事项。

### 冲突监控清单

- 未从支持文档中检测到直接的架构冲突。

## 稳定性边界

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

## 冷启动阶段待办 (文档薄弱时)

- Supporting docs were found; continue consolidating them into this page and archive stale duplicates.

## 溯源证明 (依据文件)

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`

## Preserved Notes

- 事实来源 (Source Of Truth)
  - Preserved from previous manual edits.
  - **`README.md`**：记录了项目的核心目标、安装预期和用户级示例。
  - **`doc-for-agent/SKILL.md`**：定义了智能体的触发条件和维护者的工作流共识。
  - **`doc-for-agent/agents/openai.yaml`**：提供了在智能体市场或启动器中的调用元数据。
  - **`doc-for-agent/scripts/`**：定义了具体的生成行为和仓库扫描逻辑。
- 顶层规则 (首读必看)
  - Preserved from previous manual edits.
  - **规则 1：CLI 边界** —— 严格保持 `docagent` 作为所有智能助手工作流（Codex, Claude, Continue, Copilot）的唯一物理入口表面。
  - **规则 2：事实来源边界** —— 当发生定义冲突时，在修改 CLI 入口或适配逻辑前，必须优先参考 `README.md` 与分发文档。
  - **规则 3：分发结构** —— 将具体平台的映射保留在适配器中，而核心 CLI 契约保持中心化。
- 文档维护契约
  - Preserved from previous manual edits.
  - **受众对齐**：本页面是面向维护者的核心事实来源，必须与 `AGENTS/` 目录下的执行文档保持高频事实对齐。
  - **变更驱动**：仅在系统行为发生实际变动时更新本页面，避免仅进行纯叙述性的文字刷新。
- 双视图同步检查清单
  - Preserved from previous manual edits.
  - **编辑后验证**：在修改代码或配置后，运行 `quad` 模式刷新，并验证 `AGENTS/` 与 `human.zh/` 是否在同一变更集中得到了更新。
  - **防止漂移**：如果发现一侧更新而另一侧停滞，应视其为“文档漂移”，并须在代码合并前予以解决。
- 架构逻辑综述
  - Preserved from previous manual edits.
  - **双视图共源**：本项目通过同一套仓库分析结果，同时生成面向智能体的上下文 (`AGENTS/`) 和面向人类的文档 (`human.zh/`)。
  - **职责划分**：使用 `human.zh/` 记录维护者层面的决策和政策；使用 `AGENTS/` 记录执行顺序、命令编排和运行手册。
  - **一致性基准**：当两个视图出现分歧时，应将其视为刷新漂移 (Refresh Drift)，而非独立的文档权威。
