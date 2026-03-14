---
name: feishu-board
description: "飞书画板操作：查看/创建/更新/删除节点、导入 PlantUML 图表。"
---

# 飞书画板

操作飞书画板（Whiteboard），支持节点的增删改查和图表导入。

## 子功能

| 操作 | 子目录 | 说明 |
|------|--------|------|
| 查看节点 | `list-nodes/` | 获取画板中的所有节点 |
| 创建节点 | `create-nodes/` | 创建图形节点（矩形、连线、文字等） |
| 更新节点 | `update-nodes/` | 更新节点的位置、文字、样式等 |
| 删除节点 | `delete-nodes/` | 删除画板中的节点（实验性，API 可能不生效） |
| 导入 PlantUML | `plantuml/` | 将 PlantUML 代码导入画板 |

## 关键概念

- **whiteboard_id**：画板唯一标识。获取方式：通过文档 block 列表接口，`block_type=43` 的 block 的 `token` 即为 `whiteboard_id`
- **节点类型**：`composite_shape`（基础图形）、`text_shape`（文字）、`connector`（连线）、`section`（分区）、`table`（表格）、`mind_map`（思维导图）、`sticky_note`（便签）等
- **基础图形子类型**：`round_rect`、`diamond`、`ellipse`、`rect`、`flow_chart_round_rect` 等

## 权限

| 操作 | 所需 scope |
|------|-----------|
| 查看节点/主题 | `board:whiteboard:node:read` |
| 创建节点/导入图表 | `board:whiteboard:node:create` |
| 更新节点 | `board:whiteboard:node:update` |
| 删除节点 | `board:whiteboard:node:delete` |
