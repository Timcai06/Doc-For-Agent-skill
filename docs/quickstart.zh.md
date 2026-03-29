# doc-for-agent 快速开始

[English](quickstart.md) | 简体中文

本页面向第一次使用产品的用户。

只记住一个模型：

1. 安装
2. init
3. refresh

`refresh` 支持 `agent`、`human`、`dual` 三种文档输出。
模式映射：`agent` -> `AGENTS/`，`human` -> `docs/`，`dual` -> 两者同时输出。
这条路径不是 AGENTS-only；按需要选择 `human` 或 `dual`。

## 安装

Node：

```bash
npm install -g doc-for-agent
```

Python：

```bash
pipx install doc-for-agent
```

Node 一次性开始（无需全局安装）：

```bash
npx -y doc-for-agent init --ai all --target <repo-root>
```

如果你只需要单个平台，把 `all` 替换成 `claude`、`codex`、`continue` 或 `copilot`。

## Init

统一命令形态：

```bash
docagent init --ai <claude|codex|continue|copilot|all> --target <repo-root>
```

常见选择：

```bash
docagent init --ai all --target <repo-root>
docagent init --ai claude --target <repo-root>
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
