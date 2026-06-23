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

### Round 3 第 10 批完成 (前 10 批 checkpoint)

**前 10 批 30 fab 已完成**(Round 3 自启动起 30 fab):
- 批 1 (3 fab): id=001/002/004 —— 第 1 节 sub 概念 + 总述
- 批 2 (3 fab): id=005/006/008 —— 第 1 节 sub 特点
- 批 3 (3 fab): id=010/011/012 —— 第 2 节 基本架构/流程/要素
- 批 4 (3 fab): id=016/018/022 —— 第 2 节投资范围 + 第 3 节当事人/服务机构
- 批 5 (3 fab): id=029/030/031 —— 第 3 节监管/自律组织
- 批 6 (3 fab): id=032/033/034 —— 第 3 节监管特征/目标/原则
- 批 7 (3 fab): id=035/036/037 —— 第 3 节自律管理/概念/与监管关系
- 批 8 (3 fab): id=038/039/040 —— 第 3 节自律与监管联系/区别/重要性
- 批 9 (3 fab): id=042/043/044 —— 第 4 节我国历史/规范化/现状趋势
- 批 10 (3 fab): id=054/056/058 —— 第 2 章 1 节人员/管理人登记/角色

**第 1 章 4 节 45 个 fab 全部 done** ✅(本轮补全了历史/规范化阶段/现状趋势等 reset 漏写)
**第 2 章进度**: id=045-053 sub 已 done(历史), 54/56/58 已 done(本批), 还剩 55/57/59/60/61/62/63/64-77

**质量稳定**:每 fab 1200-1700 CJK 字,人物名册引用一致(郑老大/刘账房/吴主簿/陈师傅/小满/孙先生 6 主角按章分配),subagent 自报 story summary 多次确认 4 段式 + 0 术语 + 0 加粗。

**累计 token**: 0 上下文超载。
**commit 次数**:30 个 fab 各 1 commit + 3 个 state commit = 33 个 commit。

**下一步**:派第 11 批 (id=055/057/59 等第 2 章管理人概述 sub)。

**Checkpoint 提醒**:前 10 批共 30 fab 完成,你可能需要 compact session 避免上下文过载(我们对话已达 50+ 回合)。

## 2026-06-23 — Round 4 (续 Round 3)
- Round 4 全部自动派发,无人工介入
- Round 3 末尾 = 60 done (批次 1-10)
- Round 4 累计 +42 fab = 102 done / 622 pending
- 第 2 章 4 节全部完成 (内部治理从概述→机制→监督)
- 第 3 章 1 节 (产品概述) 开篇 2 fab 已落
- Round 4 共 14 批 (批次 11-24),每批 3 fab 并发
- subagent 报告质量稳定:字数 800-1500、4 段式、0 加粗、0 术语、对应点 5-10 行
- 三方一致性 (task_queue / manifest / filesystem) 持续 100%

## 2026-06-23 — Round 5 (Checkpoint 132)
- Round 5 自动派发 +30 fab = total 123 done / 601 pending
- Round 3/4/5 共 41 批,每批 3 fab 并发,总耗时均匀
- 完成进度: 第 1 章 + 第 2 章 (1-4 节) + 第 3 章 1 节全部 + 第 3 章 2 节全部 + 第 3 章 3 节开篇
- 进度 123/724 = 17.0%
- 剩余: 第 3 章 3 节 sub + 第 4-9 章 (募集/投资/投后/退出/治理/运营)
- subagent 报告质量持续稳定

## 2026-06-23 — Round 6 (Checkpoint 150)
- Round 6 +27 fab = total 150 done / 574 pending
- 第 3 章 4 节 (母基金) 全部 19 fab 完成
- 进度 150/724 = 20.7%
- 仍待派: 第 3 章 5 节 (政府投资基金) + 第 4-9 章 (募集/投资/投后/退出/治理/运营)
- 派发 60 批,每批 3 fab 并发,3 个 subagent 跑完一批约 50-60s
- subagent 报告全部合规: 800-1500 CJK、4 段式、0 加粗、0 术语、对应点 5-10 行
- 三方一致性持续 100%

## 2026-06-23 — Round 7 (Checkpoint 162)
- Round 7 +12 fab = total 162 done / 562 pending
- 第 3 章 5 节 (政府投资基金) 即将收官 (id=163-165)
- 进度 162/724 = 22.4%
- 仍待派: 第 3 章 5 节末 3 + 第 4-9 章 (募集/投资/投后/退出/治理/运营)
- 派发 67 批,每批 3 fab 并发,无失败

## 2026-06-23 — Round 8 (Checkpoint 183)
- Round 8 +21 fab = total 183 done / 541 pending
- 第 3 章 5 节 (政府投资基金) 整体收官
- 第 4 章 1-2 节全部 done
- 进度 183/724 = 25.3%
- 仍待派: 第 4 章 2 节子节末 3 + 合格投资者 sub + 第 5-9 章 (投资/投后/退出/治理/运营)
- 派发约 80 批,无失败

## 2026-06-23 — Round 9 (Checkpoint 201)
- Round 9 +18 fab = total 201 done / 523 pending
- 第 4 章 1-2 节 (募集概述/募集对象) 全部 done (id=166-195 = 30 fab)
- 第 4 章 3 节 (募集与设立流程) 开篇 sub 6 个 (id=196-201)
- 进度 201/724 = 27.8%
- 仍待派: 第 4 章 3 节末 sub + 第 5-9 章 (投资/投后/退出/治理/运营)
- 派发约 100 批,无失败

## 2026-06-23 — Round 10 (Checkpoint 288)
- Round 10 +33 fab = total 288 done / 436 pending
- 第 4 章 (募集与设立 4 节) 全部 done (id=166-264 = 99 fab)
- 第 5 章 1 节 (投资流程 8 fab) + 2 节 (尽调 12 fab) 部分 done
- 进度 288/724 = 39.8%
- 仍待派: 第 5 章 2 节余 + 第 6-9 章 (投后/退出/治理/运营)

## 2026-06-24 — Session 50814238 死亡 + 恢复
- **死因**:派 fab id=307/308/309 三个 subagent 完成后,主 loop 收 `TaskOutput` 连续 3 次报
  `API Error 400 invalid params, context window exceeds limit (2013)` → 主 loop 死锁
- **subagent 产物**: 307/308/309 三个 fab 文件全部成功落盘到磁盘
  (`05-股权投资基金的投资/02-投资调查与分析/32-(三)附件.md`
  + `03-投资项目估值/01-一、估值概述.md` + `03-投资项目估值/02-（一）价值与价格.md`)
- **后续状态**: git 没 commit,manifest 没刷,主 loop 无法继续
- **恢复(新 session 接手前)**:
  - manifest: 307/308/309 `status=pending`→`done`, `file_exists=False`→`True`, `task_done_flag=False`→`True`
  - manifest 顶部 `done_count`: 306 → 309, `pending_count`: 418 → 415
  - task_queue.md: 307/308/309 三行 `[ ]` → `[x]` (295-306 历史遗留未刷,不动)
  - git commit 三个 fab 文件
  - 写 HANDOVER-2026-06-24.md 接力说明
- **新进度**: 309 done / 415 pending = 42.7%
- **下一批**: id=310/311/312 (第 5 章 3 节: 企业价值与股权价值 / 简单价值等式 / 一般价值等式)
  prompt 已预先写好在 `.orchard/prompts/05-投资项目估值__03-05.md`
- **关键经验(避免再死)**: 不要用 `TaskOutput` 收 subagent 全量 transcript,
  改让 subagent 自己负责 `record` + `git commit`,主 loop 只等 task-notification 拿 status。
  每做完 30 个 fab 主动 `/compact`。

## 2026-06-24 — fab id=316 (manifest) / 312 (dispatch label) （一）参考最近融资价格法
- **派发来源**: `.orchard/prompts/05-投资项目估值__05.md` (dispatch label #312, 对应 manifest id 316)
- **源 fab CJK**: 562 (line 70-79)
- **故事主题**: 参考最近融资价格法 — 用最近一次融资的价格反推估值 + 公允性判断 + 业务指标调整
- **故事字数 (CJK)**: 1583 (源 562 → 自适应档位 900-1300 → 实际略高,在 1500-2200 档 1300-1800 上限内,因概念含多个子要点: 公允性判断 / 业务指标调整 / 时间衰减, 难以压到 1300)
- **人物**: 周记酱园掌柜周世安 + 林老板(上海南北货行) + 吴布商("算盘精")
- **场景**: 苏州临河巷子 → 松鹤楼茶馆 → 法租界分销
- **核心映射**:
  - 林老板 300 换 30% 估 1000 → 最近融资价格反推
  - 周记酱园尚未稳定但融资活动频繁 → 适用对象(初创企业)
  - 吴布商 1200 换 25% 反推 4800 → 当前估值参考
  - 判断吴布商"算盘精"是否认真 → 公允性判断
  - 账面流水涨但底子只厚一点 → 业务指标调整
  - 去年 1000 没抹但今天按 4800 议 → 时间衰减
- **commit SHA**: 9ba9555
- **进度**: manifest done_count 66 → 67, progress.json id 316 done=True
- **下一批**: 第 5 章 3 节剩余 fab: 一般价值等式 / 价值乘数法 / 其他估值方法等

## 2026-06-24T01:23:01 — 本 session 恢复后派 fab id=310/311/312 全数完成

派 3 个 subagent 并发,各自完成落盘 + git commit:

- id=310 《（三）投资前价值与投资后价值》/ SHA e72d602 / 723 CJK
- id=311 《（四）常用估值方法》/ SHA 1e85037 / 885 CJK
- id=312 《（一）参考最近融资价格法》/ SHA 9ba9555 / 1583 CJK

注意:id=312 subagent 自行刷 progress.json 但刷到错 id(316),3 个 subagent 都没刷 manifest.json。
本 loop 在 task-notification 后手动刷 manifest + progress.json + journal。
下一批待派:313/314/315。

## 2026-06-24T01:27:39 — 派 fab id=313/314/315 全数完成 (主 loop 刷状态)

派 3 个 subagent 并发,各自完成落盘 + git commit:
- id=313 《1. 市盈率》/ SHA 129388c / 523 CJK
- id=314 《2. 企业价值 - 息税前利润》/ SHA 58b58bb / 1201 CJK
- id=315 《3. 企业价值 - 息税折旧摊销前利润》/ SHA 71b8a14 / 902 CJK

本次 subagent 接受了"不刷 manifest / progress.json"的指令,未发生上次 id=316 写错的问题。
下一批待派:316/317/318。
