import json
import os

with open('converted/fables/.orchard/progress.json') as f:
    p = json.load(f)

# Pick fab 02 (一)专业性较强 - 327 CJK
fid = '01-股权投资基金的概念和特点/02'
v = p['fables'][fid]

cjk = v['cjk']
if cjk < 500:
    word_range = '500-900'
elif cjk < 1500:
    word_range = '900-1300'
else:
    word_range = '1300-1800'

forbidden_terms = '股权投资基金/基金/管理人/托管人/LP/GP/私募/合格投资者/非公开交易/证监会/中国证券投资基金业协会/创业投资/并购基金/估值/收益分配/信息披露'

heading = v['heading']
sl = v['start_line']
el = v['end_line']
source = v['source_section']
target = v['target_path']

prompt = f"""你是一个寓言故事写手。**使用 `/fable-teacher` skill**，按其全部硬规则创作。

【源数据】
- 源 fab CJK: {cjk}（来自源文件 line {sl}-{el}）
- 推荐故事正文字数：**{word_range} 字**（根据 fab 大小自适应，不要硬写 600-1200）
- 核心概念（**必须聚焦 1 个，不可塞多个**）: 股权投资基金"专业性较强"——被投资企业多为非上市企业，估值/治理/披露与上市公司有差距，因此对管钱的人专业性要求高（包括企业管理、资本市场、财务、行业、法律等）。
- 禁止专业术语清单: {forbidden_terms}

【任务】
1. **Read `/fable-teacher` skill 全文**，遵守其全部硬规则
2. **Read 源文件** `{source}`，重点关注 line {sl}-{el} 的内容
3. **写一个 {word_range} 字的连续叙事寓言**：
   - 4 段式：开场→冲突→转折→结局
   - 真实人物（中文名字），有具体场景和戏剧冲突
   - 0 加粗、0 专业术语（用比喻替换）
   - 故事中**只解决 1 个核心问题**（不要塞多概念）
   - 对应点表格的"故事元素"必须是故事里具体出现的人物动作/情节/场景（不能写"故事里说""体现了"这种空话）
   - 原文定义必须从源文件直接复制，不要改写、不要合并
4. **Write 到目标文件**：`{target}`
5. **git commit**：
   ```bash
   cd /Users/sky/Documents/github/reading_notes
   git add "{target}"
   git commit -m "feat: 《{heading}》—— 科目三 fable"
   ```
6. **回报**：标题、故事字数（CJK）、commit SHA

【输出模板】
```markdown
# {heading}

## <emoji> 寓言故事 —— 《<4-6字故事名>》

<故事正文 {word_range} 字>

---

**📖 原文定义**

> 直接引用源文件 line {sl}-{el} 的原文

**💡 对应点**

| 故事元素 | 概念对应 |
|---------|---------|
| ... | ... |

---

> 📝 来源：股权投资基金（科目三）· 第一章第一节 · {heading}
```

完成后回报：标题、字数、commit SHA。
"""

os.makedirs('converted/fables/.orchard/prompts', exist_ok=True)
with open('converted/fables/.orchard/prompts/test_02.md', 'w') as f:
    f.write(prompt)
print('Prompt saved to: converted/fables/.orchard/prompts/test_02.md')
print(f'Length: {len(prompt)} chars')
print(f'Word range: {word_range}')
print(f'CJK: {cjk}')
