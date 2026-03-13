---
name: feishu-approval-query
description: "查询飞书审批实例状态。"
---

# 查询飞书审批状态

查询审批实例的当前状态和详情。

## 用法

```bash
python -X utf8 .claude/skills/feishu/approval/query/tool.py --instance-code "xxx"
```

## 参数

- `--instance-code`（必填）：审批实例 code

## 返回格式

```
审批实例: xxx
状态: APPROVED
发起人: 张三
创建时间: 2026-03-13 14:00
```
