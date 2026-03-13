---
name: feishu-bitable-update
description: "更新飞书多维表格中的记录。"
---

# 更新多维表格记录

更新数据表中已有记录的字段。

## 用法

```bash
python -X utf8 .claude/skills/feishu/bitable/update/tool.py --app-token "bascnXXX" --table-id "tblXXX" --record-id "recXXX" --fields '{"状态":"已完成"}'
```

## 参数

- `--app-token`（必填）：多维表格 app_token
- `--table-id`（必填）：数据表 ID
- `--record-id`（必填）：记录 ID
- `--fields`（必填）：要更新的字段 JSON 对象
