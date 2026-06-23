# 02-iique · 香港保险业中介人资格考试 (IIQE) 研習資料手冊

香港保险业中介人资格考试(IIQE)共 5 张卷,每卷一本 VTC(职业训练局)出版的研习资料手册。本目录收纳 5 本手册的完整 Markdown 解析。

## 5 卷汇总

| 卷 | 主题 | 出版年份 | 章/节 | 解析结果 |
|----|------|---------|-------|---------|
| Paper 1 | 保險原理及實務 | VTC 2021 版本 | 7 章 113 节 | [paper-1/](paper-1/) |
| Paper 2 | 一般保險 | VTC 2022 版本(2023 年 11 月勘误) | 3 章 53 节 | [paper-2/](paper-2/) |
| Paper 3 | 長期保險 | VTC 2022 版本 | 5 章 57 节 | [paper-3/](paper-3/) |
| Paper 4 | 強積金 | VTC 2019 年 9 月版本(第九版) | 7 章 102 节 | [paper-4/](paper-4/) |
| Paper 5 | 投資相連長期保險 | VTC 2024 版本 | 5 章 123 节 | [paper-5/](paper-5/) |

## 各卷子目录结构(统一规范)

```
paper-N/
├── sources/
│   └── 0N.PaperN研习资料手册.pdf    # symlink 到 repo 顶层原始 PDF
├── converted/
│   ├── content_list.json             # MinerU 结构化块
│   ├── raw.md                        # MinerU 解析的纯 markdown(整本)
│   ├── images/                       # 抽出的图(29 张左右)
│   └── sections/                     # 按章节切分的 markdown
│       ├── 01-<章名>/
│       │   ├── 00_index.md           # 章节目录
│       │   ├── a-NN-NN-<节名>.md     # 各节内容(ASCII 前缀保证排序)
│       │   └── ...
│       └── 02-...
├── index.md                          # 章节目录(跳转到各节)
├── progress.md                       # 学习进度(二态勾选)
└── README.md                         # 学习指引
```

## 解析流程

1. **MinerU Phase 1**: 提交 PDF 到 `http://10.1.9.133:9987/file_parse` (async)
2. **Phase 2**: 同步 polling `/tasks/{task_id}/result`,保存 `content_list.json` + `raw.md` + `images/`
3. **Phase 3**: 不需要 fix_section_titles(MinerU hybrid-engine 模式没切 title blocks,改用 raw.md 切分)
4. **Phase 4 (custom)**: `split_iique.py` — 基于 raw.md 的 `## N` / `## N.M` 标题切分章节
5. **Phase 5**: `generate_scaffold.py` 生成 `index.md` / `progress.md` / `README.md`
6. **Phase 6**: `validate.py` 校验(图片引用、节数等)— 可选

## 学习方式

- 每卷独立学习,按章节循序渐进
- AI Q&A 用法:用 `converted/sections/<章>/<节>.md` 作为上下文,提问概念/案例/计算
- 进度追踪:完成一节在 `progress.md` 中勾选 `[x]`

## 转换工具

- MinerU 服务: `http://10.1.9.133:9987` (内网)
- pdf-to-study-program skill: `~/.claude/skills/pdf-to-study-program/`
- 自定义切分脚本: `/tmp/split_iique.py`
- 任务提交+结果拉取: `/tmp/fetch_result.py`

## 已知问题与限制

- **章节标题依赖 raw.md 识别**:MinerU hybrid-engine 模式没识别 `title` block,所以分章只能靠 raw.md 的 `## N` 标题。如果原文 PDF 的章节标题本身不规范,可能漏切。
- **题目/表格混入章节**:部分章节内的"## 3 以下哪兩項..."会被误识别为新章节标题,目前的启发式过滤(标题里含 `?`/`?` 或超过 35 字符)能过滤大部分。
- **章节顺序**:文件名用 `a-NN-NN-...` 前缀(ASCII 字符在前)保证 sort order 与 sec_full 一致。
