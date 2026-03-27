# doc-for-agent 快速开始

[English](quickstart.md) | 简体中文

本页面向第一次使用产品的用户。

只记住一个模型：

1. 安装
2. init
3. refresh

## 安装

Node：

```bash
npm install -g doc-for-agent
```

Python：

```bash
pipx install doc-for-agent
```

Node 一次性运行：

```bash
npx -y doc-for-agent
```

## Init

按需选择：

```bash
docagent init --ai <claude|codex|continue|copilot|all> --target <repo-root>
docagent init --ai claude --target <repo-root>
docagent init --ai codex --target <repo-root>
docagent init --ai continue --target <repo-root>
docagent init --ai copilot --target <repo-root>
docagent init --ai all --target <repo-root>
```

CodeBuddy 用户通常从下面开始：

```bash
docagent init --ai codex --target <repo-root>
```

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

- [Platform Guide（英文）](platforms.md) / [Platform Guide（中文）](platforms.zh.md)
- [Maintainer Guide](maintainers.md)

