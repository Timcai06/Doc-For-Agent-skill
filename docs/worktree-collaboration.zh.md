# Worktree 协作规则

这份文档定义了 `doc-for-agent` 当前默认采用的 worktree 协作机制。

## 默认结构

- `main`：集成分支，也是产品判断和整合窗口
- `codex/skill-quality`：主执行分支，负责输出质量和文档引擎
- `codex/product-distribution`：辅助执行分支，负责入口、安装和产品表面

## 角色边界

### `main`

`main` 负责：

- 产品判断
- 任务拆分
- 合并顺序
- 全量验证
- 最终集成和推送

`main` 默认不承担大块功能实现，除非工作本身就是产品策略或集成相关。

### `codex/skill-quality`

这是当前的主攻分支。

负责：

- synthesis 质量
- `human / agent / dual` 输出行为
- `refresh / generate` 的保留价值
- dogfooding 输出是否真的有用
- fixtures、snapshots、引擎相关测试

应避免：

- npm/package 入口工作
- 与输出语义无关的大块 README 首页改写

### `codex/product-distribution`

这是当前的辅助分支。

负责：

- `docagent` 的首次体验
- README / quickstart / platform guide 的一致性
- installer 文案和 first-run UX
- 轻量 packaging 和 launcher 打磨

应避免：

- 深度生成器逻辑
- 大规模输出模型设计
- 除非 CLI 接线必须，否则不要扩 repo-analysis

## 工作分配规则

默认资源分配：

- `codex/skill-quality` 约占 70%
- `codex/product-distribution` 约占 30%

当产品入口已经“够用”，而输出留存价值仍然是主要差异化时，应继续保持这个比例。

## 合并规则

默认合并顺序：

1. `codex/skill-quality`
2. `codex/product-distribution`

原因：

- 产品入口和文案应建立在最新输出能力之上，而不是反过来

## 什么时候新开分支 / 新 worktree

默认**不要**长期常驻第三个 worktree。

只有在下面这些情况出现时，才新开额外分支/worktree：

- 一个战略/文档方向已经变成独立交付线，有自己的文件、测试或发布资产
- 一个高风险架构实验需要和当前两条工作线隔离
- release / launch 线开始同时和质量线、分发线冲突

如果工作还只是产品思考、判断、规划，而不是明确交付面，就继续放在 `main` 由集成窗口处理。

## Worker 交付格式

每个 worker 完成后，都应该返回：

- 改了什么
- 为什么这么设计
- 跑了哪些测试
- 风险和下一步
- 精确的 `git add`、`git commit`、`git push` 命令，供用户手动执行

## 决策优先级

当下面几件事发生冲突时，优先级顺序是：

1. 输出质量更高
2. 入口摩擦更低
3. 功能更多

这个仓库当前应该优先优化“结果是否值得保留”，而不是功能面继续扩张。
