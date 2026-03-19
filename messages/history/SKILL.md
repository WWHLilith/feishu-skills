---
name: feishu-messages-history
description: "读取飞书聊天记录 — 按用户名或 chat_id 获取对话历史消息。"
---

# 飞书聊天记录读取

读取与指定用户的单聊历史消息，或按 chat_id 读取任意会话消息。

## 用法

```bash
# 按用户名读取对话（自动搜索用户 + 查找单聊）
python -X utf8 .claude/skills/feishu/messages/history/tool.py --name "张三"

# 按 chat_id 直接读取
python -X utf8 .claude/skills/feishu/messages/history/tool.py --chat-id "oc_xxxxx"

# 限制消息条数
python -X utf8 .claude/skills/feishu/messages/history/tool.py --name "张三" --limit 20
```

## 参数

- `--name`：对方用户名（自动搜索并查找单聊，与 --chat-id 二选一）
- `--chat-id`：直接指定 chat_id（与 --name 二选一）
- `--limit`：获取消息条数，默认 50

## 实现原理

飞书 API 不支持直接列出单聊会话。使用 `--name` 时，工具会：
1. 搜索用户获取 open_id
2. 向该用户发送一条通知消息「Claude Agent 正在获取会话内容」，从响应中获取 chat_id（飞书官方推荐方式）
3. 使用 chat_id 读取消息历史

## 所需权限

- `contact:user:search` — 搜索用户
- `im:message` — 发送/删除临时消息（用于获取单聊 chat_id）
- `im:message:readonly` — 读取消息内容

## 返回格式

```
[03-19 14:30] [user:ou_abc1...]: 你好
[03-19 14:31] [user:ou_def2...]: 你好，有什么事吗？
[03-19 14:32] [user:ou_abc1...]: [图片]
```
