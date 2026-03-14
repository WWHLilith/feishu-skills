---
name: feishu-board-delete-nodes
description: "删除飞书画板中的节点。"
---

# 删除画板节点

删除指定画板中的一个或多个节点。

## 用法

```bash
# 删除单个节点
python -X utf8 .claude/skills/feishu/board/delete-nodes/tool.py --whiteboard-id "xxx" --node-ids "node_id_1"

# 删除多个节点（逗号分隔）
python -X utf8 .claude/skills/feishu/board/delete-nodes/tool.py --whiteboard-id "xxx" --node-ids "node_id_1,node_id_2,node_id_3"
```

## 参数

- `--whiteboard-id`（必填）：画板唯一标识
- `--node-ids`（必填）：要删除的节点 ID，多个用逗号分隔

## 返回格式

```
删除成功，共删除 N 个节点
```
