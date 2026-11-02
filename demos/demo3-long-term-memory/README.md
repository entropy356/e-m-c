# Demo 3：Emotion-free Long-term Memory Agent

把 Demo 2 的记忆动态机制放进一个真正连续对话的 Agent 中：先保证模型能看到按顺序保存的用户与助手消息，再让长期记忆从对话中形成、被检索和强化。

**不引入 Emotion，不做前端。** 保留真实 Chat、Embedding API 接入和离线测试。

## 要解决的问题

Demo 2 已经有记忆检索、权重衰减和激活恢复，但模型每轮只收到当前输入与 Top-K 记忆，没有收到之前的对话。Demo 3 把 Conversation Context 纳入运行时：

- 每条用户消息和助手回答都按原始内容、角色和顺序持久化。
- 每次认知都收到当前会话此前的完整消息历史，以及当前用户输入。
- 不再要求记忆库重建刚刚发生过的对话。
- 长期记忆从对话中提取，跨会话共享；每个会话的对话历史彼此隔离。
- 长期记忆继续使用 Demo 2 的权重衰减、激活恢复和稳定性机制。
- 一轮认知、消息写入、记忆更新和 Trace 在同一个 SQLite 提交中完成。

## 运行

需要 Python 3.10+；没有第三方 Python 依赖。

### 测试

在本目录运行：

~~~bash
python -m unittest discover -v
~~~

### 离线模式

离线模式使用确定性哈希字符向量和固定模板回答，只验证消息顺序、持久化、检索链路和状态提交，不代表真实语义检索或真实对话能力。

~~~bash
python -m long_term_memory --mode offline --db data/offline.sqlite3 turn "你好"
python -m long_term_memory --mode offline --db data/offline.sqlite3 history
python -m long_term_memory --mode offline --db data/offline.sqlite3 state
~~~

### 真实 Chat + Embedding API

Chat 使用 OpenAI-compatible /chat/completions；Embedding 支持 OpenAI-compatible /embeddings 或 Gemini 原生 :embedContent。Chat 和 Embedding 可以使用不同服务商、模型、密钥、代理和超时。

~~~bash
export AGENT_CHAT_BASE='https://your-chat.example/v1'
export AGENT_CHAT_MODEL='your-chat-model'
export AGENT_CHAT_KEY='your-chat-key'

export AGENT_EMBED_PROTOCOL='openai'  # 或 gemini
export AGENT_EMBED_BASE='https://your-embedding.example/v1'
export AGENT_EMBED_MODEL='your-embedding-model'
export AGENT_EMBED_KEY='your-embedding-key'
export AGENT_EMBED_DIMENSIONS='768'   # 可选，按服务商支持情况设置

# 可选：分别配置代理与超时
export AGENT_CHAT_PROXY='http://127.0.0.1:8080'
export AGENT_EMBED_PROXY='http://127.0.0.1:8080'
export AGENT_CHAT_TIMEOUT='120'
export AGENT_EMBED_TIMEOUT='60'
~~~

启动交互式聊天：

~~~bash
python -m long_term_memory --mode api --db data/agent.sqlite3 --conversation default chat
~~~

输入 /exit 或 /quit 退出。后续重新启动并使用相同数据库与会话 ID，会恢复之前的对话。

也可以逐轮调用：

~~~bash
python -m long_term_memory --mode api --db data/agent.sqlite3 --conversation default turn "我更喜欢简短的书面进度。"
python -m long_term_memory --mode api --db data/agent.sqlite3 --conversation default turn "你还记得我喜欢什么样的进度吗？"
~~~

用另一个会话 ID 开始新对话：

~~~bash
python -m long_term_memory --mode api --db data/agent.sqlite3 --conversation project-x chat
~~~

同一数据库中的长期记忆跨会话共享，但不同会话的消息历史不会混在一起。

### 场景运行

~~~bash
python -m long_term_memory --mode api --db data/scenario.sqlite3 run scenarios/continuity-and-recall.json --output results/continuity-and-recall.json
~~~

每个场景使用独立数据库。真实 API 模式下，LLM 会从对话中提出值得长期保存的记忆；离线模式不会模拟记忆提取。

## 记忆动态

每轮用户交互时，已有记忆先衰减：

\[
w^- = w \exp[-\lambda(1-\gamma s)]
\]

只有 LLM 明确报告本轮实际使用某条已提供的记忆，才执行激活：

\[
w' = w^- + (1-w^-)r
\]

\[
s' = s + (1-s)\beta(1-w^-)
\]

检索分数：

\[
score_i = \frac{1+\cos(q,m_i)}{2} \cdot w_i
\]

- weight 表示记忆当前的可访问程度。
- stability 影响后续衰减速度，不直接增加当前检索分数。
- weight-only 与 two-state 保留 Demo 2 的两种对照模式。
- 现实时间不参与衰减；每次成功提交的用户交互推进一轮。
- 新记忆以 weight=1、stability=0 写入，不在创建轮立即衰减。
- 精确重复的记忆文本不会重复写入。

## 数据组织

SQLite 中有三类主要数据：

- messages：按 conversation_id + seq 保存完整有序对话，包含 user 和 assistant。
- runtime.state：保存跨会话共享的长期记忆及其动态状态。
- rounds：保存每轮检索、认知、激活和写入 Trace。

当前 Context 组装方式：

~~~text
System Instructions
Long-term Memory Candidates
Earlier User Message
Earlier Assistant Message
...
Current User Message
        |
        v
       LLM
        |
        +--> Assistant Message
        +--> Memory Proposals
        +--> Used Memory IDs
~~~

读取历史不会推进 Runtime 轮次，也不会改变记忆权重。认知失败、记忆 Embedding 失败或并发状态冲突时，本轮消息和记忆状态都不会提交。

## 当前限制与下一步

- 当前每次请求都会传递该会话的全部原始消息，不做摘要或截断。这让连续上下文行为可以先被直接观察，但长对话最终会受到模型 Context Window 限制。
- 当前消息角色只有 user 和 assistant，尚未处理工具调用、多模态消息或流式中断恢复。
- 长期记忆由 LLM 提出，used_memory_ids 也是 LLM 自报的使用指标；需要人工抽查提取质量与实际引用情况。
- 记忆检索仍然遍历当前记忆集合，尚未引入向量索引。
- 记忆来源目前记录会话 ID，不做细粒度消息级溯源。

先用真实聊天观察：原始历史是否足以保持对话连续性，长期记忆是否能在新会话中提供有用信息，以及记忆是否会因反复激活而过度垄断上下文。之后再决定上下文压缩、记忆去重与索引优化的实现方式。
