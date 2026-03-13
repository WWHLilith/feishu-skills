# Feishu Skills for Claude Code

> 在 Claude Code 对话中用自然语言操作飞书，无需切换窗口，无需记忆 API。

8 modules · 20 tools · OAuth 用户身份

## Why Skills, Not MCP?

飞书有官方 MCP Server，为什么还要用 Skills？

| | Skills（本项目） | MCP Server |
|---|---|---|
| **部署** | `git clone` 即用，零基础设施 | 需要启动独立进程，配置 `mcp.json` |
| **依赖** | Python + `requests`（1 个包） | Node.js / Docker，依赖链更长 |
| **身份** | OAuth 用户身份，操作归属你本人 | 通常只有 Bot 身份，权限受限 |
| **上下文** | 3 层 SKILL.md 按需加载，不浪费 token | 所有工具 schema 一次性注入上下文 |
| **可扩展** | 告诉 Claude "帮我加个 XX skill"，它会自己写 | 需要改源码、重新构建、重启进程 |
| **可靠性** | 无常驻进程，不会崩溃或断连 | 进程挂了所有工具不可用 |
| **调试** | 每个 tool.py 可独立 `python tool.py` 运行测试 | 需要通过 MCP 协议交互，调试困难 |

**总结**：MCP 适合需要标准化协议对接多个 AI 客户端的场景。如果你只用 Claude Code，Skills 更轻量、更灵活、更易维护。

## Features

- **📄 云文档 docs** — 搜索、阅读、创建、更新云文档，列出文件夹内容
- **📚 知识库 wiki** — 浏览知识空间目录树，阅读知识库页面
- **📊 电子表格 sheets** — 读取、写入表格数据，创建新表格
- **💬 即时消息 messages** — 发送文本 / 富文本消息，Webhook 推送通知
- **👤 通讯录 contacts** — 按姓名搜索用户，获取用户详情
- **📋 多维表格 bitable** — 查询、新增、更新多维表格记录
- **📅 日历 calendar** — 创建日程，查询日程列表
- **✅ 审批 approval** — 发起审批实例，查询审批状态

## Quick Start

### 1. 安装

将本仓库克隆到项目的 `.claude/skills/feishu/` 目录：

```bash
git clone https://github.com/WWHLilith/feishu-skills.git .claude/skills/feishu
```

### 2. 配置环境

**方式一：一键安装（Windows）**

```bash
.claude/skills/feishu/setup.bat
```

**方式二：手动安装**

```bash
# 确保 Python 3.9+
python --version

# 安装依赖（仅需 requests）
pip install -r .claude/skills/feishu/requirements.txt
```

### 3. 配置飞书凭证

复制 `.env.example` 为 `.env`，填入飞书应用凭证：

```bash
cp .claude/skills/feishu/.env.example .claude/skills/feishu/.env
```

```env
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
```

凭证在 [飞书开放平台](https://open.feishu.cn/app) 创建应用后获取。

### 4. 首次授权

在 Claude Code 中发出飞书相关请求时，浏览器会自动弹出飞书 OAuth 授权页面，点击授权即可。后续 token 自动刷新，无需重复操作。

## Usage

直接用自然语言告诉 Claude Code 你想做什么：

```
"帮我搜一下飞书上关于战斗系统的文档"
"读一下这个文档 https://xxx.feishu.cn/docx/abc123"
"创建一个飞书文档，标题叫《技术方案》"
"给张三发一条飞书消息"
"查一下这个审批的状态"
```

## Required Scopes

飞书应用需要在开放平台开通以下权限：

| 功能 | Scope |
|------|-------|
| 文档读写 | `docs:doc`、`docx:document` |
| 云空间 | `drive:drive` |
| 知识库 | `wiki:wiki` |
| 电子表格 | `sheets:spreadsheet` |
| 多维表格 | `bitable:app` |
| 消息发送 | `im:message`、`im:message:send_as_bot` |
| 通讯录 | `contact:user.base:readonly` |
| 日历 | `calendar:calendar` |
| 审批 | `approval:approval`、`approval:instance` |

OAuth 回调地址：`http://localhost:19897/callback`（需在应用安全设置中添加）

## Project Structure

```
feishu/
├── SKILL.md              # 入口：能力路由表（Claude Code 读取）
├── scripts/              # 共享模块 (config / auth / oauth / api)
├── docs/                 # search / read / create / update / list
├── wiki/                 # search / read
├── sheets/               # read / write / create
├── messages/             # send / webhook
├── contacts/             # search & get
├── bitable/              # query / create / update
├── calendar/             # create-event / list-events
├── approval/             # create / query
├── setup.bat             # Windows 一键安装脚本
├── requirements.txt      # Python 依赖
└── .env.example          # 凭证配置模板
```

## Extending

添加新的飞书功能只需两步：

1. 在对应目录下创建 `SKILL.md`（描述用法）+ `tool.py`（CLI 工具）
2. `scripts/api.py` 已封装好认证和请求，新 tool 只需关注业务逻辑

详见 [飞书服务端 API 文档](https://open.feishu.cn/document/server-docs/api-call-guide/calling-process/overview)。

## License

MIT
