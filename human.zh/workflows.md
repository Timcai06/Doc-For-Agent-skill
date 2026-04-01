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

- 结对模式规则：在 `dual` 模式下，人和机器的文档同源生成，必须作为一个完整的变更集进行评审。
- 语言输出规则：人类视图语言 `zh` 映射至目录 `human.zh/`。
- 模板规则：人类视图模板变体 `paired-core` 是结对契约的一部分，在配对文档间必须保持一致。
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
  - **规则 1：执行契约** —— 标准操作顺序为：`docagent init` -> `docagent refresh` -> `docagent doctor`。这是环境配置、同步及其漂移检查的主路径。
  - **规则 2：验证门禁** —— 在 `docagent doctor` 通过之前，视为本仓库的文档工作流变更尚未完成。
  - **规则 3：执行约束** —— 当在目标仓库目录外运行命令时，必须显式指明 `--target` 参数；在多次刷新过程中应保持 `--output-mode` 参数的一致性。
  - **规则 4：验证顺序** —— 1) 执行 `docagent doctor`；2) 检查失败项。严禁带病执行后续刷新。
- 文档维护契约
  - Preserved from previous manual edits.
  - **事实性源**：本页面是面向维护者的核心事实来源，必须与 `AGENTS/` 目录下的执行脚本维持高频的事实对齐。
  - **变更驱动规则**：仅在实际行为更迭时更新本页面，避免仅进行叙述性的文字刷新。
- 结对刷新规则 (Pairing Rules)
  - Preserved from previous manual edits.
  - **对齐校验**：在编辑后运行 `quad` 模式，并验证对齐的四视图是否在同一变更集中得到了更新。
  - **漂移处理**：如果发现语言版本间的一侧更新而另一侧停滞，应视其为“文档漂移”，并须在提交代码前予以解决。
- 双视图配对契约
  - Preserved from previous manual edits.
  - **规则**：在 `dual/quad` 模式下，面向人类和智能体的文档由同一次仓库扫描生成，必须作为一个完整的变更集进行审阅。
- 环境初始化与验证
  - Preserved from previous manual edits.
  ### 设置 (Setup)
  ```bash
  npm install
  ```

  ### 核心验证 (Verify)
  ```bash
  # 运行单元测试
  python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
  # 验证生成器快照
  python3 doc-for-agent/tests/verify_generator_snapshots.py
  ```
- 知识状态与故障排查
  - Preserved from previous manual edits.
  ### 确认的规则
  - **执行契约顺序**：保持 `init -> refresh -> doctor` 的闭环命令顺序。
  - **故障排查优先级**：1) 运行 `docagent doctor` 捕获安装或配置漂移；2) 确认命令语境与 `README.md` 一致；3) 交叉对照 `docs/quickstart.zh.md`。
