# 前端与交互准则

## 流程指引

- Keep user-facing routes, labels, prompts, or commands stable unless the repository intentionally renames them.
- Review README examples and visible entry surfaces before changing interaction flows.
- Treat skill manifests, trigger phrasing, and invocation prompts as the user-facing interface.
- Do not let manifest language drift away from what the generator actually supports.

## 事实凭证与识别

- Detected manifest: `doc-for-agent/agents/openai.yaml`

## Preserved Notes

- 核心引导逻辑
  - Preserved from previous manual edits.
  - **界面稳定性**：除非本库有明确更名计划，否则必须确保面向用户的路由、标签、Prompt 提示词或子命令名称的高度稳定。
  - **入口契约优先**：在修改任何交互逻辑前，必须先行审阅 `README` 示例和所有可见的入口位置（Entry Surfaces）。
  - **用户界面定义**：在本项目语境下，技能清单 (Manifests)、触发短语及其关联的 Prompt 共同构成了系统的“交互界面”。
