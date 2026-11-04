# nodes.py

import asyncio
import hmac
import json
import os
import secrets
import time
from datetime import datetime
from urllib.parse import quote, urlparse

import httpx
import psutil
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from main import (
    APP_VERSION,
    DATA_DIR,
    LINKS,
    app,
    connections,
    get_host,
    log_activity,
    logger,
    require_auth,
    require_owner,
    stats,
)

NODES_FILE = DATA_DIR / "vodiwalker_nodes.json"
TOKEN_FILE = DATA_DIR / "vodiwalker_node_token.json"
NODES_LOCK = asyncio.Lock()

NODES: dict = {}          # id -> {id,name,url,token,enabled,created_at}
STATUS: dict = {}         # id -> آخرین نتیجه‌ی سنجش (فقط در حافظه)

MONITOR_INTERVAL = 30.0
CHECK_TIMEOUT = 8.0
FORWARD_TIMEOUT = 30.0
MAX_FORWARD_BODY = 5 * 1024 * 1024
MAX_NODES = 50

# فقط همین مسیرها با توکن نود (و از طریق فوروارد پنل اصلی) قابل‌دسترسی‌اند.
# عمداً بیرونشون: /api/admins، /api/change-*، /api/security، /api/settings، /api/bot،
# /api/login|logout|me، /api/nodes و /api/node/token — تا توکن نود هیچ‌وقت به
# حساب‌ها و نشست‌ها یا زنجیره‌ی نود-به-نود راه نده.
NODE_ALLOWED_PREFIXES = (
    "/api/links", "/api/proxies", "/api/subs", "/api/categories", "/api/protocols",
    "/api/reality-keypair", "/api/connections", "/api/telemetry", "/api/system",
    "/api/network", "/api/reports", "/api/activity", "/api/errors",
    "/stats",
)
NODE_ALLOWED_EXACT = ("/api/node/info",)


def path_allowed(path: str) -> bool:
    p = "/" + (path or "").strip("/")
    if ".." in p.split("/") or "//" in path:
        return False
    if p in NODE_ALLOWED_EXACT:
        return True
    return any(p == pre or p.startswith(pre + "/") for pre in NODE_ALLOWED_PREFIXES)


def _now_iso() -> str:
    return datetime.now().isoformat()


# ══════════════════════════════════════════════════════════════════════════════
# توکن این پنل (وقتی این پنل «نود» است)
# ══════════════════════════════════════════════════════════════════════════════
_node_token: str = ""
_node_token_created: str = ""


def _load_token():
    global _node_token, _node_token_created
    try:
        if TOKEN_FILE.exists():
            d = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
            _node_token = str(d.get("token") or "")
            _node_token_created = str(d.get("created_at") or "")
    except Exception as exc:
        logger.warning(f"node token load failed: {exc}")


def _save_token():
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = TOKEN_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps({"token": _node_token, "created_at": _node_token_created}), encoding="utf-8")
    try:
        os.chmod(tmp, 0o600)
    except Exception:
        pass
    tmp.replace(TOKEN_FILE)


def generate_token() -> str:
    return "vwn_" + secrets.token_urlsafe(32)


# ── محدودسازی تلاش‌های ناموفق (brute-force) بر اساس IP ─────────────────────────
_FAILS: dict = {}
FAIL_LIMIT = 10
FAIL_WINDOW = 300.0


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "?"


def _is_throttled(ip: str) -> bool:
    rec = _FAILS.get(ip)
    if not rec:
        return False
    count, first = rec
    if time.time() - first > FAIL_WINDOW:
        _FAILS.pop(ip, None)
        return False
    return count >= FAIL_LIMIT


def _register_failure(ip: str):
    now = time.time()
    count, first = _FAILS.get(ip, (0, now))
    if now - first > FAIL_WINDOW:
        count, first = 0, now
    _FAILS[ip] = (count + 1, first)
    if len(_FAILS) > 2000:
        for k in list(_FAILS)[:500]:
            _FAILS.pop(k, None)


def authorize_node_request(request: Request) -> bool:
    """از main.require_auth صدا زده می‌شه وقتی کوکی معتبری نیست و هدر Bearer اومده.
    True = توکن نود درسته و مسیر مجازه. False = بی‌اعتبار (main خودش 401 می‌ده)."""
    auth = request.headers.get("authorization", "")
    if not auth.lower().startswith("bearer "):
        return False
    ip = _client_ip(request)
    if _is_throttled(ip):
        raise HTTPException(status_code=429, detail="تلاش ناموفق زیاد؛ چند دقیقه بعد دوباره امتحان کن")
    presented = auth[7:].strip()
    if not _node_token or not hmac.compare_digest(presented.encode(), _node_token.encode()):
        _register_failure(ip)
        return False
    if not path_allowed(request.url.path):
        raise HTTPException(status_code=403, detail="این مسیر با توکن نود قابل‌دسترسی نیست")
    return True


# ══════════════════════════════════════════════════════════════════════════════
# استور نودها (وقتی این پنل «اصلی» است)
# ══════════════════════════════════════════════════════════════════════════════
def _load_nodes():
    try:
        if NODES_FILE.exists():
            d = json.loads(NODES_FILE.read_text(encoding="utf-8"))
            if isinstance(d, dict):
                NODES.clear()
                NODES.update(d)
    except Exception as exc:
        logger.warning(f"nodes store load failed: {exc}")


def _save_nodes_sync():
    NODES_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = NODES_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(NODES, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(tmp, 0o600)
    except Exception:
        pass
    tmp.replace(NODES_FILE)


async def _save_nodes():
    async with NODES_LOCK:
        await asyncio.to_thread(_save_nodes_sync)


_load_token()
_load_nodes()


def normalize_url(raw: str) -> str:
    """فقط origin (scheme://host[:port]) نگه داشته می‌شه."""
    raw = (raw or "").strip()
    if not raw:
        raise ValueError("آدرس نود را وارد کنید")
    if "://" not in raw:
        raw = "https://" + raw
    u = urlparse(raw)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise ValueError("آدرس نود معتبر نیست (باید http:// یا https:// باشد)")
    if u.username or u.password:
        raise ValueError("آدرس نباید شامل نام کاربری/رمز باشد؛ توکن را در فیلد خودش بگذار")
    host = f"[{u.hostname}]" if ":" in u.hostname else u.hostname
    try:
        port = u.port
    except ValueError:
        raise ValueError("پورت آدرس معتبر نیست")
    return f"{u.scheme}://{host}" + (f":{port}" if port else "")


def get_node(node_id: str) -> dict | None:
    return NODES.get(node_id)


class NodeCallError(Exception):
    """خطای قابل‌نمایش هنگام صدا زدن یک API روی نود (main.py این را به HTTPException تبدیل می‌کند)."""

    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.status_code = status_code


async def call_node_json(node_id: str, method: str, path: str, json_body=None, timeout: float | None = None) -> dict:
    """یک API مجاز را روی نود صدا می‌زند و JSON را برمی‌گرداند. برای استفاده‌ی داخلی
    main.py (مثل «لینک کردن اینباند یک نود در ساب‌گروه پنل اصلی»)، نه یک روت HTTP."""
    node = NODES.get(node_id)
    if not node:
        raise NodeCallError("نود پیدا نشد", 404)
    if not node.get("enabled", True):
        raise NodeCallError(f"نود «{node['name']}» غیرفعال است", 409)
    target = "/" + path.lstrip("/")
    if not path_allowed(target):
        raise NodeCallError("این مسیر روی نود مجاز نیست", 403)
    body = None
    headers = _auth_headers(node.get("token", ""))
    if json_body is not None:
        body = json.dumps(json_body).encode()
        headers["Content-Type"] = "application/json"
    try:
        r = await _http().request(method, node["url"] + target, content=body, headers=headers, timeout=(timeout or FORWARD_TIMEOUT))
    except httpx.TimeoutException:
        raise NodeCallError(f"نود «{node['name']}» در زمان تعیین‌شده جواب نداد", 504)
    except httpx.HTTPError:
        raise NodeCallError(f"اتصال به نود «{node['name']}» برقرار نشد", 502)
    if r.status_code in (401, 403):
        raise NodeCallError(f"توکن نود «{node['name']}» نامعتبر است", 502)
    if r.status_code == 404:
        raise NodeCallError("مورد موردنظر روی نود پیدا نشد (شاید حذف شده باشد)", 404)
    if r.status_code >= 400:
        detail = None
        try:
            detail = r.json().get("detail")
        except Exception:
            pass
        raise NodeCallError(detail or f"خطای نود (HTTP {r.status_code})", 502)
    try:
        return r.json()
    except Exception:
        raise NodeCallError("پاسخ نامعتبر از نود", 502)


def _public_node(n: dict) -> dict:
    tok = n.get("token") or ""
    return {
        "id": n["id"],
        "name": n.get("name", ""),
        "url": n.get("url", ""),
        "enabled": bool(n.get("enabled", True)),
        "created_at": n.get("created_at", ""),
        "token_hint": ("…" + tok[-4:]) if tok else "",
        "status": STATUS.get(n["id"]),
    }


# ══════════════════════════════════════════════════════════════════════════════
# سنجش وضعیت
# ══════════════════════════════════════════════════════════════════════════════
_client: httpx.AsyncClient | None = None


def _http() -> httpx.AsyncClient:
    global _client
    if _client is None:
        # follow_redirects=False: تا توکن هیچ‌وقت به آدرس دیگه‌ای (ریدایرکت) نره
        _client = httpx.AsyncClient(
            timeout=httpx.Timeout(CHECK_TIMEOUT, connect=6.0),
            limits=httpx.Limits(max_connections=50, max_keepalive_connections=10),
            follow_redirects=False,
        )
    return _client


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Accept": "application/json", "User-Agent": f"VodiWalker-Node/{APP_VERSION}"}


async def probe_node(url: str, token: str) -> dict:
    """GET /api/node/info روی نود. همیشه dict برمی‌گردونه (online True/False)."""
    started = time.perf_counter()
    res = {"online": False, "checked_at": _now_iso(), "error": ""}
    try:
        r = await _http().get(f"{url}/api/node/info", headers=_auth_headers(token), timeout=CHECK_TIMEOUT)
        res["latency_ms"] = round((time.perf_counter() - started) * 1000, 1)
        if r.status_code in (401, 403):
            res["error"] = "توکن نامعتبر است یا در نود غیرفعال شده است"
        elif r.status_code == 429:
            res["error"] = "نود تلاش‌های ناموفق زیاد دیده؛ چند دقیقه بعد دوباره امتحان کن"
        elif r.status_code == 404:
            res["error"] = "این آدرس یک پنل VodiWalker با قابلیت نود نیست (نسخه‌ی پنل را آپدیت کن)"
        elif 300 <= r.status_code < 400:
            res["error"] = "آدرس ریدایرکت می‌شود؛ آدرس نهایی (https) را وارد کن"
        elif r.status_code != 200:
            res["error"] = f"پاسخ نامعتبر از نود (HTTP {r.status_code})"
        else:
            d = r.json()
            if not (isinstance(d, dict) and d.get("ok") and d.get("service") == "vodiwalker"):
                res["error"] = "پاسخ این آدرس شبیه پنل VodiWalker نیست"
            else:
                res.update(
                    online=True,
                    version=d.get("version", ""),
                    host=d.get("host", ""),
                    uptime_seconds=d.get("uptime_seconds", 0),
                    inbounds=d.get("inbounds", 0),
                    clients=d.get("clients", 0),
                    connections=d.get("connections", 0),
                    total_bytes=d.get("total_bytes", 0),
                    cpu=d.get("cpu"),
                    mem=d.get("mem"),
                )
    except httpx.TimeoutException:
        res["error"] = "نود در زمان تعیین‌شده جواب نداد"
    except httpx.ConnectError:
        res["error"] = "اتصال به نود برقرار نشد (آدرس/شبکه را بررسی کن)"
    except Exception as exc:
        res["error"] = f"خطا: {type(exc).__name__}: {str(exc)[:120]}"
    return res


async def check_node(node_id: str) -> dict | None:
    node = NODES.get(node_id)
    if not node:
        return None
    prev = STATUS.get(node_id) or {}
    res = await probe_node(node["url"], node.get("token", ""))
    res["last_online_at"] = res["checked_at"] if res["online"] else prev.get("last_online_at")
    if prev.get("online") is not None and prev.get("online") != res["online"]:
        log_activity("network", f"نود «{node['name']}» {'آنلاین شد' if res['online'] else 'آفلاین شد'}", "ok" if res["online"] else "warn")
    STATUS[node_id] = res
    return res


async def check_all() -> None:
    ids = [i for i, n in NODES.items() if n.get("enabled", True)]
    if ids:
        await asyncio.gather(*(check_node(i) for i in ids), return_exceptions=True)


_monitor_task: asyncio.Task | None = None


async def _monitor_loop():
    await asyncio.sleep(3)
    while True:
        try:
            await check_all()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.warning(f"node monitor error: {exc}")
        await asyncio.sleep(MONITOR_INTERVAL)


@app.on_event("startup")
async def _start_node_monitor():
    global _monitor_task
    if _monitor_task is None or _monitor_task.done():
        _monitor_task = asyncio.create_task(_monitor_loop())


@app.on_event("shutdown")
async def _stop_node_monitor():
    global _monitor_task, _client
    if _monitor_task:
        _monitor_task.cancel()
        _monitor_task = None
    if _client is not None:
        await _client.aclose()
        _client = None


# ══════════════════════════════════════════════════════════════════════════════
# API
# ══════════════════════════════════════════════════════════════════════════════
router = APIRouter()


# ── وقتی این پنل «نود» است ──────────────────────────────────────────────────────
@router.get("/api/node/info")
async def api_node_info(request: Request, _=Depends(require_auth)):
    """اطلاعات این پنل برای پنل اصلی (با کوکی ادمین یا توکن نود)."""
    vm = psutil.virtual_memory()
    clients = sum(1 for l in LINKS.values() if l.get("parent_inbound_id"))
    return {
        "ok": True,
        "service": "vodiwalker",
        "version": APP_VERSION,
        "host": get_host(request),
        "uptime_seconds": int(time.time() - stats["start_time"]),
        "inbounds": len(LINKS) - clients,
        "clients": clients,
        "connections": len(connections),
        "total_bytes": int(stats.get("total_bytes", 0)),
        "cpu": psutil.cpu_percent(interval=None),
        "mem": vm.percent,
        "time": _now_iso(),
    }


@router.get("/api/node/token")
async def api_node_token_get(_=Depends(require_owner)):
    return {"ok": True, "enabled": bool(_node_token), "token": _node_token or None, "created_at": _node_token_created or None}


@router.post("/api/node/token")
async def api_node_token_create(_=Depends(require_owner)):
    """ساخت توکن جدید (توکن قبلی همان لحظه باطل می‌شود)."""
    global _node_token, _node_token_created
    had = bool(_node_token)
    _node_token = generate_token()
    _node_token_created = _now_iso()
    await asyncio.to_thread(_save_token)
    log_activity("network", "توکن نود " + ("دوباره ساخته شد (توکن قبلی باطل شد)" if had else "ساخته شد"), "warn" if had else "ok")
    return {"ok": True, "enabled": True, "token": _node_token, "created_at": _node_token_created}


@router.delete("/api/node/token")
async def api_node_token_disable(_=Depends(require_owner)):
    global _node_token, _node_token_created
    _node_token, _node_token_created = "", ""
    await asyncio.to_thread(_save_token)
    log_activity("network", "توکن نود غیرفعال شد", "warn")
    return {"ok": True, "enabled": False, "token": None}


# ── وقتی این پنل «اصلی» است ─────────────────────────────────────────────────────
def _parse_node_body(body) -> tuple[str, str, str, bool | None]:
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="اطلاعات نود معتبر نیست")
    try:
        url = normalize_url(str(body.get("url") or ""))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    name = str(body.get("name") or "").strip()[:60]
    token = str(body.get("token") or "").strip()
    enabled = body.get("enabled")
    return name, url, token, (None if enabled is None else bool(enabled))


@router.get("/api/nodes")
async def api_nodes_list(_=Depends(require_owner)):
    nodes = sorted(NODES.values(), key=lambda n: n.get("created_at", ""))
    return {"ok": True, "nodes": [_public_node(n) for n in nodes], "token_enabled": bool(_node_token)}


@router.post("/api/nodes/test")
async def api_nodes_test(request: Request, _=Depends(require_owner)):
    """تست اتصال قبل از ذخیره (چیزی ذخیره نمی‌شه)."""
    try:
        body = await request.json()
    except Exception:
        body = None
    _n, url, token, _e = _parse_node_body(body)
    if not token:
        nid = str((body or {}).get("id") or "")
        token = (NODES.get(nid) or {}).get("token", "")
    if not token:
        raise HTTPException(status_code=400, detail="توکن نود را وارد کنید")
    return {"ok": True, "status": await probe_node(url, token)}


@router.post("/api/nodes")
async def api_nodes_upsert(request: Request, _=Depends(require_owner)):
    try:
        body = await request.json()
    except Exception:
        body = None
    name, url, token, enabled = _parse_node_body(body)
    node_id = str((body or {}).get("id") or "").strip() or None
    existing = NODES.get(node_id) if node_id else None
    if node_id and not existing:
        raise HTTPException(status_code=404, detail="نود پیدا نشد")
    if not existing:
        if len(NODES) >= MAX_NODES:
            raise HTTPException(status_code=400, detail=f"حداکثر {MAX_NODES} نود مجاز است")
        if not token:
            raise HTTPException(status_code=400, detail="توکن نود را وارد کنید")
        if any(n.get("url") == url for n in NODES.values()):
            raise HTTPException(status_code=409, detail="این نود قبلاً اضافه شده است")
    record = {
        "id": node_id or secrets.token_urlsafe(8),
        "name": name or (existing or {}).get("name") or urlparse(url).hostname or "node",
        "url": url,
        "token": token or (existing or {}).get("token", ""),
        "enabled": (existing or {}).get("enabled", True) if enabled is None else enabled,
        "created_at": (existing or {}).get("created_at") or _now_iso(),
    }
    NODES[record["id"]] = record
    await _save_nodes()
    STATUS.pop(record["id"], None)
    if record["enabled"]:
        await check_node(record["id"])
    log_activity("network", f"نود «{record['name']}» {'ویرایش' if existing else 'اضافه'} شد", "ok")
    return {"ok": True, "node": _public_node(record)}


@router.delete("/api/nodes/{node_id}")
async def api_nodes_delete(node_id: str, _=Depends(require_owner)):
    node = NODES.pop(node_id, None)
    if not node:
        raise HTTPException(status_code=404, detail="نود پیدا نشد")
    STATUS.pop(node_id, None)
    await _save_nodes()
    try:
        from main import mark_node_removed_in_subs
        await mark_node_removed_in_subs(node_id)
    except Exception as exc:
        logger.warning(f"failed to flag orphaned remote sub-links after node removal: {exc}")
    log_activity("network", f"نود «{node.get('name')}» حذف شد", "warn")
    return {"ok": True}


@router.post("/api/nodes/check-all")
async def api_nodes_check_all(_=Depends(require_owner)):
    await check_all()
    return {"ok": True, "nodes": [_public_node(n) for n in sorted(NODES.values(), key=lambda n: n.get("created_at", ""))]}


@router.post("/api/nodes/{node_id}/check")
async def api_nodes_check(node_id: str, _=Depends(require_owner)):
    if node_id not in NODES:
        raise HTTPException(status_code=404, detail="نود پیدا نشد")
    await check_node(node_id)
    return {"ok": True, "node": _public_node(NODES[node_id])}


@router.api_route("/api/nodes/{node_id}/fwd/{path:path}", methods=["GET", "POST", "PATCH", "PUT", "DELETE"])
async def api_nodes_forward(node_id: str, path: str, request: Request, _=Depends(require_owner)):
    """همان API پنل را روی نود اجرا می‌کند (فقط مسیرهای مجاز، فقط مالک پنل)."""
    node = NODES.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="نود پیدا نشد")
    if not node.get("enabled", True):
        raise HTTPException(status_code=409, detail="این نود غیرفعال است")
    target = "/" + path.lstrip("/")
    if not path_allowed(target):
        raise HTTPException(status_code=403, detail="این مسیر روی نود مجاز نیست")

    try:
        declared = int(request.headers.get("content-length") or 0)
    except ValueError:
        declared = 0
    if declared > MAX_FORWARD_BODY:
        raise HTTPException(status_code=413, detail="حجم درخواست زیاد است")
    body = await request.body()
    if len(body) > MAX_FORWARD_BODY:
        raise HTTPException(status_code=413, detail="حجم درخواست زیاد است")

    url = node["url"] + quote(target, safe="/:@!$&'()*+,;=-._~")
    if request.url.query:
        url += "?" + request.url.query
    headers = _auth_headers(node.get("token", ""))
    if body:
        headers["Content-Type"] = request.headers.get("content-type", "application/json")

    try:
        r = await _http().request(request.method, url, content=body or None, headers=headers, timeout=FORWARD_TIMEOUT)
    except httpx.TimeoutException:
        return JSONResponse({"detail": f"نود «{node['name']}» در زمان تعیین‌شده جواب نداد"}, status_code=504)
    except httpx.HTTPError:
        return JSONResponse({"detail": f"اتصال به نود «{node['name']}» برقرار نشد"}, status_code=502)

    if r.status_code in (401, 403):
        # خطای احراز هویت نود نباید شبیه «خروج از پنل اصلی» رفتار کنه
        return JSONResponse({"detail": "توکن نود نامعتبر است یا این عملیات روی نود مجاز نیست"}, status_code=502)

    out_headers = {}
    if r.headers.get("content-disposition"):
        out_headers["content-disposition"] = r.headers["content-disposition"]
    return Response(content=r.content, status_code=r.status_code, media_type=r.headers.get("content-type"), headers=out_headers)
