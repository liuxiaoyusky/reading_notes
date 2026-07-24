#!/usr/bin/env python3
"""
把 generate_fables.py 输出的全部 mp3 合并成一个（或几个）长音频。

用法：
    python concat_audio.py \
        --audio-dir /path/to/fables/audio \
        --output all_fables.mp3

实现要点：
- 使用 ffmpeg concat demuxer（无重编码），速度快、零损
- 自动分块（每块最多 100 个文件）避免 ffmpeg 命令行超长
- 用 ffprobe 校验每个输入文件参数一致（采样率/声道/编码），不一致会告警但不阻塞
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def ffprobe_info(path: Path) -> dict:
    cmd = ["ffprobe", "-v", "error", "-select_streams", "a:0",
           "-show_entries", "stream=codec_name,sample_rate,channels,bit_rate",
           "-of", "json", str(path)]
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    info = json.loads(r.stdout)["streams"][0]
    return {
        "codec": info.get("codec_name"),
        "sample_rate": info.get("sample_rate"),
        "channels": info.get("channels"),
        "bit_rate": info.get("bit_rate"),
    }


def concat_block(mp3s: list[Path], out_path: Path) -> None:
    """concat 一个块：先把所有路径写进 list 文件，再 ffmpeg concat。"""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        list_file = Path(f.name)
        for p in mp3s:
            # 注意 ffmpeg concat demuxer 要求文件路径无单引号，或用 file '...'
            safe = str(p.absolute()).replace("'", "'\\''")
            f.write(f"file '{safe}'\n")
    try:
        cmd = ["ffmpeg", "-y", "-loglevel", "error",
               "-f", "concat", "-safe", "0",
               "-i", str(list_file),
               "-c", "copy", str(out_path)]
        subprocess.run(cmd, check=True)
    finally:
        list_file.unlink(missing_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio-dir", required=True, type=Path,
                    help="含 mp3 的目录（递归）")
    ap.add_argument("--output", required=True, type=Path,
                    help="合并后的 mp3 路径")
    ap.add_argument("--chunk-size", type=int, default=100,
                    help="每块最多包含的 mp3 数（默认 100）")
    ap.add_argument("--pattern", default="*.mp3",
                    help="glob 模式（默认 *.mp3；想排除 manifest 时可写 !manifest.json）")
    args = ap.parse_args()

    audio_dir: Path = args.audio_dir
    mp3s = sorted(p for p in audio_dir.rglob(args.pattern) if p.is_file())
    if not mp3s:
        print(f"[ERR] 在 {audio_dir} 下没找到 mp3", file=sys.stderr)
        return 1
    print(f"[INFO] 共 {len(mp3s)} 个 mp3，总大小 "
          f"{sum(p.stat().st_size for p in mp3s) / (1024**2):.1f} MB")

    # 校验参数一致性（不一致只警告，不阻断——ffmpeg concat 会自动重采样）
    params_set = set()
    for p in mp3s:
        try:
            params_set.add(json.dumps(ffprobe_info(p), sort_keys=True))
        except Exception as e:  # noqa: BLE001
            print(f"[WARN] ffprobe 失败: {p}: {e}", file=sys.stderr)
    if len(params_set) > 1:
        print(f"[WARN] 发现 {len(params_set)} 种不同音频参数，ffmpeg 会自动重采样",
              file=sys.stderr)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if len(mp3s) <= args.chunk_size:
        concat_block(mp3s, args.output)
        print(f"[DONE] 单块 concat → {args.output} "
              f"({args.output.stat().st_size / (1024**2):.1f} MB)")
        return 0

    # 多块：先 concat 各块到 _chunk_N.mp3，再 concat 这些块
    with tempfile.TemporaryDirectory() as tmpd:
        tmpd = Path(tmpd)
        chunk_files = []
        for i in range(0, len(mp3s), args.chunk_size):
            chunk = mp3s[i : i + args.chunk_size]
            out = tmpd / f"_chunk_{i // args.chunk_size:03d}.mp3"
            concat_block(chunk, out)
            chunk_files.append(out)
            print(f"[INFO] chunk {i // args.chunk_size} → {out.name} "
                  f"({len(chunk)} files, {out.stat().st_size / (1024**2):.1f} MB)")
        concat_block(chunk_files, args.output)
        print(f"[DONE] 多块 concat → {args.output} "
              f"({args.output.stat().st_size / (1024**2):.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
