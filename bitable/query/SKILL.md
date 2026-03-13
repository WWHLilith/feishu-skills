---
name: feishu-bitable-query
description: "查询飞书多维表格记录。"
---

# 查询飞书多维表格

查询多维表格中的记录。

## 用法

```bash
# 查询所有记录
python -X utf8 .claude/skills/feishu/bitable/query/tool.py --app-token "bascnXXX" --table-id "tblXXX"

# 带筛选条件查询
python -X utf8 .claude/skills/feishu/bitable/query/tool.py --app-token "bascnXXX" --table-id "tblXXX" --filter 'AND(CurrentValue.[状态]="进行中")'

# 从 URL 查询（自动提取 app_token）
python -X utf8 .claude/skills/feishu/bitable/query/tool.py --url "https://xxx.feishu.cn/base/XXX" --table-id "tblXXX"

# 列出数据表
python -X utf8 .claude/skills/feishu/bitable/query/tool.py --app-token "bascnXXX" --list-tables
```

## 参数

- `--app-token` 或 `--url`（必填）：多维表格标识
- `--table-id`：数据表 ID（与 --list-tables 二选一）
- `--list-tables`：列出所有数据表
- `--filter`（可选）：筛选条件表达式
- `--count`（可选）：返回数量，默认 20
