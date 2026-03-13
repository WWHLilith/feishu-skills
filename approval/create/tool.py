"""飞书创建审批实例。"""
import argparse
import json
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def create_approval(code: str, user_id: str, form: str) -> str:
    data = api_request("POST", "/approval/v4/instances", body={
        "approval_code": code,
        "open_id": user_id,
        "form": form,
    })
    instance_code = data.get("data", {}).get("instance_code", "")
    return f"审批实例创建成功 (instance_code: {instance_code})"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="创建飞书审批实例")
    parser.add_argument("--code", required=True, help="审批定义 code")
    parser.add_argument("--user-id", required=True, help="发起人 open_id")
    parser.add_argument("--form", required=True, help="表单数据 JSON")
    args = parser.parse_args()
    try:
        print(create_approval(args.code, args.user_id, args.form))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
