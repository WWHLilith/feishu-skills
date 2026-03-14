"""飞书 OAuth 授权 — 获取 user_access_token（用于搜索等需要用户级权限的 API）。

流程：
1. 首次调用 get_user_token() 时，如果本地无有效 token，自动打开浏览器登录
2. 本地启动临时 HTTP 服务器接收回调授权码
3. 用授权码换取 user_access_token + refresh_token
4. Token 缓存到本地文件，后续自动刷新
5. scope 按需累积：每次调用只请求当前功能所需的 scope，不足时自动追加并重新授权
"""
import json
import os
import time
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

import requests

from .config import FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_BASE_URL

_REDIRECT_PORT = 19897
_REDIRECT_URI = f"http://localhost:{_REDIRECT_PORT}/callback"
_TOKEN_FILE = Path(__file__).resolve().parent.parent / ".oauth_token.json"

_user_cache = {"token": "", "refresh_token": "", "expires_at": 0.0, "scopes": []}


def _load_cached_token() -> bool:
    """从本地文件加载缓存的 token。"""
    if _TOKEN_FILE.exists():
        try:
            data = json.loads(_TOKEN_FILE.read_text(encoding="utf-8"))
            _user_cache.update(data)
            if "scopes" not in _user_cache:
                _user_cache["scopes"] = []
            return True
        except Exception:
            pass
    return False


def _save_token():
    """保存 token 到本地文件。"""
    _TOKEN_FILE.write_text(json.dumps(_user_cache, ensure_ascii=False, indent=2), encoding="utf-8")


def _refresh_user_token() -> bool:
    """用 refresh_token 刷新 user_access_token。"""
    if not _user_cache["refresh_token"]:
        return False
    try:
        resp = requests.post(
            f"{FEISHU_BASE_URL}/authen/v1/oidc/refresh_access_token",
            headers={"Authorization": f"Bearer {_get_app_access_token()}",
                     "Content-Type": "application/json"},
            json={
                "grant_type": "refresh_token",
                "refresh_token": _user_cache["refresh_token"],
            },
            timeout=10,
        )
        data = resp.json()
        if data.get("code") != 0:
            return False
        token_data = data.get("data", {})
        _user_cache["token"] = token_data["access_token"]
        _user_cache["refresh_token"] = token_data.get("refresh_token", _user_cache["refresh_token"])
        _user_cache["expires_at"] = time.time() + token_data.get("expires_in", 7200)
        _save_token()
        return True
    except Exception:
        return False


def _get_app_access_token() -> str:
    """获取 app_access_token（用于 OAuth 流程中间步骤）。"""
    resp = requests.post(
        f"{FEISHU_BASE_URL}/auth/v3/app_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET},
        timeout=10,
    )
    data = resp.json()
    return data.get("app_access_token", "")


def _exchange_code(code: str) -> dict:
    """用授权码换取 user_access_token。"""
    app_token = _get_app_access_token()
    resp = requests.post(
        f"{FEISHU_BASE_URL}/authen/v1/oidc/access_token",
        headers={"Authorization": f"Bearer {app_token}",
                 "Content-Type": "application/json"},
        json={
            "grant_type": "authorization_code",
            "code": code,
        },
        timeout=10,
    )
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"OAuth 换取 token 失败: {data}")
    return data.get("data", {})


class _CallbackHandler(BaseHTTPRequestHandler):
    """处理 OAuth 回调的 HTTP 请求。"""
    auth_code = None

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/callback":
            params = parse_qs(parsed.query)
            code = params.get("code", [None])[0]
            if code:
                _CallbackHandler.auth_code = code
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<!DOCTYPE html><html><body><h2>授权成功！</h2><p>可以关闭此页面。</p><script>window.close()</script></body></html>".encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing code")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # 静默日志


def _do_oauth_login(scopes: list[str]) -> dict:
    """启动 OAuth 登录流程：打开浏览器 → 等待回调 → 换取 token。"""
    _CallbackHandler.auth_code = None

    # 启动本地回调服务器
    server = HTTPServer(("localhost", _REDIRECT_PORT), _CallbackHandler)
    server.timeout = 120  # 2 分钟超时

    scope_str = " ".join(scopes)
    auth_url = (
        f"https://open.feishu.cn/open-apis/authen/v1/authorize"
        f"?app_id={FEISHU_APP_ID}"
        f"&redirect_uri={_REDIRECT_URI}"
        f"&scope={scope_str}"
    )

    print(f"正在打开浏览器进行飞书登录...")
    print(f"如果浏览器未自动打开，请手动访问:\n{auth_url}")
    webbrowser.open(auth_url)

    # 等待回调
    while _CallbackHandler.auth_code is None:
        server.handle_request()

    server.server_close()

    if not _CallbackHandler.auth_code:
        raise RuntimeError("OAuth 登录超时或失败")

    return _exchange_code(_CallbackHandler.auth_code)


def get_user_token(scopes: list[str] | None = None) -> str:
    """获取 user_access_token，自动处理缓存、刷新和首次登录。

    Args:
        scopes: 当前操作所需的 OAuth scope 列表。为 None 时使用已缓存的 token（不检查 scope）。
    """
    now = time.time()

    # 加载缓存
    if not _user_cache["token"]:
        _load_cached_token()

    cached_scopes = set(_user_cache.get("scopes", []))
    required_scopes = set(scopes) if scopes else set()
    need_reauth = bool(required_scopes - cached_scopes)

    # 如果 scope 满足且 token 有效，直接返回
    if not need_reauth and _user_cache["token"] and _user_cache["expires_at"] > now + 300:
        return _user_cache["token"]

    # 如果 scope 满足但 token 过期，尝试 refresh
    if not need_reauth and _user_cache["refresh_token"] and _refresh_user_token():
        return _user_cache["token"]

    # 需要重新登录（scope 不足或无有效 token）
    all_scopes = sorted(cached_scopes | required_scopes)
    if not all_scopes:
        raise RuntimeError("未指定任何 OAuth scope，无法发起授权")
    token_data = _do_oauth_login(all_scopes)
    _user_cache["token"] = token_data["access_token"]
    _user_cache["refresh_token"] = token_data.get("refresh_token", "")
    _user_cache["expires_at"] = now + token_data.get("expires_in", 7200)
    _user_cache["scopes"] = all_scopes
    _save_token()
    print("飞书 OAuth 登录成功！")
    return _user_cache["token"]
