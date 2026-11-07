# 元规范与细化关系

规范正文见 [文档](documentation.md)、[Draft](drafts.md) 和 [实验](experiments.md)。本文件记录元规范及其细化关系。除 `[root]` 标记的根规范外，其余规范与关联仍待逐条审议。

## 记法

```text
标识符:[被细化的规范1|被细化的规范2] = 规范内容
    - 意义1
    - 意义2
```

- 方括号内引用这条规范所细化的上层规范，不表示严格的逻辑推导；`|` 用于分隔多个上层规范。
- `[root]`：已确认的根规范，无上层规范。
- `[]`：暂不指定被细化的规范，不等于根规范。
- 缩进的列表用于说明该规范存在的实际意义；按需记录，不要求每条规范预先填写。
- 跨文件规范可以用 `[文件.md #章节](文件.md#章节):[被细化的规范]` 引用，不复制正文。
- 章节内的列表、表格和段落属于该章节的内部结构，不自动成为独立规范。

## 元规范

pragmatism:[root] = 规范遵循实用主义

agent-reader:[root] = 规范是给 Agent 读的

effective-output:[] = 规范无需正确，只要 Agent 能根据规范写出正确的代码与文档即可

importance:[] = 规范按重要性排列

justifiable-value:[pragmatism] = 每条规范在受到质疑时，都应能说明其存在的实际价值；不要求事先记录说明

minimize-negative-expression:[] = 减少不必要的负面表述

organization:[] = 规范按作用对象分文件，文件内部按规则性质分块

self-example:[] = 规范本身也须遵守 [文档规范](documentation.md)，作为示例

## 既有背景与目标（待审议）

以下条目来自先前的意义引用体系，暂作背景材料，不作为独立规范或上层规范引用。

- `git-history`：普通调参、重构、修复与方案迭代已有 Git 记录
- `self-contained`：正式文档应使读者无需追溯旧提交、聊天记录或 Draft 就能理解当前内容
- `draft-temporary`：Draft 用于暂存和交换材料，不承担正式知识来源的角色
- `draft-independent`：Draft 边界外的内容需要能独立理解、运行和验证
- `demo-question`：Demo 围绕稳定的研究问题持续演化
- `experiment-infrastructure`：实验提出、检验共用能力需求，基础设施提供可组合的运行环境

## 旧版意义关联（待审议）

以下保留旧版引用信息，以便之后判断它们是否构成细化关系，或需要转为具体规范下的意义说明；**不直接按新的方括号语法解释**。

### 文档

- [documentation.md #最小化历史](documentation.md#最小化历史)：`git-history`、`self-contained`
- [documentation.md #表述](documentation.md#表述)：`agent-reader`
- [documentation.md #组织](documentation.md#组织)：`organization`

### Draft

- [drafts.md #命名与边界](drafts.md#命名与边界)：`draft-temporary`
- [drafts.md #必须遵守](drafts.md#必须遵守)：`draft-temporary`、`draft-independent`
- [drafts.md #使用与清理](drafts.md#使用与清理)：`draft-temporary`

### 实验

- [experiments.md #Demo 的演化](experiments.md#demo-的演化)：`demo-question`、`experiment-infrastructure`
- [experiments.md #验证与记录](experiments.md#验证与记录)：暂无关联
