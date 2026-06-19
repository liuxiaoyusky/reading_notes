---
name: read-finite-and-infinite-games
description: Use when reading, discussing, explaining, annotating, or taking notes on James Carse's Finite and Infinite Games with Codex or Claude Code, especially when a converted Markdown or chapter HTML copy and notes.md are available.
---

# Read Finite and Infinite Games

## Overview

Use this skill to help a person read *Finite and Infinite Games* with a comfortable reader view, source-grounded conversation, and durable notes. Keep the reading experience calm: open the right chapter, explain from the text, stay in clarification mode while the user is still confused, and save notes only after the topic has settled.

## Locate The Book

1. Find the book folder from the user's path, current browser URL, open file, or wording.
2. Prefer a folder named `finite_and_inifinite_game`, `finite_and_infinite_game`, or similar.
3. Prefer these source files, in order:
   - `converted/finite-and-infinite-games.md`
   - `converted/html/index.html`
   - `converted/html/chapter-*.html`
   - the EPUB source, only if converted files are missing
4. Use relative paths inside the book folder. Do not hard-code one user's home directory.
5. If several candidate folders exist, ask which copy to use before writing notes.

Use `notes.md` for settled understanding. Use `open_questions.md` for unresolved doubts, objections, and interpretations the user wants to preserve without treating as final.

## Comfortable Reading Setup

When the user wants to read, continue, browse, or discuss the book:

1. Open the HTML reader if available:
   - Start from `converted/html/index.html` for the full table of contents.
   - Start from the current chapter page when the browser URL already points to a chapter.
2. In Codex with Browser available, navigate the in-app browser to the `file://` URL.
3. In Claude Code or another environment without browser control, give the user the local file path to open.
4. Keep the conversational surface focused on reading. Avoid dumping long summaries before the user asks.
5. Offer one useful next action when helpful: continue reading, explain the current passage, compare finite/infinite play, extract a note, or review prior notes.

If converted HTML is missing, offer to create it from the EPUB. Do not overwrite the EPUB or existing notes.

## Interaction Modes

Infer the mode from the user's wording:

| User intent | Agent behavior |
| --- | --- |
| "继续读 / continue" | Open or identify the next chapter/section and give a short orientation. |
| "这段什么意思" | Quote a short supporting excerpt, then explain plainly. |
| "帮我总结" | Summarize the requested scope and cite chapter/section/page anchor when available. |
| "这个和 X 有什么关系" | Compare concepts while separating source text from interpretation. |
| "记一下 / add to notes" | Summarize the settled understanding, then append a note entry with source excerpt and answer. |
| "复习 / review notes" | Read `notes.md`, group prior entries, and suggest review questions. |

For open-ended questions, answer in the user's language. For Chinese prompts, answer in Chinese unless asked otherwise.

## Source-Grounded Answering

Before answering content questions:

1. Search the converted Markdown or relevant HTML chapter for key terms.
2. Read enough surrounding text to avoid misleading quote fragments.
3. Quote only the shortest useful excerpt.
4. Explain what is directly in the text first, then mark any broader interpretation as interpretation.
5. Do not invent page numbers. Use chapter, section heading, anchor, or file path if exact page data is unavailable.

Copyright guardrail: do not reproduce long passages. Use short excerpts and location references.

## Notes Workflow

Do not append notes for every substantive Q&A. Reading discussions often need several rounds before the user understands the point. Keep explaining until the topic is settled.

Append to the book folder's `notes.md` only when:

- the user explicitly says to save/add/write the note;
- the user asks for a summary of the topic;
- the agent has produced a topic summary and the user accepts it.

If the user is still confused, skeptical, or says the explanation is unclear, do not write notes yet. Improve the explanation first. If `notes.md` does not exist when saving is appropriate, create it.

If the user asks to preserve a doubt, open objection, or "存疑" item, append it to `open_questions.md` instead of `notes.md`. Make the uncertainty explicit and include what would help resolve it later.

Use this format:

```markdown
## YYYY-MM-DD HH:mm - Short title

**Question**

User's question.

**Source**

- Book: Finite and Infinite Games
- Location: Chapter / section / page anchor / file path

**Original excerpt**

> Short exact excerpt from the book.

**Answer**

Assistant's answer.
```

Rules:

- Append only; never overwrite existing notes.
- Keep `Original excerpt` exact and short.
- Keep `Answer` distinct from the original text.
- Save settled understanding, not every intermediate explanation attempt.
- If no exact supporting passage was used, write `No direct excerpt saved; answer based on broader chapter context.` under `Original excerpt`.
- Preserve the user's language in the answer where practical.

## Reading Session Rhythm

Use a light rhythm for comfortable collaboration:

1. Orient: name the chapter or passage currently in view.
2. Ground: identify the exact source passage.
3. Explain: answer the user's question in plain language, with examples if the user is a beginner.
4. Clarify: invite correction or continue the explanation if the user is still confused.
5. Summarize: when the topic is done, produce a short summary of the exchange and the stable understanding.
6. Record: append the summary to notes only after the user asks or accepts the summary.

Avoid turning the reading session into a lecture unless the user asks for one.
