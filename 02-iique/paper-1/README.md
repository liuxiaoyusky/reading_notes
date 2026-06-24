# IIQE Paper 1 / 保险考试1 — 学习项目

## 目录结构

```
.
├── index.md              # 总目录（跳转入口）
├── progress.md           # 学习进度（二态勾选）
├── converted/            # MinerU 解析结果
│   ├── content_list.json
│   ├── raw.md
│   └── images/
└── converted/sections/   # 拆分后的章节
    └── 01-<章名>/
        ├── 00_index.md
        └── 01-<节名>.md
```

## 如何使用

### 与 AI 一起学习

1. **选一节**：打开 `progress.md`，找一节未勾选的
2. **提问**：对 AI 说"读一下 `converted/sections/第N章/第M节.md`，然后帮我..."
3. **记笔记**：AI 的回答会自动追加到 `notes.md`
4. **标记完成**：对 AI 说"我完成了第N章第M节"，AI 会帮你勾选

### 快速跳转

- 总目录：[index.md](index.md)
- 学习进度：[progress.md](progress.md)

## 注意事项

- 不要修改 `converted/` 下的原始文件
- `converted/sections/` 下的 `.md` 是学习的最小单元
- 图片保存在 `converted/images/`，请勿移动
