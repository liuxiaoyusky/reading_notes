# Fable Regenerator Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 写一个 Claude Code Workflow 脚本，并行 spawn subagent 重新生成全部 ~163 个科目二寓言故事文件，统一为《老陈的陶罐》的连续叙事风格。

**Architecture:** 使用 Claude Code Workflow 工具，按章节分批并行处理。每个 subagent 接收源 markdown + 风格指南 + 三范例文件路径，生成高质量连续叙事风格的 fable，直接覆盖写入原文件。

**Tech Stack:** Claude Code Workflow (JavaScript), Agent/Read/Write/Bash 工具

---

## 项目上下文

- **仓库根目录**: `/Users/sky/Documents/github/reading_notes`
- **源文件目录**: `04-基金从业/02-科目二-证券投资基金/converted/sections/<章>/<节>.md`
- **Fable 目录**: `04-基金从业/02-科目二-证券投资基金/converted/fables/<章>/<节>/<序号>-<标题>.md`
- **映射规则**: `fables/<章>/<节>/<fable>.md` → `sections/<章>/<节>.md`（去掉最后的 fable 文件名，节目录名加 `.md`）
- **三范例文件**（保留不动，作为风格参考）:
  1. `converted/fables/01-证券投资基金概述/01-证券投资基金简介/01-证券投资基金概念.md`
  2. `converted/fables/02-基金的类型/02-股票基金/01-股票基金的概念与特点.md`
  3. `converted/fables/02-基金的类型/07-指数基金/01-指数基金的概念与特点.md`

---

### Task 1: 备份现有 fables 目录

**目标:** 防止误操作导致数据丢失，保留现有 fables 作为回退。

**Files:**
- 无文件创建/修改

**Step 1: 创建备份**

```bash
cd /Users/sky/Documents/github/reading_notes
cp -r "04-基金从业/02-科目二-证券投资基金/converted/fables" \
   "04-基金从业/02-科目二-证券投资基金/converted/fables.backup.20260611"
```

**验证:**

```bash
ls -la "04-基金从业/02-科目二-证券投资基金/converted/fables.backup.20260611" | head -5
```

Expected: 显示备份目录内容，与 fables 目录一致。

**Step 2: Commit 备份标记**

```bash
git add -A
git commit -m "backup: fables before regeneration

备份现有寓言故事文件，共 $(find '04-基金从业/02-科目二-证券投资基金/converted/fables.backup.20260611' -name '*.md' | wc -l) 个文件。

下一步将使用 Workflow 脚本全部重新生成。"
```

---

### Task 2: 创建 Workflow 脚本框架

**目标:** 创建 Workflow 脚本的基本结构（meta + 常量 + 框架）。

**Files:**
- Create: `.claude/workflows/regenerate-fables.js`

**Step 1: 创建脚本框架**

```javascript
export const meta = {
  name: 'regenerate-fables',
  description: 'Regenerate all fables with high-quality continuous narrative storytelling',
  phases: [
    { title: 'Scan', detail: 'Discover all existing fable files and build task list' },
    { title: 'Generate', detail: 'Parallel subagent generation per chapter' },
    { title: 'Review', detail: 'Sample and verify output quality' },
  ],
}

// ===== 路径常量 =====
const REPO_ROOT = '/Users/sky/Documents/github/reading_notes'
const FABLES_BASE = '04-基金从业/02-科目二-证券投资基金/converted/fables'
const SECTIONS_BASE = '04-基金从业/02-科目二-证券投资基金/converted/sections'

// 三范例文件路径（subagent 会读取这些文件获取风格参考）
const EXAMPLE_FILES = [
  '04-基金从业/02-科目二-证券投资基金/converted/fables/01-证券投资基金概述/01-证券投资基金简介/01-证券投资基金概念.md',
  '04-基金从业/02-科目二-证券投资基金/converted/fables/02-基金的类型/02-股票基金/01-股票基金的概念与特点.md',
  '04-基金从业/02-科目二-证券投资基金/converted/fables/02-基金的类型/07-指数基金/01-指数基金的概念与特点.md',
]

// ===== 风格指南（嵌入在 subagent prompt 中） =====
const STYLE_GUIDE = `
你是金融寓言故事作家。你的任务是把枯燥的金融教材概念，变成生动的、有情节的寓言故事，帮助考生通过故事记忆概念。

【硬性规则——违反任意一条即为不合格】

1. **一个完整的故事**：必须有开头、发展、高潮、结局的完整叙事弧线。禁止条目式结构（如"第一个角色...第二个角色..."、"### 第一点...第二点..."）。故事必须从头到尾连续讲述，像一篇短文。

2. **必须有具体人物**：人物要有名字或具体身份，有对话和互动。
   ✓ 好："村民阿福说：'老周，我这十两银子...'"
   ✗ 差："投资者将资金交给管理人..."

3. **概念融入情节**：概念必须自然融入故事事件中，读者看完故事就懂了。不能在故事讲完后再贴概念解释。
   ✓ 好：老周贴告示谁都可以加入 → 自然引出公募基金的概念
   ✗ 差：先讲"公募基金是公开募集的"，再补一句"就像老周贴告示一样"

4. **叙事优先**：故事占全文 60% 以上。先有故事，后有原文定义和对应点表格。

5. **故事长度**：600-1200 字。太短讲不清，太长记不住。

6. **数学/公式类概念**：用生活场景中的具体事件来演示。比如用"分粮食"解释期望值，用"打赌"解释期权。
`.trim()

// ===== 从 fable 路径推断源文件路径 =====
function getSourcePath(fablePath) {
  // fable:  .../fables/<章>/<节>/<fable>.md
  // source: .../sections/<章>/<节>.md
  const parts = fablePath.split('/')
  // parts: [..., 'fables', '<章>', '<节>', '<fable>.md']
  const fablesIdx = parts.indexOf('fables')
  const chapter = parts[fablesIdx + 1]
  const section = parts[fablesIdx + 2]
  const baseParts = parts.slice(0, fablesIdx)
  return [...baseParts, 'sections', chapter, section + '.md'].join('/')
}

// ===== Scan Phase =====
phase('Scan')
log('Scanning existing fable files...')
```

**验证:**

```bash
cd /Users/sky/Documents/github/reading_notes
node -e "
const fs = require('fs');
const code = fs.readFileSync('.claude/workflows/regenerate-fables.js', 'utf8');
console.log('File size:', code.length, 'chars');
console.log('Has meta:', code.includes('export const meta'));
console.log('Has STYLE_GUIDE:', code.includes('STYLE_GUIDE'));
console.log('Has getSourcePath:', code.includes('getSourcePath'));
"
```

Expected: 全部返回 true，文件大小 > 1000。

**Step 2: Commit**

```bash
git add .claude/workflows/regenerate-fables.js
git commit -m "feat: create fable regenerator workflow framework"
```

---

### Task 3: 实现 Scan Phase

**目标:** 遍历现有 fables 目录，构建任务列表（每个 fable 文件一个任务，记录对应的源文件路径）。

**Files:**
- Modify: `.claude/workflows/regenerate-fables.js`

**Step 1: 添加 Scan Phase 实现**

在文件末尾（`phase('Scan')` 之后）添加：

```javascript
// ===== Scan Phase =====
phase('Scan')
log('Scanning existing fable files...')

const scanResult = await agent(`
请扫描目录 "${REPO_ROOT}/${FABLES_BASE}" 下的所有 .md 文件（递归），构建任务列表。

对于每个 .md 文件，记录：
1. fablePath: 文件的完整相对路径（从 repo root 开始）
2. sourcePath: 对应的源文件路径（使用规则：把路径中的 /fables/ 换成 /sections/，去掉最后的文件名，把倒数第二级目录名加上 .md）
3. chapter: 章名称（路径中 fables 后面的第一级目录名）
4. section: 节名称（路径中 fables 后面的第二级目录名）
5. title: fable 文件名去掉 .md 和序号前缀（如 "02-基金当事人.md" → "基金当事人"）

示例：
- fable: 04-基金从业/02-科目二-证券投资基金/converted/fables/01-证券投资基金概述/01-证券投资基金简介/02-基金当事人.md
- source: 04-基金从业/02-科目二-证券投资基金/converted/sections/01-证券投资基金概述/01-证券投资基金简介.md

注意：排除以下文件：
- batch-task.md
- progress.md
- 任何以 "_" 开头的文件

返回格式必须是 JSON：
{
  "tasks": [
    {"fablePath": "...", "sourcePath": "...", "chapter": "...", "section": "...", "title": "..."}
  ],
  "totalCount": 123
}
`, { label: 'scan-fables' })

log(`Discovered ${scanResult.totalCount} fable files`)
log(`Chapters: ${[...new Set(scanResult.tasks.map(t => t.chapter))].join(', ')}`)
```

**验证:**

运行 Workflow 的 Scan phase 测试（使用 `Workflow` 工具或手动测试 `getSourcePath` 函数）。

**Step 2: Commit**

```bash
git add .claude/workflows/regenerate-fables.js
git commit -m "feat: implement scan phase for fable regenerator"
```

---

### Task 4: 实现 Generate Phase — 单文件 Subagent Prompt

**目标:** 构建 subagent 的详细 prompt，确保每个 subagent 能生成高质量的连续叙事风格 fable。

**Files:**
- Modify: `.claude/workflows/regenerate-fables.js`

**Step 1: 添加 Prompt 模板和 Generate Phase 框架**

在文件末尾添加：

```javascript
// ===== Prompt 构建函数 =====
function buildPrompt(task) {
  return `
你是一位金融寓言故事作家。请把以下教材内容变成生动的寓言故事。

${STYLE_GUIDE}

【风格参考——请先读取以下三个范例文件获取风格参考】
1. ${EXAMPLE_FILES[0]}
2. ${EXAMPLE_FILES[1]}
3. ${EXAMPLE_FILES[2]}

这三个范例的共同特点：
- 一个完整的故事从头讲到尾，没有分条目的小标题
- 有人物对话和互动
- 概念随着情节推进自然呈现
- 故事占全文 60% 以上

【源教材文件】
${task.sourcePath}

【你的任务】
1. 先读取上述三个范例文件，理解风格
2. 读取源教材文件 "${task.sourcePath}"
3. 在源教材中找到与 "${task.title}" 相关的内容（通常是某个一级或二级标题下的段落）
4. 构思一个完整的故事（开头→发展→高潮→结局），将概念自然融入情节
5. 故事要有具体人物，有对话，有情节转折
6. 故事长度控制在 600-1200 字
7. 故事讲完后，附上原文定义（引用教材原文）和对应点表格

【输出格式要求】
严格按照以下格式输出：

# <章节原始标题>

## <emoji> 寓言故事 —— 《<4-6字故事名>》

<完整的故事，连续叙事，禁止条目式结构>

---

**📖 原文定义**

> 直接引用教材原文的定义

**💡 对应点**

| 故事元素 | 概念对应 |
|---------|---------|
| ... | ... |

---

> 📝 来源：科目二 · <章> · <节> · ${task.title}

【自检清单】输出前请确认：
- [ ] 是否是一个完整的故事（开头→发展→高潮→结局），没有条目式结构？
- [ ] 是否有具体人物（有名有姓/有身份），有对话和互动？
- [ ] 概念是否自然融入情节中，而非故事后贴概念？
- [ ] 故事是否占全文 60% 以上？
- [ ] 故事长度是否在 600-1200 字之间？

请直接将生成的内容写入文件：${task.fablePath}
`.trim()
}

// ===== Generate Phase =====
phase('Generate')
log('Starting parallel generation...')
```

**验证:**

检查 `buildPrompt` 函数是否生成合理的 prompt 字符串：

```bash
cd /Users/sky/Documents/github/reading_notes
node -e "
const fs = require('fs');
const code = fs.readFileSync('.claude/workflows/regenerate-fables.js', 'utf8');
console.log('Has buildPrompt:', code.includes('function buildPrompt'));
console.log('Has STYLE_GUIDE ref:', code.includes('STYLE_GUIDE'));
console.log('Has EXAMPLE_FILES ref:', code.includes('EXAMPLE_FILES[0]'));
"
```

**Step 2: Commit**

```bash
git add .claude/workflows/regenerate-fables.js
git commit -m "feat: add subagent prompt template for fable generation"
```

---

### Task 5: 实现按章节分批并行生成

**目标:** 将任务按章节分组，每组并行 spawn subagent 处理。

**Files:**
- Modify: `.claude/workflows/regenerate-fables.js`

**Step 1: 添加分批并行逻辑**

在 `phase('Generate')` 之后添加：

```javascript
// 按章节分组
function groupByChapter(tasks) {
  const groups = {}
  for (const task of tasks) {
    if (!groups[task.chapter]) groups[task.chapter] = []
    groups[task.chapter].push(task)
  }
  return groups
}

// 分批并行生成
const chapterGroups = groupByChapter(scanResult.tasks)
const chapterNames = Object.keys(chapterGroups).sort()

for (const chapterName of chapterNames) {
  const tasks = chapterGroups[chapterName]
  log(`Processing chapter: ${chapterName} (${tasks.length} tasks)`)

  await parallel(
    tasks.map(task => () => {
      log(`  → ${task.fablePath}`)
      return agent(buildPrompt(task), {
        label: `gen:${task.title.slice(0, 20)}`,
        phase: 'Generate',
      })
    })
  )

  log(`✓ Chapter ${chapterName} complete`)
}

log('All chapters processed!')
```

**验证:**

检查代码是否包含关键逻辑：

```bash
cd /Users/sky/Documents/github/reading_notes
node -e "
const fs = require('fs');
const code = fs.readFileSync('.claude/workflows/regenerate-fables.js', 'utf8');
console.log('Has groupByChapter:', code.includes('function groupByChapter'));
console.log('Has parallel:', code.includes('await parallel'));
console.log('Has phase loop:', code.includes('for (const chapterName'));
"
```

**Step 2: Commit**

```bash
git add .claude/workflows/regenerate-fables.js
git commit -m "feat: implement chapter-based parallel batch generation"
```

---

### Task 6: 实现 Review Phase

**目标:** 每章完成后抽检质量，不合格则标记重跑。

**Files:**
- Modify: `.claude/workflows/regenerate-fables.js`

**Step 1: 添加 Review Phase**

在文件末尾添加：

```javascript
// ===== Review Phase =====
phase('Review')
log('Starting quality review...')

// 每章抽检 20%，最少 2 个
const SAMPLE_RATE = 0.2
const MIN_SAMPLES = 2

for (const chapterName of chapterNames) {
  const tasks = chapterGroups[chapterName]
  const sampleSize = Math.max(MIN_SAMPLES, Math.ceil(tasks.length * SAMPLE_RATE))

  // 随机抽样
  const shuffled = [...tasks].sort(() => Math.random() - 0.5)
  const samples = shuffled.slice(0, sampleSize)

  log(`Reviewing ${chapterName}: ${sampleSize} samples`)

  const reviews = await parallel(
    samples.map(task => () => agent(`
请读取文件 "${task.fablePath}"，检查是否符合以下质量标准：

1. 是否是一个完整的故事（开头→发展→高潮→结局），没有条目式结构？
2. 是否有具体人物（有名有姓/有身份），有对话和互动？
3. 概念是否自然融入情节中，而非故事后贴概念？
4. 故事是否占全文 60% 以上？
5. 故事长度是否在 600-1200 字之间？

返回 JSON 格式：
{
  "fablePath": "${task.fablePath}",
  "passed": true/false,
  "issues": ["问题描述1", "问题描述2"]
}
    `.trim(), {
      label: `review:${task.title.slice(0, 20)}`,
      phase: 'Review',
      schema: {
        type: 'object',
        properties: {
          fablePath: { type: 'string' },
          passed: { type: 'boolean' },
          issues: { type: 'array', items: { type: 'string' } },
        },
        required: ['fablePath', 'passed', 'issues'],
      },
    }))
  )

  const failed = reviews.filter(r => !r.passed)
  const passRate = ((reviews.length - failed.length) / reviews.length * 100).toFixed(1)

  log(`  ${chapterName}: ${passRate}% passed (${failed.length}/${reviews.length} failed)`)

  if (failed.length > 0) {
    log(`  ⚠️ Failed samples: ${failed.map(f => f.fablePath).join(', ')}`)
    log(`  ⚠️ Issues: ${failed.flatMap(f => f.issues).join('; ')}`)
  }
}

log('Review complete!')
```

**验证:**

```bash
cd /Users/sky/Documents/github/reading_notes
node -e "
const fs = require('fs');
const code = fs.readFileSync('.claude/workflows/regenerate-fables.js', 'utf8');
console.log('Has Review phase:', code.includes(\"phase('Review')\"));
console.log('Has SAMPLE_RATE:', code.includes('SAMPLE_RATE'));
console.log('Has schema:', code.includes('schema:'));
"
```

**Step 2: Commit**

```bash
git add .claude/workflows/regenerate-fables.js
git commit -m "feat: add review phase with sampling and quality checks"
```

---

### Task 7: 运行试点 — 第一章（~15 个文件）

**目标:** 运行 Workflow 处理第一章，验证输出质量。

**Files:**
- 无文件修改

**Step 1: 运行 Workflow**

使用 Claude Code 的 Workflow 工具运行脚本，但只处理第一章：

临时修改脚本，添加过滤条件只处理第一章：

```javascript
// 在 groupByChapter 之后添加过滤
const chapterNames = Object.keys(chapterGroups).sort()
const pilotChapter = chapterNames[0] // 只跑第一章
log(`Pilot mode: only processing ${pilotChapter}`)
```

运行：
```bash
cd /Users/sky/Documents/github/reading_notes
# 在 Claude Code 中使用 Workflow 工具运行 regenerate-fables.js
```

**Step 2: 人工检查输出**

随机打开 3-5 个生成的 fable 文件，检查：
- 是否是一个完整的故事？
- 是否有具体人物和对话？
- 概念是否自然融入情节？
- 是否有条目式结构？

```bash
ls "04-基金从业/02-科目二-证券投资基金/converted/fables/01-证券投资基金概述/01-证券投资基金简介/"
# 打开几个文件检查
```

**Step 3: 记录反馈**

将检查结果记录到 `docs/plans/fable-pilot-feedback.md`：
- 哪些质量OK
- 哪些需要调整
- prompt 是否需要修改

---

### Task 8: 根据试点反馈调整 Prompt

**目标:** 根据第一章的生成效果，微调 prompt 和风格指南。

**Files:**
- Modify: `.claude/workflows/regenerate-fables.js`（如果需要）

**Step 1: 分析反馈**

读取试点反馈文件，确定需要调整的地方。

**Step 2: 调整 Prompt**

常见需要调整的点：
- 故事长度（太长/太短）
- 人物对话太少
- 概念融入不自然
- 仍有模板化结构残留

在 `STYLE_GUIDE` 或 `buildPrompt` 中做出相应调整。

**Step 3: Commit**

```bash
git add .claude/workflows/regenerate-fables.js
git commit -m "refine: adjust prompt based on pilot feedback"
```

---

### Task 9: 运行全部章节

**目标:** 移除试点过滤，运行完整 Workflow 处理全部 18 章。

**Files:**
- 修改: `.claude/workflows/regenerate-fables.js`（移除 pilot 过滤）

**Step 1: 移除试点过滤**

删除或注释掉试点过滤代码：

```javascript
// 删除这一行:
// const pilotChapter = chapterNames[0]
// 恢复为处理全部章节
```

**Step 2: 运行完整 Workflow**

使用 Claude Code 的 Workflow 工具运行完整脚本。

预期时间：每章 5-15 分钟（取决于并行度和文件数），总计约 2-4 小时。

**Step 3: 监控进度**

Workflow 会自动输出每章的完成状态。如有失败，记录到日志中。

---

### Task 10: 最终验证和清理

**目标:** 确认全部生成完成，质量合格，清理备份。

**Files:**
- 可能删除: `fables.backup.20260611/`

**Step 1: 统计生成结果**

```bash
cd /Users/sky/Documents/github/reading_notes
echo "=== Fable 文件统计 ==="
find "04-基金从业/02-科目二-证券投资基金/converted/fables" -name '*.md' \
  ! -name 'batch-task.md' ! -name 'progress.md' | wc -l

echo "=== 按章节统计 ==="
for dir in "04-基金从业/02-科目二-证券投资基金/converted/fables"/0*-*/; do
  count=$(find "$dir" -name '*.md' | wc -l)
  echo "$(basename "$dir"): $count files"
done
```

**Step 2: 随机抽检**

随机抽取 10 个文件人工检查：

```bash
find "04-基金从业/02-科目二-证券投资基金/converted/fables" -name '*.md' \
  ! -name 'batch-task.md' ! -name 'progress.md' | shuf | head -10
```

**Step 3: 更新进度文档**

更新 `batch-task.md` 和 `progress.md`，标记全部完成。

**Step 4: Commit 最终版本**

```bash
git add -A
git commit -m "regenerate: all fables with high-quality continuous narrative style

- 全部 $(find '04-基金从业/02-科目二-证券投资基金/converted/fables' -name '*.md' ! -name 'batch-task.md' ! -name 'progress.md' | wc -l) 个寓言故事重新生成
- 统一为连续叙事风格（参照《老陈的陶罐》）
- 每个故事有完整情节、具体人物、概念融入叙事
- 使用 Workflow 并行 subagent 生成"
```

**Step 5: 清理备份（确认无误后）**

```bash
rm -rf "04-基金从业/02-科目二-证券投资基金/converted/fables.backup.20260611"
git add -A
git commit -m "chore: remove fables backup after successful regeneration"
```

---

## 执行前检查清单

- [ ] 备份已创建（Task 1）
- [ ] Workflow 脚本完整（Tasks 2-6）
- [ ] 试点运行成功，质量达标（Task 7）
- [ ] Prompt 已根据反馈调整（Task 8）
- [ ] 准备运行完整 Workflow（Task 9）
- [ ] 有足够的时间（预计 2-4 小时）
