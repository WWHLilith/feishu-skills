---
name: feishu-bitable-create-app
description: "创建飞书多维表格应用 — 支持自定义字段和批量写入初始数据。"
---

# 创建飞书多维表格

在用户个人空间创建一个新的多维表格应用，可自定义字段并批量写入初始数据。

## 用法

```bash
# 仅创建空表（使用默认字段）
python -X utf8 .claude/skills/feishu/bitable/create-app/tool.py --name "我的表格"

# 创建表并自定义字段
python -X utf8 .claude/skills/feishu/bitable/create-app/tool.py --name "员工信息" --fields '[{"field_name":"姓名","type":1},{"field_name":"年龄","type":2},{"field_name":"城市","type":1}]'

# 创建表、自定义字段并批量写入数据
python -X utf8 .claude/skills/feishu/bitable/create-app/tool.py --name "员工信息" --fields '[{"field_name":"姓名","type":1},{"field_name":"年龄","type":2}]' --records '[{"姓名":"张三","年龄":28},{"姓名":"李四","年龄":35}]'

# 指定目标文件夹
python -X utf8 .claude/skills/feishu/bitable/create-app/tool.py --name "项目表" --folder-token "fldcnXXX"
```

## 参数

- `--name`（必填）：多维表格名称
- `--fields`（可选）：字段定义 JSON 数组，每项包含 `field_name` 和 `type`
- `--records`（可选）：初始数据 JSON 数组，每项为字段名到值的映射
- `--folder-token`（可选）：目标文件夹 token，不指定则创建在个人空间根目录

## 字段类型

| type 值 | 类型 |
|---------|------|
| 1 | 文本 |
| 2 | 数字 |
| 3 | 单选 |
| 4 | 多选 |
| 5 | 日期 |
| 7 | 复选框 |
| 11 | 人员 |
| 13 | 电话号码 |
| 15 | 超链接 |
| 17 | 附件 |
| 18 | 关联 |
| 20 | 公式 |
| 1001 | 创建时间 |
| 1002 | 更新时间 |
| 1003 | 创建人 |
| 1004 | 更新人 |

## 输出

输出创建结果，包含 app_token、table_id 和可访问的 URL 地址。
