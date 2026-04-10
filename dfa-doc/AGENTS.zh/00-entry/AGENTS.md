# 智能体架构入口引导

## 核心目的

- 在智能体修改代码或文档前定义阅读顺序
- 陈述应在会话重置后保留的运行规则
- 为未来的智能体指明仓库的规范事实来源

## 阅读顺序

- `01-product/001-core-goals.md`
- `01-product/002-prd.md`
- `02-architecture/004-tech-stack.md`
- `01-product/003-app-flow.md`
- `02-architecture/006-backend-structure.md`
- `02-architecture/005-frontend-guidelines.md`
- `02-architecture/007-architecture-compatibility.md`
- `03-execution/008-implementation-plan.md`
- `04-memory/009-progress.md`
- `04-memory/010-lessons.md`

## 分层策略

- Contract pages（低波动规则层）: `00-entry/AGENTS.md`, `01-product/001-core-goals.md`, `01-product/002-prd.md`, `01-product/003-app-flow.md`, `02-architecture/004-tech-stack.md`, `02-architecture/005-frontend-guidelines.md`, `02-architecture/006-backend-structure.md`, `02-architecture/007-architecture-compatibility.md`, `03-execution/008-implementation-plan.md`
- Memory pages（累积记忆层）: `04-memory/009-progress.md`, `04-memory/010-lessons.md`
- Contract pages 在 refresh 时保持规则稳定，避免叙事性重写。
- Memory pages 用于持续记录项目进展、复盘和术语决策，允许追加式更新。

## 运行规则

- 在进行大范围重构前，先阅读产品和架构文档。
- 当仓库结构、工作流或术语发生实质变化后，刷新 `dfa-doc/AGENTS/`。
- 优先采用已确认事实，而不是猜测性的路线图措辞。
- 当刷新安全性重要时，用 manual blocks 保护手工维护的说明。
- 保持 skill 清单、SKILL.md 指令和生成器行为一致。

## 当前运行态势

- 保持技能定义、生成器行为与生成的文档同步。

## 规范事实来源

- `README.md`
- `docs/landing-page.md`
- `docs/landing-page.zh.md`
- `docs/maintainers.md`
