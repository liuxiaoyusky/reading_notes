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
