---
name: feishu-docs-list
description: "列出飞书文件夹下的文档。"
---

# 飞书文档列表

列出指定文件夹下的文档，或列出最近访问的文档。

## 用法

```bash
# 列出文件夹下的文件
python -X utf8 .claude/skills/feishu/docs/list/tool.py --folder-token "文件夹token"

# 列出根目录文件
python -X utf8 .claude/skills/feishu/docs/list/tool.py

# 限制返回数量
python -X utf8 .claude/skills/feishu/docs/list/tool.py --folder-token "xxx" --count 20
```

## 参数

- `--folder-token`（可选）：文件夹 token，留空列出根目录
- `--count`（可选）：返回数量，默认 20

## 返回格式

```
文件夹: fldcnXXX (共 5 项)
1. [文件夹] 项目文档 (token: fldcnYYY)
2. [docx] 需求文档 (token: doxcnZZZ)
3. [sheet] 数据统计 (token: shtcnAAA)
```
