# 核心目标与护栏

## 顶层护栏与核心规则 (首读必看)

- Rule 1: Product positioning: this repository is scoped for CLI coding-agent workflows, not a standalone end-user application.
- Rule 2: Repository adaptation scope: fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans.
- Rule 3: Retention value: prioritize repeatable `init -> refresh -> doctor` lifecycle checks so documentation stays governable, not a one-shot generator output.

## 已确认的客观事实

- English | [简体中文](README.zh.md)
- 本仓库目前的最佳判定形态为 `skill-meta`。
- 核心产品价值在于可复用的“智能体原生文档工作流”，而非仅指生成的文档文件本身。

## 严禁打破的开发约束

- Avoid drifting away from the repository's real code, scripts, and naming conventions.
- Prefer stable entrypoints and contracts over broad structural churn.
- Review mixed signals before collapsing the repository into a single simplistic mental model.

## 辅助参考文档提炼 (Product)

### 已确认的基准主张

- Product positioning: this repository is scoped for CLI coding-agent workflows, not a standalone end-user application.
- Repository adaptation scope: fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans.
- Retention value: prioritize repeatable `init -> refresh -> doctor` lifecycle checks so documentation stays governable, not a one-shot generator output.
- Positioning guardrail: describe `docagent` as an ongoing documentation system (`init/refresh/doctor/migrate`), not a one-shot markdown generator.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 (sources: `docs/landing-page.zh.md`)

### 待清理的矛盾点

- 未从支持文档中检测到直接的产品冲突。

### 悬而未决的问题

- 未从支持文档中检测到未决的产品内容项。

## Preserved Notes

- 顶层规则 (首读必看)
  - Preserved from previous manual edits.
  - **规则 1：产品定位** —— 本仓库定位于 CLI 编程智能体 (Coding-Agent) 的工作流深度集成，而非独立的终端用户应用。
  - **规则 2：仓库适配范围** —— 专注于需要长效维护、持续刷新和文档治理的仓库体系。
  - **规则 3：价值基石** —— 优先确保 `init -> refresh -> doctor` 生命周期检查的可重复性，以实现文档的长期可治理性。
- 已确认的事实 (Confirmed Facts)
  - Preserved from previous manual edits.
  - **简体中文版文档**：由 [`README.zh.md`](../../README.zh.md) 进行基准支撑。
  - **分类标识**：本仓库当前被定义并识别为 `skill-meta` (技能元仓库)。
  - **核心价值**：产品的核心价值在于其可复用的智能体文档定义工作流。
- 待保留的约束
  - Preserved from previous manual edits.
  - **严禁偏差**：严禁脱离本工程真实的源代码逻辑、脚本实现和命名契约。
  - **契约优先**：在进行大规模结构性变动前，优先保持已有的入口点和交互契约的稳定性。
- 辅助文档综合 (产品维度)
  - Preserved from previous manual edits.
  ### 已确认的内容 (Confirmed)

  - **产品定位**：定位于为 CLI 智能体提供协同能力，而非普通的 Markdown 生成工具。
  - **系统定义**：描述 `docagent` 为一套长效文档治理系统 (`init/refresh/doctor/migrate`)。
  - **快接路径**：支持通过 `npm install -g doc-for-agent@next` 进行的一键式部署路径。

  ### 潜在冲突项

  - **无**：当前未在支撑文档中检测到任何直接的产品定义冲突。

  ### 未决事项

  - **无**：当前未在支撑文档中检测到任何未定义的重大产品策略项。
