# 智能体架构入口引导

## 核心目的

- 在智能体修改代码或文档前定义阅读顺序
- 陈述应在会话重置后保留的运行规则
- 为未来的智能体指明仓库的规范事实来源

## 阅读顺序

- ``01-product/001-core-goals.md``
- ``01-product/002-prd.md``
- ``02-architecture/004-tech-stack.md``
- ``01-product/003-app-flow.md``
- ``02-architecture/006-backend-structure.md``
- ``02-architecture/005-frontend-guidelines.md``
- ``02-architecture/007-architecture-compatibility.md``
- ``03-execution/008-implementation-plan.md``
- ``04-memory/009-progress.md``
- ``04-memory/010-lessons.md``

## 运行规则

- Read product and architecture docs before broad refactors.
- Refresh `AGENTS/` after meaningful repo-shape, workflow, or terminology changes.
- Prefer confirmed facts over speculative roadmap language.
- Protect hand-maintained notes with manual blocks when refresh safety matters.
- Keep the skill manifest, SKILL.md instructions, and generator behavior aligned.

## 当前运行态势

- 保持技能定义、生成器行为与生成的文档同步。

## 规范事实来源

- `README.md`
- `docs/landing-page.md`
- `docs/landing-page.zh.md`
- `docs/maintainers.md`

## Preserved Notes

- 核心目标 (Purpose)
  - Preserved from previous manual edits.
  - **阅读指南**：定义 Agent 在修改代码或文档前应遵循的阅读顺序。
  - **运行规则**：明确在整个协作周期内必须遵守的运行准则。
  - **事实指引**：引导未来的 Agent 访问本仓库最权威的事实来源（Canonical Fact Sources）。
- 推荐阅读顺序 (Reading Order)
  - Preserved from previous manual edits.
  1.  `01-product/001-core-goals.md` —— 核心目标与护栏
  2.  `01-product/002-prd.md` —— 产品需求与用户画像
  3.  `02-architecture/004-tech-stack.md` —— 技术栈与环境依赖
  4.  `01-product/003-app-flow.md` —— 应用流与交互契约
  5.  `02-architecture/006-backend-structure.md` —— 核心逻辑结构
  6.  `02-architecture/007-architecture-compatibility.md` —— 架构兼容性与边界
  7.  `03-execution/008-implementation-plan.md` —— 实施计划与执行指南
  8.  `04-memory/009-progress.md` —— 核心进展记录
  9.  `04-memory/010-lessons.md` —— 经验教训备忘
- 顶层规则 (Rules)
  - Preserved from previous manual edits.
  - **对齐事实**：在进行大规模重构前，务必审阅产品和架构文档。
  - **同步刷新**：在仓库结构、工作流或核心术语发生重大变动后，必须运行 `docagent refresh` 以同步 `AGENTS/` 视图。
  - **事实优先**：优先采用已确认的代码事实，避免使用带有假设性质的路线图语言。
  - **手动块保护**：在刷新后保留由人类在 `<!-- doc-for-agent:manual-start -->` 块中维护的笔记。
- 事实来源 (Canonical Fact Sources)
  - Preserved from previous manual edits.
  - **Skill 标记**：检测到 `SKILL.md`、智能体清单文件（Manifests）以及已有的 `AGENTS/` 目录结构，判定本工程为技能元仓库。
