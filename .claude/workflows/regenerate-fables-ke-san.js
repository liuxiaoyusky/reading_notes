export const meta = {
  name: 'regenerate-fables-ke-san',
  description: 'Regenerate all 科目三 fables with high-quality continuous narrative storytelling',
  phases: [
    { title: 'Scan', detail: 'Discover all section files and build task list' },
    { title: 'Generate', detail: 'Parallel subagent generation per chapter' },
    { title: 'Review', detail: 'Sample and verify output quality' },
  ],
}

// ===== 路径常量 =====
const REPO_ROOT = '/Users/sky/Documents/github/reading_notes'
const FABLES_BASE = '04-基金从业/03-科目三-私募股权/converted/fables'
const SECTIONS_BASE = '04-基金从业/03-科目三-私募股权/converted/sections'

// 范例文件路径（先生成 golden sample 后再更新）
const EXAMPLE_FILES = [
  '04-基金从业/03-科目三-私募股权/converted/fables/01-股权投资基金概述 …/01-股权投资基金的概念和特点/01-股权投资基金的概念和特点.md',
  '04-基金从业/03-科目三-私募股权/converted/fables/03-股权投资基金产品 …/03-创业投资基金与并购基金/03-创业投资基金与并购基金.md',
  '04-基金从业/03-科目三-私募股权/converted/fables/05-股权投资基金的投资 …/05-投资交易结构/05-投资交易结构.md',
]

// ===== 风格指南 =====
const STYLE_GUIDE = `
你是金融寓言故事作家。你的任务是把枯燥的金融教材概念，变成生动的、有情节的寓言故事，帮助考生通过故事记忆概念。

【硬性规则——违反任意一条即为不合格】

1. **一个完整的故事**：必须有开头、发展、高潮、结局的完整叙事弧线。禁止条目式结构（如"第一个角色...第二个角色..."、"### 第一点...第二点..."）。故事必须从头到尾连续讲述，像一篇短文。

2. **必须有具体人物**：人物要有名字或具体身份，有对话和互动。
   ✓ 好："投资人老周对创业者阿福说：'我出五百万，占你三成股份...'"
   ✗ 差："投资者将资金交给管理人..."

3. **概念融入情节**：概念必须自然融入故事事件中，读者看完故事就懂了。不能在故事讲完后再贴概念解释。
   ✓ 好：老周看中了阿福的 bakery 项目，签协议、投钱、派人监管 → 自然引出股权投资流程
   ✗ 差：先讲"股权投资是购买非上市公司股权"，再补一句"就像老周投资阿福一样"

4. **叙事优先**：故事占全文 60% 以上。先有故事，后有原文定义和对应点表格。

5. **故事长度**：600-1200 字。太短讲不清，太长记不住。

6. **股权场景偏好**：用创业投资、合伙企业、项目孵化、退出转让等生活/商业场景来演示概念。人物可以是创业者、投资人、合伙人、基金管家等。

7. **专业术语准确**：故事对应点里的术语必须与教材原文一致，不能杜撰。
`.trim()

// ===== 从 section 路径推断 fable 输出路径 =====
function getFablePath(sectionPath, title, index) {
  const parts = sectionPath.split('/')
  const sectionsIdx = parts.indexOf('sections')
  const chapter = parts[sectionsIdx + 1]
  const sectionFile = parts[sectionsIdx + 2]
  const section = sectionFile.replace(/\.md$/, '')
  const baseParts = parts.slice(0, sectionsIdx)
  const seq = String(index).padStart(2, '0')
  return [...baseParts, 'fables', chapter, section, `${seq}-${title}.md`].join('/')
}

// ===== 提取 md 文件中的一级/二级标题 =====
function getHeadings(content) {
  const lines = content.split('\n')
  const headings = []
  for (const line of lines) {
    const match = line.match(/^(#{1,2})\s+(.+)$/)
    if (match) {
      headings.push({ level: match[1].length, title: match[2].trim() })
    }
  }
  return headings
}

// ===== Prompt 构建函数 =====
function buildPrompt(task) {
  return `
你是一位金融寓言故事作家。请把以下教材内容变成生动的寓言故事。

${STYLE_GUIDE}

【风格参考——请先读取以下三个范例文件获取风格参考】
1. ${EXAMPLE_FILES[0]}
2. ${EXAMPLE_FILES[1]}
3. ${EXAMPLE_FILES[2]}

如果范例文件不存在，请先跳过读取范例，直接按风格指南生成。

【源教材文件】
${task.sourcePath}

【目标概念】
${task.title}

【你的任务】
1. 读取源教材文件 "${task.sourcePath}"
2. 找到与 "${task.title}" 相关的内容
3. 先读取三个范例文件（如果存在），理解连续叙事风格
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

> 📝 来源：科目三 · <章> · <节> · ${task.title}

【自检清单】输出前请确认：
- [ ] 是否是一个完整的故事（开头→发展→高潮→结局），没有条目式结构？
- [ ] 是否有具体人物（有名有姓/有身份），有对话和互动？
- [ ] 概念是否自然融入情节中，而非故事后贴概念？
- [ ] 故事是否占全文 60% 以上？
- [ ] 故事长度是否在 600-1200 字之间？

请直接将生成的内容写入文件：${task.fablePath}
`.trim()
}

// ===== Scan Phase =====
phase('Scan')
log('Scanning 科目三 section files...')

const scanResult = await agent(`
请扫描目录 "${REPO_ROOT}/${SECTIONS_BASE}" 下的所有 .md 文件（递归），构建任务列表。

对于每个 .md 文件：
1. 读取文件内容
2. 提取所有一级标题（#）和二级标题（##）
3. 每个标题生成一个 fable 任务

对于每个任务，记录：
1. sourcePath: 源文件的完整相对路径（从 repo root 开始）
2. fablePath: 输出路径（规则：把路径中的 /sections/ 换成 /fables/，去掉最后的 .md，把倒数第二级目录名作为节目录，最后一级文件名作为 fable 文件名并加两位序号前缀）
3. chapter: 章名称（路径中 sections 后面的第一级目录名）
4. section: 节名称（路径中 sections 后面的第二级目录名，去掉 .md）
5. title: 标题内容（从 md 中提取的标题文字）
6. index: 同一节内该标题的序号（从 1 开始）

示例：
- source: 04-基金从业/03-科目三-私募股权/converted/sections/01-股权投资基金概述 …/01-股权投资基金的概念和特点.md
- fable:  04-基金从业/03-科目三-私募股权/converted/fables/01-股权投资基金概述 …/01-股权投资基金的概念和特点/01-股权投资基金的概念和特点.md

注意：排除 00_index.md 文件。

返回格式必须是 JSON：
{
  "tasks": [
    {"sourcePath": "...", "fablePath": "...", "chapter": "...", "section": "...", "title": "...", "index": 1}
  ],
  "totalCount": 123
}
`, { label: 'scan-ke-san' })

log(`Discovered ${scanResult.totalCount} fable tasks`)
const chapters = [...new Set(scanResult.tasks.map(t => t.chapter))].sort()
log(`Chapters: ${chapters.join(', ')}`)

// ===== Generate Phase =====
phase('Generate')
log('Starting parallel generation...')

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

// 支持通过 args 控制
// args.mode === 'sample' → 只生成前 3 个任务作为 golden sample
// args.chapters → 只处理指定章节数组
const targetChapters = args && args.chapters ? args.chapters : chapterNames

let tasksToRun = []
for (const chapterName of targetChapters) {
  const tasks = chapterGroups[chapterName]
  if (!tasks) {
    log(`⚠️ Chapter ${chapterName} not found, skipping`)
    continue
  }
  tasksToRun = tasksToRun.concat(tasks)
}

if (args && args.mode === 'sample') {
  tasksToRun = tasksToRun.slice(0, 3)
  log(`Sample mode: only generating ${tasksToRun.length} golden samples`)
}

for (const chapterName of targetChapters) {
  const tasks = chapterGroups[chapterName]
  if (!tasks) continue

  const chapterTasks = tasksToRun.filter(t => t.chapter === chapterName)
  if (chapterTasks.length === 0) continue

  log(`Processing chapter: ${chapterName} (${chapterTasks.length} tasks)`)

  await parallel(
    chapterTasks.map(task => () => {
      log(`  → ${task.title}`)
      return agent(buildPrompt(task), {
        label: `gen:${task.title.slice(0, 20)}`,
        phase: 'Generate',
      })
    })
  )

  log(`✓ Chapter ${chapterName} complete`)
}

log('All chapters processed!')

// ===== Review Phase =====
phase('Review')
log('Starting quality review...')

const SAMPLE_RATE = 0.2
const MIN_SAMPLES = 2
const MAX_SAMPLES = 5

for (const chapterName of targetChapters) {
  const tasks = chapterGroups[chapterName]
  if (!tasks) continue

  const chapterRunTasks = tasksToRun.filter(t => t.chapter === chapterName)
  if (chapterRunTasks.length === 0) continue

  const sampleSize = Math.min(
    MAX_SAMPLES,
    Math.max(MIN_SAMPLES, Math.ceil(chapterRunTasks.length * SAMPLE_RATE))
  )

  const step = Math.max(1, Math.floor(chapterRunTasks.length / sampleSize))
  const samples = []
  for (let i = 0; i < chapterRunTasks.length && samples.length < sampleSize; i += step) {
    samples.push(chapterRunTasks[i])
  }

  log(`Reviewing ${chapterName}: ${samples.length} samples`)

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

  log(`  ${chapterName}: ${passRate}% passed (${reviews.length - failed.length}/${reviews.length} passed)`)

  if (failed.length > 0) {
    log(`  ⚠️ Failed samples:`)
    for (const f of failed) {
      log(`     - ${f.fablePath}: ${f.issues.join('; ')}`)
    }
  }
}

log('Review complete!')
