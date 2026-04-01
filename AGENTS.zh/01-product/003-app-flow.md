# 应用交互流程与契约

## 检测到的交互界面

- 智能体清单入口：`doc-for-agent/agents/openai.yaml`

## 流程指引

- 将第一个可见或被调用的入口视为产品契约的一部分。
- 保持面向用户的名称在 README 示例、清单、路由和命令中对齐。
- 将安装、调用和提示词入口视为等同于前端契约。

## 辅助参考文档提炼 (Flow)

### 已确认的基准主张

- Product positioning: this repository is scoped for CLI coding-agent workflows, not a standalone end-user application.
- Repository adaptation scope: fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans.
- Retention value: prioritize repeatable `init -> refresh -> doctor` lifecycle checks so documentation stays governable, not a one-shot generator output.
- Positioning guardrail: describe `docagent` as an ongoing documentation system (`init/refresh/doctor/migrate`), not a one-shot markdown generator.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 (sources: `docs/landing-page.zh.md`)

### 待清理的矛盾点

- 未从支持文档中检测到直接的流程冲突。

### 悬而未决的问题

- 未检测到未决的流程项目。

## Preserved Notes

- 已检测到的入口界面 (Surfaces)
  - Preserved from previous manual edits.
  - **智能体清单入口**：`doc-for-agent/agents/openai.yaml`，该文件定义了产品如何在各助手平台中“被发现”及其元数据合约。
- 引导与准则 (Guidance)
  - Preserved from previous manual edits.
  - **产品第一印象**：将用户首次看到或调用的界面视为产品契约的重要组成部分。
  - **命名一致性**：确保全链路（README、清单文件、路由定义和子命令）中的用户侧名称保持高度中心化对齐。
  - **逻辑合约**：安装过程、调用接口和 Prompt 表面即为本仓库对外的“逻辑界面合约”。
- 辅助文档综合 (交互维度)
  - Preserved from previous manual edits.
  ### 已确认的内容

  - **产品定位**：本仓库聚焦于 CLI 智能代码助手 (Coding-Agent) 的深度工作流协同集成。
  - **适配职责**：专注于需要长效维护、持续刷新和文档管治的仓库演进。
  - **系统核心**：确立了以 `init -> refresh -> doctor` 为进阶路径的治理流程产出。
  - **入场路径**：通过 `npm install -g doc-for-agent@next` 提供的官方官方部署路径。

  ### 潜在冲突项

  - **无**：当前未在支撑文档中检测到任何直接的交互流。

  ### 未决事项

  - **无**：当前未在支撑文档中检测到任何未定义的交互行为项。
