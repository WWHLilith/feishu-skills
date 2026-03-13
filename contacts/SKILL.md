---
name: feishu-contacts
description: "飞书通讯录 — 搜索用户、获取用户信息。"
---

# 飞书通讯录

搜索用户或获取用户详细信息。

## 用法

```bash
# 按名称搜索用户
python -X utf8 .claude/skills/feishu/contacts/tool.py --search "张三"

# 按 open_id 获取用户信息
python -X utf8 .claude/skills/feishu/contacts/tool.py --user-id "ou_xxxxx"

# 按邮箱查询
python -X utf8 .claude/skills/feishu/contacts/tool.py --email "zhangsan@company.com"
```

## 参数

- `--search`：按名称搜索用户
- `--user-id`：按 open_id 获取用户详情
- `--email`：按邮箱查询用户

三选一。

## 返回格式

```
1. 张三 (open_id: ou_xxx, 部门: 技术部)
```
