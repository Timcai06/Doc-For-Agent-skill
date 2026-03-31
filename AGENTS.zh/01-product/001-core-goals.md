# Core Goals

## 核心护栏与顶层规则 (首读必看)

- 第一原则： 产品定位： 本代码库专注于 CLI 编程智能体工作流，而非独立的终端用户应用.
- 第二原则： 仓库适配范围： 适用于需要持续刷新和治理工作流的仓库，而非一次性的文档扫描.
- 第三原则： 留存价值： 优先保障可重复的 `init -> refresh -> doctor` 生命周期的可治理性 确保文档持续可控，而非一次性生成后的“僵尸”文档.

## 已确认的客观事实

- [English](README.md) | 简体中文
- This repository is currently best understood as a `技能/元数据类仓库`.
- The core product is the reusable agent-documentation workflow, not only the generated files themselves.

## 严禁打破的开发约束

- 避免偏离仓库真实的业务代码、脚本和命名规范, scripts, and naming conventions.
- 优先保持稳定的入口和契约，而不是进行大规模的解构.
- 在将仓库简化为单一思维模型前，务必审查各种交错的信号.

## 辅助参考文档提炼 (Product)

### 已确认的基准主张

- 产品定位： 本代码库专注于 CLI 编程智能体工作流，而非独立的终端用户应用.
- 仓库适配范围： 适用于需要持续刷新和治理工作流的仓库，而非一次性的文档扫描.
- 留存价值： 优先保障可重复的 `init -> refresh -> doctor` 生命周期的可治理性 确保文档持续可控，而非一次性生成后的“僵尸”文档.
- 定位护栏： 将 `docagent` 描述为一个持续运作的文档系统 (`init/refresh/doctor/migrate`), 而非一次性生成的 Markdown 工具.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 

### 待清理的矛盾点

- 未检测到直接的产品内容冲突 .

### 悬而未决的问题

- 未检测到未决的产品内容项 .

## 核心参考代码区与文档

- `README.md`
- `docs/landing-page.md`
- `docs/landing-page.zh.md`
- `docs/maintainers.md`

## 核心决策待填补区

- Confirm the top-level success criteria and non-goals for this repository.
