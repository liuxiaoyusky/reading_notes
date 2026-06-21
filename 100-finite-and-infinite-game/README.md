# Finite and Infinite Games · 学习指引

James Carse 1986 年的小书《Finite and Infinite Games》，全书 7 章 101 section（每 section 一页纸的密度），无中间节层级。

## 目录结构

```
100-finite-and-infinite-game/
├── README.md                # 本文件: 学习指引
├── index.md                 # 7 章总览 + 101 section 链接
├── progress.md              # 二态勾选（已读 / 未读）
├── notes.md                 # AI Q&A 累积笔记
├── Finite_..._Carse_..._1lib_sk,.epub    # 原始 EPUB
└── converted/
    ├── finite-and-infinite-games.md  # 完整 md 解析（238KB）
    ├── content_list.json     # 结构化块（来自 EPUB 解析）
    ├── assets/images/        # 抽出的原图
    ├── sections/             # 按章节切的 markdown（每节一页）
    │   ├── 01-there-are-at-least-two-kinds-of-games/
    │   │   ├── 00_index.md
    │   │   ├── 01.md
    │   │   ├── 02.md
    │   │   └── ... (31 sections)
    │   └── ... (7 chapters, 101 sections)
    └── fables/               # 寓言故事（1952 上海十六铺风格）
        ├── 01-there-are-at-least-two-kinds-of-games/
        │   ├── 01.md
        │   └── ... (31 fables)
        └── ... (7 chapters, 101 fables)
```

## 学习流程

1. **选一节要学的内容**: 从 [index.md](index.md) 找到 section markdown（如 `converted/sections/01-there-are-at-least-two-kinds-of-games/01.md`）。
2. **打开提问**: 把 section markdown 喂给 AI（直接复制整节，或让 AI 用 `cat` 读）。每节约一页纸的密度，丢进 AI 完全够上下文。
3. **随时追问**: section markdown 顶部有 frontmatter（`chapter` / `section` / `page_idx_start`），AI 可以直接定位。
4. **学完勾选**: 在 [progress.md](progress.md) 把对应行打勾。回退就取消勾选。
5. **累积笔记**: 在 [notes.md](notes.md) 累积 Q&A 笔记。
6. **寓言辅助理解**: `converted/fables/` 下有 101 篇用 1952 年上海十六铺米行人物（老陆、老沈、老冯、顾先生）讲的故事版本，每个对应一个 section。

## 用 AI 怎么问效果好

- **节 markdown 内提问**: 直接复制整节，问「请用简单的话解释 XX」「帮我画一个表格对比 XX」等。
- **跨节对比**: section 体积小，可以让 AI 同时读 2-3 节做对比。
- **寓言辅助**: 如果某个 section 难懂，先看 `fables/` 下对应文件（如 `fables/01-.../01.md`），再回头读原文。

## 这本书的特殊性

- **没有中间节层级**——书作者把全书切成 101 段，每段一页，没有内部子标题。section 命名是 `01.md`（Chapter 1 第 1 节，即 Section 1）。
- **寓言风格统一**——所有 101 个 fable 都用 1952 年上海十六铺码头的米行人物（老陆、老沈、老冯、顾先生等）作背景，跨 section 保持人物一致性。
- **英文为主**——原文是英文，section 文件保留英文，fable 是中文。
