# doc-for-agent 平台指南

[English](platforms.md) | 简体中文

使用 `docagent init --ai ...` 选择你的平台入口。

## 平台矩阵

| 平台 | 首条命令 | 适配类型 | 安装位置 |
| --- | --- | --- | --- |
| Claude Code | `docagent init --ai claude --target <repo-root>` | skill (`SKILL.md`) | `.claude/skills/doc-for-agent/` |
| Codex | `docagent init --ai codex --target <repo-root>` | skill (`SKILL.md`) | `.codex/skills/doc-for-agent/` |
| CodeBuddy | `docagent init --ai codex --target <repo-root>` | skill (`SKILL.md`) | `.codex/skills/doc-for-agent/` |
| Continue | `docagent init --ai continue --target <repo-root>` | skill (`SKILL.md`) | `.continue/skills/doc-for-agent/` |
| GitHub Copilot | `docagent init --ai copilot --target <repo-root>` | prompt (`PROMPT.md`) | `.github/prompts/doc-for-agent/` |

## 多 Agent 安装

```bash
docagent init --ai all --target <repo-root>
```

## 分发模型

- Python 包：规范运行时与完整 CLI。  
- npm 包：面向 Node 用户的薄启动器。  
- 两条路径最终都收敛到同一命令面：`docagent`。

## 下一条命令

初始化后：

```bash
docagent refresh --root <repo-root> --output-mode agent
```

另见：

- [Quickstart（英文）](quickstart.md) / [Quickstart（中文）](quickstart.zh.md)
- [Maintainer Guide](maintainers.md)

