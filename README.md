# Agent Runtime

一个探索持续内部状态的 Agent Runtime 实验项目。

## 文档

- [核心设计](docs/design.md)
- [项目规范](docs/vision.md)
- [Demo 规则](docs/demos.md)

## 当前 Demo

### Demo 1 — Emotion 与 Memory 的相互作用

观察 Emotion 如何影响记忆的读写，以及被读到的记忆如何反过来改变 Emotion。

~~~bash
cd demos/demo1-emotion-memory
python -m agent_runtime serve
~~~

Python 3.10+；离线模式无需额外依赖。详见 [Demo 说明](demos/demo1-emotion-memory/README.md)。

### Demo 2 — Memory Dynamics

独立验证记忆权重逐轮衰减、成功使用后的权重恢复，以及稳定性对后续衰减的影响。无前端，支持离线机制测试和真实 LLM + Embedding API 测试。

~~~bash
cd demos/demo2-memory-dynamics
python -m unittest discover -v
python -m memory_dynamics --db data/offline.sqlite3 run scenarios/spacing-and-interference.json
~~~

详见 [Demo 说明](demos/demo2-memory-dynamics/README.md)。

### Demo 3 — Emotion-free Long-term Memory Agent

把连续对话上下文与 Demo 2 的长期记忆动态整合起来。完整保存并传递有序的用户/助手消息；长期记忆从对话中提取，在不同会话间共享，并通过检索、衰减和激活持续更新。不引入 Emotion。

~~~bash
cd demos/demo3-long-term-memory
python -m unittest discover -v
python -m long_term_memory --mode api --db data/agent.sqlite3 chat
~~~

详见 [Demo 说明](demos/demo3-long-term-memory/README.md)。
