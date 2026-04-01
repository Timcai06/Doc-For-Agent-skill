# 后端逻辑架构

## 核心映射职责

- Identify the runtime or automation entrypoint before changing behavior.
- Treat outputs, contracts, and side effects as downstream-facing surfaces.
- The generator script and helper scripts are the backend-like execution layer.

## 运行时入口点

- `doc-for-agent/scripts/init_agents_docs.py`
- `doc-for-agent/scripts/render_platform_adapter.py`

## 稳定契约字段

- 未自动检测到稳定的契约字段。

## 存储与输出规则

- 未自动检测到存储或输出规则。

## Preserved Notes

- 核心职责
  - Preserved from previous manual edits.
  - **识别入口点**：在修改核心逻辑前，优先识别脚本执行或自动化行为的物理入口点。
  - **输出契约定义**：将生成的文档目录块、配置文件及其 side-effect 本地效应，视为后端直接消费的“交互契约面”。
  - **系统逻辑层级**：在本仓库中，分析引擎 (Analysis Engine)、生成器 (Generator) 和资产同步脚本共同构成了本系统的执行后端。
- 运行时入口点 (Runtime Entry Points)
  - Preserved from previous manual edits.
  - **`doc-for-agent/scripts/init_agents_docs.py`** —— 核心文档生成引擎，负责扫描与事实提取。
  - **`doc-for-agent/scripts/render_platform_adapter.py`** —— 负责将仓库元数据同步至各平台适配器。
- 稳定性与约束
  - Preserved from previous manual edits.
  - **输出边界**：四视图对应的文档目录即为本系统的输出核心。
  - **验证手段**：任何后端逻辑更迭，均须通过 `docagent refresh` 指令的全量回归。
