# The Art of Loving · 学习指引

Erich Fromm 1956 年的经典小书《The Art of Loving》(《爱的艺术》)。全书 100 页左右,英文版共 1 篇前言 + 4 章 + 1 篇后记(II 章内含 5 个子节)。

## 目录结构

```
110-the-art-of-loving/
├── README.md                # 本文件: 学习指引
├── index.md                 # 章节总览 + 段落链接
├── notes.md                 # AI Q&A 累积笔记(空)
├── open_questions.md        # 未决疑问(空)
└── sources/
│   └── the-art-of-loving.mobi           # 原始 MOBI(symlink 到 repo 顶层)
└── converted/
    ├── the-art-of-loving.md             # 完整 md 解析(238KB)
    ├── the-art-of-loving.epub           # 提取出的 EPUB(参考)
    └── sections/                        # 按章节切的 markdown(10 个 part)
        ├── 00-part0000.md               # 封面 + 简介
        ├── 01-part0001.md               # 目录
        ├── 02-part0002.md               # Forward(前言)
        ├── 03-part0003.md               # I. Is Love an Art?
        ├── 04-part0004.md               # II. The Theory of Love (含 1)
        ├── 05-part0005.md               # 2. Love Between Parent and Child
        ├── 06-part0006.md               # 3. The Objects of Love (含 a-e)
        ├── 07-part0007.md               # III. Love and its Disintegration...
        ├── 08-part0008.md               # IV. The Practice of Love
        └── 09-part0009.md               # Epilogue — World Perspectives
```

## 章节结构

| # | 章节 | 来源文件 | 字符数 |
|---|------|---------|--------|
| 00 | 封面 + 简介 | part0000 | 699 |
| 01 | Contents(目录) | part0001 | 421 |
| 02 | Forward | part0002 | 2,171 |
| 03 | I. Is Love an Art? | part0003 | 8,994 |
| 04 | II. The Theory of Love | part0004 | 51,897 |
| 05 | 2. Love Between Parent and Child | part0005 | 13,118 |
| 06 | 3. The Objects of Love | part0006 | 59,961 |
| 07 | III. Love and its Disintegration in Contemporary Western Society | part0007 | 39,210 |
| 08 | IV. The Practice of Love | part0008 | 45,438 |
| 09 | Epilogue — World Perspectives | part0009 | 16,010 |

## 转换说明

- **源文件**: MOBI (KF8/Mobipocket v6, codepage 65001)
- **转换路径**: mobi → epub (用 `mobi` Python 库) → markdown (BeautifulSoup + lxml)
- **章节切分**: mobi 自带 10 个 XHTML 分片,1:1 对应原书的 10 个 part(不是按章切,而是 mobi 内部排版的分片)
- **Heading 修正**: mobi 用 `<h3>` 写章名,本脚本将每个 part 的第一个 H3 提升为 H1,后续标题按比例降级

## 学习建议

- 英文原版,可对照中文译本(《爱的艺术》, 萨茹菲 译, 上海译文出版社)读
- 全文核心论点:**爱是一种能力,需要练习,而不是一种可以偶然"坠入"的感情**
- 适合做单本精读笔记,不建议做成寓言(这本书本身就是寓言)

## 相关链接

- 项目根 `README.md`
- 同类书籍:`109-the-price-of-blood/`, `105-myth-of-sisyphus/`, `106-reality-is-broken/`