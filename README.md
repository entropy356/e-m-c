# e-m-c

> 情绪化记忆库与时间感知（Emotion · Memory · Clock）

e-m-c 研究**情绪化记忆库与时间感知**，探索情绪、记忆与时间在 Agent 持续状态中的作用。项目包括研究模型、实验和支撑实验的基础设施。

## 研究方向

- **情绪化记忆库**：区分记忆的内容（Content）与感受关联（Affect），探索情绪如何参与记忆的写入、提取与变化，以及记忆如何影响后续情绪。
- **时间感知**：项目的另一项研究方向。具体概念、机制和验证方式将随研究明确后补充。

概念及当前研究认识见 [概念模型](docs/model.md)。

## 当前实验

[**Demo 1 — Emotion–Memory 相互作用**](demos/demo1-emotion-memory/README.md) 探索情绪与记忆读写的反馈关系，包含检索、写入、按需回忆及相关对照数据。

~~~bash
cd demos/demo1-emotion-memory
python -m emc serve
~~~

需要 Python 3.10+；离线模式只依赖标准库。具体机制与运行说明见 Demo 文档。

## 基础设施

实验探索机制、提出需求；基础设施提供模块组合、运行和状态管理等共用能力，支持不同实验复用。

[**e-m-c.runtime**](https://github.com/entropy356/e-m-c.runtime) 是准备进行模块化重构的 Runtime 原型，目标是成为项目基础设施。目前主要实现长期记忆聊天流程，其架构与改造工作在该仓库维护。

## 文档与约定

- [概念模型](docs/model.md)：情绪、记忆和时间的研究概念
- [实验约定](rules/experiments.md)：Demo 组织、验证与记录
- [文档规范](rules/documentation.md)：最小化历史、简洁表述与文档组织
- [Draft 隔离](rules/drafts.md)：临时文件、目录、分支和仓库的隔离规则

## 待验证

- 使用具有个人偏好的传统 Agent，对 Runtime 进行主观评分。
