# Feishu Skills

> 在 AI Coding Agent 对话中用自然语言操作飞书，无需切换窗口，无需记忆 API。

9 modules · 27 tools · OAuth 用户身份

## Why Skills, Not MCP?

飞书有官方 MCP Server，为什么还要用 Skills？

| | Skills（本项目） | MCP Server |
|---|---|---|
| **上下文** | 递归树形 SKILL.md 按需加载（grep 发现 → 逐层深入），token 占用只与实际使用的工具数成正比 | 所有工具 schema 一次性注入上下文，token 占用与工具总数成正比 |
| **可扩展** | 加目录 + SKILL.md + tool.py 即可，grep 自动发现，无需修改任何已有文件 | 需修改 server 代码、重新部署 |
| **可靠性** | 无常驻进程，不会崩溃或断连；每个 tool.py 可独立运行调试 | 进程挂了所有工具不可用，调试需通过 MCP 协议 |
| **部署** | `git clone` 即用，Python + `requests`（1 个包） | 需要启动独立进程，配置 `mcp.json`，依赖链更长 |
| **多人协作** | 分支节点不含子节点信息，多人可独立添加技能互不冲突 | 集中式代码，修改易冲突 |

**总结**：MCP 适合需要标准化协议对接多个 AI 客户端的场景。如果你使用支持 Skills 机制的 AI Coding Agent（如 Claude Code），Skills 上下文更省、扩展更灵活、运行更可靠。

## Features

- **📄 云文档 docs** — 搜索、阅读、创建、更新云文档，导入 Markdown，列出文件夹内容
- **📚 知识库 wiki** — 浏览知识空间目录树，阅读知识库页面，移动文档到知识库
- **📊 电子表格 sheets** — 读取、写入表格数据，创建新表格
- **💬 即时消息 messages** — 发送文本 / 富文本消息，Webhook 推送通知，读取聊天记录
- **👤 通讯录 contacts** — 按姓名搜索用户，获取用户详情
- **📋 多维表格 bitable** — 创建表格应用（含自定义字段和批量数据）、查询、新增、更新记录
- **📅 日历 calendar** — 创建日程，查询日程列表
- **🎨 画板 board** — 查看/创建/更新节点，导入 PlantUML 图表
- **🔧 辅助 common** — 部署安装、权限配置、扩展开发


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

在 Agent 中发出飞书相关请求时，浏览器会自动弹出飞书 OAuth 授权页面，点击授权即可。

**按需授权**：工具包采用 scope 按需累积机制 —— 首次使用某个功能时，只请求该功能所需的最小权限。随着你使用更多功能，scope 会自动累积，无需重复授权已有的权限。例如：
- 第一次查日程 → 仅请求 `calendar:calendar`
- 第一次搜文档 → 追加 `docs:doc`，无需重新授权日历
- 后续使用已授权的功能 → 直接复用 token，零打扰

## Usage

直接用自然语言告诉 Agent 你想做什么：

```
"帮我搜一下飞书上关于战斗系统的文档"
"读一下这个文档 https://xxx.feishu.cn/docx/abc123"
"创建一个飞书文档，标题叫《技术方案》"
"给张三发一条飞书消息"
"读一下我和张三的飞书聊天记录"
"把这个文档移动到知识库 https://xxx.feishu.cn/wiki/xxx 下面"
"查一下我今天有什么日程"
```

## Required Scopes

飞书应用需要在开放平台开通对应功能的权限。**只需开通你实际使用的功能**，无需全部开通：

| 功能 | 应用权限（后台开通） | OAuth Scope（自动请求） | Token 类型 |
|------|---------------------|------------------------|-----------|
| 文档读写 | `docs:doc`、`docx:document` | `docs:doc`、`docx:document` | user |
| 云空间 | `drive:drive` | `drive:drive` | user |
| 知识库 | `wiki:wiki` | `wiki:wiki` | user |
| 电子表格 | `sheets:spreadsheet` | `sheets:spreadsheet` | user |
| 多维表格 | `bitable:app` | `bitable:app` | user |
| 消息发送 | `im:message`、`im:message:send_as_bot` | — | tenant |
| 消息读取 | `im:message`、`im:message:readonly` | `im:message`、`im:message:readonly` | user |
| 通讯录查询 | `contact:user.base:readonly`、`contact:user.id:readonly` | — | tenant |
| 通讯录搜索 | `contact:user:search` | `contact:user:search` | user |
| 日历 | `calendar:calendar` | `calendar:calendar` | user |
| 画板 | `board:whiteboard:node:{read,create,update,delete}` | 同左 | user |


- **user**：通过 OAuth 以用户身份操作，scope 按需自动请求
- **tenant**：通过应用凭证操作（如消息以机器人身份发送），无需 OAuth

OAuth 回调地址：`http://localhost:19897/callback`（需在应用安全设置中添加）

## Project Structure

```
feishu/
├── SKILL.md              # 根：递归导航协议 + 通用规则（Agent 自动加载）
├── scripts/              # 共享模块 (config / auth / oauth / api)
├── docs/                 # search / read / create / update / list / import-md
├── wiki/                 # search / read / move
├── sheets/               # read / write / create
├── messages/             # send / webhook / history
├── contacts/             # search & get
├── bitable/              # create-app / query / create / update
├── calendar/             # create-event / list-events
├── board/                # list-nodes / create-nodes / update-nodes / delete-nodes / plantuml
├── common/               # 辅助技能（按需加载）
│   ├── setup/            # 部署安装、凭证配置
│   ├── permissions/      # 权限 scope 配置、OAuth 设置、故障排查
│   └── extending/        # 添加新 skill 的方法和模板
├── setup.bat             # Windows 一键安装脚本
├── requirements.txt      # Python 依赖
└── .env.example          # 凭证配置模板
```

## Architecture: Recursive Skill Tree

技能集采用**递归树形结构**，根节点定义一次导航协议，全树自动生效：

```
1. grep "^description:" <当前目录>/*/SKILL.md → 发现子节点
2. 无子节点 → 叶子，直接使用
3. 有子节点但当前已满足需求 → 直接使用
4. 有子节点且需要更具体的操作 → 选择子节点继续导航
```

**节点类型**：
- **分支节点**：只有 `description` + 一句话概述，不列举子节点内容
- **叶子节点**：包含完整用法（参数、示例、调用命令）+ `tool.py`
- **混合节点**：自身可用，子节点提供更细分的操作

**多人协作友好**：分支节点不包含子节点信息，新增技能只需加目录，无需修改任何已有文件，grep 自动发现。

## Extending

直接告诉 Agent："帮我加个 XX 的飞书 skill"，它会参考现有模板自动创建。

手动添加也很简单：在对应目录下创建 `SKILL.md`（描述用法）+ `tool.py`（CLI 工具），grep 会自动发现新技能，无需修改父目录或注册。`scripts/api.py` 已封装好认证和请求，新 tool 只需关注业务逻辑。调用 `api_request()` 时通过 `scopes=["xxx"]` 声明所需权限，OAuth 会自动按需请求。

详见 [飞书服务端 API 文档](https://open.feishu.cn/document/server-docs/api-call-guide/calling-process/overview)。

## License

MIT
