import re

def translate_to_zh(text: str) -> str:
    # 详尽的翻译映射表：致力于实现“全中文”输出，覆盖从骨架标题到具体分析句式的翻译。
    
    mapping = [
        # --- 顶级标题 ---
        ("# AGENTS", "# 智能体核心架构总览"),
        ("# Product", "# 产品意图与业务核心"),
        ("# Architecture", "# 系统架构与边界"),
        ("# Execution", "# 运行与执行手册"),
        ("# Memory", "# 术语表与知识记忆"),
        ("# Project Overview", "# 项目总体概览"),
        
        # --- 二级标题与结构块 ---
        ("## What This Project Is", "## 项目定位与愿景"),
        ("## Best Used For", "## 最佳适用场景"),
        ("## Dual Documentation System", "## 独创：双重视图文档架构"),
        ("## Repository Classification", "## 代码仓库分类与判定"),
        ("## Files", "## 核心文件结构清单"),
        ("## Top Rules (Read First)", "## 核心护栏与顶层规则 (首读必看)"),
        ("## Confirmed Facts", "## 已确认的客观事实"),
        ("## Constraints To Preserve", "## 严禁打破的开发约束"),
        ("## Supporting Doc Synthesis", "## 辅助参考文档提炼"),
        ("## Referenced Repository Docs", "## 核心参考代码区与文档"),
        ("## Open Questions", "## 核心决策待填补区"),
        ("## Setup", "## 环境配置序列"),
        ("## Run", "## 本地运行路径"),
        ("## Verify", "## 验证流程卡点"),
        ("## Synthesis Summary", "## 全局上下文提炼"),
        ("## Knowledge Status", "## 仓库知识健康度"),
        ("## Operational Notes", "## 运维与上线防坑记录"),
        ("## Update Triggers", "## 文档刷新触发条件"),
        ("## Maintenance Workflow", "## 文档日常维护流"),
        ("## Bootstrap Backlog", "## 冷启动阶段待办"),
        ("## Provenance", "## 溯源证明"),
        ("## Document Contract", "## 文档与执行层契约"),
        ("## Dual Sync Checklist", "## 双重视图对齐检查清单"),
        ("## Paired Refresh Rules", "## Quad模式下的同步规则"),
        ("## Dual Pairing Contract (Rules)", "## 双视图强制对齐契约"),
        ("## Output Boundary (Human vs Agent)", "## 边界定义：人读区 vs 机读区"),
        ("## Dual View Rationale", "## 双向视图设计逻辑"),
        ("## Preserved Notes", "## 已保留的旧版笔记"),
        ("## Intended Audience", "## 目标读者与受众"),
        ("## Key Entry Points", "## 关键入口点"),
        ("## Current Priorities", "## 当前任务优先级"),
        ("## Documentation Gaps To Close", "## 待填补的文档空白"),

        # --- 三级标题与状态标签 ---
        ("### Confirmed Facts", "### 确凿的基准事实"),
        ("### Confirmed Rules", "### 核心确立的规则库"),
        ("### Supporting Signals", "### 高价值辅助参考信号"),
        ("### Decision Backlog", "### 尚未决策的高风险清单"),
        ("### Conflict Watchlist", "### 矛盾与冲突预警监控"),
        ("### Confirmed", "### 已确认的基准主张"),
        ("### Conflicting", "### 待清理的矛盾点"),
        ("### Unresolved", "### 悬而未决的问题"),

        # --- 核心分析语句 (builders.py 中的硬编码内容) ---
        # 1. 产品定位类
        ("Product positioning:", "产品定位："),
        ("Repository adaptation scope:", "仓库适配范围："),
        ("Retention value:", "留存价值："),
        ("Positioning guardrail:", "定位护栏："),
        ("this repository is scoped for CLI coding-agent workflows, not a standalone end-user application", "本代码库专注于 CLI 编程智能体工作流，而非独立的终端用户应用"),
        ("fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans", "适用于需要持续刷新和治理工作流的仓库，而非一次性的文档扫描"),
        ("prioritize repeatable `init -> refresh -> doctor` lifecycle checks", "优先保障可重复的 `init -> refresh -> doctor` 生命周期的可治理性"),
        ("describe `docagent` as an ongoing documentation system", "将 `docagent` 描述为一个持续运作的文档系统"),
        ("so documentation stays governable, not a one-shot generator output", "确保文档持续可控，而非一次性生成后的“僵尸”文档"),
        ("not a one-shot markdown generator", "而非一次性生成的 Markdown 工具"),
        
        # 2. 架构与边界类
        ("Architecture rationale lives in", "架构设计逻辑存放于"),
        ("while operational boundaries for agents live in paired AGENTS architecture docs", "而针对智能体的运行边界规则存放于配套的 AGENTS 架构文档中"),
        ("Architecture is split between a frontend surface and a backend/runtime surface", "系统架构分为前端展现层与后端/运行时层"),
        ("Source-of-truth boundary:", "真相源边界："),
        ("CLI boundary:", "CLI 交互边界："),
        ("Build-path rule:", "构建路径规则："),
        ("Distribution structure:", "分发结构："),
        
        # 3. 约束与规则类
        ("Avoid drifting away from the repository's real code", "避免偏离仓库真实的业务代码、脚本和命名规范"),
        ("Prefer stable entrypoints and contracts over broad structural churn", "优先保持稳定的入口和契约，而不是进行大规模的解构"),
        ("Review mixed signals before collapsing the repository into a single simplistic mental model", "在将仓库简化为单一思维模型前，务必审查各种交错的信号"),
        
        # 4. 执行与维护类
        ("Assign one maintainer owner for this document", "为此文档分配一名维护责任人"),
        ("Update this page in the same PR as behavior changes", "在代码行为变更的同一个 PR 中同步更新此页面"),
        ("Review this document at least once per sprint", "每个 Sprint 至少评审一次此文档"),
        ("Keep setup/run/verify/triage order executable", "保持 安装/运行/验证/排障 命令序列在干净环境下可执行"),
        ("Primary command workflow centers on", "核心命令流工作流集中于"),
        ("Verification gate:", "验证关卡："),
        ("Verification order:", "验证顺序："),
        ("Execution contract:", "执行契约："),
        ("Failure triage priority:", "失败排查优先级："),
        ("Execution constraints:", "执行约束条件："),
        ("When setup/run/verify commands change, update this runbook immediately", "当 安装/运行/验证 命令变更时，请立即更新此手册"),
        ("When CI checks or release gates change, sync the Verify and Operational Notes sections", "当 CI 检查或发布门禁变更时，请同步更新验证与运维部分"),
        ("Record setup, execution, verification, and refresh commands", "记录安装、执行、验证和刷新的命令流水"),
        ("on failures, triage install/config drift first", "遇到执行失败时，优先排查安装和配置漂移"),

        # 5. 空结果提示
        ("No direct product conflicts were synthesized", "未检测到直接的产品内容冲突"),
        ("No unresolved product items were synthesized", "未检测到未决的产品内容项"),
        ("No direct project conflicts were synthesized", "未检测到直接的项目内容冲突"),
        ("No unresolved project items were synthesized", "未检测到未决的项目内容项"),
        ("No direct architecture conflicts were synthesized", "未检测到直接的架构冲突"),
        ("No unresolved architecture items were synthesized", "未检测到未决的架构项"),
        ("No direct execution conflicts were synthesized", "未检测到直接的执行冲突"),
        ("No unresolved execution items were synthesized", "未检测到未决的执行项"),
        ("No major synthesis conflicts were detected", "未检测到严重的规则提炼冲突"),
        ("No major product documentation gaps were detected", "未检测到明显的产品文档空白"),
        ("from supporting docs", ""),
        ("from supporting sources", ""),

        # 6. 其他常用词汇与长短语
        ("This page is maintainer-facing source-of-truth for its domain", "本页面是该领域面向维护者的真相源"),
        ("keep it synchronized with `AGENTS/` in dual mode", "保持其在双重模式下与 `AGENTS/` 的同步"),
        ("as the human-view root", "作为人类视角的根目录"),
        ("avoid narrative-only refreshes without command or contract changes", "避免在没有命令或契约更改的情况下进行纯叙述性的刷新"),
        ("Record scope decisions as explicit rules and owners", "将范围决策记录为明确的规则和负责人"),
        ("move stale discussion text to decision backlog", "将过时的讨论文本移至决策后台"),
        ("Repository maintainers responsible for day-to-day delivery", "负责日常交付和运营稳定的仓库维护者"),
        ("Skill maintainers keeping manifests, prompts, and generator behavior aligned", "负责保持清单、提示词与生成器行为一致的技能维护者"),
        ("Current repo shape:", "当前仓库形态："),
        ("Wait for manual confirmation", "等待人工确认"),
        ("English | [简体中文](README.zh.md)", "[English](README.md) | 简体中文"),
        ("and operational stability", "以及运营稳定性"),
        ("for its domain", ""),
        
        # --- 规则序数 ---
        ("- Rule 1:", "- 第一原则："),
        ("- Rule 2:", "- 第二原则："),
        ("- Rule 3:", "- 第三原则："),
        ("- Rule 4:", "- 第四原则："),
        ("- Rule 5:", "- 第五原则："),
        ("- Rule 6:", "- 第六原则："),
        ("- Rule 7:", "- 第七原则："),
        ("- Rule 8:", "- 第八原则："),
    ]
    
    translated = text
    # 按照优先级顺序进行批量替换 (从长到短)
    mapping.sort(key=lambda x: len(x[0]), reverse=True)
    for en, zh in mapping:
        translated = translated.replace(en, zh)
        
    # --- 动态正则替换 ---
    # 统计信息
    translated = re.sub(r"Sources analyzed: `(\d+)`", r"已分析信源数量：`\1`", translated)
    translated = re.sub(
        r"Synthesized statements: `(\d+)` confirmed, `(\d+)` conflicting, `(\d+)` unresolved",
        r"成功提炼结论：`\1` 条确认，`\2` 条矛盾，`\3` 条未决",
        translated)
    
    # 路径对齐提示
    translated = re.sub(r"human locale `zh` maps to `human.zh/`", r"中文语言包 `zh` 映射至 `human.zh/` 目录", translated)
    translated = re.sub(r"Path pair rule: `(.*)` pairs with `(.*)` for (.*)", r"路径对齐规则：`\1` 与 `\2` 结对，用于 \3", translated)
    
    # 对 for 引导的用途进行补充翻译
    translated = translated.replace("for agent-facing product rules and scope guardrails", "智能体侧的产品规则与范围护栏")
    translated = translated.replace("for agent-facing user and outcome contract", "智能体侧的用户与交付契约")
    translated = translated.replace("for agent-facing flow and entry-surface notes", "智能体侧的流程与入口说明")
    translated = translated.replace("for setup, verify, and failure-triage order", "安装、验证与排障顺序")

    # 溯源后缀去掉（实现全中文观感）
    translated = re.sub(r"\(sources: `.*`\)", "", translated)

    # 仓库分类标签
    translated = translated.replace("`skill/meta repository`", "`技能/元数据类仓库`")
    translated = translated.replace("`web-app`", "`Web 应用程序`")
    translated = translated.replace("`cli-tool`", "`CLI 工具类仓库`")
    translated = translated.replace("`library-sdk`", "`库/SDK 类仓库`")
    translated = translated.replace("`backend-service`", "`后端服务类仓库`")
    
    return translated
