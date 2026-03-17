---
name: feishu-docs-import-md
description: "导入 Markdown 文件为飞书文档（保留格式）。"
---

# 飞书文档导入（Markdown）

将本地 Markdown 文件导入为飞书云文档，完整保留标题、表格、代码块等格式。

## 用法

```bash
python -X utf8 .claude/skills/feishu/docs/import-md/tool.py --file "path/to/file.md" [--title "文档标题"] [--folder-token "xxx"]
```

## 参数

- `--file`（必填）：Markdown 文件路径
- `--title`（可选）：文档标题，默认使用文件名
- `--folder-token`（可选）：目标文件夹 token，留空则创建在根目录

## 示例

```bash
python -X utf8 .claude/skills/feishu/docs/import-md/tool.py --file "./design.md" --title "技术方案"
```

## 返回格式

```
导入成功
标题: 技术方案
链接: https://xxx.feishu.cn/docx/xxx
```

## 注意

- 文件大小上限 20MB
- 支持的 Markdown 扩展名：`.md`、`.mark`、`.markdown`
- 需要应用已开通 `drive:drive` 权限
