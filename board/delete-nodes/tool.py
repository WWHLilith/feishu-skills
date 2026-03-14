"""飞书画板删除节点。"""
import argparse
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def delete_nodes(whiteboard_id: str, node_ids: list[str]) -> str:
    data = api_request("DELETE", f"/board/v1/whiteboards/{whiteboard_id}/nodes", body={
        "node_ids": node_ids,
    }, scopes=["board:whiteboard:node:delete"])

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
