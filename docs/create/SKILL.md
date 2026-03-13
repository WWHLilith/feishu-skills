---
name: feishu-docs-create
description: "创建飞书云文档。"
---

# 飞书文档创建

创建一个新的飞书云文档。

## 用法

```bash
python -X utf8 .claude/skills/feishu/docs/create/tool.py --title "文档标题" [--folder-token "xxx"] [--content "初始内容"]
```

## 参数

- `--title`（必填）：文档标题
- `--folder-token`（可选）：目标文件夹 token，留空则创建在根目录
- `--content`（可选）：初始正文内容（纯文本）

## 示例

```bash
python -X utf8 .claude/skills/feishu/docs/create/tool.py --title "会议纪要 2026-03-13"
python -X utf8 .claude/skills/feishu/docs/create/tool.py --title "技术方案" --folder-token "fldcnXXX" --content "## 背景\n\n待补充"
```

## 返回格式

```
文档创建成功
标题: 文档标题
ID: document_id
链接: https://xxx.feishu.cn/docx/xxx
```
