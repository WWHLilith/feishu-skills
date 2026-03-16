---
name: feishu-extending
description: "现有技能不满足需求、需要新增飞书 API 功能时使用 — 添加新 skill 的方法和模板。"
---

# 扩展新功能

如果当前工具包没有覆盖你需要的飞书功能，可以自行添加 skill：

1. 查阅 [飞书服务端 API 文档](https://open.feishu.cn/document/server-docs/api-call-guide/calling-process/overview) 确认目标 API 是否存在
2. 在对应分类目录下新建子目录（如 `messages/reply/`），包含：
   - `SKILL.md` — 遵循现有叶子节点格式（frontmatter `name` + `description`，用法说明 + 参数 + 示例）
   - `tool.py` — 遵循现有模板：argparse CLI → 调用 `scripts.api.api_request()` → 纯文本输出
3. 如果是全新分类，在主 SKILL.md 中无需额外操作（grep 动态发现会自动包含新目录）
4. `scripts/api.py` 已封装好认证和请求，新 tool.py 只需关注业务逻辑
