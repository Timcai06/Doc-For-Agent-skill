<!-- @Agent: This is an automatically generated structural skeleton in English. Please translate the entire content below into professional Chinese (zh-CN) immediately, while preserving all markdown formatting, file names, and code blocks. -->

## 核心护栏与顶层规则 (首读必看)

- 第一要则： Execution contract: `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` is the documented command order for setup, sync, and drift checks.
- 第二要则： Verification gate: workflow changes are not complete until `docagent doctor --target <repo-root>` pass.
- 第三要则： Execution constraints: keep `--target <repo-root>` explicit when commands run outside the target repo; keep `--output-mode agent` consistent across refresh runs; declare `--ai <platform>` explicitly so platform routing stays deterministic.
- 第四要则： Verification order: 1) `docagent doctor --target <repo-root>`; stop at the first failing command before running later checks.

## 文档与执行层契约

- This page is maintainer-facing source-of-truth for its domain; keep it synchronized with `AGENTS/` in dual mode and `human.zh/` as the human-view root.
- Update this page in the same PR as behavior changes; avoid narrative-only refreshes without command or contract changes.
- Keep setup/run/verify/triage order executable from a clean checkout before marking this page done.

## 双重视图对齐检查清单

- After edits, refresh in dual mode and verify both `AGENTS/` and `human.zh/` were updated in the same change set.
- If one side changed without the other, treat it as documentation drift and resolve before merge.
- Run documented verify commands after refresh and keep failure-triage order aligned across both doc systems.

## Quad模式下的同步规则

- Refresh contract: run one refresh/generate action that updates paired views together; do not patch one locale/audience in isolation.
- Path contract: verify changed files include both `AGENTS*/` and `docs*/` counterparts when behavior changes affect shared source-of-truth.
- Quad-mode contract: when using `--output-mode quad`, validate all four roots (`AGENTS/`, `AGENTS.zh/`, `docs/`, `docs.zh/`) in the same review cycle.
- Execution pairing rule: if `human.zh/workflows.md` changes due to command/order updates, refresh paired execution paths under both AGENTS roots.

## 双向绑定契约 (执行规则)

- Pairing mode rule: in `dual`, human and agent docs are generated from one analysis pass and must be reviewed as one change set.
- Locale-output rule: human locale `zh` maps to `human.zh/`.
- Template rule: human template variant `paired-core` is part of the pairing contract and must remain consistent across paired docs.
- Path pair rule: `human.zh/workflows.md` pairs with `AGENTS/03-execution/008-implementation-plan.md` for setup, verify, and failure-triage order.

## 结对的 Agent 文档 (双向模式)

- `AGENTS/03-execution/008-implementation-plan.md` for setup, verify, and failure-triage order.

## 边界定义：人读区 vs 机读区

- Use `human.zh/` for maintainer-facing policy and decisions; use `AGENTS/` for execution order, command wiring, and handoff runbooks.
- If a change affects both reader types, update both systems in one dual refresh cycle instead of patching only one side.
- Keep maintainer runbook context in `human.zh/workflows.md`; keep step-by-step agent execution plan in `AGENTS/workflows.md` (or layered execution docs).

## 双重视图设计逻辑

- `human.zh/` and `AGENTS/` are two views generated from the same repository analysis and source-of-truth anchors.
- When the two views diverge, treat it as refresh drift rather than independent documentation authority.
- Maintainer runbook context lives in `human.zh/workflows.md`, while step ordering for agent actions lives in paired AGENTS execution docs.

## 环境配置序列

```bash
npm install
```

## 本地运行路径

```bash
Run the main local command from README examples.
```

## 验证流程卡点

```bash
python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
python3 doc-for-agent/tests/verify_generator_snapshots.py
```

## 全局上下文信息提炼

- 已扫描分析底层信源数量：`5`
- 成功提炼主张：`6` 条确认, `0` 条矛盾, `0` 条未决

## 仓库知识体系健康度

### 100% 确凿基准规则库

- Execution contract: `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` is the documented command order for setup, sync, and drift checks.
- Verification gate: workflow changes are not complete until `docagent doctor --target <repo-root>` pass.
- Execution constraints: keep `--target <repo-root>` explicit when commands run outside the target repo; keep `--output-mode agent` consistent across refresh runs; declare `--ai <platform>` explicitly so platform routing stays deterministic.
- Verification order: 1) `docagent doctor --target <repo-root>`; stop at the first failing command before running later checks.
- Failure triage priority: 1) run `docagent doctor` first to catch install/config drift; 2) reconcile command context with `README.md`; 3) cross-check setup assumptions in `docs/quickstart.md`; 4) inspect CI logs for command/environment mismatches; 5) if failures persist, roll back generated docs to last known-good state and rerun `docagent refresh`.

### 高价值辅助参考信号

- Primary command workflow centers on `npm` package scripts and repository-local verify commands.

### 尚未决策的高风险清单

- No unresolved execution items were synthesized from supporting docs.

### 矛盾与冲突预警监控

- No direct execution conflicts were synthesized from supporting docs.

## 运维与上线防坑记录

- Keep command examples in this file aligned with CI and README instructions.

## 文档刷新触发条件

- When setup/run/verify commands change, update this runbook immediately.
- When CI checks or release gates change, sync the Verify and Operational Notes sections.

## 文档日常维护流

- Assign one maintainer owner for this document and update it in the same pull request as behavior changes.
- Review this document at least once per sprint or before each release cut.
- Update after setup/run/verify command changes or CI workflow updates.
- No major synthesis conflicts were detected; focus on keeping this page current with implementation changes.

## 冷启动阶段待办 (When Docs Are Thin)

- Supporting docs were found; continue consolidating them into this page and archive stale duplicates.

## 溯源证明

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`
- `docs/quickstart.md`
- `docs/quickstart.zh.md`
