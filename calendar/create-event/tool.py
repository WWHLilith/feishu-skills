"""飞书创建日程。"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def _to_timestamp(dt_str: str) -> str:
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    return str(int(dt.timestamp()))


def create_event(summary: str, start: str, end: str, description: str = "", attendees: str = "") -> str:
    # 获取主日历（从日历列表中找 type=primary）
    cal_resp = api_request("GET", "/calendar/v4/calendars", scopes=["calendar:calendar"])
    calendar_id = ""
    for cal in cal_resp.get("data", {}).get("calendar_list", []):
        if cal.get("type") == "primary":
            calendar_id = cal["calendar_id"]
            break
    if not calendar_id:
        return "[error] 未找到主日历"

    body = {
        "summary": summary,
        "start_time": {"timestamp": _to_timestamp(start)},
        "end_time": {"timestamp": _to_timestamp(end)},
    }
    if description:
        body["description"] = description

    data = api_request("POST", f"/calendar/v4/calendars/{calendar_id}/events", body=body, scopes=["calendar:calendar"])
    event = data.get("data", {}).get("event", {})
    event_id = event.get("event_id", "")

    # 添加参与者
    if attendees and event_id:
        attendee_list = [{"type": "user", "user_id": uid.strip()} for uid in attendees.split(",")]
        try:
            api_request("POST", f"/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees", body={
                "attendees": attendee_list,
            }, scopes=["calendar:calendar"])
        except Exception:
            pass

    return f"日程创建成功\n标题: {summary}\n时间: {start} ~ {end.split(' ')[-1]}\n事件ID: {event_id}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="创建飞书日程")
    parser.add_argument("--summary", required=True, help="日程标题")
    parser.add_argument("--start", required=True, help="开始时间 (YYYY-MM-DD HH:MM)")
    parser.add_argument("--end", required=True, help="结束时间 (YYYY-MM-DD HH:MM)")
    parser.add_argument("--description", default="", help="日程描述")
    parser.add_argument("--attendees", default="", help="参与者 open_id，逗号分隔")
    args = parser.parse_args()
    try:
        print(create_event(args.summary, args.start, args.end, args.description, args.attendees))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
