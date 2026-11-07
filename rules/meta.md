# 元规范与意义引用

规范正文见 [文档](documentation.md)、[Draft](drafts.md) 和 [实验](experiments.md)；本文件记录元规范、可供引用的背景，以及规则存在意义的关联。除 `[root]` 外，现有条目均待审议，不因列在此处就视为已确认。

## 记法

`标识符:[意义引用1|意义引用2] = 规范内容`：左侧为语义化标识符，方括号内为可选的意义引用，右侧为规范正文。意义引用指向有助于说明规范存在价值的原则、目标或背景，不表示逻辑推导关系。

- `[root]`：已确认的根规范标记，不是意义引用。
- `[]`：没有显式记录意义引用；不代表规范没有价值，也不代表其价值已被确认。
- 跨文件规范采用 `[文件.md #章节](文件.md#章节):[意义引用1|意义引用2]`，无需另设标识符，也不复制正文。
- 章节内的列表、表格和段落属于该章节的内部结构，不自动成为独立规范。

## 元规范

pragmatism:[root] = 规范遵循实用主义

agent-reader:[root] = 规范是给 Agent 读的

effective-output:[pragmatism|agent-reader] = 规范无需正确，只要 Agent 能根据规范写出正确的代码与文档即可

importance:[] = 规范按重要性排列

justifiable-value:[pragmatism] = 每条规范在受到质疑时，都应能说明其存在的实际价值；不要求事先写出说明或填写意义引用

organization:[] = 规范按作用对象分文件，文件内部按规则性质分块

self-example:[] = 规范本身也须遵守 [文档规范](documentation.md)，作为示例

## 可引用的背景与目标（待审议）

以下条目提取自现有设计说明，仅作为理解规范意义的参考，不新增执行要求。它们可能是事实、目标或设计判断，不自动成为已确认的规范。

git-history:[] = 普通调参、重构、修复与方案迭代已有 Git 记录

self-contained:[] = 正式文档应使读者无需追溯旧提交、聊天记录或 Draft 就能理解当前内容

draft-temporary:[] = Draft 用于暂存和交换材料，不承担正式知识来源的角色

draft-independent:[] = Draft 边界外的内容需要能独立理解、运行和验证

demo-question:[] = Demo 围绕稳定的研究问题持续演化

experiment-infrastructure:[] = 实验提出、检验共用能力需求，基础设施提供可组合的运行环境

## 非元规范的意义引用（待审议）

### 文档

[documentation.md #最小化历史](documentation.md#最小化历史):[git-history|self-contained]

[documentation.md #表述](documentation.md#表述):[agent-reader]

[documentation.md #组织](documentation.md#组织):[organization]

### Draft

[drafts.md #命名与边界](drafts.md#命名与边界):[draft-temporary]

[drafts.md #必须遵守](drafts.md#必须遵守):[draft-temporary|draft-independent]

[drafts.md #使用与清理](drafts.md#使用与清理):[draft-temporary]

### 实验

[experiments.md #Demo 的演化](experiments.md#demo-的演化):[demo-question|experiment-infrastructure]

[experiments.md #验证与记录](experiments.md#验证与记录):[]
