# e-m-c.workbench

> 供 AI 使用的 e-m-c 工作台

本仓库主要供 AI 自行读取和维护，用于持久化已经讨论过的研究内容、观点、设计、资料及任务交接信息，使后续对话中的 AI 能继续利用这些内容，而不必依赖原始聊天记录。

人类主要微调 `rules/`，审视和校正工作台的使用规则；其他文档由 AI 根据讨论持续维护。具体源代码和测试保存在独立代码仓库中。

e-m-c 探索通过外部持久化状态支持 Agent 的持续认知，重点关注情绪、记忆与时间的相互作用。

## 工作台入口

- [文档与文件约定](rules/documentation.md)
- [决策与观点清单](docs/decisions-and-views.md)
- [Draft 隔离](rules/drafts.md)
- [研究流程](rules/research.md)

## 工具约定

- 开发接入 DSH 插件时，以 DSH Desktop 版为主。
