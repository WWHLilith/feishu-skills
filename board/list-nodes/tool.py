"""飞书画板节点查询。"""
import argparse
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def list_nodes(whiteboard_id: str) -> str:
    data = api_request("GET", f"/board/v1/whiteboards/{whiteboard_id}/nodes",
                       scopes=["board:whiteboard:node:read"])
    nodes = data.get("data", {}).get("nodes", [])
    if not nodes:
        return "画板中没有节点。"

    lines = [f"画板节点列表 (共 {len(nodes)} 个节点)\n"]
    for i, node in enumerate(nodes, 1):
        nid = node.get("id", "")
        ntype = node.get("type", "unknown")
        w = node.get("width", 0)
        h = node.get("height", 0)
        x = node.get("x", 0)
        y = node.get("y", 0)

        line = f"{i}. [{ntype}] id={nid}"
        if w and h:
            line += f" ({w:.0f}x{h:.0f} at {x:.0f},{y:.0f})"
        lines.append(line)

        # Show text content
        text_obj = node.get("text", {})
        if text_obj and text_obj.get("text"):
            lines.append(f"   文字: \"{text_obj['text']}\"")

        # Show composite_shape subtype
        cs = node.get("composite_shape", {})
        if cs and cs.get("type"):
            lines.append(f"   子类型: {cs['type']}")

        # Show connector info
        conn = node.get("connector", {})
        if conn:
            start = conn.get("start", {})
            end = conn.get("end", {})
            start_id = start.get("attached_object", {}).get("id", "?")
            end_id = end.get("attached_object", {}).get("id", "?")
            lines.append(f"   连接: {start_id} -> {end_id}")

        # Show parent
        parent = node.get("parent_id")
        if parent:
            lines.append(f"   父节点: {parent}")

        # Show children
        children = node.get("children", [])
        if children:
            lines.append(f"   子节点: {', '.join(children)}")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获取飞书画板节点")
    parser.add_argument("--whiteboard-id", required=True, help="画板唯一标识")
    args = parser.parse_args()
    try:
        print(list_nodes(args.whiteboard_id))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
