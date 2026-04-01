# 架构兼容性与规则

## 顶层护栏与核心规则 (首读必看)

- Rule 1: CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Rule 2: Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Rule 3: Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.

## 仓库类型判定信号

- Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).

## 事实来源 (Source of Truth)

- `README.md` for stated project goals, setup expectations, and user-facing examples
- `doc-for-agent/SKILL.md` for trigger conditions and maintainer workflow
- `doc-for-agent/agents/openai.yaml` for launcher/marketplace invocation metadata
- `doc-for-agent/scripts/` for generation behavior and repository scanning
- `doc-for-agent/references/` for documentation structure and writing constraints

## 辅助参考文档提炼 (Architecture)

### 已确认的基准主张

- CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.
- Conflict handling order: 1) check `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md`; 2) then edit adapter/config mappings.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 (sources: `docs/platforms.zh.md`)

### 待清理的矛盾点

- 未从支持文档中检测到直接的架构冲突。

### 悬而未决的问题

- 未从支持文档中检测到未决的架构事项。

## 核心参考历史文档

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`

## 兼容性边界规则

- Prefer changing source code and configuration first, then refresh `AGENTS/` docs.
- Do not let generated docs drift away from the repository's actual entrypoints and workflows.
- Skill manifests, README examples, and generator output should describe the same capability surface.

## 冲突项监控

- Skill markers dominate classification, but packaged tooling signals suggest this repository may also ship installable utilities.

## Preserved Notes

- 顶层规则
  - Preserved from previous manual edits.
  - **规则 1：CLI 入口单点化** —— 严格保持 `docagent` 作为所有智能体工作流 (Codex, Claude, Copilot, Continue) 的统一物理进入入口。
  - **规则 2：事实来源仲裁** —— 任何针对 CLI 逻辑或适配器的变更，均须优先根据 `README.md` 与产品定义的基准事实进行仲裁。
  - **规则 3：分发结构稳定性** —— 确保各平台映射（如工具调用的别名）保留在各适配器配置中，而核心 CLI 的行为契约保持中心化演进。
- 源头基准 (Source of Truth)
  - Preserved from previous manual edits.
  - **`README.md`**：项目愿景、全局安装预期、用户级示例。
  - **`doc-for-agent/SKILL.md`**：智能体任务剧本与维护者工作流共识。
  - **`doc-for-agent/scripts/`**：内部生成逻辑与仓库自动扫描事实点。
- 支撑文档综合 (架构维度)
  - Preserved from previous manual edits.
  ### 已确认的内容 (Confirmed)

  - **逻辑边界**：坚持使用 `docagent` 作为各平台的统一调用表面。
  - **冲突处理**：依次检查核心 README 和本地配置，严禁在来源冲突时进行随机变更。

  ### 潜在冲突项

  - **无**：当前未在支撑文档中检测到任何直接的架构级冲突。

  ### 未决事项

  - **新架构对齐**：针对未来可能引入的非 `layered` 文档方案，需预先定义其向后兼容逻辑。
