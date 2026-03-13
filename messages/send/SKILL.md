---
name: feishu-messages-send
description: "通过飞书 API 发送消息给用户或群组。"
---

# 飞书发送消息

通过应用身份发送消息。

## 用法

```bash
# 发送文本消息给用户（通过 open_id）
python -X utf8 .claude/skills/feishu/messages/send/tool.py --to "ou_xxxxx" --type open_id --text "你好"

# 发送文本消息到群（通过 chat_id）
python -X utf8 .claude/skills/feishu/messages/send/tool.py --to "oc_xxxxx" --type chat_id --text "通知内容"

# 发送富文本（JSON 格式）
python -X utf8 .claude/skills/feishu/messages/send/tool.py --to "ou_xxx" --type open_id --rich '{"zh_cn":{"title":"标题","content":[[{"tag":"text","text":"内容"}]]}}'
```

## 参数

- `--to`（必填）：接收方 ID
- `--type`（必填）：ID 类型，可选 `open_id`、`user_id`、`email`、`chat_id`
- `--text`：纯文本消息内容（与 --rich 二选一）
- `--rich`：富文本 JSON（与 --text 二选一）

## 返回格式

```
消息发送成功 (message_id: om_xxx)
```
