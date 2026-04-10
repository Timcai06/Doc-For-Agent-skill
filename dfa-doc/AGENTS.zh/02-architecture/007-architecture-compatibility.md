# 架构兼容性与规则

## 顶层护栏与核心规则 (首读必看)

- 第一原则： CLI 边界： 保持 `docagent` 作为 `codex`、`claudecode`、`continue`、`copilot` 工作流的统一入口。
- 第二原则： 真相源边界： 当出现冲突时，在修改 CLI 入口、adapter wiring 或分发行为前，先以 `readme.md`、`docs/platforms.md`、`docs/platforms.zh.md` 为裁决依据。
- 第三原则： 分发结构： 将平台映射保留在 adapter/config 文档中（`Claude Code` -> `docagent init --ai claudecode`），而 CLI 契约变更保持集中管理。

## 仓库类型判定信号

- 检测到 skill 标记（`SKILL.md`、agent 清单或现有 `AGENTS/` 目录）。

## 事实来源 (Source of Truth)

- `README.md` for stated project goals, setup expectations, and user-facing examples
- `doc-for-agent/SKILL.md` for trigger conditions and maintainer workflow
- `doc-for-agent/agents/openai.yaml` for launcher/marketplace invocation metadata
- `doc-for-agent/scripts/` for generation behavior and repository scanning
- `doc-for-agent/references/` for documentation structure and writing constraints

## 辅助参考文档提炼 (Architecture)

### 已确认的基准主张

- CLI 边界： 保持 `docagent` 作为 `codex`、`claudecode`、`continue`、`copilot` 工作流的统一入口。
- 真相源边界： 当出现冲突时，在修改 CLI 入口、adapter wiring 或分发行为前，先以 `readme.md`、`docs/platforms.md`、`docs/platforms.zh.md` 为裁决依据。
- 分发结构： 将平台映射保留在 adapter/config 文档中（`Claude Code` -> `docagent init --ai claudecode`），而 CLI 契约变更保持集中管理。
- 冲突处理顺序：1）检查 `readme.md`、`docs/platforms.md`、`docs/platforms.zh.md`；2）再编辑 adapter/config 映射。
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent -> docagent init --ai codex / docagent init --ai claudecode。 

### 待清理的矛盾点

- 未从支持文档中检测到直接的架构冲突。

### 悬而未决的问题

- 未从支持文档中检测到未决的架构事项。

## 核心参考历史文档

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`

## 兼容性边界规则

- 优先先改源码和配置，再刷新 `dfa-doc/AGENTS/` 文档。
- 不要让生成文档偏离仓库真实的入口点和工作流。
- skill 清单、README 示例和生成器输出应描述同一能力边界。

## 冲突项监控

- skill 标记主导了当前分类结果，但已打包工具链的信号表明该仓库也可能提供可安装工具。
