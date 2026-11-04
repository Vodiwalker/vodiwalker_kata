# tg_proxy.py — VodiWalker Telegram Proxy Engine
# ------------------------------------------------------------------
# * MTProto proxy (obfuscated2 + "dd" secure/padded secret) — بدون هیچ ابزار خارجی
# * SOCKS5 مخصوص تلگرام (فقط به رنج IP تلگرام وصل می‌شود؛ پروکسی باز نیست)
# * هر «پروکسی» = یک secret (یا یوزر/پس) مستقل با حجم، انقضا، سقف اتصال و آمار
# * همه‌ی پروکسی‌ها روی یک پورت مشترک سرو می‌شوند (مناسب هاست‌های تک‌پورتی)
# ------------------------------------------------------------------

import asyncio
import hashlib
import hmac
import ipaddress
import json
import os
import secrets
import struct
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

TG_DC_V4 = {1: "149.154.175.50", 2: "149.154.167.51", 3: "149.154.175.100",
            4: "149.154.167.91", 5: "149.154.171.5"}
TG_NETS = [ipaddress.ip_network(n) for n in (
    "149.154.160.0/20", "91.108.4.0/22", "91.108.8.0/22", "91.108.12.0/22",
    "91.108.16.0/22", "91.108.20.0/22", "91.108.56.0/22", "95.161.64.0/20",
    "185.76.151.0/24", "109.239.140.0/24")]
GOOD_TAGS = (b"\xdd\xdd\xdd\xdd", b"\xee\xee\xee\xee", b"\xef\xef\xef\xef")
FORBIDDEN_START = (b"HEAD", b"POST", b"GET ", b"OPTI", b"\xdd\xdd\xdd\xdd",
                   b"\xee\xee\xee\xee", b"\x16\x03\x01\x02")
GB = 1024 ** 3
TG_DC_PORT = int(os.environ.get("TG_DC_PORT_OVERRIDE", "443") or 443)   # فقط برای تست
if os.environ.get("TG_DC_HOST_OVERRIDE"):
    TG_DC_V4 = {k: os.environ["TG_DC_HOST_OVERRIDE"] for k in TG_DC_V4}


def _ctr(key: bytes, iv: bytes):
    return Cipher(algorithms.AES(key), modes.CTR(iv)).encryptor()


class TgProxyManager:
    def __init__(self, data_dir: Path, logger=None):
        self.file = Path(data_dir) / "tg_proxies.json"
        self.log = logger
        self.settings = {
            "enabled": True,
            "mt_port": int(os.environ.get("TG_PROXY_PORT", "8443") or 8443),
            "socks_port": int(os.environ.get("TG_SOCKS_PORT", "0") or 0),  # 0 = خاموش
            "public_host": os.environ.get("TG_PUBLIC_HOST", ""),
            "socks_tg_only": True,
            "share_panel_port": True,      # روی هاست‌های تک‌پورتی: MTProto روی همان پورت پنل
            "public_port": int(os.environ.get("TG_PUBLIC_PORT", "0") or 0),
            "default_created": False,
        }
        self.mux_active = False            # app.py آن را True می‌کند
        self.shared = False
        self.items: dict[str, dict] = {}
        self.live: dict[str, int] = {}          # id -> active connections
        self.errors: dict[str, str] = {}
        self._mt = None
        self._sk = None
        self._dirty = False
        self._task = None
        self._load()

    # ---------------- persistence ----------------
    def _load(self):
        try:
            d = json.loads(self.file.read_text(encoding="utf-8"))
            self.settings.update(d.get("settings") or {})
            self.items = d.get("items") or {}
        except Exception:
            pass

    def save(self):
        try:
            tmp = self.file.with_suffix(".tmp")
            tmp.write_text(json.dumps({"settings": self.settings, "items": self.items},
                                      ensure_ascii=False, indent=1), encoding="utf-8")
            os.replace(tmp, self.file)
            self._dirty = False
        except Exception as exc:
            self.log and self.log.warning("tg_proxy save failed: %s", exc)

    async def _flusher(self):
        while True:
            await asyncio.sleep(15)
            if self._dirty:
                self.save()

    # ---------------- lifecycle ----------------
    async def start(self):
        if self._task is None:
            self._task = asyncio.create_task(self._flusher())
        self.ensure_default()
        await self.restart_servers()

    def ensure_default(self):
        """یک پروکسی MTProto پیش‌فرض (نامحدود) فقط یک‌بار موقع اولین اجرا ساخته می‌شود."""
        if self.settings.get("default_created") or self.items:
            self.settings["default_created"] = True
            return
        px = self.create("mtproto", "Default Proxy · پیش‌فرض", 0, 0, 0, "پروکسی پیش‌فرض VodiWalker")
        px["default"] = True
        self.settings["default_created"] = True
        self.save()

    async def stop(self):
        if self._task:
            self._task.cancel()
            self._task = None
        await self._close_servers()
        self.save()

    async def _close_servers(self):
        for name in ("_mt", "_sk"):
            srv = getattr(self, name)
            if srv:
                srv.close()
                try:
                    await srv.wait_closed()
                except Exception:
                    pass
                setattr(self, name, None)

    async def restart_servers(self):
        await self._close_servers()
        self.errors = {}
        if not self.settings.get("enabled"):
            return
        mp = int(self.settings.get("mt_port") or 0)
        sp = int(self.settings.get("socks_port") or 0)
        self.shared = bool(self.mux_active and self.settings.get("share_panel_port", True))
        if self.shared:
            self.log and self.log.info("Telegram MTProto proxy shares the panel port (single-port mode)")
        elif mp:
            try:
                self._mt = await asyncio.start_server(self._handle_mt, "0.0.0.0", mp)
                self.log and self.log.info("Telegram MTProto proxy listening on :%s", mp)
            except Exception as exc:
                self.errors["mtproto"] = f"پورت {mp} قابل باز شدن نیست: {exc}"
        if sp:
            try:
                self._sk = await asyncio.start_server(self._handle_socks, "0.0.0.0", sp)
                self.log and self.log.info("Telegram SOCKS5 proxy listening on :%s", sp)
            except Exception as exc:
                self.errors["socks"] = f"پورت {sp} قابل باز شدن نیست: {exc}"

    # ---------------- helpers ----------------
    @staticmethod
    def _expired(px: dict) -> bool:
        exp = px.get("expires_at")
        if not exp:
            return False
        try:
            return datetime.fromisoformat(exp) < datetime.now()
        except Exception:
            return False

    def usable(self, px: dict) -> bool:
        if not px.get("enabled", True) or self._expired(px):
            return False
        lim = int(px.get("limit_bytes") or 0)
        return not (lim and int(px.get("used_bytes") or 0) >= lim)

    def _account(self, px: dict, n: int):
        px["used_bytes"] = int(px.get("used_bytes") or 0) + n
        px["last_seen"] = datetime.now().isoformat(timespec="seconds")
        self._dirty = True

    def _slot(self, px: dict) -> bool:
        mc = int(px.get("max_conn") or 0)
        if mc and self.live.get(px["id"], 0) >= mc:
            return False
        self.live[px["id"]] = self.live.get(px["id"], 0) + 1
        return True

    def _release(self, px: dict):
        self.live[px["id"]] = max(0, self.live.get(px["id"], 1) - 1)

    @staticmethod
    async def _close(*ws):
        for w in ws:
            try:
                w.close()
                await w.wait_closed()
            except Exception:
                pass

    # ---------------- MTProto ----------------
    def _match(self, init: bytes):
        for px in self.items.values():
            if px.get("kind") != "mtproto" or not self.usable(px):
                continue
            try:
                sec = bytes.fromhex(px["secret"])
            except Exception:
                continue
            dec_key = hashlib.sha256(init[8:40] + sec).digest()
            rev = init[8:56][::-1]
            enc_key = hashlib.sha256(rev[:32] + sec).digest()
            dec = _ctr(dec_key, init[40:56])
            plain = dec.update(init)
            if plain[56:60] in GOOD_TAGS:
                dc = struct.unpack("<h", plain[60:62])[0]
                if 1 <= abs(dc) <= 5:
                    return px, dec, _ctr(enc_key, rev[32:48]), plain[56:60], dc
        return None

    async def _handle_mt(self, reader, writer):
        up = None
        try:
            init = await asyncio.wait_for(reader.readexactly(64), 10)
            m = self._match(init)
            if not m:
                await asyncio.sleep(1.0)
                return
            px, dec, enc, tag, dc = m
            if not self._slot(px):
                return
            up = px
            ur, uw = await asyncio.wait_for(
                asyncio.open_connection(TG_DC_V4[abs(dc)], TG_DC_PORT), 10)
            while True:
                rnd = bytearray(os.urandom(64))
                if rnd[0] == 0xEF or bytes(rnd[:4]) in FORBIDDEN_START or rnd[4:8] == b"\0\0\0\0":
                    continue
                break
            rnd[56:60] = tag
            rnd[60:62] = struct.pack("<h", dc)
            rev = bytes(rnd[8:56])[::-1]
            dc_enc = _ctr(bytes(rnd[8:40]), bytes(rnd[40:56]))
            dc_dec = _ctr(rev[:32], rev[32:48])
            sealed = dc_enc.update(bytes(rnd))
            uw.write(bytes(rnd[:56]) + sealed[56:64])
            await uw.drain()

            async def c2d():
                while True:
                    data = await reader.read(16384)
                    if not data:
                        break
                    uw.write(dc_enc.update(dec.update(data)))
                    await uw.drain()
                    self._account(px, len(data))
                    if not self.usable(px):
                        break

            async def d2c():
                while True:
                    data = await ur.read(16384)
                    if not data:
                        break
                    writer.write(enc.update(dc_dec.update(data)))
                    await writer.drain()
                    self._account(px, len(data))
                    if not self.usable(px):
                        break

            t1, t2 = asyncio.ensure_future(c2d()), asyncio.ensure_future(d2c())
            await asyncio.wait({t1, t2}, return_when=asyncio.FIRST_COMPLETED)
            for t in (t1, t2):
                t.cancel()
            await self._close(uw)
        except Exception:
            pass
        finally:
            if up:
                self._release(up)
            await self._close(writer)

    # ---------------- SOCKS5 (Telegram only) ----------------
    def _find_socks(self, user: str, pw: str):
        for px in self.items.values():
            if px.get("kind") == "socks" and self.usable(px) \
                    and hmac.compare_digest(px.get("user", ""), user) \
                    and hmac.compare_digest(px.get("password", ""), pw):
                return px
        return None

    def _tg_ok(self, host: str) -> bool:
        if not self.settings.get("socks_tg_only", True):
            return True
        try:
            ip = ipaddress.ip_address(host)
            return any(ip in n for n in TG_NETS)
        except ValueError:
            h = host.lower()
            return h.endswith((".telegram.org", ".t.me", ".telegra.ph")) or h in ("telegram.org", "t.me")

    async def _handle_socks(self, reader, writer):
        px = None
        try:
            v, n = await asyncio.wait_for(reader.readexactly(2), 10)
            if v != 5:
                return
            methods = await reader.readexactly(n)
            if 2 not in methods:
                writer.write(b"\x05\xff")
                return
            writer.write(b"\x05\x02")
            await writer.drain()
            if (await reader.readexactly(1)) != b"\x01":
                return
            ul = (await reader.readexactly(1))[0]
            user = (await reader.readexactly(ul)).decode("utf-8", "ignore")
            pl = (await reader.readexactly(1))[0]
            pw = (await reader.readexactly(pl)).decode("utf-8", "ignore")
            px = self._find_socks(user, pw)
            if not px or not self._slot(px):
                writer.write(b"\x01\x01")
                px = None
                return
            writer.write(b"\x01\x00")
            _, cmd, _, atyp = await reader.readexactly(4)
            if atyp == 1:
                host = str(ipaddress.ip_address(await reader.readexactly(4)))
            elif atyp == 4:
                host = str(ipaddress.ip_address(await reader.readexactly(16)))
            elif atyp == 3:
                ln = (await reader.readexactly(1))[0]
                host = (await reader.readexactly(ln)).decode("ascii", "ignore")
            else:
                return
            port = struct.unpack(">H", await reader.readexactly(2))[0]
            if cmd != 1 or not self._tg_ok(host):
                writer.write(b"\x05\x02\x00\x01\0\0\0\0\0\0")
                return
            ur, uw = await asyncio.wait_for(asyncio.open_connection(host, port), 10)
            writer.write(b"\x05\x00\x00\x01\0\0\0\0\0\0")
            await writer.drain()

            async def pipe(r, w):
                while True:
                    data = await r.read(16384)
                    if not data:
                        break
                    w.write(data)
                    await w.drain()
                    self._account(px, len(data))
                    if not self.usable(px):
                        break

            t1, t2 = asyncio.ensure_future(pipe(reader, uw)), asyncio.ensure_future(pipe(ur, writer))
            await asyncio.wait({t1, t2}, return_when=asyncio.FIRST_COMPLETED)
            for t in (t1, t2):
                t.cancel()
            await self._close(uw)
        except Exception:
            pass
        finally:
            if px:
                self._release(px)
            await self._close(writer)

    # ---------------- حالت خودکار ----------------
    AUTO_PORTS = (443, 8443, 2053, 2083, 2087, 2096, 8080)

    async def _probe_dcs(self):
        async def probe(dc, ip):
            t0 = time.perf_counter()
            try:
                _r, w = await asyncio.wait_for(asyncio.open_connection(ip, TG_DC_PORT), 4)
                w.close()
                return {"dc": dc, "ok": True, "ms": round((time.perf_counter() - t0) * 1000)}
            except Exception as exc:
                return {"dc": dc, "ok": False, "err": type(exc).__name__}
        return await asyncio.gather(*[probe(k, v) for k, v in TG_DC_V4.items()])

    @staticmethod
    async def _can_bind(port: int) -> bool:
        try:
            srv = await asyncio.start_server(lambda r, w: None, "0.0.0.0", port)
            srv.close()
            await srv.wait_closed()
            return True
        except Exception:
            return False

    async def auto_setup(self, req_port: int, https: bool, fresh: bool = False) -> dict:
        """بهترین حالت ممکن را خودش انتخاب و راه‌اندازی می‌کند و یک پروکسی آماده برمی‌گرداند."""
        steps = []
        s = self.settings
        dcs = await self._probe_dcs()
        okd = [d for d in dcs if d["ok"]]
        avg = round(sum(d["ms"] for d in okd) / len(okd)) if okd else 0
        steps.append({"k": "dc", "ok": bool(okd), "text": f"اتصال سرور به دیتاسنترهای تلگرام: {len(okd)} از {len(dcs)}" + (f" · میانگین {avg}ms" if okd else " — هاست خروجی تلگرام را بسته است"), "dcs": dcs})
        s["enabled"] = True
        mode = "shared"
        if self.mux_active:
            s["share_panel_port"] = True
            if not req_port and not int(s.get("public_port") or 0):
                s["public_port"] = 443 if https else 80
            steps.append({"k": "port", "ok": True, "text": "تک‌پورتی روی پورت پنل فعال شد (بدون نیاز به پورت اضافه)"})
        else:
            mode = "dedicated"
            s["share_panel_port"] = False
            cur = int(s.get("mt_port") or 0)
            port = 0
            if cur and self._mt is not None:
                port = cur
            else:
                for p in ([cur] if cur else []) + [x for x in self.AUTO_PORTS if x != cur]:
                    if await self._can_bind(p):
                        port = p
                        break
            if port:
                s["mt_port"] = port
                s["public_port"] = 0
            steps.append({"k": "port", "ok": bool(port), "text": f"بهترین پورت آزاد انتخاب شد: {port}" if port else "هیچ پورت آزادی پیدا نشد؛ از پنل هاست یک پورت باز کن"})
        await self.restart_servers()
        listening = bool(self._mt) or self.shared
        steps.append({"k": "listen", "ok": listening, "text": "سرور MTProto در حال اجراست" if listening else "سرور MTProto بالا نیامد"})
        px = None
        if not fresh:
            for x in self.items.values():
                if x.get("kind") == "mtproto" and (x.get("auto") or x.get("default")) and self.usable(x):
                    px = x
                    break
        if px is None:
            px = self.create("mtproto", "Auto · " + datetime.now().strftime("%m-%d %H:%M"), 0, 0, 0, "ساخته‌شده با حالت خودکار")
            px["auto"] = True
            steps.append({"k": "secret", "ok": True, "text": "secret اختصاصی (dd · padded) ساخته شد"})
        else:
            steps.append({"k": "secret", "ok": True, "text": "از پروکسی خودکار قبلی استفاده شد"})
        self.save()
        return {"mode": mode, "steps": steps, "healthy": bool(okd) and listening, "px": px}

    # ---------------- CRUD ----------------
    def create(self, kind: str, label: str, limit_gb: float, days: int, max_conn: int, note: str = ""):
        kind = "socks" if kind == "socks" else "mtproto"
        pid = uuid.uuid4().hex[:10]
        px = {
            "id": pid, "kind": kind, "label": (label or f"Proxy {len(self.items)+1}")[:60],
            "enabled": True, "created_at": datetime.now().isoformat(timespec="seconds"),
            "expires_at": (datetime.now() + timedelta(days=days)).isoformat(timespec="seconds") if days > 0 else None,
            "limit_bytes": int(limit_gb * GB) if limit_gb > 0 else 0,
            "used_bytes": 0, "max_conn": max(0, int(max_conn)), "note": note[:200],
        }
        if kind == "mtproto":
            px["secret"] = secrets.token_hex(16)
        else:
            px["user"] = "u" + secrets.token_hex(4)
            px["password"] = secrets.token_urlsafe(9)
        self.items[pid] = px
        self.save()
        return px

    def eff_port(self, req_port: int = 0) -> int:
        pp = int(self.settings.get("public_port") or 0)
        if pp:
            return pp
        if self.shared and req_port:
            return req_port
        return int(self.settings.get("mt_port") or 0)

    def public(self, px: dict, host: str, req_port: int = 0) -> dict:
        d = {k: v for k, v in px.items() if k not in ("secret", "password")}
        d["usable"] = self.usable(px)
        d["live"] = self.live.get(px["id"], 0)
        d["links"] = self.links(px, host, req_port)
        d["expired"] = self._expired(px)
        return d

    def links(self, px: dict, host: str, req_port: int = 0) -> dict:
        host = self.settings.get("public_host") or host
        if px["kind"] == "mtproto":
            port = self.eff_port(req_port)
            sec = "dd" + px["secret"]
            q = f"server={quote(host)}&port={port}&secret={sec}"
            return {"tg": f"tg://proxy?{q}", "web": f"https://t.me/proxy?{q}",
                    "server": host, "port": port, "secret": sec}
        port = int(self.settings.get("socks_port") or 0)
        q = f"server={quote(host)}&port={port}&user={quote(px['user'])}&pass={quote(px['password'])}"
        return {"tg": f"tg://socks?{q}", "web": f"https://t.me/socks?{q}", "server": host,
                "port": port, "user": px["user"], "password": px["password"]}


# ============================================================
# Single-port multiplexer: HTTP (پنل / VLESS-WS) و MTProto روی یک پورت
# ============================================================
HTTP_PREFIXES = (b"GET ", b"POST", b"PUT ", b"HEAD", b"DELE", b"OPTI", b"PATC",
                 b"CONN", b"TRAC", b"PRI ")


class MuxProtocol(asyncio.Protocol):
    """بایت‌های اول اتصال را می‌بیند: HTTP → به uvicorn؛ غیر HTTP → MTProto."""

    def __init__(self, inner_factory, mgr):
        self._factory, self._mgr = inner_factory, mgr
        self._inner = self._reader = self._writer = self._fc = None
        self._mode = None
        self._buf = b""
        self._t = None
        self._timer = None

    def connection_made(self, transport):
        self._t = transport
        self._timer = asyncio.get_event_loop().call_later(20, self._timeout)

    def _timeout(self):
        if self._mode is None and self._t is not None:
            self._t.close()

    def data_received(self, data):
        if self._mode == "http":
            return self._inner.data_received(data)
        if self._mode == "mt":
            return self._reader.feed_data(data)
        self._buf += data
        if len(self._buf) < 4:
            return
        if self._timer:
            self._timer.cancel()
        if self._buf[:4] in HTTP_PREFIXES or not self._mgr.shared:
            self._to_http()
        else:
            self._to_mt()

    def _to_http(self):
        self._mode = "http"
        self._inner = self._factory()
        self._inner.connection_made(self._t)
        b, self._buf = self._buf, b""
        self._inner.data_received(b)

    def _to_mt(self):
        self._mode = "mt"
        loop = asyncio.get_event_loop()
        self._reader = asyncio.StreamReader(limit=2 ** 17, loop=loop)
        self._reader.set_transport(self._t)
        self._fc = asyncio.streams.FlowControlMixin(loop=loop)
        self._writer = asyncio.StreamWriter(self._t, self._fc, self._reader, loop)
        self._reader.feed_data(self._buf)
        self._buf = b""
        asyncio.ensure_future(self._mgr._handle_mt(self._reader, self._writer))

    def connection_lost(self, exc):
        if self._timer:
            self._timer.cancel()
        if self._mode == "http":
            self._inner.connection_lost(exc)
        elif self._mode == "mt":
            self._reader.feed_eof()
            self._fc.connection_lost(exc)

    def eof_received(self):
        if self._mode == "http":
            return self._inner.eof_received()
        if self._mode == "mt":
            self._reader.feed_eof()
            return True
        return False

    def pause_writing(self):
        (self._inner if self._mode == "http" else self._fc).pause_writing() if self._mode else None

    def resume_writing(self):
        (self._inner if self._mode == "http" else self._fc).resume_writing() if self._mode else None


def attach_mux(app, config):
    """از app.py صدا زده می‌شود: کلاس پروتکل HTTP uvicorn را در MuxProtocol می‌پیچد."""
    mgr = getattr(app.state, "tg_proxy", None)
    if mgr is None:
        return False
    inner = config.http_protocol_class

    def factory(*a, **kw):
        return MuxProtocol(lambda: inner(*a, **kw), mgr)

    config.http_protocol_class = factory
    mgr.mux_active = True
    return True


# ============================================================
# FastAPI integration
# ============================================================
def register(app, require_auth, data_dir, logger=None):
    from fastapi import Depends, HTTPException, Request

    mgr = TgProxyManager(data_dir, logger)
    app.state.tg_proxy = mgr

    def host_of(request: Request) -> str:
        h = request.headers.get("x-forwarded-host") or request.headers.get("host") or "localhost"
        return h.split(",")[0].strip().rsplit(":", 1)[0] if not h.startswith("[") else h

    def port_of(request: Request) -> int:
        h = (request.headers.get("x-forwarded-host") or request.headers.get("host") or "").split(",")[0].strip()
        if h and not h.startswith("[") and ":" in h:
            try:
                return int(h.rsplit(":", 1)[1])
            except ValueError:
                return 0
        return 0

    @app.on_event("startup")
    async def _tg_start():
        await mgr.start()

    @app.on_event("shutdown")
    async def _tg_stop():
        await mgr.stop()

    @app.get("/api/tgproxy")
    async def tg_list(request: Request, _=Depends(require_auth)):
        host = host_of(request)
        items = sorted(mgr.items.values(), key=lambda x: x.get("created_at", ""), reverse=True)
        tot = sum(int(x.get("used_bytes") or 0) for x in items)
        return {"ok": True, "settings": mgr.settings, "errors": mgr.errors, "host": host,
                "running": {"mtproto": (mgr._mt is not None) or mgr.shared, "socks": mgr._sk is not None, "shared": mgr.shared},
                "stats": {"total": len(items), "active": sum(1 for x in items if mgr.usable(x)),
                          "live": sum(mgr.live.values()), "used_bytes": tot},
                "items": [mgr.public(x, host, port_of(request)) for x in items]}

    @app.get("/api/tgproxy-selftest")
    async def tg_selftest(request: Request, _=Depends(require_auth)):
        async def probe(dc, ip):
            t0 = time.perf_counter()
            try:
                r, w = await asyncio.wait_for(asyncio.open_connection(ip, TG_DC_PORT), 4)
                w.close()
                return {"dc": dc, "ok": True, "ms": round((time.perf_counter() - t0) * 1000)}
            except Exception as exc:
                return {"dc": dc, "ok": False, "err": type(exc).__name__}
        dcs = await asyncio.gather(*[probe(k, v) for k, v in TG_DC_V4.items()])
        rp = port_of(request)
        tips = []
        if not any(d["ok"] for d in dcs):
            tips.append("سرور به دیتاسنترهای تلگرام وصل نمی‌شود؛ هاست خروجی تلگرام را بسته است. روی چنین هاستی MTProto کار نمی‌کند.")
        if mgr.shared and not rp and not mgr.settings.get("public_port"):
            tips.append("آدرس پنل پورت ندارد (احتمالاً پشت HTTPS/پروکسی است). در تنظیمات «پورت عمومی» را دستی بده یا اشتراک پورت را خاموش و پورت جدا باز کن.")
        if not mgr.shared and not mgr._mt:
            tips.append("پورت MTProto باز نشده است؛ خطای پورت را در بالای صفحه ببین.")
        if not mgr.mux_active:
            tips.append("پنل با «python app.py» اجرا نشده؛ حالت تک‌پورتی فعال نیست (برنامه را با app.py اجرا کن).")
        return {"ok": True, "dcs": dcs, "shared": mgr.shared, "mux_active": mgr.mux_active,
                "listening": bool(mgr._mt) or mgr.shared, "link_port": mgr.eff_port(rp), "tips": tips}

    @app.post("/api/tgproxy")
    async def tg_create(request: Request, _=Depends(require_auth)):
        b = await request.json()
        px = mgr.create(b.get("kind", "mtproto"), str(b.get("label") or ""),
                        float(b.get("limit_gb") or 0), int(b.get("days") or 0),
                        int(b.get("max_conn") or 0), str(b.get("note") or ""))
        if px["kind"] == "socks" and not int(mgr.settings.get("socks_port") or 0):
            raise_msg = "پورت SOCKS5 تنظیم نشده؛ از «تنظیمات پروکسی» یک پورت بده."
            return {"ok": True, "warning": raise_msg, "item": mgr.public(px, host_of(request), port_of(request))}
        return {"ok": True, "item": mgr.public(px, host_of(request), port_of(request))}

    @app.post("/api/tgproxy/auto")
    async def tg_auto(request: Request, _=Depends(require_auth)):
        try:
            b = await request.json()
        except Exception:
            b = {}
        https = (request.headers.get("x-forwarded-proto") or request.url.scheme or "").split(",")[0].strip() == "https"
        res = await mgr.auto_setup(port_of(request), https, bool((b or {}).get("fresh")))
        px = res.pop("px")
        res["item"] = mgr.public(px, host_of(request), port_of(request))
        res["ok"] = True
        return res

    @app.patch("/api/tgproxy/{pid}")
    async def tg_edit(pid: str, request: Request, _=Depends(require_auth)):
        px = mgr.items.get(pid)
        if not px:
            raise HTTPException(404, "پروکسی پیدا نشد")
        b = await request.json()
        if "enabled" in b:
            px["enabled"] = bool(b["enabled"])
        if "label" in b:
            px["label"] = str(b["label"])[:60]
        if "limit_gb" in b:
            px["limit_bytes"] = int(float(b["limit_gb"] or 0) * GB)
        if "days" in b:
            d = int(b["days"] or 0)
            px["expires_at"] = (datetime.now() + timedelta(days=d)).isoformat(timespec="seconds") if d > 0 else None
        if "max_conn" in b:
            px["max_conn"] = max(0, int(b["max_conn"] or 0))
        mgr.save()
        return {"ok": True, "item": mgr.public(px, host_of(request), port_of(request))}

    @app.post("/api/tgproxy/{pid}/reset")
    async def tg_reset(pid: str, request: Request, _=Depends(require_auth)):
        px = mgr.items.get(pid)
        if not px:
            raise HTTPException(404, "پروکسی پیدا نشد")
        px["used_bytes"] = 0
        mgr.save()
        return {"ok": True}

    @app.post("/api/tgproxy/{pid}/regenerate")
    async def tg_regen(pid: str, request: Request, _=Depends(require_auth)):
        px = mgr.items.get(pid)
        if not px:
            raise HTTPException(404, "پروکسی پیدا نشد")
        if px["kind"] == "mtproto":
            px["secret"] = secrets.token_hex(16)
        else:
            px["password"] = secrets.token_urlsafe(9)
        mgr.save()
        return {"ok": True, "item": mgr.public(px, host_of(request), port_of(request))}

    @app.delete("/api/tgproxy/{pid}")
    async def tg_delete(pid: str, _=Depends(require_auth)):
        if mgr.items.pop(pid, None) is None:
            raise HTTPException(404, "پروکسی پیدا نشد")
        mgr.save()
        return {"ok": True}

    @app.post("/api/tgproxy-settings")
    async def tg_settings(request: Request, _=Depends(require_auth)):
        b = await request.json()
        s = mgr.settings
        for k in ("mt_port", "socks_port"):
            if k in b:
                v = int(b[k] or 0)
                if v and not (1 <= v <= 65535):
                    raise HTTPException(400, "پورت نامعتبر است")
                s[k] = v
        if "public_host" in b:
            s["public_host"] = str(b["public_host"] or "").strip()[:200]
        if "enabled" in b:
            s["enabled"] = bool(b["enabled"])
        if "share_panel_port" in b:
            s["share_panel_port"] = bool(b["share_panel_port"])
        if "public_port" in b:
            v = int(b["public_port"] or 0)
            if v and not (1 <= v <= 65535):
                raise HTTPException(400, "پورت نامعتبر است")
            s["public_port"] = v
        if "socks_tg_only" in b:
            s["socks_tg_only"] = bool(b["socks_tg_only"])
        mgr.save()
        await mgr.restart_servers()
        return {"ok": True, "settings": s, "errors": mgr.errors}

    return mgr
