# doc-for-agent 平台指南

[English](platforms.md) | 简体中文

使用 `docagent init --ai ...` 选择你的平台入口。
入口链路位置：本页位于 `README.md` -> `docs/landing-page.zh.md` -> `docs/quickstart.zh.md` 之后。
两步模型：全局安装让 skill 对 agent 可见，repo-local init 启用当前仓库工作流。
临时 Node 场景下，`npx -y doc-for-agent init ...` 可合并两步。

## 平台矩阵

| 平台 | 首条命令 |
| --- | --- |
| Claude Code | `docagent init --ai claude --target <repo-root>` |
| Codex | `docagent init --ai codex --target <repo-root>` |
| CodeBuddy | `docagent init --ai codex --target <repo-root>` |
| Continue | `docagent init --ai continue --target <repo-root>` |
| GitHub Copilot | `docagent init --ai copilot --target <repo-root>` |

`init` 会自动处理各平台适配文件，你只需要选择 `--ai`。
初始化后，根据文档受众选择 `refresh --output-mode agent|human|dual`。
模式映射：`agent` -> `AGENTS/`，`human` -> `docs/`，`dual` -> 两者同时输出。
`dual` 模式会在一次 refresh 流程中把 `docs/`（human docs）与 `AGENTS/`（agent docs）成对维护。
平台选择与文档受众是两件事：这不是 AGENTS-only 工具。

## 多 Agent 安装

```bash
docagent init --ai all --target <repo-root>
```

## 分发模型

- Python 包：规范运行时与完整 CLI。  
- npm 包：面向 Node 用户的薄启动器。  
- 两条路径最终都收敛到同一命令面：`docagent`。

## 下一条命令

默认：

```bash
docagent refresh --root <repo-root> --output-mode agent
```

可选模式：`--output-mode human` 或 `--output-mode dual`。

另见：

- [Landing Page（英文）](landing-page.md) / [落地页说明（中文）](landing-page.zh.md)
- [Quickstart（英文）](quickstart.md) / [快速开始（中文）](quickstart.zh.md)
- [Maintainer Guide](maintainers.md)
