# 智能体全局入口 (AGENTS.zh Index)

本目录包含了辅助 AI Agent 理解和执行本仓库任务的全部文档契约及背景知识。

## 推荐阅读顺序

1.  **[核心目标](01-product/001-core-goals.md)** —— 产品边界与顶层护栏规则。
2.  **[PRD](01-product/002-prd.md)** —— 核心用户画像与预期交付产出。
3.  **[技术栈](02-architecture/004-tech-stack.md)** —— 系统的环境依赖与构建工具链。
4.  **[应用交互流](01-product/003-app-flow.md)** —— 入口表面定义与应用交互契约。
5.  **[后端逻辑架构](02-architecture/006-backend-structure.md)** —— 核心逻辑入口与脚本执行层级。
6.  **[架构兼容边界](02-architecture/007-architecture-compatibility.md)** —— 事实来源 (Source of truth) 仲裁规则。
7.  **[实施计划](03-execution/008-implementation-plan.md)** —— 执行步骤、验证命令与故障排查指南。

## 核心目标

本系统通过 `docagent` 引擎，实现面向智能体的上下文 (`AGENTS/`) 与面向维护者的文档 (`human.zh/`) 的高频事实对齐。

- **语言视图切换**：[English View](../AGENTS/AGENTS.md) | **简体中文**
- **手动块保护**：本目录下的所有文件均支持 `<!-- doc-for-agent:manual-start -->` 的手动内容保护机制，刷新文档时不会丢失手动维护的经验。
