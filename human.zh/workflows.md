# Workflows

## Top Rules (Read First)

- Rule 1: Execution contract: `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` is the documented command order for setup, sync, and drift checks.
- Rule 2: Verification gate: workflow changes are not complete until `docagent doctor --target <repo-root>` pass.
- Rule 3: Execution constraints: keep `--target <repo-root>` explicit when commands run outside the target repo; keep `--output-mode agent` consistent across refresh runs; declare `--ai <platform>` explicitly so platform routing stays deterministic.
- Rule 4: Verification order: 1) `docagent doctor --target <repo-root>`; stop at the first failing command before running later checks.

## Document Contract

- This page is maintainer-facing source-of-truth for its domain; keep it synchronized with `AGENTS/` in dual mode and `human.zh/` as the human-view root.
- Update this page in the same PR as behavior changes; avoid narrative-only refreshes without command or contract changes.
- Keep setup/run/verify/triage order executable from a clean checkout before marking this page done.

## Dual Sync Checklist

- After edits, refresh in dual mode and verify both `AGENTS/` and `human.zh/` were updated in the same change set.
- If one side changed without the other, treat it as documentation drift and resolve before merge.
- Run documented verify commands after refresh and keep failure-triage order aligned across both doc systems.

## Paired Refresh Rules

- Refresh contract: run one refresh/generate action that updates paired views together; do not patch one locale/audience in isolation.
- Path contract: verify changed files include both `AGENTS*/` and `docs*/` counterparts when behavior changes affect shared source-of-truth.
- Quad-mode contract: when using `--output-mode quad`, validate all four roots (`AGENTS/`, `AGENTS.zh/`, `docs/`, `docs.zh/`) in the same review cycle.
- Execution pairing rule: if `human.zh/workflows.md` changes due to command/order updates, refresh paired execution paths under both AGENTS roots.

## Dual Pairing Contract (Rules)

- Pairing mode rule: in `dual`, human and agent docs are generated from one analysis pass and must be reviewed as one change set.
- Locale-output rule: human locale `zh` maps to `human.zh/`.
- Template rule: human template variant `paired-core` is part of the pairing contract and must remain consistent across paired docs.
- Path pair rule: `human.zh/workflows.md` pairs with `AGENTS/03-execution/008-implementation-plan.md` for setup, verify, and failure-triage order.

## Paired Agent Docs (Dual Mode)

- `AGENTS/03-execution/008-implementation-plan.md` for setup, verify, and failure-triage order.

## Output Boundary (Human vs Agent)

- Use `human.zh/` for maintainer-facing policy and decisions; use `AGENTS/` for execution order, command wiring, and handoff runbooks.
- If a change affects both reader types, update both systems in one dual refresh cycle instead of patching only one side.
- Keep maintainer runbook context in `human.zh/workflows.md`; keep step-by-step agent execution plan in `AGENTS/workflows.md` (or layered execution docs).

## Dual View Rationale

- `human.zh/` and `AGENTS/` are two views generated from the same repository analysis and source-of-truth anchors.
- When the two views diverge, treat it as refresh drift rather than independent documentation authority.
- Maintainer runbook context lives in `human.zh/workflows.md`, while step ordering for agent actions lives in paired AGENTS execution docs.

## Setup

```bash
npm install
```

## Run

```bash
Run the main local command from README examples.
```

## Verify

```bash
python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
python3 doc-for-agent/tests/verify_generator_snapshots.py
```

## Synthesis Summary

- Sources analyzed: `5`
- Synthesized statements: `6` confirmed, `0` conflicting, `0` unresolved

## Knowledge Status

### Confirmed Rules

- Execution contract: `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` is the documented command order for setup, sync, and drift checks.
- Verification gate: workflow changes are not complete until `docagent doctor --target <repo-root>` pass.
- Execution constraints: keep `--target <repo-root>` explicit when commands run outside the target repo; keep `--output-mode agent` consistent across refresh runs; declare `--ai <platform>` explicitly so platform routing stays deterministic.
- Verification order: 1) `docagent doctor --target <repo-root>`; stop at the first failing command before running later checks.
- Failure triage priority: 1) run `docagent doctor` first to catch install/config drift; 2) reconcile command context with `README.md`; 3) cross-check setup assumptions in `docs/quickstart.md`; 4) inspect CI logs for command/environment mismatches; 5) if failures persist, roll back generated docs to last known-good state and rerun `docagent refresh`.

### Supporting Signals

- Primary command workflow centers on `npm` package scripts and repository-local verify commands.

### Decision Backlog

- No unresolved execution items were synthesized from supporting docs.

### Conflict Watchlist

- No direct execution conflicts were synthesized from supporting docs.

## Operational Notes

- Keep command examples in this file aligned with CI and README instructions.

## Update Triggers

- When setup/run/verify commands change, update this runbook immediately.
- When CI checks or release gates change, sync the Verify and Operational Notes sections.

## Maintenance Workflow

- Assign one maintainer owner for this document and update it in the same pull request as behavior changes.
- Review this document at least once per sprint or before each release cut.
- Update after setup/run/verify command changes or CI workflow updates.
- No major synthesis conflicts were detected; focus on keeping this page current with implementation changes.

## Bootstrap Backlog (When Docs Are Thin)

- Supporting docs were found; continue consolidating them into this page and archive stale duplicates.

## Provenance

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`
- `docs/quickstart.md`
- `docs/quickstart.zh.md`

## Preserved Notes

- 顶层规则 (首读必看)
  - Preserved from previous manual edits.
  - **规则 1：执行契约** —— 标准的操作顺序为：`docagent init` -> `docagent refresh` -> `docagent doctor`。这是环境配置、同步及其漂移检查的标准路径。
  - **规则 2：验证门禁** —— 在 `docagent doctor` 验证通过之前，任何关于文档工作流的变更均视为未完成。
  - **规则 3：执行约束** —— 当在目标仓库目录外运行命令时，必须显式指明 `--target` 参数；在多次刷新过程中应保持 `--output-mode` 参数的一致性。
  - **规则 4：验证顺序** —— 1) 首先运行 `docagent doctor`；若出现失败项，应立即停止并排查，严禁带病运行后续检查。
- 文档维护契约
  - Preserved from previous manual edits.
  - **事实来源**：本页面是维护者维度的核心事实来源。在双视图模式下，必须确保其与 `AGENTS/` 目录以及 `human.zh/` 根视图的高度同步。
  - **变更驱动**：仅在行为发生实际变更时更新本页面，避免仅进行无实质命令变动的叙述性刷新。
- 双视图同步清单
  - Preserved from previous manual edits.
  - **对齐检查**：编辑后，在 `dual` 模式下刷新并验证双端文档是否在同一个变更集中。
  - **漂移处理**：如果发现一侧更新而另一侧未动，应将其视为“文档漂移”，必须在合并代码前予以解决。
- 结对刷新规则 (Pairing Rules)
  - Preserved from previous manual edits.
  - **刷新契约**：必须执行能够同时更新配对视图的刷新动作；严禁孤立地修补单一受众的文档。
  - **四视图契约**：使用 `--output-mode quad` 时，需在一个评审周期内同时验证四个根目录（`AGENTS/`, `AGENTS.zh/`, `docs/`, `docs.zh/`）。
- 关键流程节点
  - Preserved from previous manual edits.
  ### 环境初始化 (Setup)
  ```bash
  npm install
  ```

  ### 核心运行 (Run)
  ```bash
  # 执行 README 示例中的本地核心命令
  ```

  ### 验证门禁 (Verify)
  ```bash
  # 运行单元测试与生成器快照验证
  python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
  python3 doc-for-agent/tests/verify_generator_snapshots.py
  ```
- 知识状态与故障排查
  - Preserved from previous manual edits.
  ### 确认的规则
  - **故障排查优先级**：1) 运行 `docagent doctor` 捕获配置漂移；2) 确认命令语境与 `README.md` 一致；3) 交叉检查 `docs/quickstart.zh.md` 中的假设。
  - **验证门禁**：所有工作流变更必须通过 `docagent doctor` 的自动化检查。
