---
name: feishu-wiki-move
description: "将飞书云文档移动到知识库指定目录下。"
---

# 飞书知识库 — 移动文档

将已有的飞书云文档移动到知识库指定节点下。

## 用法

```bash
# 通过文档 URL 移动到知识库目录
python -X utf8 .claude/skills/feishu/wiki/move/tool.py --doc-url "https://xxx.feishu.cn/docx/xxxtoken" --parent-url "https://xxx.feishu.cn/wiki/xxxtoken"

# 通过 token 移动
python -X utf8 .claude/skills/feishu/wiki/move/tool.py --doc-token "J3PNdxxxxx" --obj-type docx --parent-token "SCniwxxxxx"
```

## 参数

- `--doc-url`：文档 URL（自动提取 token 和类型，与 --doc-token 二选一）
- `--doc-token`：文档 token（与 --doc-url 二选一）
- `--obj-type`：文档类型，可选 `docx`、`sheet`、`bitable`、`file`（使用 --doc-token 时必填，默认 `docx`）
- `--parent-url`：目标知识库节点 URL（与 --parent-token 二选一）
- `--parent-token`：目标知识库节点 token（与 --parent-url 二选一）

## 所需权限

- `wiki:wiki` — 知识库读写

## 返回格式

```
移动成功
标题: 技术方案
链接: https://xxx.feishu.cn/wiki/xxxtoken
```
