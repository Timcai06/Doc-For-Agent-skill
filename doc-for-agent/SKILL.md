---
name: "doc-for-agent"
description: "智理化刷新 Quad-View 仓库文档 (中英双语 / Agent+Human 视角)"
---
# doc-for-agent 智理化刷新剧本 (Playbook)

当你收到“刷新文档”或“同步仓库文档”的任务时，请将自己视为本仓库的**文档治理专家**，而非简单的命令执行器。请严格遵循以下四阶段闭环工作流：

## 阶段 1：事实提取 (Machine Layer)
**执行指令**：`docagent refresh --output-mode quad`
- 这一步利用 Python 引擎执行 AST 扫描和事实捕获。
- **注意**：引擎产出的 `.zh` 目录（`AGENTS.zh/` 和 `human.zh/`）仅作为事实基准，可能包含未翻译的英文碎片。

## 阶段 2：全量智理校阅 (Recursive Refinement)
**职责边界**：你是最后一道“中文化”防线。
- **必须遍历**：你必须主动检查并进入 `.zh` 目录下的【每一个】子文件（001 到 010+）。
- **严禁偷懒**：严禁仅处理首页。如果子文件（如 `004-tech-stack.md`）中包含英文 Rules 或 Facts，你必须利用你的 LLM 背景理解，将其全部重塑为地道、专业的母语。
- **保护契约**：严禁删除或修改被 `<!-- doc-for-agent:manual-start -->` 包裹的人类手动维护块。

## 阶段 3：架构与产品对齐 (Cross-View Sync)
- 确保 `human.zh/overview.md` 中的宏观决策在 `AGENTS.zh/` 对应的子文档中得到了正确的拆解和落地。
- 参考 `human.zh/glossary.md` 中的术语定义，确保全书用词统一。

## 阶段 4：质量门禁 (Verification Gate)
在确认任务完成前，请进行自我 audit：
1. **中文纯度**：`.zh` 目录下是否还存在生硬的英文 Facts 碎片？
2. **全量覆盖**：是否漏掉了某个深度目录（如 `02-architecture/`）？
3. **可维护性**：生成的路径链接是否在 Quad-View 下依然有效？

---

## 常用命令索引

- **初始化**：`docagent init --ai codex --target .`
- **全量刷新**：`docagent refresh --output-mode quad`
- **健康检查**：`docagent doctor --target .`
- **版本对齐**：`docagent versions`
