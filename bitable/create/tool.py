"""飞书多维表格创建记录。"""
import argparse
import json
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def create_record(app_token: str, table_id: str, fields: dict) -> str:
    data = api_request("POST", f"/bitable/v1/apps/{app_token}/tables/{table_id}/records", body={
        "fields": fields,
    })
    record = data.get("data", {}).get("record", {})
    record_id = record.get("record_id", "")
    return f"记录创建成功 (record_id: {record_id})"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="创建多维表格记录")
    parser.add_argument("--app-token", required=True, help="多维表格 app_token")
    parser.add_argument("--table-id", required=True, help="数据表 ID")
    parser.add_argument("--fields", required=True, help="字段 JSON")
    args = parser.parse_args()
    try:
        fields = json.loads(args.fields)
        print(create_record(args.app_token, args.table_id, fields))
    except json.JSONDecodeError as e:
        print(f"[error] fields 不是合法 JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
