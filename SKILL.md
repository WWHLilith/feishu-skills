---
name: feishu
description: "当需要操作飞书（文档、消息、表格、日历、知识库等）时使用。"
alwaysApply: false
---

# 飞书技能集

## 发现子技能

使用 Bash 工具运行 `grep "^description:" <本SKILL.md所在目录>/*/SKILL.md`，获取所有直接子技能的 description。

根据用户需求匹配最相关的子技能，再读取其完整 SKILL.md 获取详细用法。

如果子技能本身也包含更深层的子技能，同样先用 `grep "^description:" <该SKILL.md所在目录>/*/SKILL.md` 发现下一层，按需加载。

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
