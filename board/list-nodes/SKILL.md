---
name: feishu-board-list-nodes
description: "获取飞书画板中的所有节点。"
---

# 获取画板节点

获取指定画板中的所有节点信息。

## 用法

```bash
python -X utf8 .claude/skills/feishu/board/list-nodes/tool.py --whiteboard-id "VF5Bwo7Z5icC0bk8EWbb57Vbckh"
```

## 参数

- `--whiteboard-id`（必填）：画板唯一标识

## 返回格式

```
画板节点列表 (共 N 个节点)

1. [composite_shape] id=xxx (100x50 at 200,300)
   子类型: round_rect
   文字: "开始"
2. [connector] id=xxx
   连接: node1 -> node2
...
```
