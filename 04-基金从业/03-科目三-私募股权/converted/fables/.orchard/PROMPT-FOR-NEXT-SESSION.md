# 接力 Prompt — 科目三 fab 流水线(336/724 续推)

## 上下文

你是新 session,接手科目三 fab 流水线。

**当前进度**:
- `done_count = 336`, `pending_count = 388`, `total = 724`, **46.4% done**
- 已完成 fab id 1-336;剩 337-724
- 详细接力说明:`.orchard/HANDOVER-2026-06-24-progress.md`
- 第一份 HANDOVER(更早 session 的):`.orchard/HANDOVER-2026-06-24.md`
- 错误教训: `.learnings/ERRORS.md` (含 ERR-20260624-001)

**最近 commit 链**:
```
b9c6ab4 docs: HANDOVER-2026-06-24-progress (336/724 = 46.4%, 4 pollution incidents fixed)
d9b6f27 chore: record fab id=334/335/336 done
58f874b feat: 《（二）重置成本法》—— 科目三 fable
0231c40 feat: 《（三）清算价值法》—— 科目三 fable
6b46950 feat: 《五、风险资本估值法》—— 科目三 fable
```

## 第一步 — 验证接续点

```bash
cd /Users/sky/Documents/github/reading_notes

git log --oneline -3
# 期望: b9c6ab4 docs: HANDOVER-2026-06-24-progress (336/724 = 46.4%)

python3 -c "
import json
m = json.load(open('04-基金从业/03-科目三-私募股权/converted/fables/.orchard/manifest.json'))
print('done_count:', m['done_count'])       # 期望 336
print('pending_count:', m['pending_count']) # 期望 388
"

cat 04-基金从业/03-科目三-私募股权/converted/fables/.orchard/journal.md | tail -30
```

如果数字不对,先停下来排查。

## 第二步 — 找下一批 3 个 fab

**主任务**:每个 fab 派 1 个 subagent 并发跑。

```bash
# 找下一个 pending fab id (跳过 [x] 找第一个 [ ])
python3 -c "
import json, re
m = json.load(open('04-基金从业/03-科目三-私募股权/converted/fables/.orchard/manifest.json'))
done = {f['id'] for f in m['fables'] if f['status'] == 'done'}
for i in range(337, 725):
    sid = f'{i:03d}'
    if sid not in done:
        f = next(x for x in m['fables'] if x['id'] == sid)
        print(f'{sid} | {f[\"h1_title\"]} | section={f[\"section\"]} | target=...{f[\"target_path\"][-50:]}')
        break
"
```

挑 3 个连续 pending fab(如 337/338/339),写 3 个 prompt 文件:

**Prompt 模板路径**:`04-基金从业/03-科目三-私募股权/converted/fables/.orchard/prompts/05-投资项目估值__NNN.md`

格式参考 HANDOVER 里提到的纪律,可直接复用以下骨架(替换 NN 和具体 topic/line):

```markdown
你是一个寓言故事写手。**使用 `/fable-teacher` skill**，按其全部硬规则创作。

【任务】
1. **Read `/fable-teacher` skill 全文** (/Users/sky/.claude/skills/fable-teacher/SKILL.md)
2. **Read 源文件** `/Users/sky/Documents/github/reading_notes/04-基金从业/03-科目三-私募股权/converted/sections/<章节路径>.md`,重点关注 line X-Y
3. **写一个 NNN-NNN 字的连续叙事寓言** (按 fab 大小自适应)
4. **Write 到目标文件**:`<完整 target_path>`
5. **git commit** —— 严禁任何变体:
   ```bash
   cd /Users/sky/Documents/github/reading_notes
   git add "<完整 target_path>"
   git diff --cached --stat   # 校验只含 1 个目标文件
   git commit -m "feat: 《<标题>》—— 科目三 fable"
   ```

【源数据】
- 源 fab CJK: NNN(来自源文件 line X-Y)
- 故事主题(**仅供你把握方向,不要在故事里直接复述这些词**): <topic>
- 禁止专业术语清单: 股权投资基金/基金/管理人/托管人/LP/GP/私募/合格投资者/非公开交易/证监会/中国证券投资基金业协会/创业投资/并购基金/估值/收益分配/信息披露

【输出模板】
```markdown
# <标题>

## <emoji> 寓言故事 —— 《<4-6字故事名>》

<故事正文>

---

**📖 原文定义**

> 直接引用源文件 line X-Y 的原文

**💡 对应点**

| 故事元素 | 概念对应 |
|---------|---------|
| ... | ... |

---

> 📝 来源：股权投资基金(科目三)· <标题>
```

完成后回报:标题、字数、commit SHA。
```

## 第三步 — 派 subagent(并发 3 个)

主 loop **只发最小指令**(避免撑爆 context):

```
你的任务:按照 `.orchard/prompts/05-投资项目估值__NNN.md` 的完整步骤,生成 fab id=NNN 的寓言文件。

🚨 极重要 git 纪律 (来自 ERR-20260624-001 + 4b06097 + race condition 3 次教训):
- 严禁 git add -A / git add . / git commit -a / 不写具体路径的 git add
- prompt 里给的 git add/commit 命令逐字执行,不要"优化"
- git add 前先 git status --short 确认无他人 staged;如有,先 git restore --staged 清空
- git commit 前必须 git diff --cached --stat 校验只含 1 个目标文件
- commit message 保持原样,严禁 "mixed untracked" 字眼
- 严禁把别人尚未 commit 的文件"顺手"加进自己的 commit

核心要求:
1. Read /Users/sky/.claude/skills/fable-teacher/SKILL.md
2. Read .orchard/prompts/05-投资项目估值__NNN.md (任务书)
3. Write + git commit (自己跑)
4. 回报:只回报标题、CJK 字数、commit SHA,不要贴正文

派发来源:.orchard/prompts/05-投资项目估值__NNN.md,请 Read 它作为任务书。
```

**用 `Agent` tool + `run_in_background: true` 并发派 3 个**。

## 第四步 — 等通知 + 立即复核(关键)

**等 3 个 task-notification。** 收到后**第一动作是 `git show --stat <sha> | tail -3`** 复核 file count == 1。

如果 file count > 1:
- 立即停止派下一批
- 排查:可能是 subagent 误把他人文件一起 commit
- 修复:参照 HANDOVER 里 4 次污染事故的修复方法(reset --hard 到干净 commit + 抽文件 + 重新 commit)

## 第五步 — 主 loop 刷状态(必备)

3 个 fab 全部 commit 干净后:

```python
import json, datetime, re
base = '04-基金从业/03-科目三-私募股权/converted/fables/.orchard'
mf = json.load(open(f'{base}/manifest.json'))
pf = json.load(open(f'{base}/progress.json'))

target_ids = {'NNN', 'NNN+1', 'NNN+2'}
for f in mf['fables']:
    if f['id'] in target_ids:
        f['status'] = 'done'
        f['file_exists'] = True
        f['task_done_flag'] = True
mf['done_count'] = sum(1 for x in mf['fables'] if x['status']=='done')
mf['pending_count'] = sum(1 for x in mf['fables'] if x['status']=='pending')
for r in pf['records']:
    if r['id'] in target_ids:
        r['status'] = 'done'
        r['task_done_flag'] = True
        r['file_exists'] = True
pf['done'] = sum(1 for x in pf['records'] if x['status']=='done')
pf['pending'] = sum(1 for x in pf['records'] if x['status']=='pending')
pf['last_updated'] = datetime.datetime.now().isoformat(timespec='seconds')

json.dump(mf, open(f'{base}/manifest.json','w'), ensure_ascii=False, indent=2)
json.dump(pf, open(f'{base}/progress.json','w'), ensure_ascii=False, indent=2)
print(f'Manifest: done={mf["done_count"]} pending={mf["pending_count"]}')
```

然后 commit 状态文件:

```bash
git add 04-基金从业/03-科目三-私募股权/converted/fables/.orchard/
git diff --cached --stat   # 校验只含 manifest/progress/task_queue/journal
git commit -m "chore: record fab id=NNN/NNN+1/NNN+2 done (XXX/724 = YY.Y%)"
```

## 第六步 — 每 30 fab 主动写 HANDOVER

**强制规则**: 每完成 30 个 fab,**必须**写一份简短的 `.orchard/HANDOVER-<date>-progress.md` 给自己当接力点。本日 session 已在 336 处写过一份。

格式参考现有的 `HANDOVER-2026-06-24-progress.md`,包含:
- 当前 done_count / pending_count
- 本批完成 fab id
- 最近 5-10 个 commit
- 剩余 fab 分布预测
- 本段 session 内新增的事故 / 教训
- 下一步做什么

## 第七步 — 循环

```
派 NNN/NNN+1/NNN+2 → 等通知 → git show --stat 复核 → 主 loop 刷状态 + commit → 派 NNN+3/...
```

每 30 fab 写 HANDOVER。直到 done_count = 724。

## ⚠️ 致命陷阱(本日 session 4 次栽过)

1. **绝不用 `TaskOutput` 拉 subagent transcript** —— 用 task-notification 拿 status
2. **绝不 `git add -A` / `git add .` / `git commit -a`** —— 必须具体路径
3. **每个 commit 前 `git diff --cached --stat`** —— 确认只含 1 个目标文件
4. **`git add` 前 `git status --short`** —— 确认无他人 staged(race condition)
5. **`git reset --hard <干净 commit>` 比 `--soft` 安全** —— soft 会留 staged 边角
6. **不读 subagent transcript** —— 撑爆主 context 撞 200K 上限会死锁

## 关键文件位置

- 接力说明: `04-基金从业/03-科目三-私募股权/converted/fables/.orchard/HANDOVER-*.md`
- 状态文件: `.orchard/manifest.json`, `.orchard/progress.json`, `.orchard/task_queue.md`, `.orchard/journal.md`
- 错误教训: `.learnings/ERRORS.md`
- Prompt 模板: `.orchard/prompts/05-投资项目估值__NNN.md`
- 源文件: `04-基金从业/03-科目三-私募股权/converted/sections/05-股权投资基金的投资/03-投资项目估值.md`
- fable 落盘目录: `04-基金从业/03-科目三-私募股权/converted/fables/05-股权投资基金的投资/03-投资项目估值/`
- skill: `/Users/sky/.claude/skills/fable-teacher/SKILL.md`

## 预估剩余工作量

388 fab / 每批 3 ≈ **130 批** × 60-120 秒 ≈ **3-4 小时不间断**

新 session 同样要每 30 fab 主动写 HANDOVER 一次。
