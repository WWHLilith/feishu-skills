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

    results = []
    for node in nodes:
        node_id = node.get("id")
        if not node_id:
            results.append("跳过：缺少 id 字段")
            continue
        api_request("PUT", f"/board/v1/whiteboards/{whiteboard_id}/nodes/{node_id}",
                     body=node, scopes=["board:whiteboard:node:update"])
        results.append(f"id={node_id} 更新成功")

    lines = [f"更新完成，共处理 {len(nodes)} 个节点\n"]
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {r}")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="更新飞书画板节点")
    parser.add_argument("--whiteboard-id", required=True, help="画板唯一标识")
    parser.add_argument("--nodes", required=True, help="要更新的节点 JSON 数组，每个节点必须包含 id 字段")
    args = parser.parse_args()
    try:
        print(update_nodes(args.whiteboard_id, args.nodes))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
