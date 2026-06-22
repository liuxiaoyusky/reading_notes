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
