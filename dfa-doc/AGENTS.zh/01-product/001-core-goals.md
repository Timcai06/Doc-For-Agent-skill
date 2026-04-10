# 核心目标与护栏

## 顶层护栏与核心规则 (首读必看)

- 第一原则： 产品定位： 本仓库面向 CLI coding-agent 工作流，而不是独立终端用户应用。
- 第二原则： 仓库适配范围： 适用于需要持续 refresh/治理工作流的仓库，而不是一次性文档扫描。
- 第三原则： 留存价值： 优先保证可重复的 `init -> refresh -> doctor` 生命周期检查，使文档保持可治理，而不是一次性生成产物。

## 已确认的客观事实

- [English](README.md) | 简体中文
- 本仓库目前的最佳判定形态为 `skill-meta`。
- 核心产品价值在于可复用的“智能体原生文档工作流”，而非仅指生成的文档文件本身。

## 严禁打破的开发约束

- 避免偏离仓库的真实代码、脚本和命名约定。
- 优先保持稳定的入口点和契约，而不是进行大范围结构改动。
- 在把仓库简化成单一心智模型之前，先审查相互混杂的信号。

## 辅助参考文档提炼 (Product)

### 已确认的基准主张

- 产品定位： 本仓库面向 CLI coding-agent 工作流，而不是独立终端用户应用。
- 仓库适配范围： 适用于需要持续 refresh/治理工作流的仓库，而不是一次性文档扫描。
- 留存价值： 优先保证可重复的 `init -> refresh -> doctor` 生命周期检查，使文档保持可治理，而不是一次性生成产物。
- 定位护栏： 将 `docagent` 描述为持续运行的文档系统（`init/refresh/doctor/migrate`），而不是一次性 Markdown 生成器。
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent -> docagent init --ai codex / docagent init --ai claudecode。 

### 待清理的矛盾点

- 未从支持文档中检测到直接的产品冲突。

### 悬而未决的问题

- 未从支持文档中检测到未决的产品内容项。

## 核心参考历史文档

- `README.md`
- `docs/landing-page.md`
- `docs/landing-page.zh.md`
- `docs/maintainers.md`
