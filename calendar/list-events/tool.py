"""飞书日程查询。"""
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def list_events(start_date: str = "", end_date: str = "") -> str:
    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")
    if not end_date:
        end_dt = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)
        end_date = end_dt.strftime("%Y-%m-%d")

    start_ts = str(int(datetime.strptime(start_date, "%Y-%m-%d").timestamp()))
    end_ts = str(int(datetime.strptime(end_date, "%Y-%m-%d").timestamp()))

    # 获取主日历
    cal_resp = api_request("GET", "/calendar/v4/calendars/primary")
    calendar_id = cal_resp.get("data", {}).get("calendar", {}).get("calendar_id", "primary")

    data = api_request("GET", f"/calendar/v4/calendars/{calendar_id}/events", params={
        "start_time": start_ts,
        "end_time": end_ts,
        "page_size": 50,
    })
    events = data.get("data", {}).get("items", [])
    if not events:
        return f"{start_date} ~ {end_date} 没有日程。"

    lines = [f"{start_date} ~ {end_date} 的日程 (共 {len(events)} 个):"]
    for i, ev in enumerate(events, 1):
        summary = ev.get("summary", "(无标题)")
        start = ev.get("start_time", {})
        end = ev.get("end_time", {})
        # 尝试格式化时间
        try:
            s = datetime.fromtimestamp(int(start.get("timestamp", 0))).strftime("%H:%M")
            e = datetime.fromtimestamp(int(end.get("timestamp", 0))).strftime("%H:%M")
            lines.append(f"{i}. {s}-{e} {summary}")
        except (ValueError, OSError):
            lines.append(f"{i}. {summary}")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="查询飞书日程")
    parser.add_argument("--start", default="", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end", default="", help="结束日期 (YYYY-MM-DD)")
    args = parser.parse_args()
    try:
        print(list_events(args.start, args.end))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
