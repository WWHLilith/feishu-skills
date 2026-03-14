---
name: feishu-board-update-nodes
description: "更新飞书画板中已有节点的属性。"
---

# 更新画板节点

更新指定画板中已有节点的位置、大小、文字、样式等属性。

## 用法

```bash
# 更新节点文字和位置
python -X utf8 .claude/skills/feishu/board/update-nodes/tool.py --whiteboard-id "xxx" --nodes '[{"id":"existing_node_id","x":200,"y":300,"text":{"text":"新文字"}}]'

# 更新节点样式
python -X utf8 .claude/skills/feishu/board/update-nodes/tool.py --whiteboard-id "xxx" --nodes '[{"id":"node_id","style":{"fill_color":"#fee3e2","border_style":"dash"}}]'
```

## 参数

- `--whiteboard-id`（必填）：画板唯一标识
- `--nodes`（必填）：要更新的节点 JSON 数组，每个节点必须包含 `id` 字段

## 可更新属性

- `x`, `y` — 位置
- `width`, `height` — 大小
- `angle` — 旋转角度
- `text` — 文字内容和样式
- `style` — 填充颜色、边框样式等
- `locked` — 是否锁定

## 返回格式

```
更新成功，共 N 个节点
1. id=xxx (type=composite_shape)
```
