# Learnings Log

Corrections, knowledge gaps, and best practices learned during work on this project.

Format follows the `self-improving-agent` skill (`~/.claude/skills/self-improving-agent/`).

Entry IDs: `LRN-YYYYMMDD-XXX`

---

## [LRN-20260623-001] best_practice

**Logged**: 2026-06-23T17:48:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: docs

### Summary
Fable 目录里出现"合并版"和"拆分版"并存时，删合订保拆分，不动序号。

### Details
科目二第一章第一节的 fab 目录里：

- `07-基金监管机构和自律组织.md` —— "两道闸"故事，同时讲守夜司（监管机构）+ 亮茶棚（自律组织），对应教材的"三、(一) 基金监管机构"和"五、基金自律组织"两节合订。
- `08-基金监管机构.md` —— 单独讲守夜司。
- `09-基金自律组织.md` —— 单独讲亮茶棚/周伯。

`pdf-to-study-program` Phase 7 的硬性规则是 **1 个 H1 = 1 个 fab、严格 1:1 映射**。07 实际跨了两个 H1，是合订版，不是真·1:1。最近一次提交（`d68d373 chore: 方案 A 拆合订 fab 让 spec 1:1 对齐`）就是为此做的拆分。删掉 07，08/09 各自独立对齐，是把这条规则真正坐实。

用户明确说"序号先不动"——所以目录里会出现 07 缺位的跳号，不要自作主张去重排 08–31 的文件名。

### Suggested Action
- 删 fab 前先确认它是不是「合订版」。看 spec 索引或 H1 数：如果一个 fab 对应多个 H1，就是合订版，优先保留拆分版。
- 删完不动后续序号，接受跳号。如果用户后续要"补齐序号"，再统一 rename。
- 删之前先 `Read` 看一遍再 `rm`，避免误删。

### Metadata
- Source: user_feedback
- Related Files:
  - `04-基金从业/02-科目二-证券投资基金/converted/fables/01-证券投资基金概述/01-证券投资基金简介/07-基金监管机构和自律组织.md` (deleted)
  - `04-基金从业/02-科目二-证券投资基金/converted/fables/01-证券投资基金概述/01-证券投资基金简介/08-基金监管机构.md`
  - `04-基金从业/02-科目二-证券投资基金/converted/fables/01-证券投资基金概述/01-证券投资基金简介/09-基金自律组织.md`
- Tags: fable, pdf-to-study-program, phase-7, naming
- See Also: LRN-20260623-002

---

## [LRN-20260623-002] best_practice

**Logged**: 2026-06-23T17:48:00+08:00
**Priority**: low
**Status**: resolved
**Area**: config

### Summary
启用 self-improving-agent：在项目根下实例化 `.learnings/` 目录和 4 个文件。

### Details
用户在 `/self-improving-agent` 流程后确认"启用 self-improving-agent"。`self-improving-agent` skill 在我的工具列表里挂着，但项目下原本没有任何 `.learnings/` 实例化（hook 没有、目录没有、文件没有）。状态属于"加载了但未生效"。

实例化内容：
- `.learnings/LEARNINGS.md` — corrections / knowledge_gap / best_practice
- `.learnings/ERRORS.md` — 命令/工具失败
- `.learnings/FEATURE_REQUESTS.md` — 用户要的新能力
- `.learnings/INDEX.md` — 一表速查，列出每条 entry 的 ID/日期/area/summary/状态/文件链接

skill 自带的 `assets/` 目录下只有 `LEARNINGS.md` 和 `SKILL-TEMPLATE.md` 两个模板，没有 ERRORS.md 和 FEATURE_REQUESTS.md 的模板——所以这两个文件是参照 skill 文档里给的格式从零写的。

未来 hook 启用后可以自动提醒；目前是手写。下次用户调用 `/self-improving-agent` 时，第一步应该是 `ls .learnings/` 看现状再决定动作。

### Suggested Action
- 每次会话结尾有"纠正/失败/缺口"时，主动 append 一条 entry 到对应文件
- 定期 review `.learnings/INDEX.md`，对 `Recurrence-Count ≥ 3` 的条目考虑 promote 到 `CLAUDE.md` / `AGENTS.md`
- 如果要启用自动 hook：在 `.claude/settings.json` 加 `UserPromptSubmit` + `PostToolUse` 的 activator / error-detector 脚本引用（参考 `~/.claude/skills/self-improving-agent/SKILL.md` 末尾的 Hook Integration 章节）

### Metadata
- Source: user_feedback
- Related Files:
  - `.learnings/LEARNINGS.md` (created)
  - `.learnings/ERRORS.md` (created)
  - `.learnings/FEATURE_REQUESTS.md` (created)
  - `.learnings/INDEX.md` (created)
- Tags: meta, self-improving-agent, configuration
- See Also: LRN-20260623-001
