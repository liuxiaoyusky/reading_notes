# 科目三 fab 流水线 supervisor 模式 — 设计

**日期**：2026-06-26
**作者**：Claude Opus 4.8（brainstorming session）
**状态**：探索中（用户要求记录后思考）

## 1. 上下文与起点

### 1.1 项目当前状态

- 项目：`04-基金从业/03-科目三-私募股权/`
- fab 总数：**724**
- 已 quality_passed：**418 / 724 = 57.7%**
- pending：**306**
- 失败 / 跳过：0
- 阶段：v2 orchard schema, 两阶段 review (spec + quality)
- 已踩坑：5 次外部污染 commit 事故

### 1.2 之前的工作模式（手跑）

- 主 session 自己跑 implementer subagent → 跑 spec review subagent → 跑 quality review subagent
- 主 session 自己 record 状态、自己 git commit
- 主 session 自己写 HANDOVER / checkpoint
- 每批 ~11 个 fab，主 session 上下文增长 ~5k-10k token
- 已成功跑 9 个 chunk（从 336 推到 418）

### 1.3 用户当前目标

> 「继续吧，从 379 推到 724 全部 quality_passed 或 skipped，中间不再人为介入。每 50 个 fab 写 HANDOVER。」

### 1.4 触发 brainstorming 的问题

> 「有其他的方法监督所有 batch 完成并优化上下文吗？」

---

## 2. 探索过程

### 2.1 第一轮：明确"监督"含义

用户选择：**「批量跑，每一批 3 个 subagent 轮流接受，走实现 验证等流程，主 session 回报+自动压缩上下文直到所有 batch 完成」**

锁定：
- 批量跑（不是单 fab 跑）
- 每批 3 个 subagent（implementer / spec / quality）
- 主 session 只看回报
- 自动压缩上下文
- 直到 724 完成（不是 429 停）

### 2.2 第二轮：明确"主 session 怎么自动压缩"

用户问「你有什么建议」，我推荐 4 层架构 supervisor 模式 + HANDOVER 兜底。

### 2.3 第三轮：定下架构

用户选 **方案 1**：supervisor 包打 3 个 sub-subagent（implementer / spec / quality）。我推荐。

理由（5 条）：
1. 契约最简单，主 session 只跟 supervisor 对话
2. 主 session 上下文增长 ≈ supervisor 回报大小（~200 token/批）
3. supervisor 内部可自杀重启（短寿工人 vs 长寿工头）
4. 状态合并点只有一个（spec → quality 状态转换 supervisor 内部处理）
5. 天然支持 checkpoint 边界处理

### 2.4 第四轮：用户追问"主 session 职责"

> 「主 session 处理流程问题，supervisor 处理业务问题？」

确认。我进一步澄清：
- 主 session 不做业务校验（4 条机械校验归 supervisor）
- supervisor 自己跑 `git show --stat`、自己数文件、自己判定 clean / dirty
- 主 session 只看 `verdict: clean | dirty`，dirty 时让用户介入

新锁定：
- 主 session **不**懂 git
- 主 session **不**懂 fab 路径
- 主 session **不**做 commit 校验
- 主 session **只**懂：checkpoint 数字 + verdict + 用户节奏

### 2.5 第五轮：摊开坏处

我列出 4 条真痛 + 3 条可忽略 + 1 条误解：

**A 类真痛**：
- A1：主 session 失去端到端可视化（用户问 "fab 425 讲什么" 时主 session 答不上）
- A2：supervisor 失败时主 session 盲（supervisor 撒谎怎么办）
- A3：supervisor 重启时状态丢失风险（race condition）
- A4：supervisor 之间不一致风险（retry 次数 / HANDOVER 格式不统一）

### 2.6 第六轮：用户指出核心问题

> 「加上人的话就是 4 层了，信息的传递会失真。」

**关键 insight**：4 层架构 = 4 次翻译 = 信息熵增。我之前把"上下文不增长"作为唯一优化目标，**忽视了信息失真代价**。

### 2.7 第七轮：探索替代方案

#### 信息失真的 4 种表现

1. **上下文压缩时的摘要腐烂**
   - 用户问 fab 425 内容 → 主 session dispatch read-only subagent → 摘要 200 token → 主 session 翻译给用户
   - 原始 800-1500 token fab 必然丢细节

2. **失败原因被层层抽象**
   - subagent 发现 fab 502 有禁用术语
   - supervisor 抽象成 `{failed_ids: [502], reason: "quality_failed"}`
   - 主 session 不知道是术语 / 字数 / 表格行数问题

3. **subagent 局部最优 vs supervisor 全局判断**
   - implementer 跑 11 个 fab 都过了
   - supervisor 看 HANDOVER 发现全用同一个比喻
   - 但 implementer 已结束，重启成本高 → 妥协接受

4. **用户意图层层转译**
   - 用户原话："每一批都用不同隐喻"
   - 主 session 翻译成 supervisor 参数
   - supervisor 翻译成 implementer prompt
   - implementer 理解成"只这一批"

#### 3 个候选方案

**方案 X：减到 3 层（去掉 supervisor）**

```
用户 ↔ 主 session ↔ subagent × 3 → 磁盘
```

- 信息失真：低（主 session 持业务上下文）
- 主 session 复杂度：高（重吃所有业务）
- 跨 session 鲁棒性：中（主 session 长寿但有上限）
- 上下文增长：~500-1000 token/批 × 145 批 ≈ 72k-145k token（接近 LLM 上限）

**方案 Y：减到 2 层（用户直对 supervisor）**

```
用户 ↔ supervisor ↔ subagent × 3
```

- 信息失真：最低（supervisor 自己知道 fab 内容，能直接答用户）
- 主 session 复杂度：最低（没有主 session）
- 跨 session 鲁棒性：高（supervisor 自杀重启 + 从 progress.json 续推）
- 风险：跨 session 一致性靠 prompt 模板，脆弱

**方案 Z：4 层 + 原文锚点（保真通道）**

```
用户 ↔ 主 session ↔ supervisor ↔ subagent
但每层之间保留"原始信息通道":
  - 用户原文直接传给 supervisor (避免主 session 翻译)
  - supervisor 把 subagent 输出原文存盘 (避免摘要压缩)
  - 主 session 持锚点路径,需要时直接 Read
```

- 信息失真：中（可回溯）
- 主 session 复杂度：中（懂磁盘路径）
- 跨 session 鲁棒性：高
- 复杂度：上升可控

### 2.8 第八轮：用户决定

> 「你记录一下我们的设计方案，和问题。我要好好想想」

---

## 3. 当前候选方案汇总

| 方案 | 架构 | 信息失真 | 主 session 复杂度 | 跨 session 鲁棒性 | 推荐度 |
|---|---|---|---|---|---|
| **1（旧推荐）** | 4 层纯抽象 (主 session + supervisor + subagent + 磁盘) | 高 | 最低 | 高 | ❌ 用户反对（信息失真） |
| **X** | 3 层 (主 session + subagent + 磁盘) | 低 | 高 | 中 | ⚠️ 上下文可能撑爆 |
| **Y** | 2 层 (supervisor + subagent + 磁盘) | 最低 | 最低（无主 session） | 高 | ⚠️ 跨 session 脆弱 |
| **Z** | 4 层 + 原文锚点 | 中（可回溯） | 中 | 高 | ⭐ 当前我推荐 |

---

## 4. 我当前的倾向

**方案 Z（4 层 + 原文锚点）**作为最佳折中：
- 保留 4 层监督结构（流程/执行分离）
- 加"原文锚点"通道降低信息失真
- 复杂度上升可控

### 4.1 方案 Z 待解决的设计点

1. **原文锚点放哪？**
   - HANDOVER 里？
   - journal.md？
   - 单独 `fab-originals/<batch>.md`？
2. **主 session 何时读锚点？**
   - 每批回报后自动 Read？
   - 用户问时再 Read？
3. **supervisor 何时写锚点？**
   - implementer 跑完立即写？
   - 整批通过才写？
4. **Z 方案的原文锚点会否抵消 4 层结构本身的优势？**
   - 主 session 又开始懂磁盘 / 路径 / IO 业务
   - 复杂度的 trade-off 怎么算？

---

## 5. 待用户决策

请用户考虑：
- Z 方案的 4 个设计点怎么定？
- 或者选回 X / Y？
- 或者完全推翻 4 层结构，找其他解？

设计进入 pending 状态，等待用户回复。
