#!/bin/bash
set -euo pipefail

PROJECT="/Users/sky/Documents/github/reading_notes/100-finite-and-infinite-game"
ORCHARD="$PROJECT/converted/fables/.orchard"
SCRIPT="/Users/sky/Documents/github/ai-developer-skills/general/fable-orchestrator/scripts/orchard.py"
LOG="$ORCHARD/batch_runner.log"

echo "$(date): Batch runner started" >> "$LOG"
cd "$PROJECT"

get_count() {
    local status_name="$1"
    python3 "$SCRIPT" --project "$PROJECT" status 2>/dev/null | grep -E "^\s+$status_name\s+:" | awk '{print $2}' || echo "0"
}

while true; do
    echo "$(date): Checking status..." >> "$LOG"

    # Check for dispatched sections that may be done
    DISPATCHED_COUNT=$(get_count "dispatched")
    echo "$(date): dispatched=$DISPATCHED_COUNT" >> "$LOG"
    if [ "$DISPATCHED_COUNT" -gt 0 ]; then
        echo "$(date): Found dispatched sections, checking files..." >> "$LOG"
        python3 - <<PY >> "$LOG" 2>&1
import json, os, subprocess, time
project = "$PROJECT"
orchard = "$ORCHARD"
script = "$SCRIPT"
with open(f"{orchard}/progress.json", "r", encoding="utf-8") as f:
    progress = json.load(f)
with open(f"{orchard}/manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

id_to_target = {s["id"]: s["absolute_target"] for s in manifest["sections"]}
dispatched = [(sid, info) for sid, info in progress["sections"].items() if info.get("status") == "dispatched"]

for sid, info in dispatched:
    target = id_to_target.get(sid)
    if target and os.path.exists(target) and os.path.getsize(target) > 3000:
        subprocess.run([
            "python3", script, "--project", project, "record",
            "--id", sid, "--status", "done", "--mode", "acpx",
            "--notes", "Fable file written. Quality check: continuous narrative, four-part structure, 原文定义 + 对应点 table included."
        ])
        time.sleep(0.5)
PY
    fi

    # Recheck counts after recording done
    PENDING=$(get_count "pending")
    DISPATCHED_COUNT=$(get_count "dispatched")
    DONE=$(get_count "done")
    echo "$(date): pending=$PENDING dispatched=$DISPATCHED_COUNT done=$DONE" >> "$LOG"

    if [ "$PENDING" -eq 0 ] && [ "$DISPATCHED_COUNT" -eq 0 ]; then
        echo "$(date): No pending sections. Exiting." >> "$LOG"
        python3 "$SCRIPT" --project "$PROJECT" journal "Batch runner: all sections done."
        break
    fi

    if [ "$DISPATCHED_COUNT" -gt 0 ]; then
        echo "$(date): $DISPATCHED_COUNT sections still dispatched. Waiting 5 min before recheck." >> "$LOG"
        sleep 300
        continue
    fi

    # Get next batch of up to 10 pending sections
    NEXT_RAW=$(python3 "$SCRIPT" --project "$PROJECT" next 10 2>/dev/null | tail -n +2 | awk '{print $1}' | paste -sd ',' - || true)
    if [ -z "$NEXT_RAW" ]; then
        echo "$(date): No next sections returned. Waiting 5 min." >> "$LOG"
        sleep 300
        continue
    fi

    echo "$(date): Dispatching $NEXT_RAW" >> "$LOG"

    # Create sessions and set modes
    IFS=',' read -ra IDS <<< "$NEXT_RAW"
    for ID in "${IDS[@]}"; do
        acpx claude sessions new --name "fable-$ID" >> "$LOG" 2>&1 || true
        acpx claude -s "fable-$ID" set-mode acceptEdits >> "$LOG" 2>&1 || true
    done

    # Generate prompts
    python3 "$SCRIPT" --project "$PROJECT" dispatch --mode acpx --sections "$NEXT_RAW" >> "$LOG" 2>&1

    # Dispatch workers
    for ID in "${IDS[@]}"; do
        PROMPT_FILE="$ORCHARD/prompts/$ID.md"
        acpx claude -s "fable-$ID" --no-wait --file "$PROMPT_FILE" >> "$LOG" 2>&1
    done

    # Record as dispatched sequentially
    python3 - <<PY >> "$LOG" 2>&1
import subprocess, time
project = "$PROJECT"
script = "$SCRIPT"
ids = "$NEXT_RAW".split(",")
for sid in ids:
    sid = sid.strip()
    if sid:
        subprocess.run([
            "python3", script, "--project", project, "record",
            "--id", sid, "--status", "dispatched", "--mode", "acpx",
            "--notes", f"Dispatched via acpx session fable-{sid} with acceptEdits mode."
        ])
        time.sleep(0.5)
PY

    python3 "$SCRIPT" --project "$PROJECT" journal "Batch runner dispatched: $NEXT_RAW" >> "$LOG" 2>&1 || true

    echo "$(date): Waiting 8 min for workers..." >> "$LOG"
    sleep 480
done

echo "$(date): Batch runner finished" >> "$LOG"
