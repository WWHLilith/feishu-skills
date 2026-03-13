---
name: feishu-bitable-create
description: "在飞书多维表格中创建新记录。"
---

# 创建多维表格记录

向数据表中插入新记录。

## 用法

```bash
python -X utf8 .claude/skills/feishu/bitable/create/tool.py --app-token "bascnXXX" --table-id "tblXXX" --fields '{"名称":"示例","状态":"待处理"}'
```

## 参数

- `--app-token`（必填）：多维表格 app_token
- `--table-id`（必填）：数据表 ID
- `--fields`（必填）：记录字段 JSON 对象
