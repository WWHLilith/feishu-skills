---
name: feishu
description: "当需要操作飞书（文档、消息、表格、日历、知识库等）时使用。"
---

# 飞书技能集

## 导航协议

本技能集是一棵递归树，**必须通过 subAgent 查找所需技能**。

当需要查找具体的飞书操作技能时：

1. **启动 Explore subAgent**，让它在本 SKILL.md 所在目录下递归搜索 `*/SKILL.md` 和 `**/SKILL.md`，根据用户意图匹配最相关的叶子节点
2. subAgent 返回匹配的 SKILL.md 路径和内容摘要
3. 主 Agent 根据返回结果读取对应的叶子 SKILL.md，获取完整用法后执行

**subAgent 提示词模板**：
```
在目录 <本SKILL.md所在目录> 下，递归查找所有 SKILL.md 文件。
读取每个 SKILL.md 的 description 字段，找到与以下意图最匹配的技能：「<用户意图>」。
返回：匹配的 SKILL.md 完整路径、description、以及该文件的完整内容。
如果有多个可能匹配，按相关度排序返回前 3 个。
```

分支节点不列举子节点内容，新增技能只需加目录 + SKILL.md，自动被发现。

## 通用规则

1. 所有 tool.py 使用 `scripts/` 下的共享认证模块，无需手动传 token
2. 调用 tool.py 前，先确认可用的 Python 3 命令：
   - Windows 优先尝试 `py -3`（Python Launcher），其次 `python3`，最后 `python`
   - 运行 `<命令> --version` 确认版本 ≥ 3.9
   - 调用格式：`<python命令> -X utf8 <skill所在目录>/tool.py <参数>`
   - 示例：`py -3 -X utf8 .claude/skills/feishu/docs/search/tool.py --query "关键词"`
3. 输出格式为 LLM 可读的纯文本，非原始 JSON
4. 出错时输出以 `[error]` 开头的错误信息
5. 路径基准：本 SKILL.md 所在目录
