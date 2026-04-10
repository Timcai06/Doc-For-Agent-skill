# doc-for-agent 平台指南

[English](platforms.md) | 简体中文

使用 `docagent init --ai ...` 选择你的平台入口。
入口链路位置：本页位于 `README.md` -> `docs/landing-page.zh.md` -> `docs/quickstart.zh.md` 之后。
两步模型：全局安装让 skill 对 agent 可见，repo-local init 启用当前仓库工作流。
`refresh` 是 init 之后的“半步”：当你需要写入或更新 agent docs、human docs 或两者时再执行它。
临时 Node 场景下，`npx -y doc-for-agent init ...` 可合并前两步；`refresh` 仍然是独立的后一步。
仅当你在仓库外为特定仓库接线时，才需要 `--target <repo-root>`。
简路径（`uipro-cli` 风格）：`npm install -g doc-for-agent` -> `docagent init --ai codex` / `docagent init --ai claudecode`。

## 平台矩阵

| 平台 | 首条命令 |
| --- | --- |
| Claude Code | `docagent init --ai claudecode` |
| Codex | `docagent init --ai codex` |
| CodeBuddy | `docagent init --ai codex --target <repo-root>` |
| Continue | `docagent init --ai continue --target <repo-root>` |
| GitHub Copilot | `docagent init --ai copilot --target <repo-root>` |

`init` 会自动处理各平台适配文件，你只需要选择 `--ai`。
初始化后，根据文档受众选择 `refresh --output-mode agent|human|dual|quad`。
模式映射：`agent` -> `dfa-doc/AGENTS/`，`human` -> `dfa-doc/handbook/`，`dual` -> 两者同时输出，`quad` -> `dfa-doc/AGENTS/`、`dfa-doc/AGENTS.zh/`、`dfa-doc/handbook/`、`dfa-doc/handbook.zh/`。
`dual` 模式会在一次 refresh 流程中把 `dfa-doc/handbook/`（human docs）与 `dfa-doc/AGENTS/`（agent docs）成对维护。
四视图布局表达的是结构能力，不等于每个双语视图都已经完整成熟。
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

可选模式：`--output-mode human`、`--output-mode dual` 或 `--output-mode quad`。

另见：

- [Landing Page（英文）](landing-page.md) / [落地页说明（中文）](landing-page.zh.md)
- [Quickstart（英文）](quickstart.md) / [快速开始（中文）](quickstart.zh.md)
- [Maintainer Guide](maintainers.md)
