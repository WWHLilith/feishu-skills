---
name: feishu-messages
description: "飞书消息操作 — 发送消息、webhook 通知。"
---

# 飞书消息操作

读取对应子目录的 SKILL.md 获取具体用法：

- **send/** — 通过 API 发送消息给用户或群组
- **webhook/** — 通过自定义机器人 webhook 发送消息

## 说明
- `send/` 需要应用有 `im:message` 权限，支持发送给指定用户或群
- `webhook/` 不需要应用权限，只需要群机器人的 webhook URL
