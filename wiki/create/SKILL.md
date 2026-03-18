---
name: feishu-wiki-create
description: "在飞书知识库指定页面下创建子页面。"
---

# 飞书知识库 — 创建子页面

在某个知识库页面下新建一个子页面。

## 用法

```bash
python -X utf8 ~/.claude/skills/feishu-skills/wiki/create/tool.py --parent "父页面URL或token" --title "新页面标题"
```

## 参数

- `--parent`：父页面的完整 URL 或 wiki token（二选一）
- `--title`：新页面的标题

## 示例

```bash
python -X utf8 ~/.claude/skills/feishu-skills/wiki/create/tool.py \
  --parent "https://lilithgames.feishu.cn/wiki/Kb5NwMdciidMFaktqf4cM859ntd" \
  --title "IM后台系统"
```

## 返回格式

```
创建成功
标题: 新页面标题
Token: XxxXxxXxx
URL: https://lilithgames.feishu.cn/wiki/XxxXxxXxx
```

## 所需权限

OAuth scope：`wiki:wiki`
