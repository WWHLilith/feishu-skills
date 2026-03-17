---
name: feishu-extending
description: "现有技能不满足需求、需要新增飞书 API 功能时使用 — 添加新 skill 的方法和模板。"
---

# 扩展新功能

如果当前工具包没有覆盖你需要的飞书功能，可以自行添加 skill：

1. 查阅 [飞书服务端 API 文档](https://open.feishu.cn/document/server-docs/api-call-guide/calling-process/overview) 确认目标 API 是否存在
2. 在对应分类目录下新建子目录（如 `messages/reply/`），包含：
   - `SKILL.md` — 叶子节点格式：frontmatter（`name` + `description`）+ 用法 + 参数 + 示例
   - `tool.py` — 遵循现有模板：argparse CLI → 调用 `scripts.api.api_request()` → 纯文本输出
3. 如果是全新分类，新建分类目录 + 分支 SKILL.md（只需 frontmatter + 一句话概述），再在其下创建叶子技能
4. **无需修改任何已有文件** — 递归导航协议通过 grep 自动发现新节点
5. `scripts/api.py` 已封装好认证和请求，新 tool.py 只需关注业务逻辑
