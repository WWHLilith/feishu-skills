---
name: feishu
description: "当需要操作飞书（文档、消息、表格、日历、知识库等）时使用。"
---

# 飞书技能集

## 导航协议

本技能集是一棵递归树。在任意层级：

1. 读取当前 SKILL.md，并运行 `grep "^description:" <当前目录>/*/SKILL.md` 发现子节点
2. 无子节点 → 叶子，当前 SKILL.md 包含完整用法，直接使用
3. 有子节点但当前 SKILL.md 已满足需求 → 直接使用
4. 有子节点且需要更具体的操作 → 选择最相关的子节点继续导航

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
