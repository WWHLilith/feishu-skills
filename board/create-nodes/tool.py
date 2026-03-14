"""飞书画板创建节点。"""
import argparse
import json
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def create_nodes(whiteboard_id: str, nodes_json: str) -> str:
    nodes = json.loads(nodes_json)
    if not isinstance(nodes, list):
        nodes = [nodes]

    data = api_request("POST", f"/board/v1/whiteboards/{whiteboard_id}/nodes", body={
        "nodes": nodes,
    }, scopes=["board:whiteboard:node:create"])

    created_ids = data.get("data", {}).get("ids", [])
    lines = [f"创建成功，共 {len(created_ids)} 个节点\n"]
    for i, nid in enumerate(created_ids, 1):
        lines.append(f"{i}. id={nid}")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="创建飞书画板节点")
    parser.add_argument("--whiteboard-id", required=True, help="画板唯一标识")
    parser.add_argument("--nodes", required=True, help="节点 JSON 数组")
    args = parser.parse_args()
    try:
        print(create_nodes(args.whiteboard_id, args.nodes))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
