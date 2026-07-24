#!/usr/bin/env python3
"""
遍历科目三寓言目录，调用本地 CosyVoice HTTP 服务生成 MP3 音频。

依赖：requests、ffmpeg（PATH 中）

CosyVoice 启动方式（Docker）：
    docker run -d --rm -p 50000:50000 \
        -v ~/.cache/modelscope:/root/.cache/modelscope \
        --name cosyvoice \
        registry.cn-hangzhou.aliyuncs.com/funasr/funasr-runtime-sdk:cnserver-latest
    # 然后在容器内跑 CosyVoice2 服务，监听 50000 端口（参考 funaudioLLM/CosyVoice README）
    # 容器外 API 入口：http://localhost:50000/inference

更简单的备用（推荐先用这个，跑通再换 Docker）：
    git clone https://github.com/FunAudioLLM/CosyVoice.git
    cd CosyVoice && pip install -r requirements.txt
    python webui.py --port 50000 --model_dir pretrained_models/CosyVoice2-0.5B
    # 然后本脚本访问 http://localhost:50000/inference
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable

import requests

# 寓言 markdown 的"故事正文"分隔符。
# 文件结构：# 标题 → ## 🏺 寓言故事 —— 《...》 → 故事段 → --- → **📖 原文定义** → ...
# 抽取 --- 之前、## 寓言故事标题 之后的所有内容。
STORY_HEADER = re.compile(r"^##\s*🏺\s*寓言故事.*?$", re.MULTILINE)
SEPARATOR = re.compile(r"^---\s*$", re.MULTILINE)


def extract_story(md_text: str) -> str:
    """从单篇寓言 markdown 抽取出供 TTS 朗读的纯故事正文（去掉标题、对应点表格、来源）。"""
    m = STORY_HEADER.search(md_text)
    if not m:
        return ""
    after_header = md_text[m.end():]
    sep = SEPARATOR.search(after_header)
    if sep:
        return after_header[:sep.start()].strip()
    return after_header.strip()


def iter_fable_files(fables_dir: Path) -> Iterable[Path]:
    """按编号顺序遍历所有寓言 .md（编号前缀 01-, 02-, ... 保证字典序即顺序）。"""
    return sorted(fables_dir.rglob("*.md"))


def safe_mp3_name(md_path: Path) -> str:
    """把章/节/编号-标题.md 拼成扁平且不冲突的 mp3 文件名。"""
    # 路径形如：04-.../03-募集与设立流程/28-1.备案要求.md
    parts = md_path.relative_to(md_path.parents[2]).with_suffix("").as_posix()
    # 把 / 换成 _，把 "28-1." 这类编号前缀保留
    return parts.replace("/", "__") + ".mp3"


def wav_to_mp3(wav_path: Path, mp3_path: Path, bitrate: str = "192k") -> None:
    """用 ffmpeg 把 wav 转成 mp3（CBR 192kbps by default）。"""
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(wav_path),
        "-codec:a", "libmp3lame", "-b:a", bitrate,
        str(mp3_path),
    ]
    subprocess.run(cmd, check=True)


def call_cosyvoice(text: str, speaker: str, host: str, timeout: int = 120) -> bytes:
    """
    调用 CosyVoice 推理接口。不同部署版本的 payload 字段名略有不同，
    这里用最常见的 /inference 端点 + sft 模式（用预置 speaker）。
    实际字段请按你部署的 CosyVoice 版本（v1/v2）调整。
    """
    url = f"{host.rstrip('/')}/inference"
    payload = {
        "tts_text": text,
        "spk": speaker,            # 预置音色 id，如 "中文女" / "中文男"
        "mode": "sft",             # sft = 预置音色；zero_shot = 声音克隆
        "speed": 1.0,
    }
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    # CosyVoice 推理默认返回 wav 二进制（或 JSON 包装的 base64，按部署版而定）
    return r.content


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fables-dir", required=True, type=Path,
                    help="04-基金从业/03-科目三-私募股权/converted/fables")
    ap.add_argument("--out-dir", required=True, type=Path,
                    help="音频输出目录")
    ap.add_argument("--host", default="http://localhost:50000",
                    help="CosyVoice HTTP 服务地址")
    ap.add_argument("--speaker", default="中文女",
                    help="预置音色名（参考 CosyVoice webui 列表）")
    ap.add_argument("--bitrate", default="192k", help="MP3 码率")
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 篇（调试用）")
    ap.add_argument("--skip-existing", action="store_true",
                    help="已存在目标 mp3 则跳过")
    args = ap.parse_args()

    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = out_dir / "_wav_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    files = list(iter_fable_files(args.fables_dir))
    if args.limit:
        files = files[: args.limit]
    print(f"[INFO] 共 {len(files)} 篇寓言待处理")

    manifest = []
    for i, md_path in enumerate(files, 1):
        rel = md_path.relative_to(args.fables_dir)
        mp3_path = out_dir / safe_mp3_name(md_path)

        if args.skip_existing and mp3_path.exists():
            print(f"[{i}/{len(files)}] SKIP {rel}")
            manifest.append({"src": str(rel), "mp3": str(mp3_path.relative_to(out_dir)),
                             "status": "skipped"})
            continue

        text = extract_story(md_path.read_text(encoding="utf-8"))
        if not text:
            print(f"[{i}/{len(files)}] EMPTY {rel}")
            manifest.append({"src": str(rel), "status": "empty"})
            continue

        wav_path = tmp_dir / (mp3_path.stem + ".wav")
        t0 = time.time()
        try:
            wav_bytes = call_cosyvoice(text, args.speaker, args.host)
            wav_path.write_bytes(wav_bytes)
            wav_to_mp3(wav_path, mp3_path, args.bitrate)
            wav_path.unlink(missing_ok=True)
            dt = time.time() - t0
            print(f"[{i}/{len(files)}] OK   {rel}  ({dt:.1f}s, {mp3_path.stat().st_size//1024}KB)")
            manifest.append({"src": str(rel), "mp3": str(mp3_path.relative_to(out_dir)),
                             "status": "ok", "seconds": round(dt, 1)})
        except Exception as e:  # noqa: BLE001
            print(f"[{i}/{len(files)}] FAIL {rel}: {e}", file=sys.stderr)
            manifest.append({"src": str(rel), "status": "fail", "error": str(e)})

    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[DONE] manifest → {out_dir / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
