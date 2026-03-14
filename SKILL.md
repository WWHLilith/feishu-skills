---
name: feishu
description: "当需要操作飞书（文档、消息、表格、日历、知识库等）时使用。"
alwaysApply: false
---

# 飞书技能集

当你需要与飞书交互时，根据操作类型读取对应子目录的 SKILL.md：

| 操作类型 | 子目录 | 说明 |
|---------|--------|------|
| 文档 | `docs/` | 创建、读取、搜索、更新云文档 |
| 表格 | `sheets/` | 读写电子表格 |
| 消息 | `messages/` | 发送文本/卡片消息、webhook |
| 通讯录 | `contacts/` | 搜索用户、获取用户信息 |
| 知识库 | `wiki/` | 搜索、阅读知识库页面 |
| 多维表格 | `bitable/` | 多维表格记录增删改查 |
| 日历 | `calendar/` | 创建/查询日程 |
| 画板 | `board/` | 查看/创建/更新/删除节点、导入 PlantUML/Mermaid |

## 快速部署

### 方式一：一键安装（推荐）
```bash
.claude/skills/feishu/setup.bat
```
自动完成 Python 检测、依赖安装和配置文件生成。

### 方式二：手动安装
1. 安装 Python 3.9+（[下载](https://www.python.org/downloads/)）
2. 安装依赖：`py -3 -m pip install -r .claude/skills/feishu/requirements.txt`
3. （可选）复制 `.env.example` 为 `.env`，填入飞书应用凭证

### 凭证配置
飞书应用凭证加载优先级：**环境变量 > `.env` 文件 > 内置默认值**

```bash
# .env 文件格式（放在 .claude/skills/feishu/.env）
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
```

如果使用团队共享的默认应用，无需额外配置。

### 环境要求
- **Python**：3.9+
- **第三方依赖**：`requests>=2.25.0`（唯一第三方包）
- **敏感文件**：`.env` 和 `.oauth_token.json` 已在 `.gitignore` 中排除

## 通用规则

1. 所有 tool.py 使用 `scripts/` 下的共享认证模块，无需手动传 token
2. 调用 tool.py 前，先确认可用的 Python 3 命令：
   - Windows 优先尝试 `py -3`（Python Launcher），其次 `python3`，最后 `python`
   - 运行 `<命令> --version` 确认版本 ≥ 3.9
   - 调用格式：`<python命令> -X utf8 <skill所在目录>/tool.py <参数>`
   - 示例：`py -3 -X utf8 .claude/skills/feishu/docs/search/tool.py --query "关键词"`
3. 输出格式为 LLM 可读的纯文本，非原始 JSON
4. 出错时输出以 `[error]` 开头的错误信息
5. 路径基准：`.claude/skills/feishu/`（相对于项目根目录）

## 权限配置

飞书应用需要在 [飞书开放平台管理后台](https://open.feishu.cn/app) 开通以下 scope：

### 应用权限（tenant_access_token，在开放平台"权限管理"开通）

| 功能 | 所需 scope |
|------|-----------|
| 文档读写 | `docs:doc`、`docx:document` |
| 云空间/文件夹 | `drive:drive` |
| 知识库 | `wiki:wiki` |
| 电子表格 | `sheets:spreadsheet` |
| 多维表格 | `bitable:app` |
| 消息发送 | `im:message`、`im:message:send_as_bot` |
| 通讯录 | `contact:user.base:readonly`、`contact:user.id:readonly` |
| 日历 | `calendar:calendar`、`calendar:calendar:readonly` |
| 画板 | `board:whiteboard:node:read`、`board:whiteboard:node:create`、`board:whiteboard:node:update`、`board:whiteboard:node:delete` |

### OAuth 用户权限（user_access_token，在"安全设置"添加重定向 URL）

OAuth 回调地址：`http://localhost:19897/callback`

OAuth scope 按需自动请求：每个 tool 声明自己需要的 scope，首次使用时触发授权，已授权的 scope 自动累积复用。

### 故障排查

- `code=99991672` (Access denied) → 对应 scope 未开通
- `code=20043` (scope 有误) → OAuth scope 名称不正确
- `code=20029` (redirect_uri 不合法) → 需在安全设置添加回调 URL

## 扩展新功能

如果当前工具包没有覆盖你需要的飞书功能，可以自行添加 skill：

1. 查阅 [飞书服务端 API 文档](https://open.feishu.cn/document/server-docs/api-call-guide/calling-process/overview) 确认目标 API 是否存在
2. 在对应分类目录下新建子目录（如 `messages/reply/`），包含：
   - `SKILL.md` — 遵循现有叶子节点格式（frontmatter `name` + `description`，用法说明 + 参数 + 示例）
   - `tool.py` — 遵循现有模板：argparse CLI → 调用 `scripts.api.api_request()` → 纯文本输出
3. 如果是全新分类，在本文件的操作类型表中补充对应条目
4. `scripts/api.py` 已封装好认证和请求，新 tool.py 只需关注业务逻辑
