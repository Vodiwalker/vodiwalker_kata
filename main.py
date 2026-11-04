# ============================================================
# VodiWalker 15.0.0
# Railway Ready
# ============================================================

import asyncio
import ipaddress
import base64
import hashlib
import json
import logging
import os
import re
import secrets
import string
import time
import psutil

from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote, parse_qs

import aiofiles
import httpx
import uvicorn

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    Depends,
)
from fastapi.responses import (
    Response,
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
)
from fastapi.middleware.cors import CORSMiddleware


# ============================================================
# APP
# ============================================================

APP_NAME = "VodiWalker"
APP_VERSION = "27.3.0"

# فقط ویرایش «متن‌های ربات» قفل است؛ تنظیمات و روشن/خاموش ربات آزاد است
BOT_TEXTS_LOCKED = True
BOT_TEXTS_LOCKED_MSG = "ویرایش متن‌های ربات قفل شده است و امکان تغییر ندارد"

SUPPORT_USERNAME = "@vodiwalker02"
CHANNEL_USERNAME = "vodiwalkervpn03"

# تنظیماتی که باید بعد از ری‌استارت هم بمانند (قبلاً فقط در حافظه بودند و با هر ری‌استارت پاک می‌شدند)
PERSISTED_EXTRA_SETTINGS = (
    "sub_remark_show_name", "sub_remark_show_volume", "sub_remark_show_id", "sub_remark_show_inbound",
    "sub_info_line_enabled", "sub_info_line_show_volume", "sub_info_line_show_expiry",
    "support_username", "channel_username", "name_style_enabled",
    "last_public_host", "last_public_scheme", "last_public_port",
)

_TG_USER_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{4,31}$")


def _clean_tg_username(raw) -> str:
    value = str(raw or "").strip()
    for prefix in ("https://t.me/", "http://t.me/", "t.me/", "https://telegram.me/", "@"):
        if value.lower().startswith(prefix):
            value = value[len(prefix):]
    return value.strip().strip("/")


def get_support_username() -> str:
    """آیدی پشتیبان تلگرام (قابل تنظیم از داخل پنل)؛ اگر خالی باشد مقدار پیش‌فرض."""
    raw = _clean_tg_username(CONFIG.get("support_username"))
    return "@" + raw if raw and _TG_USER_RE.match(raw) else SUPPORT_USERNAME


def get_support_url() -> str:
    return "https://t.me/" + get_support_username().lstrip("@")


def get_channel_url() -> str:
    raw = _clean_tg_username(CONFIG.get("channel_username"))
    return "https://t.me/" + (raw if raw and _TG_USER_RE.match(raw) else CHANNEL_USERNAME)
SUPPORT_URL = "https://t.me/vodiwalker02"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(APP_NAME)


# ============================================================
# TIMEZONE
# ============================================================

try:
    from zoneinfo import ZoneInfo

    IRAN_TZ = ZoneInfo("Asia/Tehran")

except Exception:
    IRAN_TZ = None


# ============================================================
# RAILWAY
# ============================================================

PORT = int(
    os.environ.get(
        "PORT",
        "8000",
    )
)

DATA_DIR = Path(
    os.environ.get(
        "RAILWAY_VOLUME_MOUNT_PATH",
        os.environ.get(
            "DATA_DIR",
            "./data",
        ),
    )
)

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATA_FILE = DATA_DIR / "vodiwalker_state.json"
SECRET_FILE = DATA_DIR / "vodiwalker_secret.key"


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# LOCKS
# ============================================================

SAVE_LOCK = asyncio.Lock()
LINKS_LOCK = asyncio.Lock()
SUBS_LOCK = asyncio.Lock()
SESSIONS_LOCK = asyncio.Lock()


# ============================================================
# SECRET
# ============================================================

def load_or_create_secret() -> str:
    env_secret = os.environ.get("SECRET_KEY")

    if env_secret:
        return env_secret

    try:
        if SECRET_FILE.exists():
            existing = (
                SECRET_FILE
                .read_text(
                    encoding="utf-8"
                )
                .strip()
            )

            if existing:
                return existing

        generated = secrets.token_urlsafe(48)

        SECRET_FILE.write_text(
            generated,
            encoding="utf-8",
        )

        return generated

    except Exception as exc:
        logger.warning(
            "Could not persist SECRET_KEY: %s",
            exc,
        )

        return secrets.token_urlsafe(48)


SECRET_KEY = load_or_create_secret()


# ============================================================
# CONFIG
# ============================================================

CONFIG = {
    "port": PORT,
    "secret": SECRET_KEY,
    "host": os.environ.get(
        "RAILWAY_PUBLIC_DOMAIN",
        "localhost",
    ),
   
    "public_base_url": os.environ.get("PUBLIC_BASE_URL", "").strip(),
    "tcp_public_host": os.environ.get("TCP_PUBLIC_HOST", "").strip(),
    "tcp_public_port": os.environ.get("TCP_PUBLIC_PORT", "").strip(),
}


# ============================================================
# STATE
# ============================================================

LINKS: dict = {}
SUBS: dict = {}
# Per-subscription live usage samples. Values come from the real link used_bytes field.
SUB_USAGE_HISTORY = defaultdict(lambda: deque(maxlen=144))
USAGE_PERSIST_TASK = None
SESSIONS: dict = {}
connections: dict = {}
CATEGORIES: dict = {}
DAILY_STATS: dict = {}  # "YYYY-MM-DD" -> {"traffic_bytes":.., "new_links":.., "orders":.., "stars":..}
DAILY_STATS_LOCK = asyncio.Lock()


def _today_key() -> str:
    now = datetime.now(IRAN_TZ) if IRAN_TZ else datetime.now()
    return now.strftime("%Y-%m-%d")


def bump_daily_stat(field: str, amount=1):
    """Increment a counter in today's reporting bucket (best-effort, in-memory)."""
    try:
        key = _today_key()
        bucket = DAILY_STATS.setdefault(
            key, {"traffic_bytes": 0, "new_links": 0, "orders": 0, "stars": 0}
        )
        bucket[field] = bucket.get(field, 0) + amount
        # keep only the last 180 days to avoid unbounded growth
        if len(DAILY_STATS) > 180:
            for old_key in sorted(DAILY_STATS.keys())[: len(DAILY_STATS) - 180]:
                DAILY_STATS.pop(old_key, None)
    except Exception:
        pass

stats = {
    "total_bytes": 0,
    "total_requests": 0,
    "total_errors": 0,
    "start_time": time.time(),
}

_telemetry_lock = asyncio.Lock()
_telemetry_prev = {"ts": time.time(), "rx": 0, "tx": 0}


def _pct(v):
    try:
        return round(float(v), 1)
    except Exception:
        return 0.0


def _human_uptime(seconds):
    seconds = max(0, int(seconds))
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    if days:
        return f"{days}d {hours:02d}:{minutes:02d}"
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

error_logs = deque(maxlen=100)
activity_logs = deque(maxlen=250)

hourly_traffic = defaultdict(int)
# Real server telemetry samples used by the dashboard charts.
# Samples are collected from psutil; no placeholder/synthetic values are generated.
TELEMETRY_HISTORY = deque(maxlen=90)

http_client: httpx.AsyncClient | None = None


# ============================================================
# PROTOCOL
# ============================================================

PROTOCOLS = (
    "vless-ws",
    "vless-tcp",
    "xhttp-packet-up",
    "xhttp-stream-up",
    "xhttp-stream-one",
    "vmess-ws",
    "trojan-ws",
)

# این پروتکل‌ها روی همان پورت HTTP/WebSocket برنامه (پشت TLS ری‌ورس‌پروکسی یا Railway)
# سرو می‌شن و واقعاً روی سرور پیاده‌سازی شده‌ن.
REAL_TRANSPORT_PROTOCOLS = {
    "vless-ws", "xhttp-packet-up", "xhttp-stream-up",
}
# vless-tcp هم واقعی و پیاده‌سازی‌شده‌ست ولی روی یک پورت TCP خام و جداگانه
# (به‌صورت پیش‌فرض 6543، قابل تغییر با TCP_LISTEN_PORT) — نه پورت HTTP اصلی.
REAL_RAW_TCP_PROTOCOLS = {"vless-tcp"}
# همه‌ی پروتکل‌های دمو/غیرفعال از پنل حذف شده‌اند — هر چیزی که در PROTOCOLS باشد واقعاً کار می‌کند.
NON_FUNCTIONAL_DEMO_PROTOCOLS = {"vmess-ws", "trojan-ws"}

# Protocols that this project actually serves itself. VMess/Trojan entries may
# still be generated as client-side links, but they are NOT advertised as live
# listeners because this backend has no VMess/Trojan inbound parser.
LIVE_PROTOCOLS = REAL_TRANSPORT_PROTOCOLS | REAL_RAW_TCP_PROTOCOLS

PROTOCOL_LABELS = {
    "vless-ws": "VLESS WebSocket",
    "vless-tcp": "VLESS TCP (خام)",
    "xhttp-packet-up": "XHTTP Packet Up",
    "xhttp-stream-up": "XHTTP Stream Up",
    "xhttp-stream-one": "XHTTP Stream One",
    "vmess-ws": "VMess WebSocket",
    "trojan-ws": "Trojan WebSocket",
    "manual": "پروتکل دستی (سفارشی)",
}

PROTOCOL_ALIASES = {
    "vmess": "vmess-ws", "trojan": "trojan-ws", "ss": "shadowsocks",
    "socks": "socks5", "hy2": "hysteria2", "hysteria": "hysteria2",
}

DEFAULT_PROTOCOL = "vless-ws"

# نگاشت هر پروتکل غیر-دستی (manual) به Network/Security واقعی‌ای که در لینک
# نهایی (generate_vless_link) استفاده می‌شود. این فقط برای نمایش صحیح در پنل
# است (تگ‌های "ws/tls" و ...)؛ چون قبلاً این مقادیر همیشه روی مقدار پیش‌فرض
# فیلدهای دستی (tcp/none) می‌افتادند، حتی برای پروتکل‌هایی که واقعاً ws+tls بودند.
PROTOCOL_NETWORK_SECURITY = {
    "vless-ws": ("ws", "tls"),
    "vless-tcp": ("tcp", "none"),
    "xhttp-packet-up": ("xhttp", "tls"),
    "xhttp-stream-up": ("xhttp", "tls"),
    "xhttp-stream-one": ("xhttp", "tls"),
    "vmess-ws": ("ws", "tls"),
    "trojan-ws": ("ws", "tls"),
}

FINGERPRINTS = (
    "chrome",
    "firefox",
    "safari",
    "ios",
    "android",
    "edge",
    "360",
    "qq",
    "random",
    "randomized",
)

DEFAULT_FINGERPRINT = "chrome"

DEFAULT_ALPN_BY_PROTOCOL = {
    "vless-ws": "http/1.1",
    "xhttp-packet-up": "h2,http/1.1",
    "xhttp-stream-up": "h2,http/1.1",
    "xhttp-stream-one": "h2,http/1.1",
}

DEFAULT_PORT = 443
MIN_PORT = 1
MAX_PORT = 65535

DEFAULT_SPEED_LIMIT = 0


# ============================================================
# MANUAL PROTOCOL BUILDER (پروتکل دستی — مثل پنل‌های 3x-ui/Sanaei)
# ============================================================


MANUAL_BASE_PROTOCOLS = ("vless", "vmess", "trojan", "shadowsocks")

MANUAL_BASE_PROTOCOL_LABELS = {
    "vless": "VLESS",
    "vmess": "VMess",
    "trojan": "Trojan",
    "shadowsocks": "Shadowsocks",
}

NETWORKS = ("tcp", "ws", "grpc", "xhttp")

NETWORK_LABELS = {
    "tcp": "TCP",
    "ws": "WebSocket (ws)",
    "grpc": "gRPC",
    "xhttp": "XHTTP",
}

SECURITIES = ("none", "tls", "reality")

SECURITY_LABELS = {
    "none": "بدون امنیت (None)",
    "tls": "TLS",
    "reality": "Reality",
}

XHTTP_MODES = ("auto", "packet-up", "stream-up", "stream-one")
SHADOWSOCKS_METHODS = ("chacha20-ietf-poly1305", "aes-128-gcm", "aes-256-gcm", "2022-blake3-aes-128-gcm", "2022-blake3-aes-256-gcm")

# ترکیب‌هایی که همین پنل واقعاً به‌صورت زنده سرو می‌کند (بدون نیاز به Xray-core
# جداگانه). سایر ترکیب‌ها (مثل هر چیزی با Reality) فقط لینک/کانفیگ برای استفاده
# روی یک نود Xray-core واقعی می‌سازند و به همین دلیل در پنل با یک نشان
# «فقط ساخت لینک» مشخص می‌شوند — این محدودیت صادقانه در UI نشان داده می‌شود.
MANUAL_LIVE_COMBOS = {
    ("ws", "tls"),
    ("ws", "none"),
    ("xhttp", "tls"),
    ("xhttp", "none"),
    ("tcp", "none"),
}


def normalize_protocol(protocol: str | None) -> str:
    value = str(protocol or DEFAULT_PROTOCOL).strip().lower()
    value = PROTOCOL_ALIASES.get(value, value)
    if value == "manual":
        return value
    return value if value in PROTOCOLS else DEFAULT_PROTOCOL


def normalize_network(network: str | None) -> str:
    value = str(network or "tcp").strip().lower()
    return value if value in NETWORKS else "tcp"


def normalize_security(security: str | None) -> str:
    value = str(security or "none").strip().lower()
    return value if value in SECURITIES else "none"


def normalize_xhttp_mode(mode: str | None) -> str:
    value = str(mode or "auto").strip().lower()
    return value if value in XHTTP_MODES else "auto"


def normalize_base_protocol(value: str | None) -> str:
    v = str(value or "vless").strip().lower()
    return v if v in MANUAL_BASE_PROTOCOLS else "vless"


def protocol_display_label(link: dict) -> str:
    """برچسب نمایشی پروتکل برای جدول‌ها و گزارش‌ها.
    برای کانفیگ‌های دستی به‌صورت «VLESS · WebSocket · TLS» نمایش داده می‌شود."""
    protocol = link.get("protocol", DEFAULT_PROTOCOL)
    if protocol != "manual":
        return PROTOCOL_LABELS.get(protocol, protocol)
    base = MANUAL_BASE_PROTOCOL_LABELS.get(normalize_base_protocol(link.get("base_protocol")), "VLESS")
    network = NETWORK_LABELS.get(normalize_network(link.get("network")), "TCP")
    security = SECURITY_LABELS.get(normalize_security(link.get("security")), "بدون امنیت")
    if base == "Shadowsocks":
        return f"Shadowsocks · {network}"
    return f"{base} · {network} · {security}"


# ============================================================
# LOGGING
# ============================================================

def log_activity(
    kind: str,
    message: str,
    level: str = "info",
):
    activity_logs.append(
        {
            "kind": kind,
            "level": level,
            "message": message,
            "time": datetime.now().isoformat(),
        }
    )


# ============================================================
# HELPERS
# ============================================================

def escape_html(value) -> str:
    return (
        str(
            value
            if value is not None
            else ""
        )
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#039;")
    )


def safe_int(
    value,
    default=0,
    minimum=0,
    maximum=None,
):
    try:
        number = int(value)
    except Exception:
        number = default

    if number < minimum:
        number = minimum

    if maximum is not None and number > maximum:
        number = maximum

    return number


def safe_float(
    value,
    default=0.0,
    minimum=0.0,
):
    try:
        number = float(value)
    except Exception:
        number = default

    return max(
        minimum,
        number,
    )


def generate_uuid():
    value = secrets.token_hex(16)

    return (
        f"{value[:8]}-"
        f"{value[8:12]}-"
        f"{value[12:16]}-"
        f"{value[16:20]}-"
        f"{value[20:32]}"
    )


def random_config_name(existing=None):
    existing = existing or set()
    alphabet = string.ascii_lowercase + string.digits
    for _ in range(80):
        length = secrets.randbelow(6) + 8
        name = "".join(secrets.choice(alphabet) for _ in range(length))
        if name not in existing and name and not name[0].isdigit():
            return name
    return secrets.token_hex(6)

def sanitize_config_name(name: str) -> str:
    if not name:
        return random_config_name()
    cleaned = "".join(ch for ch in str(name) if ch.isascii() and ch.isalnum())
    if not cleaned or cleaned[0].isdigit():
        cleaned = ("a" + cleaned) if cleaned else random_config_name()
    return cleaned[:40]

def auto_config_name() -> str:
    return random_config_name()


def now_ir():
    if IRAN_TZ:
        return datetime.now(IRAN_TZ)

    return datetime.now()


def uptime():
    seconds = int(
        time.time()
        - stats["start_time"]
    )

    h = seconds // 3600

    m = (
        seconds
        % 3600
    ) // 60

    s = (
        seconds
        % 60
    )

    return (
        f"{h:02d}:"
        f"{m:02d}:"
        f"{s:02d}"
    )


def fmt_bytes(value: int):
    value = int(
        value or 0
    )

    if value < 1024:
        return f"{value} B"

    if value < 1024 ** 2:
        return (
            f"{value / 1024:.1f} KB"
        )

    if value < 1024 ** 3:
        return (
            f"{value / 1024 ** 2:.2f} MB"
        )

    return (
        f"{value / 1024 ** 3:.2f} GB"
    )


def parse_size_to_bytes(
    value: float,
    unit: str,
):
    if value <= 0:
        return 0

    unit = (
        unit
        or "GB"
    ).upper()

    if unit == "TB":
        return int(
            value
            * 1024 ** 4
        )

    if unit == "GB":
        return int(
            value
            * 1024 ** 3
        )

    if unit == "MB":
        return int(
            value
            * 1024 ** 2
        )

    if unit == "KB":
        return int(
            value
            * 1024
        )

    return int(value)


def parse_speed_to_bytes(
    value: float,
    unit: str,
):
    if value <= 0:
        return 0

    unit = (
        unit
        or "MBIT"
    ).upper()

    if unit == "MBIT":
        return int(
            value
            * 1024
            * 1024
            / 8
        )

    if unit == "KB":
        return int(
            value * 1024
        )

    if unit == "MB":
        return int(
            value
            * 1024
            * 1024
        )

    return int(value)


def is_link_expired(
    link: dict,
):
    expiry = link.get(
        "expires_at"
    )

    if not expiry:
        return False

    try:
        return (
            datetime.now()
            > datetime.fromisoformat(
                expiry
            )
        )

    except Exception:
        return False


def is_link_allowed(
    link: dict | None,
):
    if link is None:
        return False

    if not link.get(
        "active",
        True,
    ):
        return False

    if is_link_expired(link):
        return False

    limit = int(
        link.get(
            "limit_bytes",
            0,
        )
        or 0
    )

    used = int(
        link.get(
            "used_bytes",
            0,
        )
        or 0
    )

    if (
        limit > 0
        and used >= limit
    ):
        return False

    return True


def unique_ips_for_uuid(
    uuid: str,
):
    return {
        connection.get("ip")
        for connection in connections.values()
        if connection.get("uuid") == uuid
        and connection.get("ip")
    }


def client_ip(
    request: Request,
):
    forwarded = request.headers.get(
        "x-forwarded-for"
    )

    if forwarded:
        return (
            forwarded
            .split(",")[0]
            .strip()
        )

    real = request.headers.get(
        "x-real-ip"
    )

    if real:
        return real.strip()

    if request.client:
        return request.client.host

    return "unknown"


def is_ip_allowed(
    link: dict | None,
    uuid: str,
    ip: str,
):
    if link is None:
        return False

    limit = int(
        link.get(
            "ip_limit",
            0,
        )
        or 0
    )

    if limit <= 0:
        return True

    ips = unique_ips_for_uuid(uuid)

    if ip in ips:
        return True

    return len(ips) < limit


def _split_base_url(raw: str):
    """آدرس عمومی ذخیره‌شده رو به (scheme, host) تجزیه می‌کنه. ورودی می‌تونه
    با یا بدون scheme باشه (مثلاً 'panel.example.com' یا 'https://panel.example.com')."""
    raw = (raw or "").strip()
    if not raw:
        return None, None
    scheme = "https"
    rest = raw
    if "://" in raw:
        scheme, rest = raw.split("://", 1)
        scheme = scheme.strip().lower() or "https"
    host = rest.split("/", 1)[0].split(":")[0].strip()
    return (scheme if scheme in ("http", "https") else "https"), (host or None)


_DOMAIN_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$")


def _is_real_public_host(host) -> bool:
    """True فقط برای دامنه/آی‌پی عمومی واقعی؛ localhost / 0.0.0.0 / آی‌پی خصوصی / آدرس داخلی ریلوی → False."""
    h = str(host or "").strip().lower().strip("[]")
    if not h or h in ("localhost", "0.0.0.0", "::", "::1"):
        return False
    if h.endswith((".local", ".internal", ".localhost", ".lan")):
        return False
    try:
        return ipaddress.ip_address(h).is_global
    except ValueError:
        pass
    return bool(_DOMAIN_RE.match(h))


def _request_public_host(request) -> str | None:
    try:
        raw = request.headers.get("x-forwarded-host") or request.headers.get("host") or ""
        host = raw.split(",")[0].split(":")[0].strip().lower()
        return host if _is_real_public_host(host) else None
    except Exception:
        return None


def remember_public_host(request) -> None:
    """آدرس واقعی پنل را از اولین درخواست ادمینِ واردشده به خاطر می‌سپارد (برای ربات و لینک‌هایی که بدون درخواست ساخته می‌شوند)."""
    try:
        host = _request_public_host(request)
        if not host:
            return
        proto = (request.headers.get("x-forwarded-proto") or request.url.scheme or "https").split(",")[0].strip().lower()
        if proto not in ("http", "https"):
            proto = "https"
        _p = _capture_request_web(request)
        proto = _p[0]
        _port = str(_p[2] or "")
        if CONFIG.get("last_public_host") != host or CONFIG.get("last_public_scheme") != proto or str(CONFIG.get("last_public_port") or "") != _port:
            CONFIG["last_public_host"] = host
            CONFIG["last_public_scheme"] = proto
            CONFIG["last_public_port"] = _port
            asyncio.get_running_loop().create_task(save_state())
    except Exception:
        pass


def get_public_host_strict(request=None) -> str | None:
    """آدرس واقعی و قابل‌اتصال پنل؛ اگر هیچ آدرس معتبری پیدا نشود None (هرگز localhost/0.0.0.0 نمی‌دهد)."""
    _, override = _split_base_url(CONFIG.get("public_base_url"))
    if override and _is_real_public_host(override):
        return override
    if request is not None:
        host = _request_public_host(request)
        if host:
            return host
    env_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "").strip()
    if _is_real_public_host(env_domain):
        return env_domain
    last = str(CONFIG.get("last_public_host") or "").strip()
    if _is_real_public_host(last):
        return last
    cfg_host = str(CONFIG.get("host") or "").strip()
    if _is_real_public_host(cfg_host):
        return cfg_host
    return None


def get_public_base(request=None) -> str | None:
    host = get_public_host_strict(request)
    if not host:
        return None
    return get_web_base(host)


# ── آدرس عمومی با پورت (برای هاست‌هایی مثل KataBump که فقط IP:PORT و بدون SSL می‌دهند) ──
import contextvars as _cv_web
_REQ_WEB = _cv_web.ContextVar("req_web", default=None)  # (scheme, host, port|None)


def _split_base_url_full(raw: str):
    """(scheme, host, port|None) از آدرس عمومی ذخیره‌شده."""
    raw = (raw or "").strip()
    if not raw:
        return None, None, None
    scheme = "https"
    rest = raw
    if "://" in raw:
        scheme, rest = raw.split("://", 1)
        scheme = scheme.strip().lower() or "https"
    if scheme not in ("http", "https"):
        scheme = "https"
    auth = rest.split("/", 1)[0].strip()
    host, port = auth, None
    if auth.startswith("["):
        host = auth.split("]")[0] + "]"
        tail = auth.split("]", 1)[1]
        if tail.startswith(":") and tail[1:].isdigit():
            port = int(tail[1:])
    elif ":" in auth:
        h, p = auth.rsplit(":", 1)
        if p.isdigit():
            host, port = h, int(p)
    return scheme, (host or None), port


def _capture_request_web(request) -> tuple:
    """scheme/host/port واقعی درخواست فعلی را از هدرها می‌خواند."""
    h = request.headers
    raw_host = (h.get("x-forwarded-host") or h.get("host") or "").split(",")[0].strip()
    proto = (h.get("x-forwarded-proto") or request.url.scheme or "http").split(",")[0].strip().lower()
    if proto not in ("http", "https"):
        proto = "http"
    host, port = raw_host, None
    if raw_host.startswith("["):
        host = raw_host.split("]")[0] + "]"
        tail = raw_host.split("]", 1)[1]
        if tail.startswith(":") and tail[1:].isdigit():
            port = int(tail[1:])
    elif ":" in raw_host:
        hh, pp = raw_host.rsplit(":", 1)
        if pp.isdigit():
            host, port = hh, int(pp)
    if port is None:
        fp = (h.get("x-forwarded-port") or "").split(",")[0].strip()
        if fp.isdigit() and not ((proto == "https" and fp == "443") or (proto == "http" and fp == "80")):
            port = int(fp)
    return proto, host.lower(), port


def get_web_base(host: str | None = None) -> str:
    """scheme://host[:port] برای ساخت لینک‌های ساب/پنل. پورت غیراستاندارد حفظ می‌شود."""
    sch, h, p = _split_base_url_full(CONFIG.get("public_base_url"))
    if h:
        base_host, base_port, base_scheme = h, p, sch
    else:
        ctx = _REQ_WEB.get()
        if ctx and (host is None or ctx[1] == str(host).split(":")[0].strip().lower()):
            base_scheme, base_host, base_port = ctx
        else:
            base_host = (host or CONFIG.get("last_public_host") or CONFIG.get("host") or "localhost")
            base_host = str(base_host).split(":")[0].strip()
            base_scheme = CONFIG.get("last_public_scheme") or "https"
            lp = CONFIG.get("last_public_port")
            base_port = int(lp) if str(lp or "").isdigit() and CONFIG.get("last_public_host") == base_host else None
    if (base_scheme == "https" and base_port == 443) or (base_scheme == "http" and base_port == 80):
        base_port = None
    return f"{base_scheme}://{base_host}" + (f":{base_port}" if base_port else "")


def _links_use_tls() -> bool:
    """کانفیگ‌های WS/xhttp با TLS ساخته شوند یا بدون آن؟ (env: VW_TLS=1/0)"""
    env = os.environ.get("VW_TLS", "").strip().lower()
    if env in ("1", "true", "yes", "on"):
        return True
    if env in ("0", "false", "no", "off"):
        return False
    return get_scheme() == "https"


def get_host(
    request: Request | None = None,
) -> str:
    # اولویت اول: آدرس عمومی صریحی که در تنظیمات پنل ثبت شده (پایدار، مستقل از
    # اینکه درخواست از کجا اومده — پروکسی، آی‌پی داخلی، هلث‌چک و ...).
    _, override_host = _split_base_url(CONFIG.get("public_base_url"))
    if override_host:
        return override_host

    if request is not None:
        forwarded = request.headers.get(
            "x-forwarded-host"
        )

        normal = request.headers.get(
            "host"
        )

        host = (
            forwarded
            or normal
        )

        if host:
            # توجه: دیگه CONFIG["host"] رو اینجا آپدیت نمی‌کنیم؛ این یک متغیر سراسری
            # مشترک بین همه‌ی درخواست‌ها بود و هر درخواست با Host نادرست (هلث‌چک،
            # اسکنر، وبهوک) می‌تونست لینک‌های بعدیِ همه رو خراب کنه.
            return host.split(":")[0].strip()

    railway_domain = os.environ.get(
        "RAILWAY_PUBLIC_DOMAIN"
    )

    if railway_domain:
        return railway_domain

    # بدون درخواست (مثلاً ربات تلگرام): آدرس واقعیِ ذخیره‌شده؛ نه localhost فیک
    return get_public_host_strict() or CONFIG["host"]


def get_scheme() -> str:
    """scheme (http/https) که باید برای ساخت لینک‌های ساب استفاده بشه."""
    scheme, host = _split_base_url(CONFIG.get("public_base_url"))
    if host:
        return scheme
    ctx = _REQ_WEB.get()
    if ctx:
        return ctx[0]
    return CONFIG.get("last_public_scheme") or "https"


def _tcp_listen_port_snapshot() -> int:
    try:
        import tcp_relay
        return tcp_relay.TCP_LISTEN_PORT
    except Exception:
        return int(os.environ.get("TCP_LISTEN_PORT", "6543"))


def _bot_settings_snapshot() -> dict:
    """وضعیت فعلی ربات تلگرام رو برمی‌گردونه؛ اگه ماژول ربات هنوز ایمپورت نشده
    یا مشکلی داشته باشه، مقدار خالی/امن برمی‌گردونه (این نباید کل پنل رو خراب کنه)."""
    try:
        import telegram_bot
        return telegram_bot.current_config()
    except Exception:
        return {"bot_token": "", "admin_ids": "", "running": False}


# ============================================================
# PASSWORD
# ============================================================

def hash_password(
    password: str,
) -> str:

    payload = (
        password
        + SECRET_KEY
    ).encode("utf-8")

    return hashlib.sha256(
        payload
    ).hexdigest()


DEFAULT_ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin").strip() or "admin"
DEFAULT_ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")

AUTH = {
    "username": DEFAULT_ADMIN_USERNAME,
    "password_hash":
        hash_password(
            DEFAULT_ADMIN_PASSWORD
        )
}

# ============================================================
# MULTI-ADMIN (sub-admins beyond the owner account)
# ============================================================
# The "owner" account is always backed by AUTH["password_hash"] above
# (fully backward compatible with older single-admin deployments).
# Additional named admin accounts live here and can be managed from
# the "مدیریت ادمین‌ها" tab in the dashboard.

ADMINS: dict = {}

# ============================================================
# ADMIN REGISTRATION REQUESTS ("ثبت‌نام ادمینی" از صفحه لاگین)
# ============================================================
# کاربری که می‌خواهد ادمین شود، فقط نام و آیدی تلگرام خود را از صفحه
# لاگین ارسال می‌کند. درخواست او اینجا به‌صورت pending ذخیره می‌شود تا
# مالک پنل از بخش «مدیریت حساب‌ها» آن را ببیند، تصمیم بگیرد چه دسترسی‌ها
# و چه رمز/نام‌کاربری‌ای به او بدهد، و در صورت تایید حساب ادمین واقعی
# برایش ساخته شود.
ADMIN_REQUESTS: dict = {}
ADMIN_REQUEST_RATE: dict = {}  # ip -> last submit timestamp (ضد اسپم ساده)
ADMIN_REQUEST_COOLDOWN_SECONDS = 60
ADMIN_REQUESTS_LOCK = asyncio.Lock()

ALL_PERMISSIONS = {
    "dashboard": "مشاهده داشبورد",
    "inbounds": "مدیریت اینباند و کلاینت",
    "clients": "ساخت کلاینت (بخش جدا)",
    "subscriptions": "مدیریت سابسکریپشن",
    "categories": "مدیریت دسته‌بندی",
    "reports": "گزارش‌ها",
    "messages": "مرکز پیام و خطا",
    "bot": "مدیریت ربات",
    "admins": "مدیریت ادمین‌ها",
    "settings": "تنظیمات پنل",
    # --- دسترسی‌های جزئی (v2) ---
    "inbound_create": "ساخت اینباند جدید",
    "inbound_edit": "ویرایش اینباند",
    "inbound_delete": "حذف اینباند",
    "client_create": "ساخت کلاینت",
    "client_edit": "ویرایش کلاینت / تغییر وضعیت",
    "client_delete": "حذف کلاینت",
    "client_reset": "ریست مصرف کلاینت",
    "outbound_manage": "مدیریت خروجی / پراکسی",
    "live_connections": "مشاهده اتصال‌های زنده و IP",
}

# کلیدهای جزئی: برای ادمین‌های قدیمی (بدون perm_v2) با داشتن «inbounds» مجاز می‌مانند
GRANULAR_PERMISSIONS = {
    "inbound_create", "inbound_edit", "inbound_delete", "client_create", "client_edit",
    "client_delete", "client_reset", "outbound_manage", "live_connections",
}

import contextvars as _ctxvars
# وقتی مالک هنگام ساخت اینباند گزینه «محدودکردن ادمین به همین اینباند» را بزند، make_link از اینجا می‌خواند
_CREATE_RESTRICT = _ctxvars.ContextVar("vw_create_restrict", default=None)


def has_permission(admin_id: str, key: str) -> bool:
    if admin_id == "owner":
        return True
    a = ADMINS.get(admin_id) or {}
    perms = set(a.get("permissions") or {"dashboard"})
    if key in perms:
        return True
    if key in GRANULAR_PERMISSIONS and not a.get("perm_v2"):
        return "inbounds" in perms          # سازگاری با ادمین‌های قدیمی
    return False


def admin_scope(admin_id: str):
    """None = بدون محدودیت. وگرنه مجموعه‌ی UUID اینباندهایی که ادمین فقط به آن‌ها دسترسی دارد."""
    if admin_id == "owner":
        return None
    a = ADMINS.get(admin_id) or {}
    lst = a.get("allowed_inbounds") or []
    return set(lst) if lst else None


def link_in_scope(scope, uid: str) -> bool:
    if scope is None:
        return True
    if uid in scope:
        return True
    link = LINKS.get(uid) or {}
    return link.get("parent_inbound_id") in scope


def client_visible(link, actor_id: str) -> bool:
    """کلاینت فقط برای سازنده‌اش دیده می‌شود (کلاینت‌های قدیمی بدون created_by = مالک).
    باگ رفع‌شده: مالک همیشه همه‌چیز را می‌بیند — این محدودیت فقط بین ادمین‌ها اعمال می‌شود،
    نه روی مالک (وگرنه مالک اصلاً کلاینت‌های ساخته‌شده توسط ادمین‌ها را نمی‌دید)."""
    if actor_id == "owner":
        return True
    if not link.get("parent_inbound_id"):
        return True
    return (link.get("created_by") or "owner") == actor_id


async def actor_id_of(request: Request) -> str:
    info = await get_session_info(request.cookies.get(SESSION_COOKIE))
    return (info or {}).get("admin_id", "owner")


def scope_replace_uid(old: str, new: str):
    for a in ADMINS.values():
        lst = a.get("allowed_inbounds")
        if lst and old in lst:
            a["allowed_inbounds"] = [new if x == old else x for x in lst]


def scope_remove_uid(uid: str):
    for a in ADMINS.values():
        lst = a.get("allowed_inbounds")
        if lst and uid in lst:
            a["allowed_inbounds"] = [x for x in lst if x != uid]


def _apply_create_restrict(uid: str):
    """در make_link صدا زده می‌شود؛ ادمین انتخاب‌شده را به همین اینباند محدود می‌کند."""
    st = _CREATE_RESTRICT.get()
    if not st:
        return
    a = ADMINS.get(st["admin_id"])
    if not a:
        return
    if st["mode"] == "only" and not st["seen"]:
        a["allowed_inbounds"] = [uid]          # فقط همین یکی (جایگزین محدودیت‌های قبلی)
    else:
        lst = list(a.get("allowed_inbounds") or [])
        if uid not in lst:
            lst.append(uid)
        a["allowed_inbounds"] = lst
    st["seen"] += 1

BOT_TEXTS = {
    "welcome": "🛡 <b>VodiWalker Control Center</b>\n\nاز منوی زیر عملیات موردنظر را انتخاب کنید.",
    "admin_menu": "🛠 <b>مدیریت پنل</b>\n\nساخت اینباند، کلاینت و گروه ساب از همین‌جا در دسترس است.",
    "config_created": "✅ کانفیگ با موفقیت ساخته شد.",
    "config_deleted": "🗑 کانفیگ حذف شد.",
    "config_disabled": "⛔ کانفیگ غیرفعال شد.",
    "config_enabled": "✅ کانفیگ فعال شد.",
}

def get_bot_text(key: str, fallback: str = "") -> str:
    return str(BOT_TEXTS.get(key, fallback))

def permissions_for_admin(admin_id: str) -> set[str]:
    if admin_id == "owner":
        return set(ALL_PERMISSIONS)
    a = ADMINS.get(admin_id) or {}
    return set(a.get("permissions") or {"dashboard"})

async def require_permission(request: Request, permission: str):
    token = request.cookies.get(SESSION_COOKIE)
    info = await get_session_info(token)
    if not info:
        raise HTTPException(status_code=401, detail="unauthorized")
    if permission not in permissions_for_admin(info.get("admin_id", "owner")):
        raise HTTPException(status_code=403, detail="دسترسی این قابلیت برای این ادمین فعال نیست")
    return info


def verify_admin_credentials(username: str | None, password: str):
    """Returns (ok, admin_id, role, display_name)."""
    username = (username or "").strip()
    password = password or ""

    if not username or username.lower() in {"owner", AUTH.get("username", DEFAULT_ADMIN_USERNAME).lower()}:
        if username and username.lower() not in {"owner", AUTH.get("username", DEFAULT_ADMIN_USERNAME).lower()}:
            return False, None, None, None
        if hash_password(password) == AUTH["password_hash"]:
            return True, "owner", "owner", AUTH.get("username", DEFAULT_ADMIN_USERNAME)
        return False, None, None, None

    for admin_id, admin in ADMINS.items():
        if not admin.get("active", True):
            continue
        if admin.get("username", "").lower() == username.lower():
            if hash_password(password) == admin.get("password_hash"):
                return True, admin_id, admin.get("role", "admin"), admin.get("username")
            return False, None, None, None

    return False, None, None, None


# ============================================================
# LOGIN BRUTE-FORCE PROTECTION
# ============================================================
# Maximum failed login attempts per IP inside the rolling window.
LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 15 * 60
LOGIN_LOCKOUT_SECONDS = 15 * 60
LOGIN_MIN_PASSWORD_LENGTH = 6

LOGIN_FAILURES = defaultdict(deque)
LOGIN_LOCKED_UNTIL = {}


def _cleanup_login_state(ip: str, now: float | None = None):
    now = now if now is not None else time.time()

    locked_until = LOGIN_LOCKED_UNTIL.get(ip, 0)
    if locked_until and locked_until <= now:
        LOGIN_LOCKED_UNTIL.pop(ip, None)

    failures = LOGIN_FAILURES.get(ip)
    if not failures:
        return

    cutoff = now - LOGIN_WINDOW_SECONDS
    while failures and failures[0] <= cutoff:
        failures.popleft()

    if not failures:
        LOGIN_FAILURES.pop(ip, None)


def login_is_blocked(ip: str):
    now = time.time()
    _cleanup_login_state(ip, now)

    locked_until = LOGIN_LOCKED_UNTIL.get(ip, 0)
    if locked_until > now:
        return True, max(1, int(locked_until - now))

    return False, 0


def register_login_failure(ip: str):
    now = time.time()
    _cleanup_login_state(ip, now)

    failures = LOGIN_FAILURES.setdefault(ip, deque())
    failures.append(now)

    if len(failures) >= LOGIN_MAX_ATTEMPTS:
        LOGIN_LOCKED_UNTIL[ip] = now + LOGIN_LOCKOUT_SECONDS
        failures.clear()
        log_activity(
            "auth",
            f"IP به دلیل تلاش‌های متعدد ورود ناموفق به مدت {LOGIN_LOCKOUT_SECONDS // 60} دقیقه مسدود شد: {ip}",
            "err",
        )
        return True, LOGIN_LOCKOUT_SECONDS

    return False, max(0, LOGIN_MAX_ATTEMPTS - len(failures))


def clear_login_failures(ip: str):
    LOGIN_FAILURES.pop(ip, None)
    LOGIN_LOCKED_UNTIL.pop(ip, None)


# ============================================================
# SESSION
# ============================================================

SESSION_COOKIE = "vodiwalker_session"

SESSION_TTL = (
    60
    * 60
    * 24
    * 365
)


async def create_session(admin_id: str = "owner", role: str = "owner") -> str:

    token = secrets.token_urlsafe(48)

    async with SESSIONS_LOCK:
        SESSIONS[token] = {
            "exp": time.time() + SESSION_TTL,
            "admin_id": admin_id,
            "role": role,
            "permissions": sorted(permissions_for_admin(admin_id)),
        }

    return token


def _session_expiry(entry) -> float:
    if isinstance(entry, dict):
        return entry.get("exp", 0)
    return entry or 0


async def is_valid_session(
    token: str | None,
) -> bool:

    if not token:
        return False

    async with SESSIONS_LOCK:

        entry = SESSIONS.get(token)

        if entry is None:
            return False

        if _session_expiry(entry) < time.time():

            SESSIONS.pop(
                token,
                None,
            )

            return False

        return True


async def get_session_info(token: str | None):
    if not token:
        return None

    async with SESSIONS_LOCK:
        entry = SESSIONS.get(token)

        if entry is None:
            return None

        if _session_expiry(entry) < time.time():
            SESSIONS.pop(token, None)
            return None

        if isinstance(entry, dict):
            return dict(entry)

        return {"exp": entry, "admin_id": "owner", "role": "owner"}


async def require_owner(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    info = await get_session_info(token)

    if not info:
        raise HTTPException(status_code=401, detail="unauthorized")

    if info.get("role") != "owner":
        raise HTTPException(
            status_code=403,
            detail="فقط مالک پنل به این بخش دسترسی دارد",
        )

    return token


async def destroy_session(
    token: str | None,
):
    if not token:
        return

    async with SESSIONS_LOCK:
        SESSIONS.pop(
            token,
            None,
        )


# مقدار برگشتیِ require_auth وقتی درخواست با «توکن نود» (Bearer) احراز شده، نه نشست ادمین.
# get_session_info() برای این مقدار None می‌ده، پس endpointهای حساس (رمز، ادمین‌ها،
# نشست‌ها) که خودشون نشست واقعی می‌خوان با توکن نود هرگز کار نمی‌کنن.
NODE_API_TOKEN_MARK = "__vodiwalker_node_api__"


async def require_auth(
    request: Request,
):
    token = request.cookies.get(
        SESSION_COOKIE
    )

    info = await get_session_info(token)
    if not info:
        if request.headers.get("authorization"):
            try:
                from nodes import authorize_node_request
            except Exception:
                authorize_node_request = None
            if authorize_node_request and authorize_node_request(request):
                return NODE_API_TOKEN_MARK
        raise HTTPException(status_code=401, detail="unauthorized")
    remember_public_host(request)
    if info.get("admin_id") != "owner":
        path = request.url.path
        method = request.method.upper()
        aid = info.get("admin_id", "")
        permission = "dashboard"
        if path.startswith("/api/links") or path.startswith("/api/protocols") or path.startswith("/api/reality") or path.startswith("/api/proxies"):
            permission = "inbounds"
        elif path.startswith("/api/sub") or path.startswith("/sub"):
            permission = "subscriptions"
        elif path.startswith("/api/categories"):
            permission = "categories"
        elif path.startswith("/api/reports"):
            permission = "reports"
        elif path.startswith("/api/errors") or path.startswith("/api/activity"):
            permission = "messages"
        elif path.startswith("/api/settings/bot") or path.startswith("/api/bot"):
            permission = "bot"
        elif path.startswith("/api/settings"):
            permission = "settings"
        elif path.startswith("/api/telemetry") or path.startswith("/api/network"):
            permission = "dashboard"
        if permission not in permissions_for_admin(aid):
            raise HTTPException(status_code=403, detail="دسترسی این قابلیت برای این ادمین فعال نیست")

        scope = admin_scope(aid)
        await _enforce_granular_and_scope(request, aid, scope, path, method)
    else:
        await _prepare_owner_create_restrict(request)
    return token


_SCOPED_STATIC_OK = ("/api/protocols", "/api/telemetry", "/stats", "/api/me")
_LINK_SPECIAL = {"auto", "combo", "outbound"}


def _forbid(msg="این ادمین فقط به اینباند مشخص‌شده دسترسی دارد"):
    raise HTTPException(status_code=403, detail=msg)


async def _safe_json(request: Request):
    try:
        data = await request.json()
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _link_kind_perm(uid: str, inbound_key: str, client_key: str) -> str:
    link = LINKS.get(uid) or {}
    return client_key if link.get("parent_inbound_id") else inbound_key


async def _enforce_granular_and_scope(request: Request, aid: str, scope, path: str, method: str):
    parts = [x for x in path.split("/") if x]          # ['api','links','<uid>','clients',...]
    need = None
    uid = None

    if path.startswith("/api/links"):
        sub = parts[2] if len(parts) > 2 else None
        if sub in _LINK_SPECIAL:
            if method == "POST" and sub in ("auto", "combo"):
                need = "inbound_create"
            elif sub == "outbound":
                need = "outbound_manage"
        elif sub is None:
            if method == "POST":
                need = "inbound_create"
        else:
            uid = sub
            tail = parts[3] if len(parts) > 3 else None
            if tail is None:
                if method == "PATCH":
                    need = _link_kind_perm(uid, "inbound_edit", "client_edit")
                elif method == "DELETE":
                    need = _link_kind_perm(uid, "inbound_delete", "client_delete")
            elif tail == "clients":
                if method == "POST":
                    need = "client_create"
                elif method == "DELETE":
                    need = "client_delete"
            elif tail == "reset-usage":
                need = "client_reset"
            elif tail in ("action", "regenerate"):
                need = _link_kind_perm(uid, "inbound_edit", "client_edit")
    elif path.startswith("/api/proxies"):
        if method != "GET":
            need = "outbound_manage"
    elif path.startswith("/api/connections"):
        need = "live_connections"

    if need and not has_permission(aid, need):
        raise HTTPException(status_code=403, detail="دسترسی این قابلیت برای این ادمین فعال نیست")

    if scope is None:
        return

    # ---- ادمینِ محدود به اینباند مشخص ----
    if path.startswith("/api/links"):
        sub = parts[2] if len(parts) > 2 else None
        if sub is None:
            if method != "GET":
                _forbid("ادمین محدود‌شده نمی‌تواند اینباند جدید بسازد")
            return                                        # GET لیست؛ داخل endpoint فیلتر می‌شود
        if sub in _LINK_SPECIAL:
            if sub == "outbound":
                body = await _safe_json(request)
                for u in (body.get("uuids") or []):
                    if not link_in_scope(scope, str(u)):
                        _forbid()
                return
            _forbid("ادمین محدود‌شده نمی‌تواند اینباند جدید بسازد")
        if not link_in_scope(scope, sub) or sub not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        return
    if path.startswith(_SCOPED_STATIC_OK):
        return
    _forbid("این بخش برای ادمین محدود‌شده در دسترس نیست")


async def _prepare_owner_create_restrict(request: Request):
    """مالک هنگام ساخت اینباند می‌تواند restrict_admin_id بفرستد."""
    if request.method.upper() != "POST":
        return
    path = request.url.path
    if path not in ("/api/links", "/api/links/auto", "/api/links/combo"):
        return
    body = await _safe_json(request)
    rid = str(body.get("restrict_admin_id") or "").strip()
    if not rid or rid not in ADMINS:
        return
    mode = "add" if str(body.get("restrict_mode") or "only") == "add" else "only"
    _CREATE_RESTRICT.set({"admin_id": rid, "mode": mode, "seen": 0})


async def actor_scope(request: Request):
    info = await get_session_info(request.cookies.get(SESSION_COOKIE))
    if not info:
        return None
    return admin_scope(info.get("admin_id", "owner"))



def set_auth_cookie(
    response,
    request: Request,
    token: str,
):
    forwarded_proto = (
        request.headers
        .get(
            "x-forwarded-proto",
            "",
        )
        .lower()
    )

    is_https = (
        forwarded_proto == "https"
        or request.url.scheme == "https"
    )

    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        max_age=SESSION_TTL,
        httponly=True,
        samesite="lax",
        path="/",
        secure=is_https,
    )


# ============================================================
# VLESS LINK GENERATION
# ============================================================

def generate_vless_link(
    uuid: str, host: str, remark: str = "VodiWalker",
    protocol: str = DEFAULT_PROTOCOL, fingerprint: str | None = None,
    alpn: str | None = None, port: int | None = None,
):
    protocol = normalize_protocol(protocol)
    fp = (fingerprint or DEFAULT_FINGERPRINT).strip().lower()
    if fp not in FINGERPRINTS: fp = DEFAULT_FINGERPRINT
    port_value = safe_int(port, DEFAULT_PORT, MIN_PORT, MAX_PORT)
    _fp_env = os.environ.get("VW_FORCE_PORT", "").strip()
    if _fp_env.isdigit() and protocol != "vless-tcp":
        port_value = int(_fp_env)
    alpn_value = (alpn or DEFAULT_ALPN_BY_PROTOCOL.get(protocol, "http/1.1")).strip()
    label = quote(str(remark or "VodiWalker"), safe="")
    _tls = _links_use_tls()
    _sec = "tls" if _tls else "none"
    def _tlsq(q):
        if _tls:
            q.update({"sni": host, "fp": fp, "alpn": alpn_value})
        return q
    if protocol == "vless-ws":
        q = _tlsq({"encryption":"none","security":_sec,"type":"ws","host":host,"path":f"/ws/{uuid}"})
        return "vless://" + uuid + "@" + host + ":" + str(port_value) + "?" + "&".join(f"{k}={quote(str(v), safe=',/') }" for k,v in q.items()) + "#" + label
    if protocol == "vless-tcp":
        tcp_host = (CONFIG.get("tcp_public_host") or "").strip() or host
        tcp_port = safe_int(CONFIG.get("tcp_public_port"), port_value, MIN_PORT, MAX_PORT)
        q = {"encryption":"none","security":"none","type":"tcp","headerType":"none"}
        return "vless://" + uuid + "@" + tcp_host + ":" + str(tcp_port) + "?" + "&".join(f"{k}={quote(str(v), safe=',/') }" for k,v in q.items()) + "#" + label
    if protocol.startswith("xhttp-"):
        mode = protocol.replace("xhttp-", "")
        q = _tlsq({"encryption":"none","security":_sec,"type":"xhttp","mode":mode,"host":host,"path":f"/xhttp-siz10/{mode}/{uuid}"})
        return "vless://" + uuid + "@" + host + ":" + str(port_value) + "?" + "&".join(f"{k}={quote(str(v), safe=',/') }" for k,v in q.items()) + "#" + label
    if protocol == "vmess-ws":
        raw = {"v":"2","ps":remark,"add":host,"port":port_value,"id":uuid,"aid":0,"scy":"auto","net":"ws","type":"none","host":host,"path":f"/ws/{uuid}","tls":("tls" if _tls else "")}
        if _tls:
            raw.update({"sni":host,"fp":fp})
        return "vmess://" + base64.b64encode(json.dumps(raw,separators=(",",":"),ensure_ascii=False).encode()).decode()
    if protocol == "trojan-ws":
        return f"trojan://{uuid}@{host}:{port_value}?security={_sec}&type=ws&host={quote(host)}&path={quote('/ws/'+uuid)}" + (f"&sni={quote(host)}" if _tls else "") + f"#{label}"
    return f"vless://{uuid}@{host}:{port_value}"

# ============================================================
# SUBSCRIPTION REMARK TEMPLATE (configurable, Settings -> Subscription Template)
# ============================================================
def build_config_remark(link: dict, uid: str) -> str:
    """می‌سازه چه متنی به‌عنوان نام کانفیگ (#remark) داخل اپ کاربر دیده بشه.
    پیش‌فرض دقیقاً مثل قبل فقط «نام» است؛ مالک پنل از تب تنظیمات می‌تونه
    نمایش حجم/آی‌دی/نام اینباند رو هم فعال کنه."""
    show_name = bool(CONFIG.get("sub_remark_show_name", True))
    show_volume = bool(CONFIG.get("sub_remark_show_volume", False))
    show_id = bool(CONFIG.get("sub_remark_show_id", False))
    show_inbound = bool(CONFIG.get("sub_remark_show_inbound", False))

    name = str(link.get("label") or "Config").strip() or "Config"
    parts: list[str] = []

    if show_name:
        parts.append(name)

    if show_volume:
        try:
            limit_bytes = int(link.get("limit_bytes") or 0)
        except Exception:
            limit_bytes = 0
        parts.append(fmt_bytes(limit_bytes) if limit_bytes > 0 else "Unlimited")

    if show_id:
        parts.append(str(uid)[:8])

    if show_inbound:
        parent_id = link.get("parent_inbound_id")
        parent = LINKS.get(parent_id) if parent_id else None
        inbound_label = str((parent or {}).get("label") or "").strip()
        if inbound_label:
            parts.append(inbound_label)

    return " | ".join(p for p in parts if p) or name


def _remaining_time_text(expires_at) -> str:
    """متن «زمان باقی‌مانده» به‌شکل خلاصه (روز/ساعت/دقیقه) — برای ردیف تزئینی اطلاعات."""
    if not expires_at:
        return "∞"
    try:
        exp_dt = datetime.fromisoformat(str(expires_at))
        now_dt = datetime.now(exp_dt.tzinfo) if getattr(exp_dt, "tzinfo", None) else datetime.now()
        secs = int((exp_dt - now_dt).total_seconds())
        if secs <= 0:
            return "منقضی"
        days, rem = divmod(secs, 86400)
        hours, rem = divmod(rem, 3600)
        mins = rem // 60
        return f"{days}د {hours}س" if days else (f"{hours}س {mins}د" if hours else f"{mins}د")
    except Exception:
        return str(expires_at)[:16]


def build_info_server_remark(used_bytes: int, limit_bytes: int, expires_at) -> str:
    """متن نمایشیِ «سرور اطلاعاتی» که (در صورت فعال بودن از تنظیمات) به‌عنوان یک ردیف
    ردیف اطلاعاتی که با آدرس و UUID واقعی ساخته می‌شود (کانفیگ واقعی و قابل‌اتصال؛ هیچ آدرس فیکی
    در خروجی نوشته نمی‌شود) و حجم/زمان باقی‌مانده را به کاربر نشان می‌دهد."""
    show_volume = bool(CONFIG.get("sub_info_line_show_volume", True))
    show_expiry = bool(CONFIG.get("sub_info_line_show_expiry", True))
    parts = ["🌐 Vodiwalkerpanel"]
    if show_volume:
        used = int(used_bytes or 0)
        limit = int(limit_bytes or 0)
        remaining = max(0, limit - used) if limit > 0 else 0
        parts.append(
            f"{fmt_bytes(used)}/{fmt_bytes(limit)} (باقی {fmt_bytes(remaining)})"
            if limit > 0 else f"{fmt_bytes(used)}/∞"
        )
    if show_expiry:
        parts.append(_remaining_time_text(expires_at))
    return " | ".join(parts)


def build_manual_uri(
    link: dict,
    uid: str,
    host: str,
    port_override: int | None = None,
) -> str:
    """ساخت لینک کانفیگ برای حالت پروتکل دستی (Manual) — دقیقاً مثل پنل‌های
    3x-ui/Sanaei: پروتکل پایه + شبکه (Network) + امنیت (Security) + فیلدهای
    دستی (آدرس، پورت، مسیر، هاست هدر، SNI، Reality و ...) هر کدام جدا انتخاب
    می‌شن و لینک نهایی از روی آن‌ها ساخته می‌شود."""

    base_protocol = normalize_base_protocol(link.get("base_protocol"))
    network = normalize_network(link.get("network"))
    security = normalize_security(link.get("security"))

    remark = build_config_remark(link, uid)
    label = quote(remark, safe="")

    fp = (link.get("fingerprint") or DEFAULT_FINGERPRINT).strip().lower()
    if fp not in FINGERPRINTS:
        fp = DEFAULT_FINGERPRINT

    port_value = safe_int(
        port_override if port_override is not None else link.get("port"),
        DEFAULT_PORT, MIN_PORT, MAX_PORT,
    )

    address = (str(link.get("address") or "")).strip() or host
    default_alpn = "h2,http/1.1" if network == "xhttp" else "http/1.1"
    alpn_value = (str(link.get("alpn") or default_alpn)).strip()
    xhttp_mode = normalize_xhttp_mode(link.get("xhttp_mode"))
    path = (str(link.get("path") or "")).strip()
    if network == "xhttp":
        # ریلی فقط روی /xhttp-siz10/{mode}/{uuid}/... جواب می‌ده (mode باید packet-up یا
        # stream-up باشه، نه auto). مسیر قدیمیِ /xhttp/{uid} هیچ‌وقت وصل نمی‌شد، پس مثل «خالی» حساب می‌شه.
        if xhttp_mode == "auto":
            xhttp_mode = "packet-up"
        if not path or path == f"/xhttp/{uid}":
            path = f"/xhttp-siz10/{xhttp_mode}/{uid}"
    elif not path:
        path = f"/{network}/{uid}"
    host_header = (str(link.get("host_header") or "")).strip() or address
    sni = (str(link.get("sni") or "")).strip() or address
    flow = (str(link.get("flow") or "")).strip()
    grpc_service = (str(link.get("grpc_service_name") or "")).strip() or uid

    q: dict[str, str] = {}
    if base_protocol == "vless":
        q["encryption"] = "none"

    if security == "tls":
        q["security"] = "tls"
        q["sni"] = sni
        q["fp"] = fp
        q["alpn"] = alpn_value
        if link.get("allow_insecure"):
            q["allowInsecure"] = "1"
    elif security == "reality":
        q["security"] = "reality"
        q["sni"] = sni
        q["fp"] = fp
        q["pbk"] = (str(link.get("reality_public_key") or "")).strip()
        q["sid"] = (str(link.get("reality_short_id") or "")).strip()
        q["spx"] = (str(link.get("reality_spider_x") or "")).strip() or "/"
    else:
        q["security"] = "none"

    if network == "ws":
        q["type"] = "ws"
        q["path"] = path
        q["host"] = host_header
    elif network == "grpc":
        q["type"] = "grpc"
        q["serviceName"] = grpc_service
        q["mode"] = (str(link.get("grpc_mode") or "gun")).strip() or "gun"
    elif network == "xhttp":
        q["type"] = "xhttp"
        q["mode"] = xhttp_mode
        q["path"] = path
        q["host"] = host_header
    else:
        q["type"] = "tcp"
        header_type = (str(link.get("header_type") or "")).strip()
        if header_type:
            q["headerType"] = header_type
        if flow:
            q["flow"] = flow

    if base_protocol == "shadowsocks":
        method = str(link.get("ss_method") or "chacha20-ietf-poly1305").strip()
        password = str(link.get("ss_password") or uid).strip()
        if not method:
            method = "chacha20-ietf-poly1305"
        userinfo = f"{method}:{password}"
        token = base64.urlsafe_b64encode(userinfo.encode()).decode().rstrip("=")
        return f"ss://{token}@{address}:{port_value}#{label}"

    if base_protocol == "vmess":
        raw = {
            "v": "2", "ps": remark, "add": address, "port": port_value, "id": uid,
            "aid": 0, "scy": "auto", "net": network, "type": "none",
            "host": host_header if network in ("ws", "xhttp") else "",
            "path": grpc_service if network == "grpc" else path,
            "tls": security if security != "none" else "",
            "sni": sni, "fp": fp,
        }
        return "vmess://" + base64.b64encode(
            json.dumps(raw, separators=(",", ":"), ensure_ascii=False).encode()
        ).decode()

    scheme = "trojan" if base_protocol == "trojan" else "vless"
    qs = "&".join(f"{k}={quote(str(v), safe=',/')}" for k, v in q.items() if v not in (None, ""))
    return f"{scheme}://{uid}@{address}:{port_value}?{qs}#{label}"


def vless_link_for_link(
    link: dict,
    uid: str,
    host: str,
    port_override: int | None = None,
):
    protocol = normalize_protocol(link.get("protocol", DEFAULT_PROTOCOL))
    if protocol == "manual":
        return build_manual_uri(link, uid, host, port_override=port_override)
    return generate_vless_link(
        uid,
        host,
        remark=str(link.get("label") or "Config"),
        protocol=protocol,
        fingerprint=link.get(
            "fingerprint",
            DEFAULT_FINGERPRINT,
        ),
        alpn=link.get(
            "alpn"
        ),
        port=port_override if port_override is not None else link.get(
            "port",
            DEFAULT_PORT,
        ),
    )


def get_link_info(
    link: dict,
    uid: str,
    host: str,
):
    connected_count = len(unique_ips_for_uuid(uid))
    is_active = is_link_allowed(link)
    limit_b = int(link.get("limit_bytes", 0) or 0)
    used_b = int(link.get("used_bytes", 0) or 0)
    is_expired = is_link_expired(link) or (limit_b > 0 and used_b >= limit_b)
    if not is_active or is_expired:
        status_color = "red"
    elif connected_count > 0:
        status_color = "green"
    else:
        status_color = "gray"
    clean_ips = link.get("clean_ips") or []
    cfg_count = int(link.get("config_count") or 1)
    show_vless = len(clean_ips) <= 1 and cfg_count <= 1
    cat = CATEGORIES.get(str(link.get("category_id") or "0")) or {}
    protocol = normalize_protocol(link.get("protocol"))
    if protocol == "manual":
        display_network = normalize_network(link.get("network"))
        display_security = normalize_security(link.get("security"))
    else:
        display_network, display_security = PROTOCOL_NETWORK_SECURITY.get(
            protocol, ("tcp", "none")
        )
    manual_network = normalize_network(link.get("network"))
    manual_security = normalize_security(link.get("security"))
    manual_mode = normalize_xhttp_mode(link.get("xhttp_mode"))
    manual_live = (
        protocol == "manual"
        and normalize_base_protocol(link.get("base_protocol")) == "vless"
        and (manual_network, manual_security) in MANUAL_LIVE_COMBOS
        and not (manual_network == "xhttp" and manual_mode == "stream-one")
    )
    if protocol == "manual":
        live_status = "live" if manual_live else "link-only"
    elif protocol in LIVE_PROTOCOLS:
        live_status = "live"
    else:
        live_status = "link-only"
    return {
        "uuid": uid,
        "name": link.get("label", ""),
        "label": link.get("label", ""),
        "protocol": link.get("protocol", DEFAULT_PROTOCOL),
        "protocol_display": protocol_display_label(link),
        "base_protocol": normalize_base_protocol(link.get("base_protocol")),
        "network": display_network,
        "security": display_security,
        "manual_live": manual_live,
        "live_status": live_status,
        "live_reason": ("این پروتکل توسط هسته فعلی سرو می‌شود." if live_status == "live" else "فقط لینک ساخته می‌شود؛ برای اجرای واقعی این ترکیب به Xray-core/Inbound خارجی نیاز است."),
        "address": link.get("address", ""),
        "path": link.get("path", ""),
        "host_header": link.get("host_header", ""),
        "sni": link.get("sni", ""),
        "flow": link.get("flow", ""),
        "grpc_service_name": link.get("grpc_service_name", ""),
        "grpc_mode": link.get("grpc_mode", "gun"),
        "xhttp_mode": normalize_xhttp_mode(link.get("xhttp_mode")),
        "header_type": link.get("header_type", ""),
        "allow_insecure": bool(link.get("allow_insecure", False)),
        "reality_public_key": link.get("reality_public_key", ""),
        "reality_short_id": link.get("reality_short_id", ""),
        "reality_spider_x": link.get("reality_spider_x", "/"),
        "active": is_active,
        "used_bytes": used_b,
        "limit_bytes": limit_b,
        "expires_at": link.get("expires_at"),
        "ip_limit": int(link.get("ip_limit", 0) or 0),
        "speed_limit_bytes": int(link.get("speed_limit_bytes", 0) or 0),
        "connection_limit": int(link.get("connection_limit", 0) or 0),
        "fragment": link.get("fragment", "off"),
        "fingerprint": link.get("fingerprint", DEFAULT_FINGERPRINT),
        "alpn": link.get("alpn", ""),
        "port": link.get("port", DEFAULT_PORT),
        "note": link.get("note", ""),
        "clean_ips": clean_ips,
        "alarm_enabled": bool(link.get("alarm_enabled", False)),
        "category_id": str(link.get("category_id") or "0"),
        "category_number": int(cat.get("number", 0)),
        "category_name": str(cat.get("name", "عمومی")),
        "config_count": cfg_count,
        "client_limit": int(link.get("client_limit") or 0),
        "outbound_proxy_id": str(link.get("outbound_proxy_id") or ""),
        "operator": str(link.get("operator") or ""),
        "outbound": outbound_info(link.get("outbound_proxy_id")),
        "combo_group_id": link.get("combo_group_id") or "",
        "parent_inbound_id": link.get("parent_inbound_id"),
        "is_client": bool(link.get("parent_inbound_id")),
        "status_color": status_color,
        "connected_ips": connected_count,
        "show_vless": show_vless,
        "vless": vless_link_for_link(link, uid, host) if show_vless else "",
        "vless_full": vless_link_for_link(link, uid, host),
        "sub": f"{get_web_base(host)}/sub/{uid}",
        "info": f"{get_web_base(host)}/info/{uid}",
        "support": get_support_username(),
        "support_url": get_support_url(),
    }


# ============================================================
# PERSISTENCE
# ============================================================

async def load_state():

    global AUTH

    try:

        DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not DATA_FILE.exists():
            return

        async with aiofiles.open(
            DATA_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            raw = await file.read()

        data = json.loads(raw)

        LINKS.update(
            data.get(
                "links",
                {},
            )
        )

        SUBS.update(
            data.get(
                "subs",
                {},
            )
        )

        CATEGORIES.update(
            data.get(
                "categories",
                {},
            )
        )

        stored_username = data.get("username")
        if isinstance(stored_username, str) and stored_username.strip():
            AUTH["username"] = stored_username.strip()

        stored_password = data.get(
            "password_hash"
        )

        if stored_password:
            AUTH[
                "password_hash"
            ] = stored_password

        ADMINS.update(
            data.get("admins", {})
        )

        ADMIN_REQUESTS.update(
            data.get("admin_requests", {})
        )

        DAILY_STATS.update(
            data.get("daily_stats", {})
        )

        # بازیابی تنظیمات پنل (آدرس عمومی + مشخصات ربات تلگرام)
        BOT_TEXTS.update(data.get("bot_texts") or {})
        settings_data = data.get("settings") or {}
        if settings_data.get("public_base_url"):
            CONFIG["public_base_url"] = str(settings_data.get("public_base_url") or "").strip()
        if settings_data.get("tcp_public_host"):
            CONFIG["tcp_public_host"] = str(settings_data.get("tcp_public_host") or "").strip()
        if settings_data.get("tcp_public_port"):
            CONFIG["tcp_public_port"] = str(settings_data.get("tcp_public_port") or "").strip()
        CONFIG["bot_auto_start"] = bool(settings_data.get("bot_auto_start", False))
        for _k in PERSISTED_EXTRA_SETTINGS:
            if _k in settings_data:
                CONFIG[_k] = settings_data[_k]
        try:
            import telegram_bot
            telegram_bot.configure(
                token=settings_data.get("bot_token"),
                admin_ids_raw=settings_data.get("bot_admin_ids"),
            )
        except Exception as exc:
            logger.warning("Could not restore bot settings: %s", exc)

        # Compatibility for older records
        for uid, link in LINKS.items():

            link.setdefault(
                "protocol",
                DEFAULT_PROTOCOL,
            )

            link.setdefault(
                "fingerprint",
                DEFAULT_FINGERPRINT,
            )

            link.setdefault(
                "alpn",
                "",
            )

            link.setdefault(
                "port",
                DEFAULT_PORT,
            )

            link.setdefault(
                "ip_limit",
                0,
            )

            link.setdefault(
                "speed_limit_bytes",
                0,
            )

            link.setdefault(
                "connection_limit",
                0,
            )

            link.setdefault(
                "fragment",
                "off",
            )

            link.setdefault(
                "used_bytes",
                0,
            )
            link.setdefault("clean_ips", [])
            link.setdefault("alarm_enabled", False)
            link.setdefault("category_id", "0")
            link.setdefault("config_count", 1)
            link.setdefault("client_limit", 0)
            link.setdefault("usage_history", [])
            link.setdefault("parent_inbound_id", None)

        logger.info(
            "State loaded: %d links / %d subscriptions",
            len(LINKS),
            len(SUBS),
        )

    except Exception as exc:

        logger.exception(
            "Could not load state: %s",
            exc,
        )


async def save_state():

    async with SAVE_LOCK:

        try:

            DATA_DIR.mkdir(
                parents=True,
                exist_ok=True,
            )

            payload = {
                "links":
                    dict(LINKS),

                "subs":
                    dict(SUBS),

                "categories":
                    dict(CATEGORIES),

                "username": AUTH.get("username", DEFAULT_ADMIN_USERNAME),

                "password_hash":
                    AUTH[
                        "password_hash"
                    ],

                "admins":
                    dict(ADMINS),

                "admin_requests":
                    dict(ADMIN_REQUESTS),

                "daily_stats":
                    dict(DAILY_STATS),

                # تنظیمات پنل: آدرس عمومی + مشخصات ربات تلگرام (برای اینکه با ری‌استارت
                # سرویس از دست نرن و نیازی به .env دستی نباشه).
                "bot_texts": BOT_TEXTS,
                "settings": {
                    "public_base_url": CONFIG.get("public_base_url", ""),
                    "tcp_public_host": CONFIG.get("tcp_public_host", ""),
                    "tcp_public_port": CONFIG.get("tcp_public_port", ""),
                    "bot_token": _bot_settings_snapshot().get("bot_token", ""),
                    "bot_admin_ids": _bot_settings_snapshot().get("admin_ids", ""),
                    "bot_auto_start": bool(CONFIG.get("bot_auto_start", False)),
                    **{k: CONFIG[k] for k in PERSISTED_EXTRA_SETTINGS if k in CONFIG},
                },

                "saved_at":
                    datetime.now().isoformat(),
            }

            temp_file = (
                DATA_FILE.with_suffix(
                    ".tmp"
                )
            )

            async with aiofiles.open(
                temp_file,
                "w",
                encoding="utf-8",
            ) as file:

                await file.write(
                    json.dumps(
                        payload,
                        ensure_ascii=False,
                        indent=2,
                    )
                )

            temp_file.replace(
                DATA_FILE
            )

        except Exception as exc:

            logger.exception(
                "Could not save state: %s",
                exc,
            )


# ============================================================
# DEFAULT LINK
# ============================================================

_default_link_created = False



async def ensure_default_categories():
    if CATEGORIES:
        return
    CATEGORIES["0"] = {
        "id": "0", "name": "عمومی", "number": 0,
        "limit_bytes": 0, "expires_days": 0, "connection_limit": 0,
        "speed_limit_bytes": 0, "ip_limit": 0, "clean_ips": [],
        "random_name": False, "single_user": False,
        "created_at": datetime.now().isoformat(),
    }
    CATEGORIES["1"] = {
        "id": "1", "name": "VIP", "number": 1,
        "limit_bytes": 0, "expires_days": 0, "connection_limit": 1,
        "speed_limit_bytes": 0, "ip_limit": 1, "clean_ips": [],
        "random_name": False, "single_user": True,
        "created_at": datetime.now().isoformat(),
    }
    asyncio.create_task(save_state())

async def ensure_default_link():

    global _default_link_created

    if _default_link_created:
        return

    async with LINKS_LOCK:

        if not any(
            item.get("is_default")
            for item in LINKS.values()
        ):

            digest = hashlib.sha256(
                (
                    "default"
                    + SECRET_KEY
                ).encode("utf-8")
            ).hexdigest()

            uid = (
                f"{digest[:8]}-"
                f"{digest[8:12]}-"
                f"{digest[12:16]}-"
                f"{digest[16:20]}-"
                f"{digest[20:32]}"
            )

            LINKS[uid] = {
                "label":
                    "لینک پیش‌فرض",

                "limit_bytes":
                    0,

                "used_bytes":
                    0,

                "created_at":
                    datetime.now().isoformat(),

                "active":
                    True,

                "expires_at":
                    None,

                "note":
                    "",

                "is_default":
                    True,

                "sub_id":
                    None,

                "protocol":
                    DEFAULT_PROTOCOL,

                "fingerprint":
                    DEFAULT_FINGERPRINT,

                "alpn":
                    "http/1.1",

                "port":
                    DEFAULT_PORT,

                "ip_limit":
                    0,

                "speed_limit_bytes":
                    DEFAULT_SPEED_LIMIT,

                "connection_limit":
                    0,

                "fragment":
                    "off",
            }

            asyncio.create_task(
                save_state()
            )

    _default_link_created = True


# ============================================================
# LINK MANAGEMENT
# ============================================================

def clean_outbound_proxy_id(value) -> str:
    """'' = مستقیم (خود Railway). غیرخالی باید شناسه‌ی یک پراکسی موجود باشه."""
    pid = str(value or "").strip()
    if not pid:
        return ""
    try:
        from outbound_proxy import get_proxy
    except Exception:
        raise HTTPException(status_code=400, detail="ماژول پراکسی خروجی در دسترس نیست")
    if not get_proxy(pid):
        raise HTTPException(status_code=400, detail="پراکسی انتخاب‌شده پیدا نشد (شاید حذف شده)")
    return pid


def public_remote_links(entries: list) -> list:
    """نسخه‌ی امن یک لیست عضو ریموت برای پنل (بدون خودِ رشته‌ی vless)."""
    try:
        from nodes import get_node
    except Exception:
        get_node = lambda _id: None
    out = []
    for e in entries:
        node = get_node(e.get("node_id") or "")
        out.append({
            "id": f"{e.get('node_id')}:{e.get('uuid')}",
            "node_id": e.get("node_id"),
            "node_name": (node or {}).get("name") or "نود حذف‌شده",
            "node_online": bool(node),
            "node_missing": bool(e.get("node_missing")),
            "uuid": e.get("uuid"),
            "label": e.get("label", ""),
            "protocol_display": e.get("protocol_display", ""),
            "active": bool(e.get("active", True)),
            "last_error": e.get("last_error", ""),
            "last_synced_at": e.get("last_synced_at"),
            "added_at": e.get("added_at"),
        })
    return out


def outbound_info(value):
    """خلاصه‌ی نام/کشور/پرچم پراکسی خروجی برای نمایش در پنل (None = مستقیم)."""
    pid = str(value or "").strip()
    if not pid:
        return None
    try:
        from outbound_proxy import proxy_summary
        return proxy_summary(pid)
    except Exception:
        return None


async def make_link(
    label: str = "لینک جدید",
    limit_bytes: int = 0,
    expires_at: str | None = None,
    note: str = "",
    sub_id: str | None = None,
    protocol: str = DEFAULT_PROTOCOL,
    fingerprint: str = DEFAULT_FINGERPRINT,
    alpn: str = "",
    port: int = DEFAULT_PORT,
    ip_limit: int = 0,
    speed_limit_bytes: int = 0,
    connection_limit: int = 0,
    fragment: str = "off",
    clean_ips=None,
    alarm_enabled: bool = False,
    category_id: str = "0",
    config_count: int = 1,
    manual_fields: dict | None = None,
    outbound_proxy_id: str = "",
):

    protocol = normalize_protocol(protocol)
    manual_fields = manual_fields or {}

    fingerprint = (
        fingerprint
        or DEFAULT_FINGERPRINT
    ).strip().lower()

    if fingerprint not in FINGERPRINTS:
        fingerprint = DEFAULT_FINGERPRINT

    if not (
        MIN_PORT
        <= port
        <= MAX_PORT
    ):
        port = DEFAULT_PORT

    uid = generate_uuid()

    record = {
        "label":
            (sanitize_display_name((label or "").strip()) if (label or "").strip() else random_config_name()),

        "limit_bytes":
            max(
                0,
                int(limit_bytes),
            ),

        "used_bytes":
            0,

        "created_at":
            datetime.now().isoformat(),

        "active":
            True,

        "expires_at":
            expires_at,

        "note":
            (
                note
                or ""
            ).strip()[:500],

        "is_default":
            False,

        "sub_id":
            sub_id,

        # A child client is a real live credential: it owns its own UUID and is
        # therefore accepted by the VLESS/XHTTP relay exactly like the parent.
        "parent_inbound_id": None,

        "protocol":
            protocol,

        "fingerprint":
            fingerprint,

        "alpn":
            (
                alpn
                or ""
            ).strip()[:100],

        "port":
            port,

        "ip_limit":
            max(
                0,
                int(ip_limit),
            ),

        "speed_limit_bytes":
            max(
                0,
                int(speed_limit_bytes),
            ),

        "connection_limit":
            max(
                0,
                int(connection_limit),
            ),

        "fragment":
            (
                fragment
                or "off"
            ).strip().lower(),

        "security_profile": "balanced",
        "multi_login": False,
        "clean_ips": list(clean_ips or []),
        "alarm_enabled": bool(alarm_enabled),
        "category_id": str(category_id or "0"),
        "config_count": max(1, min(40, int(config_count or 1))),
        "client_limit": 0,
        "usage_history": [],
        # مسیر خروجی: خالی = مستقیم از روی Railway. غیرخالی = شناسه‌ی یک پراکسی
        # SOCKS از outbound_proxy.py که ارتباط با مقصد از طریق اون رد می‌شه.
        "outbound_proxy_id": str(outbound_proxy_id or "").strip(),
    }

    if protocol == "manual":
        record.update({
            "base_protocol": normalize_base_protocol(manual_fields.get("base_protocol")),
            "network": normalize_network(manual_fields.get("network")),
            "security": normalize_security(manual_fields.get("security")),
            "address": str(manual_fields.get("address") or "").strip()[:255],
            "path": str(manual_fields.get("path") or "").strip()[:255],
            "host_header": str(manual_fields.get("host_header") or "").strip()[:255],
            "sni": str(manual_fields.get("sni") or "").strip()[:255],
            "flow": str(manual_fields.get("flow") or "").strip()[:64],
            "grpc_service_name": str(manual_fields.get("grpc_service_name") or "").strip()[:128],
            "grpc_mode": str(manual_fields.get("grpc_mode") or "gun").strip()[:32] or "gun",
            "xhttp_mode": normalize_xhttp_mode(manual_fields.get("xhttp_mode")),
            "header_type": str(manual_fields.get("header_type") or "").strip()[:32],
            "allow_insecure": bool(manual_fields.get("allow_insecure", False)),
            "reality_public_key": str(manual_fields.get("reality_public_key") or "").strip()[:128],
            "reality_short_id": str(manual_fields.get("reality_short_id") or "").strip()[:32],
            "reality_spider_x": str(manual_fields.get("reality_spider_x") or "/").strip()[:128] or "/",
            "ss_method": str(manual_fields.get("ss_method") or "chacha20-ietf-poly1305").strip()[:80],
            "ss_password": str(manual_fields.get("ss_password") or uid).strip()[:255],
        })

    record["protocol_label"] = protocol_display_label(record)

    async with LINKS_LOCK:
        LINKS[uid] = record
        if not record.get("parent_inbound_id"):
            _apply_create_restrict(uid)

    bump_daily_stat("new_links")

    if sub_id:

        async with SUBS_LOCK:

            if sub_id in SUBS:

                ids = SUBS[
                    sub_id
                ].setdefault(
                    "link_ids",
                    [],
                )

                if uid not in ids:
                    ids.append(uid)

    await save_state()

    log_activity(
        "link",
        (
            f"کانفیگ "
            f"«{record['label']}» "
            f"ساخته شد"
        ),
        "ok",
    )

    return uid, record


async def remove_link(
    uid: str,
):

    async with LINKS_LOCK:

        if uid not in LINKS:
            return None

        label = LINKS[
            uid
        ].get(
            "label",
            uid,
        )

        sub_id = LINKS[
            uid
        ].get(
            "sub_id"
        )

        del LINKS[uid]
        scope_remove_uid(uid)

    if sub_id:

        async with SUBS_LOCK:

            if sub_id in SUBS:

                ids = SUBS[
                    sub_id
                ].get(
                    "link_ids",
                    [],
                )

                if uid in ids:
                    ids.remove(uid)

    await save_state()

    log_activity(
        "link",
        (
            f"کانفیگ "
            f"«{label}» "
            f"حذف شد"
        ),
        "warn",
    )

    return label


async def update_link_fields(
    uid: str,
    *,
    label: str | None = None,
    add_bytes: int | None = None,
    set_limit_bytes: int | None = None,
    extend_days: int | None = None,
    reset_usage: bool = False,
    ip_limit: int | None = None,
    speed_limit_bytes: int | None = None,
):
    """ویرایش امن فیلدهای یک کانفیگ (برای ربات تلگرام): نام، حجم، تمدید، ریست مصرف و ..."""
    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if link is None:
            return None
        if label is not None:
            value = str(label).strip()[:60]
            if value:
                link["label"] = value
        if reset_usage:
            link["used_bytes"] = 0
        if set_limit_bytes is not None:
            link["limit_bytes"] = max(0, int(set_limit_bytes))
        if add_bytes:
            link["limit_bytes"] = max(0, int(link.get("limit_bytes") or 0)) + int(add_bytes)
        if extend_days:
            now = datetime.now()
            base = now
            try:
                cur = datetime.fromisoformat(str(link.get("expires_at"))) if link.get("expires_at") else None
                if cur is not None and cur.tzinfo is None and cur > now:
                    base = cur
            except Exception:
                pass
            link["expires_at"] = (base + timedelta(days=int(extend_days))).isoformat()
        if ip_limit is not None:
            link["ip_limit"] = max(0, int(ip_limit))
        if speed_limit_bytes is not None:
            link["speed_limit_bytes"] = max(0, int(speed_limit_bytes))
        record = link
    await save_state()
    return record


async def set_link_active(
    uid: str,
    active: bool,
):

    async with LINKS_LOCK:

        if uid not in LINKS:
            return None

        LINKS[
            uid
        ][
            "active"
        ] = bool(active)

        record = LINKS[uid]

    await save_state()

    log_activity(
        "link",
        (
            f"کانفیگ "
            f"«{record['label']}» "
            f"{'فعال' if active else 'غیرفعال'} شد"
        ),
        "ok"
        if active
        else "warn",
    )

    return record


# ============================================================
# SUB GROUPS
# ============================================================

async def create_sub_group(
    name: str = "گروه جدید",
    desc: str = "",
    password: str = "",
):

    name = (
        name
        or "گروه جدید"
    ).strip()[:60]

    desc = (
        desc
        or ""
    ).strip()[:200]

    password = (
        password
        or ""
    ).strip()

    sub_id = generate_uuid()

    uuid_key = secrets.token_urlsafe(16)

    record = {
        "name":
            name,

        "desc":
            desc,

        "password_hash":
            (
                hash_password(password)
                if password
                else None
            ),

        "uuid_key":
            uuid_key,

        "created_at":
            datetime.now().isoformat(),

        "link_ids":
            [],

        "remote_links":
            [],
    }

    async with SUBS_LOCK:
        SUBS[sub_id] = record

    await save_state()

    log_activity(
        "sub",
        (
            f"گروه "
            f"«{name}» "
            f"ساخته شد"
        ),
        "ok",
    )

    return (
        sub_id,
        record,
    )


async def set_link_sub(
    uid: str,
    sub_id: str | None,
):

    async with LINKS_LOCK:

        if uid not in LINKS:
            return False

        old_sub = LINKS[
            uid
        ].get(
            "sub_id"
        )

        label = LINKS[
            uid
        ].get(
            "label",
            uid,
        )

    if sub_id is not None:

        async with SUBS_LOCK:

            if sub_id not in SUBS:
                return False

    async with SUBS_LOCK:

        if (
            old_sub
            and old_sub in SUBS
        ):

            ids = SUBS[
                old_sub
            ].get(
                "link_ids",
                [],
            )

            if uid in ids:
                ids.remove(uid)

        if (
            sub_id
            and sub_id in SUBS
        ):

            ids = SUBS[
                sub_id
            ].setdefault(
                "link_ids",
                [],
            )

            if uid not in ids:
                ids.append(uid)

    async with LINKS_LOCK:

        if uid in LINKS:

            LINKS[
                uid
            ][
                "sub_id"
            ] = sub_id

    await save_state()

    log_activity(
        "link",
        (
            f"کانفیگ "
            f"«{label}» "
            f"{'به گروه اضافه شد' if sub_id else 'از گروه خارج شد'}"
        ),
        "info",
    )

    return True


async def remove_sub_group(
    sub_id: str,
):

    async with SUBS_LOCK:

        if sub_id not in SUBS:
            return None

        name = SUBS[
            sub_id
        ].get(
            "name",
            sub_id,
        )

        del SUBS[sub_id]

    async with LINKS_LOCK:

        for link in LINKS.values():

            if (
                link.get("sub_id")
                == sub_id
            ):
                link["sub_id"] = None

    await save_state()

    log_activity(
        "sub",
        (
            f"گروه "
            f"«{name}» "
            f"حذف شد"
        ),
        "warn",
    )

    return name


async def usage_history_loop():
    """Persist live usage history periodically so the customer graph survives restarts."""
    while True:
        try:
            await asyncio.sleep(60)
            now = now_ir()
            ts = now.replace(second=0, microsecond=0).isoformat()
            changed = False
            async with LINKS_LOCK:
                for link in LINKS.values():
                    history = link.setdefault("usage_history", [])
                    used = int(link.get("used_bytes", 0) or 0)
                    limit = int(link.get("limit_bytes", 0) or 0)
                    if history and str(history[-1].get("ts", ""))[:16] == ts[:16]:
                        if history[-1].get("used") != used or history[-1].get("limit") != limit:
                            history[-1]["used"] = used
                            history[-1]["limit"] = limit
                            changed = True
                    else:
                        history.append({"ts": ts, "used": used, "limit": limit})
                        if len(history) > 144:
                            del history[:-144]
                        changed = True
            if changed:
                await save_state()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.warning("Usage history loop error: %s", exc)


# ============================================================
# STARTUP
# ============================================================

# ---- VodiWalker v18: Telegram proxy + operator presets ----
try:
    import tg_proxy as _tg_proxy
    import operators as _operators
    _operators.register(app, require_auth, DATA_DIR)
    _tg_proxy.register(app, require_auth, DATA_DIR, logger)
    from ui_assets import HERO_JPG as _HERO_JPG
    from fastapi.responses import Response as _Resp

    @app.get("/assets/vw-hero.jpg")
    async def _vw_hero():
        return _Resp(_HERO_JPG, media_type="image/jpeg", headers={"Cache-Control": "public, max-age=604800"})
except Exception as _exc:  # پنل بدون این ماژول‌ها هم باید بالا بیاید
    logger.warning("v18 modules skipped: %s", _exc)


@app.on_event("startup")
async def startup():

    global http_client, USAGE_PERSIST_TASK

    limits = httpx.Limits(
        max_connections=500,
        max_keepalive_connections=100,
    )

    timeout = httpx.Timeout(
        30.0,
        connect=10.0,
    )

    http_client = httpx.AsyncClient(
        limits=limits,
        timeout=timeout,
        follow_redirects=True,
    )

    await load_state()

    USAGE_PERSIST_TASK = asyncio.create_task(usage_history_loop())

    await ensure_default_categories()
    await ensure_default_link()

    log_activity(
        "system",
        (
            f"{APP_NAME} "
            f"v{APP_VERSION} "
            f"راه‌اندازی شد"
        ),
        "ok",
    )

    logger.info(
        "%s v%s started on 0.0.0.0:%s",
        APP_NAME,
        APP_VERSION,
        PORT,
    )

    logger.info(
        "Data directory: %s",
        DATA_DIR,
    )

    try:
        import tcp_relay
        await tcp_relay.start_tcp_relay(app_logger=logger)
    except Exception as exc:
        logger.warning("VLESS-TCP relay startup skipped: %s", exc)


@app.on_event("shutdown")
async def shutdown():

    global USAGE_PERSIST_TASK
    if USAGE_PERSIST_TASK:
        USAGE_PERSIST_TASK.cancel()
        try:
            await USAGE_PERSIST_TASK
        except asyncio.CancelledError:
            pass
        USAGE_PERSIST_TASK = None

    await save_state()

    if http_client:
        await http_client.aclose()

    try:
        import tcp_relay
        await tcp_relay.stop_tcp_relay()
    except Exception:
        pass


# ============================================================
# LANDING
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # The old public landing/interstitial page has been removed.
    # Visitors go straight to the real login page; authenticated users go to the dashboard.
    if await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse("/dashboard")
    return RedirectResponse("/login")



# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": APP_NAME,
        "version": APP_VERSION,
        "connections": len(connections),
        "uptime": uptime(),
    }


# ============================================================
# LIVE TELEMETRY
# ============================================================

@app.get("/api/telemetry")
async def api_telemetry(_=Depends(require_auth)):
    """Lightweight live server metrics for the dashboard."""
    global _telemetry_prev
    now = time.time()
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage(str(DATA_DIR))
    cpu = psutil.cpu_percent(interval=None)
    load = None
    try:
        load = [round(x, 2) for x in os.getloadavg()]
    except Exception:
        load = []
    net = psutil.net_io_counters()
    async with _telemetry_lock:
        prev = _telemetry_prev
        dt = max(0.25, now - float(prev.get("ts", now)))
        rx_rate = max(0, net.bytes_recv - int(prev.get("rx", net.bytes_recv))) / dt
        tx_rate = max(0, net.bytes_sent - int(prev.get("tx", net.bytes_sent))) / dt
        _telemetry_prev = {"ts": now, "rx": net.bytes_recv, "tx": net.bytes_sent}
    process = psutil.Process(os.getpid())
    sample = {
        "ts": datetime.now().isoformat(),
        "cpu": _pct(cpu),
        "ram": _pct(vm.percent),
        "swap": _pct(swap.percent),
        "storage": _pct(disk.percent),
        "rx_bps": int(rx_rate),
        "tx_bps": int(tx_rate),
        "connections": len(connections),
    }
    TELEMETRY_HISTORY.append(sample)
    return {
        "ok": True,
        "cpu": _pct(cpu),
        "cpu_cores": psutil.cpu_count(logical=True) or 1,
        "ram": {"percent": _pct(vm.percent), "used": vm.used, "total": vm.total},
        "swap": {"percent": _pct(swap.percent), "used": swap.used, "total": swap.total},
        "storage": {"percent": _pct(disk.percent), "used": disk.used, "total": disk.total},
        "network": {"rx_bps": int(rx_rate), "tx_bps": int(tx_rate), "bytes_recv": int(net.bytes_recv), "bytes_sent": int(net.bytes_sent)},
        "connections": len(connections),
        "traffic_bytes": int(stats.get("total_bytes", 0)),
        "requests": int(stats.get("total_requests", 0)),
        "errors": int(stats.get("total_errors", 0)),
        "uptime": _human_uptime(now - stats.get("start_time", now)),
        "load": load,
        "process": {"rss": process.memory_info().rss, "cpu": _pct(process.cpu_percent(interval=None))},
        "bot_running": bool(_bot_settings_snapshot().get("running")),
        "history": list(TELEMETRY_HISTORY),
    }


# ============================================================
# LOGIN
# ============================================================

from pages import LOGIN_HTML
from pages import ASSET_ICONS_B64, ASSET_VAZIR_B64, ASSET_QR_JS_B64, UI_CSS

_ASSET_ICONS_BYTES = base64.b64decode(ASSET_ICONS_B64)
_ASSET_VAZIR_BYTES = base64.b64decode(ASSET_VAZIR_B64)
_ASSET_QR_BYTES = base64.b64decode(ASSET_QR_JS_B64)
_ASSET_CACHE = {"Cache-Control": "public, max-age=604800, immutable"}


@app.get("/assets/ui.css", include_in_schema=False)
async def asset_ui_css():
    return Response(UI_CSS, media_type="text/css; charset=utf-8", headers=_ASSET_CACHE)


@app.get("/assets/qr.js", include_in_schema=False)
async def asset_qr_js():
    return Response(_ASSET_QR_BYTES, media_type="application/javascript; charset=utf-8", headers=_ASSET_CACHE)


@app.get("/assets/icons.woff2", include_in_schema=False)
async def asset_icons_font():
    return Response(_ASSET_ICONS_BYTES, media_type="font/woff2", headers=_ASSET_CACHE)


_ASSET_VW_LOGO = base64.b64decode(
    "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"
)


@app.get("/assets/vw.png", include_in_schema=False)
async def asset_vw_logo():
    return Response(_ASSET_VW_LOGO, media_type="image/png", headers=_ASSET_CACHE)


@app.get("/assets/vazir.woff2", include_in_schema=False)
async def asset_vazir_font():
    return Response(_ASSET_VAZIR_BYTES, media_type="font/woff2", headers=_ASSET_CACHE)



def login_error_html(
    message: str,
):
    safe_message = escape_html(
        message
    )

    error_block = f'<div class="error" role="alert">{safe_message}</div>'

    if "<!--LOGIN_ERROR-->" in LOGIN_HTML:
        return LOGIN_HTML.replace("<!--LOGIN_ERROR-->", error_block, 1)

    return LOGIN_HTML.replace("</form>", error_block + "</form>", 1)


@app.get(
    "/login",
    response_class=HTMLResponse,
)
async def login_page(
    request: Request,
):

    if await is_valid_session(
        request.cookies.get(
            SESSION_COOKIE
        )
    ):
        return RedirectResponse(
            "/dashboard"
        )

    return HTMLResponse(
        LOGIN_HTML
    )


@app.post("/login")
async def login_form(
    request: Request,
):

    try:

        content_type = (
            request.headers
            .get(
                "content-type",
                "",
            )
            .lower()
        )

        if "application/json" in content_type:

            body = await request.json()

            password = str(
                body.get(
                    "password",
                    "",
                )
            ).strip()

            login_username = str(
                body.get(
                    "username",
                    "",
                )
            ).strip()

        else:

            raw = await request.body()

            parsed = parse_qs(
                raw.decode(
                    "utf-8",
                    errors="ignore",
                )
            )

            password = (
                parsed.get(
                    "password",
                    [""],
                )[0]
                .strip()
            )

            login_username = (
                parsed.get(
                    "username",
                    [""],
                )[0]
                .strip()
            )

    except Exception as exc:

        logger.exception(
            "Login parser error: %s",
            exc,
        )

        return HTMLResponse(
            login_error_html(
                "خطا در پردازش اطلاعات ورود."
            ),
            status_code=400,
        )

    ip = client_ip(request)

    blocked, retry_after = login_is_blocked(ip)
    if blocked:
        minutes = max(1, (retry_after + 59) // 60)
        return HTMLResponse(
            login_error_html(
                f"به دلیل تلاش‌های ناموفق متعدد، ورود موقتاً مسدود شده است. حدود {minutes} دقیقه دیگر دوباره تلاش کنید."
            ),
            status_code=429,
            headers={"Retry-After": str(retry_after)},
        )

    if not password:
        register_login_failure(ip)
        return HTMLResponse(
            login_error_html(
                "رمز عبور را وارد کنید."
            ),
            status_code=400,
        )

    ok, admin_id, role, display_name = verify_admin_credentials(login_username, password)

    if not ok:

        locked, value = register_login_failure(ip)
        if locked:
            return HTMLResponse(
                login_error_html(
                    "تعداد تلاش‌های ناموفق بیش از حد مجاز بود. این IP برای ۱۵ دقیقه مسدود شد."
                ),
                status_code=429,
                headers={"Retry-After": str(LOGIN_LOCKOUT_SECONDS)},
            )

        remaining = value
        log_activity(
            "auth",
            (
                f"تلاش ورود ناموفق از {ip}؛ "
                f"{remaining} تلاش باقی مانده"
            ),
            "err",
        )

        return HTMLResponse(
            login_error_html(
                f"رمز عبور اشتباه است. {remaining} تلاش دیگر باقی مانده است."
            ),
            status_code=401,
        )

    clear_login_failures(ip)

    if admin_id != "owner" and admin_id in ADMINS:
        ADMINS[admin_id]["last_login_at"] = datetime.now().isoformat()
        ADMINS[admin_id]["last_login_ip"] = ip
        asyncio.create_task(save_state())

    token = await create_session(admin_id, role)

    response = RedirectResponse(
        "/dashboard?login=1",
        status_code=303,
    )

    set_auth_cookie(
        response,
        request,
        token,
    )

    log_activity(
        "auth",
        (
            f"ورود موفق «{display_name or admin_id}» به پنل "
            f"از {client_ip(request)}"
        ),
        "ok",
    )

    return response


@app.post("/api/login")
async def api_login(
    request: Request,
):

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="JSON نامعتبر است",
        )

    password = str(
        body.get(
            "password",
            "",
        )
    ).strip()

    login_username = str(
        body.get(
            "username",
            "",
        )
    ).strip()

    ip = client_ip(request)

    blocked, retry_after = login_is_blocked(ip)
    if blocked:
        raise HTTPException(
            status_code=429,
            detail=f"ورود موقتاً مسدود است. حدود {max(1, (retry_after + 59) // 60)} دقیقه دیگر تلاش کنید.",
            headers={"Retry-After": str(retry_after)},
        )

    if not password:
        register_login_failure(ip)
        raise HTTPException(
            status_code=400,
            detail="رمز عبور را وارد کنید",
        )

    ok, admin_id, role, display_name = verify_admin_credentials(login_username, password)

    if not ok:

        locked, value = register_login_failure(ip)
        if locked:
            raise HTTPException(
                status_code=429,
                detail="تعداد تلاش‌های ناموفق بیش از حد مجاز بود. این IP برای ۱۵ دقیقه مسدود شد.",
                headers={"Retry-After": str(LOGIN_LOCKOUT_SECONDS)},
            )

        log_activity(
            "auth",
            (
                f"تلاش ورود ناموفق از {ip}؛ "
                f"{value} تلاش باقی مانده"
            ),
            "err",
        )

        raise HTTPException(
            status_code=401,
            detail=f"رمز عبور اشتباه است؛ {value} تلاش دیگر باقی مانده است",
        )

    clear_login_failures(ip)

    if admin_id != "owner" and admin_id in ADMINS:
        ADMINS[admin_id]["last_login_at"] = datetime.now().isoformat()
        ADMINS[admin_id]["last_login_ip"] = ip
        asyncio.create_task(save_state())

    log_activity(
        "auth",
        f"ورود موفق «{display_name or admin_id}» به پنل از {ip}",
        "ok",
    )

    token = await create_session(admin_id, role)

    response = JSONResponse(
        {
            "ok": True,
            "authenticated": True,
            "admin": {"id": admin_id, "username": display_name or admin_id, "role": role},
        }
    )

    set_auth_cookie(
        response,
        request,
        token,
    )

    return response


# ============================================================
# LOGOUT
# ============================================================

@app.get("/logout")
async def logout_page(
    request: Request,
):

    await destroy_session(
        request.cookies.get(
            SESSION_COOKIE
        )
    )

    response = RedirectResponse(
        "/login"
    )

    response.delete_cookie(
        SESSION_COOKIE,
        path="/",
    )

    return response


@app.post("/api/logout")
async def api_logout(
    request: Request,
):

    await destroy_session(
        request.cookies.get(
            SESSION_COOKIE
        )
    )

    response = JSONResponse(
        {
            "ok": True
        }
    )

    response.delete_cookie(
        SESSION_COOKIE,
        path="/",
    )

    return response


@app.get("/api/me")
async def api_me(
    request: Request,
):

    info = await get_session_info(
        request.cookies.get(SESSION_COOKIE)
    )

    if not info:
        return {"authenticated": False}

    admin_id = info.get("admin_id", "owner")
    role = info.get("role", "owner")

    if admin_id == "owner":
        username = AUTH.get("username", DEFAULT_ADMIN_USERNAME)
    else:
        admin = ADMINS.get(admin_id, {})
        username = admin.get("username", admin_id)

    _a = ADMINS.get(admin_id, {}) if admin_id != "owner" else {}
    return {
        "authenticated": True,
        "admin": {
            "id": admin_id, "username": username, "role": role,
            "permissions": sorted(permissions_for_admin(admin_id)),
            "granted": sorted(k for k in ALL_PERMISSIONS if has_permission(admin_id, k)),
            "allowed_inbounds": list(_a.get("allowed_inbounds") or []),
            "scoped": bool(_a.get("allowed_inbounds")),
        },
    }


# ============================================================
# CHANGE PASSWORD
# ============================================================

@app.get("/api/system/diagnostics")
async def api_system_diagnostics(request: Request, token=Depends(require_auth)):
    """Authenticated live diagnostics used by the Pro dashboard."""
    try:
        import psutil
        proc = psutil.Process(os.getpid())
        vm = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=None)
        mem = proc.memory_info().rss
        net = psutil.net_io_counters()
        disk = psutil.disk_usage("/")
        bot = _bot_settings_snapshot()
        async with LINKS_LOCK:
            links_snapshot = dict(LINKS)
        async with SUBS_LOCK:
            subs_snapshot = dict(SUBS)
        active = sum(1 for x in links_snapshot.values() if is_link_allowed(x))
        clients = sum(1 for x in links_snapshot.values() if x.get("parent_inbound_id"))
        inbounds = len(links_snapshot) - clients
        return {
            "ok": True,
            "time": datetime.now().isoformat(),
            "uptime": _human_uptime(time.time() - stats.get("start_time", time.time())),
            "service": {"status": "healthy", "version": "VodiWalker Pro"},
            "resources": {
                "cpu_percent": round(float(cpu), 1),
                "memory_rss": int(mem),
                "memory_percent": round(float(proc.memory_percent()), 1),
                "system_memory_percent": round(float(vm.percent), 1),
                "disk_percent": round(float(disk.percent), 1),
                "rx_bytes": int(net.bytes_recv),
                "tx_bytes": int(net.bytes_sent),
            },
            "objects": {
                "inbounds": max(0, inbounds),
                "clients": clients,
                "active_links": active,
                "subscriptions": len(subs_snapshot),
                "admins": len(ADMINS) + 1,
                "errors": len(error_logs),
            },
            "bot": {"running": bool(bot.get("running")), "admin_count": len(bot.get("admin_ids", "").split(",")) if bot.get("admin_ids") else 0},
            "security": {"session_count": len(SESSIONS), "username": AUTH.get("username", DEFAULT_ADMIN_USERNAME)},
        }
    except Exception as exc:
        logger.exception("Diagnostics error: %s", exc)
        raise HTTPException(status_code=500, detail="Diagnostics unavailable")


@app.post("/api/security/revoke-other-sessions")
async def api_revoke_other_sessions(request: Request, token=Depends(require_auth)):
    info = await get_session_info(token)
    if not info:
        raise HTTPException(status_code=401, detail="نشست نامعتبر است")
    admin_id = info.get("admin_id", "owner")
    removed = 0
    async with SESSIONS_LOCK:
        stale = [tok for tok, sess in SESSIONS.items() if tok != token and isinstance(sess, dict) and sess.get("admin_id", "owner") == admin_id]
        for tok in stale:
            SESSIONS.pop(tok, None)
            removed += 1
    log_activity("auth", f"نشست‌های قبلی حساب «{AUTH.get('username') if admin_id == 'owner' else ADMINS.get(admin_id, {}).get('username', admin_id)}» لغو شد", "warn")
    return {"ok": True, "revoked": removed}


@app.post("/api/change-password")
async def api_change_password(
    request: Request,
    token=Depends(require_auth),
):
    # نکته مهم (رفع باگ): این endpoint قبلاً همیشه رمز عبور مالک (owner) را
    # چک/جایگزین می‌کرد، حتی وقتی یک ادمین فرعی (sub-admin) وارد شده بود.
    # نتیجه: تغییر رمز برای ادمین‌های فرعی یا با خطای «رمز فعلی اشتباه است»
    # مواجه می‌شد (چون با هش رمز owner مقایسه می‌شد)، یا در بدترین حالت رمز
    # owner را به‌جای رمز خودِ ادمین overwrite می‌کرد. همچنین همه‌ی session های
    # تمام ادمین‌ها پاک می‌شد. اینجا اول مشخص می‌کنیم کدام حساب (owner یا کدام
    # sub-admin) درخواست را زده، سپس دقیقاً همان حساب را چک/آپدیت می‌کنیم و
    # فقط نشست‌های همان حساب باطل می‌شوند، نه بقیه‌ی ادمین‌ها.

    info = await get_session_info(token)
    if not info:
        raise HTTPException(status_code=401, detail="نشست نامعتبر است، دوباره وارد شوید")

    admin_id = info.get("admin_id", "owner")
    is_owner = admin_id == "owner"
    admin_record = None if is_owner else ADMINS.get(admin_id)

    if not is_owner and not admin_record:
        raise HTTPException(status_code=401, detail="حساب کاربری یافت نشد")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="اطلاعات نامعتبر است",
        )

    current_password = str(body.get("current_password", ""))
    current_hash = AUTH["password_hash"] if is_owner else admin_record.get("password_hash", "")

    if hash_password(current_password) != current_hash:
        raise HTTPException(
            status_code=400,
            detail="رمز فعلی اشتباه است",
        )

    new_password = str(body.get("new_password", ""))
    repeat_password = str(body.get("repeat_password", ""))

    if len(new_password) < 8:
        raise HTTPException(
            status_code=400,
            detail="رمز جدید باید حداقل ۸ کاراکتر باشد",
        )

    if new_password == current_password:
        raise HTTPException(
            status_code=400,
            detail="رمز جدید باید با رمز فعلی متفاوت باشد",
        )

    if new_password != repeat_password:
        raise HTTPException(
            status_code=400,
            detail="تکرار رمز عبور یکسان نیست",
        )

    new_hash = hash_password(new_password)

    if is_owner:
        AUTH["password_hash"] = new_hash
    else:
        admin_record["password_hash"] = new_hash

    async with SESSIONS_LOCK:
        # فقط نشست‌های همین حساب باطل می‌شوند (نه همه‌ی ادمین‌ها)، اما نشست
        # فعلی زنده می‌ماند تا کاربر بلافاصله logout نشود.
        stale = [
            tok for tok, sess in SESSIONS.items()
            if sess.get("admin_id", "owner") == admin_id and tok != token
        ]
        for tok in stale:
            SESSIONS.pop(tok, None)

        SESSIONS[token] = {
            "exp": time.time() + SESSION_TTL,
            "admin_id": admin_id,
            "role": info.get("role", "owner" if is_owner else "admin"),
            "permissions": sorted(permissions_for_admin(admin_id)),
        }

    await save_state()

    log_activity(
        "auth",
        "رمز عبور پنل تغییر کرد" if is_owner else f"رمز عبور ادمین «{admin_record.get('username', admin_id)}» تغییر کرد",
        "ok",
    )

    return {
        "ok": True
    }


# ============================================================
# CHANGE USERNAME
# ============================================================

@app.post("/api/change-username")
async def api_change_username(
    request: Request,
    token=Depends(require_auth),
):
    info = await get_session_info(token)
    if not info:
        raise HTTPException(status_code=401, detail="نشست نامعتبر است، دوباره وارد شوید")

    admin_id = info.get("admin_id", "owner")
    is_owner = admin_id == "owner"
    admin_record = None if is_owner else ADMINS.get(admin_id)
    if not is_owner and not admin_record:
        raise HTTPException(status_code=401, detail="حساب کاربری یافت نشد")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    username = str(body.get("username", "")).strip()
    if not username:
        raise HTTPException(status_code=400, detail="نام کاربری نمی‌تواند خالی باشد")
    if len(username) < 3 or len(username) > 40:
        raise HTTPException(status_code=400, detail="نام کاربری باید بین ۳ تا ۴۰ کاراکتر باشد")
    if any(ch.isspace() for ch in username):
        raise HTTPException(status_code=400, detail="نام کاربری نباید فاصله داشته باشد")
    if username.lower() == "owner":
        raise HTTPException(status_code=400, detail="این نام کاربری رزرو شده است")

    current = AUTH.get("username", DEFAULT_ADMIN_USERNAME) if is_owner else admin_record.get("username", admin_id)
    for aid, admin in ADMINS.items():
        if aid != admin_id and str(admin.get("username", "")).lower() == username.lower():
            raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")
    if is_owner and username.lower() in {str(a.get("username", "")).lower() for a in ADMINS.values()}:
        raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")

    if is_owner:
        AUTH["username"] = username
    else:
        admin_record["username"] = username

    async with SESSIONS_LOCK:
        sess = SESSIONS.get(token)
        if sess:
            sess["exp"] = time.time() + SESSION_TTL

    await save_state()
    log_activity("auth", f"نام کاربری «{current}» به «{username}» تغییر کرد", "ok")
    return {"ok": True, "username": username}


# ============================================================
# CREATE LINK
# ============================================================


@app.get("/api/network/railway")
async def railway_network_info(_=Depends(require_auth)):
    """Return Railway networking hints without exposing secrets."""
    return {
        "is_railway": bool(os.environ.get("RAILWAY_PROJECT_ID") or os.environ.get("RAILWAY_ENVIRONMENT_ID")),
        "public_domain": os.environ.get("RAILWAY_PUBLIC_DOMAIN", ""),
        "tcp_proxy_domain": os.environ.get("RAILWAY_TCP_PROXY_DOMAIN", ""),
        "tcp_proxy_port": safe_int(os.environ.get("RAILWAY_TCP_PROXY_PORT", "0"), minimum=0, maximum=65535),
        "tcp_application_port": safe_int(os.environ.get("RAILWAY_TCP_APPLICATION_PORT", "0"), minimum=0, maximum=65535),
        "app_port": safe_int(os.environ.get("PORT", "0"), minimum=0, maximum=65535),
    }


@app.post("/api/network/tcp-ping")
async def tcp_ping(request: Request, _=Depends(require_auth)):
    """Server-side TCP connectivity test for an address/port entered in the builder."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات تست اتصال معتبر نیست.")
    host = str(body.get("host") or body.get("address") or "").strip()
    port = safe_int(body.get("port", 0), minimum=1, maximum=65535)
    timeout = min(max(float(body.get("timeout", 4.0) or 4.0), 0.5), 8.0)
    if not host:
        raise HTTPException(status_code=400, detail="آدرس سرور را وارد کنید.")
    if not port:
        raise HTTPException(status_code=400, detail="پورت باید بین 1 تا 65535 باشد.")
    started = time.perf_counter()
    try:
        infos = await asyncio.get_running_loop().run_in_executor(None, lambda: __import__('socket').getaddrinfo(host, port, type=__import__('socket').SOCK_STREAM))
        resolved = []
        for info in infos:
            addr = info[4][0]
            if addr not in resolved:
                resolved.append(addr)
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        return {"ok": True, "host": host, "port": port, "latency_ms": round((time.perf_counter()-started)*1000, 1), "resolved": resolved[:6], "message": "اتصال TCP برقرار شد."}
    except asyncio.TimeoutError:
        return {"ok": False, "host": host, "port": port, "latency_ms": round((time.perf_counter()-started)*1000, 1), "message": "Timeout: سرور در زمان تعیین‌شده پاسخ نداد."}
    except Exception as exc:
        return {"ok": False, "host": host, "port": port, "latency_ms": round((time.perf_counter()-started)*1000, 1), "message": f"اتصال ناموفق: {type(exc).__name__}: {str(exc)[:180]}"}


# ═══════════════ Telegram Mini App (روی آدرس خود پنل: /app) ═══════════════
TMA_HTML = r"""<!doctype html><html lang="fa" dir="rtl" translate="no" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no"><meta name="google" content="notranslate"><title>VodiWalker</title>
<link rel="stylesheet" href="/assets/ui.css"><script src="https://telegram.org/js/telegram-web-app.js"></script><script src="/assets/qr.js"></script>
<style>
:root{--bg:#070b11;--s1:#0e151e;--s2:#141d29;--ln:rgba(255,255,255,.07);--ln2:rgba(255,255,255,.14);--ac:#4cd7f6;--ac2:#7c8cff;--ok:#34d399;--wn:#fbbf24;--bd:#fb7185;--tx:#e8eef7;--sb:#8593a8;--sb2:#566377;--glow:rgba(76,215,246,.16)}
[data-theme=light]{--bg:#eef2f7;--s1:#fff;--s2:#f3f6fa;--ln:rgba(15,23,42,.08);--ln2:rgba(15,23,42,.16);--ac:#0891b2;--ac2:#4f46e5;--ok:#059669;--wn:#d97706;--bd:#e11d48;--tx:#0e1726;--sb:#5b6a80;--sb2:#8b98ab;--glow:rgba(8,145,178,.12)}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}html,body{margin:0}
body{background:radial-gradient(90% 38% at 50% -8%,var(--glow),transparent 70%),var(--bg);color:var(--tx);font:14px/1.7 Vazirmatn,Tahoma,sans-serif;min-height:100dvh;padding-bottom:calc(98px + env(safe-area-inset-bottom,0));font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
button,input,select{font:inherit;color:inherit}button{cursor:pointer;border:0;background:none;padding:0}
.l{direction:ltr;unicode-bidi:plaintext}small{color:var(--sb);font-size:11.5px}
header{position:sticky;top:0;z-index:10;padding:calc(10px + env(safe-area-inset-top,0)) 14px 10px;background:color-mix(in srgb,var(--bg) 78%,transparent);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-bottom:1px solid var(--ln)}
.hd{display:flex;align-items:center;gap:11px}.lg{width:40px;height:40px;border-radius:13px;display:grid;place-items:center;font-size:21px;color:var(--bg);background:linear-gradient(140deg,var(--ac),var(--ac2));box-shadow:0 6px 22px var(--glow)}
.hd h1{margin:0;font-size:16px;font-weight:800;line-height:1.3;flex:1}.hd h1 small{display:block;font-weight:500}
.ib{width:38px;height:38px;border-radius:12px;background:var(--s1);border:1px solid var(--ln);display:grid;place-items:center;font-size:18px;color:var(--sb)}.ib:active{transform:scale(.92)}
.sr{position:relative;margin-top:10px}.sr i{position:absolute;top:50%;translate:0 -50%;inset-inline-start:13px;color:var(--sb2);font-size:17px}
input,select{width:100%;background:var(--s2);border:1px solid var(--ln);border-radius:13px;padding:11px 13px;font-size:16px;outline:0;transition:border-color .15s,box-shadow .15s}
input:focus,select:focus{border-color:var(--ac);box-shadow:0 0 0 3px var(--glow)}.sr input{padding-inline-start:40px;background:var(--s1)}
main{padding:14px}.sec{display:flex;align-items:center;justify-content:space-between;margin:20px 2px 10px;font-weight:800;font-size:13.5px}.sec small{font-weight:500}.sec:first-child{margin-top:4px}
.card{background:var(--s1);border:1px solid var(--ln);border-radius:20px;padding:15px;margin-bottom:10px}
.hero{display:flex;align-items:center;gap:18px;padding:18px;position:relative;overflow:hidden}.hero:before{content:"";position:absolute;inset-inline-end:-60px;top:-60px;width:200px;height:200px;background:radial-gradient(circle,var(--glow),transparent 70%)}
.ring{position:relative;width:118px;height:118px;flex:none}.ring svg{width:100%;height:100%;rotate:-90deg}.ring circle{fill:none;stroke-width:9;stroke-linecap:round}.ring .bg{stroke:var(--s2)}.ring .fg{stroke:url(#rg);transition:stroke-dasharray .9s cubic-bezier(.2,.8,.2,1)}
.rc{position:absolute;inset:0;display:grid;place-content:center;text-align:center;line-height:1.2}.rc b{font-size:30px;font-weight:800}.rc small{font-size:11px}
.hs{flex:1;min-width:0;position:relative}.hs>small{display:block}.hs .big{font-size:25px;font-weight:800;display:block;line-height:1.3;margin-bottom:10px;text-align:right}
.kv{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--ln);padding-top:9px}.kv div{text-align:center;line-height:1.35}.kv div+div{border-inline-start:1px solid var(--ln)}.kv b{display:block;font-size:15px}.kv small{font-size:10.5px}
.pre{display:flex;gap:9px;overflow-x:auto;margin:0 -14px;padding:2px 14px 6px;scrollbar-width:none;scroll-snap-type:x proximity}.pre::-webkit-scrollbar{display:none}
.pc{flex:none;scroll-snap-align:start;min-width:96px;padding:12px 14px;border-radius:17px;background:var(--s1);border:1px solid var(--ln);text-align:right;transition:transform .15s,border-color .15s}.pc:active{transform:scale(.95);border-color:var(--ac)}
.pc b{display:block;font-size:22px;font-weight:800;line-height:1.2}.pc small{display:block}.pc.cu{background:transparent;border:1px dashed var(--ln2);display:grid;place-content:center;gap:2px;text-align:center;color:var(--ac)}.pc.cu i{font-size:22px}
.it{display:flex;align-items:center;gap:12px;padding:12px 13px;background:var(--s1);border:1px solid var(--ln);border-radius:18px;margin-bottom:8px;width:100%;text-align:right;transition:transform .12s,border-color .15s}.it:active{transform:scale(.985);border-color:var(--ln2)}
.av{position:relative;width:42px;height:42px;flex:none;border-radius:14px;display:grid;place-items:center;font-size:20px;background:var(--s2);color:var(--ac)}
.av:after{content:"";position:absolute;bottom:-3px;inset-inline-end:-3px;width:12px;height:12px;border-radius:50%;border:2.5px solid var(--s1);background:var(--sb2)}.av.ok:after{background:var(--ac)}.av.live:after{background:var(--ok);animation:pl 1.8s infinite}.av.bad:after{background:var(--bd)}
@keyframes pl{0%{box-shadow:0 0 0 0 rgba(52,211,153,.55)}80%,100%{box-shadow:0 0 0 7px rgba(52,211,153,0)}}
.n{flex:1;min-width:0}.n b{display:block;font-size:13.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:right;font-weight:700}.n small{display:flex;gap:7px;align-items:center;flex-wrap:wrap}
.bar{height:5px;border-radius:9px;background:var(--s2);overflow:hidden;margin-top:7px}.bar i{display:block;height:100%;border-radius:9px;background:linear-gradient(90deg,var(--ac),var(--ac2));transition:width .8s cubic-bezier(.2,.8,.2,1)}.bar.w i{background:var(--wn)}.bar.d i{background:var(--bd)}
.tg{padding:0 8px;border-radius:99px;font-size:10.5px;font-weight:700;line-height:1.8;background:var(--s2);color:var(--sb)}.tg.live{color:var(--ok);background:rgba(52,211,153,.12)}.tg.bad{color:var(--bd);background:rgba(251,113,133,.12)}.tg.ok{color:var(--ac);background:var(--glow)}
.seg{display:flex;gap:4px;padding:4px;background:var(--s1);border:1px solid var(--ln);border-radius:15px;margin-bottom:12px;overflow-x:auto;scrollbar-width:none}.seg::-webkit-scrollbar{display:none}
.seg button{flex:1;white-space:nowrap;padding:7px 12px;border-radius:11px;font-size:12.5px;font-weight:700;color:var(--sb);transition:.2s}.seg button.on{background:var(--s2);color:var(--tx);box-shadow:inset 0 0 0 1px var(--ln2)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:7px;padding:11px 14px;border-radius:14px;background:var(--s2);border:1px solid var(--ln);font-size:13px;font-weight:700;transition:transform .12s}.btn:active{transform:scale(.96)}
.btn.p{background:linear-gradient(135deg,var(--ac),var(--ac2));color:#04121a;border:0}.btn.d{color:var(--bd)}.btn.w{width:100%}.rw{display:flex;gap:8px}.rw>*{flex:1;min-width:0}.g2{display:grid;grid-template-columns:1fr 1fr;gap:8px}.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.ac{display:flex;flex-direction:column;align-items:center;gap:3px;padding:11px 4px;border-radius:15px;background:var(--s2);font-size:11px;font-weight:700;color:var(--sb)}.ac i{font-size:20px;color:var(--tx)}.ac:active{transform:scale(.93)}.ac.d i{color:var(--bd)}
.u{font:11px ui-monospace,monospace;direction:ltr;text-align:left;word-break:break-all;background:var(--s2);border:1px dashed var(--ln2);padding:10px;border-radius:13px;color:var(--ac);margin:8px 0}
.dock{position:fixed;z-index:12;bottom:calc(12px + env(safe-area-inset-bottom,0));left:50%;translate:-50% 0;width:min(calc(100% - 24px),440px);display:flex;padding:6px;border-radius:24px;background:color-mix(in srgb,var(--s1) 82%,transparent);backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px);border:1px solid var(--ln2);box-shadow:0 18px 40px rgba(0,0,0,.35)}
.dock a{flex:1;position:relative;z-index:1;text-align:center;padding:7px 0 5px;font-size:10.5px;font-weight:700;color:var(--sb);transition:color .2s;text-decoration:none}.dock a i{display:block;font-size:22px;transition:transform .25s}.dock a.on{color:var(--ac)}.dock a.on i{transform:translateY(-2px)}
#ind{position:absolute;top:6px;bottom:6px;border-radius:18px;background:var(--glow);box-shadow:inset 0 0 0 1px var(--ac),0 0 22px var(--glow);transition:left .35s cubic-bezier(.3,1.2,.4,1),width .35s}
.sh{position:fixed;inset:0;z-index:30;background:rgba(0,0,0,.55);backdrop-filter:blur(3px);opacity:0;pointer-events:none;transition:opacity .25s;display:flex;align-items:flex-end}.sh.on{opacity:1;pointer-events:auto}
.sp{width:100%;max-height:92dvh;overflow:auto;background:var(--s1);border-radius:28px 28px 0 0;border-top:1px solid var(--ln2);padding:0 16px calc(20px + env(safe-area-inset-bottom,0));translate:0 100%;transition:translate .38s cubic-bezier(.2,.9,.3,1)}.sh.on .sp{translate:0 0}
.gr{position:sticky;top:0;padding:10px 0 12px;background:var(--s1);z-index:2;touch-action:none}.gr:before{content:"";display:block;width:42px;height:4px;border-radius:9px;background:var(--ln2);margin:0 auto}
.q{display:block;width:176px;height:176px;background:#fff;padding:9px;border-radius:18px;margin:12px auto}
.sk{height:68px;border-radius:18px;margin-bottom:8px;background:linear-gradient(100deg,var(--s1) 30%,var(--s2) 50%,var(--s1) 70%);background-size:300% 100%;animation:sk 1.3s infinite}@keyframes sk{to{background-position:-100% 0}}
#tt{position:fixed;z-index:60;top:calc(14px + env(safe-area-inset-top,0));left:50%;translate:-50% -140%;background:var(--s2);border:1px solid var(--ln2);padding:9px 18px;border-radius:99px;font-size:12.5px;font-weight:700;box-shadow:0 14px 34px rgba(0,0,0,.4);transition:translate .35s cubic-bezier(.3,1.3,.5,1)}#tt.on{translate:-50% 0}
.em{text-align:center;color:var(--sb);padding:34px 10px}.em i{display:block;font-size:34px;margin-bottom:4px;color:var(--sb2)}
.m{margin-bottom:12px}.m div{display:flex;justify-content:space-between;font-size:12px;margin-bottom:5px}
.ck{display:flex;align-items:center;gap:12px;padding:11px 12px;border-radius:15px;background:var(--s2);margin-bottom:7px}.ck input{width:20px;height:20px;margin:0;accent-color:var(--ac);flex:none}
.lg2{padding:9px 0;border-bottom:1px solid var(--ln);font-size:12px}.lg2:last-child{border:0}
details summary{list-style:none;cursor:pointer;padding:10px 0;font-weight:700;font-size:13px;color:var(--ac)}details summary::-webkit-details-marker{display:none}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}

.mg{display:grid;grid-template-columns:1fr 1fr;gap:10px}.mt{display:flex;flex-direction:column;align-items:flex-start;gap:2px;text-align:right;padding:15px;border-radius:20px;background:var(--s1);border:1px solid var(--ln);transition:transform .12s,border-color .15s}.mt:active{transform:scale(.96);border-color:var(--ac)}.mt i{font-size:24px;color:var(--ac);margin-bottom:6px}.mt b{font-size:13.5px}.mt small{font-size:11px}
button.lg{border:0;cursor:pointer}details[open] summary{margin-bottom:6px}select{appearance:none;background-image:none}

.lg{overflow:hidden;background:#0b0f18;padding:0}.lg img{width:100%;height:100%;object-fit:cover;display:block}.lg i{color:var(--ac)}
.pf{display:flex;align-items:center;gap:12px;padding:10px 12px;margin-bottom:12px;border-radius:20px;background:var(--s1);border:1px solid var(--ln)}.pf img{width:46px;height:46px;border-radius:15px;object-fit:cover;flex:none;box-shadow:0 0 0 2px var(--ac),0 8px 24px var(--glow)}.pf b{display:block;font-size:14px;line-height:1.4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pf small{display:block}
.pf.big{flex-direction:column;text-align:center;padding:22px 16px;gap:10px;position:relative;overflow:hidden}.pf.big:before{content:"";position:absolute;inset:-40% -10% auto;height:180px;background:radial-gradient(60% 100% at 50% 0,var(--glow),transparent 75%)}.pf.big img{width:92px;height:92px;border-radius:28px;position:relative}.pf.big>div{position:relative}.pf.big b{font-size:17px}.pf.big .tg{position:relative}
</style></head><body>
<header><div class="hd"><button class="lg" id="lg" data-a="" aria-label="بازگشت"><i class="ti ti-shield-check"></i></button><h1 id="ttl">VodiWalker<small>مرکز کنترل</small></h1><button class="ib" data-a="theme" aria-label="تم"><i class="ti ti-moon"></i></button><button class="ib" data-a="reload" aria-label="بروزرسانی"><i class="ti ti-refresh"></i></button></div>
<div class="sr" id="sr"><i class="ti ti-search"></i><input id="gs" placeholder="جستجو…" autocomplete="off"></div></header>
<main id="v"></main><nav class="dock" id="nv"><span id="ind"></span></nav><div class="sh" id="sh"><div class="sp" id="sp"><div class="gr" id="gr"></div><div id="sb"></div></div></div><div id="tt"></div>
<svg width="0" height="0" style="position:absolute"><defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4cd7f6"/><stop offset="1" stop-color="#7c8cff"/></linearGradient></defs></svg>
<script>
const W=window.Telegram&&Telegram.WebApp,$=i=>document.getElementById(i),R=document.documentElement;
const S={tab:'h',stack:[],q:'',f:'all',tok:'',all:[],L:[],C:[],subs:[],cats:[],T:null};
const ROOT=['h','c','g','r','m'],TABS=[['h','ti-layout-dashboard','خانه'],['c','ti-router','اینباندها'],['g','ti-folders','ساب‌ها'],['r','ti-chart-donut','گزارش'],['m','ti-layout-grid','بیشتر']];
const MORE=[['nod','ti-server','نودها','سرورهای متصل'],['prx','ti-arrows-shuffle','پروکسی خروجی','SOCKS و Outbound'],['auto','ti-wand','ساخت هوشمند','پروفایل آماده'],['cmb','ti-git-merge','کامبو WS+XHTTP','جفت‌کانفیگ'],['cat','ti-category','دسته‌بندی‌ها','قالب پیش‌فرض ساخت'],['con','ti-plug-connected','اتصال‌های زنده','IPهای متصل'],['msg','ti-bell','پیام و خطا','لاگ فعالیت'],['adm','ti-users','ادمین‌ها','دسترسی و درخواست‌ها'],['bot','ti-brand-telegram','ربات تلگرام','توکن و کنترل'],['set','ti-settings','تنظیمات','ساب، دامنه، پشتیبان'],['sec','ti-shield-lock','امنیت','رمز و نشست‌ها']];
const TITLE={h:'VodiWalker',c:'اینباندها',g:'سابسکریپشن‌ها',r:'گزارش‌ها',m:'بیشتر',cat:'دسته‌بندی‌ها',nod:'نودها',prx:'پروکسی خروجی',auto:'ساخت هوشمند',cmb:'کامبو WS+XHTTP',con:'اتصال‌های زنده',msg:'پیام و خطا',adm:'ادمین‌ها',bot:'ربات تلگرام',set:'تنظیمات',sec:'امنیت'};
function setTheme(t){R.dataset.theme=t;try{localStorage.vwt=t;if(W){W.setHeaderColor(t=='dark'?'#070b11':'#eef2f7');W.setBackgroundColor(t=='dark'?'#070b11':'#eef2f7')}}catch(x){}}
if(W){W.ready();W.expand();try{W.disableVerticalSwipes()}catch(x){}}
setTheme((()=>{try{return localStorage.vwt}catch(x){}})()||(W&&W.colorScheme)||'dark');
const e=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const hap=k=>{try{W.HapticFeedback.notificationOccurred(k||'success')}catch(x){}},tap=()=>{try{W.HapticFeedback.impactOccurred('light')}catch(x){}};
function tt(m,bad){const x=$('tt');x.textContent=m;x.classList.add('on');clearTimeout(tt.h);tt.h=setTimeout(()=>x.classList.remove('on'),2200);bad?hap('error'):tap()}
const INIT=()=>W?W.initData:'';
async function auth(){const r=await fetch('/api/tma/session',{method:'POST',headers:{'Content-Type':'application/json','X-TG-Init':INIT()},body:'{}'});const j=await r.json().catch(()=>({}));if(!r.ok)throw Error(j.detail||'احراز هویت ناموفق');S.tok=j.token}
async function J(m,u,b,again){const r=await fetch(u,{method:m,headers:{'Content-Type':'application/json','x-vw-session':S.tok,'X-TG-Init':INIT()},body:b===undefined?undefined:JSON.stringify(b)});if(r.status==401&&!again){await auth();return J(m,u,b,1)}let j={};try{j=await r.json()}catch(x){}if(!r.ok)throw Error(typeof j.detail=='string'?j.detail:'خطا ('+r.status+')');return j}
const T=(a,b)=>J('POST','/api/tma/'+a,b||{});
function cp(v){const ok=()=>{tt('کپی شد ✓');hap()};const fb_=()=>{const a=document.createElement('textarea');a.value=v;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove();ok()};try{navigator.clipboard.writeText(v).then(ok,fb_)}catch(x){fb_()}}
function fb(n){n=+n||0;const u=['B','KB','MB','GB','TB'];let i=0;while(n>=1024&&i<4){n/=1024;i++}return(i==0?n:n>=10?n.toFixed(1):n.toFixed(2))+' '+u[i]}
function qr(v){try{const q=qrcode(0,'M');q.addData(v);q.make();return'data:image/svg+xml;charset=utf-8,'+encodeURIComponent(q.createSvgTag(5,4))}catch(x){return''}}
const ask=(m,f)=>{if(W&&W.showConfirm)W.showConfirm(m,ok=>ok&&f());else if(confirm(m))f()};
const arr=j=>Array.isArray(j)?j:(Object.values(j||{}).find(Array.isArray)||[]);
const v_=id=>{const x=$(id);return x?x.value.trim():''},n_=id=>+v_(id)||0;
/* ---- normalize ---- */
function nz(r){let d=null;if(r.expires_at){const t=new Date(r.expires_at).getTime();d=isFinite(t)?Math.max(0,Math.floor((t-Date.now())/864e5)):null}
return{id:r.uuid,label:r.label||r.name||'?',active:!!r.active&&!r.expired,off:!r.active,used:+r.used_bytes||0,limit:+r.limit_bytes||0,days:r.expired?0:d,online:+r.connected_ips||0,clients:+r.client_count||0,parent:r.parent_inbound_id,r}}
async function loadLinks(){const j=await J('GET','/api/links');S.all=(j.links||[]).map(nz);S.L=S.all.filter(x=>!x.parent);S.C=S.all.filter(x=>x.parent)}
const item=id=>S.all.find(x=>x.id==id),sub_=id=>S.subs.find(x=>x.sub_id==id);
const st=l=>l.off?{c:'',t:'غیرفعال'}:(l.limit&&l.used>=l.limit)||l.days===0?{c:'bad',t:'تمام‌شده'}:l.online?{c:'live',t:'آنلاین'}:{c:'ok',t:'آماده'};
const pct=l=>l.limit?Math.min(100,Math.round(l.used/l.limit*100)):0,bc=p=>p>=90?'d':p>=70?'w':'';
const needs=l=>!l.off&&((l.days!==null&&l.days<=3)||(l.limit&&l.used>=l.limit*.85));
const row=l=>{const s=st(l),p=pct(l);return`<button class="it" data-a="open" data-id="${e(l.id)}"><div class="av ${s.c}"><i class="ti ti-router"></i></div><div class="n"><b class="l">${e(l.label)}</b><small><span class="tg ${s.c}">${s.t}</span><span class="l">${fb(l.used)} / ${l.limit?fb(l.limit):'∞'}</span><span>${l.days===null?'بدون انقضا':l.days+' روز'}</span>${l.clients?`<span><i class="ti ti-users"></i> ${l.clients}</span>`:''}</small><div class="bar ${bc(p)}"><i style="width:${l.limit?p:100}%;opacity:${l.limit?1:.25}"></i></div></div><i class="ti ti-chevron-left" style="color:var(--sb2)"></i></button>`};
const sec=(t,x)=>`<div class="sec"><span>${t}</span>${x?`<small>${x}</small>`:''}</div>`;
const em=(i,t)=>`<div class="em"><i class="ti ${i}"></i>${t}</div>`;
const fld=(id,ph,val,ty)=>`<input id="${id}" placeholder="${ph}" value="${e(val==null?'':val)}" ${ty?`type="${ty}" inputmode="decimal"`:''} style="margin-bottom:8px">`;
const ck=(id,t,on)=>`<label class="ck"><input type="checkbox" id="${id}" ${on?'checked':''}><div class="n"><b>${t}</b></div></label>`;
const U=()=>(W&&W.initDataUnsafe&&W.initDataUnsafe.user)||{};
const prof=big=>{const u=U(),nm=[u.first_name,u.last_name].filter(Boolean).join(' ')||'مدیر پنل';return`<div class="pf ${big?'big':''}"><img src="/assets/vw.png" alt=""><div style="flex:1;min-width:0"><b>${e(nm)}</b><small>${u.username?'@'+e(u.username)+' · ':''}مالک پنل VodiWalker</small></div><span class="tg live">متصل</span></div>`};
const sk=()=>'<div class="sk" style="height:140px"></div><div class="sk"></div><div class="sk"></div>';
/* ---- shell / router ---- */
function cur(){return S.stack.length?S.stack[S.stack.length-1]:S.tab}
function shell(){const p=cur(),sub=S.stack.length>0;$('lg').innerHTML=sub?'<i class="ti ti-chevron-right"></i>':'<img src="/assets/vw.png" alt="VodiWalker">';$('lg').dataset.a=sub?'back':'';$('ttl').innerHTML=(TITLE[p]||'')+`<small>${sub?'VodiWalker':'مرکز کنترل'}</small>`;$('sr').style.display=['c','g','h'].includes(p)?'':'none';$('nv').style.display=sub?'none':'';
const n=$('nv');n.querySelectorAll('a').forEach(a=>a.remove());n.insertAdjacentHTML('beforeend',TABS.map(t=>`<a href="#" data-a="tab" data-id="${t[0]}" class="${S.tab==t[0]?'on':''}"><i class="ti ${t[1]}"></i>${t[2]}</a>`).join(''));const a=n.querySelector('a.on'),i=$('ind');if(a&&a.offsetWidth){i.style.left=a.offsetLeft+'px';i.style.width=a.offsetWidth+'px'}
try{sub?W.BackButton.show():W.BackButton.hide()}catch(x){}}
async function draw(){const p=cur();shell();const f=P[p];if(!f)return;const my=S.seq=(S.seq||0)+1;try{const h=await f();if(my!==S.seq)return;if(h!=null)$('v').innerHTML=h}catch(x){if(my===S.seq)$('v').innerHTML=`<div class="card em"><i class="ti ti-alert-triangle"></i><b>${e(x.message)}</b><br><button class="btn" data-a="reload" style="margin-top:12px">تلاش دوباره</button></div>`}}
const reload=()=>draw();
function go(p){S.stack.push(p);S.q='';$('gs').value='';draw();scrollTo({top:0})}
/* ---- pages ---- */
const P={
async h(){await loadLinks();const L=S.L,q=S.q.toLowerCase();
if(q){const a=L.filter(l=>(l.label+l.id).toLowerCase().includes(q));return sec('نتایج «'+e(S.q)+'»')+(a.map(row).join('')||em('ti-search-off','چیزی پیدا نشد'))}
const act=L.filter(l=>!l.off).length,on=L.reduce((a,l)=>a+l.online,0),tr=S.all.reduce((a,l)=>a+l.used,0),nl=L.filter(needs).slice(0,4),r=44,c=2*Math.PI*r,p=L.length?act/L.length:0;
return prof()+`<section class="card hero"><div class="ring"><svg viewBox="0 0 100 100"><circle class="bg" cx="50" cy="50" r="${r}"/><circle class="fg" cx="50" cy="50" r="${r}" stroke-dasharray="${p*c} ${c}"/></svg><div class="rc"><b>${on}</b><small>آنلاین</small></div></div><div class="hs"><small>ترافیک کل مصرف‌شده</small><b class="big l">${fb(tr)}</b><div class="kv"><div><b>${act}</b><small>فعال</small></div><div><b>${L.length}</b><small>اینباند</small></div><div><b>${S.C.length}</b><small>کلاینت</small></div></div></div></section>`+sec('ساخت سریع','واقعی و آنی')+`<div class="pre">${[[10,30],[30,30],[50,30],[100,30],[200,60],[0,30]].map(p=>`<button class="pc" data-a="qc" data-id="${p[0]},${p[1]}"><b>${p[0]||'∞'}</b><small>${p[0]?'گیگابایت':'نامحدود'} · ${p[1]} روز</small></button>`).join('')}<button class="pc cu" data-a="create"><i class="ti ti-plus"></i><small>دلخواه</small></button></div>`+(nl.length?sec('نیاز به توجه',nl.length+' مورد')+nl.map(row).join(''):'')},
async c(){await loadLinks();const q=S.q.toLowerCase(),F=[['all','همه'],['on','فعال'],['net','آنلاین'],['near','نزدیک انقضا'],['off','غیرفعال']],fl=l=>S.f=='all'||(S.f=='on'&&!l.off&&st(l).c!='bad')||(S.f=='off'&&l.off)||(S.f=='net'&&l.online)||(S.f=='near'&&needs(l)),L=S.L.filter(fl).filter(l=>!q||(l.label+l.id).toLowerCase().includes(q));
return`<div class="seg">${F.map(x=>`<button class="${S.f==x[0]?'on':''}" data-a="flt" data-id="${x[0]}">${x[1]}</button>`).join('')}</div>`+(L.map(row).join('')||em('ti-inbox','موردی نیست'))+`<button class="btn p w" data-a="create" style="margin-top:6px"><i class="ti ti-plus"></i> اینباند جدید</button>`},
async g(){const j=await J('GET','/api/subs');S.subs=j.subs||[];await loadLinks();const q=S.q.toLowerCase(),G=S.subs.filter(s=>!q||(s.name||'').toLowerCase().includes(q));
return`<button class="btn p w" data-a="gnew" style="margin-bottom:12px"><i class="ti ti-folder-plus"></i> گروه ساب جدید</button>`+(G.map(gc).join('')||em('ti-folders','هنوز گروهی ندارید'))},
async r(){const[j,s]=await Promise.all([J('GET','/api/reports/summary?days=14'),T('state').catch(()=>null)]);await loadLinks();const se=j.series||[],mx=Math.max(1,...se.map(x=>x.traffic_mb)),tt_=j.totals||{},pd=j.protocol_distribution||[],tl=j.top_links||[],tm=Math.max(1,...tl.map(x=>x.used_bytes));
const bars=se.map((x,i)=>{const h=Math.max(3,Math.round(x.traffic_mb/mx*86));return`<g><rect x="${i*22+4}" y="${96-h}" width="14" height="${h}" rx="5" fill="url(#rg)" opacity="${x.traffic_mb?1:.25}"/></g>`}).join('');
return sec('ترافیک ۱۴ روز اخیر',fb(se.reduce((a,x)=>a+x.traffic_mb,0)*1048576))+`<div class="card"><svg viewBox="0 0 ${se.length*22+4} 100" style="width:100%;height:110px">${bars}</svg><div style="display:flex;justify-content:space-between"><small>${e((se[0]||{}).date||'').slice(5)}</small><small>${e((se[se.length-1]||{}).date||'').slice(5)}</small></div></div><div class="card"><div class="kv" style="border:0;padding:0">${[['کل',tt_.links],['فعال',tt_.active_links],['منقضی',tt_.expired_links],['ساب',tt_.subs]].map(x=>`<div><b>${x[1]||0}</b><small>${x[0]}</small></div>`).join('')}</div></div>`
+(s?sec('وضعیت سرور')+`<div class="card">${[['CPU',s.srv.cpu],['RAM',s.srv.ram],['دیسک',s.srv.disk]].map(x=>`<div class="m"><div><span>${x[0]}</span><b>${x[1]}%</b></div><div class="bar ${bc(x[1])}" style="margin:0"><i style="width:${x[1]}%"></i></div></div>`).join('')}</div>`:'')
+sec('پروتکل‌ها')+`<div class="card">${pd.map(x=>`<div class="m"><div><span class="l">${e(x.protocol)}</span><b>${x.count}</b></div><div class="bar" style="margin:0"><i style="width:${Math.round(x.count/Math.max(1,tt_.links)*100)}%"></i></div></div>`).join('')||em('ti-chart-pie','داده‌ای نیست')}</div>`
+sec('پرمصرف‌ترین‌ها')+`<div class="card">${tl.slice(0,8).map(x=>`<div class="m"><div><span class="l">${e(x.label)}</span><small>${fb(x.used_bytes)}</small></div><div class="bar" style="margin:0"><i style="width:${Math.round(x.used_bytes/tm*100)}%"></i></div></div>`).join('')||em('ti-flame','داده‌ای نیست')}</div>`},
async m(){return prof(1)+`<div class="mg">${MORE.map(x=>`<button class="mt" data-a="go" data-id="${x[0]}"><i class="ti ${x[1]}"></i><b>${x[2]}</b><small>${x[3]}</small></button>`).join('')}</div><div class="card" style="margin-top:12px"><div class="rw"><button class="btn" data-a="theme"><i class="ti ti-moon"></i> تغییر تم</button><button class="btn" data-a="reload"><i class="ti ti-refresh"></i> بروزرسانی</button></div></div>`},
async nod(){const j=await J('GET','/api/nodes');S.nodes=j.nodes||[];return`<div class="rw" style="margin-bottom:12px"><button class="btn p" data-a="nodf" data-id=""><i class="ti ti-plus"></i> نود جدید</button><button class="btn" data-a="nodall"><i class="ti ti-activity"></i> بررسی همه</button></div>`+(S.nodes.map(n=>{const s=n.status,c=!n.enabled?'':s?(s.online?'live':'bad'):'ok';return`<button class="it" data-a="nodf" data-id="${e(n.id)}"><div class="av ${c}"><i class="ti ti-server"></i></div><div class="n"><b>${e(n.name)}</b><small class="l">${e(n.url)}</small><small><span class="tg ${c}">${!n.enabled?'غیرفعال':s?(s.online?'آنلاین':'آفلاین'):'بررسی‌نشده'}</span>${s&&s.latency_ms?`<span>${Math.round(s.latency_ms)}ms</span>`:''}${s&&s.version?`<span>v${e(s.version)}</span>`:''}</small>${s&&!s.online&&s.error?`<small style="color:var(--bd)">${e(s.error)}</small>`:''}</div><i class="ti ti-chevron-left" style="color:var(--sb2)"></i></button>`}).join('')||em('ti-server','نودی ثبت نشده'))},
async prx(){const j=await J('GET','/api/proxies').catch(x=>({proxies:[],err:x.message}));S.prx=j.proxies||[];return`<button class="btn p w" data-a="prxf" style="margin-bottom:12px"><i class="ti ti-plus"></i> پروکسی SOCKS5 جدید</button>`+(j.err&&!S.prx.length?`<div class="card em"><i class="ti ti-alert-triangle"></i>${e(j.err)}</div>`:'')+(S.prx.map(p=>{const c=p.test_ok?'live':p.test_message?'bad':'ok';return`<div class="card"><div style="display:flex;justify-content:space-between;align-items:center"><b>${e(p.name)}</b><span class="tg ${c}">${p.test_ok?(p.tcp_ms!=null?Math.round(p.tcp_ms)+'ms':'سالم'):p.test_message?'خطا':'تست‌نشده'}</span></div><small class="l">${e(String(p.scheme||'socks5').toUpperCase())} · ${e(p.host)}:${e(p.port)}${p.has_auth?' · 🔒':''}</small>${p.country?`<br><small>${e(p.country)}${p.city?' · '+e(p.city):''}${p.isp?' · '+e(p.isp):''}</small>`:''}${p.exit_ip?`<br><small class="l">IP خروجی: ${e(p.exit_ip)}</small>`:''}${p.test_message&&!p.test_ok?`<br><small style="color:var(--bd)">${e(p.test_message)}</small>`:''}${p.in_use?`<br><small>${e(p.in_use)} کانفیگ استفاده می‌کنند</small>`:''}<div class="rw" style="margin-top:10px"><button class="btn" data-a="prxt" data-id="${e(p.id)}"><i class="ti ti-activity"></i> تست</button><button class="btn d" data-a="prxd" data-id="${e(p.id)}"><i class="ti ti-trash"></i> حذف</button></div></div>`}).join('')||em('ti-arrows-shuffle','پروکسی ثبت نشده'))},
async auto(){await pxl();return`<div class="card"><b style="font-size:13px">پروفایل امنیتی</b><div style="height:8px"></div><div class="seg" id="ap_pf">${[['balanced','متعادل'],['normal','معمولی'],['gaming','گیمینگ'],['maximum','حداکثر']].map((x,i)=>`<button class="${i?'':'on'}" data-a="pf" data-id="${x[0]}">${x[1]}</button>`).join('')}</div>${ck('ap_cb','کامبو WS+XHTTP',false)}<div class="rw">${fld('ap_p','پورت (443)','','n')}${fld('ap_n','تعداد جفت','','n')}</div>${pxsel('ap_o')}<button class="btn p w" data-a="autogo"><i class="ti ti-wand"></i> ساخت هوشمند</button></div><small>با پروفایل انتخابی، فینگرپرینت و فرگمنت و محدودیت اتصال به‌صورت خودکار تنظیم می‌شود.</small>`},
async cmb(){await pxl();let cats=S.cats;if(!cats.length)try{cats=S.cats=(await J('GET','/api/categories')).categories||[]}catch(x){}return`<div class="card">${fld('cm_l','نام گروه / برچسب')}<div class="rw">${fld('cm_g','حجم GB (0=∞)','','n')}${fld('cm_d','روز (0=∞)','','n')}</div><div class="rw">${fld('cm_p','پورت','','n')}${fld('cm_n','تعداد جفت','2','n')}</div><div class="rw">${fld('cm_c','تعداد کانفیگ','1','n')}${fld('cm_k','سقف کلاینت','','n')}</div><div class="rw">${fld('cm_i','محدودیت IP','','n')}${fld('cm_x','اتصال هم‌زمان','','n')}</div>${cats.length?`<select id="cm_ct" style="margin-bottom:8px"><option value="">دسته‌بندی: پیش‌فرض</option>${cats.map(c=>`<option value="${e(c.id)}">${e(c.name)}</option>`).join('')}</select>`:''}${S.prx.length?`<small>خروجی‌ها (اختیاری)</small><div style="height:6px"></div>${S.prx.map(p=>`<label class="ck"><input type="checkbox" class="cmo" value="${e(p.id)}"><div class="n"><b>${e(p.name)}</b></div></label>`).join('')}`:''}<button class="btn p w" data-a="cmbgo"><i class="ti ti-git-merge"></i> ساخت کامبو</button></div>`},
async cat(){const j=await J('GET','/api/categories');S.cats=j.categories||[];return`<button class="btn p w" data-a="catf" data-id="" style="margin-bottom:12px"><i class="ti ti-plus"></i> دسته‌بندی جدید</button>`+(S.cats.map(c=>`<button class="it" data-a="catf" data-id="${e(c.id)}"><div class="av"><i class="ti ti-category"></i></div><div class="n"><b>${e(c.name)}</b><small><span class="tg ok">#${e(c.number)}</span>${c.limit_value?`<span>${e(c.limit_value)} GB</span>`:''}${c.expires_days?`<span>${e(c.expires_days)} روز</span>`:''}</small></div><i class="ti ti-chevron-left" style="color:var(--sb2)"></i></button>`).join('')||em('ti-category','دسته‌بندی ندارید'))},
async con(){const j=await J('GET','/api/connections'),L=arr(j.connections||j);return sec('اتصال‌های فعال',L.length+' IP')+(L.map(c=>`<div class="card"><div style="display:flex;justify-content:space-between;align-items:center"><b class="l">${e(c.ip)}</b><span class="tg live">${e(c.sessions||1)} نشست</span></div><small>${e([].concat(c.labels||[]).join('، '))}</small><br><small>${fb(c.bytes)} · ${e([].concat(c.transports||[]).join('/'))}</small></div>`).join('')||em('ti-plug-off','اتصال فعالی نیست'))},
async msg(){const[a,b]=await Promise.all([J('GET','/api/activity'),J('GET','/api/errors')]),tab=S.mt||'a',lg=x=>`<div class="lg2"><span class="tg ${/err|error/.test(x.level||'')?'bad':/warn/.test(x.level||'')?'ok':''}">${e(x.kind||x.source||x.level||'log')}</span> ${e(x.message||x.msg||'')}<br><small>${e(String(x.time||x.created_at||'').slice(5,16).replace('T',' '))}</small></div>`;
return`<div class="seg"><button class="${tab=='a'?'on':''}" data-a="mt" data-id="a">فعالیت‌ها</button><button class="${tab=='e'?'on':''}" data-a="mt" data-id="e">خطاها (${b.total_errors||0})</button></div><div class="card">${tab=='a'?((a.logs||[]).slice().reverse().map(lg).join('')||em('ti-bell','فعالیتی نیست')):((b.errors||[]).slice().reverse().map(lg).join('')||em('ti-circle-check','خطایی ثبت نشده'))}</div>`+(tab=='e'&&(b.errors||[]).length?`<button class="btn d w" data-a="errclr"><i class="ti ti-trash"></i> پاک‌کردن خطاها</button>`:'')},
async adm(){const[a,q]=await Promise.all([J('GET','/api/admins'),J('GET','/api/admin-requests').catch(()=>({requests:[]}))]);S.adm=a.admins||[];S.req=(q.requests||[]).filter(r=>!r.status||r.status=='pending');
return(S.req.length?sec('درخواست‌های جدید',S.req.length)+S.req.map(r=>`<div class="card"><b>${e(r.full_name||r.name||r.username||'متقاضی')}</b><br><small class="l">${e(r.telegram_id||r.telegram||'')}</small><div class="rw" style="margin-top:10px"><button class="btn p" data-a="rq" data-id="${e(r.id)}" data-v="approve"><i class="ti ti-check"></i> تایید</button><button class="btn d" data-a="rq" data-id="${e(r.id)}" data-v="reject"><i class="ti ti-x"></i> رد</button></div></div>`).join(''):'')+sec('مدیران')+`<button class="btn p w" data-a="admf" data-id="" style="margin-bottom:10px"><i class="ti ti-user-plus"></i> ادمین جدید</button>`+S.adm.map(x=>`<button class="it" data-a="admf" data-id="${e(x.id)}"><div class="av ${x.active===false?'bad':'ok'}"><i class="ti ti-user-shield"></i></div><div class="n"><b>${e(x.username)}</b><small><span class="tg ${x.role=='owner'?'ok':''}">${x.role=='owner'?'مالک':'ادمین'}</span>${x.last_login_at?`<span>${e(String(x.last_login_at).slice(0,10))}</span>`:''}</small></div><i class="ti ti-chevron-left" style="color:var(--sb2)"></i></button>`).join('')},
async bot(){const s=S.set=await J('GET','/api/settings');return`<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><b><i class="ti ti-robot"></i> وضعیت ربات</b><span class="tg ${s.bot_running?'live':'bad'}">${s.bot_running?'روشن':'خاموش'}</span></div>${fld('bt','توکن ربات',s.bot_token)}${fld('bi','آیدی ادمین‌ها (با کاما)',s.bot_admin_ids)}${ck('ba','شروع خودکار با پنل',s.bot_auto_start)}<button class="btn p w" data-a="botsave" style="margin-top:6px">ذخیره</button></div><div class="rw"><button class="btn" data-a="botgo" data-id="start"><i class="ti ti-player-play"></i> روشن</button><button class="btn d" data-a="botgo" data-id="stop"><i class="ti ti-player-stop"></i> خاموش</button></div>`},
async set(){const s=S.set=await J('GET','/api/settings');const t=[['sub_remark_show_name','نمایش نام در ریمارک ساب'],['sub_remark_show_volume','نمایش حجم در ریمارک'],['sub_remark_show_id','نمایش شناسه در ریمارک'],['sub_remark_show_inbound','نمایش اینباند در ریمارک'],['sub_info_line_enabled','ردیف اطلاعات اشتراک'],['sub_info_line_show_volume','حجم در ردیف اطلاعات'],['sub_info_line_show_expiry','انقضا در ردیف اطلاعات'],['name_style_enabled','استایل خودکار نام']];
return`<div class="card"><b style="font-size:13px">آدرس‌ها</b><div style="height:8px"></div>${fld('sb','آدرس عمومی پنل (https://…)',s.public_base_url)}${fld('sh','هاست TCP عمومی',s.tcp_public_host)}${fld('sp','پورت TCP عمومی',s.tcp_public_port)}</div><div class="card"><b style="font-size:13px">تلگرام</b><div style="height:8px"></div>${fld('su','آیدی پشتیبان',s.support_username)}${fld('sc','آیدی کانال',s.channel_username)}</div><div class="card"><b style="font-size:13px">سابسکریپشن</b><div style="height:8px"></div>${t.map(x=>ck('k_'+x[0],x[1],s[x[0]])).join('')}</div><button class="btn p w" data-a="setsave"><i class="ti ti-device-floppy"></i> ذخیره تنظیمات</button>`},
async sec(){return`<div class="card"><b style="font-size:13px"><i class="ti ti-key"></i> تغییر رمز</b><div style="height:8px"></div><input id="p0" type="password" placeholder="رمز فعلی" style="margin-bottom:8px"><input id="p1" type="password" placeholder="رمز جدید" style="margin-bottom:8px"><input id="p2" type="password" placeholder="تکرار رمز جدید" style="margin-bottom:8px"><button class="btn p w" data-a="pw">تغییر رمز</button></div><div class="card"><b style="font-size:13px"><i class="ti ti-user"></i> نام کاربری مالک</b><div style="height:8px"></div><input id="u1" placeholder="نام کاربری جدید" style="margin-bottom:8px"><input id="u0" type="password" placeholder="رمز فعلی" style="margin-bottom:8px"><button class="btn w" data-a="un">تغییر نام کاربری</button></div><button class="btn d w" data-a="revoke"><i class="ti ti-logout"></i> خروج سایر نشست‌ها</button>`}};
function gc(g){return`<div class="card"><div style="display:flex;justify-content:space-between;align-items:center"><b>${e(g.name)}${g.has_password?' <i class="ti ti-lock" style="color:var(--wn)"></i>':''}</b><span class="tg ok">${g.local_count||0} کانفیگ</span></div><small>${e(g.desc||'')}${g.total_used_fmt?' · '+e(g.total_used_fmt):''}</small><div class="u">${e(g.public_url)}</div><div class="g4"><button class="ac" data-a="gcp" data-id="${e(g.sub_id)}"><i class="ti ti-copy"></i>کپی</button><button class="ac" data-a="gqr" data-id="${e(g.sub_id)}"><i class="ti ti-qrcode"></i>QR</button><button class="ac" data-a="gmem" data-id="${e(g.sub_id)}"><i class="ti ti-list-check"></i>اعضا</button><button class="ac" data-a="gnew" data-id="${e(g.sub_id)}"><i class="ti ti-edit"></i>ویرایش</button></div></div>`}
const pxl=async()=>{try{S.prx=(await J('GET','/api/proxies')).proxies||[]}catch(x){S.prx=S.prx||[]}};
const pxsel=(id,cur)=>S.prx&&S.prx.length?`<select id="${id}" style="margin-bottom:8px"><option value="">بدون پروکسی خروجی</option>${S.prx.map(p=>`<option value="${e(p.id)}" ${cur==p.id?'selected':''}>${e(p.name)} — ${e(p.host)}</option>`).join('')}</select>`:'';
/* ---- sheets ---- */
function sheet(h){$('sb').innerHTML=h;$('sh').classList.add('on');$('sp').scrollTop=0;try{W.BackButton.show()}catch(x){}}
function closeS(){$('sh').classList.remove('on');try{S.stack.length?W.BackButton.show():W.BackButton.hide()}catch(x){}}
try{W.BackButton.onClick(()=>$('sh').classList.contains('on')?closeS():back())}catch(x){}$('sh').onclick=x=>{if(x.target===$('sh'))closeS()};
(()=>{let y0=null,dy=0;const g=$('gr'),p=$('sp');g.addEventListener('touchstart',t=>{y0=t.touches[0].clientY;p.style.transition='none'});g.addEventListener('touchmove',t=>{if(y0==null)return;dy=Math.max(0,t.touches[0].clientY-y0);p.style.translate='0 '+dy+'px'});g.addEventListener('touchend',()=>{p.style.transition='';p.style.translate='';if(dy>110)closeS();y0=null;dy=0})})();
const back=()=>{S.stack.pop();draw()};
const hd=(t,s)=>`<div class="hd" style="margin-bottom:14px"><h1>${t}<small>${s||''}</small></h1></div>`;
const gbOf=b=>b?Math.round(b/1073741824*100)/100:0;
async function op(id){const l=item(id);if(!l)return;const r=l.r,s=st(l),p=pct(l);let cs=[];try{cs=(await J('GET',`/api/links/${id}/clients`)).clients||[]}catch(x){}cs=cs.map(nz);
sheet(`<div class="hd" style="margin-bottom:12px"><div class="av ${s.c}"><i class="ti ti-router"></i></div><h1 class="l" style="font-size:14.5px;text-align:right">${e(l.label)}<small style="text-align:right">${e(r.protocol_display||r.protocol||'')} · ${e(r.port||'')}${r.category_name?' · '+e(r.category_name):''}</small></h1><span class="tg ${s.c}">${s.t}</span></div><div class="card" style="background:var(--s2)"><div class="m" style="margin:0"><div><span class="l">${fb(l.used)} / ${l.limit?fb(l.limit):'∞'}</span><small>${l.days===null?'بدون انقضا':l.days+' روز مانده'}${l.online?' · '+l.online+' IP آنلاین':''}</small></div><div class="bar ${bc(p)}" style="margin:0"><i style="width:${l.limit?p:100}%;opacity:${l.limit?1:.25}"></i></div></div></div>${r.note?`<small>${e(r.note)}</small>`:''}<img class="q" alt="QR" src="${qr(r.vless_full||'')}"><div class="u">${e(r.vless_full||'—')}</div><div class="rw"><button class="btn p" data-a="cpv" data-id="${e(id)}" data-v="vless_full"><i class="ti ti-copy"></i> لینک</button><button class="btn" data-a="cpv" data-id="${e(id)}" data-v="sub"><i class="ti ti-link"></i> ساب</button><button class="btn" data-a="cpv" data-id="${e(id)}" data-v="info"><i class="ti ti-info-circle"></i> صفحه</button></div>`+sec('مدیریت سریع')+`<div class="g4">${[['tog',l.off?'ti-player-play':'ti-player-pause',l.off?'فعال':'توقف'],['rst','ti-rotate','ریست مصرف'],['rgn','ti-refresh-dot','لینک نو'],['edt','ti-edit','ویرایش'],['add10','ti-database-plus','+10GB'],['add50','ti-database-plus','+50GB'],['d30','ti-calendar-plus','+30روز'],['del','ti-trash','حذف']].map(x=>`<button class="ac ${x[0]=='del'?'d':''}" data-a="q_${x[0]}" data-id="${e(id)}"><i class="ti ${x[1]}"></i>${x[2]}</button>`).join('')}</div>`
+(l.parent?'':sec('کلاینت‌ها','('+cs.length+')')+cs.map(x=>`<div class="ck"><div class="n"><b class="l">${e(x.label)}</b><small class="l">${fb(x.used)} / ${x.limit?fb(x.limit):'∞'} · ${x.days===null?'∞':x.days+'d'}</small></div><button class="ib" data-a="cpv" data-id="${e(x.id)}" data-v="vless_full"><i class="ti ti-copy"></i></button><button class="ib" data-a="cdel" data-id="${e(x.id)}" data-v="${e(id)}" style="color:var(--bd)"><i class="ti ti-trash"></i></button></div>`).join('')+`<details><summary><i class="ti ti-user-plus"></i> افزودن کلاینت</summary>${fld('cn_','نام کلاینت')}<div class="rw">${fld('cg_','حجم GB','','n')}${fld('cd_','روز','','n')}</div><button class="btn p w" data-a="cadd" data-id="${e(id)}">افزودن</button></details>`))}
async function edt(id){const l=item(id),r=l.r;await pxl();sheet(hd('ویرایش اینباند',e(l.label))+fld('e_l','نام',l.label)+`<div class="rw">${fld('e_g','حجم GB (0=∞)',gbOf(l.limit),'n')}${fld('e_d','روز از امروز (خالی=بدون تغییر)','','n')}</div><div class="rw">${fld('e_p','پورت',r.port,'n')}${fld('e_i','محدودیت IP',r.ip_limit||0,'n')}</div><div class="rw">${fld('e_c','اتصال هم‌زمان',r.connection_limit||0,'n')}${fld('e_s','سرعت Mbit (0=∞)',r.speed_limit_bytes?Math.round(r.speed_limit_bytes*8/1e5)/10:0,'n')}</div>${r.client_limit!==undefined&&!l.parent?fld('e_k','سقف کلاینت',r.client_limit||0,'n'):''}${fld('e_n','یادداشت',r.note)}${pxsel('e_o',r.outbound_proxy_id)}<button class="btn p w" data-a="esave" data-id="${e(id)}">ذخیره</button>`)}
const protos=async()=>{if(!S.T)try{S.T=await T('state')}catch(x){S.T={protocols:[]}}return S.T.protocols||[]};
async function create(){const pr=await protos();let cats=S.cats;if(!cats.length)try{cats=S.cats=(await J('GET','/api/categories')).categories||[]}catch(x){}
sheet(hd('اینباند جدید','حجم و زمان را مشخص کنید')+fld('a_l','نام (خالی = خودکار)')+`<div class="rw">${fld('a_g','حجم GB (0=∞)','','n')}${fld('a_d','روز (0=∞)','','n')}</div><details><summary><i class="ti ti-adjustments"></i> گزینه‌های پیشرفته</summary><select id="a_pr" style="margin-bottom:8px">${pr.map(p=>`<option>${e(p)}</option>`).join('')}</select>${cats.length?`<select id="a_ct" style="margin-bottom:8px"><option value="">دسته‌بندی: پیش‌فرض</option>${cats.map(c=>`<option value="${e(c.id)}">${e(c.name)}</option>`).join('')}</select>`:''}<div class="rw">${fld('a_p','پورت','','n')}${fld('a_i','محدودیت IP','','n')}</div><div class="rw">${fld('a_c','اتصال هم‌زمان','','n')}${fld('a_s','سرعت Mbit','','n')}</div><div class="rw">${fld('a_k','تعداد کلاینت','','n')}${fld('a_n','یادداشت')}</div></details><button class="btn p w" data-a="cv" style="margin-top:6px"><i class="ti ti-plus"></i> ساخت</button>`)}
function nodf(id){const n=id?S.nodes.find(x=>x.id==id):null;sheet(hd(n?'ویرایش نود':'نود جدید','آدرس و توکن نود')+fld('nd_n','نام',n&&n.name)+`<input id="nd_u" class="l" placeholder="https://node.example.com" value="${e(n?n.url:'')}" style="margin-bottom:8px"><input id="nd_t" class="l" placeholder="${n?'توکن (خالی = بدون تغییر)':'توکن نود'}" style="margin-bottom:8px"><div id="nd_r"></div><div class="rw"><button class="btn" data-a="nodtest" data-id="${id||''}"><i class="ti ti-plug-connected"></i> تست اتصال</button><button class="btn p" data-a="nodsave" data-id="${id||''}">ذخیره</button></div>`+(n?`<div class="g4" style="margin-top:10px"><button class="ac" data-a="nodchk" data-id="${e(id)}"><i class="ti ti-activity"></i>بررسی</button><button class="ac" data-a="nodtog" data-id="${e(id)}"><i class="ti ti-${n.enabled?'player-pause':'player-play'}"></i>${n.enabled?'توقف':'فعال'}</button><button class="ac d" data-a="noddel" data-id="${e(id)}"><i class="ti ti-trash"></i>حذف</button></div>`:''))}
function prxf(){sheet(hd('پروکسی SOCKS5 جدید','برای خروجی کانفیگ‌ها')+fld('px_n','نام')+`<div class="rw">${fld('px_h','هاست / IP')}${fld('px_p','پورت','','n')}</div><div class="rw">${fld('px_u','کاربر (اختیاری)')}<input id="px_w" type="password" placeholder="رمز (اختیاری)" style="margin-bottom:8px"></div><button class="btn p w" data-a="prxsave">افزودن</button>`)}
async function gnew(id){const g=id?sub_(id):null;sheet(hd(g?'ویرایش گروه':'گروه ساب جدید')+fld('s_n','نام گروه',g&&g.name)+fld('s_d','توضیح',g&&g.desc)+`<input id="s_p" placeholder="${g&&g.has_password?'رمز جدید (خالی=بدون تغییر، -=حذف رمز)':'رمز (اختیاری)'}" style="margin-bottom:8px"><button class="btn p w" data-a="gsave" data-id="${id||''}">ذخیره</button>`+(g?`<button class="btn d w" data-a="gdel" data-id="${id}" style="margin-top:8px"><i class="ti ti-trash"></i> حذف گروه</button>`:''))}
function gmem(id){const g=sub_(id),sel=g.link_ids||[];sheet(hd('اعضای «'+e(g.name)+'»','کانفیگ‌های گروه را انتخاب کنید')+`<div style="max-height:46dvh;overflow:auto">${S.L.map(l=>`<label class="ck"><input type="checkbox" class="gk" value="${e(l.id)}" ${sel.includes(l.id)?'checked':''}><div class="n"><b class="l">${e(l.label)}</b></div></label>`).join('')||em('ti-inbox','اینباندی نیست')}</div><button class="btn p w" data-a="gmsave" data-id="${e(id)}" style="margin-top:8px">ذخیره</button>`)}
function catf(id){const c=id?S.cats.find(x=>x.id==id):null;sheet(hd(c?'ویرایش دسته‌بندی':'دسته‌بندی جدید','قالب پیش‌فرض اینباندهای این دسته')+fld('c_n','نام',c&&c.name)+`<div class="rw">${fld('c_g','حجم GB',c&&c.limit_value,'n')}${fld('c_d','روز',c&&c.expires_days,'n')}</div><div class="rw">${fld('c_i','محدودیت IP',c&&c.ip_limit,'n')}${fld('c_c','اتصال هم‌زمان',c&&c.connection_limit,'n')}</div><button class="btn p w" data-a="csave" data-id="${id||''}">ذخیره</button>`+(c?`<button class="btn d w" data-a="cdelc" data-id="${id}" style="margin-top:8px"><i class="ti ti-trash"></i> حذف</button>`:''))}
const PERMS=[['dashboard','داشبورد'],['inbounds','اینباند و کلاینت'],['clients','ساخت کلاینت'],['subscriptions','سابسکریپشن'],['categories','دسته‌بندی'],['reports','گزارش‌ها'],['messages','پیام و خطا'],['bot','ربات'],['settings','تنظیمات']];
function admf(id){const a=id?S.adm.find(x=>x.id==id):null,own=a&&a.role=='owner',pm=(a&&a.permissions)||['dashboard'];
if(own)return tt('مالک قابل ویرایش نیست');
sheet(hd(a?'ویرایش «'+e(a.username)+'»':'ادمین جدید')+(a?'':fld('d_u','نام کاربری'))+`<input id="d_p" type="password" placeholder="${a?'رمز جدید (خالی=بدون تغییر)':'رمز عبور'}" style="margin-bottom:10px"><small>دسترسی‌ها</small><div style="height:6px"></div>${PERMS.map(p=>ck('pm_'+p[0],p[1],pm.includes(p[0]))).join('')}<button class="btn p w" data-a="admsave" data-id="${id||''}" style="margin-top:6px">ذخیره</button>`+(a?`<div class="rw" style="margin-top:8px"><button class="btn" data-a="admtog" data-id="${e(id)}">${a.active===false?'فعال‌سازی':'غیرفعال‌سازی'}</button><button class="btn d" data-a="admdel" data-id="${e(id)}">حذف</button></div>`:''))}
/* ---- actions ---- */
const ER=x=>tt(x.message,1),ok=(m)=>{tt(m||'انجام شد ✓');hap()},refresh=()=>draw();
const SW=async(f,m,keep)=>{try{await f();if(!keep)closeS();ok(m);await draw()}catch(x){ER(x)}};
const body_=()=>{const b={label:v_('a_l'),limit_value:n_('a_g'),limit_unit:'GB',expires_days:n_('a_d')};if(!b.label)b.random_name=true;const pr=v_('a_pr');if(pr)b.protocol=pr;if(n_('a_p'))b.port=n_('a_p');if(n_('a_i'))b.ip_limit=n_('a_i');if(n_('a_c'))b.connection_limit=n_('a_c');if(n_('a_s')){b.speed_limit_value=n_('a_s');b.speed_limit_unit='MBIT'}if(n_('a_k'))b.client_limit=n_('a_k');if(v_('a_n'))b.note=v_('a_n');if(v_('a_ct'))b.category_id=v_('a_ct');return b};
const act=(id,a)=>J('POST',`/api/links/${id}/action`,{action:a});
const A={
tab(id){S.tab=id;S.stack=[];S.q='';$('gs').value='';tap();draw();scrollTo({top:0})},go(id){go(id)},back,flt(id){S.f=id;draw()},mt(id){S.mt=id;draw()},open:op,create,gnew,gmem,catf,admf,edt,nodf,prxf,
theme(){setTheme(R.dataset.theme=='dark'?'light':'dark')},reload:refresh,
cpv(id,k){const l=item(id);cp(l.r[k]||'')},gcp(id){cp(sub_(id).public_url)},gqr(id){const g=sub_(id);sheet(hd(e(g.name),'اسکن برای افزودن اشتراک')+`<img class="q" alt="QR" src="${qr(g.public_url)}"><div class="u">${e(g.public_url)}</div><button class="btn p w" data-a="gcp" data-id="${e(id)}"><i class="ti ti-copy"></i> کپی</button>`)},
async qc(v){const[g,d]=v.split(',');try{const r=await J('POST','/api/links',{random_name:true,limit_value:+g,limit_unit:'GB',expires_days:+d});ok('ساخته شد ✓');await draw();const u=r.uuid||(r.link&&r.link.uuid)||r.id;if(u){await loadLinks();op(u)}}catch(x){ER(x)}},
cv(){SW(async()=>{await J('POST','/api/links',body_())},'ساخته شد ✓')},
q_tog(id){const l=item(id);SW(async()=>{await act(id,l.off?'enable':'disable');await loadLinks();op(id)},null,1)},
q_rst(id){SW(async()=>{await act(id,'reset');await loadLinks();op(id)},'مصرف ریست شد',1)},
q_rgn(id){ask('لینک جدید ساخته شود؟ لینک قبلی از کار می‌افتد.',()=>SW(async()=>{await J('POST',`/api/links/${id}/regenerate`,{});await loadLinks();op(id)},'لینک جدید ساخته شد',1))},
q_edt:edt,
q_add10(id){const l=item(id);if(!l.limit)return tt('حجم نامحدود است',1);SW(async()=>{await J('PATCH','/api/links/'+id,{limit_value:gbOf(l.limit)+10,limit_unit:'GB'});await loadLinks();op(id)},'+10GB',1)},
q_add50(id){const l=item(id);if(!l.limit)return tt('حجم نامحدود است',1);SW(async()=>{await J('PATCH','/api/links/'+id,{limit_value:gbOf(l.limit)+50,limit_unit:'GB'});await loadLinks();op(id)},'+50GB',1)},
q_d30(id){const l=item(id),d=(l.days||0)+30;SW(async()=>{await J('PATCH','/api/links/'+id,{expires_days:d});await loadLinks();op(id)},'+30 روز',1)},
q_del(id){ask('این اینباند و کلاینت‌هایش حذف شود؟',()=>SW(()=>J('DELETE','/api/links/'+id),'حذف شد'))},
esave(id){const b={label:v_('e_l'),limit_value:n_('e_g'),limit_unit:'GB',ip_limit:n_('e_i'),connection_limit:n_('e_c'),speed_limit_value:n_('e_s'),speed_limit_unit:'MBIT',note:v_('e_n')};if(n_('e_p'))b.port=n_('e_p');if(v_('e_d')!=='')b.expires_days=n_('e_d');if($('e_k'))b.client_limit=n_('e_k');if($('e_o'))b.outbound_proxy_id=v_('e_o');SW(()=>J('PATCH','/api/links/'+id,b),'ذخیره شد ✓')},
cadd(id){const b={label:v_('cn_'),limit_value:n_('cg_'),limit_unit:'GB',expires_days:n_('cd_')};if(!b.label)b.random_name=true;SW(async()=>{await J('POST',`/api/links/${id}/clients`,b);await loadLinks();op(id)},'کلاینت ساخته شد ✓',1)},
cdel(id,pid){ask('کلاینت حذف شود؟',()=>SW(async()=>{await J('DELETE',`/api/links/${pid}/clients/${id}`);await loadLinks();op(pid)},'حذف شد',1))},
gsave(id){const b={name:v_('s_n')||'گروه جدید',desc:v_('s_d')},p=$('s_p').value.trim();SW(async()=>{if(id){if(p)b.password=p=='-'?'':p;await J('PATCH','/api/subs/'+id,b)}else{if(p)b.password=p;await J('POST','/api/subs',b)}},'ذخیره شد ✓')},
gdel(id){ask('گروه حذف شود؟ (کانفیگ‌ها حذف نمی‌شوند)',()=>SW(()=>J('DELETE','/api/subs/'+id),'حذف شد'))},
gmsave(id){const ids=[...document.querySelectorAll('.gk:checked')].map(x=>x.value);SW(()=>J('PATCH','/api/subs/'+id,{link_ids:ids}),'ذخیره شد ✓')},
csave(id){const b={name:v_('c_n'),limit_value:n_('c_g'),limit_unit:'GB',expires_days:n_('c_d'),ip_limit:n_('c_i'),connection_limit:n_('c_c')};if(!b.name)return tt('نام را وارد کنید',1);SW(()=>id?J('PATCH','/api/categories/'+id,b):J('POST','/api/categories',b),'ذخیره شد ✓')},
cdelc(id){ask('دسته‌بندی حذف شود؟',()=>SW(()=>J('DELETE','/api/categories/'+id),'حذف شد'))},
nodsave(id){const b={id:id||undefined,name:v_('nd_n'),url:v_('nd_u'),token:v_('nd_t')};if(!b.name||!b.url)return tt('نام و آدرس لازم است',1);SW(()=>J('POST','/api/nodes',b),'ذخیره شد ✓')},
async nodtest(id){const b={id:id||undefined,name:v_('nd_n'),url:v_('nd_u'),token:v_('nd_t')},bx=$('nd_r');bx.innerHTML='<small>در حال تست…</small>';try{const s=(await J('POST','/api/nodes/test',b)).status||{};bx.innerHTML=s.online?`<div class="tg live" style="display:block;margin-bottom:8px;padding:6px 10px">متصل · ${Math.round(s.latency_ms||0)}ms · v${e(s.version||'?')} · ${s.inbounds??0} اینباند</div>`:`<div class="tg bad" style="display:block;margin-bottom:8px;padding:6px 10px">${e(s.error||'اتصال ناموفق')}</div>`}catch(x){bx.innerHTML='';ER(x)}},
nodchk(id){SW(()=>J('POST',`/api/nodes/${id}/check`,{}),'بررسی شد')},nodall(){SW(()=>J('POST','/api/nodes/check-all',{}),'همه بررسی شدند',1)},
nodtog(id){const n=S.nodes.find(x=>x.id==id);SW(()=>J('POST','/api/nodes',{id,name:n.name,url:n.url,enabled:!n.enabled}),'انجام شد ✓')},
noddel(id){ask('نود حذف شود؟',()=>SW(()=>J('DELETE','/api/nodes/'+id),'حذف شد'))},
prxsave(){const b={name:v_('px_n'),host:v_('px_h'),port:n_('px_p'),username:v_('px_u'),password:$('px_w').value};if(!b.host||!b.port)return tt('هاست و پورت لازم است',1);if(!b.name)b.name=b.host;SW(()=>J('POST','/api/proxies',b),'اضافه شد ✓')},
prxt(id){tt('در حال تست…');SW(()=>J('POST',`/api/proxies/${id}/test`,{}),'تست انجام شد',1)},
prxd(id){ask('پروکسی حذف شود؟',()=>SW(()=>J('DELETE','/api/proxies/'+id),'حذف شد',1))},
pf(id,x,t){document.querySelectorAll('#ap_pf button').forEach(b=>b.classList.toggle('on',b.dataset.id==id));S.pf=id},
autogo(){const b={profile:S.pf||'balanced',combo:$('ap_cb').checked};if(n_('ap_p'))b.port=n_('ap_p');if(n_('ap_n'))b.pairs_count=n_('ap_n');if(v_('ap_o'))b.outbound_proxy_id=v_('ap_o');SW(()=>J('POST','/api/links/auto',b),'ساخته شد ✓',1)},
cmbgo(){const o=[...document.querySelectorAll('.cmo:checked')].map(x=>x.value),b={label:v_('cm_l'),limit_value:n_('cm_g'),limit_unit:'GB',expires_days:n_('cm_d'),pairs_count:n_('cm_n')||2,config_count:n_('cm_c')||1,client_limit:n_('cm_k'),ip_limit:n_('cm_i'),connection_limit:n_('cm_x')};if(n_('cm_p'))b.port=n_('cm_p');if(v_('cm_ct'))b.category_id=v_('cm_ct');if(o.length){b.outbound_proxy_ids=o;b.outbound_proxy_id=o[0]}SW(()=>J('POST','/api/links/combo',b),'کامبو ساخته شد ✓',1)},
errclr(){SW(()=>J('POST','/api/errors/clear',{}),'پاک شد',1)},
rq(id,k){SW(async()=>{const r=await J('POST',`/api/admin-requests/${id}/${k}`,{});const m=r.message||r.text||r.telegram_message;if(k=='approve'&&m)sheet(hd('درخواست تایید شد','این پیام را برای متقاضی بفرستید')+`<div class="u" style="white-space:pre-wrap">${e(m)}</div><button class="btn p w" data-a="cptxt" data-v="${e(m)}"><i class="ti ti-copy"></i> کپی پیام</button>`)},'انجام شد ✓',1)},
cptxt(id,v){cp(v)},
admsave(id){const pm=PERMS.filter(p=>$('pm_'+p[0]).checked).map(p=>p[0]);if(!pm.includes('dashboard'))pm.push('dashboard');const b={permissions:pm};if(v_('d_p'))b.password=$('d_p').value;SW(async()=>{if(id)await J('PATCH','/api/admins/'+id,b);else{b.username=v_('d_u');if(!b.username||!b.password)throw Error('نام کاربری و رمز لازم است');await J('POST','/api/admins',b)}},'ذخیره شد ✓')},
admtog(id){const a=S.adm.find(x=>x.id==id);SW(()=>J('PATCH','/api/admins/'+id,{active:a.active===false}),'انجام شد ✓')},
admdel(id){ask('ادمین حذف شود؟',()=>SW(()=>J('DELETE','/api/admins/'+id),'حذف شد'))},
botsave(){SW(()=>J('POST','/api/settings',{bot_token:v_('bt'),bot_admin_ids:v_('bi'),bot_auto_start:$('ba').checked}),'ذخیره شد ✓',1)},
botgo(id){SW(()=>J('POST','/api/settings/bot/'+id,{}),id=='start'?'ربات روشن شد':'ربات خاموش شد',1)},
setsave(){const b={public_base_url:v_('sb'),tcp_public_host:v_('sh'),tcp_public_port:v_('sp'),support_username:v_('su'),channel_username:v_('sc')};Object.keys(S.set).filter(k=>/^(sub_|name_style)/.test(k)).forEach(k=>{if($('k_'+k))b[k]=$('k_'+k).checked});SW(()=>J('POST','/api/settings',b),'ذخیره شد ✓',1)},
pw(){if(v_('p1')!==v_('p2'))return tt('تکرار رمز یکسان نیست',1);SW(()=>J('POST','/api/change-password',{current_password:$('p0').value,new_password:$('p1').value,repeat_password:$('p2').value}),'رمز تغییر کرد ✓',1)},
un(){SW(()=>J('POST','/api/change-username',{username:v_('u1'),current_password:$('u0').value}),'نام کاربری تغییر کرد ✓',1)},
revoke(){ask('همهٔ نشست‌های دیگر خارج شوند؟',()=>SW(()=>J('POST','/api/security/revoke-other-sessions',{}),'انجام شد ✓',1))}};
document.addEventListener('click',ev=>{const t=ev.target.closest('[data-a]');if(!t||!t.dataset.a)return;ev.preventDefault();const f=A[t.dataset.a];f&&f(t.dataset.id,t.dataset.v)});
$('gs').addEventListener('input',function(){S.q=this.value;clearTimeout(S.dq);S.dq=setTimeout(draw,180)});
$('v').innerHTML=sk();shell();addEventListener('resize',shell);
auth().then(draw).catch(x=>{$('v').innerHTML=`<div class="card em"><i class="ti ti-lock"></i><b>دسترسی ندارید</b><br><small>${e(x.message)}</small><br><small>این مینی‌اپ فقط برای ادمین‌های ربات است.</small></div>`});
setInterval(()=>{if(!$('sh').classList.contains('on')&&document.activeElement.tagName!='INPUT'&&!S.q&&['h','c','g','con'].includes(cur()))draw()},45000);
</script></body></html>
"""


def _tma_admin(request: Request) -> int:
    """اعتبارسنجی initData تلگرام (HMAC با توکن ربات) + فقط ادمین‌های ربات."""
    import hmac
    from urllib.parse import parse_qsl
    import telegram_bot as _tb
    cfg = _tb.current_config()
    token = cfg.get("bot_token") or ""
    raw = request.headers.get("x-tg-init", "")
    try:
        pairs = dict(parse_qsl(raw, keep_blank_values=True))
        got = pairs.pop("hash", "")
        check = "\n".join(f"{k}={v}" for k, v in sorted(pairs.items()))
        secret = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
        ok = bool(token) and hmac.compare_digest(hmac.new(secret, check.encode(), hashlib.sha256).hexdigest(), got)
        if not ok or time.time() - int(pairs.get("auth_date", "0")) > 86400:
            raise ValueError
        uid = int(json.loads(pairs["user"])["id"])
    except Exception:
        raise HTTPException(status_code=401, detail="احراز هویت تلگرام نامعتبر است")
    if uid not in {int(x) for x in str(cfg.get("admin_ids", "")).split(",") if x.strip().isdigit()}:
        raise HTTPException(status_code=403, detail="شما ادمین ربات نیستید")
    return uid


def _tma_item(request: Request, uid: str, l: dict, host: str) -> dict:
    exp = l.get("expires_at")
    try:
        days = max(0, int((datetime.fromisoformat(str(exp)) - datetime.now()).total_seconds() // 86400)) if exp else None
    except Exception:
        days = None
    return {
        "id": uid, "label": l.get("label", "?"), "active": bool(l.get("active", True)),
        "used": int(l.get("used_bytes") or 0), "limit": int(l.get("limit_bytes") or 0), "days": days,
        "online": len(unique_ips_for_uuid(uid)),
        "link": vless_link_for_link(l, uid, host), "sub": f"{get_web_base(host)}/sub/{uid}",
        "parent": l.get("parent_inbound_id"), "port": l.get("port"), "protocol": l.get("protocol"),
    }


@app.middleware("http")
async def _vw_session_header(request: Request, call_next):
    """مینی‌اپ تلگرام: توکن نشست را از هدر x-vw-session به‌صورت کوکی به همان APIهای پنل می‌رساند."""
    try:
        _REQ_WEB.set(_capture_request_web(request))
    except Exception:
        pass
    tok = request.headers.get("x-vw-session")
    if tok and SESSION_COOKIE not in request.cookies:
        old = request.headers.get("cookie", "")
        cookie = (old + "; " if old else "") + f"{SESSION_COOKIE}={tok}"
        request.scope["headers"] = [(k, v) for k, v in request.scope["headers"] if k != b"cookie"] + [(b"cookie", cookie.encode())]
    return await call_next(request)


@app.get("/app", response_class=HTMLResponse, include_in_schema=False)
@app.get("/miniapp", response_class=HTMLResponse, include_in_schema=False)
async def tma_page():
    return HTMLResponse(TMA_HTML, headers={"Cache-Control": "no-store"})


@app.post("/api/tma/{action}", include_in_schema=False)
async def tma_api(action: str, request: Request):
    _tma_admin(request)
    if action == "session":
        return {"ok": True, "token": await create_session("owner", "owner")}
    try:
        b = await request.json()
    except Exception:
        b = {}
    host = get_host(request)
    if action == "create":
        gb, days = float(b.get("gb") or 0), int(b.get("days") or 0)
        label = decorate_label(sanitize_display_name(str(b.get("label")))) if str(b.get("label") or "").strip() else auto_display_name()
        proto = str(b.get("protocol") or "")
        if proto not in LIVE_PROTOCOLS:
            proto = "vless-ws" if "vless-ws" in LIVE_PROTOCOLS else DEFAULT_PROTOCOL
        uid, link = await make_link(
            label=label, limit_bytes=int(parse_size_to_bytes(gb, "GB")) if gb > 0 else 0,
            expires_at=(datetime.now() + timedelta(days=days)).isoformat() if days > 0 else None,
            protocol=proto, port=max(1, min(65535, int(b.get("port") or DEFAULT_PORT))),
            ip_limit=max(0, int(b.get("ip") or 0)), connection_limit=max(0, int(b.get("conn") or 0)),
            note=str(b.get("note") or "")[:200],
        )
        return {"ok": True, "item": _tma_item(request, uid, link, host)}
    if action == "edit":
        uid, op, v = str(b.get("id")), b.get("op"), b.get("v")
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="کانفیگ پیدا نشد")
        if op == "del":
            await remove_link(uid)
        elif op == "toggle":
            await set_link_active(uid, not LINKS[uid].get("active", True))
        elif op == "gb":
            if not int(LINKS[uid].get("limit_bytes") or 0):
                raise HTTPException(status_code=400, detail="حجم این کانفیگ نامحدود است")
            await update_link_fields(uid, add_bytes=int(parse_size_to_bytes(float(v), "GB")))
        elif op == "d":
            await update_link_fields(uid, extend_days=int(v))
        elif op == "reset":
            await update_link_fields(uid, reset_usage=True)
        elif op == "rname":
            await update_link_fields(uid, label=auto_display_name())
        return {"ok": True}
    if action == "client_add":
        gb = float(b.get("gb") or 0)
        lab = str(b.get("label") or "").strip()
        res = await add_client_to_inbound(
            str(b.get("id")), label=decorate_label(sanitize_display_name(lab)) if lab else None,
            limit_bytes=int(parse_size_to_bytes(gb, "GB")) if gb > 0 else None, expires_days=int(b.get("days") or 0),
        )
        if not res:
            raise HTTPException(status_code=400, detail="ساخت کلاینت ممکن نیست")
        return {"ok": True}
    if action in ("group", "group_create"):
        name = sanitize_display_name(str(b.get("name") or "")) or "VodiWalker"
        sid, _s = await create_sub_group(name=name, password=str(b.get("password") or ""))
        ids = b.get("ids") or [u for u, l in LINKS.items() if l.get("active", True) and not l.get("parent_inbound_id")]
        for u in ids:
            await set_link_sub(str(u), sid)
        return {"ok": True}
    if action == "group_set":
        gid = str(b.get("gid"))
        if gid not in SUBS:
            raise HTTPException(status_code=404, detail="گروه پیدا نشد")
        want = {str(x) for x in (b.get("ids") or [])}
        for u in list(SUBS[gid].get("link_ids") or []):
            if u not in want:
                await set_link_sub(u, None)
        for u in want:
            await set_link_sub(u, gid)
        return {"ok": True}
    if action == "group_del":
        if await remove_sub_group(str(b.get("gid"))) is None:
            raise HTTPException(status_code=404, detail="گروه پیدا نشد")
        return {"ok": True}
    if action == "activity":
        return {"logs": list(activity_logs)[-80:][::-1]}
    if action == "support":
        v = _clean_tg_username(b.get("v"))
        if v and not _TG_USER_RE.match(v):
            raise HTTPException(status_code=400, detail="آیدی تلگرام معتبر نیست")
        CONFIG["support_username"] = v
        await save_state()
        return {"ok": True}
    if action != "state":
        raise HTTPException(status_code=404, detail="unknown")
    import psutil
    items = sorted((_tma_item(request, u, l, host) for u, l in LINKS.items()), key=lambda x: x["label"])
    base = get_public_base(request) or f"{get_web_base(host)}"
    return {
        "links": items, "total": len(items), "active": sum(1 for i in items if i["active"]),
        "near": sum(1 for i in items if i["active"] and ((i["days"] is not None and i["days"] <= 3) or (i["limit"] and i["used"] >= i["limit"] * .85))),
        "traffic": sum(i["used"] for i in items), "online": sum(i["online"] for i in items),
        "protocols": sorted(LIVE_PROTOCOLS),
        "groups": [{"id": sid_, "ids": list(s.get("link_ids") or []), "name": s.get("name", "?"), "count": len(s.get("link_ids") or []), "url": f"{base}/p/{s.get('uuid_key', '')}"} for sid_, s in SUBS.items()],
        "srv": {"cpu": psutil.cpu_percent(), "ram": psutil.virtual_memory().percent, "disk": psutil.disk_usage("/").percent},
        "host": host, "support": get_support_username(),
    }



@app.get("/api/name-suggestions")
async def api_name_suggestions(request: Request, _=Depends(require_auth)):
    base = request.query_params.get("base", "")
    count = safe_int(request.query_params.get("n"), default=12, minimum=4, maximum=24)
    return {
        "ok": True,
        "enabled": bool(CONFIG.get("name_style_enabled", True)),
        "suggestions": name_suggestions(base, count),
    }


@app.post("/api/links")
async def create_link_api(
    request: Request,
    _=Depends(require_auth),
):

    try:
        body = await request.json()

        if not isinstance(body, dict):
            raise ValueError(
                "body is not object"
            )

    except Exception as exc:

        logger.exception(
            "Create link JSON error: %s",
            exc,
        )

        raise HTTPException(
            status_code=400,
            detail="اطلاعات ارسال‌شده معتبر نیست.",
        )

    limit_value = safe_float(
        body.get(
            "limit_value",
            0,
        )
    )

    limit_unit = str(
        body.get(
            "limit_unit",
            "GB",
        )
        or "GB"
    ).upper()

    limit_bytes = (
        0
        if limit_value <= 0
        else parse_size_to_bytes(
            limit_value,
            limit_unit,
        )
    )

    expires_days = safe_int(
        body.get(
            "expires_days",
            0,
        ),
        minimum=0,
    )

    expires_at = (
        (
            datetime.now()
            + timedelta(
                days=expires_days
            )
        ).isoformat()
        if expires_days > 0
        else None
    )

    port = safe_int(
        body.get(
            "port",
            DEFAULT_PORT,
        ),
        default=DEFAULT_PORT,
        minimum=MIN_PORT,
        maximum=MAX_PORT,
    )

    ip_limit = safe_int(
        body.get(
            "ip_limit",
            0,
        ),
        minimum=0,
    )

    speed_value = safe_float(
        body.get(
            "speed_limit_value",
            0,
        )
    )

    speed_unit = str(
        body.get(
            "speed_limit_unit",
            "MBIT",
        )
        or "MBIT"
    ).upper()

    speed_bytes = (
        0
        if speed_value <= 0
        else parse_speed_to_bytes(
            speed_value,
            speed_unit,
        )
    )

    connection_limit = safe_int(
        body.get(
            "connection_limit",
            0,
        ),
        minimum=0,
    )

    protocol = str(
        body.get(
            "protocol",
            DEFAULT_PROTOCOL,
        )
        or DEFAULT_PROTOCOL
    ).strip().lower()

    if protocol != "manual" and protocol not in PROTOCOLS:
        protocol = DEFAULT_PROTOCOL

    manual_fields = body.get("manual") or {}
    if not isinstance(manual_fields, dict):
        manual_fields = {}

    fingerprint = str(
        body.get(
            "fingerprint",
            DEFAULT_FINGERPRINT,
        )
        or DEFAULT_FINGERPRINT
    ).strip().lower()

    if fingerprint not in FINGERPRINTS:
        fingerprint = DEFAULT_FINGERPRINT

    fragment = str(
        body.get(
            "fragment",
            "off",
        )
        or "off"
    ).strip().lower()

    allowed_fragments = {
        "off",
        "safe",
        "balanced",
        "aggressive",
    }

    if fragment not in allowed_fragments:
        fragment = "off"

    raw_clean = body.get("clean_ips") or body.get("clean_ip") or ""
    if isinstance(raw_clean, list):
        clean_ips = [str(x).strip() for x in raw_clean if str(x).strip()]
    else:
        clean_ips = [x.strip() for x in str(raw_clean).replace(",", "\n").splitlines() if x.strip()]
    alarm_enabled = bool(body.get("alarm_enabled", False))
    category_id = str(body.get("category_id") or "0")
    if category_id not in CATEGORIES:
        category_id = "0"
    config_count = safe_int(body.get("config_count", 1), minimum=1, maximum=40)
    client_limit = safe_int(body.get("client_limit", 0), minimum=0, maximum=1000)
    requested_expires_at = str(body.get("expires_at") or "").strip()
    if requested_expires_at:
        try:
            dt = datetime.fromisoformat(requested_expires_at.replace("Z", "+00:00"))
            expires_at = dt.replace(tzinfo=None).isoformat()
        except Exception:
            raise HTTPException(status_code=400, detail="زمان انقضا معتبر نیست")
    cat = CATEGORIES.get(category_id) or {}
    if cat.get("limit_bytes") and limit_bytes <= 0:
        limit_bytes = int(cat["limit_bytes"])
    if cat.get("expires_days") and expires_days <= 0:
        expires_days = int(cat["expires_days"])
        expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat() if expires_days > 0 else None
    if cat.get("connection_limit") and connection_limit <= 0:
        connection_limit = int(cat["connection_limit"])
    if cat.get("speed_limit_bytes") and speed_bytes <= 0:
        speed_bytes = int(cat["speed_limit_bytes"])
    if cat.get("ip_limit") and ip_limit <= 0:
        ip_limit = int(cat["ip_limit"])
    if cat.get("clean_ips") and not clean_ips:
        clean_ips = list(cat["clean_ips"])
    if cat.get("single_user"):
        if ip_limit == 0: ip_limit = 1
        if connection_limit == 0: connection_limit = 1
    label_val = body.get("label", "")
    if cat.get("random_name") or not str(label_val).strip():
        label_val = auto_display_name()
    else:
        label_val = decorate_label(sanitize_display_name(str(label_val)))

    uid, link = await make_link(
        label=label_val,
        limit_bytes=limit_bytes,
        expires_at=expires_at,
        note=body.get(
            "note",
            "",
        ),
        sub_id=body.get(
            "sub_id"
        ),
        protocol=protocol,
        fingerprint=fingerprint,
        alpn=body.get(
            "alpn",
            DEFAULT_ALPN_BY_PROTOCOL.get(
                protocol,
                "http/1.1",
            ),
        ),
        port=port,
        ip_limit=ip_limit,
        speed_limit_bytes=speed_bytes,
        connection_limit=connection_limit,
        fragment=fragment,
        clean_ips=clean_ips,
        alarm_enabled=alarm_enabled,
        category_id=category_id,
        config_count=config_count,
        manual_fields=manual_fields,
        outbound_proxy_id=clean_outbound_proxy_id(body.get("outbound_proxy_id")),
    )

    async with LINKS_LOCK:
        LINKS[uid]["client_limit"] = client_limit
    await save_state()

    host = get_host(request)

    result = {
        **get_link_info(
            link,
            uid,
            host,
        ),
        "ok": True,
    }

    return result


# ============================================================
# WS + XHTTP COMBO SUBSCRIPTION  ·  OUTBOUND (EXIT) CONTROL
# ============================================================
#
# «کامبو» = یک گروه ساب (یک لینک اشتراک) که برای هر «خروجی» انتخاب‌شده دقیقاً
# دو اینباند دارد: یک VLESS-WS و یک VLESS-XHTTP. خروجی یعنی مسیر خروج ترافیک:
#   ""        -> مستقیم از خود Railway
#   "<id>"    -> از یک پراکسی SOCKS5 (outbound_proxy.py)
# با یک خروجی: اشتراک دقیقاً ۲ خط دارد (۱ WS + ۱ XHTTP).
# با N خروجی : اشتراک ۲×N خط دارد و اسم هر خط با کد کشورش تفکیک می‌شود.

COMBO_MEMBERS = (("vless-ws", "ws"), ("xhttp-packet-up", "xhttp"))
MAX_COMBO_EXITS = 20
MAX_BULK_LINKS = 500

# اموجی‌های «خفن» که به‌ترتیب برای هر خروجی/کانفیگ جدید استفاده می‌شن (چرخشی).
CONFIG_EMOJI_POOL = [
    "🚀", "⚡", "🔥", "🛡", "🌪", "💎", "🦾", "🌊", "🎯", "🧿",
    "🐉", "🦅", "🌟", "🛰", "🧊", "🌀", "🪐", "🦁", "🔱", "💠",
    "🧨", "🌈", "🦈", "🐺", "🔮", "🛸", "🧬", "🕹", "🎇", "🌋",
]


def sanitize_display_name(name: str, fallback: str = "VodiWalker") -> str:
    """برخلاف sanitize_config_name (که فقط ASCII نگه می‌داره و برای اسم داخلیِ
    گروه/اسلاگ استفاده می‌شه)، این تابع اسمی که کاربر برای نمایش در کلاینت
    انتخاب کرده (فارسی/انگلیسی/هر چیزی، به‌همراه فاصله) رو دست‌نخورده نگه
    می‌داره و فقط کاراکترهای کنترلی/خط‌جدید رو حذف و طولش رو محدود می‌کنه."""
    cleaned = "".join(ch for ch in str(name or "") if ch.isprintable()).strip()
    return cleaned[:40] if cleaned else fallback


def emoji_for_index(i: int) -> str:
    return CONFIG_EMOJI_POOL[i % len(CONFIG_EMOJI_POOL)]


# ---------------- اسم‌های خفن برای کانفیگ‌ها (دستی و خودکار) ----------------
COOL_WORDS = [
    "Tofan", "Barq", "Shahab", "Simorgh", "Parvaz", "Aftab", "Setareh", "Atash", "Sayeh", "Oghab",
    "Palang", "Rostam", "Sohrab", "Kaveh", "Arash", "Zagros", "Alborz", "Damavand", "Ghoghnoos", "Azhdaha",
    "Storm", "Thunder", "Phantom", "Ghost", "Nova", "Falcon", "Viper", "Titan", "Orbit", "Comet",
    "Pulse", "Turbo", "Rocket", "Blaze", "Shadow", "Vortex", "Nebula", "Zenith", "Apex", "Matrix",
    "Cyber", "Neon", "Sonic", "Hyper", "Warp", "Quantum", "Nitro", "Spark", "Wolf", "Dragon", "Phoenix", "Raven",
]
COOL_EMOJIS = [
    "🚀", "⚡", "🔥", "🌪️", "🦅", "🐉", "🛡️", "💎", "🌌", "⭐", "✨", "🧿", "🏹", "⚔️", "👑", "💜",
    "🌐", "🛰️", "🦁", "🐺", "🦋", "🌙", "☄️", "🎯", "💫", "🔮", "🧬", "🏴‍☠️", "🌋", "🪐", "🛸", "💠",
    "🔱", "🧊", "🌀", "🎇",
]
COOL_STYLES = [
    "{base}|{word}{emoji}",
    "{emoji} {base} | {word}",
    "{base} ✦ {word} {emoji}",
    "{base}·{word}{emoji}{emoji2}",
    "【{base}】{word}{emoji}",
    "{base} ⟪{word}⟫ {emoji}",
    "{emoji}{base}-{word}",
    "{base} ▸ {word} {emoji}",
]


def is_name_styled(name: str) -> bool:
    """اگر کاربر خودش اسم را تزئین کرده باشد (| یا اموجی/نماد)، دیگر دست نمی‌زنیم."""
    text = str(name or "")
    return "|" in text or any(ord(ch) >= 0x2190 for ch in text)


def style_config_name(base: str, index: int | None = None, style: int | None = None) -> str:
    """Vodiwalker → Vodiwalker|Tofan🚀 ؛ با index هر خروجی اسم/اموجی متفاوتی می‌گیرد."""
    base = "".join(ch for ch in str(base or "") if ch.isprintable()).strip()[:32] or "VodiWalker"
    rnd = secrets.SystemRandom()
    if index is None:
        word, emoji = rnd.choice(COOL_WORDS), rnd.choice(COOL_EMOJIS)
        emoji2 = rnd.choice(COOL_EMOJIS)
    else:
        word = COOL_WORDS[index % len(COOL_WORDS)]
        emoji = COOL_EMOJIS[(index * 5 + 1) % len(COOL_EMOJIS)]
        emoji2 = COOL_EMOJIS[(index * 5 + 9) % len(COOL_EMOJIS)]
    tpl = COOL_STYLES[(style or 0) % len(COOL_STYLES)]
    return tpl.format(base=base, word=word, emoji=emoji, emoji2=emoji2)[:60]


def decorate_label(base: str, index: int | None = None) -> str:
    """اعمال استایل خودکار روی اسم (در صورت فعال بودن از تنظیمات و تزئین‌نشده بودن اسم)."""
    if CONFIG.get("name_style_enabled", True) and not is_name_styled(base):
        return style_config_name(base, index=index)
    return base


def auto_display_name() -> str:
    """اسم خودکار خفن برای وقتی که کاربر چیزی ننوشته."""
    if CONFIG.get("name_style_enabled", True):
        return style_config_name("VodiWalker")
    return auto_config_name()


def name_suggestions(base: str, count: int = 12) -> list[str]:
    base = sanitize_display_name(base, "VodiWalker")
    rnd = secrets.SystemRandom()
    words = rnd.sample(COOL_WORDS, min(count, len(COOL_WORDS)))
    out: list[str] = []
    for i, word in enumerate(words):
        tpl = COOL_STYLES[0] if i < 4 else COOL_STYLES[i % len(COOL_STYLES)]
        out.append(tpl.format(base=base[:32], word=word, emoji=rnd.choice(COOL_EMOJIS), emoji2=rnd.choice(COOL_EMOJIS))[:60])
    return out


def normalize_exit_ids(body: dict) -> list[str]:
    """لیست یکتا و اعتبارسنجی‌شده‌ی خروجی‌ها از بدنه‌ی درخواست.
    هم `outbound_proxy_ids: [...]` و هم `outbound_proxy_id: "..."` قبول می‌شود."""
    raw = body.get("outbound_proxy_ids")
    if raw is None:
        raw = [body.get("outbound_proxy_id") or ""]
    elif not isinstance(raw, list):
        raise HTTPException(status_code=400, detail="لیست خروجی‌ها معتبر نیست")
    exits: list[str] = []
    for item in raw:
        pid = clean_outbound_proxy_id(item)
        if pid not in exits:
            exits.append(pid)
    if not exits:
        exits = [""]
    if len(exits) > MAX_COMBO_EXITS:
        raise HTTPException(status_code=400, detail=f"حداکثر {MAX_COMBO_EXITS} خروجی همزمان مجاز است")
    return exits


def _exit_tag(info: dict | None, used: dict) -> str:
    """پسوند کوتاه ASCII برای اسم کانفیگ: de / us / dir (مستقیم)؛ تکراری‌ها de2, de3 ..."""
    if not info:
        tag = "dir"
    else:
        cc = "".join(ch for ch in str(info.get("country_code") or "").lower() if ch.isascii() and ch.isalnum())
        tag = cc[:3] or "px"
    used[tag] = used.get(tag, 0) + 1
    return tag if used[tag] == 1 else f"{tag}{used[tag]}"


async def create_combo_subscription(
    request: Request,
    *,
    exits: list[str],
    pairs_per_exit: int = 1,
    port: int,
    label: str = "",
    group_name: str = "",
    limit_bytes: int = 0,
    expires_at: str | None = None,
    ip_limit: int = 0,
    connection_limit: int = 0,
    speed_limit_bytes: int = 0,
    fingerprint: str = DEFAULT_FINGERPRINT,
    fragment: str = "off",
    note: str = "",
    category_id: str = "0",
    client_limit: int = 0,
    config_count: int = 1,
    clean_ips=None,
    alarm_enabled: bool = False,
    security_profile: str = "balanced",
) -> dict:
    """یک گروه ساب می‌سازد و برای هر خروجی یک WS + یک XHTTP داخلش می‌گذارد."""
    host = get_host(request)
    display_name = sanitize_display_name(label) if str(label or "").strip() else "VodiWalker"
    base = sanitize_config_name(label) if str(label or "").strip() else auto_config_name()
    infos = {pid: outbound_info(pid) for pid in exits}
    _emoji_counter = 0

    def _flag_country(info):
        return f"{info.get('flag') or ''} {info.get('country') or info.get('name') or ''}".strip()

    desc = "WS + XHTTP · خروجی: " + " ، ".join(_flag_country(infos[p]) if infos[p] else "مستقیم" for p in exits)
    sub_id, sub = await create_sub_group(name=(group_name or base)[:60], desc=desc[:200])

    pairs_per_exit = max(1, min(40, int(pairs_per_exit or 1)))
    used_tags: dict = {}
    multi = len(exits) > 1 or pairs_per_exit > 1
    rows: list[dict] = []
    items: list[dict] = []

    for pid in exits:
        for _pair_i in range(pairs_per_exit):
            # هر بار که تگ برای همون pid دوباره خواسته بشه، _exit_tag خودش شماره‌گذاری
            # می‌کنه (de, de2, de3, ...) — دقیقاً همون چیزی که برای «تعداد کل کانفیگ» لازمه.
            tag = _exit_tag(infos[pid], used_tags) if multi else ""
            row = {"outbound_proxy_id": pid, "outbound": infos[pid], "tag": tag}
            # هر خروجی/جفت یک اموجی خفنِ مخصوص خودش می‌گیره؛ اسم نمایشی برای همه‌شون
            # همون اسمیه که کاربر انتخاب کرده (WS و XHTTP یک خروجی هم اموجی مشترک دارن).
            pair_emoji = emoji_for_index(_emoji_counter)
            _emoji_counter += 1
            display_label = (
                decorate_label(display_name, _emoji_counter - 1)
                if CONFIG.get("name_style_enabled", True) and not is_name_styled(display_name)
                else f"{pair_emoji} {display_name}"
            )
            for protocol, suffix in COMBO_MEMBERS:
                uid, link = await make_link(
                    label=display_label,
                    limit_bytes=limit_bytes,
                    expires_at=expires_at,
                    note=note,
                    sub_id=sub_id,
                    protocol=protocol,
                    fingerprint=fingerprint,
                    alpn=DEFAULT_ALPN_BY_PROTOCOL.get(protocol, ""),
                    port=port,
                    ip_limit=ip_limit,
                    speed_limit_bytes=speed_limit_bytes,
                    connection_limit=connection_limit,
                    fragment=fragment,
                    clean_ips=clean_ips,
                    alarm_enabled=alarm_enabled,
                    category_id=category_id,
                    config_count=config_count,
                    outbound_proxy_id=pid,
                )
                async with LINKS_LOCK:
                    LINKS[uid]["combo_group_id"] = sub_id
                    # combo_tag یعنی «شریک جفت»: ws و xhttپ همین تگ، تا موقع ساخت
                    # کلاینت بشه جفتشون رو پیدا کرد و توی یک ساب گذاشت (نه دوتا جدا).
                    LINKS[uid]["combo_tag"] = tag
                    LINKS[uid]["combo_base_label"] = display_name
                    LINKS[uid]["client_limit"] = client_limit
                    LINKS[uid]["security_profile"] = security_profile
                row[suffix] = uid
                items.append(get_link_info(LINKS[uid], uid, host))
            rows.append(row)

    await save_state()
    sub_url = f"{get_web_base(host)}/sub-group/{sub['uuid_key']}"
    public_url = f"{get_web_base(host)}/p/{sub['uuid_key']}"
    where = "، ".join(infos[p]["name"] if infos[p] else "مستقیم" for p in exits)
    log_activity("link", f"اشتراک WS+XHTTP روی پورت {port} ساخته شد (خروجی: {where})", "ok")
    return {
        "ok": True, "combo": True,
        "combo_group_id": sub_id, "sub_id": sub_id,
        "sub_url": sub_url, "public_url": public_url, "sub_name": sub.get("name", base),
        "exits": rows,
        "outbound": infos[exits[0]] if len(exits) == 1 else None,   # سازگاری با UI قدیمی
        "items": items,
    }


async def add_combo_exits(sub_id: str, host: str, new_exits: list[str]) -> dict:
    """به یک اشتراک WS+XHTTP از قبل موجود، بدون ساخت اشتراک جدید، خروجی‌های تازه
    اضافه می‌کنه — تنظیمات (پورت، فینگرپرینت، محدودیت‌ها و ...) دقیقاً از روی یکی
    از جفت‌های موجود همون گروه کپی می‌شه، فقط outbound_proxy_id عوض می‌شه."""
    async with LINKS_LOCK:
        existing_pairs = [(uid, dict(l)) for uid, l in LINKS.items() if l.get("combo_group_id") == sub_id]
    if not existing_pairs:
        raise ValueError("این گروه یک اشتراک WS+XHTTP نیست (هیچ جفتی در آن پیدا نشد)")
    template = existing_pairs[0][1]
    already = {l.get("outbound_proxy_id", "") for _uid, l in existing_pairs}

    to_add, seen = [], set()
    for raw in new_exits:
        pid = clean_outbound_proxy_id(raw)
        if pid in already or pid in seen:
            continue
        seen.add(pid)
        to_add.append(pid)
    if not to_add:
        return {"added": 0, "items": [], "skipped_existing": list(new_exits)}

    infos = {pid: outbound_info(pid) for pid in to_add}

    # از تگ‌های موجود میان همین گروه، شمارنده‌ی هر پیشوند (de, us, dir, ...) رو
    # دوباره می‌سازیم تا خروجی‌های جدید با شماره‌ی درست ادامه پیدا کنن (de -> de2)
    used_tags: dict = {}
    for tag in {l.get("combo_tag", "") for _uid, l in existing_pairs if l.get("combo_tag")}:
        m = re.match(r"^([a-zA-Z]+)(\d*)$", tag)
        if not m:
            continue
        base, num = m.group(1), m.group(2)
        used_tags[base] = max(used_tags.get(base, 0), int(num) if num else 1)
    multi = True  # با بیش از یک خروجی در گروه، تگ‌گذاری همیشه لازمه

    rows, items = [], []
    _existing_exit_count = len(existing_pairs) // max(1, len(COMBO_MEMBERS))
    _combo_display_name = (
        template.get("combo_base_label")
        or sanitize_display_name(template.get("label") or "")
        or "VodiWalker"
    )
    for _add_i, pid in enumerate(to_add):
        tag = _exit_tag(infos[pid], used_tags)
        row = {"outbound_proxy_id": pid, "outbound": infos[pid], "tag": tag}
        pair_emoji = emoji_for_index(_existing_exit_count + _add_i)
        display_label = (
            decorate_label(_combo_display_name, _existing_exit_count + _add_i)
            if CONFIG.get("name_style_enabled", True) and not is_name_styled(_combo_display_name)
            else f"{pair_emoji} {_combo_display_name}"
        )
        for protocol, suffix in COMBO_MEMBERS:
            uid, link = await make_link(
                label=display_label,
                limit_bytes=template.get("limit_bytes", 0),
                expires_at=template.get("expires_at"),
                note=template.get("note", ""),
                sub_id=sub_id,
                protocol=protocol,
                fingerprint=template.get("fingerprint", DEFAULT_FINGERPRINT),
                alpn=DEFAULT_ALPN_BY_PROTOCOL.get(protocol, ""),
                port=int(template.get("port") or DEFAULT_PORT),
                ip_limit=template.get("ip_limit", 0),
                speed_limit_bytes=template.get("speed_limit_bytes", 0),
                connection_limit=template.get("connection_limit", 0),
                fragment=template.get("fragment", "off"),
                clean_ips=list(template.get("clean_ips") or []),
                alarm_enabled=bool(template.get("alarm_enabled", False)),
                category_id=template.get("category_id", "0"),
                config_count=template.get("config_count", 1),
                outbound_proxy_id=pid,
            )
            async with LINKS_LOCK:
                LINKS[uid]["combo_group_id"] = sub_id
                LINKS[uid]["combo_tag"] = tag
                LINKS[uid]["client_limit"] = template.get("client_limit", 0)
                LINKS[uid]["security_profile"] = template.get("security_profile", "balanced")
            row[suffix] = uid
            items.append(get_link_info(LINKS[uid], uid, host))
        rows.append(row)

    await save_state()
    where = "، ".join((infos[p]["name"] if infos[p] else "مستقیم") for p in to_add)
    async with SUBS_LOCK:
        sub_name = (SUBS.get(sub_id) or {}).get("name", "")
    log_activity("link", f"{len(to_add)} خروجی تازه (WS+XHTTP) به اشتراک «{sub_name}» اضافه شد: {where}", "ok")
    return {"added": len(to_add), "exits": rows, "items": items}


@app.post("/api/subs/{sub_id}/combo-exits")
async def api_add_combo_exits(sub_id: str, request: Request, _=Depends(require_auth)):
    """چک‌باکسی: هر چقدر پروکسی (به‌علاوه‌ی «مستقیم» اگه بخوای) روی این اشتراک بزن —
    برای هرکدوم که هنوز نداره، یک جفت WS+XHTTP تازه با همون تنظیمات ساخته می‌شه."""
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="گروه ساب پیدا نشد")
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON نامعتبر است")
    exits = body.get("outbound_proxy_ids") if isinstance(body, dict) else None
    if not isinstance(exits, list) or not exits:
        raise HTTPException(status_code=400, detail="حداقل یک خروجی (پروکسی یا مستقیم) انتخاب کن")
    if len(exits) > MAX_COMBO_EXITS:
        raise HTTPException(status_code=400, detail=f"حداکثر {MAX_COMBO_EXITS} خروجی در هر بار")
    host = get_host(request)
    try:
        result = await add_combo_exits(sub_id, host, exits)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"ok": True, **result}


@app.post("/api/links/auto")
async def create_auto_link(
    request: Request,
    _=Depends(require_auth),
):
    try:
        body = await request.json()
    except Exception:
        body = {}
    if not isinstance(body, dict):
        body = {}
    host = get_host(request)
    profile = str(body.get("profile", "balanced")).strip().lower()
    profiles = {
        # ساخت خودکار: محدودیت آی‌پی همیشه نامحدود (0) است
        "normal": {"ip":0,"conn":0,"speed":0,"fp":"chrome","fragment":"off"},
        "balanced": {"ip":0,"conn":4,"speed":0,"fp":"chrome","fragment":"safe"},
        "gaming": {"ip":0,"conn":2,"speed":0,"fp":"chrome","fragment":"safe"},
        "maximum": {"ip":0,"conn":0,"speed":0,"fp":"randomized","fragment":"safe"},
    }
    cfg = dict(profiles.get(profile, profiles["balanced"]))
    cfg["ip"] = 0  # حتی اگر پروفایل/درخواست چیز دیگری بگوید، ساخت خودکار = آی‌پی نامحدود
    port = safe_int(body.get("port", 443), minimum=MIN_PORT, maximum=MAX_PORT)
    exits = normalize_exit_ids(body)
    pairs_per_exit = max(1, (safe_int(body.get("pairs_count", 2), minimum=2, maximum=80) + 1) // 2)
    note = f"Auto generated by VodiWalker | profile={profile}"
    combo = bool(body.get("combo")) or str(body.get("protocol", "")).strip().lower() in ("combo", "ws+xhttp", "combo-ws-xhttp")

    if combo:
        result = await create_combo_subscription(
            request, exits=exits, pairs_per_exit=pairs_per_exit, port=port, note=note, fingerprint=cfg["fp"], fragment=cfg["fragment"],
            ip_limit=cfg["ip"], connection_limit=cfg["conn"], speed_limit_bytes=cfg["speed"], security_profile=profile,
        )
        result["profile"] = profile
        return result

    protocol = normalize_protocol(body.get("protocol", DEFAULT_PROTOCOL))
    uid, link = await make_link(
        label=auto_display_name(), limit_bytes=0, expires_at=None, note=note, protocol=protocol,
        fingerprint=cfg["fp"], alpn=DEFAULT_ALPN_BY_PROTOCOL.get(protocol, ""), port=port,
        ip_limit=cfg["ip"], speed_limit_bytes=cfg["speed"], connection_limit=cfg["conn"],
        fragment=cfg["fragment"], outbound_proxy_id=exits[0],
    )
    link["security_profile"] = profile
    log_activity("link", f"کانفیگ خودکار «{link['label']}» با {PROTOCOL_LABELS.get(protocol, protocol)} ساخته شد", "ok")
    return {**get_link_info(link, uid, host), "ok": True, "profile": profile}


@app.post("/api/links/combo")
async def create_combo_api(
    request: Request,
    _=Depends(require_auth),
):
    """«اینباند جدید» پیش‌فرض: یک اشتراک با ۱ WS + ۱ XHTTP برای هر خروجی انتخاب‌شده."""
    try:
        body = await request.json()
    except Exception:
        body = None
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="اطلاعات ارسال‌شده معتبر نیست.")

    exits = normalize_exit_ids(body)

    limit_value = safe_float(body.get("limit_value", 0))
    limit_unit = str(body.get("limit_unit", "GB") or "GB").upper()
    limit_bytes = 0 if limit_value <= 0 else parse_size_to_bytes(limit_value, limit_unit)
    expires_days = safe_int(body.get("expires_days", 0), minimum=0)
    speed_value = safe_float(body.get("speed_limit_value", 0))
    speed_unit = str(body.get("speed_limit_unit", "MBIT") or "MBIT").upper()
    speed_bytes = 0 if speed_value <= 0 else parse_speed_to_bytes(speed_value, speed_unit)
    ip_limit = safe_int(body.get("ip_limit", 0), minimum=0)
    connection_limit = safe_int(body.get("connection_limit", 0), minimum=0)
    port = safe_int(body.get("port", DEFAULT_PORT), default=DEFAULT_PORT, minimum=MIN_PORT, maximum=MAX_PORT)
    config_count = safe_int(body.get("config_count", 1), minimum=1, maximum=40)
    client_limit = safe_int(body.get("client_limit", 0), minimum=0, maximum=1000)

    fingerprint = str(body.get("fingerprint", DEFAULT_FINGERPRINT) or DEFAULT_FINGERPRINT).strip().lower()
    if fingerprint not in FINGERPRINTS:
        fingerprint = DEFAULT_FINGERPRINT
    fragment = str(body.get("fragment", "off") or "off").strip().lower()
    if fragment not in {"off", "safe", "balanced", "aggressive"}:
        fragment = "off"

    category_id = str(body.get("category_id") or "0")
    if category_id not in CATEGORIES:
        category_id = "0"
    cat = CATEGORIES.get(category_id) or {}
    clean_ips = list(cat.get("clean_ips") or [])
    if cat.get("limit_bytes") and limit_bytes <= 0:
        limit_bytes = int(cat["limit_bytes"])
    if cat.get("expires_days") and expires_days <= 0:
        expires_days = int(cat["expires_days"])
    if cat.get("connection_limit") and connection_limit <= 0:
        connection_limit = int(cat["connection_limit"])
    if cat.get("speed_limit_bytes") and speed_bytes <= 0:
        speed_bytes = int(cat["speed_limit_bytes"])
    if cat.get("ip_limit") and ip_limit <= 0:
        ip_limit = int(cat["ip_limit"])
    if cat.get("single_user"):
        ip_limit = ip_limit or 1
        connection_limit = connection_limit or 1
    expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat() if expires_days > 0 else None

    pairs_per_exit = max(1, (safe_int(body.get("pairs_count", 2), minimum=2, maximum=80) + 1) // 2)
    label = "" if cat.get("random_name") else str(body.get("label") or "").strip()
    return await create_combo_subscription(
        request, exits=exits, pairs_per_exit=pairs_per_exit, port=port, label=label, group_name=label,
        limit_bytes=limit_bytes, expires_at=expires_at, ip_limit=ip_limit,
        connection_limit=connection_limit, speed_limit_bytes=speed_bytes,
        fingerprint=fingerprint, fragment=fragment, note=str(body.get("note") or "")[:500],
        category_id=category_id, client_limit=client_limit, config_count=config_count,
        clean_ips=clean_ips, alarm_enabled=bool(body.get("alarm_enabled", False)),
    )


@app.post("/api/links/outbound")
async def set_links_outbound(
    request: Request,
    _=Depends(require_auth),
):
    """اعمال (یا تغییر) خروجی روی هر تعداد اینباند. کلاینت‌های هر اینباند هم
    پیش‌فرض همراهش عوض می‌شوند، چون ریلی خروجی را از UUID خودِ کلاینت می‌خواند.
    body: {uuids: [...], outbound_proxy_id: "" | "<id>", include_clients: true}"""
    try:
        body = await request.json()
    except Exception:
        body = None
    if not isinstance(body, dict) or not isinstance(body.get("uuids"), list) or not body["uuids"]:
        raise HTTPException(status_code=400, detail="حداقل یک اینباند انتخاب کنید.")
    if len(body["uuids"]) > MAX_BULK_LINKS:
        raise HTTPException(status_code=400, detail=f"حداکثر {MAX_BULK_LINKS} مورد در هر بار")
    pid = clean_outbound_proxy_id(body.get("outbound_proxy_id"))
    include_clients = bool(body.get("include_clients", True))
    targets = [str(u) for u in dict.fromkeys(body["uuids"])]

    updated, clients, missing = 0, 0, []
    async with LINKS_LOCK:
        for uid in targets:
            link = LINKS.get(uid)
            if link is None:
                missing.append(uid)
                continue
            link["outbound_proxy_id"] = pid
            updated += 1
            if include_clients:
                for child in LINKS.values():
                    if child.get("parent_inbound_id") == uid:
                        child["outbound_proxy_id"] = pid
                        clients += 1
    await save_state()
    info = outbound_info(pid)
    log_activity("link", f"خروجی {updated} اینباند و {clients} کلاینت روی «{info['name'] if info else 'مستقیم'}» تنظیم شد", "ok")
    return {"ok": True, "updated": updated, "clients": clients, "missing": missing, "outbound": info}


# ============================================================
# INBOUND CLIENT MANAGER
# ============================================================

async def add_client_to_inbound(uid: str, label: str = None, limit_bytes: int = None, expires_days: int = 0,
                                  ip_limit: int = None, speed_limit_bytes: int = None, connection_limit: int = None,
                                  note: str = None, outbound_proxy_id: str | None = None, created_by: str = "owner",
                                  operator: str | None = None):
    """Core logic to create a real client (child link) under an inbound. Shared by the
    HTTP API and the Telegram bot so both stay in sync."""
    async with LINKS_LOCK:
        parent = LINKS.get(uid)
        if not parent:
            raise ValueError("اینباند پیدا نشد")
        source = dict(parent)
        existing_clients = sum(1 for x in LINKS.values() if x.get("parent_inbound_id") == uid)
        client_limit = int(source.get("client_limit") or 0)
        if client_limit and existing_clients >= client_limit:
            raise ValueError(f"ظرفیت اینباند تکمیل است ({client_limit} کاربر)")
    final_label = str(label or f"Client · {existing_clients+1}").strip()[:120]
    _ops = getattr(app.state, "operators", None)
    _preset = _ops.preset(operator) if (_ops and operator) else None
    if _preset:
        final_label = f"{final_label} · {_preset['name']}"[:120]
    final_limit_bytes = safe_int(limit_bytes if limit_bytes is not None else source.get("limit_bytes", 0), minimum=0)
    expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat() if expires_days else source.get("expires_at")
    child_uid, child = await make_link(
        label=final_label,
        limit_bytes=final_limit_bytes,
        expires_at=expires_at,
        note=str(note or source.get("note") or "")[:500],
        # اشتراک ترکیبی «ساخت سریع» (یک WS + یک XHTTP) باید همیشه دقیقاً دو خط بمونه؛
        # پس کلاینتِ اینباندهای اون گروه وارد اون گروه نمی‌شه.
        sub_id=(None if (source.get("combo_group_id") and source.get("combo_group_id") == source.get("sub_id")) else source.get("sub_id")),
        protocol=source.get("protocol", DEFAULT_PROTOCOL),
        fingerprint=(_preset["fingerprint"] if _preset else source.get("fingerprint", DEFAULT_FINGERPRINT)),
        alpn=(_preset["alpn"] if (_preset and _preset.get("alpn")) else source.get("alpn", "")),
        port=int(source.get("port", DEFAULT_PORT) or DEFAULT_PORT),
        ip_limit=safe_int(ip_limit if ip_limit is not None else source.get("ip_limit", 0), minimum=0),
        speed_limit_bytes=safe_int(speed_limit_bytes if speed_limit_bytes is not None else source.get("speed_limit_bytes", 0), minimum=0),
        connection_limit=safe_int(connection_limit if connection_limit is not None else source.get("connection_limit", 0), minimum=0),
        fragment=(_preset["fragment"] if _preset else source.get("fragment", "off")),
        clean_ips=((_preset.get("clean_ips") or source.get("clean_ips", [])) if _preset else source.get("clean_ips", [])),
        alarm_enabled=bool(source.get("alarm_enabled", False)),
        category_id=str(source.get("category_id") or "0"),
        config_count=1,
        manual_fields={k: source.get(k) for k in ("base_protocol","network","security","address","path","host_header","sni","flow","grpc_service_name","grpc_mode","xhttp_mode","header_type","allow_insecure","reality_public_key","reality_short_id","reality_spider_x","ss_method","ss_password")},
        # None = مثل اینباند والد؛ "" = مستقیم؛ غیرخالی = همون پراکسی
        outbound_proxy_id=(str(source.get("outbound_proxy_id") or "") if outbound_proxy_id is None else str(outbound_proxy_id).strip()),
    )
    async with LINKS_LOCK:
        LINKS[child_uid]["parent_inbound_id"] = uid
        LINKS[child_uid]["created_by"] = created_by or "owner"
        LINKS[child_uid]["is_default"] = False
        if _preset:
            LINKS[child_uid]["operator"] = operator
        LINKS[child_uid]["protocol_label"] = protocol_display_label(LINKS[child_uid])
    await save_state()
    log_activity("client", f"کلاینت جدید برای «{source.get('label','اینباند')}» ساخته شد", "ok")
    return child_uid, LINKS[child_uid]


async def remove_inbound_client(uid: str, client_id: str):
    async with LINKS_LOCK:
        child = LINKS.get(client_id)
        if not child or child.get("parent_inbound_id") != uid:
            raise ValueError("کلاینت پیدا نشد")
        LINKS.pop(client_id, None)
    await save_state()
    log_activity("client", f"کلاینت {client_id[:8]}… حذف شد", "warn")


@app.get("/api/links/{uid}/clients")
async def list_inbound_clients(uid: str, request: Request, _=Depends(require_auth)):
    async with LINKS_LOCK:
        parent = LINKS.get(uid)
        if not parent:
            raise HTTPException(status_code=404, detail="اینباند پیدا نشد")
        _aid = await actor_id_of(request)
        children = [(cid, dict(link)) for cid, link in LINKS.items() if link.get("parent_inbound_id") == uid and client_visible(link, _aid)]
    host = get_host(request)
    return {"ok": True, "inbound": get_link_info(parent, uid, host), "clients": [get_link_info(x, cid, host) for cid, x in children]}

def find_combo_sibling(uid: str) -> str | None:
    """اگه uid یکی از دو عضو یک جفت WS+XHTTP باشه (همون combo_tag، همون گروه، پروتکل متفاوت)،
    UUID شریکش رو برمی‌گردونه؛ وگرنه None (یعنی اینباند تکی و معمولیه)."""
    parent = LINKS.get(uid)
    if not parent or not parent.get("combo_group_id"):
        return None
    group_id, tag, protocol = parent.get("combo_group_id"), parent.get("combo_tag", ""), parent.get("protocol")
    for other_uid, other in LINKS.items():
        if other_uid != uid and other.get("combo_group_id") == group_id and other.get("combo_tag", "") == tag and other.get("protocol") != protocol:
            return other_uid
    return None


@app.post("/api/links/{uid}/clients")
async def create_inbound_client(uid: str, request: Request, _=Depends(require_auth)):
    try:
        body = await request.json()
    except Exception:
        body = {}
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="اینباند پیدا نشد")
        sibling_uid = find_combo_sibling(uid)
    if not link_in_scope(await actor_scope(request), uid):
        raise HTTPException(status_code=403, detail="به این اینباند دسترسی ندارید")
    kwargs = dict(
        created_by=await actor_id_of(request),
        label=body.get("label"),
        limit_bytes=body.get("limit_bytes"),
        expires_days=safe_int(body.get("expires_days", 0), minimum=0),
        ip_limit=body.get("ip_limit"),
        speed_limit_bytes=body.get("speed_limit_bytes"),
        connection_limit=body.get("connection_limit"),
        note=body.get("note"),
        outbound_proxy_id=(clean_outbound_proxy_id(body.get("outbound_proxy_id")) if "outbound_proxy_id" in body else None),
    )
    host = get_host(request)
    _op_key = str(body.get("operator") or "").strip().lower()
    _op_mgr = getattr(app.state, "operators", None)
    if _op_key and _op_mgr and (_op_key == "all" or _op_key in _op_mgr.data) and not sibling_uid:
        _targets = _op_mgr.keys_for(_op_key)
        if not _targets:
            raise HTTPException(status_code=400, detail="هیچ اپراتور فعالی وجود ندارد")
        try:
            if _op_key == "all":
                base_label = str(body.get("label") or "Client").strip()[:60] or "Client"
                sub_id, sub = await create_sub_group(name=base_label[:60], desc="کلاینت همه‌ی اپراتورها")
                made = []
                for _k in _targets:
                    cu, _c = await add_client_to_inbound(uid, operator=_k, **kwargs)
                    await set_link_sub(cu, sub_id)
                    made.append(cu)
                await save_state()
                items = [get_link_info(LINKS[c], c, host) for c in made]
                return {"ok": True, "combo": True, "operator": "all", "clients": items, "client": items[0],
                        "sub_url": f"{get_web_base(host)}/sub-group/{sub['uuid_key']}",
                        "public_url": f"{get_web_base(host)}/p/{sub['uuid_key']}"}
            cu, _c = await add_client_to_inbound(uid, operator=_op_key, **kwargs)
            return {"ok": True, "client": get_link_info(LINKS[cu], cu, host)}
        except ValueError as exc:
            raise HTTPException(status_code=409 if "ظرفیت" in str(exc) else 404, detail=str(exc))
    try:
        if sibling_uid:
            # اینباند مقصد بخشی از یک جفت WS+XHTTP است: به‌جای یک کلاینت تکی، برای
            # هر دو عضو کلاینت می‌سازیم و هر دو را در یک ساب‌گروه مخصوص همین کاربر
            # می‌گذاریم — یعنی مشتری یک لینک اشتراک می‌گیرد که هم WS و هم XHTTP دارد.
            base_label = str(body.get("label") or "Client").strip()[:80] or "Client"
            sub_id, sub = await create_sub_group(name=f"{base_label}"[:60], desc="کلاینت WS + XHTTP")
            created_ids = []
            for member_uid in (uid, sibling_uid):
                child_uid, _child = await add_client_to_inbound(member_uid, **kwargs)
                await set_link_sub(child_uid, sub_id)
                created_ids.append(child_uid)
            await save_state()
            items = [get_link_info(LINKS[c], c, host) for c in created_ids]
            return {
                "ok": True, "combo": True,
                "clients": items, "client": items[0],
                "sub_url": f"{get_web_base(host)}/sub-group/{sub['uuid_key']}",
                "public_url": f"{get_web_base(host)}/p/{sub['uuid_key']}",
            }
        child_uid, _child = await add_client_to_inbound(uid, **kwargs)
    except ValueError as exc:
        code = 409 if "ظرفیت" in str(exc) else 404
        raise HTTPException(status_code=code, detail=str(exc))
    return {"ok": True, "client": get_link_info(LINKS[child_uid], child_uid, host)}

@app.delete("/api/links/{uid}/clients/{client_id}")
async def delete_inbound_client(uid: str, client_id: str, request: Request, _=Depends(require_auth)):
    _aid = await actor_id_of(request)
    _c = LINKS.get(client_id)
    if _c is not None and not client_visible(_c, _aid):
        raise HTTPException(status_code=404, detail="کلاینت پیدا نشد")
    try:
        await remove_inbound_client(uid, client_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"ok": True, "deleted": client_id}

# ============================================================
# LIST LINKS
# ============================================================

@app.get("/api/protocols")
async def api_protocols(request: Request, _=Depends(require_auth)):
    return {
        "protocols": [
            {
                "id": p,
                "label": PROTOCOL_LABELS.get(p, p),
                "functional": p in LIVE_PROTOCOLS,
                "live_status": "live" if p in LIVE_PROTOCOLS else "link-only",
            }
            for p in PROTOCOLS
        ],
        "default": DEFAULT_PROTOCOL,
        "manual": {
            "base_protocols": [
                {"id": p, "label": MANUAL_BASE_PROTOCOL_LABELS.get(p, p)}
                for p in MANUAL_BASE_PROTOCOLS
            ],
            "networks": [
                {"id": n, "label": NETWORK_LABELS.get(n, n)}
                for n in NETWORKS
            ],
            "securities": [
                {"id": s, "label": SECURITY_LABELS.get(s, s)}
                for s in SECURITIES
            ],
            "xhttp_modes": list(XHTTP_MODES),
            "shadowsocks_methods": list(SHADOWSOCKS_METHODS),
            "fingerprints": list(FINGERPRINTS),
            "live_combos": [["vless", n, s] for n, s in MANUAL_LIVE_COMBOS],
        },
    }


@app.get("/api/reality-keypair")
async def api_reality_keypair(_=Depends(require_auth)):
    """تولید یک جفت‌کلید X25519 و Short ID تصادفی برای Reality — دقیقاً با همان
    فرمتی که Xray-core و کلاینت‌ها (v2rayN، NekoBox، Streisand، ...) انتظار دارند
    (base64url بدون padding، ۳۲ بایت خام)."""
    try:
        from cryptography.hazmat.primitives.asymmetric import x25519
        from cryptography.hazmat.primitives import serialization

        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()

        priv_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )

        b64 = lambda b: base64.urlsafe_b64encode(b).decode().rstrip("=")

        return {
            "ok": True,
            "private_key": b64(priv_bytes),
            "public_key": b64(pub_bytes),
            "short_id": secrets.token_hex(4),
        }
    except Exception as exc:
        logger.exception("Reality keypair generation failed: %s", exc)
        raise HTTPException(status_code=500, detail="تولید کلید Reality ممکن نشد. کتابخانه‌ی cryptography نصب است؟")


@app.get("/api/links")
async def list_links(
    request: Request,
    _=Depends(require_auth),
):

    host = get_host(request)
    _scope = await actor_scope(request)

    async with LINKS_LOCK:
        snapshot = dict(LINKS)
    if _scope is not None:
        snapshot = {u: l for u, l in snapshot.items() if u in _scope or l.get("parent_inbound_id") in _scope}
    _aid = await actor_id_of(request)
    snapshot = {u: l for u, l in snapshot.items() if client_visible(l, _aid)}

    result = []

    for uid, link in snapshot.items():

        info = get_link_info(
            link,
            uid,
            host,
        )

        info["client_count"] = sum(1 for x in snapshot.values() if x.get("parent_inbound_id") == uid)
        result.append(
            {
                **info,

                "created_at":
                    link.get(
                        "created_at"
                    ),

                "expired":
                    is_link_expired(
                        link
                    ),

                "sub_url":
                    f"{get_web_base(host)}/sub/{uid}",

                "info_url":
                    f"{get_web_base(host)}/info/{uid}",

                "connected_ips":
                    len(
                        unique_ips_for_uuid(
                            uid
                        )
                    ),
            }
        )

    result.sort(
        key=lambda item:
            item.get(
                "created_at",
                "",
            ),
        reverse=True,
    )

    return {
        "links": result
    }


# ============================================================
# LINK INFO API
# ============================================================

@app.get("/api/links/{uid}/info")
async def link_info_api(
    uid: str,
    request: Request,
    _=Depends(require_auth),
):

    async with LINKS_LOCK:

        link = LINKS.get(uid)

        if not link:
            raise HTTPException(
                status_code=404,
                detail="link not found",
            )

        snapshot = dict(link)

    host = get_host(request)

    return {
        "ok": True,
        **get_link_info(
            snapshot,
            uid,
            host,
        ),
    }


# ============================================================
# UPDATE LINK
# ============================================================

@app.patch("/api/links/{uid}")
async def update_link(
    uid: str,
    request: Request,
    _=Depends(require_auth),
):

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="اطلاعات نامعتبر است",
        )

    if not isinstance(body, dict):
        raise HTTPException(
            status_code=400,
            detail="اطلاعات نامعتبر است",
        )

    async with LINKS_LOCK:

        if uid not in LINKS:
            raise HTTPException(
                status_code=404,
                detail="link not found",
            )

        link = LINKS[uid]

        old_sub = link.get(
            "sub_id"
        )

        label = link.get(
            "label",
            uid,
        )

        if "active" in body:
            link["active"] = bool(
                body["active"]
            )

        if "label" in body:

            value = str(
                body["label"]
            ).strip()

            if value:
                link["label"] = value[:60]

        if "note" in body:

            link["note"] = str(
                body.get(
                    "note",
                    "",
                )
            )[:500]

        if "reset_usage" in body:

            if body.get(
                "reset_usage"
            ):
                link[
                    "used_bytes"
                ] = 0

        if "limit_value" in body:

            value = safe_float(
                body.get(
                    "limit_value",
                    0,
                )
            )

            unit = str(
                body.get(
                    "limit_unit",
                    "GB",
                )
                or "GB"
            )

            link[
                "limit_bytes"
            ] = (
                0
                if value <= 0
                else parse_size_to_bytes(
                    value,
                    unit,
                )
            )

        if "expires_at" in body and str(body.get("expires_at") or "").strip():
            try:
                dt = datetime.fromisoformat(str(body.get("expires_at")).replace("Z", "+00:00"))
                link["expires_at"] = dt.replace(tzinfo=None).isoformat()
            except Exception:
                raise HTTPException(status_code=400, detail="زمان انقضا معتبر نیست")
        elif "expires_at" in body and not str(body.get("expires_at") or "").strip() and "expires_days" not in body:
            link["expires_at"] = None

        if "expires_days" in body:

            days = safe_int(
                body.get(
                    "expires_days",
                    0,
                ),
                minimum=0,
            )

            link[
                "expires_at"
            ] = (
                (
                    datetime.now()
                    + timedelta(
                        days=days
                    )
                ).isoformat()
                if days > 0
                else None
            )

        if "fingerprint" in body:

            fingerprint = str(
                body.get(
                    "fingerprint",
                    DEFAULT_FINGERPRINT,
                )
            ).strip().lower()

            link[
                "fingerprint"
            ] = (
                fingerprint
                if fingerprint in FINGERPRINTS
                else DEFAULT_FINGERPRINT
            )

        if "alpn" in body:

            link["alpn"] = str(
                body.get(
                    "alpn",
                    "",
                )
            )[:100]

        if "port" in body:

            p = safe_int(
                body.get(
                    "port",
                    DEFAULT_PORT,
                ),
                default=DEFAULT_PORT,
                minimum=MIN_PORT,
                maximum=MAX_PORT,
            )

            link["port"] = p

        if "ip_limit" in body:

            link["ip_limit"] = safe_int(
                body.get(
                    "ip_limit",
                    0,
                ),
                minimum=0,
            )

        if "connection_limit" in body:

            link[
                "connection_limit"
            ] = safe_int(
                body.get(
                    "connection_limit",
                    0,
                ),
                minimum=0,
            )

        if "client_limit" in body:
            link["client_limit"] = safe_int(body.get("client_limit", 0), minimum=0, maximum=1000)

        if "config_count" in body:
            link["config_count"] = safe_int(body.get("config_count", 1), minimum=1, maximum=40)

        if "speed_limit_value" in body:

            speed_value = safe_float(
                body.get(
                    "speed_limit_value",
                    0,
                )
            )

            speed_unit = str(
                body.get(
                    "speed_limit_unit",
                    "MBIT",
                )
                or "MBIT"
            )

            link[
                "speed_limit_bytes"
            ] = (
                0
                if speed_value <= 0
                else parse_speed_to_bytes(
                    speed_value,
                    speed_unit,
                )
            )

        if "protocol" in body:

            protocol = str(
                body.get(
                    "protocol",
                    DEFAULT_PROTOCOL,
                )
            ).strip().lower()

            link["protocol"] = (
                protocol
                if protocol == "manual" or protocol in PROTOCOLS
                else DEFAULT_PROTOCOL
            )
            if link["protocol"] != "manual":
                link["protocol_label"] = protocol_display_label(link)

        if link.get("protocol") == "manual" and isinstance(body.get("manual"), dict):
            manual_fields = body["manual"]
            link["base_protocol"] = normalize_base_protocol(manual_fields.get("base_protocol", link.get("base_protocol")))
            link["network"] = normalize_network(manual_fields.get("network", link.get("network")))
            link["security"] = normalize_security(manual_fields.get("security", link.get("security")))
            if "address" in manual_fields:
                link["address"] = str(manual_fields.get("address") or "").strip()[:255]
            if "path" in manual_fields:
                link["path"] = str(manual_fields.get("path") or "").strip()[:255]
            if "host_header" in manual_fields:
                link["host_header"] = str(manual_fields.get("host_header") or "").strip()[:255]
            if "sni" in manual_fields:
                link["sni"] = str(manual_fields.get("sni") or "").strip()[:255]
            if "flow" in manual_fields:
                link["flow"] = str(manual_fields.get("flow") or "").strip()[:64]
            if "grpc_service_name" in manual_fields:
                link["grpc_service_name"] = str(manual_fields.get("grpc_service_name") or "").strip()[:128]
            if "grpc_mode" in manual_fields:
                link["grpc_mode"] = str(manual_fields.get("grpc_mode") or "gun").strip()[:32] or "gun"
            if "xhttp_mode" in manual_fields:
                link["xhttp_mode"] = normalize_xhttp_mode(manual_fields.get("xhttp_mode"))
            if "header_type" in manual_fields:
                link["header_type"] = str(manual_fields.get("header_type") or "").strip()[:32]
            if "allow_insecure" in manual_fields:
                link["allow_insecure"] = bool(manual_fields.get("allow_insecure"))
            if "reality_public_key" in manual_fields:
                link["reality_public_key"] = str(manual_fields.get("reality_public_key") or "").strip()[:128]
            if "reality_short_id" in manual_fields:
                link["reality_short_id"] = str(manual_fields.get("reality_short_id") or "").strip()[:32]
            if "reality_spider_x" in manual_fields:
                link["reality_spider_x"] = str(manual_fields.get("reality_spider_x") or "/").strip()[:128] or "/"
            if "ss_method" in manual_fields:
                link["ss_method"] = str(manual_fields.get("ss_method") or "chacha20-ietf-poly1305").strip()[:80]
            if "ss_password" in manual_fields:
                link["ss_password"] = str(manual_fields.get("ss_password") or "").strip()[:255]
            link["protocol_label"] = protocol_display_label(link)

        if "outbound_proxy_id" in body:
            link["outbound_proxy_id"] = clean_outbound_proxy_id(body.get("outbound_proxy_id"))
            # کلاینت‌های این اینباند باید همان خروجی را داشته باشند (ریلی از UUID کلاینت می‌خواند)
            for _child in LINKS.values():
                if _child.get("parent_inbound_id") == uid:
                    _child["outbound_proxy_id"] = link["outbound_proxy_id"]

        if "fragment" in body:

            fragment = str(
                body.get(
                    "fragment",
                    "off",
                )
                or "off"
            ).strip().lower()

            if fragment not in {
                "off",
                "safe",
                "balanced",
                "aggressive",
            }:
                fragment = "off"

            link["fragment"] = fragment

        if "sub_id" in body:

            link[
                "sub_id"
            ] = (
                body.get(
                    "sub_id"
                )
                or None
            )

        new_sub = body.get(
            "sub_id",
            "UNCHANGED",
        )

    if new_sub != "UNCHANGED":

        async with SUBS_LOCK:

            if (
                old_sub
                and old_sub in SUBS
            ):

                ids = SUBS[
                    old_sub
                ].get(
                    "link_ids",
                    [],
                )

                if uid in ids:
                    ids.remove(uid)

            if (
                new_sub
                and new_sub in SUBS
            ):

                ids = SUBS[
                    new_sub
                ].setdefault(
                    "link_ids",
                    [],
                )

                if uid not in ids:
                    ids.append(uid)

    await save_state()

    log_activity(
        "link",
        (
            f"کانفیگ "
            f"«{label}» "
            f"ویرایش شد"
        ),
        "info",
    )

    return {
        "ok": True
    }


# ============================================================
# RESET USAGE
# ============================================================

@app.post(
    "/api/links/{uid}/reset-usage"
)
async def reset_link_usage(
    uid: str,
    _=Depends(require_auth),
):

    async with LINKS_LOCK:

        link = LINKS.get(uid)

        if not link:
            raise HTTPException(
                status_code=404,
                detail="link not found",
            )

        link["used_bytes"] = 0

        label = link.get(
            "label",
            uid,
        )

    await save_state()

    log_activity(
        "link",
        (
            f"مصرف کانفیگ "
            f"«{label}» ریست شد"
        ),
        "info",
    )

    return {
        "ok": True,
        "uuid": uid,
        "used_bytes": 0,
    }


# ============================================================
# REGENERATE / SWAP LINK (تعویض لینک — UUID جدید، همان تنظیمات)
# ============================================================
# لینک قدیمی بلافاصله از کار می‌افتد (چون UUID عوض شده) و یک UUID جدید با
# همان تنظیمات (حجم، انقضا، دسته، پروتکل، محدودیت‌ها و ...) جایگزینش می‌شود.
# برای کلاینت‌های فرزند یک اینباند هم پشتیبانی می‌شود.

@app.post("/api/links/{uid}/regenerate")
async def regenerate_link(
    uid: str,
    request: Request,
    _=Depends(require_auth),
):
    async with LINKS_LOCK:
        old_link = LINKS.get(uid)
        if not old_link:
            raise HTTPException(status_code=404, detail="link not found")

        new_uid = generate_uuid()
        while new_uid in LINKS:
            new_uid = generate_uuid()

        new_link = dict(old_link)
        # مصرف قبلی حفظ می‌شود (این فقط تعویض کلید/لینک است، نه ریست حجم)
        LINKS[new_uid] = new_link
        del LINKS[uid]
        scope_replace_uid(uid, new_uid)

        parent_id = old_link.get("parent_inbound_id")
        sub_id = old_link.get("sub_id")
        label = old_link.get("label", uid)

        # اگر این اینباند بود، فرزندانش را به UUID جدید مادر وصل کن
        updated_children = 0
        for child in LINKS.values():
            if child.get("parent_inbound_id") == uid:
                child["parent_inbound_id"] = new_uid
                updated_children += 1

    if sub_id:
        async with SUBS_LOCK:
            sub = SUBS.get(sub_id)
            if sub:
                ids = sub.get("link_ids", [])
                if uid in ids:
                    ids[ids.index(uid)] = new_uid

    await save_state()

    log_activity(
        "link",
        f"لینک «{label}» تعویض شد (UUID جدید صادر شد)",
        "warn",
    )

    host = get_host(request)
    async with LINKS_LOCK:
        refreshed = LINKS.get(new_uid)

    return {
        **(get_link_info(refreshed, new_uid, host) if refreshed else {}),
        "ok": True,
        "old_uuid": uid,
        "uuid": new_uid,
        "updated_children": updated_children,
    }


# ============================================================
# LINK ACTION
# ============================================================

@app.post(
    "/api/links/{uid}/action"
)
async def link_action(
    uid: str,
    request: Request,
    _=Depends(require_auth),
):

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="JSON نامعتبر است",
        )

    action = str(
        body.get(
            "action",
            "",
        )
    ).strip().lower()

    if action == "reset":

        await reset_link_usage(
            uid,
            _
        )

        return {
            "ok": True,
            "action": "reset",
        }

    if action == "enable":

        result = await set_link_active(
            uid,
            True,
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="link not found",
            )

        return {
            "ok": True,
            "action": "enable",
        }

    if action == "disable":

        result = await set_link_active(
            uid,
            False,
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="link not found",
            )

        return {
            "ok": True,
            "action": "disable",
        }

    raise HTTPException(
        status_code=400,
        detail="unknown action",
    )


# ============================================================
# DELETE LINK
# ============================================================

@app.delete("/api/links/{uid}")
async def delete_link(
    uid: str,
    _=Depends(require_auth),
):

    label = await remove_link(uid)

    if label is None:
        raise HTTPException(
            status_code=404,
            detail="link not found",
        )

    return {
        "ok": True,
        "deleted": uid,
    }




def subscription_metadata_headers(used_bytes: int, limit_bytes: int, expires_at, host: str, info_url: str, title: str):
    """Standard subscription headers understood by v2rayNG/v2rayN/Hiddify and similar clients."""
    used_bytes = max(0, int(used_bytes or 0))
    limit_bytes = max(0, int(limit_bytes or 0))

    expire_unix = 0
    if expires_at:
        try:
            dt = datetime.fromisoformat(str(expires_at))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=IRAN_TZ) if IRAN_TZ else dt
            expire_unix = max(0, int(dt.timestamp()))
        except Exception:
            expire_unix = 0

    userinfo = f"upload=0; download={used_bytes}; total={limit_bytes}; expire={expire_unix}"

    return {
        "profile-title": quote(title, safe=""),
        "profile-web-page-url": info_url,
        "support-url": get_support_url(),
        "profile-update-interval": "12",
        "subscription-userinfo": userinfo,
        "content-disposition": 'inline; filename="subscription.txt"',
    }

# ============================================================
# ONE SUBSCRIPTION LINK FOR BOTH APPS AND BROWSERS
# ============================================================
# VPN clients (v2rayNG, v2rayN, Hiddify, Clash, sing-box, ...) send a
# non-browser User-Agent and never ask for text/html, so they keep getting
# the raw base64 config feed below exactly as before. A normal visit from a
# desktop/mobile browser is redirected to the rich HTML portal instead — the
# customer only ever needs to hand out a single /sub/{uuid} link, whether
# it's pasted into an app or opened by hand to check usage.
_SUB_CLIENT_UA_HINTS = (
    "v2ray", "v2rayng", "v2rayn", "hiddify", "clash", "sing-box", "sing_box",
    "shadowrocket", "streisand", "nekobox", "nekoray", "karing", "matsuri",
    "kitsunebi", "quantumult", "surge", "loon", "stash", "husi", "foxray",
    "v2box", "happ", "flclash", "mihomo", "openclash", "passwall",
    "npvtunnel", "netch", "qv2ray", "leaf", "outline", "throne", "exclave",
    "okhttp", "curl", "wget", "python", "go-http", "libcurl",
)
_SUB_BROWSER_UA_HINTS = ("mozilla", "chrome", "safari", "firefox", "edg/", "opr/", "webkit", "gecko")

_SUB_APP_ONLY_HEADERS = ("x-hwid", "x-device-os", "x-ver-os", "x-device-model", "hwid", "x-app-version")
_SUB_NO_STORE = {
    "Cache-Control": "no-store, max-age=0",
    "Vary": "User-Agent, Accept, Sec-Fetch-Mode, Sec-Fetch-Dest",
}

def _subscription_wants_browser_view(request: Request) -> bool:
    """True فقط وقتی یک انسان واقعاً لینک را در مرورگر باز کرده باشد.

    ‏اپ‌های VPN هرگز هدرهای Sec-Fetch-* نمی‌فرستند، ولی هر مرورگر مدرن روی باز کردن
    یک صفحه (navigate) آن‌ها را می‌فرستد؛ پس این تشخیص برخلاف حدس‌زدن با User-Agent
    اپ را هیچ‌وقت به صفحه‌ی HTML نمی‌برد. برای حالت‌های خاص:
      ?raw=1  ->  همیشه کانفیگ خام (دکمه‌ی «دریافت کانفیگ»)
      ?web=1  ->  همیشه صفحه‌ی گرافیکی
    """
    qp = request.query_params
    if str(qp.get("raw", "")).lower() in ("1", "true", "yes"):
        return False
    if str(qp.get("web", "")).lower() in ("1", "true", "yes"):
        return True
    h = request.headers
    ua = (h.get("user-agent") or "").lower()
    if not ua or any(x in ua for x in _SUB_CLIENT_UA_HINTS):
        return False
    if any(h.get(k) for k in _SUB_APP_ONLY_HEADERS):
        return False
    accept = (h.get("accept") or "").lower()
    if "text/html" not in accept:
        return False
    mode = (h.get("sec-fetch-mode") or "").lower()
    dest = (h.get("sec-fetch-dest") or "").lower()
    if mode or dest:
        return mode == "navigate" and dest in ("document", "")
    # مرورگرهای خیلی قدیمی بدون Sec-Fetch: فقط اگر کاملاً شبیه مرورگر باشند
    return ua.startswith("mozilla/") and "application/xhtml+xml" in accept

# ============================================================
# SINGLE SUB
# ============================================================

@app.get("/sub/{uuid}")
async def subscription_single(
    uuid: str,
    request: Request,
):

    async with LINKS_LOCK:
        link = LINKS.get(uuid)

    if not is_link_allowed(link):
        raise HTTPException(
            status_code=404,
            detail="not found or inactive",
        )

    if _subscription_wants_browser_view(request):
        return RedirectResponse(url=f"/subscription/{uuid}", status_code=307, headers=_SUB_NO_STORE)

    host = get_host(request)
    clean_ips = link.get("clean_ips") or []
    used = int(link.get("used_bytes", 0) or 0)
    limit = int(link.get("limit_bytes", 0) or 0)
    expires_at = link.get("expires_at")
    stats_remark = build_info_server_remark(used, limit, expires_at)
    lines = []
    if bool(CONFIG.get("sub_info_line_enabled", True)):
        # ردیف اطلاعات (حجم/زمان باقی‌مانده): یک کانفیگ واقعی و قابل‌اتصال با آدرس واقعی پنل
        lines.append(vless_link_for_link({**link, "label": stats_remark}, uuid, (clean_ips[0] if clean_ips else host)))
    used_names = set()
    cfg_count = max(1, min(40, int(link.get("config_count") or 1)))
    if clean_ips:
        hosts = list(clean_ips)
        while len(hosts) < cfg_count:
            hosts.extend(clean_ips)
        hosts = hosts[:cfg_count]
        for cip in hosts:
            name = random_config_name(used_names)
            used_names.add(name)
            lines.append(vless_link_for_link({**link, "label": name}, uuid, cip))
    else:
        for i in range(cfg_count):
            name = random_config_name(used_names)
            used_names.add(name)
            lines.append(vless_link_for_link({**link, "label": name}, uuid, host))
    content = base64.b64encode("\n".join(lines).encode()).decode()
    profile_title = stats_remark
    headers = subscription_metadata_headers(
        used,
        limit,
        link.get("expires_at"),
        host,
        f"{get_web_base(host)}/info/{uuid}",
        profile_title,
    )
    headers.update(_SUB_NO_STORE)

    return Response(
        content=content,
        media_type="text/plain; charset=utf-8",
        headers=headers,
    )

# ============================================================
# LIVE SUBSCRIPTION TELEMETRY
# ============================================================

@app.get("/api/subscription/{uuid}")
async def subscription_telemetry(uuid: str):
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
        if not link or not is_link_allowed(link):
            raise HTTPException(status_code=404, detail="subscription not found or inactive")
        used = int(link.get("used_bytes", 0) or 0)
        limit = int(link.get("limit_bytes", 0) or 0)
        history = list(link.get("usage_history") or [])[-144:]
        if not history:
            history = [{"ts": now_ir().replace(second=0, microsecond=0).isoformat(), "used": used, "limit": limit}]
        active_ips = sorted({str(x.get("ip") or "").strip() for x in connections.values() if x.get("uuid") == uuid and str(x.get("ip") or "").strip()})
        active_sessions = sum(1 for x in connections.values() if x.get("uuid") == uuid)
        return {
            "ok": True, "uuid": uuid, "active": bool(link.get("active", True)),
            "traffic_used": used, "traffic_limit": limit,
            "traffic_remaining": max(0, limit - used) if limit else None,
            "traffic_percent": min(100, round((used / limit) * 100, 1)) if limit else 0,
            "active_connections": len(active_ips), "active_sessions": active_sessions,
            "active_ips": active_ips,
            "connection_limit": int(link.get("connection_limit", 0) or 0),
            "ip_limit": int(link.get("ip_limit", 0) or 0),
            "updated_at": now_ir().isoformat(), "usage_history": history,
        }

# ============================================================
# SMART SUBSCRIPTION PORTAL
# ============================================================

@app.get("/subscription/{uuid}", response_class=HTMLResponse)
async def subscription_portal(uuid: str, request: Request):
    '''Premium customer subscription portal. All figures come from live backend state.'''
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
        if link:
            link = dict(link)
    if not is_link_allowed(link):
        raise HTTPException(status_code=404, detail="subscription not found or inactive")

    host = get_host(request)
    raw_url = f"{get_web_base(host)}/sub/{uuid}"
    info_url = f"{get_web_base(host)}/info/{uuid}"
    label = str(link.get("label") or "VodiWalker Subscription")
    protocol = protocol_display_label(link)
    used = int(link.get("used_bytes", 0) or 0)
    limit = int(link.get("limit_bytes", 0) or 0)
    pct = min(100, round((used / limit) * 100, 1)) if limit else 0
    remaining = max(0, limit - used) if limit else None
    expires = str(link.get("expires_at") or "نامحدود")
    conn_limit = int(link.get("connection_limit", 0) or 0)
    ip_limit = int(link.get("ip_limit", 0) or 0)
    active = bool(link.get("active", True))
    active_ips = {str(x.get("ip") or "").strip() for x in connections.values()
                  if x.get("uuid") == uuid and str(x.get("ip") or "").strip()}
    active_people = len(active_ips)
    active_sessions = sum(1 for x in connections.values() if x.get("uuid") == uuid)
    qr = quote(raw_url, safe="")
    initial = (label.strip()[:1] or "V").upper()

    from ui_portal import PORTAL_V18 as _PORTAL_V18
    html = _PORTAL_V18
    replacements={
      '__LABEL__':escape_html(label),'__PROTOCOL__':escape_html(protocol),'__EXPIRES__':escape_html(expires[:19]),
      '__STATUS__':'فعال' if active else 'غیرفعال','__PCT__':str(pct),'__USED__':escape_html(fmt_bytes(used)),
      '__REMAINING__':escape_html(fmt_bytes(remaining) if remaining is not None else 'نامحدود'),
      '__LIMIT__':escape_html(fmt_bytes(limit) if limit else 'نامحدود'),'__ACTIVE_CONN__':str(active_people),
      '__ACTIVE_SESSIONS__':str(active_sessions),'__CONN_LIMIT__':('حداکثر '+str(conn_limit)+' اتصال') if conn_limit else 'بدون محدودیت اتصال',
      '__IP_LIMIT__':('حداکثر '+str(ip_limit)+' IP') if ip_limit else 'بدون محدودیت','__RAW__':escape_html(raw_url),
      '__RAW_URL__':escape_html(raw_url),'__INFO_URL__':escape_html(info_url),'__QR__':qr,'__UUID__':escape_html(uuid),
      '__RAW_JS__':repr(raw_url),'__INITIAL__':escape_html(initial),
      '__SUPPORT__':escape_html(get_support_username()),'__SUPPORT_URL__':escape_html(get_support_url()),
    }
    for k,v in replacements.items(): html=html.replace(k,v)
    return HTMLResponse(html)

@app.get("/sub-all")
async def subscription_all(
    request: Request,
    _=Depends(require_auth),
):

    host = get_host(request)

    async with LINKS_LOCK:

        lines = [
            vless_link_for_link(
                link,
                uid,
                host,
            )

            for uid, link
            in LINKS.items()

            if is_link_allowed(link)
        ]

    content = (
        base64
        .b64encode(
            "\n".join(
                lines
            ).encode()
        )
        .decode()
    )

    return Response(
        content=content,
        media_type="text/plain",
    )


# ============================================================
# INFO PAGE
# ============================================================

@app.get(
    "/info/{uid}",
    response_class=HTMLResponse,
)
async def info_page(uid: str, request: Request):
    """Premium client portal. Keeps the stable /info/{uid} route but replaces the legacy card layout."""
    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if not link:
            return HTMLResponse("<html lang=\"fa\" dir=\"rtl\"><body style=\"margin:0;background:#070a10;color:#fff;font-family:sans-serif;padding:40px\"><h2>سرویس پیدا نشد</h2></body></html>", status_code=404)
        snapshot = dict(link)

    host = get_host(request)
    vless_url = vless_link_for_link(snapshot, uid, host)
    sub_url = f"{get_web_base(host)}/sub/{uid}"
    label = str(snapshot.get("label") or "VodiWalker")
    protocol = protocol_display_label(snapshot)
    used = int(snapshot.get("used_bytes", 0) or 0)
    limit = int(snapshot.get("limit_bytes", 0) or 0)
    pct = max(0, min(100, round((used / limit) * 100, 1))) if limit else 0
    remaining = fmt_bytes(max(0, limit-used)) if limit else "نامحدود"
    expires_at = snapshot.get("expires_at")
    expiry_display = str(expires_at) if expires_at else "نامحدود"
    expiry_remaining = "نامحدود"
    if expires_at:
        try:
            expiry_dt = datetime.fromisoformat(str(expires_at))
            now_dt = datetime.now(expiry_dt.tzinfo) if expiry_dt.tzinfo else datetime.now()
            seconds = int((expiry_dt - now_dt).total_seconds())
            if seconds <= 0:
                expiry_remaining = "منقضی شده"
            else:
                days, rem = divmod(seconds, 86400)
                hours, rem = divmod(rem, 3600)
                minutes, _ = divmod(rem, 60)
                expiry_remaining = f"{days} روز" if days else (f"{hours} ساعت" if hours else f"{minutes} دقیقه")
        except Exception:
            expiry_remaining = "نامشخص"
    active = is_link_allowed(snapshot)
    ip_limit = "نامحدود" if not snapshot.get("ip_limit", 0) else str(snapshot.get("ip_limit"))
    conn_limit = "نامحدود" if not snapshot.get("connection_limit", 0) else str(snapshot.get("connection_limit"))
    speed_limit = "نامحدود" if not snapshot.get("speed_limit_bytes", 0) else fmt_bytes(snapshot.get("speed_limit_bytes", 0)) + "/s"
    ips = len(unique_ips_for_uuid(uid))

    esc = lambda x: escape_html(str(x))
    label_e = esc(label); protocol_e = esc(protocol); uid_e = esc(uid)
    sub_e = esc(sub_url); vless_e = esc(vless_url); expiry_e = esc(expiry_display)
    rem_e = esc(remaining); speed_e = esc(speed_limit); ip_e = esc(ip_limit); conn_e = esc(conn_limit)
    used_e = esc(fmt_bytes(used)); limit_e = esc(fmt_bytes(limit) if limit else "نامحدود")
    status_e = "فعال" if active else "غیرفعال"
    raw_js = json.dumps(raw_url if 'raw_url' in locals() else sub_url)
    vless_js = json.dumps(vless_url)
    sub_js = json.dumps(sub_url)

    html = """<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#070a12"><meta name="color-scheme" content="dark"><title>__LABEL__ · VodiWalker</title>
<link rel="stylesheet" href="/assets/ui.css">
<script src="/assets/qr.js"></script>
<style>
:root{--bg:#060812;--panel:#0d1220;--panel2:#111827;--line:rgba(255,255,255,.08);--muted:#8b97ad;--text:#f5f7fb;--accent:#7c5cff;--cyan:#3dd8ff;--good:#2dd4a0;--warn:#f5b942;--danger:#ff6175}
*{box-sizing:border-box}html,body{margin:0;min-height:100%;font-family:Vazirmatn,Inter,sans-serif;background:var(--bg);color:var(--text)}body{overflow-x:hidden;background:radial-gradient(900px 420px at 85% -10%,rgba(124,92,255,.18),transparent 60%),radial-gradient(700px 380px at 5% 25%,rgba(61,216,255,.08),transparent 62%),linear-gradient(180deg,#070a12,#05070d)}
body:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.28;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);background-size:48px 48px;mask-image:linear-gradient(#000,transparent 90%)}
.wrap{width:min(1180px,calc(100% - 28px));margin:auto;padding:22px 0 70px;position:relative;z-index:1}.top{display:flex;justify-content:space-between;align-items:center;gap:14px;margin-bottom:14px}.brand{display:flex;align-items:center;gap:11px}.mark{width:42px;height:42px;border-radius:14px;display:grid;place-items:center;background:linear-gradient(145deg,#1b1730,#111c2c);border:1px solid rgba(124,92,255,.35);box-shadow:0 10px 35px rgba(0,0,0,.3);font-size:18px}.brand b{display:block;font-size:15px}.brand small{display:block;color:#66738a;font-size:9px;letter-spacing:.14em;margin-top:3px}.top-actions{display:flex;gap:8px;flex-wrap:wrap}.btn{border:1px solid var(--line);background:rgba(255,255,255,.035);color:#dce3ef;border-radius:11px;padding:10px 13px;font:800 11px inherit;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:7px}.btn.primary{border-color:rgba(124,92,255,.45);background:linear-gradient(135deg,#7c5cff,#5d72ff);color:#fff;box-shadow:0 12px 32px rgba(92,91,255,.2)}.btn.good{color:#7bf0c6;border-color:rgba(45,212,160,.25);background:rgba(45,212,160,.07)}
.hero{display:grid;grid-template-columns:1fr 250px;gap:18px;padding:28px;border:1px solid var(--line);border-radius:26px;background:linear-gradient(135deg,rgba(17,24,39,.92),rgba(8,12,21,.88));box-shadow:0 30px 100px rgba(0,0,0,.25);overflow:hidden;position:relative}.hero:after{content:"";position:absolute;width:360px;height:360px;left:-140px;top:-220px;border-radius:50%;background:radial-gradient(circle,rgba(124,92,255,.22),transparent 68%)}.hero-main{position:relative;z-index:1}.eyebrow{font-size:9px;letter-spacing:.18em;color:#8290a8;font-weight:900;text-transform:uppercase}.hero h1{font-size:clamp(28px,5vw,50px);line-height:1.08;letter-spacing:-.045em;margin:10px 0 8px}.hero p{margin:0;color:var(--muted);font-size:12px;line-height:2;max-width:700px}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:15px}.chip{border:1px solid var(--line);background:rgba(255,255,255,.035);padding:7px 9px;border-radius:10px;color:#b9c4d5;font-size:9.5px}.chip b{color:#fff}.hero-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:17px}.qr-card{position:relative;z-index:1;border:1px solid var(--line);border-radius:20px;background:rgba(0,0,0,.18);padding:14px;text-align:center}.qr-card img{width:174px;height:174px;background:#fff;border-radius:14px;padding:8px}.qr-card small{display:block;color:#69768c;font-size:9px;margin-top:8px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:12px 0}.kpi{border:1px solid var(--line);border-radius:17px;background:rgba(13,18,32,.82);padding:16px}.kpi .cap{font-size:9px;color:#6e7b90}.kpi .num{font-size:19px;font-weight:900;margin-top:6px}.kpi.good .num{color:#5ee7ba}.kpi.warn .num{color:#ffd067}.kpi.blue .num{color:#72cfff}.kpi.purple .num{color:#b8a7ff}
.grid{display:grid;grid-template-columns:1.35fr .65fr;gap:12px}.panel{border:1px solid var(--line);border-radius:20px;background:rgba(13,18,32,.84);overflow:hidden}.head{padding:16px 18px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:10px}.head b{font-size:12px}.head small{display:block;color:#6e7b90;font-size:9px;margin-top:3px}.body{padding:18px}.usage-top{display:flex;align-items:center;gap:18px}.ring{width:130px;height:130px;border-radius:50%;background:conic-gradient(var(--accent) __PCT__%,#1b2332 0);position:relative;display:grid;place-items:center;flex-shrink:0}.ring:before{content:"";position:absolute;inset:9px;border-radius:50%;background:#0d1220}.ring>div{position:relative;text-align:center}.ring strong{font-size:22px}.ring small{display:block;color:#6d7890;font-size:8px;margin-top:2px}.usage-val{font-size:26px;font-weight:950;letter-spacing:-.04em}.usage-val span{font-size:11px;color:#69768c;font-weight:600}.bar{height:10px;border-radius:99px;background:#1a2230;overflow:hidden;margin:13px 0 9px}.bar i{display:block;height:100%;width:__PCT__%;background:linear-gradient(90deg,var(--accent),var(--cyan));border-radius:inherit}.remaining{display:flex;justify-content:space-between;gap:10px;color:#768297;font-size:9.5px;flex-wrap:wrap}.trend{margin-top:15px;border:1px solid var(--line);background:rgba(0,0,0,.12);border-radius:14px;padding:10px}.trend svg{width:100%;height:80px}.facts{display:grid;grid-template-columns:1fr 1fr;gap:9px}.fact{padding:13px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.018)}.fact small{display:block;color:#6d7890;font-size:8.5px}.fact b{display:block;margin-top:6px;font-size:11px;word-break:break-word}.linkbox{margin-top:12px;padding:13px;border:1px solid var(--line);border-radius:14px;background:#080c15;direction:ltr;text-align:left;color:#b8c7ff;font:10px/1.8 ui-monospace,SFMono-Regular,Consolas,monospace;word-break:break-all}.actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:9px}.wide{grid-column:1/-1}.tech{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}.tech .fact{min-height:76px}.apps{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}.app{padding:13px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.018);text-decoration:none}.app b{font-size:11px}.app small{display:block;color:#6d7890;font-size:8.5px;margin-top:4px}.footer{text-align:center;color:#566174;font-size:9px;padding:22px 0}.toast{position:fixed;bottom:22px;left:50%;transform:translate(-50%,18px);opacity:0;pointer-events:none;background:#111827;border:1px solid var(--line);border-radius:12px;padding:10px 14px;font-size:10px;transition:.2s;z-index:20}.toast.show{opacity:1;transform:translate(-50%,0)}
@media(max-width:900px){.hero{grid-template-columns:1fr}.qr-card{max-width:240px}.grid{grid-template-columns:1fr}.kpis{grid-template-columns:repeat(2,1fr)}.tech{grid-template-columns:repeat(2,1fr)}}@media(max-width:540px){.wrap{width:calc(100% - 18px);padding-top:12px}.hero{padding:20px;border-radius:21px}.kpis{grid-template-columns:1fr 1fr}.usage-top{align-items:flex-start}.ring{width:100px;height:100px}.usage-val{font-size:21px}.facts{grid-template-columns:1fr}.tech,.apps{grid-template-columns:1fr}.actions{grid-template-columns:1fr}.top{align-items:flex-start}.top-actions{justify-content:flex-end}.hero h1{font-size:32px}}
</style></head><body>
<main class="wrap">
<div class="top"><div class="brand"><div class="mark">✦</div><div><b>VodiWalker</b><small>SECURE CLIENT PORTAL</small></div></div><div class="top-actions"><button class="btn" onclick="toggleTheme()">◐ پوسته</button><button class="btn" onclick="openQr()">▦ QR</button><span class="btn good">● __STATUS__</span></div></div>
<section class="hero"><div class="hero-main"><div class="eyebrow">Private Access Workspace</div><h1>__LABEL__</h1><p>مرکز حرفه‌ای مدیریت دسترسی شما؛ وضعیت مصرف، اعتبار سرویس، لینک اشتراک و مشخصات اتصال در یک فضای سریع و تمیز.</p><div class="chips"><span class="chip">پروتکل <b>__PROTOCOL__</b></span><span class="chip">شناسه <b>__UID_SHORT__</b></span><span class="chip">انقضا <b>__EXPIRY__</b></span></div><div class="hero-actions"><button class="btn primary" onclick="copy(SUB)">کپی Subscription</button><button class="btn" onclick="copy(VLESS)">کپی کانفیگ</button><a class="btn" href="__SUB_URL__?raw=1">دریافت Subscription</a></div></div><div class="qr-card"><img id="qrImg" alt="QR"><small>اسکن برای اتصال سریع</small></div></section>
<section class="kpis"><div class="kpi good"><div class="cap">مصرف‌شده</div><div class="num">__USED__</div></div><div class="kpi warn"><div class="cap">باقی‌مانده</div><div class="num">__REMAINING__</div></div><div class="kpi blue"><div class="cap">IP فعال</div><div class="num">__IPS__</div></div><div class="kpi purple"><div class="cap">زمان باقی‌مانده</div><div class="num">__EXPIRY_REMAINING__</div></div></section>
<section class="grid"><div class="panel"><div class="head"><div><b>مصرف و سلامت سرویس</b><small>Real-time service overview</small></div><span style="color:#68e6b7;font-size:9px">● LIVE</span></div><div class="body"><div class="usage-top"><div class="ring"><div><strong>__PCT__%</strong><small>مصرف</small></div></div><div style="flex:1;min-width:0"><div class="usage-val">__USED__ <span>/ __LIMIT__</span></div><div class="bar"><i></i></div><div class="remaining"><span>باقی‌مانده: <b style="color:#dce3ef">__REMAINING__</b></span><span>انقضا: <b style="color:#dce3ef">__EXPIRY__</b></span></div></div></div><div class="trend"><small style="color:#6d7890;font-size:8.5px">روند مصرف</small><svg viewBox="0 0 700 90" preserveAspectRatio="none"><polyline points="0,78 80,68 150,72 230,48 310,55 390,34 470,43 550,24 700,18" fill="none" stroke="#6f83ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><polyline points="0,78 80,68 150,72 230,48 310,55 390,34 470,43 550,24 700,18 700,90 0,90" fill="url(#g)" opacity=".22"/><defs><linearGradient id="g" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#6f83ff"/><stop offset="1" stop-color="#6f83ff" stop-opacity="0"/></linearGradient></defs></svg></div></div></div>
<aside class="panel"><div class="head"><div><b>مشخصات دسترسی</b><small>Limits & connection</small></div></div><div class="body"><div class="facts"><div class="fact"><small>IP Limit</small><b>__IP__</b></div><div class="fact"><small>Connection</small><b>__CONN__</b></div><div class="fact"><small>Speed</small><b>__SPEED__</b></div><div class="fact"><small>Expiry</small><b>__EXPIRY__</b></div></div><div class="linkbox" id="subLink">__SUB_URL__</div><div class="actions"><button class="btn primary" onclick="copy(SUB)">کپی لینک</button><button class="btn" onclick="openQr()">نمایش QR</button></div></div></aside></section>
<section class="panel" style="margin-top:12px"><div class="head"><div><b>اطلاعات فنی</b><small>Connection profile</small></div></div><div class="body"><div class="tech"><div class="fact"><small>Protocol</small><b dir="ltr">__PROTOCOL__</b></div><div class="fact"><small>Fingerprint</small><b dir="ltr">__FINGERPRINT__</b></div><div class="fact"><small>UUID</small><b dir="ltr">__UUID__</b></div><div class="fact"><small>Public subscription</small><b>READY</b></div></div></div></section>
<section class="panel" style="margin-top:12px"><div class="head"><div><b>کلاینت‌های پیشنهادی</b><small>Import the subscription link into a compatible client</small></div></div><div class="body"><div class="apps"><a class="app" href="https://github.com/2dust/v2rayNG/releases/latest" target="_blank" rel="noopener"><b>v2rayNG</b><small>Android</small></a><a class="app" href="https://github.com/2dust/v2rayN/releases/latest" target="_blank" rel="noopener"><b>v2rayN</b><small>Windows / macOS / Linux</small></a><a class="app" href="https://github.com/hiddify/hiddify-app/releases/latest" target="_blank" rel="noopener"><b>Hiddify</b><small>Android / Desktop</small></a></div></div></section>
<div class="footer">VodiWalker Secure Client Portal · اطلاعات اتصال فقط برای صاحب این لینک</div>
</main><div id="toast" class="toast"></div>
<div id="qrModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.86);backdrop-filter:blur(6px);z-index:10;align-items:center;justify-content:center;padding:20px"><div style="width:min(360px,100%);background:#0c1220;border:1px solid var(--line);border-radius:22px;padding:22px;text-align:center"><button class="btn" onclick="closeQr()" style="float:left">بستن</button><h3 style="margin:4px 0 16px">QR اتصال</h3><div style="background:#fff;padding:12px;border-radius:16px;display:inline-block"><div id="qrBox"></div></div><p id="qrText" style="font:9px/1.7 ui-monospace;color:#aebcff;word-break:break-all;direction:ltr;margin-top:14px"></p></div></div>
<script>
const SUB=__SUB_JS__, VLESS=__VLESS_JS__;
function toast(t){const e=document.getElementById('toast');e.textContent=t;e.classList.add('show');setTimeout(()=>e.classList.remove('show'),1600)}
async function copy(v){try{await navigator.clipboard.writeText(v);toast('کپی شد ✓')}catch(e){const x=document.createElement('textarea');x.value=v;document.body.appendChild(x);x.select();document.execCommand('copy');x.remove();toast('کپی شد ✓')}}
function toggleTheme(){document.body.classList.toggle('light');localStorage.setItem('vw_portal_theme',document.body.classList.contains('light')?'light':'dark')}
(function(){if(localStorage.getItem('vw_portal_theme')==='light'){document.body.classList.add('light');document.documentElement.style.setProperty('--bg','#eef1f7');document.documentElement.style.setProperty('--panel','#fff');document.documentElement.style.setProperty('--panel2','#f5f7fb');document.documentElement.style.setProperty('--text','#151827');document.documentElement.style.setProperty('--muted','#667085')}})();
function qrFor(v){try{const q=qrcode(0,'M');q.addData(v);q.make();document.getElementById('qrImg').src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(q.createSvgTag(4,4));document.getElementById('qrBox').innerHTML=q.createSvgTag(5,4);document.getElementById('qrText').textContent=v}catch(e){}}
function openQr(){document.getElementById('qrModal').style.display='flex'}function closeQr(){document.getElementById('qrModal').style.display='none'}qrFor(VLESS);
</script><a href="__SUPPORT_URL__" target="_blank" rel="noopener" aria-label="support" style="position:fixed;inset-inline-start:14px;bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:40;display:flex;align-items:center;gap:8px;padding:11px 16px;border-radius:999px;background:linear-gradient(120deg,#0ea5e9,#22d3ee);color:#03121c;font:800 12px Vazirmatn,Tahoma,sans-serif;text-decoration:none;box-shadow:0 14px 30px -12px rgba(34,211,238,.8)"><i class="ti ti-brand-telegram" style="font-size:18px"></i> پشتیبانی <bdi dir="ltr">__SUPPORT__</bdi></a>
</body></html>"""
    repl = {
        "__LABEL__": label_e, "__PROTOCOL__": protocol_e, "__UID_SHORT__": esc(uid[:18]+'…'),
        "__EXPIRY__": expiry_e, "__STATUS__": status_e, "__USED__": used_e, "__REMAINING__": rem_e,
        "__IPS__": str(ips), "__EXPIRY_REMAINING__": esc(expiry_remaining), "__LIMIT__": limit_e,
        "__IP__": ip_e, "__CONN__": conn_e, "__SPEED__": speed_e, "__FINGERPRINT__": esc(snapshot.get("fingerprint", "chrome")),
        "__UUID__": uid_e, "__SUB_URL__": sub_e, "__VLESS_URL__": vless_e, "__PCT__": str(pct),
        "__SUB_JS__": sub_js, "__VLESS_JS__": vless_js,
        "__SUPPORT__": esc(get_support_username()), "__SUPPORT_URL__": esc(get_support_url()),
    }
    for k,v in repl.items(): html = html.replace(k,v)
    return HTMLResponse(html)

# ============================================================
# SUB GROUP API
# ============================================================

@app.post("/api/subs")
async def create_sub_api(
    request: Request,
    _=Depends(require_auth),
):

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="JSON نامعتبر است",
        )

    sub_id, sub = await create_sub_group(
        name=body.get(
            "name",
            "گروه جدید",
        ),
        desc=body.get(
            "desc",
            "",
        ),
        password=body.get(
            "password",
            "",
        ),
    )

    host = get_host(request)

    return {
        "sub_id":
            sub_id,

        **sub,

        "password_hash":
            None,

        "public_url":
            (
                f"{get_web_base(host)}"
                f"/p/{sub['uuid_key']}"
            ),

        "sub_url":
            (
                f"{get_web_base(host)}"
                f"/sub-group/{sub['uuid_key']}"
            ),
    }


@app.get("/api/subs")
async def list_subs_api(
    request: Request,
    _=Depends(require_auth),
):

    host = get_host(request)

    async with SUBS_LOCK:
        snapshot_subs = dict(SUBS)

    async with LINKS_LOCK:
        snapshot_links = dict(LINKS)

    result = []

    for sid, sub in snapshot_subs.items():

        link_ids = sub.get(
            "link_ids",
            [],
        )

        active_count = sum(
            1
            for lid in link_ids
            if is_link_allowed(
                snapshot_links.get(
                    lid
                )
            )
        )

        total_used = sum(
            snapshot_links[
                lid
            ].get(
                "used_bytes",
                0,
            )

            for lid in link_ids

            if lid in snapshot_links
        )

        result.append(
            {
                "sub_id":
                    sid,

                **sub,

                "password_hash":
                    None,

                "has_password":
                    sub.get(
                        "password_hash"
                    ) is not None,

                "links_count":
                    len(link_ids) + len(sub.get("remote_links", [])),

                "local_count":
                    len(link_ids),

                "remote_count":
                    len(sub.get("remote_links", [])),

                "active_count":
                    active_count,

                "total_used_bytes":
                    total_used,

                "total_used_fmt":
                    fmt_bytes(
                        total_used
                    ),

                "public_url":
                    (
                        f"{get_web_base(host)}"
                        f"/p/{sub['uuid_key']}"
                    ),

                "sub_url":
                    (
                        f"{get_web_base(host)}"
                        f"/sub-group/{sub['uuid_key']}"
                    ),

                "remote_links":
                    public_remote_links(sub.get("remote_links", [])),
            }
        )

    result.sort(
        key=lambda item:
            item.get(
                "created_at",
                "",
            ),
        reverse=True,
    )

    return {
        "subs": result
    }


@app.patch("/api/subs/{sub_id}")
async def update_sub_api(
    sub_id: str,
    request: Request,
    _=Depends(require_auth),
):

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="JSON نامعتبر است",
        )

    async with SUBS_LOCK:

        if sub_id not in SUBS:
            raise HTTPException(
                status_code=404,
                detail="sub not found",
            )

        sub = SUBS[sub_id]

        if "name" in body:
            sub["name"] = str(
                body["name"]
            )[:60]

        if "desc" in body:
            sub["desc"] = str(
                body["desc"]
            )[:200]

        if "password" in body:

            password = str(
                body.get(
                    "password",
                    "",
                )
            ).strip()

            sub["password_hash"] = (
                hash_password(password)
                if password
                else None
            )

        if "link_ids" in body:

            sub["link_ids"] = list(
                body["link_ids"]
            )

    await save_state()

    return {
        "ok": True
    }


@app.delete("/api/subs/{sub_id}")
async def delete_sub_api(
    sub_id: str,
    _=Depends(require_auth),
):

    name = await remove_sub_group(
        sub_id
    )

    if name is None:
        raise HTTPException(
            status_code=404,
            detail="sub not found",
        )

    return {
        "ok": True,
        "deleted": sub_id,
    }


@app.post("/api/subs/{sub_id}/links")
async def assign_link_to_sub(
    sub_id: str,
    request: Request,
    _=Depends(require_auth),
):

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="JSON نامعتبر است",
        )

    link_id = str(
        body.get(
            "link_id",
            "",
        )
    )

    action = str(
        body.get(
            "action",
            "add",
        )
    )

    if action == "add":

        success = await set_link_sub(
            link_id,
            sub_id,
        )

    else:

        success = await set_link_sub(
            link_id,
            None,
        )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="link or sub not found",
        )

    return {
        "ok": True
    }


# ============================================================
# NODE LINKS IN A SUBSCRIPTION  ·  دقیقاً مثل «Nodes» در پنل سنایی:
# یک اینباند در این پنل + یک اینباند روی یک نودِ دیگر، هر دو در یک اشتراک
# ============================================================

MAX_REMOTE_LINKS_PER_SUB = 200


@app.get("/api/nodes/{node_id}/inbounds")
async def api_node_inbounds(node_id: str, _=Depends(require_owner)):
    """لیست اینباندهای واقعی (نه کلاینت‌ها) روی یک نود، برای انتخاب و اتصال به یک ساب‌گروه اینجا."""
    try:
        from nodes import call_node_json, NodeCallError, get_node
    except Exception:
        raise HTTPException(status_code=503, detail="ماژول نودها در دسترس نیست")
    node = get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="نود پیدا نشد")
    try:
        data = await call_node_json(node_id, "GET", "/api/links")
    except NodeCallError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))
    items = [l for l in (data.get("links") or []) if not l.get("is_client")]
    items.sort(key=lambda l: l.get("created_at") or "", reverse=True)
    return {
        "ok": True,
        "node": {"id": node_id, "name": node.get("name", "")},
        "inbounds": [
            {
                "uuid": l.get("uuid"),
                "label": l.get("label", ""),
                "protocol_display": l.get("protocol_display", ""),
                "network": l.get("network", ""),
                "port": l.get("port"),
                "active": bool(l.get("active", True)),
                "outbound": l.get("outbound"),
                "client_count": l.get("client_count", 0),
            }
            for l in items
        ],
    }


@app.post("/api/subs/{sub_id}/remote-links")
async def add_remote_links_to_sub(sub_id: str, request: Request, _=Depends(require_owner)):
    try:
        from nodes import call_node_json, NodeCallError, get_node
    except Exception:
        raise HTTPException(status_code=503, detail="ماژول نودها در دسترس نیست")
    async with SUBS_LOCK:
        sub = SUBS.get(sub_id)
        if not sub:
            raise HTTPException(status_code=404, detail="گروه ساب پیدا نشد")
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON نامعتبر است")
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="اطلاعات معتبر نیست")
    node_id = str(body.get("node_id") or "").strip()
    uuids = body.get("uuids")
    if uuids is None:
        uuids = [body.get("uuid")]
    if not isinstance(uuids, list) or not uuids:
        raise HTTPException(status_code=400, detail="حداقل یک اینباند از نود انتخاب کن")
    node = get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="نود پیدا نشد")

    async with SUBS_LOCK:
        entries = sub.setdefault("remote_links", [])
        existing_keys = {(e["node_id"], e["uuid"]) for e in entries}

    added, failed = [], []
    for raw_uid in dict.fromkeys(str(u) for u in uuids):
        if (node_id, raw_uid) in existing_keys:
            continue
        if len(existing_keys) + len(added) >= MAX_REMOTE_LINKS_PER_SUB:
            failed.append({"uuid": raw_uid, "error": f"حداکثر {MAX_REMOTE_LINKS_PER_SUB} عضو ریموت در هر ساب"})
            continue
        try:
            data = await call_node_json(node_id, "GET", f"/api/links/{raw_uid}/info", timeout=10.0)
        except NodeCallError as exc:
            failed.append({"uuid": raw_uid, "error": str(exc)})
            continue
        entry = {
            "node_id": node_id,
            "uuid": raw_uid,
            "label": str(data.get("label") or ""),
            "protocol_display": str(data.get("protocol_display") or ""),
            "vless": str(data.get("vless_full") or data.get("vless") or ""),
            "active": bool(data.get("active", True)),
            "used_bytes": int(data.get("used_bytes") or 0),
            "limit_bytes": int(data.get("limit_bytes") or 0),
            "expires_at": data.get("expires_at"),
            "added_at": datetime.now().isoformat(),
            "last_synced_at": datetime.now().isoformat(),
            "last_error": "",
        }
        added.append(entry)

    if added:
        async with SUBS_LOCK:
            sub.setdefault("remote_links", []).extend(added)
        await save_state()
        log_activity("sub", f"{len(added)} اینباند از نود «{node['name']}» به گروه «{sub.get('name','')}» اضافه شد", "ok")

    return {"ok": True, "added": len(added), "failed": failed, "remote_links": public_remote_links(sub.get("remote_links", []))}


@app.delete("/api/subs/{sub_id}/remote-links/{ref_id}")
async def remove_remote_link_from_sub(sub_id: str, ref_id: str, _=Depends(require_owner)):
    async with SUBS_LOCK:
        sub = SUBS.get(sub_id)
        if not sub:
            raise HTTPException(status_code=404, detail="گروه ساب پیدا نشد")
        node_id, _, uid = ref_id.partition(":")
        before = len(sub.get("remote_links", []))
        sub["remote_links"] = [e for e in sub.get("remote_links", []) if not (e["node_id"] == node_id and e["uuid"] == uid)]
        removed = before - len(sub["remote_links"])
    if removed:
        await save_state()
        log_activity("sub", f"یک عضو ریموت از گروه «{sub.get('name','')}» حذف شد", "warn")
    return {"ok": True, "removed": bool(removed)}


@app.post("/api/subs/{sub_id}/remote-links/refresh")
async def refresh_remote_links_api(sub_id: str, _=Depends(require_owner)):
    async with SUBS_LOCK:
        sub = SUBS.get(sub_id)
        if not sub:
            raise HTTPException(status_code=404, detail="گروه ساب پیدا نشد")
    await refresh_remote_links_if_stale(sub, sub_id=sub_id, force=True)
    return {"ok": True, "remote_links": public_remote_links(sub.get("remote_links", []))}


# ============================================================
# GROUP SUB
# ============================================================

REMOTE_LINK_TTL = 300.0  # ثانیه؛ کش لینک‌های نود تا این مدت بدون تماس با نود سرو می‌شود


async def refresh_remote_link_entry(entry: dict) -> dict:
    """کش یک عضو ریموت (لینک روی یک نود) را با یک تماس به همان نود تازه می‌کند.
    اگر نود جواب ندهد، آخرین نسخه‌ی کش‌شده دست‌نخورده می‌ماند (فقط last_error ست می‌شود)."""
    try:
        from nodes import call_node_json, NodeCallError, get_node
    except Exception:
        entry["last_error"] = "ماژول نودها در دسترس نیست"
        return entry
    if not get_node(entry["node_id"]):
        # نود از رجیستری پنل اصلی حذف شده؛ دیگه سعی نمی‌کنیم بهش وصل بشیم و
        # این عضو رو توی خروجی اشتراک نمی‌ذاریم (تا کانفیگِ یتیم بی‌صدا سرو نشه)
        entry["node_missing"] = True
        entry["last_error"] = "این نود از پنل اصلی حذف شده است"
        return entry
    entry.pop("node_missing", None)
    try:
        data = await call_node_json(entry["node_id"], "GET", f"/api/links/{entry['uuid']}/info", timeout=6.0)
        entry.update(
            label=str(data.get("label") or entry.get("label") or ""),
            protocol_display=str(data.get("protocol_display") or entry.get("protocol_display") or ""),
            vless=str(data.get("vless_full") or data.get("vless") or ""),
            active=bool(data.get("active", True)),
            used_bytes=int(data.get("used_bytes") or 0),
            limit_bytes=int(data.get("limit_bytes") or 0),
            expires_at=data.get("expires_at"),
            last_synced_at=datetime.now().isoformat(),
            last_error="",
        )
    except NodeCallError as exc:
        entry["last_error"] = str(exc)[:200]
    except Exception as exc:
        entry["last_error"] = f"{type(exc).__name__}: {str(exc)[:150]}"
    return entry


async def mark_node_removed_in_subs(node_id: str):
    """وقتی یک نود از رجیستری پنل اصلی حذف می‌شه، بلافاصله (نه فقط بعد از TTL کش)
    عضوهای ریموتی که به همون نود اشاره می‌کنن رو «یتیم» علامت می‌زنیم تا از سرو شدن
    یک کانفیگ بدون نظارت جلوگیری بشه. صدا زده می‌شه از nodes.py، هنگام حذف نود."""
    changed = False
    async with SUBS_LOCK:
        for sub in SUBS.values():
            for entry in sub.get("remote_links", []):
                if entry.get("node_id") == node_id and not entry.get("node_missing"):
                    entry["node_missing"] = True
                    entry["last_error"] = "این نود از پنل اصلی حذف شده است"
                    changed = True
    if changed:
        await save_state()


async def refresh_remote_links_if_stale(sub: dict, sub_id: str | None = None, force: bool = False) -> list[dict]:
    entries = sub.get("remote_links", [])
    if not entries:
        return []
    now = time.time()

    def _is_stale(e):
        ts = e.get("last_synced_at")
        if not ts:
            return True
        try:
            return (now - datetime.fromisoformat(ts).timestamp()) > REMOTE_LINK_TTL
        except Exception:
            return True

    stale = entries if force else [e for e in entries if _is_stale(e)]
    if stale:
        await asyncio.gather(*(refresh_remote_link_entry(e) for e in stale), return_exceptions=True)
        if sub_id:
            await save_state()
    return entries


@app.get("/sub-group/{uuid_key}")
async def sub_group_subscription(
    uuid_key: str,
    request: Request,
):

    async with SUBS_LOCK:

        sub = next(
            (
                item
                for item
                in SUBS.values()
                if item.get(
                    "uuid_key"
                ) == uuid_key
            ),
            None,
        )

    if not sub:
        raise HTTPException(
            status_code=404,
            detail="not found",
        )

    if _subscription_wants_browser_view(request):
        _qs = "&".join(
            f"{quote(str(k), safe='')}={quote(str(v), safe='')}"
            for k, v in request.query_params.multi_items()
            if k not in ("web", "raw")
        )
        return RedirectResponse(
            url=f"/p/{uuid_key}" + (f"?{_qs}" if _qs else ""),
            status_code=307,
            headers=_SUB_NO_STORE,
        )

    if sub.get(
        "password_hash"
    ):

        password = (
            request.query_params.get(
                "pw",
                "",
            )
        )

        if (
            hash_password(password)
            != sub["password_hash"]
        ):

            raise HTTPException(
                status_code=403,
                detail="wrong password",
            )

    host = get_host(request)

    template_link = None
    template_id = None
    total_used = 0
    total_limit = 0
    expiries = []

    async with LINKS_LOCK:

        lines = []

        for link_id in sub.get(
            "link_ids",
            [],
        ):

            link = LINKS.get(
                link_id
            )

            if (
                link
                and is_link_allowed(
                    link
                )
            ):

                if template_link is None:
                    template_link = link
                    template_id = link_id
                total_used += int(link.get("used_bytes", 0) or 0)
                total_limit += int(link.get("limit_bytes", 0) or 0)
                if link.get("expires_at"):
                    expiries.append(str(link.get("expires_at")))

                lines.append(
                    vless_link_for_link(
                        link,
                        link_id,
                        host,
                    )
                )

    # اعضای «ریموت» = لینک‌هایی که روی یک نود دیگر ساخته شده‌اند و به این ساب‌گروه
    # وصل شده‌اند (دقیقاً همان ایده‌ی «Nodes» در پنل سنایی: یک اینباند روی پنل اصلی +
    # یک اینباند روی پنل دیگر، هر دو داخل یک اشتراک).
    remote_entries = await refresh_remote_links_if_stale(sub, sub_id=next((k for k, v in SUBS.items() if v is sub), None))
    for entry in remote_entries:
        if not entry.get("active", True):
            continue
        total_used += int(entry.get("used_bytes", 0) or 0)
        total_limit += int(entry.get("limit_bytes", 0) or 0)
        if entry.get("expires_at"):
            expiries.append(str(entry.get("expires_at")))
        if not entry.get("node_missing") and entry.get("vless"):
            lines.append(entry["vless"])

    # For a group subscription, expose aggregate usage/expiry in standard headers.
    group_limit = total_limit if total_limit > 0 else 0
    group_expiry = None
    if expiries:
        try:
            group_expiry = min(
                expiries,
                key=lambda x: datetime.fromisoformat(x)
            )
        except Exception:
            group_expiry = expiries[0]

    # ردیف اطلاعاتی (با آدرس و UUID واقعی، بدون هیچ آدرس فیک) — اگر حداقل یک
    # کانفیگ واقعی در این گروه باشد، به‌عنوان اولین ردیفِ لیست سرورها اضافه می‌شود تا
    # کاربر همان لحظه که اپش را باز می‌کند، حجم/زمان باقی‌مانده‌اش را ببیند.
    group_info_remark = build_info_server_remark(total_used, group_limit, group_expiry)
    if template_link is not None and bool(CONFIG.get("sub_info_line_enabled", True)):
        lines.insert(0, vless_link_for_link({**template_link, "label": group_info_remark}, template_id, host))

    content = (
        base64
        .b64encode(
            "\n".join(
                lines
            ).encode()
        )
        .decode()
    )

    _chan = _clean_tg_username(CONFIG.get("channel_username")) or CHANNEL_USERNAME
    group_title = f"{group_info_remark} | {sub['name']} | @{_chan}"
    headers = subscription_metadata_headers(
        total_used,
        group_limit,
        group_expiry,
        host,
        f"{get_web_base(host)}/p/{uuid_key}",
        group_title,
    )
    headers.update(_SUB_NO_STORE)

    return Response(
        content=content,
        media_type="text/plain; charset=utf-8",
        headers=headers,
    )


# ============================================================
# PUBLIC GROUP
# ============================================================

from ui_portal import PUBLIC_SUB_V18 as PUBLIC_SUB_HTML



@app.get(
    "/p/{uuid_key}",
    response_class=HTMLResponse,
)
async def public_sub_page(
    uuid_key: str,
):

    async with SUBS_LOCK:

        exists = any(
            item.get(
                "uuid_key"
            ) == uuid_key
            for item in SUBS.values()
        )

    if not exists:

        return HTMLResponse(
            """
            <h2
            style="
            font-family:sans-serif;
            padding:40px;
            "
            >
            گروه پیدا نشد
            </h2>
            """,
            status_code=404,
        )

    return HTMLResponse(
        PUBLIC_SUB_HTML
    )


@app.get("/api/public/sub/{uuid_key}")
async def public_sub_data(
    uuid_key: str,
    request: Request,
):

    async with SUBS_LOCK:

        entry = next(
            (
                (
                    sid,
                    item,
                )

                for sid, item
                in SUBS.items()

                if item.get(
                    "uuid_key"
                ) == uuid_key
            ),
            None,
        )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="not found",
        )

    _, sub = entry

    has_password = (
        sub.get(
            "password_hash"
        ) is not None
    )

    if has_password:

        password = (
            request
            .query_params
            .get(
                "pw",
                "",
            )
        )

        if (
            hash_password(password)
            != sub[
                "password_hash"
            ]
        ):

            return JSONResponse(
                {
                    "locked": True,
                    "name":
                        sub["name"],
                }
            )

    host = get_host(request)

    async with LINKS_LOCK:
        snapshot = dict(LINKS)

    links_out = []

    active_ip_set = set()
    active_session_count = 0

    for link_id in sub.get(
        "link_ids",
        [],
    ):

        link = snapshot.get(
            link_id
        )

        if not link:
            continue

        allowed = is_link_allowed(
            link
        )

        link_ips = {
            str(item.get("ip") or "").strip()
            for item in connections.values()
            if item.get("uuid") == link_id and str(item.get("ip") or "").strip()
        }
        connection_count = len(link_ips)
        active_session_count += sum(1 for item in connections.values() if item.get("uuid") == link_id)
        active_ip_set.update(link_ips)

        links_out.append(
            {
                "uuid":
                    link_id,

                "label":
                    link.get(
                        "label"
                    ),

                "active":
                    allowed,

                "protocol":
                    link.get(
                        "protocol",
                        DEFAULT_PROTOCOL,
                    ),

                "used_bytes":
                    link.get(
                        "used_bytes",
                        0,
                    ),

                "used_fmt":
                    fmt_bytes(
                        link.get(
                            "used_bytes",
                            0,
                        )
                    ),

                "limit_bytes":
                    link.get(
                        "limit_bytes",
                        0,
                    ),

                "limit_fmt":
                    (
                        "∞"
                        if not link.get(
                            "limit_bytes",
                            0,
                        )
                        else fmt_bytes(
                            link[
                                "limit_bytes"
                            ]
                        )
                    ),

                "expires_at":
                    link.get(
                        "expires_at"
                    ),

                "vless_link":
                    vless_link_for_link(
                        link,
                        link_id,
                        host,
                    ),

                "sub_url":
                    (
                        f"{get_web_base(host)}"
                        f"/sub/{link_id}"
                    ),

                "info_url":
                    (
                        f"{get_web_base(host)}"
                        f"/info/{link_id}"
                    ),

                "connections":
                    connection_count,

                "ip_limit":
                    link.get(
                        "ip_limit",
                        0,
                    ),

                "speed_limit_bytes":
                    link.get(
                        "speed_limit_bytes",
                        0,
                    ),

                "connection_limit":
                    link.get(
                        "connection_limit",
                        0,
                    ),
            }
        )

    total_used = sum(
        item["used_bytes"]
        for item in links_out
    )

    # حجم کل: اگر حتی یک کانفیگ نامحدود باشد، کل اشتراک نامحدود حساب می‌شود
    _limits = [int(item.get("limit_bytes") or 0) for item in links_out]
    _sub_total_limit = sum(_limits) if _limits and all(x > 0 for x in _limits) else 0
    _exps = [str(item.get("expires_at") or "") for item in links_out]
    _sub_expires_at = max(_exps) if _exps and all(_exps) else None

    return {
        "locked": False,

        "name":
            sub["name"],

        "desc":
            sub.get(
                "desc",
                "",
            ),

        "sub_url":
            (
                f"{get_web_base(host)}"
                f"/sub-group/{uuid_key}"
            ),

        "active_connections":
            len(active_ip_set),

        "active_sessions":
            active_session_count,

        "active_ips":
            sorted(active_ip_set),

        "total_used_fmt":
            fmt_bytes(
                total_used
            ),

        "support":
            get_support_username(),

        "support_url":
            get_support_url(),

        "channel_url":
            get_channel_url() if _clean_tg_username(CONFIG.get("channel_username")) else "",

        "total_used_bytes":
            total_used,

        "total_limit_bytes":
            _sub_total_limit,

        "expires_at":
            _sub_expires_at,

        "links":
            links_out,
    }




@app.post("/api/mix-sub")
async def mix_subscription(request: Request, _=Depends(require_auth)):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON نامعتبر")
    ids = body.get("link_ids") or []
    if not isinstance(ids, list) or len(ids) < 2:
        raise HTTPException(status_code=400, detail="حداقل ۲ کانفیگ انتخاب کنید")
    if len(ids) > 40:
        raise HTTPException(status_code=400, detail="حداکثر ۴۰ کانفیگ")
    host = get_host(request)
    lines = []
    used_names = set()
    total_used = 0
    total_limit = 0
    labels = []
    async with LINKS_LOCK:
        for lid in ids:
            link = LINKS.get(lid)
            if not link or not is_link_allowed(link):
                continue
            labels.append(str(link.get("label") or lid[:8]))
            total_used += int(link.get("used_bytes", 0) or 0)
            total_limit += int(link.get("limit_bytes", 0) or 0)
            name = random_config_name(used_names)
            used_names.add(name)
            lines.append(vless_link_for_link({**link, "label": name}, lid, host))
    if not lines:
        raise HTTPException(status_code=400, detail="هیچ کانفیگ معتبری انتخاب نشده")
    # stats first line
    vol = f"{fmt_bytes(total_used)}/{fmt_bytes(total_limit)}" if total_limit > 0 else f"{fmt_bytes(total_used)}/∞"
    mix_label = "Mix-" + random_config_name()[:6]
    stats = f"{mix_label} | {vol} | {len(lines)} configs"
    first = generate_vless_link(ids[0], "127.0.0.1", remark=stats, protocol="vless-ws")
    content = base64.b64encode(("\n".join([first] + lines)).encode()).decode()
    # store as a sub group for reuse
    sub_id, sub = await create_sub_group(name=mix_label, desc="مخلوط‌سازی کانفیگ‌ها")
    async with SUBS_LOCK:
        if sub_id in SUBS:
            SUBS[sub_id]["link_ids"] = list(ids)
    await save_state()
    return {
        "ok": True,
        "sub_url": f"{get_web_base(host)}/sub-group/{sub['uuid_key']}",
        "name": mix_label,
        "count": len(lines),
        "content_preview": stats,
    }


@app.get("/api/categories")
async def list_categories(_=Depends(require_auth)):
    items = [{**cat, "id": cid} for cid, cat in CATEGORIES.items()]
    items.sort(key=lambda x: int(x.get("number", 0)))
    return {"categories": items}

@app.post("/api/categories")
async def create_category(request: Request, _=Depends(require_auth)):
    if len(CATEGORIES) >= 10:
        raise HTTPException(status_code=400, detail="حداکثر ۱۰ دسته‌بندی")
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON نامعتبر")
    name = str(body.get("name") or "دسته جدید").strip()[:40]
    used = {int(x.get("number", 0)) for x in CATEGORIES.values()}
    num = 0
    while num in used:
        num += 1
    cid = str(num)
    limit_value = safe_float(body.get("limit_value", 0))
    limit_unit = str(body.get("limit_unit") or "GB").upper()
    limit_bytes = 0 if limit_value <= 0 else parse_size_to_bytes(limit_value, limit_unit)
    speed_value = safe_float(body.get("speed_limit_value", 0))
    speed_bytes = 0 if speed_value <= 0 else parse_speed_to_bytes(speed_value, "MBIT")
    raw_clean = body.get("clean_ips") or ""
    if isinstance(raw_clean, list):
        clean_ips = [str(x).strip() for x in raw_clean if str(x).strip()]
    else:
        clean_ips = [x.strip() for x in str(raw_clean).replace(",", "\n").splitlines() if x.strip()]
    record = {
        "id": cid, "name": name, "number": num,
        "limit_bytes": limit_bytes,
        "expires_days": safe_int(body.get("expires_days", 0), minimum=0),
        "connection_limit": safe_int(body.get("connection_limit", 0), minimum=0),
        "speed_limit_bytes": speed_bytes,
        "ip_limit": safe_int(body.get("ip_limit", 0), minimum=0),
        "clean_ips": clean_ips,
        "random_name": bool(body.get("random_name", False)),
        "single_user": bool(body.get("single_user", False)),
        "created_at": datetime.now().isoformat(),
    }
    CATEGORIES[cid] = record
    await save_state()
    return {"ok": True, **record}


@app.patch("/api/categories/{cid}")
async def update_category(cid: str, request: Request, _=Depends(require_auth)):
    if cid not in CATEGORIES:
        raise HTTPException(status_code=404, detail="یافت نشد")
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON نامعتبر")
    cat = CATEGORIES[cid]
    if "name" in body:
        cat["name"] = str(body.get("name") or cat["name"]).strip()[:40]
    if "limit_value" in body:
        lv = safe_float(body.get("limit_value", 0))
        unit = str(body.get("limit_unit") or "GB").upper()
        cat["limit_bytes"] = 0 if lv <= 0 else parse_size_to_bytes(lv, unit)
    if "expires_days" in body:
        cat["expires_days"] = safe_int(body.get("expires_days", 0), minimum=0)
    if "connection_limit" in body:
        cat["connection_limit"] = safe_int(body.get("connection_limit", 0), minimum=0)
    if "speed_limit_value" in body:
        sv = safe_float(body.get("speed_limit_value", 0))
        cat["speed_limit_bytes"] = 0 if sv <= 0 else parse_speed_to_bytes(sv, "MBIT")
    if "ip_limit" in body:
        cat["ip_limit"] = safe_int(body.get("ip_limit", 0), minimum=0)
    if "clean_ips" in body:
        raw = body.get("clean_ips") or ""
        if isinstance(raw, list):
            cat["clean_ips"] = [str(x).strip() for x in raw if str(x).strip()]
        else:
            cat["clean_ips"] = [x.strip() for x in str(raw).replace(",", "\n").splitlines() if x.strip()]
    if "random_name" in body:
        cat["random_name"] = bool(body.get("random_name"))
    if "single_user" in body:
        cat["single_user"] = bool(body.get("single_user"))
    await save_state()
    return {"ok": True, **cat}

@app.delete("/api/categories/{cid}")
async def delete_category(cid: str, _=Depends(require_auth)):
    if cid in ("0", "1"):
        raise HTTPException(status_code=400, detail="پیش‌فرض قابل حذف نیست")
    if cid not in CATEGORIES:
        raise HTTPException(status_code=404, detail="یافت نشد")
    del CATEGORIES[cid]
    for link in LINKS.values():
        if str(link.get("category_id")) == cid:
            link["category_id"] = "0"
    await save_state()
    return {"ok": True}

# ============================================================
# STATS
# ============================================================

@app.get("/stats")
async def get_stats(
    request: Request,
    _=Depends(require_auth),
):

    async with LINKS_LOCK:
        snapshot = dict(LINKS)
    _scope = await actor_scope(request)
    _aid = await actor_id_of(request)
    snapshot = {u: l for u, l in snapshot.items() if client_visible(l, _aid)}
    if _scope is not None:
        snapshot = {u: l for u, l in snapshot.items() if u in _scope or l.get("parent_inbound_id") in _scope}
        used = sum(int(l.get("used_bytes", 0) or 0) for l in snapshot.values())
        return {
            "service": APP_NAME, "version": APP_VERSION, "scoped": True,
            "active_connections": sum(1 for c in connections.values() if c.get("uuid") in snapshot),
            "total_traffic_mb": round(used / (1024 ** 2), 2), "total_traffic_bytes": used,
            "total_requests": 0, "total_errors": 0, "uptime": uptime(),
            "timestamp": datetime.now().isoformat(), "hourly": {}, "recent_errors": [],
            "links_count": len(snapshot),
            "active_links": sum(1 for l in snapshot.values() if is_link_allowed(l)),
            "expired_links": sum(1 for l in snapshot.values() if is_link_expired(l)),
            "subs_count": 0,
        }

    return {
        "service":
            APP_NAME,

        "version":
            APP_VERSION,

        "active_connections":
            len(connections),

        "total_traffic_mb":
            round(
                stats[
                    "total_bytes"
                ]
                / (
                    1024 ** 2
                ),
                2,
            ),

        "total_traffic_bytes":
            stats[
                "total_bytes"
            ],

        "total_requests":
            stats[
                "total_requests"
            ],

        "total_errors":
            stats[
                "total_errors"
            ],

        "uptime":
            uptime(),

        "timestamp":
            datetime.now().isoformat(),

        "hourly":
            dict(
                hourly_traffic
            ),

        "recent_errors":
            list(
                error_logs
            )[-10:],

        "links_count":
            len(snapshot),

        "active_links":
            sum(
                1
                for link
                in snapshot.values()
                if is_link_allowed(
                    link
                )
            ),

        "expired_links":
            sum(
                1
                for link
                in snapshot.values()
                if is_link_expired(
                    link
                )
            ),

        "subs_count":
            len(SUBS),
    }


@app.get("/api/errors")
async def get_errors(
    _=Depends(require_auth),
):
    rows = list(error_logs)[-100:]
    warnings = sum(1 for x in rows if x.get("level") == "warn")
    client_errors = sum(1 for x in rows if x.get("source") == "client")
    return {
        "ok": True,
        "errors": rows,
        "total_errors": len(rows),
        "warnings": warnings,
        "client_errors": client_errors,
        "healthy": not any(x.get("level", "err") == "err" for x in rows[-20:]),
    }


@app.post("/api/errors/client")
async def report_client_error(request: Request, _=Depends(require_auth)):
    try:
        body = await request.json()
    except Exception:
        body = {}
    message = str(body.get("message") or "Unknown browser error").strip()[:1200]
    path = str(body.get("path") or request.url.path).strip()[:500]
    stack = str(body.get("stack") or "").strip()[:4000]
    details = str(body.get("details") or "").strip()[:1500]
    error_logs.append({
        "error": message,
        "path": path,
        "method": "CLIENT",
        "source": "client",
        "level": "err",
        "stack": stack,
        "details": details,
        "time": datetime.now().isoformat(),
    })
    stats["total_errors"] += 1
    logger.error("Client error: %s | %s", path, message)
    return {"ok": True}


@app.post("/api/errors/clear")
async def clear_errors(_=Depends(require_owner)):
    count = len(error_logs)
    error_logs.clear()
    stats["total_errors"] = 0
    log_activity("system", f"مرکز پیام پاک شد؛ {count} خطا حذف شد", "warn" if count else "info")
    return {"ok": True, "cleared": count}


@app.get("/api/activity")
async def get_activity(
    _=Depends(require_auth),
):

    return {
        "logs":
            list(
                activity_logs
            )[-150:]
    }


# ============================================================
# CONNECTIONS
# ============================================================

@app.get("/api/connections")
async def get_connections(
    _=Depends(require_auth),
):

    async with LINKS_LOCK:
        snapshot = dict(LINKS)

    grouped = {}

    for connection in connections.values():

        ip = connection.get(
            "ip",
            "نامشخص",
        )

        link = snapshot.get(
            connection.get(
                "uuid"
            )
        )

        label = (
            link.get(
                "label"
            )
            if link
            else "نامشخص"
        )

        group = grouped.get(ip)

        if group is None:

            group = {
                "ip":
                    ip,

                "sessions":
                    0,

                "bytes":
                    0,

                "labels":
                    set(),

                "transports":
                    set(),

                "first_connected_at":
                    connection.get(
                        "connected_at"
                    ),

                "last_connected_at":
                    connection.get(
                        "connected_at"
                    ),
            }

            grouped[ip] = group

        group["sessions"] += 1

        group["bytes"] += int(
            connection.get(
                "bytes",
                0,
            )
            or 0
        )

        group["labels"].add(
            label
        )

        group["transports"].add(
            connection.get(
                "transport",
                DEFAULT_PROTOCOL,
            )
        )

    result = []

    for group in grouped.values():

        result.append(
            {
                "ip":
                    group["ip"],

                "sessions":
                    group["sessions"],

                "labels":
                    sorted(
                        group["labels"]
                    ),

                "label":
                    (
                        " · ".join(
                            sorted(
                                group["labels"]
                            )
                        )
                        if group["labels"]
                        else "نامشخص"
                    ),

                "transports":
                    sorted(
                        group["transports"]
                    ),

                "bytes":
                    group["bytes"],

                "bytes_fmt":
                    fmt_bytes(
                        group["bytes"]
                    ),

                "connected_at":
                    group[
                        "first_connected_at"
                    ],

                "last_connected_at":
                    group[
                        "last_connected_at"
                    ],
            }
        )

    result.sort(
        key=lambda item:
            item.get(
                "last_connected_at"
            )
            or "",
        reverse=True,
    )

    return {
        "connections":
            result,

        "count":
            len(result),

        "raw_count":
            len(connections),
    }


# ============================================================
# OPTIONAL EXISTING PROJECT MODULES
# ============================================================

# ============================================================
# IMPORTANT:
# DO NOT REPLACE THIS VLESS CORE.
# ============================================================

try:

    from relay_vless import (
        RELAY_BUF,
        parse_vless_header,
        check_and_use,
        relay_ws_to_tcp,
        relay_tcp_to_ws,
        websocket_tunnel,
    )

    app.add_api_websocket_route(
        "/ws/{uuid}",
        websocket_tunnel,
    )

    logger.info(
        "VLESS relay loaded."
    )

except Exception as exc:

    logger.warning(
        "VLESS relay module unavailable: %s",
        exc,
    )


# ============================================================
# XHTTP
# ============================================================

try:

    from xhttp_siz10 import (
        router as xhttp_router
    )

    app.include_router(
        xhttp_router
    )

    logger.info(
        "XHTTP module loaded."
    )

except Exception as exc:

    logger.warning(
        "XHTTP module unavailable: %s",
        exc,
    )


# ============================================================
# OUTBOUND PROXY (SOCKS)
# ============================================================

try:

    from outbound_proxy import (
        router as outbound_proxy_router
    )

    app.include_router(
        outbound_proxy_router
    )

    logger.info(
        "Outbound proxy module loaded."
    )

except Exception as exc:

    logger.warning(
        "Outbound proxy module unavailable: %s",
        exc,
    )


# نودها: توکن API این پنل + اتصال به پنل‌های دیگر (nodes.py)
try:

    from nodes import router as nodes_router

    app.include_router(nodes_router)

    logger.info("Nodes module loaded.")

except Exception as exc:

    logger.warning(
        "Nodes module unavailable: %s",
        exc,
    )


# ============================================================
# TELEGRAM
# ============================================================

try:

    from telegram_bot import (
        start_bot as _tg_start_bot,
        stop_bot as _tg_stop_bot,
    )

except Exception:

    async def _tg_start_bot():
        return None

    async def _tg_stop_bot():
        return None


@app.on_event("startup")
async def start_optional_telegram():

    try:

        await _tg_start_bot()

        logger.info(
            "Telegram module initialized."
        )

    except Exception as exc:

        logger.warning(
            "Telegram bot disabled/error: %s",
            exc,
        )


# ============================================================
# HTTP PROXY
# ============================================================

_HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-encoding",
    "content-length",
}


@app.api_route(
    "/proxy/{target_url:path}",
    methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
        "HEAD",
        "OPTIONS",
    ],
)
async def http_proxy(
    target_url: str,
    request: Request,
):

    if not target_url.startswith("http"):
        target_url = (
            "https://"
            + target_url
        )

    if http_client is None:
        raise HTTPException(
            status_code=503,
            detail="HTTP client not ready",
        )

    try:

        body = await request.body()

        headers = {
            key: value
            for key, value
            in request.headers.items()
            if (
                key.lower()
                not in _HOP
            )
            and (
                key.lower()
                != "host"
            )
        }

        response = await http_client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
        )

        stats["total_bytes"] += len(
            response.content
        )

        bump_daily_stat("traffic_bytes", len(response.content))

        stats["total_requests"] += 1

        hourly_traffic[
            now_ir().strftime(
                "%H:00"
            )
        ] += len(
            response.content
        )

        output_headers = {
            key: value
            for key, value
            in response.headers.items()
            if key.lower() not in _HOP
        }

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=output_headers,
        )

    except Exception as exc:

        stats["total_errors"] += 1

        error_logs.append(
            {
                "error":
                    str(exc),

                "url":
                    target_url,

                "time":
                    datetime.now().isoformat(),
            }
        )

        logger.exception(
            "Proxy error: %s",
            target_url,
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "Proxy error: "
                f"{exc}"
            ),
        )


# ============================================================
# DASHBOARD
# ============================================================

from pages import DASHBOARD_HTML


@app.get(
    "/dashboard",
    response_class=HTMLResponse,
)
async def dashboard(
    request: Request,
):

    if not await is_valid_session(
        request.cookies.get(
            SESSION_COOKIE
        )
    ):
        return RedirectResponse(
            "/login"
        )

    await ensure_default_categories()
    await ensure_default_link()

    return HTMLResponse(
        DASHBOARD_HTML
    )


# ============================================================
# TEST
# ============================================================

@app.get(
    "/test-ws",
    response_class=HTMLResponse,
)
async def test_ws():

    return HTMLResponse(
        """
        <script>
        location.href='/dashboard'
        </script>
        """
    )


# ============================================================
# ADMIN MANAGEMENT (multi-admin / sub-admins)
# ============================================================

def _admin_public(admin_id: str, admin: dict) -> dict:
    return {
        "id": admin_id,
        "username": admin.get("username", admin_id),
        "role": admin.get("role", "admin"),
        "permissions": sorted(admin.get("permissions") or {"dashboard"}),
        "active": admin.get("active", True),
        "created_at": admin.get("created_at"),
        "last_login_at": admin.get("last_login_at"),
        "last_login_ip": admin.get("last_login_ip"),
        "credit_stars": admin.get("credit_stars", 0),
        "full_name": admin.get("full_name", ""),
        "telegram_id": admin.get("telegram_id", ""),
        "allowed_inbounds": list(admin.get("allowed_inbounds") or []),
        "perm_v2": bool(admin.get("perm_v2")),
    }


def _clean_allowed_inbounds(raw):
    if not isinstance(raw, list):
        return []
    out = []
    for u in raw:
        u = str(u)
        l = LINKS.get(u)
        if l and not l.get("parent_inbound_id") and u not in out:
            out.append(u)
    return out


@app.get("/api/admins")
async def api_list_admins(token=Depends(require_owner)):
    owner_entry = {
        "id": "owner",
        "username": AUTH.get("username", DEFAULT_ADMIN_USERNAME),
        "role": "owner",
        "active": True,
        "created_at": None,
        "last_login_at": None,
        "last_login_ip": None,
    }
    admins = [owner_entry] + [
        _admin_public(aid, a) for aid, a in ADMINS.items()
    ]
    return {"ok": True, "admins": admins}


@app.post("/api/admins")
async def api_create_admin(request: Request, token=Depends(require_owner)):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    username = str(body.get("username", "")).strip()
    password = str(body.get("password", "")).strip()

    if not username or username.lower() == "owner":
        raise HTTPException(status_code=400, detail="نام کاربری نامعتبر است")

    if len(password) < LOGIN_MIN_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"رمز عبور باید حداقل {LOGIN_MIN_PASSWORD_LENGTH} کاراکتر باشد",
        )

    if username.lower() == AUTH.get("username", DEFAULT_ADMIN_USERNAME).lower():
        raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")
    for a in ADMINS.values():
        if a.get("username", "").lower() == username.lower():
            raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")

    admin_id = secrets.token_hex(6)

    ADMINS[admin_id] = {
        "username": username,
        "password_hash": hash_password(password),
        "role": "admin",
        "permissions": [p for p in (body.get("permissions") or ["dashboard", "inbounds", "subscriptions"]) if p in ALL_PERMISSIONS],
        "perm_v2": True,
        "allowed_inbounds": _clean_allowed_inbounds(body.get("allowed_inbounds")),
        "active": True,
        "created_at": datetime.now().isoformat(),
        "last_login_at": None,
        "last_login_ip": None,
    }

    await save_state()

    log_activity("auth", f"ادمین جدید «{username}» ایجاد شد", "ok")

    return {"ok": True, "admin": _admin_public(admin_id, ADMINS[admin_id])}


@app.patch("/api/admins/{admin_id}")
async def api_update_admin(admin_id: str, request: Request, token=Depends(require_owner)):
    admin = ADMINS.get(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="ادمین یافت نشد")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    if "username" in body:
        new_username = str(body["username"]).strip()
        if not new_username or new_username.lower() == "owner":
            raise HTTPException(status_code=400, detail="نام کاربری نامعتبر است")
        for aid, a in ADMINS.items():
            if aid != admin_id and a.get("username", "").lower() == new_username.lower():
                raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")
        admin["username"] = new_username

    password_changed = False
    if "password" in body and str(body["password"]).strip():
        new_password = str(body["password"]).strip()
        if len(new_password) < LOGIN_MIN_PASSWORD_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"رمز عبور باید حداقل {LOGIN_MIN_PASSWORD_LENGTH} کاراکتر باشد",
            )
        admin["password_hash"] = hash_password(new_password)
        password_changed = True

    if "permissions" in body:
        raw_permissions = body.get("permissions") or []
        if not isinstance(raw_permissions, list):
            raise HTTPException(status_code=400, detail="لیست دسترسی‌ها نامعتبر است")
        admin["permissions"] = [p for p in raw_permissions if p in ALL_PERMISSIONS]
        admin["perm_v2"] = True

    if "allowed_inbounds" in body:
        admin["allowed_inbounds"] = _clean_allowed_inbounds(body.get("allowed_inbounds"))

    if "active" in body:
        admin["active"] = bool(body["active"])

    # Password changes must invalidate existing sessions for that account.
    # Otherwise an old stolen/remembered session would remain usable after a
    # credential reset. Deactivation also revokes every session.
    if password_changed or not admin.get("active", True):
        async with SESSIONS_LOCK:
            for tok in [t for t, info in SESSIONS.items()
                        if isinstance(info, dict) and info.get("admin_id") == admin_id]:
                SESSIONS.pop(tok, None)

    await save_state()

    log_activity("auth", f"اطلاعات ادمین «{admin.get('username')}» ویرایش شد", "ok")

    return {"ok": True, "admin": _admin_public(admin_id, admin)}


@app.delete("/api/admins/{admin_id}")
async def api_delete_admin(admin_id: str, token=Depends(require_owner)):
    admin = ADMINS.pop(admin_id, None)
    if not admin:
        raise HTTPException(status_code=404, detail="ادمین یافت نشد")

    async with SESSIONS_LOCK:
        for tok in [t for t, info in SESSIONS.items() if isinstance(info, dict) and info.get("admin_id") == admin_id]:
            SESSIONS.pop(tok, None)

    await save_state()

    log_activity("auth", f"ادمین «{admin.get('username')}» حذف شد", "warn")

    return {"ok": True}


# ============================================================
# ADMIN REGISTRATION REQUESTS ("ثبت‌نام ادمینی" روی صفحه لاگین)
# ============================================================

def _admin_request_public(req_id: str, req: dict) -> dict:
    return {
        "id": req_id,
        "full_name": req.get("full_name", ""),
        "telegram_id": req.get("telegram_id", ""),
        "note": req.get("note", ""),
        "status": req.get("status", "pending"),
        "created_at": req.get("created_at"),
        "decided_at": req.get("decided_at"),
        "admin_id": req.get("admin_id"),
        "ip": req.get("ip"),
    }


@app.post("/api/admin-requests")
async def api_submit_admin_request(request: Request):
    """صفحه لاگین این را صدا می‌زند؛ نیازی به احراز هویت ندارد."""

    ip = client_ip(request)

    now = time.time()
    if len(ADMIN_REQUEST_RATE) > 2000:
        for _ip in [k for k, v in ADMIN_REQUEST_RATE.items() if now - v > ADMIN_REQUEST_COOLDOWN_SECONDS]:
            ADMIN_REQUEST_RATE.pop(_ip, None)
    last = ADMIN_REQUEST_RATE.get(ip, 0)
    if now - last < ADMIN_REQUEST_COOLDOWN_SECONDS:
        raise HTTPException(
            status_code=429,
            detail="کمی صبر کنید و دوباره تلاش کنید",
        )

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    full_name = str(body.get("full_name", "")).strip()
    telegram_id = str(body.get("telegram_id", "")).strip().lstrip("@")
    note = str(body.get("note", "")).strip()[:500]

    if not full_name or len(full_name) < 3:
        raise HTTPException(status_code=400, detail="نام و نام خانوادگی را کامل وارد کنید")
    if not re.fullmatch(r"[A-Za-z0-9_]{3,64}", telegram_id):
        raise HTTPException(status_code=400, detail="آیدی تلگرام معتبر وارد کنید")

    if sum(1 for r in ADMIN_REQUESTS.values() if r.get("status") == "pending") >= 200:
        raise HTTPException(status_code=429, detail="ظرفیت درخواست‌ها پر است؛ بعداً تلاش کنید")

    ADMIN_REQUEST_RATE[ip] = now

    async with ADMIN_REQUESTS_LOCK:
        req_id = secrets.token_hex(6)
        ADMIN_REQUESTS[req_id] = {
            "full_name": full_name[:120],
            "telegram_id": telegram_id[:120],
            "note": note,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "decided_at": None,
            "admin_id": None,
            "ip": ip,
        }

    await save_state()

    log_activity(
        "auth",
        f"درخواست ثبت‌نام ادمین جدید از «{full_name}» (@{telegram_id})",
        "info",
    )

    return {"ok": True, "id": req_id}


@app.get("/api/admin-requests")
async def api_list_admin_requests(token=Depends(require_owner)):
    pending = sum(1 for r in ADMIN_REQUESTS.values() if r.get("status") == "pending")
    requests_list = sorted(
        (_admin_request_public(rid, r) for rid, r in ADMIN_REQUESTS.items()),
        key=lambda r: r.get("created_at") or "",
        reverse=True,
    )
    return {"ok": True, "requests": requests_list, "pending": pending}


@app.post("/api/admin-requests/{req_id}/approve")
async def api_approve_admin_request(req_id: str, request: Request, token=Depends(require_owner)):
    """مالک اینجا تصمیم می‌گیرد چه نام‌کاربری/رمز/دسترسی/شارژی به درخواست‌کننده بدهد
    و همان لحظه حساب ادمین واقعی برایش ساخته می‌شود."""

    req = ADMIN_REQUESTS.get(req_id)
    if not req:
        raise HTTPException(status_code=404, detail="درخواست یافت نشد")
    if req.get("status") != "pending":
        raise HTTPException(status_code=409, detail="این درخواست قبلاً بررسی شده است")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    username = str(body.get("username", "")).strip()
    password = str(body.get("password", "")).strip()

    if not username or username.lower() == "owner":
        raise HTTPException(status_code=400, detail="نام کاربری نامعتبر است")
    if len(password) < LOGIN_MIN_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"رمز عبور باید حداقل {LOGIN_MIN_PASSWORD_LENGTH} کاراکتر باشد",
        )
    if username.lower() == AUTH.get("username", DEFAULT_ADMIN_USERNAME).lower():
        raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")
    for a in ADMINS.values():
        if a.get("username", "").lower() == username.lower():
            raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")

    credit_stars = safe_int(body.get("credit_stars"), default=0, minimum=0)

    admin_id = secrets.token_hex(6)
    ADMINS[admin_id] = {
        "username": username,
        "password_hash": hash_password(password),
        "role": "admin",
        "permissions": list(body.get("permissions") or {"dashboard", "inbounds", "subscriptions"}),
        "active": True,
        "created_at": datetime.now().isoformat(),
        "last_login_at": None,
        "last_login_ip": None,
        "credit_stars": credit_stars,
        "full_name": req.get("full_name", ""),
        "telegram_id": req.get("telegram_id", ""),
        "perm_v2": True,
        "allowed_inbounds": _clean_allowed_inbounds(body.get("allowed_inbounds")),
    }

    req["status"] = "approved"
    req["decided_at"] = datetime.now().isoformat()
    req["admin_id"] = admin_id

    await save_state()

    log_activity(
        "auth",
        f"درخواست «{req.get('full_name')}» تایید و حساب ادمین «{username}» ساخته شد",
        "ok",
    )

    delivery_message = (
        f"سلام {req.get('full_name','')} عزیز 👋\n\n"
        f"حساب ادمین شما در VodiWalker فعال شد.\n\n"
        f"نام کاربری: {username}\n"
        f"رمز عبور: {password}\n\n"
        f"از طریق صفحه ورود پنل وارد شوید و رمز خود را در اولین فرصت تغییر دهید."
    )

    return {
        "ok": True,
        "admin": _admin_public(admin_id, ADMINS[admin_id]),
        "telegram_id": req.get("telegram_id", ""),
        "delivery_message": delivery_message,
    }


@app.post("/api/admin-requests/{req_id}/reject")
async def api_reject_admin_request(req_id: str, request: Request, token=Depends(require_owner)):
    req = ADMIN_REQUESTS.get(req_id)
    if not req:
        raise HTTPException(status_code=404, detail="درخواست یافت نشد")
    if req.get("status") != "pending":
        raise HTTPException(status_code=409, detail="این درخواست قبلاً بررسی شده است")

    try:
        body = await request.json()
    except Exception:
        body = {}

    reason = str((body or {}).get("reason", "")).strip()[:300]

    req["status"] = "rejected"
    req["decided_at"] = datetime.now().isoformat()
    req["note"] = reason or req.get("note", "")

    await save_state()

    log_activity("auth", f"درخواست ادمینی «{req.get('full_name')}» رد شد", "warn")

    return {"ok": True}


@app.delete("/api/admin-requests/{req_id}")
async def api_delete_admin_request(req_id: str, token=Depends(require_owner)):
    if req_id not in ADMIN_REQUESTS:
        raise HTTPException(status_code=404, detail="درخواست یافت نشد")
    ADMIN_REQUESTS.pop(req_id, None)
    await save_state()
    return {"ok": True}


# ============================================================
# BOT CONTROL CENTER
@app.get("/api/bot/texts")
async def api_bot_texts(token=Depends(require_owner)):
    return {"ok": True, "texts": BOT_TEXTS}

@app.post("/api/bot/texts")
async def api_bot_texts_save(request: Request, token=Depends(require_owner)):
    if BOT_TEXTS_LOCKED:
        raise HTTPException(status_code=403, detail=BOT_TEXTS_LOCKED_MSG)
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")
    texts = body.get("texts") if isinstance(body, dict) else None
    if not isinstance(texts, dict):
        raise HTTPException(status_code=400, detail="ساختار متن‌ها نامعتبر است")
    for key in list(BOT_TEXTS):
        if key in texts:
            BOT_TEXTS[key] = str(texts[key])[:4000]
    await save_state()
    log_activity("bot", "متن‌های ربات از پنل بروزرسانی شد", "ok")
    return {"ok": True, "texts": BOT_TEXTS}

# PANEL SETTINGS (آدرس عمومی پنل + مدیریت ربات تلگرام از داخل پنل)
# ============================================================

@app.get("/api/settings")
async def api_get_settings(request: Request, token=Depends(require_owner)):
    bot_cfg = _bot_settings_snapshot()
    override_scheme, override_host = _split_base_url(CONFIG.get("public_base_url"))
    return {
        "ok": True,
        "public_base_url": CONFIG.get("public_base_url", ""),
        "effective_host": get_host(request),
        "effective_scheme": get_scheme(),
        "tcp_public_host": CONFIG.get("tcp_public_host", ""),
        "tcp_public_port": CONFIG.get("tcp_public_port", ""),
        "tcp_listen_port": _tcp_listen_port_snapshot(),
        "bot_token": bot_cfg.get("bot_token", ""),
        "bot_admin_ids": bot_cfg.get("admin_ids", ""),
        "bot_running": bot_cfg.get("running", False),
        "bot_texts_locked": BOT_TEXTS_LOCKED,
        "bot_auto_start": bool(CONFIG.get("bot_auto_start", False)),
        "admin_username": AUTH.get("username", DEFAULT_ADMIN_USERNAME),
        "sub_remark_show_name": bool(CONFIG.get("sub_remark_show_name", True)),
        "sub_remark_show_volume": bool(CONFIG.get("sub_remark_show_volume", False)),
        "sub_remark_show_id": bool(CONFIG.get("sub_remark_show_id", False)),
        "sub_remark_show_inbound": bool(CONFIG.get("sub_remark_show_inbound", False)),
        "sub_info_line_enabled": bool(CONFIG.get("sub_info_line_enabled", True)),
        "sub_info_line_show_volume": bool(CONFIG.get("sub_info_line_show_volume", True)),
        "sub_info_line_show_expiry": bool(CONFIG.get("sub_info_line_show_expiry", True)),
        "support_username": _clean_tg_username(CONFIG.get("support_username")),
        "channel_username": _clean_tg_username(CONFIG.get("channel_username")),
        "name_style_enabled": bool(CONFIG.get("name_style_enabled", True)),
    }


@app.post("/api/settings")
async def api_update_settings(request: Request, token=Depends(require_owner)):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    bot_settings_changed = False

    if "public_base_url" in body:
        raw = str(body.get("public_base_url") or "").strip()
        # اعتبارسنجی سبک: اگه چیزی وارد شده، باید حداقل یک هاست معتبر ازش دربیاد
        if raw:
            _, parsed_host = _split_base_url(raw)
            if not parsed_host:
                raise HTTPException(status_code=400, detail="آدرس عمومی نامعتبر است (مثال درست: https://panel.example.com)")
        CONFIG["public_base_url"] = raw

    if "bot_auto_start" in body:
        CONFIG["bot_auto_start"] = bool(body.get("bot_auto_start"))

    if "tcp_public_host" in body:
        CONFIG["tcp_public_host"] = str(body.get("tcp_public_host") or "").strip()

    if "tcp_public_port" in body:
        raw_port = str(body.get("tcp_public_port") or "").strip()
        if raw_port and not raw_port.isdigit():
            raise HTTPException(status_code=400, detail="پورت عمومی TCP باید عدد باشد")
        CONFIG["tcp_public_port"] = raw_port

    if "support_username" in body:
        value = _clean_tg_username(body.get("support_username"))
        if value and not _TG_USER_RE.match(value):
            raise HTTPException(status_code=400, detail="آیدی تلگرام معتبر نیست (۵ تا ۳۲ کاراکتر: حروف انگلیسی، عدد و _ ؛ مثال: @MySupport)")
        CONFIG["support_username"] = value

    if "channel_username" in body:
        value = _clean_tg_username(body.get("channel_username"))
        if value and not _TG_USER_RE.match(value):
            raise HTTPException(status_code=400, detail="آیدی کانال معتبر نیست (مثال: @MyChannel)")
        CONFIG["channel_username"] = value

    for flag in (
        "name_style_enabled",
        "sub_remark_show_name", "sub_remark_show_volume", "sub_remark_show_id", "sub_remark_show_inbound",
        "sub_info_line_enabled", "sub_info_line_show_volume", "sub_info_line_show_expiry",
    ):
        if flag in body:
            CONFIG[flag] = bool(body.get(flag))

    try:
        import telegram_bot

        if "bot_token" in body or "bot_admin_ids" in body:
            new_token = body.get("bot_token")
            new_admin_ids = body.get("bot_admin_ids")
            telegram_bot.configure(
                token=(str(new_token).strip() if new_token is not None else None),
                admin_ids_raw=(str(new_admin_ids).strip() if new_admin_ids is not None else None),
            )
            bot_settings_changed = True
    except HTTPException:
        raise
    except Exception as exc:
        logger.warning("Bot configure error: %s", exc)

    await save_state()

    # اگه ربات از قبل روشن بوده و توکن/آیدی‌ها عوض شده، برای اعمال شدنِ واقعی
    # باید دوباره راه‌اندازی بشه (وگرنه با کانکشن قدیمی به توکن قبلی وصل می‌مونه)
    restarted = False
    try:
        import telegram_bot
        if bot_settings_changed and telegram_bot.is_running():
            await telegram_bot.restart_bot()
            restarted = True
    except Exception as exc:
        logger.warning("Bot restart error: %s", exc)

    log_activity("system", "تنظیمات پنل (آدرس عمومی/ربات) به‌روزرسانی شد", "ok")

    return {"ok": True, "bot_restarted": restarted, **_bot_settings_snapshot()}


@app.post("/api/settings/bot/start")
async def api_bot_start(token=Depends(require_owner)):
    try:
        import telegram_bot
        await telegram_bot.start_bot()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"خطا در روشن کردن ربات: {exc}")
    log_activity("system", "ربات تلگرام از داخل پنل روشن شد", "ok")
    return {"ok": True, **_bot_settings_snapshot()}


@app.post("/api/settings/bot/stop")
async def api_bot_stop(token=Depends(require_owner)):
    try:
        import telegram_bot
        await telegram_bot.stop_bot()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"خطا در خاموش کردن ربات: {exc}")
    log_activity("system", "ربات تلگرام از داخل پنل خاموش شد", "warn")
    return {"ok": True, **_bot_settings_snapshot()}


# ============================================================
# ADVANCED REPORTING
# ============================================================

@app.get("/api/reports/summary")
async def api_reports_summary(request: Request, token=Depends(require_auth)):
    days = safe_int(request.query_params.get("days"), default=14, minimum=1, maximum=180)

    today = datetime.now(IRAN_TZ) if IRAN_TZ else datetime.now()
    date_keys = [
        (today - timedelta(days=offset)).strftime("%Y-%m-%d")
        for offset in range(days - 1, -1, -1)
    ]

    series = []
    for key in date_keys:
        bucket = DAILY_STATS.get(key, {})
        series.append({
            "date": key,
            "traffic_mb": round(bucket.get("traffic_bytes", 0) / (1024 ** 2), 2),
            "new_links": bucket.get("new_links", 0),
        })

    now_ts = time.time()
    active_links = 0
    expired_links = 0
    unlimited_links = 0
    protocol_counts = defaultdict(int)
    top_links = []

    for uid, link in LINKS.items():
        protocol_counts[protocol_display_label(link)] += 1

        expires_at = link.get("expires_at")
        is_expired = False
        if expires_at:
            try:
                is_expired = datetime.fromisoformat(expires_at).timestamp() < now_ts
            except Exception:
                is_expired = False

        if is_expired:
            expired_links += 1
        else:
            active_links += 1

        if not link.get("limit_bytes"):
            unlimited_links += 1

        top_links.append({
            "uid": uid,
            "label": link.get("label", ""),
            "used_bytes": link.get("used_bytes", 0),
            "limit_bytes": link.get("limit_bytes", 0),
            "protocol": link.get("protocol", DEFAULT_PROTOCOL),
        })

    top_links.sort(key=lambda x: x["used_bytes"], reverse=True)

    return {
        "ok": True,
        "series": series,
        "totals": {
            "links": len(LINKS),
            "active_links": active_links,
            "expired_links": expired_links,
            "unlimited_links": unlimited_links,
            "subs": len(SUBS),
            "admins": len(ADMINS) + 1,
        },
        "protocol_distribution": [
            {"protocol": proto, "count": count} for proto, count in protocol_counts.items()
        ],
        "top_links": top_links[:10],
    }


@app.get("/api/reports/export.csv")
async def api_reports_export_csv(token=Depends(require_auth)):
    lines = ["uid,label,protocol,used_bytes,limit_bytes,expires_at,created_at"]

    for uid, link in LINKS.items():
        row = [
            uid,
            str(link.get("label", "")).replace(",", " "),
            link.get("protocol", DEFAULT_PROTOCOL),
            str(link.get("used_bytes", 0)),
            str(link.get("limit_bytes", 0)),
            str(link.get("expires_at", "") or ""),
            str(link.get("created_at", "") or ""),
        ]
        lines.append(",".join(row))

    csv_content = "\n".join(lines)

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=vodiwalker-links-report.csv"},
    )


# ============================================================
# GLOBAL ERROR HANDLER
# ============================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):

    stats[
        "total_errors"
    ] += 1

    error_logs.append(
        {
            "error": str(exc) or "internal server error",
            "path": str(request.url.path),
            "method": request.method,
            "source": "server",
            "level": "err",
            "time": datetime.now().isoformat(),
        }
    )

    logger.exception(
        "Unhandled exception: %s %s",
        request.method,
        request.url,
    )

    # API requests
    if (
        request.url.path.startswith(
            "/api/"
        )
        or request.url.path == "/stats"
    ):

        return JSONResponse(
            {
                "ok": False,
                "error":
                    str(exc)
                or "internal server error",
            },
            status_code=500,
        )

    return HTMLResponse(
        """
        <html lang="fa" dir="rtl">
        <body style="
            background:#07070a;
            color:#fff;
            font-family:sans-serif;
            padding:40px;
        ">
            <h2>
            خطای داخلی VodiWalker
            </h2>

            <p>
            لطفاً لاگ Railway را بررسی کنید.
            </p>
        </body>
        </html>
        """,
        status_code=500,
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        log_level="info",
        workers=1,
    )
