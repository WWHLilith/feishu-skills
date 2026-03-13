---
name: feishu-docs
description: "飞书云文档操作 — 创建、读取、搜索、更新文档。"
---

# 飞书文档操作

读取对应子目录的 SKILL.md 获取具体用法：

- **search/** — 按关键词搜索文档
- **read/** — 读取文档内容（需要 document_id）
- **create/** — 创建新文档
- **update/** — 更新/追加文档内容
- **list/** — 列出文件夹下的文档或最近文档

## ID 说明

- `document_id`: 文档 URL 中 `/docx/` 后面的部分（如 `Abc123def`）
- `folder_token`: 文件夹 URL 中的 token，根目录留空
- `wiki_token`: 知识库页面的 token（与 document_id 不同）
