---
name: feishu-messages-read
description: "读取飞书群聊消息，支持按群名搜索、列出加入的群、过滤自己的发言。"
---

# 飞书群聊消息读取

读取指定会话的消息记录，自动解析发送者姓名和 @mention。仅支持群聊（飞书隐私政策不开放私聊消息 API）。

## 用法

```bash
# 列出当前用户加入的所有会话（可按名称过滤）
python -X utf8 <skill目录>/tool.py list-chats [--query "关键词"]

# 读取群消息（按 chat_id）
python -X utf8 <skill目录>/tool.py read --chat-id <chat_id> [--count 50] [--mine]

# 读取群消息（按群名自动查找 chat_id）
python -X utf8 <skill目录>/tool.py read --chat-name "群名关键词" [--count 50] [--mine]
```

## 参数

### list-chats
- `--query`：按群名过滤，留空列出所有群

### read
- `--chat-id`：群的 chat_id（与 `--chat-name` 二选一）
- `--chat-name`：按群名搜索，自动定位 chat_id
- `--count`：拉取消息数量，默认 50，最大 50
- `--mine`：只显示当前用户自己的发言

## 返回格式

```
[MM-DD HH:MM] 发送者姓名: 消息内容
```

- 富文本消息自动展开为可读文本
- 图片显示为 `[图片]`，表情显示为 `[表情名]`
- @mention 解析为真实姓名
- 系统消息（入群通知等）保留原始格式
- bot 发送的卡片消息（sender 以 `cli_` 开头）保留原始 JSON

## 所需权限

需在飞书开放平台开启**机器人能力**，并授权以下 OAuth scope：
- `im:message:readonly`
- `im:chat:readonly`
- `im:message.group_msg:get_as_user`
- `contact:user.base:readonly`
