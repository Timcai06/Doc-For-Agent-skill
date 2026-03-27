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

同时把 `doc-for-agent` 定位为“项目文档系统工具”，而不是一次性 markdown 生成器。

## 入口路径

从仓库入口文档开始，建议按这个顺序：

1. `README.md`
2. `docs/landing-page.md`
3. `docs/quickstart.md`
4. `docs/platforms.md`

## 本地预览

```bash
cd landing
npm install
npm run dev
```

## 另见

- [Quickstart（英文）](quickstart.md) / [Quickstart（中文）](quickstart.zh.md)
- [Platform Guide（英文）](platforms.md) / [Platform Guide（中文）](platforms.zh.md)
