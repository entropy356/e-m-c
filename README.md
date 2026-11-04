# e-m-c

> emotion, memory, clock

一个探索持续内部状态的 Agent Runtime 实验项目。目标是**像人**，而不是以 Agent 的任务执行能力为设计中心：它允许记错、执着于旧结论、因为当下状态而想起不同的事。

## 文档

- [核心设计](docs/design.md)：Emotion、Memory、Clock 与认知的概念边界
- [项目规范](docs/guidelines.md)：总体原则、局部原则与记录方式
- [Demo 组织规则](docs/demos.md)：实验的拆分与演化
- [参考资料](docs/references.md)：论文、相关实现与架构
- [临时分支](docs/scratch-branches.md)：跨 Agent 或设备交换文件

## 当前实验

**[Demo 1 — Emotion 与 Memory 的相互作用](demos/demo1-emotion-memory/README.md)**：观察 Emotion 如何影响记忆读写，以及被调用的记忆如何反过来改变 Emotion。

```bash
cd demos/demo1-emotion-memory
python -m emc serve
```

需要 Python 3.10+；离线模式无需第三方依赖。运行方式、机制和实验数据见 Demo 文档。

## 相关仓库

- [e-m-c.runtime](https://github.com/entropy356/e-m-c.runtime)：独立的无 Emotion 长期记忆聊天 Runtime 实验，未集成进本仓库。

## 待验证

- 使用具有个人偏好的传统 Agent，对 Runtime 进行主观评分。
