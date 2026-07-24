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

---

## [LRN-20260624-003] knowledge_gap

**Logged**: 2026-06-24T23:10:00+08:00
**Priority**: low
**Status**: open
**Area**: tooling

### Summary
"字节 wavtts / 声音克隆" 与 "Miso One" 实时语音模型的开源与定价情况，外网检索被沙箱拦截，未能 100% 核实。

### Details
用户列出两个语音模型需求：
1. **字节 wavtts / 声音克隆** —— 大概率指火山引擎/豆包线上的 Seed-TTS 系列；字节没放完整开源权重，仅 API 可用。粗略单价约 ¥0.0008/千字（标准）+ 一次性声音克隆训练费；具体 SKU 名 / 最新价格需登录火山控制台。
2. **Miso One 实时语音** —— 公开信息不足；最可能是某个闭源配音 App 的 demo，或 CosyVoice / ChatTTS 的某个音色变体。需用户提供原始链接/截图才能定论。

外部检索受沙箱限制（WebSearch、WebFetch 对 google.com / github.com / modelscope 等全部 `Unable to verify if domain ... is safe`），只能在已有知识库 + 推理的基础上给出"最可能开源替代 = CosyVoice 2"的结论。

### Suggested Action
- 用户看到 Miso 原始出处时，把链接贴回对话，再做一次精准定位
- 后续若要拿字节官方报价，去火山引擎控制台 → 语音技术 → 大模型语音合成 页面截一张价格表存进 `.learnings/`
- 推荐本地替代：**CosyVoice 2**（`FunAudioLLM/CosyVoice`，Apache 2.0，2GB 权重，中文声音克隆 + 情感强），已写进 `tools/tts/README.md` 对照表

### Metadata
- Source: knowledge_gap
- Related Files:
  - `tools/tts/README.md` (created)
  - `tools/tts/generate_fables.py` (created)
  - `tools/tts/concat_audio.py` (created)
- Tags: tts, cosyvoice, bytedance, volcano, external-research, sandbox-limit
- See Also: _none_

---

## [LRN-20260624-004] best_practice

**Logged**: 2026-06-24T23:10:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: tooling

### Summary
批量 TTS + 长音频合并的标准流水线：迭代寓言 → 调本地 TTS → ffmpeg concat demuxer 合并。

### Details
科目三的寓言 fables 目录共 **370 篇 / ~2.2MB 文本 / 估算朗读 30 小时**。一次性合并的脚本要点：

1. **iter 顺序**：`Path.rglob("*.md")` 加 `sorted()` —— 文件名按 `01-.../02-.../03-...` 排列，字典序天然按"章 → 节 → 编号"遍历，不用额外建索引。
2. **文本抽取**：markdown 里 `## 🏺 寓言故事 —— 《...》` 标题之后、`---` 分隔之前的那段是纯故事正文，跳过原文定义 / 对应点表格 / 来源标注。
3. **音频格式**：先 wav（无压缩），再 ffmpeg 转 MP3 192kbps（CBR）。30 小时 mp3 大约 2.5GB，可接受。
4. **合并**：`ffmpeg -f concat -safe 0 -i list.txt -c copy` —— **无重编码**，快、零损。文件多时分块（每块 ≤100）再二次 concat，避免命令行超长 + 支持断点续跑。
5. **断点续跑**：`--skip-existing` 检查目标 mp3 是否已存在，重跑时自动跳过已完成的篇。
6. **manifest**：`manifest.json` 记录每篇的 ok / skipped / fail / empty 状态，方便定位失败的篇手工重跑。

### Suggested Action
- 跑流水线前先 `--limit 1` 验证链路（cosyvoice 服务是否起来、speaker 名是否正确、MP3 是否真的写到磁盘）
- 全量跑完后再跑合并；中途不要在另一个终端同时跑生成 + 合并，避免 list 抖动
- 想分章合并时用 `--pattern "01-*.mp3"` glob 直接过滤，不要临时改脚本
- 长音频（>10 小时）首次听建议用支持断点记忆的播放器（iPhone Books / macOS QuickTime 都不行 → 推荐 VLC / MPV）

### Metadata
- Source: self_derived
- Related Files:
  - `tools/tts/generate_fables.py` (created)
  - `tools/tts/concat_audio.py` (created)
  - `04-基金从业/03-科目三-私募股权/converted/fables/` (input, 370 fab files)
- Tags: tts, ffmpeg, concat-demuxer, batch-pipeline, mp3
- See Also: LRN-20260624-003
