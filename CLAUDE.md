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
- Each book folder may have an `open_questions.md` file for unsettled doubts, objections, and interpretations that should not be treated as final notes yet.
- Converted files, such as Markdown or HTML generated from EPUB, should stay under that book folder.
- Do not rewrite or clean converted book text unless the user explicitly asks.

Current known book folder:

- `finite_and_inifinite_game/` - `Finite and Infinite Games` by James Carse.

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
