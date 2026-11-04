# e-m-c

> emotion, memory, clock

一个探索持续内部状态的 agent runtime 实验项目。仓库名取自三块内容：Emotion、Memory、Clock。

目标是**像人**，不是可靠或有用：它允许记错、执着于旧结论、因为当下情绪而想起不同的事。

## 文档

- [核心设计](docs/design.md)
- [项目规范](docs/guidelines.md)
- [Demo 规则](docs/demos.md)
- [可用资料](docs/references.md)
- [临时协作分支约定](docs/scratch-branches.md)

## 当前 Demo

### Demo 1 — Emotion 与 Memory 的相互作用

观察 Emotion 如何影响记忆的读写，以及被读到的记忆如何反过来改变 Emotion。

```bash
cd demos/demo1-emotion-memory
python -m emc serve
```

Python 3.10+；离线模式无需额外依赖。详见 [Demo 说明](demos/demo1-emotion-memory/README.md)。

## 关联实验

- [e-m-c.runtime](https://github.com/entropy356/e-m-c.runtime)：独立的无 Emotion 长期记忆聊天 Runtime 实验；与本仓库的 Demo 1 分开维护。
