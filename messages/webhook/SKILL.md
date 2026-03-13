---
name: feishu-messages-webhook
description: "通过飞书自定义机器人 webhook 发送消息。"
---

# 飞书 Webhook 消息

通过群机器人 webhook URL 发送消息，无需应用权限。

## 用法

```bash
# 发送文本
python -X utf8 .claude/skills/feishu/messages/webhook/tool.py --url "https://open.feishu.cn/open-apis/bot/v2/hook/xxx" --text "通知内容"

# 发送富文本
python -X utf8 .claude/skills/feishu/messages/webhook/tool.py --url "https://open.feishu.cn/open-apis/bot/v2/hook/xxx" --rich '{"post":{"zh_cn":{"title":"标题","content":[[{"tag":"text","text":"内容"}]]}}}'
```

## 参数

- `--url`（必填）：webhook URL
- `--text`：纯文本消息（与 --rich 二选一）
- `--rich`：富文本 JSON（与 --text 二选一）
