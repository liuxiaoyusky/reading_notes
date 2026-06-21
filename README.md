# Reading Notes

个人阅读与备考笔记仓库。混了两类内容：

- **书**：单本 PDF / EPUB 转 markdown，方便和 AI 一起读 + 整理。
- **备考项目**：基金从业、CFA 这类多资料集合，按科目 / 级别分子目录。

详细约定见 [CLAUDE.md](CLAUDE.md)（[AGENTS.md](AGENTS.md) 是 symlink，规则同源）。

## 目录

### 书（100+）

- [100-finite-and-infinite-game/](./100-finite-and-infinite-game/) — `Finite and Infinite Games`（James Carse）。已转 markdown 放 `converted/`，笔记累在 `notes.md`。
- [101-agentic-design-patterns/](./101-agentic-design-patterns/) — `Agentic Design Patterns`（zeljkoavramovic/agentic-design-patterns，GitHub）。
- [102-deng-xiaoping-era/](./102-deng-xiaoping-era/) — `邓小平时代`（傅高义 / Ezra Vogel）。
- [103-mao-zedong-selected-works/](./103-mao-zedong-selected-works/) — `毛泽东选集`（一至五卷）。
- [104-the-prince/](./104-the-prince/) — `君主论`（Machiavelli）。
- [105-myth-of-sisyphus/](./105-myth-of-sisyphus/) — `西西弗神话`（Camus）。
- [106-reality-is-broken/](./106-reality-is-broken/) — `游戏改变世界`（Jane McGonigal）。
- [107-zhang-yiming/](./107-zhang-yiming/) — `张一鸣传记`。
- [108-ordinary-men/](./108-ordinary-men/) — `Ordinary Men`（Christopher Browning）。
- [109-the-price-of-blood/](./109-the-price-of-blood/) — `血酬定律`（吴思）。

### 备考项目（0–99）

- [01-cfa/](./01-cfa/) — CFA 资料集合，按考试年份分
  - [01-cfa/2025-12/](./01-cfa/2025-12/) — CFA 一级 2025-12
  - [01-cfa/2020/](./01-cfa/2020/) — CFA 二级 2020
- [02-iique/](./02-iique/) — 香港保险业中介人资格考试（IIQE），5 张卷（占位，暂无 PDF）
- [04-基金从业/](./04-基金从业/) — 基金从业三个科目
  - [01-科目一-法律法规](./04-基金从业/01-科目一-法律法规/) — 教材 PDF 是 symlink，未拆分。
  - [02-科目二-证券投资基金](./04-基金从业/02-科目二-证券投资基金/) — 教材 PDF 已通过 MinerU 拆成 18 章 60 节 markdown，574 张原图。带 `index.md` / `progress.md` / `README.md`。
  - [03-科目三-私募股权](./04-基金从业/03-科目三-私募股权/) — 占位（暂无 PDF）。

## 备考项目的标准结构

```
0N-科目X-.../
├── README.md         # 学习指引（怎么用 AI 学）
├── index.md          # 章节总览 + 链接
├── progress.md       # 二态勾选（已读 / 未读）
├── notes.md          # AI Q&A 累积笔记（可选）
├── sources/          # 原始素材，PDF 走 symlink，不写
│   ├── 01-教材.pdf
│   └── 02-历年真题/
└── converted/        # 解析产物（解析后才是 AI 用的"原文"）
    ├── content_list.json
    ├── content_list_v2.json
    ├── raw.md
    ├── images/
    └── sections/
        ├── 01-章标题/
        │   ├── 00_index.md
        │   └── NN-节标题.md
        └── …
```

## 维护准则（速查）

- `sources/` 永远只读。所有解析结果都进 `converted/` 或同级。
- 大文件用 symlink，别复制多份占空间。
- 跳过 `.DS_Store`、`.downloading`、`._*` 等系统/下载残留。
- 解析时 `lang_list` 不传（hybrid-auto-engine 不接受，只用 `start_page_id` / `end_page_id` 控页范围）。
- 解析只产出，不动原 PDF；正文里所有图都引用 `converted/images/`，不要重抽。
- 拆分按原文的「第 N 章 / 第 N 节」边界，不合并、不拆。
- 进度用 `[ ]` / `[x]` 二态，不引入第三种。

## 工具栈

- **MinerU**（`http://10.1.9.133:9987`） — PDF → content_list + md + images
- **Python 脚本** — 在 `/Users/sky/Documents/Codex/2026-06-09/files-mentioned-by-the-user-2025/work/` 下，源文件不写
