---
name: feishu-wiki-search
description: "搜索飞书知识库节点、列出知识空间、浏览目录树。"
---

# 飞书知识库搜索

搜索知识库节点、列出空间、浏览目录。

**注意**：飞书 wiki API 没有全文搜索，只能按标题匹配一级节点。深层文档建议通过 URL 直接用 `docs/read` 读取。

## 用法

```bash
# 列出所有知识空间
python -X utf8 .claude/skills/feishu/wiki/search/tool.py --list-spaces

# 在指定空间搜索（一级节点标题匹配）
python -X utf8 .claude/skills/feishu/wiki/search/tool.py --query "关键词" --space-id "7361047859690897412"

# 浏览指定节点的子节点
python -X utf8 .claude/skills/feishu/wiki/search/tool.py --browse "父节点token"
```

## 参数

- `--query`：搜索关键词（标题匹配）
- `--space-id`：限定知识空间 ID
- `--list-spaces`：列出所有可访问的知识空间
- `--browse`：浏览指定节点的子节点
- `--count`（可选）：返回数量，默认 10

## 常用空间

- P-Game: `7361047859690897412`
