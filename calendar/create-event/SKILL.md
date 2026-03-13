---
name: feishu-calendar-create-event
description: "创建飞书日历日程。"
---

# 创建飞书日程

在主日历上创建日程事件。

## 用法

```bash
python -X utf8 .claude/skills/feishu/calendar/create-event/tool.py --summary "会议标题" --start "2026-03-15 14:00" --end "2026-03-15 15:00" [--description "会议说明"]
```

## 参数

- `--summary`（必填）：日程标题
- `--start`（必填）：开始时间，格式 `YYYY-MM-DD HH:MM`
- `--end`（必填）：结束时间，格式 `YYYY-MM-DD HH:MM`
- `--description`（可选）：日程描述
- `--attendees`（可选）：参与者 open_id，逗号分隔

## 返回格式

```
日程创建成功
标题: xxx
时间: 2026-03-15 14:00 ~ 15:00
事件ID: xxx
```
