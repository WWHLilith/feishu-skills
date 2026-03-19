"""飞书应用凭证配置。优先级：环境变量 > .env 文件 > 内置默认值。"""
import os
from pathlib import Path

def _load_env():
    """从 .env 文件加载配置到环境变量（不覆盖已有值）。"""
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if key and key not in os.environ:
                os.environ[key] = value

_load_env()

FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
FEISHU_BASE_URL = "https://open.feishu.cn/open-apis"
FEISHU_DOMAIN = os.environ.get("FEISHU_DOMAIN", "feishu.cn")
