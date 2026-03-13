# Feishu Skills

> 在 AI Coding Agent 对话中用自然语言操作飞书，无需切换窗口，无需记忆 API。

8 modules · 20 tools · OAuth 用户身份

## Why Skills, Not MCP?

飞书有官方 MCP Server，为什么还要用 Skills？

| | Skills（本项目） | MCP Server |
|---|---|---|
| **上下文** | 3 层 SKILL.md 按需加载，不浪费 token；可通过代码组合复杂操作，一次调用完成多步任务 | 所有工具 schema 一次性注入上下文，每个操作独立调用 |
| **可扩展** | 告诉 Agent "帮我加个 XX skill"，它会自己写代码扩展 | 官方 MCP 无法自行添加功能，需等待官方更新 |
| **可靠性** | 无常驻进程，不会崩溃或断连；每个 tool.py 可独立运行调试 | 进程挂了所有工具不可用，调试需通过 MCP 协议 |
| **部署** | `git clone` 即用，Python + `requests`（1 个包） | 需要启动独立进程，配置 `mcp.json`，依赖链更长 |

**总结**：MCP 适合需要标准化协议对接多个 AI 客户端的场景。如果你使用支持 Skills 机制的 AI Coding Agent（如 Claude Code），Skills 上下文更省、扩展更灵活、运行更可靠。

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

将本仓库克隆到项目 Skills 目录（以 Claude Code 为例，其他 Agent 请参考对应文档）：

```bash
git clone https://github.com/WenHaoWang1997/feishu-skills.git <skills-dir>/feishu
# Claude Code 示例：
git clone https://github.com/WenHaoWang1997/feishu-skills.git .claude/skills/feishu
```

### 2. 配置环境

**方式一：一键安装（Windows）**

```bash
<skills-dir>/feishu/setup.bat
```

**方式二：手动安装**

```bash
# 确保 Python 3.9+
python --version

# 安装依赖（仅需 requests）
pip install -r <skills-dir>/feishu/requirements.txt
```

### 3. 配置飞书应用

在 [飞书开放平台](https://open.feishu.cn/app) 完成以下配置：

1. **获取凭证**：创建应用（或使用已有应用），记下 App ID 和 App Secret
2. **开通权限**：在「权限管理」中开通所需的 scope（见下方 [Required Scopes](#required-scopes)）
3. **配置 OAuth 回调**：在「安全设置」→「重定向 URL」中添加：
   ```
   http://localhost:19897/callback
   ```
   > ⚠️ 不配置此项会导致 OAuth 授权失败，无法获取 user_access_token

然后复制 `.env.example` 为 `.env`，填入凭证：

```bash
cp <skills-dir>/feishu/.env.example <skills-dir>/feishu/.env
```

```env
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
```

### 4. 首次授权

在 Agent 中发出飞书相关请求时，浏览器会自动弹出飞书 OAuth 授权页面，点击授权即可。后续 token 自动刷新，无需重复操作。

## Usage

直接用自然语言告诉 Agent 你想做什么：

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
├── SKILL.md              # 入口：能力路由表（Agent 自动加载）
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

直接告诉 Agent："帮我加个 XX 的飞书 skill"，它会参考现有模板自动创建。

手动添加也很简单：在对应目录下创建 `SKILL.md`（描述用法）+ `tool.py`（CLI 工具）。`scripts/api.py` 已封装好认证和请求，新 tool 只需关注业务逻辑。

详见 [飞书服务端 API 文档](https://open.feishu.cn/document/server-docs/api-call-guide/calling-process/overview)。

## License

MIT
