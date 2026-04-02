# 应用交互流程与契约

## 检测到的交互界面

- 智能体清单入口：`doc-for-agent/agents/openai.yaml`

## 流程指引

- 将第一个可见或被调用的入口视为产品契约的一部分。
- 保持面向用户的名称在 README 示例、清单、路由和命令中对齐。
- 将安装、调用和提示词入口视为等同于前端契约。

## 辅助参考文档提炼 (Flow)

### 已确认的基准主张

- 产品定位： 本仓库面向 CLI coding-agent 工作流，而不是独立终端用户应用。
- 仓库适配范围： 适用于需要持续 refresh/治理工作流的仓库，而不是一次性文档扫描。
- 留存价值： 优先保证可重复的 `init -> refresh -> doctor` 生命周期检查，使文档保持可治理，而不是一次性生成产物。
- 定位护栏： 将 `docagent` 描述为持续运行的文档系统（`init/refresh/doctor/migrate`），而不是一次性 Markdown 生成器。
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 

### 待清理的矛盾点

- 未从支持文档中检测到直接的流程冲突。

### 悬而未决的问题

- 未检测到未决的流程项目。
