# Errors Log

Command failures, exceptions, and unexpected tool / API behavior.

Format follows the `self-improving-agent` skill (`~/.claude/skills/self-improving-agent/`).

Entry IDs: `ERR-YYYYMMDD-XXX`

## ERR-20260624-001 — subagent `git add` 把整个 working tree 拉进单 commit

**日期**: 2026-06-24
**Context**: 科目三 fab 流水线,派 subagent 生成 fab id=326 后让它自己 `git add <file> && git commit`
**症状**: 收到的 commit `56cc738` 含 696 files 203806 insertions,包括 02-iique 5 张 paper 整目录、110-the-art-of-loving 整本、其它未提交修改。完全偏离 fab 主题。

**根因分析**:
1. subagent 内部跑了某个 `git add` 动作(可能是 `git add -A` 或 `git add .`,prompt 里的 `git add "<具体路径>"` 没被严格执行)
2. commit 之前**没有** `git status` 校验 staged 列表
3. 主 loop 在 subagent 完成时只看 `git log --stat` 复核,**但** subagent 报回 commit SHA 时主 loop 也没立即 stat 验证

**修复**:
1. `git reset --hard cdfa84a` 回到污染前(上批 chore 记录点)
2. `git checkout ba974a7 -- <18/19/20 .md>` 提取 fab 文件
3. 逐个 `git add <file> && git commit` 重做 3 个干净 commit

**教训(Why)**:
- prompt 模板里的 `git add "<具体路径>"` **不够强**;subagent 容易在重置 working tree 状态时被"git add"惯用法拉走
- 主 loop 必须**强制在收到 commit SHA 后立刻 `git show --stat <sha> | tail -5` 复核**,如果 file count > 3 立即报警

**How to apply**:
- 派 fab subagent 的 prompt 必须**显式包含**:`(1) 严禁 git add -A / git add . / git commit -a;(2) git add <file> 后必须 git diff --cached --stat 确认只有目标文件;(3) commit 消息保持 feat: 《<标题>》—— 科目三 fable,严禁把 'mixed untracked' 之类的话术塞进 message`
- 主 loop 收到通知后,第一动作是 `git show --stat <sha>` 校验 file count == 1,异常立即排查不派下一批
