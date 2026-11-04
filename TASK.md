# 临时分支工作流讨论

purpose: 讨论并验证 e-m-c 的临时协作分支约定与 GitHub Actions 自动清理工作流。
done_when: 工作流的触发条件、权限、竞态与清理行为已达成结论；需要保留的修改已整合进 main；本分支不再需要继续讨论。

## 讨论范围

- 孤立分支的创建与跨 Agent 读写
- `.scratch/DONE` 的 push 事件与自动删除
- 工作流文件的继承、token 权限和 GitHub Actions 触发限制
- 并发提交、删除竞态及失败后的恢复策略

讨论记录和临时实验可以直接添加到本分支；完成前不要创建 `.scratch/DONE`。
