# 执行计划与验证流程

## 当前运行态势

- Keep the skill definition, generator behavior, and generated documentation in sync.

## 顶层护栏与核心规则 (首读必看)

- 第一原则： 执行契约： `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` 是安装、同步与漂移检查的文档化命令顺序。
- 第二原则： 验证关卡： 在 `docagent doctor --target <repo-root>` 通过前，workflow 变更不算完成。
- 第三原则： 执行约束： 当命令在目标仓库外运行时，显式保留 `--target <repo-root>`；在多次 refresh 之间保持 `--output-mode agent` 一致；显式声明 `--ai <platform>` 以保持平台路由确定。
- 第四原则： 验证顺序： 1）先执行 `docagent doctor --target <repo-root>`；在运行后续检查前停在第一个失败命令。

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

- 执行契约： `docagent init --ai codex` -> `docagent refresh --root <repo-root> --output-mode agent|human|dual|quad` -> `docagent doctor --target <repo-root>` 是安装、同步与漂移检查的文档化命令顺序。
- 验证关卡： 在 `docagent doctor --target <repo-root>` 通过前，workflow 变更不算完成。
- 执行约束： 当命令在目标仓库外运行时，显式保留 `--target <repo-root>`；在多次 refresh 之间保持 `--output-mode agent` 一致；显式声明 `--ai <platform>` 以保持平台路由确定。
- 验证顺序： 1）先执行 `docagent doctor --target <repo-root>`；在运行后续检查前停在第一个失败命令。
- 失败排查优先级： 1）先运行 `docagent doctor` 捕获安装/配置漂移；2）结合 `README.md` 校对命令上下文；3）交叉检查 `docs/quickstart.md` 中的 setup 假设；4）检查 CI 日志中的命令/环境不匹配；5）若失败持续，回滚生成文档到最近一次可用状态并重新执行 `docagent refresh`。
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
