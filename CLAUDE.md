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
