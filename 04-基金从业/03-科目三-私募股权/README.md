# 股权投资基金 — 学习项目

> 基金从业资格考试 2025 统编教材 · 科目三 · 《股权投资基金》

## 目录结构

```
.
├── index.md                   # 总目录（跳转入口）
├── progress.md                # 学习进度（二态勾选）
├── notes.md                   # 学习笔记（AI 问答追加，可选）
├── 基金从业2025新编教材-股权投资基金基础知识（科目三）.pdf
└── converted/                 # MinerU 解析结果
    ├── content_list.json      # 全文结构化数据
    ├── raw.md                 # 原始 markdown
    ├── images/                # 提取的图片
    └── sections/              # 拆分后的章节（学习最小单元）
        └── 01-<章名>/
            ├── 00_index.md
            └── 01-<节名>.md
```

## 统计

- 总章节：**9 章 41 节**
- 总页数：351 页
- 教材版本：2025 版（中国证券投资基金业协会组编）

## 如何使用

### 与 AI 一起学习

1. **选一节**：打开 `progress.md`，找一节未勾选的
2. **提问**：对 AI 说"读一下 `converted/sections/第N章/第M节.md`，然后帮我..."
3. **记笔记**：AI 的回答会自动追加到 `notes.md`
4. **标记完成**：对 AI 说"我完成了第N章第M节"，AI 会帮你勾选

### 快速跳转

- 总目录：[index.md](index.md)
- 学习进度：[progress.md](progress.md)
- 章节目录：[converted/sections/](converted/sections/)

## 注意事项

- 不要修改 `converted/` 下的原始文件
- `converted/sections/` 下的 `.md` 是学习的最小单元
- 图片保存在 `converted/images/`，请勿移动
- MinerU 解析的内容可能存在小错误（错别字、表格识别等），以原 PDF 为准
