---
name: feishu-sheets-write
description: "写入数据到飞书电子表格。"
---

# 写入飞书电子表格

向指定范围写入数据。

## 用法

```bash
# 写入数据（JSON 二维数组）
python -X utf8 .claude/skills/feishu/sheets/write/tool.py --token "表格token" --range "Sheet1!A1:B2" --values '[["姓名","分数"],["张三",95]]'
```

## 参数

- `--token`（必填）：电子表格 token
- `--range`（必填）：写入范围，格式 `工作表名!A1:B2` 或 `sheet_id!A1:B2`
- `--values`（必填）：JSON 格式的二维数组

## 返回格式

```
写入成功：范围 Sheet1!A1:B2，更新 4 个单元格
```
