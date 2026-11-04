# 临时协作分支

用于跨机器、跨 Agent 共享和修改过程文件，不让临时交流进入正式分支的历史。

## 约定

- 使用 `scratch/<topic>` 命名，主题应简短、具体且有语义，例如 `scratch/runtime-review`。
- 需要 Git 工作副本时始终浅克隆（`--depth 1 --single-branch`）；创建临时分支时使用孤立分支（`git switch --orphan`），不继承 `main` 的提交历史。
- 创建时在分支根目录提交 `TASK.md`，写明用途与**结束条件**（`done_when`）。结束条件由参与者判断，不由自动化猜测。
- 多 Agent 可正常提交、拉取、推送；推送前先同步并处理冲突。临时分支不合并、不创建 PR。
- 重要结果应单独整合进正式代码、测试或文档；不要通过合并临时分支保留过程历史。
- 达成结束条件后，提交 `.scratch/DONE` 作为结束标志；不要在标记完成后继续向该分支写入。
- 每个临时分支都应携带从 `main` 复制的 [清理工作流](../.github/workflows/scratch-cleanup.yml)。当 `.scratch/DONE` 被推送时，由该分支的 `push` 事件立即触发清理；工作流只会在存在 `TASK.md` 和完成标志、且分支未发生后续更新时删除它。无需定时扫描。
- 不放入密钥或敏感数据。删除分支只移除 Git 引用，不能保证 GitHub 缓存、PR 引用或既有克隆中的历史立即消失。

## 创建

```bash
git clone --depth 1 --single-branch --branch main https://github.com/entropy356/e-m-c.git e-m-c-scratch
cd e-m-c-scratch
git switch --orphan scratch/runtime-review
# 孤立分支无父提交，但可从 main 复制所需的工作流文件
git restore --source=main -- .github/workflows/scratch-cleanup.yml
cat > TASK.md <<'EOF'
# Runtime review
purpose: Agent 之间交换运行时架构审查材料
done_when: 结论已整合进正式代码或文档，且不再需要临时交流
EOF
git add TASK.md .github/workflows/scratch-cleanup.yml
git commit -m "Start scratch/runtime-review"
git push -u origin HEAD
```

## 协作

```bash
git clone --depth 1 --single-branch --branch scratch/runtime-review \
  https://github.com/entropy356/e-m-c.git
# 修改文件后：git pull --rebase && git add ... && git commit ... && git push
```

## 结束

确认 `done_when` 已满足、需要保留的成果已进入正式分支后：

```bash
mkdir -p .scratch
printf 'done\n' > .scratch/DONE
git add .scratch/DONE
git commit -m "Finish scratch task"
git push
```

推送含 `.scratch/DONE` 的提交将触发分支内的工作流删除远程分支。若工作流被禁用、缺失或权限不足，可手动执行 `git push origin --delete scratch/runtime-review`。
