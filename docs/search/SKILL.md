---
name: feishu-docs-search
description: "搜索飞书云文档。"
---

# 飞书文档搜索

按关键词搜索飞书云文档，返回匹配的文档列表。

## 用法

```bash
python -X utf8 .claude/skills/feishu/docs/search/tool.py --query "搜索关键词" [--count 10]
```

## 参数

- `--query`（必填）：搜索关键词
- `--count`（可选）：返回数量，默认 10

## 示例

```bash
python -X utf8 .claude/skills/feishu/docs/search/tool.py --query "需求文档"
python -X utf8 .claude/skills/feishu/docs/search/tool.py --query "战斗系统设计" --count 5
```

## 返回格式

```
1. 文档标题A (ID: abc123, 类型: docx, 链接: https://xxx.feishu.cn/docx/abc123)
2. 文档标题B (ID: def456, 类型: sheet, 链接: https://xxx.feishu.cn/sheets/def456)
未找到结果时输出：未找到匹配的文档。
```

## 注意

- 搜索 API 使用 **user_access_token**（用户级授权），首次使用会自动打开浏览器登录飞书
- 登录后 token 缓存到本地文件，后续自动刷新，无需重复登录
- 搜索范围为当前登录用户有权限查看的所有文档
