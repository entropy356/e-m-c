# e-m-c

> emotion, memory, clock

一个研究 Agent 持续内部状态的项目，包含**研究模型、实验和基础设施**。研究目标是探索更接近人的行为，而不是以任务执行能力为中心：Agent 可以记错、受旧结论影响，也可以因为当前状态不同而对同一输入作出不同反应。

## 项目组成

- **研究模型**：描述 Emotion、Memory、Clock 及其与认知的关系。见 [概念模型](docs/model.md)。
- **实验**：实现和验证具体机制，并反过来发现对基础设施的需求。当前有 [Demo 1 — Emotion 与 Memory 的相互作用](demos/demo1-emotion-memory/README.md)。
- **基础设施**：提供运行、模块组合、状态管理和可观测性等公共能力，供不同实验复用；不应把某一种实验机制固定为 Runtime 的唯一流程。

[**e-m-c.runtime**](https://github.com/entropy356/e-m-c.runtime) 是从之前的长期记忆实验中抽离出来的独立 Runtime 原型，**目标是通过模块化重构发展为基础设施**。目前它仍以特定的无 Emotion 长期记忆聊天流程组织，尚未集成进本仓库，也不能视为已经完成的通用 Runtime。

实验与基础设施相互促进：实验检验机制并提出能力需求；基础设施减少重复工程工作，让实验能够组合、运行和观察不同机制。基础设施的具体架构与改造工作在其自身仓库维护。

## 文档

- [概念模型](docs/model.md)：当前的概念区分与数学结构
- [参考资料](docs/references.md)：论文、相关实现与架构

## 约定

- [实验约定](rules/experiments.md)：Demo 组织、验证与记录
- [文档与历史](rules/documentation.md)：当前文档与可保留的实验记录
- [Draft 隔离](rules/drafts.md)：临时文件、目录、分支和仓库的严格隔离

## 运行当前实验

```bash
cd demos/demo1-emotion-memory
python -m emc serve
```

需要 Python 3.10+；离线模式无需第三方依赖。运行方式及具体机制见 [Demo 1 文档](demos/demo1-emotion-memory/README.md)。

## 待验证

- 使用具有个人偏好的传统 Agent，对 Runtime 进行主观评分。
