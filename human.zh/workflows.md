# Workflows

## 核心护栏与顶层规则 (首读必看)

- 第一原则： 执行契约： `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` is the documented command order for setup, sync, and drift checks.
- 第二原则： 验证关卡： workflow changes are not complete until `docagent doctor --target <repo-root>` pass.
- 第三原则： 执行约束条件： keep `--target <repo-root>` explicit when commands run outside the target repo; keep `--output-mode agent` consistent across refresh runs; declare `--ai <platform>` explicitly so platform routing stays deterministic.
- 第四原则： 验证顺序： 1) `docagent doctor --target <repo-root>`; stop at the first failing command before running later checks.

## 文档与执行层契约

- 本页面是该领域面向维护者的真相源; 保持其在双重模式下与 `AGENTS/` 的同步 and `human.zh/` 作为人类视角的根目录.
- 在代码行为变更的同一个 PR 中同步更新此页面; 避免在没有命令或契约更改的情况下进行纯叙述性的刷新.
- 保持 安装/运行/验证/排障 命令序列在干净环境下可执行 from a clean checkout before marking this page done.

## 双重视图对齐检查清单

- After edits, refresh in dual mode and verify both `AGENTS/` and `human.zh/` were updated in the same change set.
- If one side changed without the other, treat it as documentation drift and resolve before merge.
- Run documented verify commands after refresh and keep failure-triage order aligned across both doc systems.

## Quad模式下的同步规则

- Refresh contract: run one refresh/generate action that updates paired views together; do not patch one locale/audience in isolation.
- Path contract: verify changed files include both `AGENTS*/` and `docs*/` counterparts when behavior changes affect shared source-of-truth.
- Quad-mode contract: when using `--output-mode quad`, validate all four roots (`AGENTS/`, `AGENTS.zh/`, `docs/`, `docs.zh/`) in the same review cycle.
- Execution pairing rule: if `human.zh/workflows.md` changes due to command/order updates, refresh paired execution paths under both AGENTS roots.

## 双视图强制对齐契约

- Pairing mode rule: in `dual`, human and agent docs are generated from one analysis pass and must be reviewed as one change set.
- Locale-output rule: 中文语言包 `zh` 映射至 `human.zh/` 目录.
- Template rule: human template variant `paired-core` is part of the pairing contract and must remain consistent across paired docs.
- 路径对齐规则：`human.zh/workflows.md` 与 `AGENTS/03-execution/008-implementation-plan.md` 结对，用于 setup, verify, and failure-triage order.

## Paired Agent Docs (Dual Mode)

- `AGENTS/03-execution/008-implementation-plan.md` 安装、验证与排障顺序.

## 边界定义：人读区 vs 机读区

- Use `human.zh/` for maintainer-facing policy and decisions; use `AGENTS/` for execution order, command wiring, and handoff runbooks.
- If a change affects both reader types, update both systems in one dual refresh cycle instead of patching only one side.
- Keep maintainer runbook context in `human.zh/workflows.md`; keep step-by-step agent execution plan in `AGENTS/workflows.md` (or layered execution docs).

## 双向视图设计逻辑

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

## 全局上下文提炼

- 已分析信源数量：`5`
- 成功提炼结论：`6` 条确认，`0` 条矛盾，`0` 条未决

## 仓库知识健康度

### 核心确立的规则库

- 执行契约： `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` is the documented command order for setup, sync, and drift checks.
- 验证关卡： workflow changes are not complete until `docagent doctor --target <repo-root>` pass.
- 执行约束条件： keep `--target <repo-root>` explicit when commands run outside the target repo; keep `--output-mode agent` consistent across refresh runs; declare `--ai <platform>` explicitly so platform routing stays deterministic.
- 验证顺序： 1) `docagent doctor --target <repo-root>`; stop at the first failing command before running later checks.
- 失败排查优先级： 1) run `docagent doctor` first to catch install/config drift; 2) reconcile command context with `README.md`; 3) cross-check setup assumptions in `docs/quickstart.md`; 4) inspect CI logs for command/environment mismatches; 5) if failures persist, roll back generated docs to last known-good state and rerun `docagent refresh`.

### 高价值辅助参考信号

- 核心命令流工作流集中于 `npm` package scripts and repository-local verify commands.

### 尚未决策的高风险清单

- 未检测到未决的执行项 .

### 矛盾与冲突预警监控

- 未检测到直接的执行冲突 .

## 运维与上线防坑记录

- Keep command examples in this file aligned with CI and README instructions.

## 文档刷新触发条件

- 当 安装/运行/验证 命令变更时，请立即更新此手册.
- 当 CI 检查或发布门禁变更时，请同步更新验证与运维部分.

## 文档日常维护流

- 为此文档分配一名维护责任人 and update it in the same pull request as behavior changes.
- 每个 Sprint 至少评审一次此文档 or before each release cut.
- Update after setup/run/verify command changes or CI workflow updates.
- 未检测到严重的规则提炼冲突; focus on keeping this page current with implementation changes.

## 冷启动阶段待办 (When Docs Are Thin)

- Supporting docs were found; continue consolidating them into this page and archive stale duplicates.

## 溯源证明

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`
- `docs/quickstart.md`
- `docs/quickstart.zh.md`
