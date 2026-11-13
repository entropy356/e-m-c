# e-m-c.workbench

> e-m-c 的 AI 持久化工作台

本仓库主要供 AI 读取和维护，用于保存讨论中值得跨对话复用的研究内容、观点、设计、决策与资料，使后续 AI 不必依赖原始聊天记录即可接续工作。这里不是源代码仓库，也不要求保存完整聊天记录。

人类主要审视和微调 `rules/`；其他文档由 AI 根据讨论持续维护。具体实现与测试由独立代码仓库承担。

e-m-c 探索通过外部持久化状态支持 Agent 的持续认知，重点关注情绪、记忆与时间的相互作用。

## 项目仓库索引

e-m-c 相关仓库按研究文档、模型实验、运行基础设施与观察界面分工。以下链接指向各仓库当前 README；仓库之间不默认代表已完成集成。

| 仓库 | 职责 | 入口 |
| --- | --- | --- |
| **e-m-c.workbench** | AI 持久化研究工作台，整理观点、决策、规范与研究资料；不是源代码仓库。 | [本仓库](https://github.com/entropy356/e-m-c.workbench) |
| **e-m-c.memory** | Memory 数学模型与 DeepSeek Harness 插件方向的独立实验。 | [仓库](https://github.com/entropy356/e-m-c.memory) · [数学模型](https://github.com/entropy356/e-m-c.memory/blob/main/docs/memory-model.md) · [DSH 插件](https://github.com/entropy356/e-m-c.memory/blob/main/docs/dsh-plugin.md) |
| **e-m-c.runtime** | 可独立运行的模块化 Agent 实验运行环境，提供事件、上下文编排、状态事务、Provider 和 CLI 等基础设施。 | [仓库](https://github.com/entropy356/e-m-c.runtime) · [架构](https://github.com/entropy356/e-m-c.runtime/blob/main/docs/architecture.md) |
| **e-m-c.extra** | 杂项与辅助项目仓库；目前包含实验用聊天前端，可展示运行链、会话与评分日志。其 README 描述的对接对象为早期 demo，不能据此推定已对接当前 runtime。 | [仓库](https://github.com/entropy356/e-m-c.extra) |

## AI 使用入口

- [文档与文件约定](rules/documentation.md)：写入约定、文件职责与认可署名。
- [决策与观点清单](docs/decisions-and-views.md)：当前有效的研究背景与指导观点。
- [研究流程](rules/research.md)：模型研究的阶段与证据要求。
- [Draft 隔离](rules/drafts.md)：临时内容的隔离约定。
- [规范维护](rules/meta.md)：仅在审查或修改规则时按需阅读。

AI 按任务读取相关内容，并将值得保留的讨论结果更新至工作台。认可署名由 AI 主动添加；GitHub Actions 自动归档认可版本并清理失效署名，具体规则见[认可署名](rules/documentation.md#认可署名)。

## 对接方向

对接 DSH 时，以 DSH Desktop 为主要目标环境；e-m-c 作为独立可选的 Agent Preset（Agent 模式）呈现。具体决策见[决策与观点清单](docs/decisions-and-views.md#e4以独立-agent-模式接入-dsh)。
