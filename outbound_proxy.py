# outbound_proxy.py  —  v2 (Pro Scanner)
import asyncio
import ipaddress
import json
import os
import re
import secrets
import socket
import ssl
import time
from datetime import datetime
from urllib.parse import quote, unquote, urljoin, urlparse

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request

from main import (
    DATA_DIR,
    LINKS,
    LINKS_LOCK,
    logger,
    log_activity,
    require_auth,
    safe_int,
    save_state,
    get_session_info,
    SESSION_COOKIE,
    NODE_API_TOKEN_MARK,
)

PROXIES_FILE = DATA_DIR / "vodiwalker_proxies.json"
PROXIES_LOCK = asyncio.Lock()
PROXIES: dict = {}


def _env_int(name: str, default: int, lo: int, hi: int) -> int:
    try:
        return max(lo, min(hi, int(os.environ.get(name, default))))
    except (TypeError, ValueError):
        return default


def _env_flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


GEOIP_TIMEOUT = 6.0
TCP_PING_TIMEOUT = 5.0
PROBE_TIMEOUT = 10.0

# هدف‌های تست (از داخل تونل). همه قابل تغییرند (برای تست/محیط‌های خاص).
LATENCY_TARGET = ("cp.cloudflare.com", 80)           # پینگ = handshake پراکسی + اتصال پراکسی→Cloudflare
TLS_TARGET = ("www.cloudflare.com", 443)             # بررسی رهگیری TLS با تایید گواهی
SPEED_TARGET = ("speed.cloudflare.com", 443, "/__down?bytes=1500000")
PROBE_ENDPOINTS = [                                   # (host, port, path, kind) — HTTP ساده
    ("ip-api.com", 80, "/json/?fields=status,message,country,countryCode,regionName,city,isp,org,as,hosting,proxy,mobile,query", "ipapi"),
    ("ipinfo.io", 80, "/json", "ipinfo"),
]

MAX_PROXIES = 300
FALLBACK_DIRECT = _env_flag("OUTBOUND_FALLBACK_DIRECT")
ALLOW_PRIVATE_TARGETS = _env_flag("SCAN_ALLOW_PRIVATE")

# محدودیت‌های اسکن
SCAN_MAX_TEXT_BYTES = 1_000_000
SCAN_URL_MAX_BYTES = 2_000_000
SCAN_JOB_MAX_CANDIDATES = _env_int("SCAN_JOB_MAX_CANDIDATES", 3000, 50, 20000)
SCAN_DEFAULT_CONCURRENCY = 40
SCAN_MAX_CONCURRENCY = _env_int("SCAN_MAX_CONCURRENCY", 100, 5, 300)
SCAN_MAX_ACTIVE_JOBS = 2
SCAN_JOB_TTL = 1800
SCAN_CAND_HARD_CAP = 45.0        # سقف زمان برای هر کاندید (همه‌ی مراحل)
# سازگاری با نسخه‌ی قبل (endpoint همزمان قدیمی)
SCAN_MAX_CANDIDATES = 60
SCAN_CONCURRENCY = 20
SCAN_TCP_TIMEOUT = 3.0
SCAN_PROBE_TIMEOUT = 6.0

# circuit-breaker روی relay
BREAKER_THRESHOLD = 3
BREAKER_COOLDOWN = 20.0
_BREAKER: dict = {}


def _now_iso() -> str:
    return datetime.now().isoformat()


def _flag_from_country_code(cc: str) -> str:
    cc = (cc or "").strip().upper()
    if len(cc) != 2 or not cc.isalpha():
        return "🏳️"
    base = 0x1F1E6
    return "".join(chr(base + (ord(c) - ord("A"))) for c in cc)


# ══════════════════════════════════════════════════════════════════════════════
# استور
# ══════════════════════════════════════════════════════════════════════════════

def _load_sync():
    try:
        if PROXIES_FILE.exists():
            data = json.loads(PROXIES_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                PROXIES.clear()
                PROXIES.update(data)
    except Exception as exc:
        logger.warning(f"proxy store load failed: {exc}")


def _save_sync():
    PROXIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = PROXIES_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(PROXIES, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(PROXIES_FILE)


def load_proxies():
    _load_sync()


async def save_proxies():
    async with PROXIES_LOCK:
        await asyncio.to_thread(_save_sync)


load_proxies()


def _public(p: dict) -> dict:
    """نسخه‌ی امن برای API/پنل: پسورد هیچ‌وقت به مرورگر برنمی‌گرده."""
    d = dict(p)
    d["has_auth"] = bool(d.get("username"))
    d.pop("password", None)
    d.setdefault("scheme", "socks5")
    return d


def list_proxies() -> list:
    return sorted(PROXIES.values(), key=lambda p: p.get("created_at", ""))


def get_proxy(proxy_id: str):
    return PROXIES.get(proxy_id)


def proxy_summary(proxy_id: str) -> dict | None:
    """خلاصه‌ی کوتاه برای نمایش روی کارت اینباند (نام/کشور/پرچم)."""
    p = PROXIES.get(proxy_id or "")
    if not p:
        return None
    return {
        "id": p.get("id"),
        "name": p.get("name", ""),
        "country": p.get("country", ""),
        "country_code": (p.get("country_code") or "").lower(),
        "flag": p.get("flag", ""),
        "ping_ms": p.get("ping_ms"),
        "test_ok": bool(p.get("test_ok")),
        "scheme": p.get("scheme", "socks5"),
        "score": p.get("score"),
        "grade": p.get("grade", ""),
    }


def proxy_usage_counts() -> dict:
    counts: dict = {}
    for link in LINKS.values():
        pid = link.get("outbound_proxy_id") or ""
        if pid:
            counts[pid] = counts.get(pid, 0) + 1
    return counts


# فیلدهای نتیجه‌ی تست که روی رکورد ذخیره می‌شن (و با تغییر آدرس ریست می‌شن)
_TEST_DEFAULTS = {
    "ping_ms": None, "tcp_ms": None, "exit_ip": "", "country": "", "country_code": "",
    "flag": "", "tested_at": None, "test_ok": False, "test_message": "",
    "score": None, "grade": "", "jitter": None, "loss": None, "tls_state": "",
    "speed_mbps": None, "city": "", "isp": "", "asn": "", "hosting": None,
}


def _build_record(pid: str, data: dict, existing: dict) -> dict:
    host = str(data.get("host") or existing.get("host") or "").strip()[:255]
    port = max(1, min(65535, int(data.get("port") or existing.get("port") or 1080)))
    scheme = _norm_scheme(data.get("scheme") or existing.get("scheme") or "socks5")
    changed = bool(existing) and (
        host != existing.get("host") or port != existing.get("port")
        or scheme != existing.get("scheme", "socks5")
    )
    record = {
        "id": pid,
        "name": str(data.get("name") or existing.get("name") or "پراکسی جدید").strip()[:80],
        "host": host,
        "port": port,
        "scheme": scheme,
        "username": str(data.get("username") if data.get("username") is not None else existing.get("username", "") or "").strip()[:120],
        "password": str(data.get("password") if data.get("password") is not None else existing.get("password", "") or "").strip()[:200],
        "created_at": existing.get("created_at") or _now_iso(),
    }
    for k, dv in _TEST_DEFAULTS.items():
        record[k] = dv if changed else existing.get(k, dv)
    return record


async def upsert_proxy(proxy_id: str | None, data: dict) -> dict:
    pid = proxy_id or secrets.token_urlsafe(8)
    record = _build_record(pid, data, PROXIES.get(pid, {}))
    PROXIES[pid] = record
    await save_proxies()
    return record


async def delete_proxy(proxy_id: str) -> int:
    """پراکسی رو حذف می‌کنه و از همه‌ی کانفیگ‌هایی که ازش استفاده می‌کردن جدا می‌کنه
    (برمی‌گردن به مستقیم). تعداد کانفیگ‌های تغییرکرده رو برمی‌گردونه."""
    PROXIES.pop(proxy_id, None)
    _BREAKER.pop(proxy_id, None)
    await save_proxies()
    changed = 0
    async with LINKS_LOCK:
        for link in LINKS.values():
            if link.get("outbound_proxy_id") == proxy_id:
                link["outbound_proxy_id"] = ""
                changed += 1
    if changed:
        await save_state()
    return changed


# ══════════════════════════════════════════════════════════════════════════════
# پارس ورودی
# ══════════════════════════════════════════════════════════════════════════════
_SCHEME_ALIASES = {
    "socks5": "socks5", "socks5h": "socks5", "socks": "socks5",
    "socks4": "socks4", "socks4a": "socks4",
    "http": "http",
}
_DEFAULT_PORTS = {"socks5": 1080, "socks4": 1080, "http": 8080, "auto": 1080}
_HOST_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9\.\-]{0,251}[A-Za-z0-9])?$")


def _norm_scheme(s, default: str = "socks5") -> str:
    s = str(s or "").strip().lower().rstrip(":/")
    return _SCHEME_ALIASES.get(s, default)


def _valid_host(host: str) -> bool:
    if not host:
        return False
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return bool(_HOST_RE.match(host)) and ".." not in host


def parse_candidate(line: str, default_scheme: str = "socks5") -> dict | None:
    """یک خط ورودی → {scheme, host, port, username, password}.
    فرمت‌ها: host | host:port | host:port:user:pass | user:pass@host:port |
             scheme://[user:pass@]host:port | [ipv6]:port
    scheme یکی از socks5/socks5h/socks4/socks4a/http؛ پیش‌فرض همون default_scheme
    (می‌تونه «auto» باشه). متن بعد از فاصله (مثل کد کشور) نادیده گرفته می‌شه."""
    line = (line or "").strip()
    if not line or line.startswith(("#", "//", ";")):
        return None
    token = line.split()[0].strip(",;\"'")
    if not token:
        return None
    scheme = default_scheme if default_scheme == "auto" else _norm_scheme(default_scheme)
    m = re.match(r"^([A-Za-z0-9]+)://(.*)$", token)
    if m:
        sc = m.group(1).lower()
        if sc not in _SCHEME_ALIASES:
            return None
        scheme, rest = _SCHEME_ALIASES[sc], m.group(2)
    else:
        rest = token
    rest = rest.split("/", 1)[0]
    username = password = ""
    if "@" in rest:
        cred, _, rest = rest.rpartition("@")
        username, _, password = cred.partition(":")
        username, password = unquote(username), unquote(password)
    host, port = "", None
    if rest.startswith("["):
        end = rest.find("]")
        if end < 0:
            return None
        host, tail = rest[1:end], rest[end + 1:]
        if tail.startswith(":"):
            port = tail[1:]
        elif tail:
            return None
    else:
        parts = rest.split(":")
        if len(parts) == 1:
            host = parts[0]
        elif len(parts) == 2:
            host, port = parts
        elif len(parts) == 4 and not username:
            host, port, username, password = parts
        else:
            return None
    if port in (None, ""):
        port = _DEFAULT_PORTS.get(scheme, 1080)
    elif str(port).strip().isdigit():
        port = int(port)
    else:
        return None
    host = host.strip()
    if not (1 <= port <= 65535) or not _valid_host(host):
        return None
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if "." not in host:      # «junk»، «ss» و کلمه‌های ساده آدرس پراکسی نیستند
            return None
    return {"scheme": scheme, "host": host, "port": port,
            "username": username.strip(), "password": password.strip()}


def parse_proxy_line(line: str):
    """سازگاری با نسخه‌ی قبل: (host, port, username, password) یا None."""
    c = parse_candidate(line, "socks5")
    return (c["host"], c["port"], c["username"], c["password"]) if c else None


def _parse_host_input(host: str, port, username: str, password: str):
    """کاربرها معمولاً کل آدرس رو پیست می‌کنن؛ (host, port, username, password, scheme|'')."""
    raw = (host or "").strip()
    c = parse_candidate(raw, "socks5") if raw else None
    scheme = ""
    if c:
        has_scheme = "://" in raw
        scheme = c["scheme"] if has_scheme else ""
        host = c["host"]
        if ":" in raw.split("://", 1)[-1].rpartition("@")[2] or has_scheme or raw.count(":") in (1, 3):
            port = c["port"]
        username = c["username"] or username
        password = c["password"] or password
    return host, port, username, password, scheme


def _ip_not_public(ip) -> bool:
    return (not ip.is_global) or ip.is_multicast


async def _host_is_blocked(host: str) -> bool:
    """جلوگیری از SSRF: آدرس‌های لوکال/خصوصی/link-local تست نمی‌شن."""
    if ALLOW_PRIVATE_TARGETS:
        return False
    try:
        return _ip_not_public(ipaddress.ip_address(host))
    except ValueError:
        pass
    try:
        loop = asyncio.get_running_loop()
        infos = await asyncio.wait_for(loop.getaddrinfo(host, None, type=socket.SOCK_STREAM), 4.0)
    except Exception:
        return False   # حل نشد → خودش به‌عنوان «مرده» گزارش می‌شه
    for info in infos:
        try:
            if _ip_not_public(ipaddress.ip_address(info[4][0].split("%")[0])):
                return True
        except ValueError:
            continue
    return False


# ══════════════════════════════════════════════════════════════════════════════
# موتور تست
# ══════════════════════════════════════════════════════════════════════════════

def _make_socks_proxy(proxy: dict):
    """نکته: Proxy.from_url(url, username=..., password=...) در python-socks خطای
    «multiple values for argument 'username'» می‌ده؛ پس مستقیم با create می‌سازیم.
    rdns=True یعنی DNS مقصد روی خود پراکسی resolve بشه (نه روی سرور پنل).
    نوع پراکسی از فیلد scheme می‌آد (socks5 | socks4 | http)."""
    from python_socks import ProxyType
    from python_socks.async_.asyncio import Proxy

    ptype = {"socks5": ProxyType.SOCKS5, "socks4": ProxyType.SOCKS4, "http": ProxyType.HTTP}[
        _norm_scheme(proxy.get("scheme") or "socks5")
    ]
    return Proxy.create(
        proxy_type=ptype,
        host=proxy["host"],
        port=int(proxy["port"]),
        username=(proxy.get("username") or None),
        password=(proxy.get("password") or None),
        rdns=True,
    )


async def _tunnel(c: dict, host: str, port: int, timeout: float):
    px = _make_socks_proxy(c)
    return await asyncio.wait_for(px.connect(dest_host=host, dest_port=port, timeout=timeout), timeout=timeout + 1.0)


def _close_sock(sock):
    try:
        sock.close()
    except Exception:
        pass


async def _tcp_ping(host: str, port: int, timeout: float = TCP_PING_TIMEOUT):
    started = time.perf_counter()
    try:
        _, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        return True, round((time.perf_counter() - started) * 1000, 1), ""
    except asyncio.TimeoutError:
        return False, None, "Timeout: پراکسی در زمان تعیین‌شده پاسخ نداد."
    except Exception as exc:
        return False, None, f"اتصال ناموفق: {type(exc).__name__}: {str(exc)[:180]}"


_STATUS_TEXT = {
    "dead": "پراکسی در دسترس نیست (اتصال رد شد)",
    "timeout": "زمان اتصال تمام شد",
    "auth": "احراز هویت ناموفق (نام کاربری/رمز را چک کن)",
    "handshake": "پروتکل اشتباه است یا پراکسی اتصال به مقصد را نپذیرفت",
    "error": "خطای نامشخص",
}


def _classify(exc: BaseException) -> str:
    """نوع خطای تونل: dead | timeout | auth | handshake | error"""
    try:
        from python_socks import ProxyConnectionError, ProxyError, ProxyTimeoutError
    except Exception:  # pragma: no cover
        ProxyConnectionError = ProxyError = ProxyTimeoutError = ()  # type: ignore
    txt = str(exc).lower()
    if isinstance(exc, (asyncio.TimeoutError, TimeoutError)) or (ProxyTimeoutError and isinstance(exc, ProxyTimeoutError)):
        return "timeout"
    if "auth" in txt or "password" in txt or "407" in txt or "credential" in txt:
        return "auth"
    if ProxyConnectionError and isinstance(exc, ProxyConnectionError):
        return "dead"
    if ProxyError and isinstance(exc, ProxyError):
        return "handshake"
    if isinstance(exc, OSError):
        return "dead"
    return "error"


def _is_proxy_down(exc: BaseException) -> bool:
    """فقط خطاهایی که تقصیر خود پراکسی‌اند (نه مقصدِ خراب) به breaker شمرده می‌شن."""
    return _classify(exc) in ("dead", "auth")


def _json_from_body(body: bytes):
    text = body.decode("utf-8", errors="ignore")
    a, b = text.find("{"), text.rfind("}")
    if a == -1 or b <= a:
        return None
    try:
        return json.loads(text[a:b + 1])
    except ValueError:
        return None


async def _http_get(sock, host: str, path: str, timeout: float, limit: int = 16384):
    """GET ساده روی سوکتِ تونل. (status_code, body_bytes) برمی‌گردونه."""
    try:
        reader, writer = await asyncio.open_connection(sock=sock)
    except Exception:
        _close_sock(sock)
        raise
    buf = b""
    try:
        writer.write(
            f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: VodiWalker-Scanner/2\r\n"
            f"Accept: application/json\r\nConnection: close\r\n\r\n".encode()
        )
        await writer.drain()

        async def _read():
            nonlocal buf
            while len(buf) < limit:
                chunk = await reader.read(4096)
                if not chunk:
                    break
                buf += chunk

        try:
            await asyncio.wait_for(_read(), timeout)
        except asyncio.TimeoutError:
            pass
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
    head, _, body = buf.partition(b"\r\n\r\n")
    m = re.match(rb"HTTP/\d\.\d\s+(\d{3})", head)
    return (int(m.group(1)) if m else 0), body


def _normalize_geo(kind: str, data) -> dict | None:
    if not isinstance(data, dict):
        return None
    if kind == "ipapi":
        if data.get("status") != "success":
            return None
        return {
            "exit_ip": data.get("query", "") or "", "country": data.get("country", "") or "",
            "country_code": data.get("countryCode", "") or "", "city": data.get("city", "") or "",
            "isp": data.get("isp", "") or data.get("org", "") or "",
            "asn": (data.get("as", "") or "").split(" ")[0],
            "hosting": bool(data.get("hosting")) if "hosting" in data else None,
        }
    if kind == "ipinfo":
        if not data.get("ip"):
            return None
        org = str(data.get("org", "") or "")
        asn, _, name = org.partition(" ")
        return {
            "exit_ip": data.get("ip", ""), "country": data.get("country", "") or "",
            "country_code": data.get("country", "") or "", "city": data.get("city", "") or "",
            "isp": name or org, "asn": asn if asn.upper().startswith("AS") else "", "hosting": None,
        }
    return None


async def _geo_probe(c: dict, timeout: float) -> dict | None:
    """IP/کشور/ISP «خروجی» (چیزی که سایت‌ها می‌بینن) از داخل تونل."""
    for host, port, path, kind in PROBE_ENDPOINTS:
        try:
            sock = await _tunnel(c, host, port, timeout)
            code, body = await _http_get(sock, host, path, timeout)
            if code != 200:
                continue
            geo = _normalize_geo(kind, _json_from_body(body))
            if geo:
                return geo
        except Exception:
            continue
    return None


def _tls_context() -> ssl.SSLContext:
    return ssl.create_default_context()


async def _tls_check(c: dict, timeout: float) -> tuple:
    """(state, ms): clean = گواهی واقعی تایید شد | intercepted = رهگیری TLS (MITM) |
    blocked = پراکسی اتصال ۴۴۳ / TLS را اجازه نداد."""
    try:
        sock = await _tunnel(c, TLS_TARGET[0], TLS_TARGET[1], timeout)
    except Exception:
        return "blocked", None
    started = time.perf_counter()
    writer = None
    try:
        _, writer = await asyncio.open_connection(
            sock=sock, ssl=_tls_context(), server_hostname=TLS_TARGET[0], ssl_handshake_timeout=timeout,
        )
        return "clean", round((time.perf_counter() - started) * 1000, 1)
    except ssl.SSLCertVerificationError:
        return "intercepted", None
    except ssl.SSLError as exc:
        return ("intercepted" if "CERTIFICATE_VERIFY_FAILED" in str(exc) else "blocked"), None
    except Exception:
        _close_sock(sock)
        return "blocked", None
    finally:
        if writer is not None:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass


async def _speed_test(c: dict, timeout: float):
    """سرعت دانلود (Mbps) از داخل تونل؛ None اگه داده‌ی کافی نیومد."""
    host, port, path = SPEED_TARGET
    sock = await _tunnel(c, host, port, timeout)
    writer = None
    try:
        reader, writer = await asyncio.open_connection(
            sock=sock, ssl=_tls_context(), server_hostname=host, ssl_handshake_timeout=timeout,
        )
        writer.write(f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: VodiWalker-Scanner/2\r\nConnection: close\r\n\r\n".encode())
        await writer.drain()
        data = b""
        while b"\r\n\r\n" not in data and len(data) < 65536:
            chunk = await asyncio.wait_for(reader.read(8192), timeout)
            if not chunk:
                return None
            data += chunk
        body = len(data) - data.index(b"\r\n\r\n") - 4
        t0 = time.perf_counter()
        deadline = t0 + 8.0
        while time.perf_counter() < deadline:
            try:
                chunk = await asyncio.wait_for(reader.read(65536), max(0.5, deadline - time.perf_counter()))
            except asyncio.TimeoutError:
                break
            if not chunk:
                break
            body += len(chunk)
        elapsed = max(time.perf_counter() - t0, 0.001)
        if body < 50_000:
            return None
        return round(body * 8 / elapsed / 1e6, 2)
    finally:
        if writer is not None:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        else:
            _close_sock(sock)


def _score(r: dict) -> int:
    """امتیاز ۰..۱۰۰: تاخیر ۳۵ | پایداری(loss+jitter) ۲۵ | TLS ۱۵ | جغرافیا ۱۰ | سرعت ۱۵"""
    if not r.get("ok"):
        return 0
    avg = r.get("ping_ms") or 9999
    lat = 35 if avg <= 120 else 30 if avg <= 250 else 22 if avg <= 500 else 12 if avg <= 900 else 4
    loss = (r.get("loss") or 0) / 100.0
    jit = r.get("jitter") or 0
    stab = max(0.0, 25 * (1 - loss * 1.5) - min(10.0, jit / 40.0))
    tls = {"clean": 15, "": 8, None: 8, "blocked": 3, "intercepted": 0}.get(r.get("tls_state"), 8)
    geo = 10 if r.get("country_code") else 3
    mbps = r.get("speed_mbps")
    spd = 8 if mbps is None else min(15.0, mbps * 1.5)
    total = lat + stab + tls + geo + spd
    if r.get("tls_state") == "intercepted":
        total = min(total, 25)
    return int(max(0, min(100, round(total))))


def _grade(score: int, ok: bool) -> str:
    if not ok:
        return "F"
    return "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 50 else "D"


def _blank_result(c: dict) -> dict:
    return {
        "key": f"{c['scheme']}://{c['host']}:{c['port']}",
        "scheme": c["scheme"], "host": c["host"], "port": c["port"],
        "username": c.get("username", ""), "password": c.get("password", ""),
        "ok": False, "status": "error", "message": "",
        "tcp_ms": None, "ping_ms": None, "ping_min": None, "jitter": None, "loss": None,
        "tls_state": "", "speed_mbps": None,
        "exit_ip": "", "country": "", "country_code": "", "flag": "", "city": "", "isp": "", "asn": "",
        "hosting": None, "geo_source": "", "score": 0, "grade": "F", "tested_at": _now_iso(),
    }


async def probe_candidate(
    c: dict, *, samples: int = 3, check_tls: bool = True, check_speed: bool = False,
    tcp_timeout: float = SCAN_TCP_TIMEOUT, probe_timeout: float = SCAN_PROBE_TIMEOUT,
) -> dict:
    """تست کامل یک پراکسی. c = {scheme(socks5|socks4|http|auto), host, port, username, password}"""
    r = _blank_result(c)
    samples = max(1, min(5, int(samples)))

    tcp_ok, tcp_ms, tcp_msg = await _tcp_ping(c["host"], c["port"], tcp_timeout)
    r["tcp_ms"] = tcp_ms
    if not tcp_ok:
        r.update(status="dead", message=tcp_msg or _STATUS_TEXT["dead"])
        return r

    # ۱) تشخیص پروتکل + اولین نمونه‌ی پینگ
    schemes = ["socks5", "http", "socks4"] if c["scheme"] == "auto" else [c["scheme"]]
    working, lat, kinds = None, [], []
    for sc in schemes:
        cc = {**c, "scheme": sc}
        t0 = time.perf_counter()
        try:
            sock = await _tunnel(cc, LATENCY_TARGET[0], LATENCY_TARGET[1], probe_timeout)
            lat.append((time.perf_counter() - t0) * 1000)
            _close_sock(sock)
            working = cc
            break
        except Exception as exc:
            kinds.append(_classify(exc))
    if not working:
        kind = "auth" if "auth" in kinds else "handshake" if "handshake" in kinds else (kinds[0] if kinds else "error")
        r.update(status=kind, message=_STATUS_TEXT.get(kind, _STATUS_TEXT["error"]))
        return r
    r["scheme"] = working["scheme"]
    r["key"] = f"{r['scheme']}://{r['host']}:{r['port']}"

    # ۲) نمونه‌های بعدی پینگ → avg / jitter / loss
    fails = 0
    for _ in range(samples - 1):
        await asyncio.sleep(0.04)
        t0 = time.perf_counter()
        try:
            sock = await _tunnel(working, LATENCY_TARGET[0], LATENCY_TARGET[1], probe_timeout)
            lat.append((time.perf_counter() - t0) * 1000)
            _close_sock(sock)
        except Exception:
            fails += 1
    r["ping_ms"] = round(sum(lat) / len(lat), 1)
    r["ping_min"] = round(min(lat), 1)
    r["jitter"] = round(sum(abs(a - b) for a, b in zip(lat, lat[1:])) / (len(lat) - 1), 1) if len(lat) > 1 else 0.0
    r["loss"] = round(fails / samples * 100, 1)

    # ۳) جغرافیا + TLS موازی
    tasks = [_geo_probe(working, probe_timeout)]
    if check_tls:
        tasks.append(_tls_check(working, probe_timeout))
    out = await asyncio.gather(*tasks, return_exceptions=True)
    geo = out[0] if not isinstance(out[0], BaseException) else None
    if geo:
        cc_ = geo.get("country_code", "")
        r.update(
            exit_ip=geo["exit_ip"], country=geo["country"] or cc_, country_code=cc_,
            flag=_flag_from_country_code(cc_) if cc_ else "🏳️", city=geo["city"], isp=geo["isp"],
            asn=geo["asn"], hosting=geo["hosting"], geo_source="exit",
        )
    if check_tls and len(out) > 1 and not isinstance(out[1], BaseException):
        r["tls_state"] = out[1][0]

    # ۴) سرعت (اختیاری)
    if check_speed:
        try:
            r["speed_mbps"] = await _speed_test(working, probe_timeout + 4)
        except Exception:
            r["speed_mbps"] = None

    r["ok"] = True
    r["status"] = "risky" if r["tls_state"] == "intercepted" else "ok"
    r["score"] = _score(r)
    r["grade"] = _grade(r["score"], True)
    bits = [f"{r['scheme'].upper()} سالم", f"{round(r['ping_ms'])}ms"]
    if r["exit_ip"]:
        bits.append(f"IP خروجی {r['exit_ip']}")
    if r["tls_state"] == "intercepted":
        bits.append("⚠ رهگیری TLS (ناامن)")
    elif r["tls_state"] == "blocked":
        bits.append("پورت ۴۴۳ مسدود")
    r["message"] = " · ".join(bits)
    return r


async def _probe_via_socks(proxy: dict, timeout: float = PROBE_TIMEOUT) -> dict:
    """سازگاری با نسخه‌ی قبل: {connect_ms, geo(ip-api style)}."""
    t0 = time.perf_counter()
    sock = await _tunnel(proxy, PROBE_ENDPOINTS[0][0], 80, timeout)
    connect_ms = round((time.perf_counter() - t0) * 1000, 1)
    code, body = await _http_get(sock, PROBE_ENDPOINTS[0][0], PROBE_ENDPOINTS[0][2], timeout)
    data = _json_from_body(body) if code == 200 else None
    return {"connect_ms": connect_ms, "geo": data if data and data.get("status") == "success" else None}


async def _geo_lookup_host(host: str) -> dict | None:
    """پشتیبان: اگه از داخل تونل کشور معلوم نشد، کشور «آدرس ورودی» پراکسی رو می‌گیریم."""
    async with httpx.AsyncClient(timeout=GEOIP_TIMEOUT) as client:
        try:
            r = await client.get(f"http://ip-api.com/json/{host}?fields=status,country,countryCode,query")
            j = r.json()
            if j.get("status") == "success":
                return j
        except Exception as exc:
            logger.warning(f"geoip(ip-api) failed for {host}: {exc}")
        try:
            r = await client.get(f"https://ipwho.is/{host}")
            j = r.json()
            if j.get("success"):
                return {"country": j.get("country", ""), "countryCode": j.get("country_code", ""), "query": j.get("ip", "")}
        except Exception as exc:
            logger.warning(f"geoip(ipwho) failed for {host}: {exc}")
    return None


def _apply_result(record: dict, r: dict) -> dict:
    """نتیجه‌ی تست رو روی رکورد ذخیره‌شده می‌نشونه."""
    ok = bool(r.get("ok"))
    rs = r.get("scheme")
    record.update({
        "scheme": rs if rs in ("socks5", "socks4", "http") else (record.get("scheme") or "socks5"),
        "ping_ms": r.get("ping_ms") if ok else None,
        "tcp_ms": r.get("tcp_ms"),
        "exit_ip": r.get("exit_ip", "") or "",
        "country": r.get("country") or record.get("country", ""),
        "country_code": r.get("country_code") or record.get("country_code", ""),
        "flag": r.get("flag") or record.get("flag", ""),
        "city": r.get("city", "") or "",
        "isp": r.get("isp", "") or "",
        "asn": r.get("asn", "") or "",
        "hosting": r.get("hosting"),
        "score": r.get("score") if ok else 0,
        "grade": r.get("grade", "F") if ok else "F",
        "jitter": r.get("jitter"),
        "loss": r.get("loss"),
        "tls_state": r.get("tls_state", ""),
        "speed_mbps": r.get("speed_mbps"),
        "tested_at": r.get("tested_at") or _now_iso(),
        "test_ok": ok,
        "test_message": r.get("message", ""),
    })
    return record


async def test_proxy(proxy_id: str, *, samples: int = 3, check_tls: bool = True, check_speed: bool = False) -> dict:
    """تست عمیق یک پراکسی ذخیره‌شده؛ نتیجه در استور ذخیره می‌شه."""
    proxy = PROXIES.get(proxy_id)
    if not proxy:
        raise ValueError("پراکسی پیدا نشد")
    cand = {
        "scheme": _norm_scheme(proxy.get("scheme") or "socks5"), "host": proxy["host"], "port": int(proxy["port"]),
        "username": proxy.get("username", ""), "password": proxy.get("password", ""),
    }
    r = await probe_candidate(
        cand, samples=samples, check_tls=check_tls, check_speed=check_speed,
        tcp_timeout=TCP_PING_TIMEOUT, probe_timeout=PROBE_TIMEOUT,
    )
    if r["ok"] and not r["country_code"]:
        geo = await _geo_lookup_host(proxy["host"])
        if geo:
            r["country"] = geo.get("country", "") or ""
            r["country_code"] = geo.get("countryCode", "") or ""
            r["flag"] = _flag_from_country_code(r["country_code"]) if r["country_code"] else ""
            r["message"] += " (کشور از روی آدرس پراکسی حدس زده شد)"
            r["score"] = _score(r)
            r["grade"] = _grade(r["score"], True)
    _apply_result(proxy, r)
    if r["ok"]:
        _BREAKER.pop(proxy_id, None)
    PROXIES[proxy_id] = proxy
    await save_proxies()
    shown = f"{r['ping_ms']}ms" if r["ok"] else "قطع"
    log_activity("network", f"تست پراکسی «{proxy['name']}» — {'موفق' if r['ok'] else 'ناموفق'} ({shown})", "ok" if r["ok"] else "warn")
    return proxy


# ══════════════════════════════════════════════════════════════════════════════
# اتصال واقعی relay ها (همان API قبلی)
# ══════════════════════════════════════════════════════════════════════════════

async def _connect_via_socks(proxy: dict, address: str, port: int):
    """یک اتصال TCP از طریق پراکسی به مقصد باز می‌کنه و reader/writer استاندارد
    asyncio برمی‌گردونه — دقیقاً همون شکلی که asyncio.open_connection برمی‌گردوند."""
    px = _make_socks_proxy(proxy)
    sock = await px.connect(dest_host=address, dest_port=port)
    return await asyncio.open_connection(sock=sock)


async def open_target_connection(link: dict | None, address: str, port: int, timeout: float = 10.0):
    """جایگزین asyncio.open_connection برای همه‌ی relayها. اگه کانفیگ outbound_proxy_id
    معتبر داشته باشه از اون پراکسی رد می‌شه؛ وگرنه اتصال مستقیم.
    circuit-breaker: بعد از چند شکست پشت‌سرهم «خودِ پراکسی»، چند ثانیه فوراً رد
    می‌کنیم (یا مستقیم) تا هر اتصال ۱۰ ثانیه معطل نشه."""
    proxy_id = (link or {}).get("outbound_proxy_id") or ""
    proxy = PROXIES.get(proxy_id) if proxy_id else None
    if proxy_id and (not proxy or not proxy.get("host")):
        logger.warning(f"outbound proxy id={proxy_id} not found; using direct")
        proxy = None
    if not proxy:
        return await asyncio.wait_for(asyncio.open_connection(address, port), timeout=timeout)

    st = _BREAKER.get(proxy_id)
    if st and st[1] > time.monotonic():
        if FALLBACK_DIRECT:
            return await asyncio.wait_for(asyncio.open_connection(address, port), timeout=timeout)
        raise ConnectionError(f"outbound proxy «{proxy.get('name')}» temporarily unavailable (circuit open)")
    try:
        conn = await asyncio.wait_for(_connect_via_socks(proxy, address, port), timeout=timeout)
        _BREAKER.pop(proxy_id, None)
        return conn
    except Exception as exc:
        if _is_proxy_down(exc):
            cnt = (st[0] if st else 0) + 1
            _BREAKER[proxy_id] = [cnt, time.monotonic() + BREAKER_COOLDOWN if cnt >= BREAKER_THRESHOLD else 0.0]
        if FALLBACK_DIRECT:
            logger.warning(f"outbound proxy «{proxy.get('name')}» failed ({exc!r}); falling back to direct")
            return await asyncio.wait_for(asyncio.open_connection(address, port), timeout=timeout)
        raise ConnectionError(f"outbound proxy «{proxy.get('name')}» failed: {type(exc).__name__}: {exc}") from exc


# ══════════════════════════════════════════════════════════════════════════════
# Job manager — اسکن زنده با polling
# ══════════════════════════════════════════════════════════════════════════════
SCAN_JOBS: dict = {}


def _purge_jobs():
    now = time.time()
    for jid in [j for j, v in SCAN_JOBS.items() if v["state"] != "running" and now - v.get("finished_at", now) > SCAN_JOB_TTL]:
        SCAN_JOBS.pop(jid, None)
    done = sorted((v for v in SCAN_JOBS.values() if v["state"] != "running"), key=lambda v: v.get("finished_at", 0))
    for v in done[:-6]:
        SCAN_JOBS.pop(v["id"], None)


def _active_jobs() -> int:
    return sum(1 for v in SCAN_JOBS.values() if v["state"] == "running")


def _job_opts(body: dict) -> dict:
    return {
        "samples": max(1, min(5, safe_int(body.get("samples", 3), minimum=1, maximum=5))),
        "tls": bool(body.get("tls", True)),
        "speed": bool(body.get("speed", False)),
        "concurrency": max(5, min(SCAN_MAX_CONCURRENCY, safe_int(body.get("concurrency", SCAN_DEFAULT_CONCURRENCY), minimum=5, maximum=SCAN_MAX_CONCURRENCY))),
        "timeout": max(2.0, min(15.0, float(body.get("timeout", SCAN_PROBE_TIMEOUT) or SCAN_PROBE_TIMEOUT))),
    }


async def _run_job(job: dict, candidates: list, opts: dict):
    sem = asyncio.Semaphore(opts["concurrency"])

    async def one(c: dict):
        async with sem:
            if job["cancel"]:
                return
            try:
                r = await asyncio.wait_for(
                    probe_candidate(
                        c, samples=opts["samples"], check_tls=opts["tls"], check_speed=opts["speed"],
                        tcp_timeout=min(opts["timeout"], 5.0), probe_timeout=opts["timeout"],
                    ),
                    timeout=SCAN_CAND_HARD_CAP,
                )
            except asyncio.CancelledError:
                raise
            except asyncio.TimeoutError:
                r = _blank_result(c)
                r.update(status="timeout", message=_STATUS_TEXT["timeout"])
            except Exception as exc:
                r = _blank_result(c)
                r.update(status="error", message=f"{_STATUS_TEXT['error']}: {type(exc).__name__}")
            if c.get("proxy_id"):
                r["proxy_id"] = c["proxy_id"]
            r["i"] = len(job["results"])
            job["results"].append(r)
            job["done"] += 1
            if r["ok"]:
                job["working"] += 1
            if r["status"] == "risky":
                job["risky"] += 1

    job["tasks"] = [asyncio.create_task(one(c)) for c in candidates]
    try:
        await asyncio.gather(*job["tasks"], return_exceptions=True)
    finally:
        if job["mode"] == "saved":
            for r in job["results"]:
                pid = r.get("proxy_id")
                if pid and pid in PROXIES:
                    _apply_result(PROXIES[pid], r)
                    if r["ok"]:
                        _BREAKER.pop(pid, None)
            try:
                await save_proxies()
            except Exception as exc:
                logger.warning(f"saving re-tested proxies failed: {exc}")
        job["state"] = "cancelled" if job["cancel"] else "done"
        job["finished_at"] = time.time()
        job.pop("tasks", None)
        log_activity(
            "network",
            f"اسکن پروکسی ({'لغو شد' if job['cancel'] else 'تمام شد'}): {job['working']} سالم از {job['done']} بررسی‌شده",
            "ok" if job["working"] else "warn",
        )


def _start_job(mode: str, candidates: list, opts: dict, extra: dict | None = None) -> dict:
    job = {
        "id": secrets.token_urlsafe(9), "mode": mode, "state": "running", "cancel": False,
        "total": len(candidates), "done": 0, "working": 0, "risky": 0, "results": [],
        "opts": opts, "started_at": time.time(), "finished_at": None, **(extra or {}),
    }
    SCAN_JOBS[job["id"]] = job
    job["runner"] = asyncio.create_task(_run_job(job, candidates, opts))
    return job


def _public_result(r: dict) -> dict:
    d = dict(r)
    d["has_auth"] = bool(d.get("username"))
    d.pop("password", None)
    return d


async def _fetch_list(url: str) -> str:
    """دانلود لیست از URL ادمین — با بررسی SSRF روی هر redirect و سقف حجم."""
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=False) as client:
        for _ in range(4):
            u = urlparse(url)
            if u.scheme not in ("http", "https") or not u.hostname:
                raise HTTPException(status_code=400, detail="آدرس لیست باید با http:// یا https:// شروع بشه")
            if await _host_is_blocked(u.hostname):
                raise HTTPException(status_code=400, detail="آدرس داخلی/لوکال مجاز نیست")
            async with client.stream("GET", url) as resp:
                if resp.status_code in (301, 302, 303, 307, 308) and resp.headers.get("location"):
                    url = urljoin(url, resp.headers["location"])
                    continue
                if resp.status_code >= 400:
                    raise HTTPException(status_code=400, detail=f"سرور لیست پاسخ {resp.status_code} داد")
                chunks, size = [], 0
                async for chunk in resp.aiter_bytes():
                    chunks.append(chunk)
                    size += len(chunk)
                    if size >= SCAN_URL_MAX_BYTES:
                        break
                return b"".join(chunks)[:SCAN_URL_MAX_BYTES].decode("utf-8", errors="ignore")
    raise HTTPException(status_code=400, detail="تعداد redirect بیش از حد مجاز است")


async def _collect_candidates(body: dict, default_scheme: str, cap: int):
    source = str(body.get("source") or "text").strip().lower()
    raw_text = str(body.get("text") or "")[:SCAN_MAX_TEXT_BYTES]
    if source == "url":
        url = str(body.get("url") or "").strip()
        try:
            raw_text = await _fetch_list(url)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"دریافت لیست ناموفق بود: {type(exc).__name__}: {str(exc)[:150]}")
    cands, seen, blocked, truncated = [], set(), 0, False
    for line in raw_text.replace("\r", "\n").replace(",", "\n").split("\n"):
        c = parse_candidate(line, default_scheme)
        if not c:
            continue
        key = (c["host"], c["port"])
        if key in seen:
            continue
        seen.add(key)
        if await _host_is_blocked(c["host"]):
            blocked += 1
            continue
        if len(cands) >= cap:
            truncated = True
            break
        cands.append(c)
    return cands, blocked, truncated


# ══════════════════════════════════════════════════════════════════════════════
# API
# ══════════════════════════════════════════════════════════════════════════════
router = APIRouter()


async def require_owner(request: Request, token=Depends(require_auth)):
    if token == NODE_API_TOKEN_MARK:   # پنل اصلی که با توکن نود این پنل را مدیریت می‌کند
        return token
    info = await get_session_info(request.cookies.get(SESSION_COOKIE))
    if not info or info.get("admin_id") != "owner":
        raise HTTPException(status_code=403, detail="فقط مالک پنل می‌تواند پراکسی‌ها را مدیریت کند.")
    return token


async def _json_body(request: Request) -> dict:
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="ورودی معتبر نیست")
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="ورودی معتبر نیست")
    return body


@router.get("/api/proxies")
async def api_list_proxies(_=Depends(require_auth)):
    counts = proxy_usage_counts()
    out = []
    for p in list_proxies():
        d = _public(p)
        d["in_use"] = counts.get(p["id"], 0)
        st = _BREAKER.get(p["id"])
        d["breaker_open"] = bool(st and st[1] > time.monotonic())
        out.append(d)
    return {"ok": True, "proxies": out, "fallback_direct": FALLBACK_DIRECT,
            "scan_limits": {"max_candidates": SCAN_JOB_MAX_CANDIDATES, "max_concurrency": SCAN_MAX_CONCURRENCY}}


@router.post("/api/proxies")
async def api_upsert_proxy(request: Request, _=Depends(require_owner)):
    body = await _json_body(request)
    host, port, username, password, scheme = _parse_host_input(
        str(body.get("host") or ""), body.get("port", 1080),
        str(body.get("username") or ""), str(body.get("password") or ""),
    )
    if not host:
        raise HTTPException(status_code=400, detail="آدرس (Host) پراکسی را وارد کنید.")
    proxy_id = str(body.get("id") or "").strip() or None
    if proxy_id and proxy_id not in PROXIES:
        raise HTTPException(status_code=404, detail="پراکسی پیدا نشد")
    if not proxy_id and len(PROXIES) >= MAX_PROXIES:
        raise HTTPException(status_code=400, detail=f"حداکثر {MAX_PROXIES} پراکسی مجاز است")
    scheme = _norm_scheme(body.get("scheme") or scheme or (PROXIES.get(proxy_id or "", {}).get("scheme")) or "socks5")
    record = await upsert_proxy(proxy_id, {
        "name": body.get("name"), "host": host, "scheme": scheme,
        "port": safe_int(port, minimum=1, maximum=65535),
        "username": username, "password": password,
    })
    log_activity("network", f"پراکسی «{record['name']}» ذخیره شد", "ok")
    return {"ok": True, "proxy": _public(record)}


@router.delete("/api/proxies/{proxy_id}")
async def api_delete_proxy(proxy_id: str, _=Depends(require_owner)):
    if proxy_id not in PROXIES:
        raise HTTPException(status_code=404, detail="پراکسی پیدا نشد")
    name = PROXIES[proxy_id].get("name", proxy_id)
    detached = await delete_proxy(proxy_id)
    log_activity("network", f"پراکسی «{name}» حذف شد ({detached} کانفیگ به مستقیم برگشت)", "warn")
    return {"ok": True, "detached": detached}


@router.post("/api/proxies/{proxy_id}/test")
async def api_test_proxy(proxy_id: str, _=Depends(require_owner)):
    if proxy_id not in PROXIES:
        raise HTTPException(status_code=404, detail="پراکسی پیدا نشد")
    try:
        result = await test_proxy(proxy_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"ok": True, "proxy": _public(result)}


# ---------- اسکنر زنده (Job) ----------

@router.post("/api/proxies/scan/start")
async def api_scan_start(request: Request, _=Depends(require_owner)):
    """شروع اسکن زنده. body: {source: text|url, text|url, protocol: socks5|socks4|http|auto,
    samples:1-5, tls:bool, speed:bool, concurrency, timeout}"""
    body = await _json_body(request)
    _purge_jobs()
    if _active_jobs() >= SCAN_MAX_ACTIVE_JOBS:
        raise HTTPException(status_code=429, detail="یک اسکن دیگر در حال اجراست؛ صبر کن تمام شود یا لغوش کن")
    proto = str(body.get("protocol") or "socks5").strip().lower()
    proto = "auto" if proto == "auto" else _norm_scheme(proto)
    cands, blocked, truncated = await _collect_candidates(body, proto, SCAN_JOB_MAX_CANDIDATES)
    if not cands:
        detail = "هیچ پروکسی معتبری در ورودی پیدا نشد (فرمت: host:port یا host:port:user:pass یا scheme://user:pass@host:port)"
        if blocked:
            detail += f" — {blocked} آدرس داخلی/لوکال بلاک شد"
        raise HTTPException(status_code=400, detail=detail)
    job = _start_job("scan", cands, _job_opts(body), {"blocked": blocked, "truncated": truncated})
    return {"ok": True, "job_id": job["id"], "total": job["total"], "blocked": blocked, "truncated": truncated}


@router.post("/api/proxies/scan/saved")
async def api_scan_saved(request: Request, _=Depends(require_owner)):
    """تست دوباره‌ی پراکسی‌های ذخیره‌شده (همه یا ids) با همین موتور؛ نتیجه روی رکوردها ذخیره می‌شه."""
    body = await _json_body(request)
    _purge_jobs()
    if _active_jobs() >= SCAN_MAX_ACTIVE_JOBS:
        raise HTTPException(status_code=429, detail="یک اسکن دیگر در حال اجراست")
    ids = body.get("ids")
    pool = [PROXIES[i] for i in ids if i in PROXIES] if isinstance(ids, list) else list(PROXIES.values())
    if not pool:
        raise HTTPException(status_code=400, detail="پراکسی‌ای برای تست وجود ندارد")
    cands = [{
        "scheme": _norm_scheme(p.get("scheme") or "socks5"), "host": p["host"], "port": int(p["port"]),
        "username": p.get("username", ""), "password": p.get("password", ""), "proxy_id": p["id"],
    } for p in pool]
    job = _start_job("saved", cands, _job_opts(body))
    return {"ok": True, "job_id": job["id"], "total": job["total"]}


@router.get("/api/proxies/scan/{job_id}")
async def api_scan_status(job_id: str, since: int = 0, _=Depends(require_owner)):
    job = SCAN_JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="اسکن پیدا نشد (ممکن است منقضی شده باشد)")
    since = max(0, int(since))
    new = [_public_result(r) for r in job["results"][since:since + 400]]
    elapsed = (job["finished_at"] or time.time()) - job["started_at"]
    return {
        "ok": True, "job_id": job_id, "mode": job["mode"], "state": job["state"],
        "total": job["total"], "done": job["done"], "working": job["working"], "risky": job["risky"],
        "elapsed": round(elapsed, 1), "blocked": job.get("blocked", 0), "truncated": job.get("truncated", False),
        "next": since + len(new), "results": new,
    }


@router.post("/api/proxies/scan/{job_id}/cancel")
async def api_scan_cancel(job_id: str, _=Depends(require_owner)):
    job = SCAN_JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="اسکن پیدا نشد")
    if job["state"] == "running":
        job["cancel"] = True
        for t in list(job.get("tasks") or []):
            t.cancel()
    return {"ok": True}


def _select_results(job: dict, body: dict) -> list:
    idx = body.get("indexes")
    include_risky = bool(body.get("include_risky", False))
    min_score = max(0, min(100, safe_int(body.get("min_score", 0), minimum=0, maximum=100)))
    res = job["results"]
    if isinstance(idx, list):
        picked = [res[i] for i in idx if isinstance(i, int) and 0 <= i < len(res)]
        picked = [r for r in picked if r["ok"]]
    else:
        picked = [r for r in res if r["ok"] and (include_risky or r["status"] == "ok") and r["score"] >= min_score]
    return sorted(picked, key=lambda r: (-r["score"], r["ping_ms"] if r["ping_ms"] is not None else 1e9))


def _auto_name(r: dict) -> str:
    base = r.get("country") or r["host"]
    return (f"{base} · {r['city']}" if r.get("city") else base)[:80]


@router.post("/api/proxies/scan/{job_id}/import")
async def api_scan_import(job_id: str, request: Request, _=Depends(require_owner)):
    """افزودن نتیجه‌های اسکن به لیست پراکسی‌ها — مشخصات ورود (پسورد) سمت سرور می‌مونه.
    body: {indexes?: [int]} یا فیلتر {min_score, include_risky, limit}"""
    body = await _json_body(request)
    job = SCAN_JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="اسکن پیدا نشد")
    if job["mode"] != "scan":
        raise HTTPException(status_code=400, detail="این اسکن مربوط به پراکسی‌های ذخیره‌شده است")
    limit = max(1, min(200, safe_int(body.get("limit", 100), minimum=1, maximum=200)))
    picked = _select_results(job, body)[:limit]
    if not picked:
        raise HTTPException(status_code=400, detail="موردی با این شرایط پیدا نشد")
    existing = {(p["host"], p["port"]) for p in PROXIES.values()}
    added, skipped = [], 0
    for r in picked:
        if len(PROXIES) >= MAX_PROXIES:
            break
        if (r["host"], r["port"]) in existing:
            skipped += 1
            continue
        pid = secrets.token_urlsafe(8)
        rec = _build_record(pid, {
            "name": _auto_name(r), "host": r["host"], "port": r["port"], "scheme": r["scheme"],
            "username": r.get("username", ""), "password": r.get("password", ""),
        }, {})
        _apply_result(rec, r)
        PROXIES[pid] = rec
        existing.add((r["host"], r["port"]))
        added.append(pid)
    if added:
        await save_proxies()
        log_activity("network", f"{len(added)} پراکسی از اسکن اضافه شد" + (f" ({skipped} تکراری رد شد)" if skipped else ""), "ok")
    return {"ok": True, "added": len(added), "skipped": skipped, "proxies": [_public(PROXIES[i]) for i in added]}


@router.post("/api/proxies/scan/{job_id}/export")
async def api_scan_export(job_id: str, request: Request, _=Depends(require_owner)):
    """لیست متنی سالم‌ها (scheme://user:pass@host:port) برای کپی. POST است تا پسورد در URL/لاگ نیاید."""
    body = await _json_body(request)
    job = SCAN_JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="اسکن پیدا نشد")
    lines = []
    for r in _select_results(job, body):
        cred = f"{quote(r['username'], safe='')}:{quote(r['password'], safe='')}@" if r.get("username") else ""
        lines.append(f"{r['scheme']}://{cred}{r['host']}:{r['port']}")
    return {"ok": True, "count": len(lines), "lines": lines}


# ---------- سازگاری با نسخه‌ی قبل ----------

@router.post("/api/proxies/scan")
async def api_scan_proxies(request: Request, _=Depends(require_owner)):
    """نسخه‌ی همزمان و قدیمی (حداکثر ۶۰ کاندید). پیشنهاد: از /api/proxies/scan/start استفاده کن."""
    body = await _json_body(request)
    cands, _blocked, truncated = await _collect_candidates(body, "socks5", SCAN_MAX_CANDIDATES)
    if not cands:
        raise HTTPException(status_code=400, detail="هیچ پروکسی معتبری در ورودی پیدا نشد (فرمت: host:port یا host:port:user:pass)")
    sem = asyncio.Semaphore(SCAN_CONCURRENCY)

    async def _bounded(c):
        async with sem:
            try:
                return await asyncio.wait_for(
                    probe_candidate(c, samples=1, check_tls=False, tcp_timeout=SCAN_TCP_TIMEOUT, probe_timeout=SCAN_PROBE_TIMEOUT),
                    timeout=SCAN_CAND_HARD_CAP,
                )
            except Exception as exc:
                r = _blank_result(c)
                r.update(status="error", message=f"{_STATUS_TEXT['error']}: {type(exc).__name__}")
                return r

    results = await asyncio.gather(*(_bounded(c) for c in cands))
    results = sorted(results, key=lambda r: (not r["ok"], r["ping_ms"] if r["ping_ms"] is not None else 999999))
    working = sum(1 for r in results if r["ok"])
    log_activity("network", f"اسکن پروکسی: {working} از {len(results)} مورد سالم بود", "ok" if working else "warn")
    return {"ok": True, "scanned": len(results), "working": working, "truncated": truncated, "results": results}


@router.post("/api/proxies/bulk")
async def api_bulk_add_proxies(request: Request, _=Depends(require_owner)):
    """چند پراکسی رو یک‌جا ذخیره می‌کنه (نتیجه‌ی تست همراه آیتم کش می‌شه)."""
    body = await _json_body(request)
    items = body.get("items")
    if not isinstance(items, list) or not items:
        raise HTTPException(status_code=400, detail="حداقل یک پراکسی انتخاب کن")
    if len(items) > 50:
        raise HTTPException(status_code=400, detail="حداکثر ۵۰ مورد در هر بار")
    if len(PROXIES) >= MAX_PROXIES:
        raise HTTPException(status_code=400, detail=f"حداکثر {MAX_PROXIES} پراکسی مجاز است")
    existing = {(p["host"], p["port"]) for p in PROXIES.values()}
    added, skipped = [], 0
    for it in items:
        if not isinstance(it, dict) or len(PROXIES) >= MAX_PROXIES:
            continue
        host = str(it.get("host") or "").strip()
        try:
            port = max(1, min(65535, int(it.get("port") or 1080)))
        except (TypeError, ValueError):
            continue
        if not host or (host, port) in existing:
            skipped += 1
            continue
        pid = secrets.token_urlsafe(8)
        rec = _build_record(pid, {
            "name": str(it.get("name") or it.get("country") or host)[:80], "host": host, "port": port,
            "scheme": it.get("scheme") or "socks5",
            "username": it.get("username", ""), "password": it.get("password", ""),
        }, {})
        if it.get("ok"):
            _apply_result(rec, {**it, "ok": True, "tested_at": _now_iso(), "message": str(it.get("message") or "از اسکن")})
        PROXIES[pid] = rec
        existing.add((host, port))
        added.append(pid)
    if added:
        await save_proxies()
        msg = f"{len(added)} پراکسی از اسکن اضافه شد" + (f" ({skipped} مورد تکراری رد شد)" if skipped else "")
        log_activity("network", msg, "ok")
    return {"ok": True, "added": len(added), "skipped": skipped, "proxies": [_public(PROXIES[i]) for i in added]}
