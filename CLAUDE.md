# Reading Notes Agent Rules

## Source Of Truth

- `CLAUDE.md` is the only editable project instruction file.
- `AGENTS.md` must be a symbolic link to `CLAUDE.md` in the same directory.
- When these instructions need to change, edit `CLAUDE.md` first, then ensure `AGENTS.md` still points to it.
- If `AGENTS.md` is ever found as a separate regular file, merge any useful content into `CLAUDE.md`, delete the regular file, and recreate the symlink.

## Project Shape

This repository stores book source files, converted reading copies, and notes.

- Top-level subfolders are split into two kinds, distinguished by their numeric prefix:
  - **Study programs (exams)** use a 1–2 digit prefix `0N-...` (e.g. `01-cfa/`, `04-基金从业/`). They keep raw materials under `sources/` and derived working copies under `converted/`.
  - **Books** use a 3-digit prefix `NNN-...` starting at `100-` (e.g. `100-finite-and-infinite-game/`).
- Each book folder should have a `notes.md` file for accumulated reading notes.
- Each book folder may have an `open_questions.md` file for unsettled doubts, objections, and interpretations that should not be treated as final notes yet.
- Converted files, such as Markdown or HTML generated from EPUB, should stay under that book folder.
- Do not rewrite or clean converted book text unless the user explicitly asks.

Current known book folders:

- `100-finite-and-infinite-game/` - `Finite and Infinite Games` by James Carse.
- `101-agentic-design-patterns/` - `Agentic Design Patterns` (zeljkoavramovic/agentic-design-patterns, GitHub).
- `102-deng-xiaoping-era/` - `邓小平时代` (Ezra Vogel, 《Deng Xiaoping and the Transformation of China》).
- `103-mao-zedong-selected-works/` - `毛泽东选集` (一至五卷).
- `104-the-prince/` - `君主论` (Niccolò Machiavelli, 《Il Principe》).
- `105-myth-of-sisyphus/` - `西西弗神话` (Albert Camus, 《Le Mythe de Sisyphe》).
- `106-reality-is-broken/` - `游戏改变世界` (Jane McGonigal, 《Reality Is Broken》).
- `107-zhang-yiming/` - `张一鸣传记`.
- `108-ordinary-men/` - `Ordinary Men` (Christopher Browning).
- `109-the-price-of-blood/` - `血酬定律` (吴思).

## Book Content Q&A Workflow

When the user asks a question about the content of a book in this repository:

1. Identify the corresponding book folder from the user's wording, referenced file path, current browser URL, or open file context.
2. Prefer the converted Markdown or HTML as the source for lookup. For `finite_and_inifinite_game/`, use `converted/finite-and-infinite-games.md` or `converted/html/`.
3. Explain first. Do not rush to record an answer while the user is still confused or pushing back.
4. Treat the conversation as a clarification loop until the user signals the topic is understood, asks to save it, or asks for a summary.
5. At the end of a topic, produce a concise summary of the exchange and the stable understanding reached.
6. Append to that book folder's `notes.md` only after the user explicitly asks to save/add notes, or after the user accepts the summary.
7. If the user asks to preserve a doubt, unresolved objection, or "存疑" item, append it to that book folder's `open_questions.md` instead of `notes.md`.
8. Never overwrite existing notes or open questions. Append a new entry at the end.
9. If the target book folder is ambiguous, ask before writing.
10. If `notes.md` or `open_questions.md` does not exist when needed, create it.

Use this entry format:

```markdown
## YYYY-MM-DD HH:mm - Short question title

**Question**

User's question.

**Source**

- Book: Book title
- Location: chapter / section / page anchor / file path if available

**Original excerpt**

> Exact excerpt from the book, kept short and directly relevant.

**Answer**

Assistant's answer.
```

Keep original text and interpretation separate:

- `Original excerpt` must be copied from the book text, not paraphrased.
- `Answer` may summarize, explain, compare, or translate, but should not pretend to be source text.
- Use only the excerpt needed to support the answer. For long passages, quote a short relevant excerpt and cite the chapter or page anchor instead of copying large blocks.
- Do not save half-baked explanations. Notes should capture settled understanding, not every intermediate attempt.

## Interaction Defaults

- User experience and clarity take priority over tooling preferences.
- Make the smallest change that satisfies the request.
- Before editing files, state what will be changed.
- When uncertain, surface the uncertainty and ask instead of guessing silently.
- Keep unrelated cleanup out of scope.

## Study Program Folders (基金从业 / CFA / IIQE 备考)

Folders named `0N-...` at the top level of this repo are study programs, not books. They keep raw materials under `sources/` and derived working copies under `converted/`. Books live at the `NNN-...` (100+) level and follow different conventions.

Conventions for study program folders:

- `sources/` is the original material. PDFs are symlinked, not copied. Never write to files inside `sources/`.
- `converted/` is the parsed working copy. Once generated, the markdown text and extracted images are the canonical "source of truth" for AI Q&A.
- The top-level `index.md`, `progress.md`, and `README.md` (when present) describe the program and link into `converted/`.
- Sections are kept fine-grained (one 节 / one 章节 per file) so a single section fits comfortably in an AI context window for back-and-forth Q&A.

Known study program folders:

- `01-cfa/` - CFA 资料集合，按考试年份分子目录。
  - `01-cfa/2025-12/` - CFA 一级 2025-12 备考资料。
  - `01-cfa/2020/` - CFA 二级 2020 资料。
- `02-iique/` - 香港保险业中介人资格考试（IIQE），5 张卷（占位，暂无 PDF）。
- `04-基金从业/01-科目一-法律法规/` - 基金法律法规、职业道德与业务规范。`sources/01-教材.pdf` 是 symlink，未拆分。
- `04-基金从业/02-科目二-证券投资基金/` - 证券投资基金基础知识。教材 PDF 已通过 MinerU 拆成 `converted/sections/<章>/<节>.md`，18 章 60 节。
- `04-基金从业/03-科目三-私募股权/` - 占位（暂无 PDF）。

## Study Program Q&A Workflow

When the user asks a question about a 基金从业 or CFA study program:

1. Identify the program from the user's wording, referenced file path, current browser URL, or open file context.
2. For converted programs (e.g. 基金从业 科目二), use the per-section markdown under `converted/sections/<章>/<节>.md` as the source. Open the relevant section, not the whole book.
3. Answer the user normally in the conversation.
4. Append a short entry to the program's `notes.md` if it exists. If `notes.md` does not exist, create it.
5. Never overwrite existing notes. Append a new entry at the end.
6. If the program folder is ambiguous, ask before writing notes.

Use this entry format for `notes.md`:

```markdown
## YYYY-MM-DD HH:mm - Short question title

**Question**

User's question.

**Source**

- Program: e.g. 基金从业 科目二 / CFA L1 2025-12
- Location: chapter / section / 节 markdown 路径

**Original excerpt**

> Exact excerpt from the 节 markdown, kept short and directly relevant.

**Answer**

Assistant's answer.
```

Keep original text and interpretation separate:

- `Original excerpt` must be copied from the 节 markdown, not paraphrased.
- `Answer` may summarize, explain, compare, or translate, but should not pretend to be source text.
- Use only the excerpt needed to support the answer. For long passages, quote a short relevant excerpt and cite the section / page anchor instead of copying large blocks.

## Progress Tracking (二态)

Study program folders may have a `progress.md` with checkbox lines `- [ ]` (unread) and `- [x]` (read). When the user says they finished a section:

1. Open the program's `progress.md`.
2. Find the matching line and change `[ ]` to `[x]`. Do not introduce a third state.
3. If the program has no `progress.md` and the user asks for one, generate it from the section index in `index.md`.

Do not edit `progress.md` for any other reason (e.g. "studying" or "in progress"). Read = checked, unread = unchecked, nothing else.
