# Implementation Plan

## Current Operating Posture

- Keep the skill definition, generator behavior, and generated documentation in sync.

## 核心护栏与顶层规则 (首读必看)

- 第一原则： 执行契约： `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` is the documented command order for setup, sync, and drift checks.
- 第二原则： 验证关卡： workflow changes are not complete until `docagent doctor --target <repo-root>` pass.
- 第三原则： 执行约束条件： keep `--target <repo-root>` explicit when commands run outside the target repo; keep `--output-mode agent` consistent across refresh runs; declare `--ai <platform>` explicitly so platform routing stays deterministic.
- 第四原则： 验证顺序： 1) `docagent doctor --target <repo-root>`; stop at the first failing command before running later checks.

## Immediate Next Steps

- Validate setup, run, and verify commands before broad edits.
- Refresh AGENTS docs after changing repository structure or workflow commands.

## 环境配置序列

```bash
npm install
```

## 本地运行路径

```bash
Run the primary local command from README examples (app start, CLI invocation, or generator refresh).
```

## 验证流程卡点

```bash
python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
python3 doc-for-agent/tests/verify_generator_snapshots.py
```

## 辅助参考文档提炼 (Execution)

### 已确认的基准主张

- 执行契约： `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` is the documented command order for setup, sync, and drift checks.
- 验证关卡： workflow changes are not complete until `docagent doctor --target <repo-root>` pass.
- 执行约束条件： keep `--target <repo-root>` explicit when commands run outside the target repo; keep `--output-mode agent` consistent across refresh runs; declare `--ai <platform>` explicitly so platform routing stays deterministic.
- 验证顺序： 1) `docagent doctor --target <repo-root>`; stop at the first failing command before running later checks.
- 失败排查优先级： 1) run `docagent doctor` first to catch install/config drift; 2) reconcile command context with `README.md`; 3) cross-check setup assumptions in `docs/quickstart.md`; 4) inspect CI logs for command/environment mismatches; 5) if failures persist, roll back generated docs to last known-good state and rerun `docagent refresh`.
- Run `docagent init --ai codex` (sources: `README.md`, `docs/platforms.md` (+3 more))

### 待清理的矛盾点

- 未检测到直接的执行冲突 .

### 悬而未决的问题

- 未检测到未决的执行项 .

## Supporting Execution Docs

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`
- `docs/quickstart.md`
- `docs/quickstart.zh.md`
