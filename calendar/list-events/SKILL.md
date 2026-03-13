---
name: feishu-calendar-list-events
description: "查询飞书日历日程列表。"
---

# 查询飞书日程

查询指定时间范围内的日程。

## 用法

```bash
# 查询今天的日程
python -X utf8 .claude/skills/feishu/calendar/list-events/tool.py

# 查询指定日期范围
python -X utf8 .claude/skills/feishu/calendar/list-events/tool.py --start "2026-03-15" --end "2026-03-20"
```

## 参数

- `--start`（可选）：开始日期 `YYYY-MM-DD`，默认今天
- `--end`（可选）：结束日期 `YYYY-MM-DD`，默认 start + 1 天

## 返回格式

```
2026-03-15 的日程 (共 3 个):
1. 14:00-15:00 周会
2. 16:00-17:00 评审会议
```
