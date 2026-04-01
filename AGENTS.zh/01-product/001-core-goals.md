# Core Goals

## Top Rules (Read First)

- Rule 1: Product positioning: this repository is scoped for CLI coding-agent workflows, not a standalone end-user application.
- Rule 2: Repository adaptation scope: fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans.
- Rule 3: Retention value: prioritize repeatable `init -> refresh -> doctor` lifecycle checks so documentation stays governable, not a one-shot generator output.

## Confirmed Facts

- English | [简体中文](README.zh.md)
- This repository is currently best understood as a `skill/meta repository`.
- The core product is the reusable agent-documentation workflow, not only the generated files themselves.

## Constraints To Preserve

- Avoid drifting away from the repository's real code, scripts, and naming conventions.
- Prefer stable entrypoints and contracts over broad structural churn.
- Review mixed signals before collapsing the repository into a single simplistic mental model.

## Supporting Doc Synthesis (Product)

### Confirmed

- Product positioning: this repository is scoped for CLI coding-agent workflows, not a standalone end-user application.
- Repository adaptation scope: fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans.
- Retention value: prioritize repeatable `init -> refresh -> doctor` lifecycle checks so documentation stays governable, not a one-shot generator output.
- Positioning guardrail: describe `docagent` as an ongoing documentation system (`init/refresh/doctor/migrate`), not a one-shot markdown generator.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 (sources: `docs/landing-page.zh.md`)

### Conflicting

- No direct product conflicts were synthesized from supporting docs.

### Unresolved

- No unresolved product items were synthesized from supporting docs.

## Preserved Notes

- 顶层规则 (首读必看)
  - Preserved from previous manual edits.
  - **规则 1：产品定位** —— 本仓库专为 **CLI 智能代码助手 (Coding-Agent)** 的工作流设计，而非独立的终端用户应用程序。
  - **规则 2：仓库适配范围** —— 适用于需要持续刷新和治理文档的工作流，而非单次性的文档扫描。
  - **规则 3：持久化价值** —— 优先考虑可重复的 `init -> refresh -> doctor` 生命周期检查，确保文档随代码同步进化，而非某种一次性的生成器产物。
- 已确认的事实
  - Preserved from previous manual edits.
  - [English](../01-product/001-core-goals.md) | 简体中文
  - 当前仓库被定义为：`skill/meta repository`（技能元仓库）。
  - **核心产品定义**：产品本身是“可复用的 Agent 文档工作流”，而不仅仅是生成的 Markdown 文件。
- 必须遵守的约束
  - Preserved from previous manual edits.
  - **严禁偏离事实**：文档必须与仓库实际的代码逻辑、脚本和命名规范保持高度一致。
  - **入口契约优先**：优先保持稳定的入口点和契约，避免频繁的结构性震荡。
  - **审视混合信号**：在将仓库简化为单一心理模型前，必须充分评估所有检测到的混合信号。
- 支撑文档综合 (产品维度)
  - Preserved from previous manual edits.
  ### 已确认 (Confirmed)

  - **产品定位**：本仓库专为 CLI 智能代码助手 (Coding-Agent) 的工作流设计。
  - **适配范围**：旨在适配需要长期文档治理和同步的仓库。
  - **生命周期价值**：强调 `init -> refresh -> doctor` 的闭环检查能力。
  - **系统定义**：`docagent` 是一个持续的文档治理系统，而非一次性的生成器。
  - **快捷路径**（uipro-cli 风格）：`npm install -g doc-for-agent@next` -> `docagent init --ai codex`。

  ### 冲突项 (Conflicting)

  - 未从支撑文档中检测到直接的产品内容冲突。

  ### 未决项 (Unresolved)

  - 未从支撑文档中检测到未解决的产品争议项。
