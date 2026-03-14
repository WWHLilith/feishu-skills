---
name: feishu-board-create-nodes
description: "在飞书画板中创建图形节点。"
---

# 创建画板节点

在指定画板中创建图形节点，支持批量创建和父子关系。

## 用法

```bash
# 创建单个矩形
python -X utf8 .claude/skills/feishu/board/create-nodes/tool.py --whiteboard-id "xxx" --nodes '[{"type":"composite_shape","composite_shape":{"type":"round_rect"},"x":100,"y":100,"width":160,"height":80,"text":{"text":"开始"}}]'

# 创建多个节点 + 连线
python -X utf8 .claude/skills/feishu/board/create-nodes/tool.py --whiteboard-id "xxx" --nodes '[
  {"id":"n1","type":"composite_shape","composite_shape":{"type":"round_rect"},"x":100,"y":100,"width":160,"height":80,"text":{"text":"步骤1"}},
  {"id":"n2","type":"composite_shape","composite_shape":{"type":"round_rect"},"x":100,"y":250,"width":160,"height":80,"text":{"text":"步骤2"}},
  {"type":"connector","connector":{"start":{"attached_object":{"id":"n1","snap_to":"bottom"}},"end":{"attached_object":{"id":"n2","snap_to":"top"}},"shape":"right_angled_polyline"}}
]'
```

## 参数

- `--whiteboard-id`（必填）：画板唯一标识
- `--nodes`（必填）：节点 JSON 数组

## 支持的节点类型

- `composite_shape` — 基础图形（round_rect, diamond, ellipse, rect, flow_chart_round_rect 等）
- `text_shape` — 纯文字
- `connector` — 连线
- `section` — 分区
- `table` — 表格
- `sticky_note` — 便签
- `mind_map` — 思维导图
- `image` — 图片

## 返回格式

```
创建成功，共 N 个节点
1. id=xxx (type=composite_shape)
```
