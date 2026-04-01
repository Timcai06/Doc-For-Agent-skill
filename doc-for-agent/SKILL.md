---
name: "doc-for-agent"
description: "智能体原生 (Agent-Native) 全量仓库智理剧本"
---
# doc-for-agent 智理化刷新剧本 (Agent-Native Playbook)

当你执行此技能时，请将自己视为本仓库的**“首席文档架构师”**。本技能已进化至 **原生对齐 (Native Alignment)** 架构，实现了基于事实的多视图同步。

## ⚠️ 核心工作流 (The Triad Loop)

### 阶段 1：机器事实提取 (Machine Layer)
**执行指令**：`docagent refresh --output-mode quad`
- **原生优势**：引擎已集成全量 `locales.py`。生成的 `.zh` 视图（`AGENTS.zh/` 和 `human.zh/`）默认已具备 **100% 纯净的中文标题与系统逻辑**。
- **职责**：确保命令在目标目录中成功执行，生成四视图基准。

### 阶段 2：逻辑智理与对齐 (Logic Refinement)
**职责边界**：你不再是一个翻译者，而是一个**“规则审计员”**。
- **事实对齐**：遍历 `AGENTS.zh/` 下的子文件（001 到 010+），核实引擎提取的“已确认事实”是否与代码现状、PRD 或 `SKILL.md` 的最新定义一致。
- **母语级精修**：针对核心产品逻辑、技术栈细节进行地道润色，确保表达符合“高级软件工程师”的沟通直觉。
- **Quad-View 校准**：确保英文视图 (`AGENTS/`) 保持纯净英文，中文视图 (`AGENTS.zh/`) 保持纯净中文，严禁出现语言漂移。

### 阶段 3：架构一致性审计 (Architectural Consistency)
- **索引对正**：核实 `AGENTS.zh/AGENTS.md` 是否已作为根索引文件，并清晰引导了阅读路径。
- **术语同步**：对照 `human.zh/glossary.md` 中的定义，确保所有视图中的业务名词解释（如 `skill-meta`, `dual-sync`）高度统一。

## 🚥 质量门禁 (Verification Gate)

1. **语言纯度**：英/中两个视图是否都实现了 100% 的语言解耦？
2. **事实精准度**：文档中的 CLI 命令、路径和包管理器名称是否与代码实际完全一致？
3. **入口透明度**：根目录下的 `AGENTS.md` 是否已正确建立？

---

## 常用命令参考

- **深度初始化**：`docagent init --ai codex --target .`
- **全量 Quad 刷新**：`docagent refresh --output-mode quad`
- **配置漂移检查**：`docagent doctor --target .`
- **版本对齐校验**：`docagent versions`
