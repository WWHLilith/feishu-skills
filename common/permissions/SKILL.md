---
name: feishu-permissions
description: "遇到权限报错（Access denied、scope 有误、redirect_uri 不合法等）时使用 — scope 开通、OAuth 设置、故障排查。"
---

# 飞书权限配置

飞书应用需要在 [飞书开放平台管理后台](https://open.feishu.cn/app) 开通以下 scope：

## 应用权限（tenant_access_token，在开放平台"权限管理"开通）

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

## OAuth 用户权限（user_access_token，在"安全设置"添加重定向 URL）

OAuth 回调地址：`http://localhost:19897/callback`

OAuth scope 按需自动请求：每个 tool 声明自己需要的 scope，首次使用时触发授权，已授权的 scope 自动累积复用。

## 故障排查

- `code=99991672` (Access denied) → 对应 scope 未开通
- `code=20043` (scope 有误) → OAuth scope 名称不正确
- `code=20029` (redirect_uri 不合法) → 需在安全设置添加回调 URL
