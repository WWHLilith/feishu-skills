---
name: feishu-wiki-read
description: "阅读飞书知识库页面内容。"
---

# 飞书知识库阅读

读取知识库页面的完整内容。

## 用法

```bash
python -X utf8 .claude/skills/feishu/wiki/read/tool.py --token "节点token"
python -X utf8 .claude/skills/feishu/wiki/read/tool.py --url "https://xxx.feishu.cn/wiki/TOKEN"
```

## 参数

- `--token`：知识库节点 token
- `--url`：飞书知识库页面 URL（自动提取 token）

二选一。

## 返回格式

```
标题: 页面标题
---
页面正文内容...
```
