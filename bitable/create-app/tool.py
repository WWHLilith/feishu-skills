"""飞书多维表格 — 创建应用（含自定义字段和批量写入）。"""
import argparse
import json
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request

SCOPES = ["bitable:app"]


def create_app(name: str, folder_token: str | None = None) -> dict:
    """创建多维表格应用，返回 app 信息。"""
    body: dict = {"name": name}
    if folder_token:
        body["folder_token"] = folder_token
    data = api_request("POST", "/bitable/v1/apps", body=body, scopes=SCOPES)
    return data.get("data", {}).get("app", {})


def get_default_table(app_token: str) -> str:
    """获取默认数据表 ID。"""
    data = api_request("GET", f"/bitable/v1/apps/{app_token}/tables", scopes=SCOPES)
    items = data.get("data", {}).get("items", [])
    if not items:
        raise RuntimeError("未找到默认数据表")
    return items[0]["table_id"]


def add_fields(app_token: str, table_id: str, fields: list[dict]) -> list[str]:
    """批量添加自定义字段，返回字段 ID 列表。"""
    field_ids = []
    for f in fields:
        r = api_request(
            "POST",
            f"/bitable/v1/apps/{app_token}/tables/{table_id}/fields",
            body=f,
            scopes=SCOPES,
        )
        fid = r.get("data", {}).get("field", {}).get("field_id", "")
        field_ids.append(fid)
    return field_ids


def batch_create_records(app_token: str, table_id: str, records: list[dict]) -> int:
    """批量创建记录，返回成功条数。"""
    batch = [{"fields": r} for r in records]
    data = api_request(
        "POST",
        f"/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create",
        body={"records": batch},
        scopes=SCOPES,
    )
    return len(data.get("data", {}).get("records", []))


def main():
    parser = argparse.ArgumentParser(description="创建飞书多维表格应用")
    parser.add_argument("--name", required=True, help="多维表格名称")
    parser.add_argument("--fields", help="字段定义 JSON 数组")
    parser.add_argument("--records", help="初始数据 JSON 数组")
    parser.add_argument("--folder-token", help="目标文件夹 token")
    args = parser.parse_args()

    # 1. 创建应用
    app = create_app(args.name, args.folder_token)
    app_token = app.get("app_token", "")
    url = app.get("url", "")
    print(f"多维表格创建成功: {args.name}")
    print(f"  app_token: {app_token}")
    print(f"  url: {url}")

    # 2. 获取默认数据表
    table_id = get_default_table(app_token)
    print(f"  table_id: {table_id}")

    # 3. 添加自定义字段
    if args.fields:
        try:
            fields = json.loads(args.fields)
        except json.JSONDecodeError as e:
            print(f"[error] fields 不是合法 JSON: {e}", file=sys.stderr)
            sys.exit(1)
        field_ids = add_fields(app_token, table_id, fields)
        print(f"  已添加 {len(field_ids)} 个自定义字段")

    # 4. 批量写入记录
    if args.records:
        try:
            records = json.loads(args.records)
        except json.JSONDecodeError as e:
            print(f"[error] records 不是合法 JSON: {e}", file=sys.stderr)
            sys.exit(1)
        count = batch_create_records(app_token, table_id, records)
        print(f"  已写入 {count} 条记录")

    print(f"\n访问地址: {url}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
