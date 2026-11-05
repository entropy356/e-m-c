# Demo 1 — Emotion 与 Memory 的相互作用

## 研究问题

本 Demo 研究情绪化记忆库中的 Emotion–Memory 反馈：当前情绪参与记忆的检索与写入，被提取的记忆影响认知，认知产生的感受又更新 Emotion，进而影响下一轮检索。

实验关注机制变化是否可观察、可复现，以及这些变化的来源。

## 运行

Python 3.10+；默认离线模式只依赖标准库。

~~~bash
git clone https://github.com/entropy356/e-m-c.git
cd e-m-c/demos/demo1-emotion-memory
python -m emc serve
~~~

打开 http://127.0.0.1:8765，可初始化人工夹具、进行 A/B 对照或逐轮交互。默认数据库路径为 `data/runtime.sqlite3`；独立实验应使用不同的 `--db`。

~~~bash
python -m emc seed                          # 空库中创建人工夹具
python -m emc compare                       # 同一记忆库的只读 A/B
python -m emc step '我们再一起试一次吧。'   # 推进一轮
python -m emc step                          # 无外部输入的一轮
python -m emc state                         # 状态与 trace
python -m emc replaced                      # 已替代记忆的调试记录
python -m emc save checkpoint
python -m emc restore checkpoint
python -m unittest discover -v
~~~

全局参数见 `python -m emc --help`：`--rho` 默认 0.85；`--recall-limit` 默认 2，设为 0 可关闭额外检索。

## 情绪化记忆库的当前机制

### Emotion 与检索

LLM 返回的感受描述先编码为单位向量 `V`。首轮初始化为 `E = V`，之后按 `E_next = rho * E + (1 - rho) * V` 更新。

每条记忆包含内容向量、感受向量及写入强度。Content 与 Affect 是概念上独立的空间；**本 Demo 使用同一个 embedding 模型分别编码内容和感受描述**。

查询与记忆内容分别相对内容均值中心化；Emotion 与记忆感受分别相对感受均值中心化，然后单位化残差。以下符号均表示中心化后的向量：

~~~text
relevance_i = (1 + dot(q, v_i)) / 2
match_i = dot(e, a_i)
read_i = sigmoid(4 * match_i)
score_i = relevance_i * read_i * write_strength_i
~~~

按 `score` 取前三条；关闭 Emotion 读取调节时 `read_i = 0.5`。余弦采用移位而非负值截断，避免把中心化后的大量负值压成同分。库内均值会随记忆增删变化，因此不同库的分数不可直接比较；无均值时使用未中心化向量，近零残差视为零向量。

新记忆写入时，以**写入前**的记忆感受均值中心化新感受与更新后的 Emotion，计算 `write_strength = sigmoid(3 * dot(...))`。写入强度此后不随使用次数变化。

检索不直接修改持久状态。认知、embedding 和关系校验全部成功后，才统一提交 Emotion、记忆、引用与替代；失败不会提交本轮状态。

### 关系与使用记录

LLM 每轮最多提出三条新记忆，并可自报：

- `source_memory_ids`：来自本轮提供的哪些记忆；只是出处线索，不是已验证的因果关系。
- `replaces`：由新记忆明确替代本轮提供的哪些旧记忆。旧记忆离开 Runtime，不再参与检索与均值；`replaced` 表只保存调试副本。

没有自动判重、合并或失效机制。模型能够查看记忆的内容、形成轮次和关系元数据，但不直接接收 Emotion 向量或感受描述。

`uses` 与 `recent_uses` 分别记录累计引用次数和最近 16 个成功轮次的引用记录。频率**只供观察**，不影响排序、写入强度或上下文名额。

### 按需检索

初次认知只提供最高分的三条记忆，同时告知 `library_size`（全库数量）。模型可在回答前请求：

~~~json
{"recall": "想寻找的往事"}
~~~

Runtime 用模型自写的查询、同一 Emotion 和同一评分公式追加最多 6 条未出现过的记忆，再次认知。每轮默认最多 2 次，没有新记忆时不再继续尝试。追加的记忆也可以被引用和替代。

按需检索只扩大可见上下文，不保证查询准确。**A/B 只读对照禁用 recall**，四组保持相同的上下文预算。

### Clock 与认知上下文

网页支持固定间隔的自动运行，也可手动执行无输入的轮次。记忆记录形成轮次，Clock 当前负责运行调度。

认知请求包含本轮输入、所选记忆及其元数据；完整有序对话历史未纳入当前请求。

## 实验与观察

- **人工夹具 A/B**：同一记忆库与输入，分别注入暖、冷两种 Emotion，再对照开启和关闭情绪读取的检索结果。夹具不是 Agent 自行形成的经历。
- **连续对话**：逐轮观察检索、认知、感受更新与下一轮检索，记录偏差、漂移与失败案例。

[2026-10-31 实验记录](experiments/2026-10-31-emotion-memory-interaction.md)保留了模型、参数、具体记忆 ID、对照结果与局限；[原始 CSV](results/)保留逐轮指标。该批数据表明：中心化明显改变了检索分数与入选集合；六轮真实对话中写入强度和内容相关性往往比当轮读取门控影响更大；按需检索既能补充被遗漏的记忆，也会捞回无关内容。

以上结果来自所记录的模型、数据和实验条件，用于分析本 Demo 中的情绪化记忆读写机制。

## Provider 配置

离线模式使用确定性字符哈希向量和模板认知，只用于工程验证。API 模式使用 OpenAI-compatible Chat 与 OpenAI-compatible / Gemini Embedding；两者可以来自不同服务商。

~~~bash
export AGENT_CHAT_BASE='https://your-chat.example/v1'
export AGENT_CHAT_MODEL='your-chat-model'
export AGENT_CHAT_KEY='your-chat-key'

export AGENT_EMBED_PROTOCOL='openai'   # 或 gemini
export AGENT_EMBED_BASE='https://your-embed.example/v1'
export AGENT_EMBED_MODEL='your-embed-model'
export AGENT_EMBED_KEY='your-embed-key'
export AGENT_EMBED_DIMENSIONS='768'     # 可选

python -m emc --mode api --db data/api.sqlite3 serve
~~~

嵌入侧缺省的地址、密钥可从 Chat 侧取得；可分别设置 `AGENT_CHAT_PROXY` 与 `AGENT_EMBED_PROXY`。数据库只校验 embedding 协议、模型名和维度，无法识别同名同维模型的服务变化；更换 embedding 服务时应使用新数据库。

## 局限

- Content 与 Affect 尚未使用独立表示；离线模式没有真实语义理解。
- 没有自主的记忆衰减、过期或合并，写入强度固定，引用频率仅供观察。
- 模型只能替代本轮可见的旧记忆，且无法看到被替代的原文；recall 可能引入噪声。
- 当前没有完整对话历史存储；Clock 使用固定间隔调度，尚未实现 Emotion 对运行频率的调节。
- 夹具和有限对话不能用于证明长期稳定性或拟人程度。
