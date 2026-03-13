---
name: feishu-docs-read
description: "读取飞书云文档内容。"
---

# 飞书文档读取

读取飞书云文档或知识库页面的纯文本内容。支持三种输入方式。

## 用法

```bash
# 方式1：直接传飞书 URL（推荐，自动识别文档类型）
python -X utf8 .claude/skills/feishu/docs/read/tool.py --url "https://xxx.feishu.cn/wiki/TOKEN"
python -X utf8 .claude/skills/feishu/docs/read/tool.py --url "https://xxx.feishu.cn/docx/TOKEN"

# 方式2：传 document_id（docx token）
python -X utf8 .claude/skills/feishu/docs/read/tool.py --doc-id "X1Gndy4rwoV7btxPkwacXEbPnAe"

# 方式3：传 wiki token
python -X utf8 .claude/skills/feishu/docs/read/tool.py --wiki-token "Ynxowih7iinvQAku6Y0cei2vnag"
```

## 参数（三选一）

- `--url`：飞书文档或知识库 URL（自动解析 token 和类型）
- `--doc-id`：文档 ID（docx token）
- `--wiki-token`：知识库页面 token（会先解析为 docx token 再读取）

## 返回格式

```
标题: 文档标题
---
文档正文纯文本内容...
```

## 注意

- 返回的是文档的纯文本表示，不包含格式信息
- 知识库页面会自动转换为 docx 读取
