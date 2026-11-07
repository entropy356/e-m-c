# 元规范与因果关系

规范正文见 [文档](documentation.md)、[Draft](drafts.md) 和 [实验](experiments.md)；本文件只记录元规范、既有依据与因果关系。

## 记法

`[原因1,原因2]: 规范内容 = 标识符` 表示原因指向规范；标识符使用有意义的名称。

- `[root]`：根规范，无需其他原因。
- `[]`：不指定原因，适用于元规范与作为依据的事实。
- `[?]`：非元规范必填的原因尚未确定；可与已知原因并列，如 `[agent-reader,?]`。
- 跨文件规范直接使用 Markdown 链接，不复制正文。
- 章节内的列表、表格和段落属于该章节的内部结构，不自动成为独立规范。

为避免 Markdown 把 `[标识符]:` 当作链接定义，以下将语法标记写为行内代码；链接仍可直接点击。

## 元规范

`[root]:` 规范遵循实用主义 `= pragmatism`

`[root]:` 规范是给 Agent 读的 `= agent-reader`

`[pragmatism,agent-reader]:` 规范无需正确，只要 Agent 能根据规范写出正确的代码与文档即可 `= effective-output`

`[]:` 规范按重要性排列 `= importance`

`[]:` 非元规范必须注明原因 `= required-reason`

`[]:` 规范按作用对象分文件，文件内部按规则性质分块 `= organization`

`[]:` 规范本身也须遵守 [文档规范](documentation.md)，作为示例 `= self-example`

## 已有依据

以下节点提取自现有设计说明，仅用于表达原因，不新增执行要求。

`[]:` 普通调参、重构、修复与方案迭代已有 Git 记录 `= git-history`

`[]:` 正式文档应使读者无需追溯旧提交、聊天记录或 Draft 就能理解当前内容 `= self-contained`

`[]:` Draft 用于暂存和交换材料，不承担正式知识来源的角色 `= draft-temporary`

`[]:` Draft 边界外的内容需要能独立理解、运行和验证 `= draft-independent`

`[]:` Demo 围绕稳定的研究问题持续演化 `= demo-question`

`[]:` 实验提出、检验共用能力需求，基础设施提供可组合的运行环境 `= experiment-infrastructure`

## 非元规范的原因

### 文档

`[git-history,self-contained]:` [documentation.md #最小化历史](documentation.md#最小化历史) `= documentation-minimize-history`

`[agent-reader,?]:` [documentation.md #表述](documentation.md#表述) `= documentation-wording`

`[organization,?]:` [documentation.md #组织](documentation.md#组织) `= documentation-organization`

### Draft

`[draft-temporary,?]:` [drafts.md #命名与边界](drafts.md#命名与边界) `= drafts-naming`

`[draft-temporary,draft-independent]:` [drafts.md #必须遵守](drafts.md#必须遵守) `= drafts-isolation`

`[draft-temporary]:` [drafts.md #使用与清理](drafts.md#使用与清理) `= drafts-cleanup`

### 实验

`[demo-question,experiment-infrastructure,?]:` [experiments.md #Demo 的演化](experiments.md#demo-的演化) `= experiments-evolution`

`[?]:` [experiments.md #验证与记录](experiments.md#验证与记录) `= experiments-verification`
