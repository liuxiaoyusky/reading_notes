# Reading Notes Agent Rules

## Source Of Truth

- `CLAUDE.md` is the only editable project instruction file.
- `AGENTS.md` must be a symbolic link to `CLAUDE.md` in the same directory.
- When these instructions need to change, edit `CLAUDE.md` first, then ensure `AGENTS.md` still points to it.
- If `AGENTS.md` is ever found as a separate regular file, merge any useful content into `CLAUDE.md`, delete the regular file, and recreate the symlink.

## Project Shape

This repository stores book source files, converted reading copies, and notes.

- Each book should live in its own top-level subfolder.
- Each book folder should have a `notes.md` file for accumulated reading notes.
- Converted files, such as Markdown or HTML generated from EPUB, should stay under that book folder.
- Do not rewrite or clean converted book text unless the user explicitly asks.

Current known book folder:

- `finite_and_inifinite_game/` - `Finite and Infinite Games` by James Carse.

## Book Content Q&A Workflow

When the user asks a question about the content of a book in this repository:

1. Identify the corresponding book folder from the user's wording, referenced file path, current browser URL, or open file context.
2. Prefer the converted Markdown or HTML as the source for lookup. For `finite_and_inifinite_game/`, use `converted/finite-and-infinite-games.md` or `converted/html/`.
3. Answer the user normally in the conversation.
4. Append the original supporting excerpt and the answer to that book folder's `notes.md`.
5. Never overwrite existing notes. Append a new entry at the end.
6. If the target book folder is ambiguous, ask before writing notes.
7. If `notes.md` does not exist in the target book folder, create it.

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

## Interaction Defaults

- User experience and clarity take priority over tooling preferences.
- Make the smallest change that satisfies the request.
- Before editing files, state what will be changed.
- When uncertain, surface the uncertainty and ask instead of guessing silently.
- Keep unrelated cleanup out of scope.

## Study Program Folders (基金从业 / CFA 备考)

Folders named `0N-...` at the top level of this repo are study programs, not books. They keep raw materials under `sources/` and derived working copies under `converted/`.

Conventions for study program folders:

- `sources/` is the original material. PDFs are symlinked, not copied. Never write to files inside `sources/`.
- `converted/` is the parsed working copy. Once generated, the markdown text and extracted images are the canonical "source of truth" for AI Q&A.
- The top-level `index.md`, `progress.md`, and `README.md` (when present) describe the program and link into `converted/`.
- Sections are kept fine-grained (one 节 / one 章节 per file) so a single section fits comfortably in an AI context window for back-and-forth Q&A.

Known study program folders:

- `04-基金从业/01-科目一-法律法规/` - 基金法律法规、职业道德与业务规范。`sources/01-教材.pdf` 是 symlink，未拆分。
- `04-基金从业/02-科目二-证券投资基金/` - 证券投资基金基础知识。教材 PDF 已通过 MinerU 拆成 `converted/sections/<章>/<节>.md`，18 章 60 节。
- `04-基金从业/03-科目三-私募股权/` - 占位（暂无 PDF）。
- `02-cfa-l1-2025-12/` - CFA 一级 2025-12 备考资料集合（Schweser / 教材 / 题库 / mock / 思维导图 / 公式 / 1000 题），全部存为原文件副本。
- `03-cfa-l2-2020/` - CFA 二级 2020 资料集合。

## Study Program Q&A Workflow

When the user asks a question about a 基金从业 or CFA study program:

1. Identify the program from the user's wording, referenced file path, current browser URL, or open file context.
2. For converted programs (科目二), use the per-section markdown under `converted/sections/<章>/<节>.md` as the source. Open the relevant section, not the whole book.
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

- Program: e.g. 基金从业 科目二
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
