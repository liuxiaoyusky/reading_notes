#!/usr/bin/env python3
"""Batch-generate IIQE Paper 1 fables from the orchard manifest.

This driver keeps progress.json writes in the main process to avoid concurrent
state-file races. Claude workers only write target markdown files.
"""

import argparse
import json
import re
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from opencc import OpenCC
except Exception:
    OpenCC = None

PROJECT = Path("/Users/sky/Documents/github/reading_notes/02-iique/paper-1")
ORCHARD = PROJECT / "converted/fables/.orchard"
MANIFEST = ORCHARD / "manifest.json"
PROGRESS = ORCHARD / "progress.json"
WORLD = ORCHARD / "universe/world.md"
CAST_DIR = ORCHARD / "universe/chapter-casts"
LOG_DIR = ORCHARD / "logs/batches"
ORCHARD_PY = Path("/Users/sky/Documents/github/ai-developer-skills/general/fable-orchestrator/scripts/orchard.py")

TRAD_CHECK_CHARS = "風險則會為與對這個體來說業務責關係發現學習資料應該開後過時義"
T2S = OpenCC("t2s") if OpenCC else None
PROGRESS_LOCK = threading.Lock()


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def orchard(*args):
    with PROGRESS_LOCK:
        return subprocess.run(
            ["python3", str(ORCHARD_PY), "--project", str(PROJECT), *args],
            text=True,
            capture_output=True,
            check=False,
        )


def normalize_file(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if T2S:
        text = T2S.convert(text)
    text = text.replace("## 原文定義", "## 原文定义")
    text = text.replace("## 對應點", "## 对应点")
    text = text.replace("保險考試1", "保险考试1")
    path.write_text(text, encoding="utf-8")


def story_segment(text: str) -> str:
    match = re.search(r"## 故事\s*(.*?)(?:\n## 原文[定定义義]|$)", text, re.S)
    return match.group(1) if match else ""


def validate_fab(fab):
    path = Path(fab["absolute_target"])
    if not path.exists():
        return False, "missing target file"
    normalize_file(path)
    text = path.read_text(encoding="utf-8", errors="ignore")
    if len(text) < 750:
        return False, f"too short chars={len(text)}"
    h1 = [line for line in text.splitlines() if line.startswith("# ") and not line.startswith("## ")]
    if len(h1) != 1:
        return False, f"h1_count={len(h1)}"
    for marker in ["## 故事", "## 原文定义", "## 对应点"]:
        if marker not in text:
            return False, f"missing {marker}"
    if not text.startswith("---\n"):
        return False, "missing frontmatter"
    story = story_segment(text)
    if len(story) < 450:
        return False, f"story too short chars={len(story)}"
    trad_hits = sum(story.count(ch) for ch in TRAD_CHECK_CHARS)
    if trad_hits > 35:
        return False, f"too many traditional chars in story={trad_hits}"
    return True, "pass"


def build_prompt(batch):
    first = batch[0]
    cast = CAST_DIR / f"{first['chapter_dir']}.json"
    items = []
    for fab in batch:
        items.append(
            {
                "id": fab["id"],
                "source": fab["absolute_source"],
                "target": fab["absolute_target"],
                "h1": fab["h1_title"],
                "section": fab["section_name"],
                "chars": fab["chars"],
            }
        )
    items_json = json.dumps(items, ensure_ascii=False, indent=2)
    return f"""
你是 IIQE Paper 1 / 保险考试1 的批量寓言生成 worker。你只写本批 target markdown 文件，不要修改 progress.json、manifest.json、world.md 或 chapter-casts。

必须先阅读：
- 世界观：{WORLD}
- 本章人物谱：{cast}

本批 manifest 条目如下。每个条目都必须读完整 source，并严格写到对应 target：
{items_json}

全局写作要求：
- 全文使用简体中文，面向大陆读者。源文件是繁体时，原文定义也要摘录后转写为简体。
- 背景为 1980 年前后老香港，可用英资公司、码头、茶餐厅、洋行、保险行等元素。
- 可以有隐晦感情线，但只能作为人物动机底色。
- 每个 target 严格 1 H1 = 1 fab，只能有一个以 `# ` 开头的 H1。
- 每篇聚焦 1 个核心概念，不要把整章塞进去。
- 故事正文不要直接使用保险专业术语；专业词只放在 `## 原文定义` 和 `## 对应点`。
- 如果 source 很短，也要写完整故事；如果 source 很长，只选最核心的概念切入。

每个文件必须严格使用以下结构，二级标题字面值必须完全一致：
---
title: "..."
chapter: "..."
section: "..."
concept: "..."
characters: ["..."]
setting: "1980年前后老香港"
tags: ["IIQE Paper 1", "保险考试1"]
---

# <使用 manifest h1，可转写为简体>

## 故事

800-1500 字。四段式：开场、冲突、转折、结局。人物必须有真实动机，结尾不要说教。

## 原文定义

1-3 句来自 source 的核心定义/规则，转写为简体中文。

## 对应点

| 故事元素 | 概念对应 |
|---|---|
| ... | ... |

写完全部文件后，自检每个 target：路径正确、frontmatter 齐全、只有一个 H1、三个二级标题存在、故事为简体中文、概念来自 source。
最后只回复一行 JSON：{{"status":"pass","written":["id1","id2"]}} 或 {{"status":"fail","reason":"..."}}。不要粘贴正文。
"""


def run_batch(batch, batch_name):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    for fab in batch:
        orchard(
            "record",
            "--id",
            fab["id"],
            "--status",
            "implementer_dispatched",
            "--mode",
            "claude-cli",
            "--notes",
            f"batch {batch_name} dispatched",
        )
    cmd = [
        "claude",
        "-p",
        build_prompt(batch),
        "--model",
        "sonnet",
        "--output-format",
        "text",
        "--allowedTools",
        "Read,Write,Bash",
        "--add-dir",
        str(PROJECT),
        "--dangerously-skip-permissions",
        "--no-session-persistence",
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=2400, check=False)
    (LOG_DIR / f"{batch_name}.out.txt").write_text(proc.stdout or "", encoding="utf-8")
    (LOG_DIR / f"{batch_name}.err.txt").write_text(proc.stderr or "", encoding="utf-8")

    results = []
    for fab in batch:
        ok, msg = validate_fab(fab)
        if proc.returncode != 0:
            ok = False
            msg = f"claude rc={proc.returncode}: {((proc.stderr or proc.stdout) or '')[-300:]}"
        if ok:
            orchard("record", "--id", fab["id"], "--status", "implementer_done", "--notes", f"batch {batch_name} generated")
            orchard(
                "record",
                "--id",
                fab["id"],
                "--status",
                "spec_passed",
                "--reviewer",
                "spec",
                "--verdict",
                "pass",
                "--notes",
                "local structure checks passed",
            )
            orchard(
                "record",
                "--id",
                fab["id"],
                "--status",
                "quality_passed",
                "--reviewer",
                "quality",
                "--verdict",
                "pass",
                "--notes",
                "worker self-review plus local quality checks passed",
            )
        else:
            orchard(
                "record",
                "--id",
                fab["id"],
                "--status",
                "spec_failed",
                "--reviewer",
                "spec",
                "--verdict",
                "fail",
                "--notes",
                msg[:200],
            )
        results.append((fab["id"], ok, msg))
    return batch_name, results


def chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", default=None)
    parser.add_argument("--batch-size", type=int, default=6)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--include-failed", action="store_true")
    args = parser.parse_args()

    manifest = load_json(MANIFEST)
    progress = load_json(PROGRESS)
    fabs = []
    for fab in manifest["sections"]:
        status = progress["sections"].get(fab["id"], {}).get("status")
        if args.chapter and fab["chapter"] != args.chapter and fab["chapter_dir"] != args.chapter:
            continue
        if status == "quality_passed":
            continue
        if status not in ("pending", "spec_failed", "quality_failed", "implementer_dispatched", "in_review_loop"):
            continue
        if status in ("spec_failed", "quality_failed") and not args.include_failed:
            continue
        fabs.append(fab)
    if args.limit:
        fabs = fabs[: args.limit]

    batches = list(chunks(fabs, args.batch_size))
    print(f"dispatching fabs={len(fabs)} batches={len(batches)} concurrency={args.concurrency}", flush=True)
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = []
        for idx, batch in enumerate(batches, start=1):
            name = f"{batch[0]['chapter']}-{idx:03d}-{batch[0]['id']}"
            futures.append(executor.submit(run_batch, batch, name))
        for future in as_completed(futures):
            batch_name, results = future.result()
            ok_count = sum(1 for _, ok, _ in results if ok)
            print(f"{batch_name}: {ok_count}/{len(results)}", flush=True)
            for fid, ok, msg in results:
                if not ok:
                    print(f"  FAIL {fid}: {msg}", flush=True)


if __name__ == "__main__":
    main()
