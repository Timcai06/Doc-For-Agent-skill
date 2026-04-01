# Architecture Compatibility

## Top Rules (Read First)

- Rule 1: CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Rule 2: Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Rule 3: Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.

## Repo-Type Signals

- Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).

## Source Of Truth

- `README.md` for stated project goals, setup expectations, and user-facing examples
- `doc-for-agent/SKILL.md` for trigger conditions and maintainer workflow
- `doc-for-agent/agents/openai.yaml` for launcher/marketplace invocation metadata
- `doc-for-agent/scripts/` for generation behavior and repository scanning
- `doc-for-agent/references/` for documentation structure and writing constraints

## Supporting Doc Synthesis (Architecture)

### Confirmed

- CLI boundary: keep `docagent` as the single entry surface for `codex`, `claude`, `continue`, `copilot` workflows.
- Source-of-truth boundary: on conflicts, arbitrate against `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md` before changing CLI entry, adapter wiring, or distribution behavior.
- Distribution structure: keep platform mappings in adapter/config docs (`Claude Code` -> `docagent init --ai claudecode`) while CLI contract changes stay centralized.
- Conflict handling order: 1) check `readme.md`, `docs/platforms.md`, `docs/platforms.zh.md`; 2) then edit adapter/config mappings.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 (sources: `docs/platforms.zh.md`)

### Conflicting

- No direct architecture conflicts were synthesized from supporting docs.

### Unresolved

- No unresolved architecture items were synthesized from supporting docs.

## Referenced Architecture Docs

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`

## Compatibility Boundaries

- Prefer changing source code and configuration first, then refresh `AGENTS/` docs.
- Do not let generated docs drift away from the repository's actual entrypoints and workflows.
- Skill manifests, README examples, and generator output should describe the same capability surface.

## Conflicting Signals

- Skill markers dominate classification, but packaged tooling signals suggest this repository may also ship installable utilities.

## Preserved Notes

- 顶层规则 (首读必看)
  - Preserved from previous manual edits.
  - **规则 1：CLI 边界** —— 保持 `docagent` 作为所有智能体工作流（Codex, Claude, Continue, Copilot 等）的唯一入口界面。
  - **规则 2：事实来源边界** —— 在发生冲突时，应首先根据 `README.md` 和 `docs/platforms.zh.md` 提供的基准事实进行仲裁，随后再决定是否修改 CLI 入口或适配器逻辑。
  - **规则 3：分发结构** —— 确保平台映射关系保留在适配器配置中，而核心 CLI 契约的变更必须保持在引擎内部的中心化管理。
- 仓库类型识别信号
  - Preserved from previous manual edits.
  - **检测到 Skill 标记**：存在 `SKILL.md`、智能体清单文件（Manifests）以及已有的 `AGENTS/` 目录结构。
- 事实来源 (Source Of Truth)
  - Preserved from previous manual edits.
  - **`README.md`**：定义了项目目标、安装预期和用户示例。
  - **`doc-for-agent/SKILL.md`**：定义了智能体触发条件和维护者工作流。
  - **`doc-for-agent/agents/openai.yaml`**：提供了启动器和市场调用的元数据。
  - **`doc-for-agent/scripts/`**：定义了文档生成的具体行为和仓库扫描逻辑。
- 支撑文档综合 (架构维度)
  - Preserved from previous manual edits.
  ### 已确认 (Confirmed)

  - **入口一致性**：坚持使用 `docagent` 作为跨平台的统一入口。
  - **冲突处理顺序**：1) 检查核心文档；2) 随后才修改适配器/配置映射。

  ### 兼容性边界

  - **由于架构逻辑决定**：优先修改源代码和配置，随后通过刷新 `AGENTS/` 文档来同步。
  - **严禁偏差**：确保生成的文档绝不脱离仓库实际的入口点和工作流。
  - **一致性要求**：技能清单、README 示例与生成器输出必须描述同一个能力表面。
