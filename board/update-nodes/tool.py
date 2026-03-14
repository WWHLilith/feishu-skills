"""飞书画板更新节点。"""
import argparse
import json
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def update_nodes(whiteboard_id: str, nodes_json: str) -> str:
    nodes = json.loads(nodes_json)
    if not isinstance(nodes, list):
        nodes = [nodes]

    data = api_request("PATCH", f"/board/v1/whiteboards/{whiteboard_id}/nodes", body={
        "nodes": nodes,
    }, scopes=["board:whiteboard:node:update"])

    updated = data.get("data", {}).get("nodes", [])
    lines = [f"更新成功，共 {len(updated)} 个节点\n"]
    for i, node in enumerate(updated, 1):
        nid = node.get("id", "")
        ntype = node.get("type", "")
        lines.append(f"{i}. id={nid} (type={ntype})")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="更新飞书画板节点")
    parser.add_argument("--whiteboard-id", required=True, help="画板唯一标识")
    parser.add_argument("--nodes", required=True, help="要更新的节点 JSON 数组")
    args = parser.parse_args()
    try:
        print(update_nodes(args.whiteboard_id, args.nodes))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
