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
