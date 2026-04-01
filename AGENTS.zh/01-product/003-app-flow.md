# App Flow

## Surfaces Detected

- Agent manifest surface: `doc-for-agent/agents/openai.yaml`

## Guidance

- Treat the first visible or invoked surface as part of the product contract.
- Keep user-facing names aligned across README examples, manifests, routes, and commands.
- Treat install, invocation, and prompt surfaces as the equivalent of a frontend contract.

## Supporting Doc Synthesis (Flow)

### Confirmed

- Product positioning: this repository is scoped for CLI coding-agent workflows, not a standalone end-user application.
- Repository adaptation scope: fit repositories that need ongoing refresh/governance workflows, not one-off documentation scans.
- Retention value: prioritize repeatable `init -> refresh -> doctor` lifecycle checks so documentation stays governable, not a one-shot generator output.
- Positioning guardrail: describe `docagent` as an ongoing documentation system (`init/refresh/doctor/migrate`), not a one-shot markdown generator.
- 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 (sources: `docs/landing-page.zh.md`)

### Conflicting

- No direct flow conflicts were synthesized from supporting docs.

### Unresolved

- No unresolved flow items were synthesized from supporting docs.

## Preserved Notes

- 辅助参考文档提炼 (Flow)
  - Preserved from previous manual edits.
  ### 已确认的基准主张

  - 产品定位： 本代码库专注于 CLI 编程智能体工作流，而非独立的终端用户应用.
  - 仓库适配范围： 适用于需要持续刷新和治理工作流的仓库，而非一次性的文档扫描.
  - 留存价值： 优先保障可重复的 `init -> refresh -> doctor` 生命周期的可治理性 确保文档持续可控，而非一次性生成后的“僵尸”文档.
  - 定位护栏： 将 `docagent` 描述为一个持续运作的文档系统 (`init/refresh/doctor/migrate`), 而非一次性生成的 Markdown 工具.
  - 简路径（uipro-cli 风格）：npm install -g doc-for-agent@next -> docagent init --ai codex / docagent init --ai claudecode。 

  ### 待清理的矛盾点

  - No direct flow conflicts were synthesized .

  ### 悬而未决的问题

  - No unresolved flow items were synthesized .
