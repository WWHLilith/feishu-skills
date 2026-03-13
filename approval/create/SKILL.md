---
name: feishu-approval-create
description: "创建飞书审批实例。"
---

# 创建飞书审批实例

发起一个审批流程。

## 用法

```bash
python -X utf8 .claude/skills/feishu/approval/create/tool.py --code "审批定义code" --user-id "ou_xxx" --form '[{"id":"widget1","type":"input","value":"申请内容"}]'
```

## 参数

- `--code`（必填）：审批定义 code（在审批管理后台获取）
- `--user-id`（必填）：发起人 open_id
- `--form`（必填）：表单数据 JSON 数组

## 返回格式

```
审批实例创建成功 (instance_code: xxx)
```
