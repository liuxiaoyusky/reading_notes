# TTS 寓言音频流水线

把 `04-基金从业/03-科目三-私募股权/converted/fables/` 下的 370 篇寓言批量转成中文 MP3，
可选再合并成一个长音频。

## 选型说明

| 选项 | 开源？ | 适合场景 | 备注 |
|---|---|---|---|
| **CosyVoice 2** (FunAudioLLM) | ✅ Apache 2.0 | 中文 + 声音克隆 + 情感 | **本流水线默认使用** |
| ChatTTS (2noise) | ✅ Apache 2.0 | 表情符号控制情感、长文本 | 备选 |
| Fish Speech | ✅ Apache 2.0 | 轻量、声音克隆 | 备选 |
| GPT-SoVITS | ✅ MIT | 社区最火、需 5–30s 参考音频 | 想克隆你/某人声音时切换 |
| 火山 wavtts / 豆包语音 | ❌ | 线上 API | 按字符计费，详见 `.learnings/LEARNINGS.md` |

> 备注：字节的 wavtts / Seed-TTS 没有开源权重，只能走 API；Miso One 未确认有公开开源版本。
> 本地跑 CosyVoice 2 一次性下完权重后就是"无限免费"。

## 前置依赖

- macOS（Apple Silicon 优先）或 Linux
- Python 3.10+
- `ffmpeg`、`ffprobe`（`brew install ffmpeg`）
- CosyVoice 服务跑在 `localhost:50000`

## 启动 CosyVoice（Docker 方式，最快）

```bash
# 1. 拉取镜像（含 CosyVoice2 0.5B 权重，预下载慢）
docker pull registry.cn-hangzhou.aliyuncs.com/funasr/funasr-runtime-sdk:cnserver-latest

# 2. 启动容器并把模型缓存目录挂载出来（避免每次重建都重新下载）
docker run -d --rm -p 50000:50000 \
    -v ~/.cache/modelscope:/root/.cache/modelscope \
    --name cosyvoice \
    registry.cn-hangzhou.aliyuncs.com/funasr/funasr-runtime-sdk:cnserver-latest

# 3. 进容器启动 CosyVoice2 服务
docker exec -it cosyvoice bash
cd /workspace/CosyVoice  # 或仓库里的实际路径
python webui.py --port 50000 --model_dir pretrained_models/CosyVoice2-0.5B
```

**替代**：用 ModelScope 直接下模型，本地起 `python webui.py`：

```bash
git clone https://github.com/FunAudioLLM/CosyVoice.git
cd CosyVoice
pip install -r requirements.txt
# 用 modelscope 下权重（约 2GB），首次会自动下载
python webui.py --port 50000 --model_dir pretrained_models/CosyVoice2-0.5B
```

## 跑流水线

```bash
# 1. 先试 1 篇验证链路（--limit 1）
python tools/tts/generate_fables.py \
    --fables-dir 04-基金从业/03-科目三-私募股权/converted/fables \
    --out-dir    04-基金从业/03-科目三-私募股权/converted/fables/audio \
    --speaker 中文女 \
    --limit 1

# 2. 听到效果满意后，跑完全部（370 篇），已生成的会自动跳过
python tools/tts/generate_fables.py \
    --fables-dir 04-基金从业/03-科目三-私募股权/converted/fables \
    --out-dir    04-基金从业/03-科目三-私募股权/converted/fables/audio \
    --speaker 中文女 \
    --skip-existing

# 3. 合并成一个长音频（约 30 小时 mp3，2.5GB 左右）
python tools/tts/concat_audio.py \
    --audio-dir 04-基金从业/03-科目三-私募股权/converted/fables/audio \
    --output    04-基金从业/03-科目三-私募股权/converted/fables/audio/all_fables.mp3
```

## 输出结构

```
04-基金从业/03-科目三-私募股权/converted/fables/audio/
├── 01-股权投资基金概述__...__01-...mp3
├── 02-...__...__02-...mp3
├── ...
├── all_fables.mp3              ← 合并后的长音频
└── manifest.json               ← 每篇的生成状态（ok / skipped / fail / empty）
```

## 常见问题

- **`requests.exceptions.ConnectionError`**：CosyVoice 服务没起来，或端口不是 50000。检查 `docker ps`。
- **生成单篇耗时太长**：默认串行。如果你的 Mac 有 GPU，可以改 `generate_fables.py` 用 `concurrent.futures.ThreadPoolExecutor` 并发。
- **想要你自己的声音**：把 CosyVoice 切到 `mode: zero_shot`，先在 `voices/` 录 5–10 秒参考音频上传。GPT-SoVITS 在克隆质量上通常更稳，是进阶选项。
- **想分章合并**：`concat_audio.py --pattern "01-*.mp3"` 即可按章名 glob。

## 已知未确认事项

- 字节豆包/火山 TTS 的最新单价（API 文档需要登录控制台查）
- "Miso One" 是否为某个 CosyVoice / ChatTTS 的音色变体（需要原始来源链接才能确认）
