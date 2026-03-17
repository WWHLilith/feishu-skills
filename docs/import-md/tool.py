"""导入 Markdown 文件为飞书文档。"""
import argparse
import os
import sys
import time
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

import requests
from scripts.config import FEISHU_BASE_URL
from scripts.oauth import get_user_token
from scripts.api import api_request

SCOPES = ["drive:drive"]


def _upload_media(file_path: str, token: str) -> str:
    """上传文件为素材，返回 file_token。"""
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    resp = requests.post(
        f"{FEISHU_BASE_URL}/drive/v1/medias/upload_all",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "file_name": file_name,
            "parent_type": "ccm_import_open",
            "size": str(file_size),
            "extra": '{"obj_type":"docx","file_extension":"md"}',
        },
        files={"file": (file_name, open(file_path, "rb"))},
        timeout=30,
    )
    data = resp.json()
    if data.get("code", 0) != 0:
        raise RuntimeError(f"上传失败: code={data['code']}, msg={data.get('msg', '')}")
    return data["data"]["file_token"]


def _create_import_task(file_token: str, title: str, folder_token: str) -> str:
    """创建导入任务，返回 ticket。"""
    data = api_request("POST", "/drive/v1/import_tasks", body={
        "file_extension": "md",
        "file_token": file_token,
        "type": "docx",
        "file_name": title,
        "point": {"mount_type": 1, "mount_key": folder_token},
    }, use_user_token=True, scopes=SCOPES)
    return data["data"]["ticket"]


def _poll_result(ticket: str, max_wait: int = 30) -> dict:
    """轮询导入结果，返回结果 dict。"""
    for _ in range(max_wait):
        data = api_request("GET", f"/drive/v1/import_tasks/{ticket}",
                           use_user_token=True, scopes=SCOPES)
        result = data.get("data", {}).get("result", {})
        if result.get("url"):
            return result
        time.sleep(1)
    raise RuntimeError("导入超时，请稍后在飞书云空间中检查")


def import_markdown(file_path: str, title: str = "", folder_token: str = "") -> str:
    path = Path(file_path)
    if not path.exists():
        raise RuntimeError(f"文件不存在: {file_path}")
    if path.suffix.lower() not in (".md", ".mark", ".markdown"):
        raise RuntimeError(f"不支持的文件类型: {path.suffix}，仅支持 .md/.mark/.markdown")

    title = title or path.stem
    token = get_user_token(SCOPES)

    file_token = _upload_media(str(path), token)
    ticket = _create_import_task(file_token, title, folder_token)
    result = _poll_result(ticket)

    return f"导入成功\n标题: {title}\n链接: {result['url']}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="导入 Markdown 文件为飞书文档")
    parser.add_argument("--file", required=True, help="Markdown 文件路径")
    parser.add_argument("--title", default="", help="文档标题（默认使用文件名）")
    parser.add_argument("--folder-token", default="", help="目标文件夹 token")
    args = parser.parse_args()
    try:
        print(import_markdown(args.file, args.title, args.folder_token))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
