---
name: feishu-docs-update
description: "更新飞书云文档内容。"
---

# 飞书文档更新

向已有飞书云文档追加内容。

## 用法

```bash
python -X utf8 .claude/skills/feishu/docs/update/tool.py --doc-id "文档ID" --content "要追加的内容"
```

## 参数

- `--doc-id`（必填）：文档 ID
- `--content`（必填）：要追加的文本内容

## 示例

```bash
python -X utf8 .claude/skills/feishu/docs/update/tool.py --doc-id "Abc123def" --content "## 新增章节\n\n这是追加的内容"
```

## 返回格式

```
文档更新成功
ID: document_id
追加内容长度: 42 字符
```

## 注意

- 当前仅支持追加纯文本段落到文档末尾
- 如需更复杂的编辑（插入图片、表格等），需直接使用飞书 API
