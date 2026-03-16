---
name: feishu-setup
description: "首次使用飞书技能或遇到环境/依赖异常时使用 — 一键安装、手动安装、凭证配置、环境要求。"
---

# 飞书技能集部署安装

## 方式一：一键安装（推荐）
```bash
.claude/skills/feishu/setup.bat
```
自动完成 Python 检测、依赖安装和配置文件生成。

## 方式二：手动安装
1. 安装 Python 3.9+（[下载](https://www.python.org/downloads/)）
2. 安装依赖：`py -3 -m pip install -r .claude/skills/feishu/requirements.txt`
3. （可选）复制 `.env.example` 为 `.env`，填入飞书应用凭证

## 凭证配置
飞书应用凭证加载优先级：**环境变量 > `.env` 文件 > 内置默认值**

```bash
# .env 文件格式（放在 .claude/skills/feishu/.env）
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
```

如果使用团队共享的默认应用，无需额外配置。

## 环境要求
- **Python**：3.9+
- **第三方依赖**：`requests>=2.25.0`（唯一第三方包）
- **敏感文件**：`.env` 和 `.oauth_token.json` 已在 `.gitignore` 中排除
