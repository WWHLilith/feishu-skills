"""飞书画板导入 PlantUML/Mermaid 图表。"""
import argparse
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request

SYNTAX_MAP = {"plantuml": 1, "mermaid": 2}
STYLE_MAP = {"board": 1, "classic": 2}


def import_diagram(whiteboard_id: str, code: str, syntax: str = "plantuml", style: str = "classic") -> str:
    syntax_type = SYNTAX_MAP.get(syntax, 1)
    style_type = STYLE_MAP.get(style, 2)

    data = api_request("POST", f"/board/v1/whiteboards/{whiteboard_id}/nodes/plantuml", body={
        "plant_uml_code": code,
        "syntax_type": syntax_type,
        "style_type": style_type,
        "diagram_type": 0,
    }, scopes=["board:whiteboard:node:create"])

    node_id = data.get("data", {}).get("node_id", "")
    return f"导入成功 (node_id: {node_id})"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="导入 PlantUML/Mermaid 到飞书画板")
    parser.add_argument("--whiteboard-id", required=True, help="画板唯一标识")
    parser.add_argument("--code", required=True, help="PlantUML 或 Mermaid 代码")
    parser.add_argument("--syntax", default="plantuml", choices=["plantuml", "mermaid"], help="语法类型")
    parser.add_argument("--style", default="classic", choices=["classic", "board"], help="渲染样式")
    args = parser.parse_args()
    try:
        print(import_diagram(args.whiteboard_id, args.code, args.syntax, args.style))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
