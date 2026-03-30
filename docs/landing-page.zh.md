# 落地页原型说明

[English](landing-page.md) | 简体中文

当前仓库包含一个 React 落地页原型，用于公开产品入口展示。

## 位置

- `landing/`

## 目标

落地页面向 CLI coding-agent 用户，强调短路径：

1. install
2. init
3. refresh

两步入口模型：全局安装让 skill 对 coding agent 可见，repo-local init 为每个仓库启用工作流。
把 `refresh` 理解成安装完成后的“半步”：当仓库准备好后，由它负责写入或更新整套文档系统。
临时 Node 上手场景下，`npx -y doc-for-agent init ...` 可合并两步。
同时把 `doc-for-agent` 定位为“项目文档系统工具”，而不是一次性 markdown 生成器。
文档输出模型可按用户意图选择：`agent`、`human`、`dual`、`quad`。
模式映射：`agent` 面向 `AGENTS/`，`human` 面向 `docs/`，`dual` 同时覆盖两者，`quad` 覆盖 `AGENTS/`、`AGENTS.zh/`、`docs/`、`docs.zh/`。
`dual` 模式会在一次 refresh 流程中把 `docs/`（human docs）与 `AGENTS/`（agent docs）成对维护。`quad` 模式建立双语四视图布局。
产品对外叙事是双文档系统，而不是 AGENTS-only。

## 入口路径

从仓库入口文档开始，建议按这个顺序：

1. `README.md`
2. `docs/landing-page.zh.md`
3. `docs/quickstart.zh.md`
4. `docs/platforms.zh.md`

如果你更习惯英文文档，可按同样顺序使用不带 `.zh.md` 的版本。

## 本地预览

```bash
cd landing
npm install
npm run dev
```

## 另见

看完这里后，先去“快速开始”，再去“平台指南”。
这样可以把 dual 文档系统叙事与命令路径从头到尾保持一致。

- [Quickstart（英文）](quickstart.md) / [快速开始（中文）](quickstart.zh.md)
- [Platform Guide（英文）](platforms.md) / [平台指南（中文）](platforms.zh.md)
