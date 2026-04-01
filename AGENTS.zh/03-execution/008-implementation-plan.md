# Implementation Plan

## Current Operating Posture

- Keep the skill definition, generator behavior, and generated documentation in sync.

## Top Rules (Read First)

- Rule 1: Execution contract: `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` is the documented command order for setup, sync, and drift checks.
- Rule 2: Verification gate: workflow changes are not complete until `docagent doctor --target <repo-root>` pass.
- Rule 3: Execution constraints: keep `--target <repo-root>` explicit when commands run outside the target repo; keep `--output-mode agent` consistent across refresh runs; declare `--ai <platform>` explicitly so platform routing stays deterministic.
- Rule 4: Verification order: 1) `docagent doctor --target <repo-root>`; stop at the first failing command before running later checks.

## Immediate Next Steps

- Validate setup, run, and verify commands before broad edits.
- Refresh AGENTS docs after changing repository structure or workflow commands.

## Setup

```bash
npm install
```

## Run

```bash
Run the primary local command from README examples (app start, CLI invocation, or generator refresh).
```

## Verify

```bash
python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
python3 doc-for-agent/tests/verify_generator_snapshots.py
```

## Supporting Doc Synthesis (Execution)

### Confirmed

- Execution contract: `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` is the documented command order for setup, sync, and drift checks.
- Verification gate: workflow changes are not complete until `docagent doctor --target <repo-root>` pass.
- Execution constraints: keep `--target <repo-root>` explicit when commands run outside the target repo; keep `--output-mode agent` consistent across refresh runs; declare `--ai <platform>` explicitly so platform routing stays deterministic.
- Verification order: 1) `docagent doctor --target <repo-root>`; stop at the first failing command before running later checks.
- Failure triage priority: 1) run `docagent doctor` first to catch install/config drift; 2) reconcile command context with `README.md`; 3) cross-check setup assumptions in `docs/quickstart.md`; 4) inspect CI logs for command/environment mismatches; 5) if failures persist, roll back generated docs to last known-good state and rerun `docagent refresh`.
- Run `docagent init --ai codex` (sources: `README.md`, `docs/platforms.md` (+3 more))

### Conflicting

- No direct execution conflicts were synthesized from supporting docs.

### Unresolved

- No unresolved execution items were synthesized from supporting docs.

## Supporting Execution Docs

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`
- `docs/quickstart.md`
- `docs/quickstart.zh.md`

## Preserved Notes

- 核心工作流规则
  - Preserved from previous manual edits.
  - **设置与配置**：优先检查 `docagent doctor` 以确保多平台适配器路径正确无误。
  - **验证流程**：在本地修改后，必须运行 `node doc-for-agent/installer/node/docagent.js refresh`（或全局 `docagent refresh`）验证四视图同步性。
  - **故障排除**：若出现参数不支持报错（Unrecognized arguments），优先核查是否安装了旧版本 npm 包或资产同步是否缺失。
- 已确认的实施细节
  - Preserved from previous manual edits.
  - 本仓库当前处于 **快速交付与架构重构** 阶段。
  - 实施重心已从“纯工具开发”转向“智能体原生能力集成”。
  - 发布流程：`sync_assets.py` -> `npm publish`。
