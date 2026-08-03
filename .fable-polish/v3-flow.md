# 寓言大改润色 v3 — 整体流程

```
┌─────────────────────────────────────────────────────────────┐
│ Master Prompt v3 (v3-master.md)                             │
│   包含 改写规则 + 验收规则 + 失败反馈循环                    │
└─────────────────────────────────────────────────────────────┘
        ↓                                  ↑
   Subagent 1                            Subagent 2
   (改写 worker)                         (验收 reviewer)
        ↓                                  ↓
   写改后 .md                    评估每篇档位（A/B/C）
   写 _human_touch_log.md        不合格 → 把具体失败点反馈
        ↓                           ↓
        └────────→ 通过 ←────────────┘
                  ↓
            标记 "verified_A"
```

## 启动流程

每次启动一组（4-6 worker 并发）：

```
1. 主会话启动 N 个 Subagent 1（每个 worker 处理一章），背景任务
2. 等所有 Subagent 1 完成
3. 主会话启动 N 个 Subagent 2（验证 worker，每个对应一章），背景任务
4. 等所有 Subagent 2 完成
5. 主会话读 _review_log.md，统计通过率
6. 通过率 ≥80% → 进入下一组（章节未改的）
7. 通过率 <80% → 修改 prompt，循环补完本章
8. 全部章节 verified → commit
```

## Master 修改 Prompt 的时机

每次 Subagent 2 验收完一章，把 `_review_log.md` 看一遍：

### 情况 A：通过率 ≥ 80%

- Prompt 不改，继续
- 这一章标 "verified"，可以进入下一章

### 情况 B：通过率 < 80%

- 找失败原因：**是 worker 没遵守规则，还是规则本身不清楚？**
- 修改 master prompt 增加明确指令：
  - 例：如果 worker 普遍漏掉"心理停顿" → 在硬约束里加红色警告"心理停顿 ≤1 是上限，不是目标"
  - 例：如果 worker 普遍保留金句收尾 → 加"金句收尾 = FAIL"的红线
- 修改后，**只跑未通过的几篇**，不重跑整章（节省 token）
- 重新走 Subagent 1 → Subagent 2 循环
