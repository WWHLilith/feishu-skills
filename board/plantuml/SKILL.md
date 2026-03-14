---
name: feishu-board-plantuml
description: "将 PlantUML 图表代码导入飞书画板。"
---

# 导入 PlantUML 图表

将 PlantUML 代码解析并导入到指定画板。

## 用法

```bash
# 导入 PlantUML
python -X utf8 .claude/skills/feishu/board/plantuml/tool.py --whiteboard-id "xxx" --code "@startuml\nAlice -> Bob: Hello\nBob --> Alice: Hi\n@enduml"

# 使用画板样式（解析为独立节点，可编辑）
python -X utf8 .claude/skills/feishu/board/plantuml/tool.py --whiteboard-id "xxx" --code "..." --style board
```

## 参数

- `--whiteboard-id`（必填）：画板唯一标识
- `--code`（必填）：PlantUML 代码
- `--style`：渲染样式，`classic`（默认，图片可二次编辑）或 `board`（画板节点）

## 返回格式

```
导入成功 (node_id: xxx)
```
