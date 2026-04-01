# 执行计划与验证流程

## 当前运行态势

- Keep the skill definition, generator behavior, and generated documentation in sync.

## 顶层护栏与核心规则 (首读必看)

- Rule 1: Execution contract: `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` is the documented command order for setup, sync, and drift checks.
- Rule 2: Verification gate: workflow changes are not complete until `docagent doctor --target <repo-root>` pass.
- Rule 3: Execution constraints: keep `--target <repo-root>` explicit when commands run outside the target repo; keep `--output-mode agent` consistent across refresh runs; declare `--ai <platform>` explicitly so platform routing stays deterministic.
- Rule 4: Verification order: 1) `docagent doctor --target <repo-root>`; stop at the first failing command before running later checks.

## 即时关注事项

- Validate setup, run, and verify commands before broad edits.
- Refresh AGENTS docs after changing repository structure or workflow commands.

## 环境设置 (Setup)

```bash
npm install
```

## 运行 (Run)

```bash
Run the primary local command from README examples (app start, CLI invocation, or generator refresh).
```

## 验证 (Verify)

```bash
python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
python3 doc-for-agent/tests/verify_generator_snapshots.py
```

## 辅助参考文档提炼 (Execution)

### 已确认的基准主张

- Execution contract: `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` is the documented command order for setup, sync, and drift checks.
- Verification gate: workflow changes are not complete until `docagent doctor --target <repo-root>` pass.
- Execution constraints: keep `--target <repo-root>` explicit when commands run outside the target repo; keep `--output-mode agent` consistent across refresh runs; declare `--ai <platform>` explicitly so platform routing stays deterministic.
- Verification order: 1) `docagent doctor --target <repo-root>`; stop at the first failing command before running later checks.
- Failure triage priority: 1) run `docagent doctor` first to catch install/config drift; 2) reconcile command context with `README.md`; 3) cross-check setup assumptions in `docs/quickstart.md`; 4) inspect CI logs for command/environment mismatches; 5) if failures persist, roll back generated docs to last known-good state and rerun `docagent refresh`.
- Run `docagent init --ai codex` (sources: `README.md`, `docs/platforms.md` (+3 more))

### 待清理的矛盾点

- 未从支持文档中检测到直接的执行冲突。

### 悬而未决的问题

- 未从支持文档中检测到未决的执行事项。

## 执行层辅助参考文档

- `README.md`
- `docs/platforms.md`
- `docs/platforms.zh.md`
- `docs/quickstart.md`
- `docs/quickstart.zh.md`

## Preserved Notes

- 核心工作流规则
  - Preserved from previous manual edits.
  - **设置与配置**：优先通过 `docagent doctor` 命令，确保各平台适配器的物理路径和环境配置正确无误。
  - **验证流程**：在进行本地代码或配置修改后，必须运行 `node doc-for-agent/installer/node/docagent.js refresh` (或已发布的 `docagent refresh`)，深度验证四视图的对齐性。
  - **故障排除**：若在执行中遭遇未知参数报错，应优先核实是否由于本地缓存的旧版全局 NPM 包与新资产产生了版本冲突。
- 核心执行合约 (Rules)
  - Preserved from previous manual edits.
  - **执行顺序感**：确保 `init` -> `refresh` -> `doctor` 是维护者执行操作的固定步步进路径。
  - **验证闭环**：在 `docagent doctor` 全量通过前，视为本项目的工作流变更尚未达到“发布态”。
- 实施详情
  - Preserved from previous manual edits.
  - 本工程当前的核心交付期：处于**架构重构与生产环境全量适配**的加速阶段。
  - 工作重心调整：已从单纯的脚本生成器，彻底进化为具备动态感知能力的“智能体原生技能元数据”。
  - 发布契约流程：`sync_assets.py` (底层同步) -> `npm publish` (全球分发)。
