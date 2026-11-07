# 元规范与因果关系

规范正文见 [文档](documentation.md)、[Draft](drafts.md) 和 [实验](experiments.md)；本文件只记录元规范、既有依据与因果关系。

## 记法

- `[^规范标识符]: 规范内容[^原因标识符]` 定义规范及其原因；多个原因连续写，如 `[^pragmatism][^agent-reader]`。
- `[^规范标识符]: [章节](文件.md#标题)[^原因]` 为其他 Markdown 文档中的章节登记原因，不复制正文。
- `[^root]` 是根规范标记，表示无须更上层的原因；元规范可以不写原因。
- `[^?]` 表示必填原因尚未补全，可与已知原因并列。此标记故意不定义为脚注，方便在 Markdown 渲染结果中发现未完成项。
- 脚注标识符采用语义化名称；嵌套的段落、列表和表格是章节内部结构，不自动产生独立规范。

## 节点索引

元规范：[^pragmatism] [^importance] [^required-reason] [^agent-reader] [^effective-output] [^organization] [^self-example]

已有依据：[^git-history] [^self-contained] [^draft-temporary] [^draft-independent] [^demo-question] [^experiment-infrastructure]

文档规则：[^documentation-minimize-history] [^documentation-wording] [^documentation-organization]

Draft 规则：[^drafts-naming] [^drafts-isolation] [^drafts-cleanup]

实验规则：[^experiments-evolution] [^experiments-verification]

> 注：Markdown 渲染器会将脚注定义汇总至页面末尾；上面的索引使它们在渲染后仍可见。因果关系以源 Markdown 中的脚注引用为准。

## 元规范

[^pragmatism]: 规范遵循实用主义[^root]

[^importance]: 规范按重要性排列

[^required-reason]: 非元规范必须注明原因

[^agent-reader]: 规范是给 Agent 读的[^root]

[^effective-output]: 规范无需正确，只要 Agent 能根据规范写出正确的代码与文档即可[^pragmatism][^agent-reader]

[^organization]: 规范按作用对象分文件，文件内部按规则性质分块

[^self-example]: 规范本身也须遵守 [文档规范](documentation.md)，作为示例

## 已有依据

以下节点提取自现有设计说明，仅用于表达原因，不新增执行要求。

[^git-history]: 普通调参、重构、修复与方案迭代已有 Git 记录

[^self-contained]: 正式文档应使读者无需追溯旧提交、聊天记录或 Draft 就能理解当前内容

[^draft-temporary]: Draft 用于暂存和交换材料，不承担正式知识来源的角色

[^draft-independent]: Draft 边界外的内容需要能独立理解、运行和验证

[^demo-question]: Demo 围绕稳定的研究问题持续演化

[^experiment-infrastructure]: 实验提出、检验共用能力需求，基础设施提供可组合的运行环境

## 非元规范的原因

### 文档

[^documentation-minimize-history]: [documentation.md #最小化历史](documentation.md#最小化历史)[^git-history][^self-contained]

[^documentation-wording]: [documentation.md #表述](documentation.md#表述)[^agent-reader][^?]

[^documentation-organization]: [documentation.md #组织](documentation.md#组织)[^organization][^?]

### Draft

[^drafts-naming]: [drafts.md #命名与边界](drafts.md#命名与边界)[^draft-temporary][^?]

[^drafts-isolation]: [drafts.md #必须遵守](drafts.md#必须遵守)[^draft-temporary][^draft-independent]

[^drafts-cleanup]: [drafts.md #使用与清理](drafts.md#使用与清理)[^draft-temporary]

### 实验

[^experiments-evolution]: [experiments.md #Demo 的演化](experiments.md#demo-的演化)[^demo-question][^experiment-infrastructure][^?]

[^experiments-verification]: [experiments.md #验证与记录](experiments.md#验证与记录)[^?]

## 特殊标记

[^root]: 根规范标记：根规范无需外部原因。此项是类型标记，不是独立的规范要求。
