"""飞书 API 通用请求。"""
import requests
from .auth import get_token
from .config import FEISHU_BASE_URL


def api_request(method: str, path: str, body: dict = None, params: dict = None,
                use_user_token: bool = True, scopes: list[str] | None = None) -> dict:
    """发送飞书 API 请求，自动鉴权，返回解析后的 JSON。

    Args:
        use_user_token: True（默认）使用 user_access_token，操作归属当前用户。
                        False 时使用 tenant_access_token（应用级），无需 scope。
        scopes: 当前操作所需的 OAuth scope 列表。按需请求，首次使用新功能时触发授权。
    """
    if use_user_token:
        from .oauth import get_user_token
        token = get_user_token(scopes)
    else:
        token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    resp = requests.request(
        method, f"{FEISHU_BASE_URL}{path}",
        headers=headers, json=body, params=params, timeout=15,
    )
    data = resp.json()
    if data.get("code", 0) != 0:
        raise RuntimeError(f"[飞书API错误] code={data['code']}, msg={data.get('msg', '')}")
    return data
