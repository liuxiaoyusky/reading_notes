# 接力 Prompt — 科目三 fab 流水线(v2 orchard schema, 336/724 续推)

## 必读 — 本项目已迁移到 v2 orchard schema

你是新 session,接手科目三 fab 流水线。开始前必须 Read:
- `/Users/sky/.claude/skills/pdf-to-study-program/SKILL.md`
- `/Users/sky/.claude/skills/fable-orchestrator/SKILL.md`
- `/Users/sky/.claude/skills/fable-teacher/SKILL.md`

当前项目 `.orchard/manifest.json` 已迁移为 v2-compatible schema:
- manifest 使用 `sections[]`, 每个 entry 仍保留原 fab id `001`-`724`
- progress 使用 `sections{}` keyed by fab id
- legacy `done` 已迁移为 `quality_passed`; legacy `pending` 仍为 `pending`
- 不要使用旧的 `manifest["fables"]` / `progress["records"]` / `status="done"` 更新方式
- 不要运行 `orchard.py init` 重新生成 id; 本项目必须保留 `001`-`724`

本项目暂未启用 `universe_enabled`。如果用户明确要求共同人物宇宙,只从后续章节启用,且遵守:解释清楚内容 > 故事性 > 人物宇宙复用。

## 上下文

你是新 session,接手科目三 fab 流水线。

**当前进度**:
- `quality_passed = 336`, `pending = 388`, `total_fables = 724`, **46.4% quality_passed**
- 已完成 fab id 001-336 已迁移为 `quality_passed`;剩 337-724 为 `pending`
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
p = json.load(open('04-基金从业/03-科目三-私募股权/converted/fables/.orchard/progress.json'))
print('schema_version:', m['schema_version'])  # 期望 2
print('total_fables:', m['total_fables'])      # 期望 724
print('quality_passed:', sum(1 for x in p['sections'].values() if x['status']=='quality_passed'))  # 期望 336
print('pending:', sum(1 for x in p['sections'].values() if x['status']=='pending'))                # 期望 388
"

cat 04-基金从业/03-科目三-私募股权/converted/fables/.orchard/journal.md | tail -30
```

如果数字不对,先停下来排查。

## 第二步 — 找下一个 pending section

**主任务**:按新版 skill 的策略推进:优先 `1 section = 1 implementer`,串行跑 implementer → spec reviewer → quality reviewer。不要再按“每个 fab 一个 subagent 并发 3 个”推进,也不要手工改 `progress.json`。

```bash
# 找第一个仍有 pending 的 section,并列出该 section 的 pending fab id
python3 -c "
import json
m = json.load(open('04-基金从业/03-科目三-私募股权/converted/fables/.orchard/manifest.json'))
p = json.load(open('04-基金从业/03-科目三-私募股权/converted/fables/.orchard/progress.json'))
first = None
for s in m['sections']:
    if p['sections'][s['id']]['status'] not in ('quality_passed', 'skipped'):
        first = s['source_path']
        break
items = [s for s in m['sections'] if s['source_path'] == first and p['sections'][s['id']]['status'] not in ('quality_passed', 'skipped')]
print('source_path:', first)
print('pending_count_in_section:', len(items))
for s in items:
    print(f'{s[\"id\"]} | {s[\"h1_title\"]} | target=...{s[\"target_path\"][-60:]}')
"
```

当前接续点的第一个 pending section 应是:
- `converted/sections/05-股权投资基金的投资/03-投资项目估值.md`
- pending ids: `337`-`347`
- 共 11 个 pending fab,超过 9 个,按 skill 推荐应使用 acpx/独立 session；如果当前客户端没有 acpx,则拆成两个**串行** chunk(例如 `337`-`341`,再 `342`-`347`),不要并发写同一 section。

## 第三步 — 组装 implementer prompt

**Prompt 模板路径**:
- acpx/独立 session 可用时:`04-基金从业/03-科目三-私募股权/converted/fables/.orchard/prompts/05-投资项目估值__337-347.md`
- 只能用普通 subagent 时,拆成两个串行 chunk:`05-投资项目估值__337-341.md`、`05-投资项目估值__342-347.md`

主 session 先从 `manifest.json` 取本 section 的 pending fab 列表,再从源 markdown 抽取每个 H1 对应原文块,把 spec 全文塞进 prompt。implementer 不要自己重新扫描整本书。

```markdown
你是一个寓言故事写手。**使用 `/fable-teacher` skill**，按其全部硬规则创作。

【任务】
1. **Read `/fable-teacher` skill 全文** (/Users/sky/.claude/skills/fable-teacher/SKILL.md)
2. 按下面 fab_list 顺序,为每个 H1 写 1 个 fab,**1 H1 = 1 fab,禁止跨 H1 合订**
3. 每个 fab 写到 fab_list 指定的完整 target_path,文件名不能改编号、不能改标题
4. 故事正文按源内容自适应字数;末尾必须有「📖 原文定义」「💡 对应点」「📝 来源」
5. 写完后自检:文件存在、文件名匹配、无合订、0 加粗、0 专业术语、对应点 5-7 行
6. **git commit** —— 只提交本 prompt 的 target_path 文件,严禁任何变体:
   ```bash
   cd /Users/sky/Documents/github/reading_notes
   git add "<target_path_1>" "<target_path_2>" ...
   git diff --cached --stat   # 校验只含本 prompt 指定的目标文件
   git commit -m "feat: 《投资项目估值》—— 科目三 fables"
   ```

【源数据】
- fab_list:
  - 337 （一）风险资本估值法概述 → converted/fables/.../30-（一）风险资本估值法概述.md
  - ...
- spec 全文:
  ### H1 #30: （一）风险资本估值法概述
  <从源 markdown 抽取的该 H1 完整原文>

  ---

  ### H1 #31: （二）风险资本估值法的步骤
  <从源 markdown 抽取的该 H1 完整原文>

  ...
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

## 第四步 — 串行派 implementer

派发前先把本 chunk 的 id 逐个记录为 `implementer_dispatched`:

```bash
PROJECT=/Users/sky/Documents/github/reading_notes/04-基金从业/03-科目三-私募股权
ORCHARD=/Users/sky/.claude/skills/fable-orchestrator/scripts/orchard.py
for id in 337 338 339 340 341; do
  python3 "$ORCHARD" --project "$PROJECT" record --id "$id" --status implementer_dispatched --mode subagent
done
```

主 loop **只发最小指令**(避免撑爆 context),不要贴 spec 全文到主对话里:

```
你的任务:按照 `.orchard/prompts/05-投资项目估值__337-341.md` 的完整步骤,生成其中列出的寓言文件。

🚨 极重要 git 纪律 (来自 ERR-20260624-001 + 4b06097 + race condition 3 次教训):
- 严禁 git add -A / git add . / git commit -a / 不写具体路径的 git add
- prompt 里给的 git add/commit 命令逐字执行,不要"优化"
- git add 前先 git status --short 确认无他人 staged;如有,先 git restore --staged 清空
- git commit 前必须 git diff --cached --stat 校验只含本 chunk 的目标文件
- commit message 保持原样,严禁 "mixed untracked" 字眼
- 严禁把别人尚未 commit 的文件"顺手"加进自己的 commit

核心要求:
1. Read /Users/sky/.claude/skills/fable-teacher/SKILL.md
2. Read .orchard/prompts/05-投资项目估值__337-341.md (任务书)
3. Write + git commit (自己跑)
4. 回报:只回报每个文件标题、CJK 字数、commit SHA,不要贴正文

派发来源:.orchard/prompts/05-投资项目估值__337-341.md,请 Read 它作为任务书。
```

不要并发派多个 implementer 写同一 section。等本 chunk 完成并 review 通过后,再派下一个 chunk 或下一个 section。

## 第五步 — 等通知 + 立即复核(关键)

收到 task-notification 后**第一动作是 `git show --stat <sha> | tail -20`** 复核只包含本 chunk 的目标文件。

如果出现非目标文件:
- 立即停止派下一批
- 排查:可能是 subagent 误把他人文件一起 commit
- 修复:参照 HANDOVER 里 4 次污染事故的修复方法(reset --hard 到干净 commit + 抽文件 + 重新 commit)

实现完成后先记录 `implementer_done`:

```bash
for id in 337 338 339 340 341; do
  python3 "$ORCHARD" --project "$PROJECT" record --id "$id" --status implementer_done --mode subagent
done
```

然后跑两阶段 review:
- Stage 1: 用 `/Users/sky/.claude/skills/pdf-to-study-program/spec-reviewer-prompt.md` 验证文件存在、命名、1:1 映射、无合订
- Stage 2: spec 通过后,用 `/Users/sky/.claude/skills/pdf-to-study-program/quality-reviewer-prompt.md` 验证故事质量
- reviewer 输出保持 200-300 token,不要把全文贴回主 session

review 通过后只用 `orchard.py record` 更新状态:

```bash
for id in 337 338 339 340 341; do
  python3 "$ORCHARD" --project "$PROJECT" record --id "$id" --status spec_passed --reviewer spec --verdict pass
  python3 "$ORCHARD" --project "$PROJECT" record --id "$id" --status quality_passed --reviewer quality --verdict pass
done

python3 "$ORCHARD" --project "$PROJECT" status
```

如果任一 reviewer 失败:
- 不要记录 `quality_passed`
- spec 失败记录:`record --id <id> --status spec_failed --reviewer spec --verdict fail --notes "<具体问题>"`
- quality 失败记录:`record --id <id> --status quality_failed --reviewer quality --verdict fail --notes "<具体问题>"`
- 把 reviewer 的具体问题写进下一轮修复 prompt,修完后重新从 Stage 1 spec review 开始

然后 commit 状态文件:

```bash
git add 04-基金从业/03-科目三-私募股权/converted/fables/.orchard/progress.json \
        04-基金从业/03-科目三-私募股权/converted/fables/.orchard/journal.md
git diff --cached --stat   # 校验只含 progress/journal
git commit -m "chore: record fab id=337-341 quality_passed (XXX/724 = YY.Y%)"
```

## 第六步 — 每 30 fab 主动写 HANDOVER

**强制规则**: 每完成 30 个 fab,**必须**写一份简短的 `.orchard/HANDOVER-<date>-progress.md` 给自己当接力点。本日 session 已在 336 处写过一份。

格式参考现有的 `HANDOVER-2026-06-24-progress.md`,包含:
- 当前 quality_passed / pending
- 本批完成 fab id
- 最近 5-10 个 commit
- 剩余 fab 分布预测
- 本段 session 内新增的事故 / 教训
- 下一步做什么

## 第七步 — 循环

```
派 NNN/NNN+1/NNN+2 → 等通知 → git show --stat 复核 → 主 loop 刷状态 + commit → 派 NNN+3/...
```

每 30 fab 写 HANDOVER。直到 quality_passed = 724。

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
