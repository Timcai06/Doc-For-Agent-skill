# doc-for-agent

[English](README.md) | 简体中文

`doc-for-agent` 是一个面向 CLI coding-agent 用户的统一 CLI。

适用于 Claude Code、Codex、CodeBuddy、Continue、Copilot 等终端优先工作流。

它支持 `agent`、`human`、`dual`、`quad` 四种输出。
模式映射：`agent` 写入 `AGENTS/`，`human` 写入 `docs/`，`dual` 同时写入两者，`quad` 写入 `AGENTS/`、`AGENTS.zh/`、`docs/`、`docs.zh/`。
`dual` 模式会在一次 refresh 流程中同时维护 `docs/`（human docs）与 `AGENTS/`（agent docs）。`quad` 模式建立双语四视图目录契约。
它不是 AGENTS-only 工具：应按文档受众选择输出模式。

产品路径很短：

1. 安装
2. `init`
3. `refresh`

## 30 秒开始

先安装一次：

```bash
# Node 用户
npm install -g doc-for-agent@next

# Python 用户
pipx install doc-for-agent
```

然后初始化 agent skill：

```bash
docagent init --ai codex
docagent init --ai claudecode
```

如需在同一个命令里同时接线当前仓库，添加 `--target <repo-root>`。一次性 `npx -y doc-for-agent init ...` 仍可用于临时场景。

如果你需要按步骤的文档入口图，先运行：

```bash
docagent quickstart --target <repo-root>
```

## 按 Agent 选入口

| 你使用... | 先执行 |
| --- | --- |
| Claude Code | `docagent init --ai claudecode` |
| Codex | `docagent init --ai codex` |
| CodeBuddy | `docagent init --ai codex --target <repo-root>` |
| Continue | `docagent init --ai continue --target <repo-root>` |
| GitHub Copilot | `docagent init --ai copilot --target <repo-root>` |
| 多个 Agent | `docagent init --ai all` |

## 安装矩阵

| 用户类型 | 安装方式 | 起步命令 |
| --- | --- | --- |
| Node-first（全局） | `npm install -g doc-for-agent@next` | `docagent init --ai all` |
| Node-first（一次性） | `npx -y doc-for-agent` | `npx -y doc-for-agent init --ai all --target <repo-root>` |
| Python-first（推荐） | `pipx install doc-for-agent` | `docagent init --ai all` |
| Python-first（venv/system） | `python3 -m pip install doc-for-agent` | `docagent init --ai all` |

## Product CLI v1

主流程命令：

```bash
docagent init --ai <codex|claudecode|all>
docagent refresh --root <repo-root> --output-mode agent|human|dual|quad
docagent doctor --target <repo-root>
```

其他主命令：

```bash
docagent generate --root <repo-root> --mode refresh --output-mode agent|human|dual
docagent update --target <repo-root>
docagent versions --target <repo-root>
docagent quickstart --target <repo-root>
```

兼容命令（保留）：

```bash
docagent install --platform codex --target <repo-root>
docagent all --target <repo-root>
```

## 文档

入口文档路径：

1. [Landing Page（英文）](docs/landing-page.md) / [落地页说明（中文）](docs/landing-page.zh.md)
2. [Quickstart（英文）](docs/quickstart.md) / [快速开始（中文）](docs/quickstart.zh.md)
3. [Platform Guide（英文）](docs/platforms.md) / [平台指南（中文）](docs/platforms.zh.md)

这条链路用于 dual 文档系统上手：先看产品定位，再跑首轮命令，再选平台入口。

维护文档：

- [Maintainer Guide](docs/maintainers.md)
