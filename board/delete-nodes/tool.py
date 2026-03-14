"""飞书画板删除节点。"""
import argparse
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

import requests
from scripts.oauth import get_user_token
from scripts.config import FEISHU_BASE_URL


def delete_nodes(whiteboard_id: str, node_ids: list[str]) -> str:
    token = get_user_token(["board:whiteboard:node:delete"])
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    # batch_delete 通过 query param 传 node_ids（逗号分隔）
    ids_str = ",".join(node_ids)
    resp = requests.delete(
        f"{FEISHU_BASE_URL}/board/v1/whiteboards/{whiteboard_id}/nodes/batch_delete",
        headers=headers, params={"node_ids": ids_str}, timeout=15,
    )
    try:
        data = resp.json()
    except (ValueError, requests.exceptions.JSONDecodeError):
        if resp.ok:
            return f"删除成功，共删除 {len(node_ids)} 个节点"
        raise RuntimeError(f"[飞书API错误] HTTP {resp.status_code}: {resp.text[:200]}")
    if data.get("code", 0) != 0:
        raise RuntimeError(f"[飞书API错误] code={data['code']}, msg={data.get('msg', '')}")
    return f"删除成功，共删除 {len(node_ids)} 个节点"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="删除飞书画板节点")
    parser.add_argument("--whiteboard-id", required=True, help="画板唯一标识")
    parser.add_argument("--node-ids", required=True, help="要删除的节点 ID，多个用逗号分隔")
    args = parser.parse_args()
    try:
        ids = [x.strip() for x in args.node_ids.split(",") if x.strip()]
        print(delete_nodes(args.whiteboard_id, ids))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
