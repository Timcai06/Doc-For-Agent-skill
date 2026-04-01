# App Flow

## Surfaces Detected

- Agent manifest surface: `doc-for-agent/agents/openai.yaml`

## Guidance

- Treat the first visible or invoked surface as part of the product contract.
- Keep user-facing names aligned across README examples, manifests, routes, and commands.
- Treat install, invocation, and prompt surfaces as the equivalent of a frontend contract.

## Supporting Doc Synthesis (Flow)

### Confirmed

- Product positioning: this repository is scoped for CLI coding-agent workflows, not a standalone end-user application.
- Repository adaptation scope: fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans.
- Retention value: prioritize repeatable `init -> refresh -> doctor` lifecycle checks so documentation stays governable, not a one-shot generator output.
- Positioning guardrail: describe `docagent` as an ongoing documentation system (`init/refresh/doctor/migrate`), not a one-shot markdown generator.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 (sources: `docs/landing-page.zh.md`)

### Conflicting

- No direct flow conflicts were synthesized from supporting docs.

### Unresolved

- No unresolved flow items were synthesized from supporting docs.

## Preserved Notes

- 已检测到的入口界面 (Surfaces)
  - Preserved from previous manual edits.
  - **智能体清单入口**：`doc-for-agent/agents/openai.yaml`，该文件定义了产品在各类智能体助手平台中的“被发现”机制及其元数据合约。
- 引导与交互准则 (Guidance)
  - Preserved from previous manual edits.
  - **产品契约第一印象**：将用户首次看到或调用的界面（如 `docagent init`）视为产品契约的重要组成部分。
  - **全链路命名一致性**：确保 README 中的示例、清单文件、路由定义和具体的子命令名称在语义上保持高度统一。
  - **逻辑契约对齐**：将安装流程、调用接口和 Prompt 触点视为本仓库对外的“前端逻辑合约”。
- 支撑文档综合 (交互流维度)
  - Preserved from previous manual edits.
  ### 已确认的内容 (Confirmed)

  - **产品定位**：本仓库聚焦于 CLI 智能代码助手 (Coding-Agent) 的工作流深度集成。
  - **适配范围**：专注于需要长效维护、持续刷新和文档治理的仓库体系。
  - **系统价值**：确立了以 `init -> refresh -> doctor` 为核心的阶梯式治理流程产出。
  - **入口指引**：通过 `npm install -g doc-for-agent@next` 提供的便捷安装路径，大幅降低新用户的入场门槛。

  ### 交互流状态监控

  - **冲突项**：当前未在支撑文档中检测到任何直接的交互流冲突项。
  - **未决项**：当前未在支撑文档中检测到任何未定义的交互行为项。
