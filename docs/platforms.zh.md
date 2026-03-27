# doc-for-agent 平台指南

[English](platforms.md) | 简体中文

使用 `docagent init --ai ...` 选择你的平台入口。

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
