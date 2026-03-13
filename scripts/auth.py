"""飞书认证 — tenant_access_token 获取与缓存。"""
import time
import requests
from .config import FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_BASE_URL

_cache = {"token": "", "expires_at": 0.0}


def get_token() -> str:
    """获取 tenant_access_token，带过期缓存（提前 5 分钟刷新）。"""
    now = time.time()
    if _cache["token"] and _cache["expires_at"] > now + 300:
        return _cache["token"]
    resp = requests.post(
        f"{FEISHU_BASE_URL}/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET},
        timeout=10,
    )
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"飞书认证失败: code={data.get('code')}, msg={data.get('msg')}")
    _cache["token"] = data["tenant_access_token"]
    _cache["expires_at"] = now + data.get("expire", 7200)
    return _cache["token"]
