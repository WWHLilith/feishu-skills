"""飞书审批实例查询。"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request

_STATUS_MAP = {
    "PENDING": "审批中",
    "APPROVED": "已通过",
    "REJECTED": "已拒绝",
    "CANCELED": "已撤回",
    "DELETED": "已删除",
}


def query_approval(instance_code: str) -> str:
    data = api_request("GET", f"/approval/v4/instances/{instance_code}")
    inst = data.get("data", {})
    status = inst.get("status", "UNKNOWN")
    status_text = _STATUS_MAP.get(status, status)

    # 格式化时间
    create_time = inst.get("start_time", "")
    if create_time:
        try:
            create_time = datetime.fromtimestamp(int(create_time) / 1000).strftime("%Y-%m-%d %H:%M")
        except (ValueError, OSError):
            pass

    lines = [
        f"审批实例: {instance_code}",
        f"状态: {status_text}",
        f"审批名称: {inst.get('approval_name', 'N/A')}",
        f"创建时间: {create_time}",
    ]

    # 审批节点
    tasks = inst.get("task_list", [])
    if tasks:
        lines.append(f"\n审批节点 ({len(tasks)} 个):")
        for i, task in enumerate(tasks, 1):
            node = task.get("node_name", "")
            task_status = _STATUS_MAP.get(task.get("status", ""), task.get("status", ""))
            lines.append(f"  {i}. {node}: {task_status}")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="查询飞书审批状态")
    parser.add_argument("--instance-code", required=True, help="审批实例 code")
    args = parser.parse_args()
    try:
        print(query_approval(args.instance_code))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
