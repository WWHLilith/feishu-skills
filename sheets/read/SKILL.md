---
name: feishu-sheets-read
description: "读取飞书电子表格数据。"
---

# 读取飞书电子表格

读取指定范围的表格数据。

## 用法

```bash
# 读取整个工作表
python -X utf8 .claude/skills/feishu/sheets/read/tool.py --token "表格token"

# 读取指定范围
python -X utf8 .claude/skills/feishu/sheets/read/tool.py --token "表格token" --range "Sheet1!A1:D10"

# 从 URL 读取
python -X utf8 .claude/skills/feishu/sheets/read/tool.py --url "https://xxx.feishu.cn/sheets/TOKEN"
```

## 参数

- `--token`：电子表格 token
- `--url`：飞书表格 URL（自动提取 token）
- `--range`（可选）：读取范围，格式 `工作表名!A1:D10`，留空读取第一个工作表全部数据

## 返回格式

表格数据以 TSV（制表符分隔）格式输出。
