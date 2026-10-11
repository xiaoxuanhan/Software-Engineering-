import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


def load_env_file(path):
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_env_file(ENV_FILE)
else:
    load_dotenv(ENV_FILE)

ARK_API_KEY = os.getenv("ARK_API_KEY")
MODEL = (
    os.getenv("ARK_MODEL")
    or os.getenv("ARK_ENDPOINT")
    or "doubao-seed-2-1-pro-260628"
)

if not ARK_API_KEY:
    raise ValueError("没有读取到 ARK_API_KEY，请检查 .env 文件。")
