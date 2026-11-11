# Draft 隔离

Draft 用于隔离文件。任何一个 Draft 都应可以无感删除。

## 命名与边界

- 文件用 `x.draft.y`（如 `memory.draft.md`），保留扩展名。
- 目录、Git 分支及仓库名以 `.draft` 结尾（如 `research.draft/`、`review.draft`）。

## 隔离
- 每个 Draft 相互独立，嵌套的 Draft 有独立边界。
- 对于任意一个Draft，其不得被外部文件提及（包括其他 Draft ，不包括issue、discussion等）；文档链接、代码导入、构建、测试、配置和工作流中的直接或间接依赖均在此范围内。
- Draft 内可以引用自身及正式内容。
- 隔离约束的是**持久引用和依赖**。普通 Git 提交祖先关系不视为 Draft 引用。
