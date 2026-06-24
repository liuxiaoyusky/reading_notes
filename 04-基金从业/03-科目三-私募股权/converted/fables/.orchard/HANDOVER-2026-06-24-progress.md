# 接力说明 — 2026-06-24 (第二份,本日续 session)

> 本文档接续 `.orchard/HANDOVER-2026-06-24.md`(第一份,记录 session `50814238` 死锁 + 恢复至 309/724)。

## 上下文

**上一个 session** 在 HANDOVER-2026-06-24 第一份交接后,**主 loop 上下文逐步膨胀**(累计派 9 批共 27 个 fab + 经历 4 次 git 污染事故修复)。session 内累计统计:

- ✅ 完成 fab id = 310 ~ 336,共 27 个 fab 落盘
- ✅ 当前进度 **336/724 = 46.4%** done
- ✅ 已 commit `d9b6f27 chore: record fab id=334/335/336 done`
- ⚠️ 已累计 30 fab 触发 /compact 阈值,但本 session 无手动 compact 工具
- 🚦 上下文已膨胀,继续派活有撞 200K 上限风险

新 session 接手时,**所有 fab 文件 + commits + 状态文件都已落盘**,可直接从 337 继续。

## 本日 session 内事故清单(4 次,全部已修复)

### 事故 1:ERR-20260624-001 — subagent 326 commit `56cc738` 696 files
**根因**: subagent 内部跑了某个 `git add` 变体(`git add -A` 或 `git add .` 或类似),把整个 working tree 加进去
**修复**: `git reset --hard cdfa84a`(污染前)+ `git checkout ba974a7 -- <18/19/20>` 抽 fab 文件 + 3 个 1-file commit
**教训** (已落入 `.learnings/ERRORS.md`): prompt 模板必须显式禁止 `git add -A` / `git commit -a`,且强制 `git diff --cached --stat` 校验

### 事故 2:我自己 add ERRORS.md 时触发 695 files 污染 (`3d87d17`)
**根因**: `git add .learnings/ERRORS.md` 之前,某些 staged 状态被保留(可能 reset --soft 的边角效应)
**修复**: `git reset --hard 9916b6b` 回到干净点,然后手动 `Write` + `git add` + `git diff --cached --stat` 校验后再 commit
**教训**: 任何 `git add` 之前都先 `git status --short` 确认没有遗留 staged

### 事故 3:`4b06097` 2-file commit 错 message (fab 21 + fab 23 一起)
**根因**: 这是事故 1 的"边角"——污染 commit `56cc738` 里其实有 fab 21 + fab 23 的文件(被 reset 撤回后,这些文件的 working tree 内容保留),后续有 subagent 用 reset --soft 试图拆 commit 时,只 staged 了 fab 22(红利折现模型,内容是 fab 329),fab 21 + fab 23 仍在 4b06097 commit 里
**修复**: `git reset --hard 2ead1ad` 回到干净点 → `git show <commit>:<path>` 抽 fab 文件 → 重新做 3 个 1-file commit:`8abc177`(fab 21) + `129db6f`(fab 22) + `85fc27e`(fab 23)
**教训**: `git reset --soft` 不一定把 working tree 里**已有**的文件 staged 回来(因为它们 index entry == HEAD tree)。遇到这种情况需要 `git checkout <commit> -- <path>` 或 `git show <commit>:<path> > file` 抽文件。

### 事故 4:本批 3 subagent 并发 race condition(334/335/336)
**根因**: 3 个 subagent 并发写不同 fab 文件,但 `git add` 时 staging 区是共享的 —— subagent A `git add <A's file>` 时如果 staging 区已有 B 的文件(被 B 预先 add 但未 commit),A 的 commit 就把 B 的文件一起带进去
**修复**: 3 个 subagent **各自**做了 `git reset --soft HEAD~1` + `git restore --staged <他文件>` + 重 commit,最终 main 链上是 3 个 1-file commit 干净(`58f874b` / `0231c40` / `6b46950`)
**教训**: prompt 模板里需加上"git add 前必须先 `git restore --staged .` 清空 staged 区,或 `git status --short` 确认无他人 staged 文件"。当前 subagent 已自发学会 reset --soft 自修复。

## 当前状态(接续点)

```
done_count = 336
pending_count = 388
total = 724
percent = 46.4%
```

### 已完成的章节进度

- ✅ 第 5 章 3 节 估值(部分):fab id 313-336,共 24 个 fab 落盘
  - 估值章**还没结束**,剩 fab id 337-342+:
    - 337 (一) 风险资本估值法概述
    - 338 (二) 风险资本估值法的步骤
    - 339 1. 估计目标公司在股权投资基金退出时的股权价值
    - 340 2. 计算当前股权价值
    - 341 3. 估计股权投资基金在退出时的要求持股比例
    - 342 六、股权投资基金的估值应用
    - (后续可能还有更多子节,manifest 看 342 后是什么)

### git chain 最近 commit

```
d9b6f27 chore: record fab id=334/335/336 done (336/724 = 46.4%)
58f874b feat: 《（二）重置成本法》—— 科目三 fable
0231c40 feat: 《（三）清算价值法》—— 科目三 fable
6b46950 feat: 《五、风险资本估值法》—— 科目三 fable
5486e11 chore: record fab id=331/332/333 done (333/724 = 46.0%)
b258a51 feat: 《（四）企业自由现金流折现模型》—— 科目三 fable
2a2a29a feat: 《四、成本法》—— 科目三 fable
5cc77fa feat: 《（一）账面价值法》—— 科目三 fable
0b16a2c chore: record fab id=328/329/330 done + 4b06097 拆 commit 修复 (330/724 = 45.6%)
85fc27e feat: 《（三）股权自由现金流折现模型》—— 科目三 fable
129db6f feat: 《（二）红利折现模型》—— 科目三 fable
8abc177 feat: 《3. 现金流折现法的优点和不足》—— 科目三 fable
2ead1ad docs: ERR-20260624-001 subagent git add 污染回滚教训
```

## 接下来要做的事

### 第 1 步 — 验证恢复正确

```bash
cd /Users/sky/Documents/github/reading_notes
git log --oneline -3
# 应该看到:d9b6f27 chore: record fab id=334/335/336 done

python3 -c "
import json
m = json.load(open('04-基金从业/03-科目三-私募股权/converted/fables/.orchard/manifest.json'))
print('done_count:', m['done_count'])   # 应该是 336
print('pending_count:', m['pending_count'])  # 应该是 388
"
```

### 第 2 步 — 派下一批 fab id=337/338/339

写 3 个新 prompt 文件(命名 `.orchard/prompts/05-投资项目估值__337.md` 等),然后并发派 3 个 subagent。

**预期**: ~50-90 秒完成,3 个 fab 各 500-1000 CJK 故事。

**关键 prompt 纪律**(已强化,可直接复用):

```
🚨 极重要 git 纪律 (来自 ERR-20260624-001 + 4b06097 + race condition 3 次教训):
- 严禁 git add -A / git add . / git commit -a / 不写具体路径的 git add
- prompt 里给的 git add/commit 命令逐字执行,不要"优化"成更短的命令
- git add 前必须 git status --short 确认无他人 staged 文件;如有,
  先 git restore --staged <他文件> 清空再 add 自己的
- git commit 前必须 git diff --cached --stat 校验 staged 区只含 1 个目标文件
- commit message 保持原样,严禁出现 "mixed untracked" 字眼
- 严禁把别人尚未 commit 的文件"顺手"加进自己的 commit
```

### 第 3 步 — 循环 + 每 30 fab 主动 compact

- 派 337/338/339 → 等 notification → **立即 `git show --stat <sha>` 复核 1-file** → 主 loop 亲自刷 manifest + commit → 派 340/341/342
- 每做完 30 fab,**强烈建议主 loop 写一份简短 HANDOVER 给自己**(避免 session 上下文膨胀到撞 200K)
- 用 `task_queue.md` 找下一个 `[ ]`,不要完全相信 `manifest.done_count`

## 剩余 fab 分布预估

按 manifest 推进,大致结构:
- 第 5 章 3 节 估值:剩 fab 337-342 (6 fab),后续可能有更多子节
- 第 5 章 4 节 交易文件/结构:估计 20-40 fab
- 第 5 章 5 节 投后管理:估计 20-40 fab
- 第 6 章 投后管理 / 投后监督 / 风险:估计 50-80 fab
- 第 7 章 股权投资基金退出:估计 60-100 fab
- 第 8-9 章 治理 / 运营 / 争议解决:估计 100-150 fab

**总剩余 388 fab / 每批 3 fab ≈ 130 批 × 60-120s ≈ 3-5 小时不间断**(新 session 同样要每 30 fab 主动 compact 一次)

## 关键经验(避免再死 + 避免污染)

1. **不要用 `TaskOutput` 收 subagent 全量结果** —— 它会把整个 subagent transcript 拉回主 context,3 个 fab × 几 KB 就爆。换法:等 `task-notification` 拿 status。

2. **派 subagent 时不要把整段 prompt 都塞在 main loop 里** —— prompt 模板已经写在 `.orchard/prompts/` 下,新 session 只发一个 "Read prompt file X, dispatch subagent, await notification" 的最小指令。

3. **每 30 个 fab 主动 /compact** —— 但本 session 无手动 compact 工具,**只能靠主动写 HANDOVER 给下 session 替代**。本 HANDOVER 文件就是为此目的。

4. **收 subagent 通知后,第一动作是 `git show --stat <sha> | tail -3` 复核 file count == 1** —— 异常立即排查不派下一批。

5. **`git add <path>` 前先 `git status --short` 确认无他人 staged** —— race condition 防御。

6. **如果 commit 出问题,`git reset --hard <干净 commit>` 比 `git reset --soft` 安全** —— soft 会留 staged 边角状态污染后续。

## 死因(给未来 session 提个醒)

50814238 (前一个 session) 死因:用 `TaskOutput` 拉 subagent 全量 transcript,3 subagent × 几 KB = 主 context 撞 200K → API 400 → 死锁。

本日 session 内 4 次污染事故都已修复,但**主 loop 上下文持续膨胀**(每次派活 + 收通知 + 修复污染都会加 KB),**今日 session 在 336 done 时主动停下写 HANDOVER**,避免下个 session 再陷入同样的死锁。

新 session 接手时:
- main 上 `git log` 看到的 chain **是干净的**(3 个污染 commit `56cc738` / `3d87d17` / `04027e6` 都在 reflog 里待 gc,不在 main chain)
- fab 文件 `04-基金从业/03-科目三-私募股权/converted/fables/05-股权投资基金的投资/03-投资项目估值/` 下有 1-29 文件 = fab 313-336 内容(部分文件名 `__NN` 编号与 manifest id 错位 1-2 位是历史问题,但路径里的 `NN-<title>.md` 与 manifest `target_path` 一致)
- 状态文件 `.orchard/manifest.json` + `progress.json` + `task_queue.md` + `journal.md` 都已同步
- 教训文件 `.learnings/ERRORS.md` 已写入 ERR-20260624-001

**新 session 必须避开以下循环**:
- 只 Read subagent 末尾回报(用 task-notification 拿 status,绝不拉 transcript)
- 写新 prompt 文件而非在 main loop 里塞 prompt 文本
- 每 30 fab 主动写 HANDOVER(本日第二次接力说明即此功能)
- `git show --stat` 复核 1-file 是主 loop 的 reflex
