---
name: feishu-sheets-create
description: "创建飞书电子表格。"
---

# 创建飞书电子表格

创建一个新的电子表格。

## 用法

```bash
python -X utf8 .claude/skills/feishu/sheets/create/tool.py --title "表格标题" [--folder-token "文件夹token"]
```

## 参数

- `--title`（必填）：表格标题
- `--folder-token`（可选）：目标文件夹 token，留空创建在根目录

## 返回格式

```
表格创建成功
标题: xxx
Token: shtcnXXX
链接: https://xxx.feishu.cn/sheets/...
```
