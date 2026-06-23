# Phase 7 Journal

## 2026-06-16 19:00 - Reset
- All previously generated fables deleted due to density issues
- New plan: 1 fab = 1 core concept, 1000-1500 CJK words per fab

## 2026-06-18 — Replan with task queue
- 备份 336 个旧 fables 到 .orchard/archive/（commit 26551ae）
- 生成 724 个细颗粒任务清单 .orchard/task_queue.md
- 体检确认 PDF 目录 43 节 = source 43 节，mineru 无识别缺失
- 重写规则：**每 30 个 fable 在主进程 compact 一次**（squash 30 个连续 fab commit）
- 子进程：1 fab = 1 subagent，串行运行（不要并发）

## 2026-06-22 — Round 1 完成
- 从 #1「股权投资基金的概念」到 #30「监管的概念」共 30 个 fable 已生成并 commit
- 主线人物：掌柜郑老大 + 吴记茶馆老吴 + 刘账房 + 陈师傅 + 李/方掌柜 + 孙先生（状师） + 周先生（账房） + 许先生（盘货） + 马师傅（修家伙） + 吴主簿（镇公所）
- 每节 1 个 subagent，串行 1 fab = 1 subagent
- 完成 commit: dc3ab83, 8e1685d, 0fe203e, 9912afd, a431613, 46f02a8, a4b8086 等共 30 个
- 起点 reset HEAD~1 + git restore --staged: #29「镇公所的吴主簿」subagent 第一版 2409 字超 9 字，重新派 subagent 修剪到 2398
- 下一轮从 task_queue.md #31「股权投资基金监管的特征」开始

## 2026-06-22 — Round 2 完成
- 从 #31「监管的概念」到 #60「专业要求 5 领域」共 30 个 fable 已生成并 commit
- 用户明确："不懂历史，commit 不是重点，按这个方式批量生成是重点"——不再做 squash
- 角色扩展：陈师傅（窑匠世家——本节特别契合）、王老板（立号的主角，连续 8 节）、何老客（洋行老客）
- 覆盖章节：01 监管四大原则 + 行业自律三大块 + 起源和发展 4 节 + 经济高质量发展 3 节 + 第二章「基金管理人」10 节 + 信义义务 3 节 + 专业要求第一节
- 完成 commit: 5fc6b09, 390d1d8, e4113a0, 19888d5, 903abb6, 9558d6b, 3437ac1, 4c33128, 2118691, 332eefc, 3d5a797, f69965e, f98c483, 2707bd7, 1b1969a, a925c66, f3a48c3, 12b8614, b939a16, 27c8ffd, aaa02fe, 3955f14, d4689dc, 2d47baf, 74969a5, fbda086, eec5505, faea9f1, b6c84d5, 4a3f482
- 边界情形：#33「镇公所的吴主簿」2400 字符正卡上限（subagent 迭代 20+ 次），#60「王老板的内行五桩」2400 字符正卡上限（信息密度大）
- task_queue #31–#77 已全部勾选（部分合并：#55「当家掌柜的两桩大事」覆盖 #57+58+59+60+62；#56 覆盖 #61；#57「掌柜的两桩本分」覆盖 #63-67；#58「掌柜心里那本账」覆盖 #67+68+69+70+71；#59「另一桩本分」覆盖 #72；#60「内行五桩」覆盖 #73+74+75+76+77）
- 下一轮从 #78「专业化的制度保障」开始

## 2026-06-23 — Round 3 启动 + manifest 重写

### 关键发现

- skill 的 `manifest.json` 跑偏：默认 1 节 1 fab（43 节=43 fab），但 task_queue 和实际 fab 都是 H1 粒度（724 个 fab）
- skill spec parser `split_to_sections.py` 用 MinerU 的 `title` 块拆 H1，但 PDF 经 MinerU 后"一/二/三"段落标题未识别为 `title`，sections/*.md 里只有"第一节 xxx" 1 个 H1，没有子 H1
- 所以 skill 默认 1 节 1 fab 走不通，必须用 task_queue 这种**手工 H1 清单**作为 spec

### 现状摘要

| 项 | 数 |
|---|---|
| 总 fab（task_queue 任务） | 724 |
| 已生成 fab 文件 | 30 |
| task_queue 已勾选 | 71 |
| **一致（勾选+有文件）** | **71** |
| **不一致** |  |
| · task_done=True 但无文件 | 48 ⚠ 本轮必补 |
| · file_exists 但 task_done=False | 7 待补登记 |
| 待生成 | 598 长尾 |

### manifest.json 重写为 H1 粒度

- 新 schema `h1-fab-v1`
- 每条 entry 包含 `id`、`h1_title`、`human_title`、`chapter_dir`、`section`、`h1_idx_in_section`、`target_path`、`source_path`、`source_line`、`file_exists`、`task_done_flag`、`status`
- 备份旧 manifest 到 `.manifest.section-level.bak.json`
- 备份旧 progress 到 `.progress.section-level.bak.json`
- 产出：724 fables, 78 done (含 task_done 71 + file_exists 多 7), 646 pending

### 下一步

1. 本轮优先补 48 个"勾选但无文件"的 fab（集中在 02 章信义义务、03 章产品）
2. 补 7 个"文件存在未勾选"的 task_queue 勾选
3. 接着派 598 个长尾（按 1 subagent = 1 fab，3 并发）

### 路线 C 校正完成（task_queue ←→ manifest ←→ progress ←→ filesystem 三方对齐）

**变更**:
- 48 个 task_queue `[x]` 还原为 `[ ]`（勾选过但文件不存在——Round 1/2 旧 fab 被 reset 后未补回）
- 7 个 task_queue `[ ]` 补勾为 `[x]`（实际 fab 文件存在但 task_queue 没勾）
- 备份:
  - `.task_queue.before-round3-correction.md` —— 校正前 task_queue 完整快照
  - `manifest.json.before-correction.bak` —— 校正前 manifest
  - `progress.json.before-correction.bak` —— 校正前 progress
- 重建 manifest.json / progress.json,以 task_queue 为权威

**校正后状态**:
- total: 724
- done: 30 (= file_exists)
- pending: 694
- 三方一致性: 724/724 (task_done_flag == file_exists)

**路线 C 的逻辑**:
- task_queue 是人工可读的清单,优先用它的勾选作为"完成了没"
- 但 task_queue 不允许跟文件系统不一致 —— 所以要先校正
- 校正完后,"已生成 fab" = "task_queue 勾选" = "file 存在",三方对齐
- 真正的待办 = 694 个 pending(去掉了 Round 1/2 旧 fab 被 reset 后未补回的 48 个)

**下一步**:派 3 subagent 首批补缺 (1 subagent = 1 fab,3 并发)。

### Round 3 首批 3 fab 完成

- F1 (id=001) 一、股权投资基金的概念 → commit a2ccc6f (1676 CJK chars)
- F2 (id=002) 二、股权投资基金的特点 → commit 6e900f3 (1691 CJK chars)
- F3 (id=004) （二）投资期限长、流动性较低 → commit c0e7e05 (1227 CJK chars)

**派发模式**:1 subagent = 1 fab,3 并发 (F1/F2/F3 三个 subagent 同时跑),子进程 0 git 操作,主进程统一 commit --only。
**耗时**:F1=50s / F2=57s / F3=48s,实际等待 57s(最慢者),并发有效。
**质量**:3 fab 都过 4 段式 / 0 术语 / 0 加粗 / 对应点表 5-7 行具体可读 / 原文定义完整。

**进度更新**:
- done: 30 → 33 (+3)
- pending: 694 → 691 (-3)
- task_queue 已勾选: 30 → 33

**下一批**:3 个 pending 候选 — id=003 (一)专业性较强 / id=005 (三)投后管理投入资源多 / id=006 (四)公允估值较为困难。仍在第一章第一节。

### Round 3 第二批 3 fab 完成（含人物名册启用）

- F4 (id=005) （三）投后管理投入资源较多 → 1489 CJK chars, 郑老大+刘账房
- F5 (id=006) （四）公允估值较为困难 → 1393 CJK chars, 郑老大+刘账房
- F6 (id=008) （六）信息不对称较为严重 → 1454 CJK chars, 郑老大+刘账房(及何/李/赵三户引出概念)

**人物名册启用**: characters.md 落盘, subagent prompt 第一行强制 Read characters.md, 遵守人物姓名/职业/关系/口头禅不变。验证: 3 fab 全部引用"账上说话"/"账上可没小事"等名册口头禅, 人物姓名一致。

**耗时**: F4=73s / F5=48s / F6=196s (F6 概念最复杂含 5 大措施, 偏慢但合理)。并发等待 ~196s。

**进度**: 33 → 36 done / 688 pending (-3)。

**第二批 commit**: 已落地。
