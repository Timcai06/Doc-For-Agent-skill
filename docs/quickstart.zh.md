# doc-for-agent 快速开始

[English](quickstart.md) | 简体中文

本页面向第一次使用产品的用户。

只记住一个模型：

1. 安装
2. init
3. refresh
把它理解成“两步半”最合适：全局安装负责 agent 可见性，repo-local init 负责仓库工作流，随后在需要写入或更新文档时再执行 refresh。

`refresh` 支持 `agent`、`human`、`dual`、`quad` 四种文档输出。
模式映射：`agent` -> `AGENTS/`，`human` -> `docs/`，`dual` -> 两者同时输出，`quad` -> `AGENTS/`、`AGENTS.zh/`、`docs/`、`docs.zh/`。
`dual` 模式会在一次 refresh 流程中把 `docs/`（human docs）与 `AGENTS/`（agent docs）成对维护。`quad` 模式建立双语四视图目录契约。
这条路径不是 AGENTS-only；按需要选择 `human` 或 `dual`。

## 安装
步骤 1（全局安装）：让 coding agent 能看到这个 skill。
简路径（`uipro-cli` 风格）：`npm install -g doc-for-agent@next` -> `docagent init --ai codex` / `docagent init --ai claudecode`。

Node：

```bash
npm install -g doc-for-agent@next
```

Python：

```bash
pipx install doc-for-agent
```

Node 一次性开始（无需全局安装）：

```bash
npx -y doc-for-agent init --ai all --target <repo-root>
```
该一次性命令会在临时场景下合并“全局安装 + repo-local init”。如果你要真正生成或更新文档，后一步仍然是执行 `refresh`。

如果你只需要单个平台，把 `all` 替换成 `claudecode`、`codex`、`continue` 或 `copilot`。

## Init

步骤 2（repo-local init）：在目标仓库启用工作流。

如果你只需要让 agent 看见这个 skill，使用短命令：

```bash
docagent init --ai codex
docagent init --ai claudecode
```

如果你还要同时接线当前仓库，使用 repo-local 形态：

```bash
docagent init --ai <codex|claudecode|continue|copilot|all> --target <repo-root>
```

常见选择：

```bash
docagent init --ai all --target <repo-root>
docagent init --ai claudecode --target <repo-root>
docagent init --ai codex --target <repo-root>
```

CodeBuddy 用户通常从 `--ai codex` 开始。

## Refresh

只生成 agent 文档：

```bash
docagent refresh --root <repo-root> --output-mode agent
```

只生成 human 文档：

```bash
docagent refresh --root <repo-root> --output-mode human
```

同时生成两套：

```bash
docagent refresh --root <repo-root> --output-mode dual
docagent refresh --root <repo-root> --output-mode quad
```

## 验证

```bash
docagent doctor --target <repo-root>
docagent versions --target <repo-root>
```

另见：
入口链路提醒：`README.md` -> `docs/landing-page.zh.md` -> `docs/quickstart.zh.md` -> `docs/platforms.zh.md`。
- [Landing Page（英文）](landing-page.md) / [落地页说明（中文）](landing-page.zh.md)
- [Platform Guide（英文）](platforms.md) / [平台指南（中文）](platforms.zh.md)
- [Maintainer Guide](maintainers.md)
