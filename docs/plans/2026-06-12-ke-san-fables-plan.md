# 科目三寓言故事批量生成 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 写一个 Claude Code Workflow 脚本，自动为 科目三（股权投资基金基础知识）全部 34 个 section 生成寓言故事 fable，支持自动拆分概念、并行生成、质量抽检和 git 版本控制。

**Architecture:** 使用 Claude Code Workflow 工具，按 Scan → Plan → Generate → Review 四阶段执行。Scan 遍历 section 目录；Plan 由 subagent 按“每 fable 最多 3 个概念”自动拆分任务；Generate 由 subagent 读取原文和风格范例生成故事并写入文件；Review 每章抽检 20% 并触发重跑。全程用 git commit 做快照。

**Tech Stack:** Claude Code Workflow (JavaScript), Agent/Read/Write/Bash 工具，git 版本控制。

---

## 项目上下文

- **仓库根目录**: `/Users/sky/Documents/github/reading_notes`
- **源文件目录**: `04-基金从业/03-科目三-私募股权/converted/sections/<章>/<节>.md`
- **Fable 输出目录**: `04-基金从业/03-科目三-私募股权/converted/fables/<章>/<节>/<序号>-<标题>.md`
- **风格范例目录**: `04-基金从业/03-科目三-私募股权/converted/fables/01-股权投资基金概述 …/`
- **设计文档**: `docs/plans/2026-06-12-ke-san-fables-design.md`
- **进度文件**: `04-基金从业/03-科目三-私募股权/converted/fables/batch-task.md`

---

### Task 1: 创建 Workflow 脚本框架

**目标:** 创建 `.claude/workflows/generate-ke-san-fables.js` 的基本结构。

**Files:**
- Create: `.claude/workflows/generate-ke-san-fables.js`

**Step 1: 写入框架代码**

```javascript
export const meta = {
  name: 'generate-ke-san-fables',
  description: 'Generate all 科目三 fables with automatic concept splitting and quality review',
  phases: [
    { title: 'Scan', detail: 'Discover all section markdown files' },
    { title: 'Plan', detail: 'Split each section into 1-3 fable tasks' },
    { title: 'Generate', detail: 'Parallel subagent generation per fable task' },
    { title: 'Review', detail: 'Sample and verify output quality per chapter' },
  ],
}

// ===== 路径常量 =====
const REPO_ROOT = '/Users/sky/Documents/github/reading_notes'
const PROGRAM_BASE = '04-基金从业/03-科目三-私募股权'
const SECTIONS_BASE = `${PROGRAM_BASE}/converted/sections`
const FABLES_BASE = `${PROGRAM_BASE}/converted/fables`
const DESIGN_DOC = 'docs/plans/2026-06-12-ke-san-fables-design.md'

// ===== 风格范例文件路径 =====
const EXAMPLE_FILES = [
  `${FABLES_BASE}/01-股权投资基金概述 …/01-股权投资基金的概念和特点/01-股权投资基金的概念和特点.md`,
  `${FABLES_BASE}/01-股权投资基金概述 …/03-股权投资基金市场参与主体/01-股权投资基金市场参与主体.md`,
  `${FABLES_BASE}/01-股权投资基金概述 …/04-股权投资基金的起源和发展/01-股权投资基金的起源和发展.md`,
  `${FABLES_BASE}/01-股权投资基金概述 …/05-股权投资基金对经济高质量发展的作用/01-股权投资基金对经济高质量发展的作用.md`,
]

// ===== 风格指南 =====
const STYLE_GUIDE = `
你是金融寓言故事作家。请把枯燥的金融教材概念，变成生动的、有情节的寓言故事。

【硬性规则——违反任意一条即为不合格】
1. 一个完整的故事：必须有开头、发展、高潮、结局，禁止条目式结构。
2. 必须有具体人物：人物要有名字或具体身份，有对话和互动。
3. 概念融入情节：概念必须自然融入故事事件中，不能在故事讲完后再贴概念。
4. 故事占全文 60% 以上。
5. 故事长度 600-1200 字。
6. 一个 fable 最多讲 3 个核心概念，宁多勿挤。

【输出格式】
# <原节标题>

## <emoji> 寓言故事 —— 《<4-6字故事名>》

<完整故事，连续叙事>

---

**📖 原文定义**

> 直接引用教材原文的定义

**💡 对应点**

| 故事元素 | 概念对应 |
|---------|---------|
| ... | ... |

---

> 📝 来源：科目三 · <章> · <节> · <标题>
`.trim()

// ===== 工具函数 =====
function absolutePath(relativePath) {
  return `${REPO_ROOT}/${relativePath}`
}
```

**Step 2: 验证文件创建成功**

```bash
cd /Users/sky/Documents/github/reading_notes
node -e "
const fs = require('fs');
const code = fs.readFileSync('.claude/workflows/generate-ke-san-fables.js', 'utf8');
console.log('File size:', code.length, 'chars');
console.log('Has meta:', code.includes('export const meta'));
console.log('Has STYLE_GUIDE:', code.includes('STYLE_GUIDE'));
console.log('Has EXAMPLE_FILES:', code.includes('EXAMPLE_FILES'));
"
```

Expected: `File size:` > 1000, 其他三行均为 `true`。

**Step 3: Commit**

```bash
cd /Users/sky/Documents/github/reading_notes
git add .claude/workflows/generate-ke-san-fables.js
git commit -m "feat: create 科目三 fable generator workflow framework

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: 实现 Scan Phase

**目标:** 遍历 section 目录，构建任务列表（每节一个 task，记录路径、章、节、标题）。

**Files:**
- Modify: `.claude/workflows/generate-ke-san-fables.js`

**Step 1: 在脚本末尾添加 Scan Phase**

```javascript
// ===== Scan Phase =====
phase('Scan')
log('Scanning section files...')

const scanResult = await agent(`
请扫描目录 "${absolutePath(SECTIONS_BASE)}" 下的所有 .md 文件（递归）。

要求：
1. 排除任何名为 "00_index.md" 的文件；
2. 对每个 .md 文件，记录：
   - sectionPath: 从 repo root 开始的相对路径
   - chapter: 路径中 sections 后面的第一级目录名
   - section: 文件名去掉 .md
   - title: 文件内容中第一个 # 标题的文本

返回 JSON：
{
  "tasks": [
    {"sectionPath": "...", "chapter": "...", "section": "...", "title": "..."}
  ],
  "totalCount": 34
}
`, { label: 'scan-sections' })

log(`Discovered ${scanResult.totalCount} section files`)
log(`Chapters: ${[...new Set(scanResult.tasks.map(t => t.chapter))].join(', ')}`)
```

**Step 2: 验证 Scan Phase**

运行 Workflow 的 Scan phase 测试：

```bash
cd /Users/sky/Documents/github/reading_notes
# 在 Claude Code 中使用 Workflow 工具运行 generate-ke-san-fables.js
# 观察日志是否显示 "Discovered 34 section files" 和 9 个 chapter 名称
```

Expected: 日志显示 34 个 section 文件，9 个 chapter 名称。

**Step 3: Commit**

```bash
cd /Users/sky/Documents/github/reading_notes
git add .claude/workflows/generate-ke-san-fables.js
git commit -m "feat: implement scan phase for 科目三 fable generator

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: 实现 Plan Phase

**目标:** 每节 spawn 一个 subagent，自动拆分为 1-3 个 fable 任务，每个任务聚焦 1-3 个概念。

**Files:**
- Modify: `.claude/workflows/generate-ke-san-fables.js`

**Step 1: 添加 Plan Phase 框架**

```javascript
// ===== Plan Phase =====
phase('Plan')
log('Planning fable tasks for each section...')

function buildPlanPrompt(task) {
  return `
你是一名教材内容分析助手。请阅读下面这节教材，判断需要拆成几个 fable。

规则：
- 一节最多拆成 3 个 fable；
- 每个 fable 聚焦 1-3 个核心概念；
- 优先按“自然段落/子标题”拆分；
- 不要为了拆而拆，概念少的节就 1 个 fable。

【教材文件】${task.sectionPath}

请先读取该文件，然后返回 JSON：
[
  {
    "conceptFocus": "这个 fable 要讲的核心概念（一句话）",
    "title": "用于文件名和标题的概念名（4-10字）",
    "filename": "01-标题.md"
  }
]

注意：
- filename 必须使用 "01-", "02-", "03-" 这样的序号前缀；
- ConceptFocus 要具体，让下一个写故事的 subagent 知道重点写什么。
`.trim()
}
```

**Step 2: 添加按章分批 Plan 逻辑**

```javascript
function groupByChapter(tasks) {
  const groups = {}
  for (const task of tasks) {
    if (!groups[task.chapter]) groups[task.chapter] = []
    groups[task.chapter].push(task)
  }
  return groups
}

const chapterGroups = groupByChapter(scanResult.tasks)
const chapterNames = Object.keys(chapterGroups).sort()

const allFableTasks = []

for (const chapterName of chapterNames) {
  const tasks = chapterGroups[chapterName]
  log(`Planning chapter: ${chapterName} (${tasks.length} sections)`)

  const plans = await parallel(
    tasks.map(task => () => agent(buildPlanPrompt(task), {
      label: `plan:${task.section.slice(0, 20)}`,
      phase: 'Plan',
      schema: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            conceptFocus: { type: 'string' },
            title: { type: 'string' },
            filename: { type: 'string' },
          },
          required: ['conceptFocus', 'title', 'filename'],
        },
      },
    }))
  )

  for (let i = 0; i < tasks.length; i++) {
    const task = tasks[i]
    const plan = plans[i]
    if (!plan || !Array.isArray(plan)) {
      log(`⚠️ Failed to plan ${task.sectionPath}`)
      continue
    }
    for (const item of plan) {
      const fableDir = `${FABLES_BASE}/${task.chapter}/${task.section}`
      allFableTasks.push({
        sectionPath: task.sectionPath,
        chapter: task.chapter,
        section: task.section,
        sectionTitle: task.title,
        conceptFocus: item.conceptFocus,
        title: item.title,
        fablePath: `${fableDir}/${item.filename}`,
      })
    }
  }

  log(`✓ Chapter ${chapterName} planned: ${allFableTasks.filter(t => t.chapter === chapterName).length} fable tasks`)
}

log(`Total fable tasks: ${allFableTasks.length}`)
```

**Step 3: 验证 Plan Phase**

```bash
cd /Users/sky/Documents/github/reading_notes
node -e "
const fs = require('fs');
const code = fs.readFileSync('.claude/workflows/generate-ke-san-fables.js', 'utf8');
console.log('Has Plan phase:', code.includes(\"phase('Plan')\"));
console.log('Has buildPlanPrompt:', code.includes('function buildPlanPrompt'));
console.log('Has schema:', code.includes('schema:'));
"
```

Expected: 全部返回 `true`。

**Step 4: Commit**

```bash
cd /Users/sky/Documents/github/reading_notes
git add .claude/workflows/generate-ke-san-fables.js
git commit -m "feat: implement plan phase with automatic concept splitting

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: 实现 Generate Phase

**目标:** 每个 fable task 由一个 subagent 生成故事并写入文件。

**Files:**
- Modify: `.claude/workflows/generate-ke-san-fables.js`

**Step 1: 添加 Generate Prompt 和 Phase**

```javascript
function buildGeneratePrompt(task) {
  return `
你是一位金融寓言故事作家。请把以下教材内容变成生动的寓言故事。

${STYLE_GUIDE}

【风格参考——请先读取以下 4 个范例文件，学习叙事风格】
1. ${EXAMPLE_FILES[0]}
2. ${EXAMPLE_FILES[1]}
3. ${EXAMPLE_FILES[2]}
4. ${EXAMPLE_FILES[3]}

【源教材文件】${task.sectionPath}
【本节标题】${task.sectionTitle}
【本 fable 聚焦概念】${task.conceptFocus}
【本 fable 标题】${task.title}

【你的任务】
1. 先读取上述 4 个范例文件，理解风格；
2. 读取源教材文件 "${task.sectionPath}"；
3. 找到与 "${task.conceptFocus}" 相关的内容；
4. 构思一个完整的故事（开头→发展→高潮→结局），将概念自然融入情节；
5. 故事要有具体人物、对话、情节转折；
6. 故事长度 600-1200 字；
7. 故事讲完后，附上原文定义和对应点表格；
8. 将生成的内容直接写入文件：${task.fablePath}

【自检清单】输出前请确认：
- [ ] 是否是一个完整的故事，没有条目式结构？
- [ ] 是否有具体人物，有对话和互动？
- [ ] 概念是否自然融入情节中？
- [ ] 故事是否占全文 60% 以上？
- [ ] 故事长度是否在 600-1200 字之间？
- [ ] 是否只聚焦了 1-3 个核心概念？
`.trim()
}

// ===== Generate Phase =====
phase('Generate')
log('Starting parallel generation...')

function groupFableTasksByChapter(tasks) {
  const groups = {}
  for (const task of tasks) {
    if (!groups[task.chapter]) groups[task.chapter] = []
    groups[task.chapter].push(task)
  }
  return groups
}

const fableChapterGroups = groupFableTasksByChapter(allFableTasks)
const fableChapterNames = Object.keys(fableChapterGroups).sort()

for (const chapterName of fableChapterNames) {
  const tasks = fableChapterGroups[chapterName]
  log(`Generating chapter: ${chapterName} (${tasks.length} fables)`)

  await parallel(
    tasks.map(task => () => agent(buildGeneratePrompt(task), {
      label: `gen:${task.title.slice(0, 20)}`,
      phase: 'Generate',
    }))
  )

  log(`✓ Chapter ${chapterName} generated`)
}

log('All chapters generated!')
```

**Step 2: 验证 Generate Phase**

```bash
cd /Users/sky/Documents/github/reading_notes
node -e "
const fs = require('fs');
const code = fs.readFileSync('.claude/workflows/generate-ke-san-fables.js', 'utf8');
console.log('Has Generate phase:', code.includes(\"phase('Generate')\"));
console.log('Has buildGeneratePrompt:', code.includes('function buildGeneratePrompt'));
console.log('Has parallel generation:', code.includes('await parallel'));
"
```

Expected: 全部返回 `true`。

**Step 3: Commit**

```bash
cd /Users/sky/Documents/github/reading_notes
git add .claude/workflows/generate-ke-san-fables.js
git commit -m "feat: implement generate phase with parallel subagents

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: 实现 Review Phase

**目标:** 每章完成后抽检 20%（最少 2 个），不合格重跑。

**Files:**
- Modify: `.claude/workflows/generate-ke-san-fables.js`

**Step 1: 添加 Review Phase**

```javascript
// ===== Review Phase =====
phase('Review')
log('Starting quality review...')

const SAMPLE_RATE = 0.2
const MIN_SAMPLES = 2
const PASS_THRESHOLD = 70

for (const chapterName of fableChapterNames) {
  const tasks = fableChapterGroups[chapterName]
  const sampleSize = Math.max(MIN_SAMPLES, Math.ceil(tasks.length * SAMPLE_RATE))

  // 简单伪随机抽样（按索引取，避免 Workflow 中无 Math.random）
  const samples = tasks.filter((_, idx) => idx % Math.ceil(tasks.length / sampleSize) === 0).slice(0, sampleSize)

  log(`Reviewing ${chapterName}: ${samples.length} samples`)

  const reviews = await parallel(
    samples.map(task => () => agent(`
请读取文件 "${task.fablePath}"，按以下标准评分（满分 100）：

1. 故事完整性（20分）：是否有开头→发展→高潮→结局，没有条目式结构？
2. 人物对话（20分）：是否有具体人物、对话和互动？
3. 概念融入（30分）：概念是否自然融入情节，而非故事后贴概念？
4. 格式规范（20分）：是否有原文定义、对应点表格、来源标注？
5. 长度适中（10分）：故事是否在 600-1200 字之间？

返回 JSON：
{
  "fablePath": "${task.fablePath}",
  "score": 85,
  "passed": true,
  "issues": ["问题描述1"]
}
    `.trim(), {
      label: `review:${task.title.slice(0, 20)}`,
      phase: 'Review',
      schema: {
        type: 'object',
        properties: {
          fablePath: { type: 'string' },
          score: { type: 'number' },
          passed: { type: 'boolean' },
          issues: { type: 'array', items: { type: 'string' } },
        },
        required: ['fablePath', 'score', 'passed', 'issues'],
      },
    }))
  )

  const failed = reviews.filter(r => !r.passed || r.score < PASS_THRESHOLD)
  const passRate = ((reviews.length - failed.length) / reviews.length * 100).toFixed(1)

  log(`  ${chapterName}: ${passRate}% passed (${failed.length}/${reviews.length} failed)`)

  if (failed.length > 0) {
    log(`  ⚠️ Failed samples: ${failed.map(f => f.fablePath).join(', ')}`)
    log(`  ⚠️ Issues: ${failed.flatMap(f => f.issues).join('; ')}`)
  }
}

log('Review complete!')
```

**Step 2: 验证 Review Phase**

```bash
cd /Users/sky/Documents/github/reading_notes
node -e "
const fs = require('fs');
const code = fs.readFileSync('.claude/workflows/generate-ke-san-fables.js', 'utf8');
console.log('Has Review phase:', code.includes(\"phase('Review')\"));
console.log('Has SAMPLE_RATE:', code.includes('SAMPLE_RATE'));
console.log('Has PASS_THRESHOLD:', code.includes('PASS_THRESHOLD'));
"
```

Expected: 全部返回 `true`。

**Step 3: Commit**

```bash
cd /Users/sky/Documents/github/reading_notes
git add .claude/workflows/generate-ke-san-fables.js
git commit -m "feat: add review phase with sampling and quality scoring

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: 添加 Git Commit 集成

**目标:** 每章生成并抽检通过后自动 commit，实现版本控制。

**Files:**
- Modify: `.claude/workflows/generate-ke-san-fables.js`

**Step 1: 添加 git commit helper**

```javascript
// ===== Git helper =====
async function commitChapter(chapterName) {
  const msg = `feat: generate fables for 科目三 ${chapterName}

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`

  await bash(`cd "${REPO_ROOT}" && git add "${FABLES_BASE}" && git commit -m "${msg}"`, {
    description: `Commit fables for ${chapterName}`,
  })
}
```

**Step 2: 在 Generate Phase 每章结束后调用 commit**

修改 Generate Phase 循环，在 `log(`✓ Chapter ${chapterName} generated`)` 之后添加：

```javascript
  log(`✓ Chapter ${chapterName} generated`)
  await commitChapter(chapterName)
  log(`✓ Chapter ${chapterName} committed`)
```

**Step 3: 验证**

```bash
cd /Users/sky/Documents/github/reading_notes
node -e "
const fs = require('fs');
const code = fs.readFileSync('.claude/workflows/generate-ke-san-fables.js', 'utf8');
console.log('Has commitChapter:', code.includes('function commitChapter'));
console.log('Has bash call:', code.includes('await bash'));
"
```

Expected: 全部返回 `true`。

**Step 4: Commit**

```bash
cd /Users/sky/Documents/github/reading_notes
git add .claude/workflows/generate-ke-san-fables.js
git commit -m "feat: add per-chapter git commit integration

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: 添加 batch-task.md 进度追踪

**目标:** 创建并更新进度文件，记录每章状态和失败任务。

**Files:**
- Modify: `.claude/workflows/generate-ke-san-fables.js`
- Create: `04-基金从业/03-科目三-私募股权/converted/fables/batch-task.md`

**Step 1: 添加进度追踪 helper**

```javascript
// ===== Progress tracking =====
const PROGRESS_FILE = `${FABLES_BASE}/batch-task.md`

async function writeProgress(statusMap, failedTasks = []) {
  const lines = [
    '# 科目三 Fable 生成进度',
    '',
    `生成时间：${new Date().toISOString()}`,
    '',
    '## 章节状态',
    '',
    ...Array.from(statusMap.entries()).map(([chapter, status]) => `- ${chapter}: ${status}`),
    '',
    '## 失败任务',
    '',
    ...(failedTasks.length === 0 ? ['无'] : failedTasks.map(t => `- ${t.fablePath}: ${t.reason}`)),
    '',
  ]

  await writeFile(absolutePath(PROGRESS_FILE), lines.join('\n'))
}
```

**Step 2: 在 Workflow 各阶段更新进度**

- Scan 完成后初始化 `statusMap`，所有章节为 `pending`；
- Plan 开始前更新为 `planning`；
- Generate 开始前更新为 `generating`；
- Review 期间更新为 `reviewing`；
- Review 通过后更新为 `done`。

**Step 3: 验证**

```bash
cd /Users/sky/Documents/github/reading_notes
node -e "
const fs = require('fs');
const code = fs.readFileSync('.claude/workflows/generate-ke-san-fables.js', 'utf8');
console.log('Has PROGRESS_FILE:', code.includes('PROGRESS_FILE'));
console.log('Has writeProgress:', code.includes('function writeProgress'));
"
```

Expected: 全部返回 `true`。

**Step 4: Commit**

```bash
cd /Users/sky/Documents/github/reading_notes
git add .claude/workflows/generate-ke-san-fables.js
git commit -m "feat: add batch-task.md progress tracking

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 8: 试点运行 —— 第二章

**目标:** 先用第二章验证 Workflow 端到端是否正常工作。

**Files:**
- Modify: `.claude/workflows/generate-ke-san-fables.js`（临时过滤）

**Step 1: 临时添加 pilot 过滤**

在 Generate Phase 前临时添加：

```javascript
// Pilot mode: only process chapter 2
const pilotChapter = '02-股权投资基金管理人 …'
log(`Pilot mode: only processing ${pilotChapter}`)
const pilotTasks = allFableTasks.filter(t => t.chapter === pilotChapter)
// 临时替换后续循环使用 pilotTasks
```

**Step 2: 运行 Workflow**

在 Claude Code 中使用 Workflow 工具运行 `.claude/workflows/generate-ke-san-fables.js`。

**Step 3: 检查输出**

```bash
cd /Users/sky/Documents/github/reading_notes
find "04-基金从业/03-科目三-私募股权/converted/fables/02-股权投资基金管理人 …" -type f -name "*.md" | sort
```

Expected: 第二章目录下出现 1-3 个 fable 文件。

**Step 4: 人工抽检**

随机打开 2 个生成的 fable 文件，检查：
- 是否有完整故事？
- 是否有具体人物和对话？
- 概念是否自然融入？
- 是否有原文定义和对应点表格？

**Step 5: 移除 pilot 过滤并 commit**

```bash
cd /Users/sky/Documents/github/reading_notes
git add .claude/workflows/generate-ke-san-fables.js
git commit -m "refine: pilot chapter 2 passed, remove pilot filter

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 9: 运行全部章节

**目标:** 移除 pilot 过滤，运行完整 Workflow 处理全部 9 章。

**Files:**
- 无文件修改（已在 Task 8 移除过滤）

**Step 1: 运行完整 Workflow**

在 Claude Code 中使用 Workflow 工具运行 `.claude/workflows/generate-ke-san-fables.js`。

**Step 2: 监控进度**

观察 Workflow 日志，确认每章状态从 pending → planning → generating → reviewing → done。

**Step 3: 检查 git 历史**

```bash
cd /Users/sky/Documents/github/reading_notes
git log --oneline -15
```

Expected: 看到每章生成后的 commit 记录。

---

### Task 10: 最终验证

**目标:** 确认全部生成完成，统计文件数量，人工抽检。

**Files:**
- 可能修改：根据抽检结果重跑个别 fable

**Step 1: 统计生成结果**

```bash
cd /Users/sky/Documents/github/reading_notes
echo "=== Fable 文件统计 ==="
find "04-基金从业/03-科目三-私募股权/converted/fables" -name '*.md' ! -name 'batch-task.md' ! -name 'progress.md' | wc -l

echo "=== 按章节统计 ==="
for dir in "04-基金从业/03-科目三-私募股权/converted/fables"/0*-*/; do
  count=$(find "$dir" -name '*.md' | wc -l)
  echo "$(basename "$dir"): $count files"
done
```

Expected: 总数 ≥ 34（预计 40-50），每章有对应文件。

**Step 2: 随机抽检**

```bash
cd /Users/sky/Documents/github/reading_notes
find "04-基金从业/03-科目三-私募股权/converted/fables" -name '*.md' ! -name 'batch-task.md' ! -name 'progress.md' | sort -R | head -5
```

打开这些文件，检查故事质量。

**Step 3: 最终 commit**

```bash
cd /Users/sky/Documents/github/reading_notes
git add -A
git commit -m "feat: complete 科目三 fable generation

- 全部章节寓言故事生成完毕
- 使用 Workflow 自动拆分概念、并行生成、质量抽检
- 每章通过 git commit 保存快照

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```

---

## 执行前检查清单

- [ ] Workflow 脚本框架完成（Task 1）
- [ ] Scan Phase 能发现 34 个 section（Task 2）
- [ ] Plan Phase 能正确拆分概念（Task 3）
- [ ] Generate Phase 能并行生成故事（Task 4）
- [ ] Review Phase 能抽检评分（Task 5）
- [ ] Git commit 集成正常（Task 6）
- [ ] batch-task.md 进度追踪正常（Task 7）
- [ ] 第二章试点通过（Task 8）
- [ ] 完整 Workflow 运行完成（Task 9）
- [ ] 最终验证通过（Task 10）
