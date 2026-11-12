# 类脑长文本记忆：机制研究地图（Draft）

> 定位：探索候选机制与可组合的数学思想，不是架构选型、实施清单或性能承诺。各方向可以并存；不预设系统必然优于 RAG，也不预先规定评测指标。

## 已明确的研究边界

- **探索性**：目标是理解类脑动力学与外部长文本结合后可能出现的行为，暂不以实用效果或超越 RAG 为硬目标。
- **多对多关联**：一个神经元可以关联多段文本，同一段文本可以关联多个神经元。
- **查询驱动**：无外界查询时不自主激活；一次查询内部允许多轮传播。跨轮保留状态不要求后台持续计算。
- **移动的初始激活**：上一轮最终激活状态或提取的文本，均可能影响下一轮初始激活；具体形式未定。
- **数学借鉴**：可以借用 Transformer 注意力的数学方式，但不预设复刻 Transformer。
- **非刻意制造的不可靠性**：关注动力学、学习、竞争等机制是否自然导致遗忘、偏向、错误联想和路径依赖，不以随机噪声注入替代机制解释。
- **文本是否参与传播**：尚未确定。文本可仅被最终读取，也可在激活过程中被 LLM 解释并反作用于网络。
- **对照**：RAG 可作比较基线；具体评测指标留待工程实现阶段确定。

## 结构分层（只为整理问题，并非预选架构）

- **外部内容层**：存储与神经元关联的长文本及可能的片段结构；不预设所有原始历史都能完整保存。
- **关联表示层**：神经元—文本多对多映射；神经元内部表示与神经元间关系尚待研究。
- **激活动力学层**：查询触发的初始激活、传播、吸引、竞争、停止。
- **跨轮状态与学习层**：移动指针、可塑性、时间影响、情绪调制。
- **读取与生成层**：选择文本、必要时反复查询、交给 LLM 形成当前上下文。

一种纯结构性记法：神经元集合 $N$、文本集合 $M$、关联关系 $R\subseteq N\times M$。这不是对节点语义、边权重或更新规则的承诺。

## 候选机制地图

| 研究方向 | 代表性数学/机制线索 | 与长文本关联的研究问题 |
| --- | --- | --- |
| 1. 关联拓扑 | 二部图、超图、异构图、可学习稀疏连接 | 神经元是否是概念、地址、局部状态或纯计算单元？共享文本的神经元怎样互相影响？ |
| 2. 分布式表示 | 稀疏分布式记忆（SDM）、向量符号架构（VSA）、模式分离/补全 | 一段记忆可由神经元群共同编码，而不依赖唯一「代表节点」吗？ |
| 3. 初始寻址 | 查询–键匹配、Softmax/其他归一化、历史状态混合、内容/位置寻址 | 查询与移动指针怎样共同决定起始激活？历史应作为位置、分布还是文本线索？ |
| 4. 激活传播 | 扩散激活、随机游走、图扩散、局部递归动力学 | 能否从当前线索间接找到语义不近、但经历上有关联的文本？ |
| 5. 吸引子与联想恢复 | 经典/现代 Hopfield、能量函数、固定点及其吸引域 | 不完整线索能否恢复关联记忆群？是否出现混合记忆或错误稳定状态？ |
| 6. 竞争与容量 | Softmax、阈值、局部抑制、k-WTA、稀疏激活 | 让神经元争夺激活或允许共同活跃，将带来哪些动力学差异？ |
| 7. 时间与状态延续 | 递归状态、衰减核、事件时间、短期痕迹 | 同一查询如何因历史路径不同而得到不同结果，而又不锁死在旧话题？ |
| 8. 可塑性与结构学习 | Hebbian、STDP、共激活统计、稳态调节、连接生成/剪除 | 阅读、回忆与共同激活是否改变以后可触达的文本？ |
| 9. 编码与巩固 | 互补学习系统（CLS）、快慢学习、情景–语义分化 | 应否区分快速写入具体经历与缓慢抽取长期关联结构？ |
| 10. 外部记忆读写 | Neural Turing Machine、DNC、内容寻址与位置寻址、迭代检索 | 长文本是只读对象，还是能被回忆、总结、改写、重关联？LLM 何时参与？ |
| 11. 情绪调制 | 状态依赖检索、调制激活/学习/提取 | 外部存储的情绪状态可以影响哪些数学量？不要预先假设对应生物机制。 |
| 12. 重构与不可靠性 | 干扰、吸引子误入、状态惯性、记忆再巩固 | 能否观察到机制自然导致的遗漏、偏向、混合或关系漂移？如何区分网络效应与 LLM 错误？ |
| 13. 非类脑对照 | 向量 RAG、图 RAG、HippoRAG、迭代检索 | 哪些现象其实是普通检索、多跳图遍历或重排序即可得到的？ |

这些是**问题空间**，而非十三个必做功能；部分概念跨层重叠。

## 值得分开研究的几组分歧

1. **节点的角色**：神经元是文本索引，还是自身构成可记忆的分布式状态？
2. **历史延续的载体**：上轮神经元活动、上轮文本结果，或两者共同参与；目前三者均开放。
3. **语义参与的时机**：仅写入时编码、仅读取时解释、还是传播时也由 LLM 参与。
4. **状态与内容的可塑性**：仅改连边；改文本关联；还是允许改写文本本身。
5. **激活的组织方式**：竞争性注意力、独立阈值激活、吸引子收敛、图扩散，未必互斥。
6. **不可靠性的来源**：有限触达、竞争、干扰、可塑性和路径依赖，应与人为随机扰动分开讨论。

## 研究地图如何扩展

先横向收集希望观察到的**结果**，再扩展候选机制；对每个机制仅记录：**数学思想、可能出现的现象、与其他方向的联系、证据状态**。区分已有论证、对本项目的类比及待验证假设。通过对比与剪枝收敛探索范围：数学矛盾等技术判断可由 AI 提出并检验，价值性去留应由人参与；不以 AI 提出的某项机制自动决定深入方向。

## 入门资料（作为机制线索，不意味着项目已采用这些模型）

- Collins & Loftus (1975), *A Spreading-Activation Theory of Semantic Processing* — 语义网络的扩散激活理论。https://doi.org/10.1037/0033-295X.82.6.407
- Hopfield (1982), *Neural networks and physical systems with emergent collective computational abilities* — 联想记忆和吸引子。https://pmc.ncbi.nlm.nih.gov/articles/PMC346238/
- Kanerva (1988), *Sparse Distributed Memory* — 稀疏分布式内容寻址。https://ntrs.nasa.gov/search.jsp?R=19900032242
- McClelland, McNaughton & O'Reilly (1995), *Why there are complementary learning systems...* — 快慢学习系统。https://pubmed.ncbi.nlm.nih.gov/7624455/
- Bi & Poo (1998), *Synaptic modifications... dependence on spike timing* — 脉冲时间依赖可塑性实验证据。https://pubmed.ncbi.nlm.nih.gov/9852584/
- Graves et al. (2014), *Neural Turing Machines* — 可微的外部记忆寻址。https://arxiv.org/abs/1410.5401
- Graves et al. (2016), *Hybrid computing using a neural network with dynamic external memory* — DNC 外部结构化记忆。https://www.nature.com/articles/nature20101
- Ramsauer et al. (2020), *Hopfield Networks Is All You Need* — 现代 Hopfield 更新与注意力的数学联系。https://arxiv.org/abs/2008.02217
- Kleyko et al. (2022), *A Survey on Hyperdimensional Computing aka Vector Symbolic Architectures* — 分布式符号表示。https://research.ibm.com/publications/a-survey-on-hyperdimensional-computing-aka-vector-symbolic-architectures-part-i-models-and-data-transformations
- Nader (2015), *Reconsolidation and the Dynamic Nature of Memory* — 回忆后记忆可塑性的生物学研究。https://pubmed.ncbi.nlm.nih.gov/26354895/
- Kensinger & Ford (2020), *Retrieval of Emotional Events from Memory* — 情绪如何影响回忆。https://doi.org/10.1146/annurev-psych-010419-051123
- Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* — 非参数外部记忆与 RAG 基线。https://arxiv.org/abs/2005.11401
- Edge et al. (2024), *From Local to Global: A Graph RAG Approach to Query-Focused Summarization* — 图式检索对照。https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/
- Gutiérrez et al. (2024), *HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models* — 知识图谱与 Personalized PageRank 的脑启发检索。https://proceedings.neurips.cc/paper_files/paper/2024/hash/6ddc001d07ca4f319af96a3024f6dbd1-Abstract-Conference.html
