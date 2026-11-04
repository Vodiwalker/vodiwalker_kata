import asyncio
import os
import re

import httpx

from datetime import datetime, timedelta

from main import (
    LINKS,
    make_link,
    remove_link,
    set_link_active,
    vless_link_for_link,
    get_host,
    fmt_bytes,
    is_link_allowed,
    logger,
    PROTOCOLS,
    DEFAULT_PROTOCOL,
    FINGERPRINTS,
    DEFAULT_FINGERPRINT,
    DEFAULT_ALPN_BY_PROTOCOL,
    DEFAULT_PORT,
    DEFAULT_SPEED_LIMIT,
    MIN_PORT,
    MAX_PORT,
    parse_size_to_bytes,
    parse_speed_to_bytes,
    SUBS,
    create_sub_group,
    set_link_sub,
    remove_sub_group,
    get_bot_text,
    add_client_to_inbound,
    remove_inbound_client,
    LIVE_PROTOCOLS,
    CONFIG,
    DATA_FILE,
    save_state,
    unique_ips_for_uuid,
    get_public_host_strict,
    get_public_base,
    _split_base_url,
    _is_real_public_host,
    decorate_label,
    auto_display_name,
    style_config_name,
    get_support_username,
    update_link_fields,
)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
_admin_ids_raw = os.environ.get("TELEGRAM_ADMIN_IDS", "").strip()
ADMIN_IDS = {int(x) for x in _admin_ids_raw.replace(" ", "").split(",") if x.isdigit()} if _admin_ids_raw else set()

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"


def configure(token: str = None, admin_ids_raw: str = None):
    """توکن/آیدی‌ ادمین‌های ربات رو در زمان اجرا (مثلاً از تنظیمات پنل وب) تغییر می‌ده.
    اگر ربات در حال اجرا باشه، لازمه بعدش stop_bot() و start_bot() دوباره صدا زده بشه
    تا تغییرات اعمال بشه (این کار در روت /api/settings انجام می‌شه)."""
    global BOT_TOKEN, API_BASE, ADMIN_IDS
    if token is not None:
        BOT_TOKEN = (token or "").strip()
        API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
    if admin_ids_raw is not None:
        raw = (admin_ids_raw or "").strip()
        ADMIN_IDS = {int(x) for x in raw.replace(" ", "").split(",") if x.isdigit()} if raw else set()


def is_running() -> bool:
    return bool(_running)


def current_config() -> dict:
    return {
        "bot_token": BOT_TOKEN,
        "admin_ids": ",".join(str(x) for x in sorted(ADMIN_IDS)),
        "running": is_running(),
    }
PAGE_SIZE = 6

_client: httpx.AsyncClient | None = None
_poll_task: asyncio.Task | None = None
_running = False
_pending: dict = {}   # chat_id -> {"action": "wizard", "step": "...", "data": {...}}

# ── Config creation wizard ────────────────────────────────────────────────────
# مراحل ساخت کانفیگ جدید، دقیقاً هم‌راستا با فیلدهایی که پنل وب موقع ساخت کاربر می‌گیره:
# برچسب، پروتکل، fingerprint، ALPN، پورت، محدودیت حجم، محدودیت سرعت، محدودیت آی‌پی، روز انقضا.
WIZARD_STEPS = ["label", "protocol", "fingerprint", "alpn", "port", "volume", "speed", "iplimit", "days"]

PROTOCOL_LABELS = {
    "vless-ws": "VLESS + WebSocket",
    "vless-tcp": "VLESS + TCP (خام)",
    "xhttp-packet-up": "XHTTP (packet-up)",
    "xhttp-stream-up": "XHTTP (stream-up)",
    "xhttp-stream-one": "XHTTP (stream-one)",
    "vmess-ws": "VMess + WebSocket",
    "trojan-ws": "Trojan + WebSocket",
}

def _protocol_label(p: str) -> str:
    label = PROTOCOL_LABELS.get(p, p)
    if p not in LIVE_PROTOCOLS:
        label += " 🔗"
    return label

import html as _html_mod

def _h(text) -> str:
    """برچسب/نام‌هایی که خودِ ادمین آزادانه تایپ می‌کنه (مثلاً می‌تونن '<' یا '&' داشته باشن)
    رو قبل از قرار گرفتن توی پیام‌های parse_mode=HTML امن می‌کنه؛ وگرنه تلگرام کل پیام رو
    رد می‌کنه (400 Bad Request: can't parse entities) و ادمین هیچ خروجی‌ای نمی‌بینه."""
    return _html_mod.escape(str(text if text is not None else ""), quote=False)

def _fp_label(fp: str) -> str:
    return fp.capitalize()

_VOLUME_RE = re.compile(r"^([\d.]+)\s*(GB|MB|KB)?$", re.IGNORECASE)
_SPEED_RE = re.compile(r"^([\d.]+)\s*(MBIT|MBPS|MB|KB)?$", re.IGNORECASE)

def _parse_volume_text(text: str):
    """ورودی مثل '10GB' یا '500 MB' رو به بایت تبدیل می‌کنه. اگه نامعتبر بود None برمی‌گردونه."""
    m = _VOLUME_RE.match(text.strip())
    if not m:
        return None
    try:
        value = float(m.group(1))
    except ValueError:
        return None
    if value <= 0:
        return 0
    unit = (m.group(2) or "GB").upper()
    return parse_size_to_bytes(value, unit)

def _parse_speed_text(text: str):
    """ورودی مثل '20' یا '20Mbit' رو به بایت‌بر‌ثانیه تبدیل می‌کنه (پیش‌فرض واحد Mbit)."""
    m = _SPEED_RE.match(text.strip())
    if not m:
        return None
    try:
        value = float(m.group(1))
    except ValueError:
        return None
    if value <= 0:
        return 0
    unit_raw = (m.group(2) or "MBIT").upper()
    unit = "MBIT" if unit_raw in ("MBIT", "MBPS") else unit_raw
    return parse_speed_to_bytes(value, unit)

def _parse_nonneg_int(text: str):
    try:
        n = int(text.strip())
    except ValueError:
        return None
    return max(0, n)

# ── Telegram API helpers ────────────────────────────────────────────────────
async def _call(method: str, **params):
    if _client is None:
        return None
    try:
        r = await _client.post(f"{API_BASE}/{method}", json=params, timeout=40)
        data = r.json()
        if not data.get("ok"):
            logger.warning(f"Telegram API {method} failed: {data}")
        return data
    except Exception as e:
        logger.warning(f"Telegram API {method} error: {e}")
        return None

async def _send(chat_id: int, text: str, kb: dict | None = None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    if kb:
        payload["reply_markup"] = kb
    return await _call("sendMessage", **payload)

async def _edit(chat_id: int, message_id: int, text: str, kb: dict | None = None):
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    if kb:
        payload["reply_markup"] = kb
    res = await _call("editMessageText", **payload)
    if res and not res.get("ok") and "not modified" in str(res.get("description", "")).lower():
        return
    if res is None or not res.get("ok"):
        # اگه ادیت به هر دلیلی نشد (مثلاً پیام قدیمی/حذف‌شده)، پیام جدید بفرست
        await _send(chat_id, text, kb)

async def _answer_cb(cb_id: str, text: str = ""):
    await _call("answerCallbackQuery", callback_query_id=cb_id, text=text)

def _is_admin(chat_id: int) -> bool:
    return chat_id in ADMIN_IDS

# ── Keyboards ────────────────────────────────────────────────────────────────
def _tma_url():
    base = get_public_base()
    return f"{base}/app" if base and base.startswith("https://") else None


async def _set_menu_button():
    url = _tma_url()
    if url:
        await _call("setChatMenuButton", menu_button={"type": "web_app", "text": "🚀 مینی‌اپ", "web_app": {"url": url}})


def _main_menu_kb():
    _tma = _tma_url()
    return {"inline_keyboard": [
        *([[{"text": "🚀 باز کردن مینی‌اپ VodiWalker", "web_app": {"url": _tma}}]] if _tma else []),
        [{"text": "⚡ ساخت سریع کانفیگ", "callback_data": "quick"}, {"text": "🧩 ساخت پیشرفته", "callback_data": "newcfg"}],
        [{"text": "📋 لیست کانفیگ‌ها", "callback_data": "list:0"}, {"text": "🗂 گروه‌های ساب", "callback_data": "subs:0"}],
        [{"text": "🟢 آنلاین‌ها", "callback_data": "online"}, {"text": "🔥 پرمصرف‌ها", "callback_data": "top"}, {"text": "⏳ نزدیک انقضا", "callback_data": "expiring"}],
        [{"text": "📊 آمار", "callback_data": "stats"}, {"text": "🖥 سرور", "callback_data": "server"}, {"text": "💾 بکاپ", "callback_data": "backup"}],
        [{"text": _alerts_label(), "callback_data": "alerts:toggle"}, {"text": "📖 راهنما", "callback_data": "help"}],
        [{"text": "🔄 رفرش", "callback_data": "menu"}],
    ]}

def _links_list_kb(page: int):
    items = sorted(LINKS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    total = len(items)
    start = page * PAGE_SIZE
    chunk = items[start:start + PAGE_SIZE]
    rows = []
    for uid, l in chunk:
        dot = "🟢" if is_link_allowed(l) else "🔴"
        rows.append([{"text": f"{dot} {l.get('label','?')[:28]}", "callback_data": f"view:{uid}"}])
    nav = []
    if start > 0:
        nav.append({"text": "◀ قبلی", "callback_data": f"list:{page-1}"})
    if start + PAGE_SIZE < total:
        nav.append({"text": "بعدی ▶", "callback_data": f"list:{page+1}"})
    if nav:
        rows.append(nav)
    rows.append([{"text": "➕ ساخت کانفیگ جدید", "callback_data": "newcfg"}])
    rows.append([{"text": "⬅ منوی اصلی", "callback_data": "menu"}])
    return {"inline_keyboard": rows}

def _link_detail_kb(uid: str, active: bool):
    return {"inline_keyboard": [
        [{"text": "🔗 لینک اتصال + QR", "callback_data": f"link:{uid}"}, {"text": "✏️ ویرایش", "callback_data": f"edit:{uid}"}],
        [{"text": "👥 کاربران این اینباند", "callback_data": f"clients:{uid}:0"}],
        [{"text": "🗂 گروه ساب (لینک حرفه‌ای)", "callback_data": f"cfggroup:{uid}"}],
        [{"text": ("⛔ غیرفعال‌سازی" if active else "✅ فعال‌سازی"), "callback_data": f"toggle:{uid}"}],
        [{"text": "🗑 حذف کانفیگ", "callback_data": f"del:{uid}"}],
        [{"text": "⬅ بازگشت به لیست", "callback_data": "list:0"}],
    ]}

# ── Client (user) management under an inbound ────────────────────────────────
def _clients_list_kb(parent_uid: str, page: int = 0):
    children = [(cid, l) for cid, l in LINKS.items() if l.get("parent_inbound_id") == parent_uid]
    children.sort(key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    total = len(children)
    start = page * PAGE_SIZE
    chunk = children[start:start + PAGE_SIZE]
    rows = []
    for cid, l in chunk:
        dot = "🟢" if is_link_allowed(l) else "🔴"
        rows.append([
            {"text": f"{dot} {l.get('label','?')[:24]}", "callback_data": f"view:{cid}"},
            {"text": "🗑", "callback_data": f"delclient:{cid}"},
        ])
    nav = []
    if start > 0:
        nav.append({"text": "◀ قبلی", "callback_data": f"clients:{parent_uid}:{page-1}"})
    if start + PAGE_SIZE < total:
        nav.append({"text": "بعدی ▶", "callback_data": f"clients:{parent_uid}:{page+1}"})
    if nav:
        rows.append(nav)
    rows.append([{"text": "➕ افزودن کاربر جدید", "callback_data": f"addclient:{parent_uid}"}])
    rows.append([{"text": "⬅ بازگشت به اینباند", "callback_data": f"view:{parent_uid}"}])
    return {"inline_keyboard": rows}

def _format_clients_list(parent_uid: str) -> str:
    parent = LINKS.get(parent_uid)
    children = [l for l in LINKS.values() if l.get("parent_inbound_id") == parent_uid]
    lines = [f"👥 <b>کاربران اینباند «{_h(parent.get('label','?')) if parent else '؟'}»</b>", f"تعداد کاربر: {len(children)}"]
    limit = int((parent or {}).get("client_limit") or 0)
    if limit:
        lines.append(f"ظرفیت مجاز: {limit}")
    if not children:
        lines.append("\nهنوز کاربری اضافه نشده. با دکمه‌ی زیر یک کاربر جدید بساز.")
    return "\n".join(lines)

def _confirm_delete_client_kb(parent_uid: str, client_id: str):
    return {"inline_keyboard": [
        [{"text": "✅ بله، حذف کن", "callback_data": f"delclientok:{client_id}"},
         {"text": "❌ انصراف", "callback_data": f"clients:{parent_uid}:0"}],
    ]}

def _wizard_client_prompt(step: str, data: dict) -> str:
    if step == "label":
        return "👤 نام/برچسب کاربر جدید رو بفرست:"
    if step == "volume":
        return "📦 سقف حجم این کاربر رو بفرست (مثل <code>10GB</code> یا <code>500MB</code>)، یا برای ارث‌بری از اینباند دکمه زیر رو بزن:"
    if step == "days":
        return "📅 چند روز اعتبار داشته باشه؟ یه عدد بفرست، یا برای ارث‌بری از انقضای اینباند دکمه زیر رو بزن:"
    if step == "confirm":
        limit_txt = fmt_bytes(data["limit_bytes"]) if data.get("limit_bytes") else "ارث‌بری از اینباند"
        days_txt = f"{data['expires_days']} روز" if data.get("expires_days") else "ارث‌بری از اینباند"
        return (f"📋 <b>پیش‌نمایش کاربر جدید</b>\n\n"
                f"برچسب: {_h(data.get('label'))}\n"
                f"حجم: {limit_txt}\n"
                f"انقضا: {days_txt}\n\n"
                f"تایید می‌کنی؟")
    return ""

def _wizard_client_cancel_kb():
    return {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "wc:cancel"}]]}

def _wizard_client_skip_kb(step_key: str, label: str):
    return {"inline_keyboard": [
        [{"text": label, "callback_data": f"wc:skip:{step_key}"}],
        [{"text": "❌ انصراف", "callback_data": "wc:cancel"}],
    ]}

def _wizard_client_confirm_kb():
    return {"inline_keyboard": [
        [{"text": "✅ ساخت کاربر", "callback_data": "wc:confirm"}],
        [{"text": "❌ انصراف", "callback_data": "wc:cancel"}],
    ]}

def _confirm_delete_kb(uid: str):
    return {"inline_keyboard": [
        [{"text": "✅ بله، حذف کن", "callback_data": f"delok:{uid}"},
         {"text": "❌ انصراف", "callback_data": f"view:{uid}"}],
    ]}

# ── Wizard keyboards ─────────────────────────────────────────────────────────
def _wizard_cancel_kb():
    return {"inline_keyboard": [[{"text": "❌ انصراف", "callback_data": "w:cancel"}]]}

def _wizard_label_kb():
    return {"inline_keyboard": [
        [{"text": "🎲 اسم خودکار خفن", "callback_data": "w:autolabel"}],
        [{"text": "❌ انصراف", "callback_data": "w:cancel"}],
    ]}

def _wizard_protocol_kb():
    rows = [[{"text": _protocol_label(p), "callback_data": f"w:proto:{p}"}] for p in PROTOCOLS]
    rows.append([{"text": "❌ انصراف", "callback_data": "w:cancel"}])
    return {"inline_keyboard": rows}

def _wizard_fp_kb():
    rows, row = [], []
    for fp in FINGERPRINTS:
        row.append({"text": _fp_label(fp), "callback_data": f"w:fp:{fp}"})
        if len(row) == 3:
            rows.append(row); row = []
    if row:
        rows.append(row)
    rows.append([{"text": "❌ انصراف", "callback_data": "w:cancel"}])
    return {"inline_keyboard": rows}

def _wizard_skip_kb(step_key: str, label: str):
    return {"inline_keyboard": [
        [{"text": label, "callback_data": f"w:skip:{step_key}"}],
        [{"text": "❌ انصراف", "callback_data": "w:cancel"}],
    ]}

ALPN_PRESET_MAP = {"p1": "http/1.1", "p2": "h2,http/1.1", "p3": "h2"}

def _wizard_alpn_kb():
    return {"inline_keyboard": [
        [{"text": "🔤 http/1.1 (پیشنهادی)", "callback_data": "w:alpnpreset:p1"}],
        [{"text": "🔤 h2,http/1.1", "callback_data": "w:alpnpreset:p2"}],
        [{"text": "🔤 h2", "callback_data": "w:alpnpreset:p3"}],
        [{"text": "⏭ پیش‌فرض پروتکل", "callback_data": "w:skip:alpn"}],
        [{"text": "❌ انصراف", "callback_data": "w:cancel"}],
    ]}

def _wizard_unlimited_kb(step_key: str):
    return _wizard_skip_kb(step_key, "♾ نامحدود")

def _wizard_confirm_kb():
    return {"inline_keyboard": [
        [{"text": "✅ ساخت کانفیگ", "callback_data": "w:confirm"}],
        [{"text": "❌ انصراف", "callback_data": "w:cancel"}],
    ]}

def _wizard_prompt(step: str, data: dict) -> str:
    n = WIZARD_STEPS.index(step) + 1 if step in WIZARD_STEPS else len(WIZARD_STEPS)
    head = f"🧩 ساخت کانفیگ جدید — مرحله {n}/{len(WIZARD_STEPS)}\n\n"
    if step == "label":
        return head + "✏️ اسم/برچسب کانفیگ رو بفرست (مثلاً <code>Vodiwalker</code> → <code>Vodiwalker|Tofan🚀</code>)\nیا اسم خودکار خفن رو بزن:"
    if step == "protocol":
        return head + "🌐 پروتکل رو از دکمه‌های زیر انتخاب کن:\n<i>🔗 یعنی این پروتکل فقط لینک/کانفیگ می‌سازه و خودِ این پنل بهش سرویس نمی‌ده (برای استفاده روی یک نود Xray-core جدا).</i>"
    if step == "fingerprint":
        return head + "🖐 Fingerprint (uTLS) رو انتخاب کن:"
    if step == "alpn":
        return head + ("🔤 ALPN رو از دکمه‌های زیر انتخاب کن (پیشنهادی: <code>http/1.1</code>)\n"
                        "یا خودت هر مقدار دلخواهی رو تایپ و ارسال کن (مثلاً h2,http/1.1):")
    if step == "port":
        return head + f"🔌 شماره پورت (بین {MIN_PORT} تا {MAX_PORT}) رو بفرست\nیا پیش‌فرض ({DEFAULT_PORT}) رو انتخاب کن:"
    if step == "volume":
        return head + "📦 محدودیت حجم مصرفی رو بفرست، مثلاً:\n<code>10GB</code> یا <code>500MB</code>\nیا دکمه‌ی نامحدود رو بزن:"
    if step == "speed":
        return head + "🚀 محدودیت سرعت رو به مگابیت‌بر‌ثانیه بفرست، مثلاً <code>20</code>\nیا دکمه‌ی نامحدود رو بزن:"
    if step == "iplimit":
        return head + "👥 حداکثر تعداد آی‌پی/کاربر هم‌زمان مجاز رو بفرست\nیا دکمه‌ی نامحدود رو بزن:"
    if step == "days":
        return head + "📅 تعداد روزهای اعتبار کانفیگ رو بفرست\nیا دکمه‌ی نامحدود (بدون انقضا) رو بزن:"
    return head

def _wizard_summary(data: dict) -> str:
    limit = "نامحدود" if not data.get("limit_bytes") else fmt_bytes(data["limit_bytes"])
    speed = "نامحدود" if not data.get("speed_limit_bytes") else f"{data['speed_limit_bytes']*8/1024/1024:.1f} Mbps"
    iplim = data.get("ip_limit", 0) or "نامحدود"
    days = data.get("expires_days", 0)
    days_txt = "بدون انقضا" if not days else f"{days} روز"
    proto = data.get("protocol", DEFAULT_PROTOCOL)
    alpn = data.get("alpn") or f"پیش‌فرض ({DEFAULT_ALPN_BY_PROTOCOL.get(proto, 'http/1.1')})"
    return (
        "🧩 خلاصه‌ی کانفیگ جدید — تایید کن:\n\n"
        f"برچسب: <b>{_h(data.get('label','?'))}</b>\n"
        f"پروتکل: {_protocol_label(proto)}\n"
        f"Fingerprint: {_fp_label(data.get('fingerprint', DEFAULT_FINGERPRINT))}\n"
        f"ALPN: {alpn}\n"
        f"پورت: {data.get('port', DEFAULT_PORT)}\n"
        f"محدودیت حجم: {limit}\n"
        f"محدودیت سرعت: {speed}\n"
        f"محدودیت آی‌پی: {iplim}\n"
        f"انقضا: {days_txt}"
    )

# ── View builders ────────────────────────────────────────────────────────────
def _format_detail(uid: str, l: dict) -> str:
    status = "🟢 فعال" if is_link_allowed(l) else "🔴 غیرفعال/منقضی"
    limit_bytes = l.get("limit_bytes") or 0
    used_bytes = l.get("used_bytes", 0)
    limit = "نامحدود" if not limit_bytes else fmt_bytes(limit_bytes)
    speed = "نامحدود" if not l.get("speed_limit_bytes") else f"{l['speed_limit_bytes']*8/1024/1024:.1f} Mbps"
    exp = l.get("expires_at")
    exp_txt = exp.split("T")[0] if exp else "بدون انقضا"
    proto = l.get("protocol", DEFAULT_PROTOCOL)
    alpn = l.get("alpn") or f"پیش‌فرض ({DEFAULT_ALPN_BY_PROTOCOL.get(proto, 'http/1.1')})"
    usage_line = f"مصرف: {fmt_bytes(used_bytes)} / {limit}"
    if limit_bytes:
        pct = min(100, round((used_bytes / limit_bytes) * 100, 1))
        usage_line += f"\n{_progress_bar(pct)}  {pct}%"
    dl = _days_left(l)
    dl_txt = "" if dl is None else (f" ({int(dl)} روز مانده)" if dl > 0 else " (منقضی)")
    return (
        f"<b>{_h(l.get('label','?'))}</b>\n"
        f"وضعیت: {status}\n"
        f"🟣 آنلاین همین الان: {_online_count(uid)}\n"
        f"نوع: {_live_badge(l)}\n"
        f"{usage_line}\n"
        f"محدودیت سرعت: {speed}\n"
        f"محدودیت آی‌پی: {l.get('ip_limit',0) or 'نامحدود'}\n"
        f"پروتکل: {_protocol_label(proto)}\n"
        f"Fingerprint: {_fp_label(l.get('fingerprint', DEFAULT_FINGERPRINT))}\n"
        f"ALPN: {alpn}\n"
        f"پورت: {l.get('port', DEFAULT_PORT)}\n"
        f"انقضا: {exp_txt}{dl_txt}\n"
        f"UUID: <code>{uid}</code>"
    )

# ── Sub-group (لینک ساب حرفه‌ای) view builders ────────────────────────────────
def _group_public_url(s: dict) -> str:
    base = get_public_base()
    if not base:
        return "⚠️ آدرس پنل نامشخص است (دستور /seturl)"
    return f"{base}/p/{s.get('uuid_key','')}"

def _subs_list_kb(page: int):
    items = sorted(SUBS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    total = len(items)
    start = page * PAGE_SIZE
    chunk = items[start:start + PAGE_SIZE]
    rows = []
    for sid, s in chunk:
        cnt = len(s.get("link_ids", []))
        rows.append([{"text": f"🗂 {s.get('name','?')[:26]} ({cnt})", "callback_data": f"subview:{sid}"}])
    nav = []
    if start > 0:
        nav.append({"text": "◀ قبلی", "callback_data": f"subs:{page-1}"})
    if start + PAGE_SIZE < total:
        nav.append({"text": "بعدی ▶", "callback_data": f"subs:{page+1}"})
    if nav:
        rows.append(nav)
    rows.append([{"text": "➕ ساخت گروه جدید", "callback_data": "newsub"}])
    rows.append([{"text": "⬅ منوی اصلی", "callback_data": "menu"}])
    return {"inline_keyboard": rows}

def _format_sub_detail(sid: str, s: dict) -> str:
    cnt = len(s.get("link_ids", []))
    pw = "🔒 دارد" if s.get("password_hash") else "بدون رمز"
    desc = _h(s.get("desc")) or "—"
    return (
        f"🗂 <b>{_h(s.get('name','?'))}</b>\n"
        f"توضیحات: {desc}\n"
        f"تعداد کانفیگ‌های داخل گروه: {cnt}\n"
        f"رمز عبور: {pw}\n\n"
        f"🔗 لینک ساب حرفه‌ای این گروه:\n<code>{_group_public_url(s)}</code>"
    )

def _sub_detail_kb(sid: str):
    return {"inline_keyboard": [
        [{"text": "➕ افزودن کانفیگ به این گروه", "callback_data": f"subaddlink:{sid}:0"}],
        [{"text": "🗑 حذف گروه", "callback_data": f"subdel:{sid}"}],
        [{"text": "⬅ بازگشت به لیست گروه‌ها", "callback_data": "subs:0"}],
    ]}

def _confirm_subdel_kb(sid: str):
    return {"inline_keyboard": [
        [{"text": "✅ بله، حذف کن", "callback_data": f"subdelok:{sid}"},
         {"text": "❌ انصراف", "callback_data": f"subview:{sid}"}],
    ]}

def _pick_link_for_group_kb(sid: str, page: int):
    """لیست همه‌ی کانفیگ‌ها برای انتخاب و افزودن به یک گروه ساب مشخص."""
    items = sorted(LINKS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)
    total = len(items)
    start = page * PAGE_SIZE
    chunk = items[start:start + PAGE_SIZE]
    rows = []
    for uid, l in chunk:
        in_this = "✅ " if l.get("sub_id") == sid else ""
        rows.append([{"text": f"{in_this}{l.get('label','?')[:28]}", "callback_data": f"subaddlinkdo:{uid}"}])
    nav = []
    if start > 0:
        nav.append({"text": "◀ قبلی", "callback_data": f"subaddlink:{sid}:{page-1}"})
    if start + PAGE_SIZE < total:
        nav.append({"text": "بعدی ▶", "callback_data": f"subaddlink:{sid}:{page+1}"})
    if nav:
        rows.append(nav)
    rows.append([{"text": "⬅ بازگشت به گروه", "callback_data": f"subview:{sid}"}])
    return {"inline_keyboard": rows}

# ── Per-config "group" (ساب لینک حرفه‌ای) view builders ───────────────────────
def _cfg_group_kb(uid: str):
    link = LINKS.get(uid, {})
    sid = link.get("sub_id")
    if sid and sid in SUBS:
        return {"inline_keyboard": [
            [{"text": "➖ خارج کردن از گروه", "callback_data": f"cfgungroup:{uid}"}],
            [{"text": "⬅ بازگشت", "callback_data": f"view:{uid}"}],
        ]}
    rows = []
    for sid2, s in sorted(SUBS.items(), key=lambda kv: kv[1].get("created_at", ""), reverse=True)[:8]:
        rows.append([{"text": f"➕ افزودن به «{s.get('name','?')[:24]}»", "callback_data": f"cfgaddgroup:{sid2}"}])
    rows.append([{"text": "🆕 ساخت گروه جدید و افزودن", "callback_data": f"cfgnewgroup:{uid}"}])
    rows.append([{"text": "⬅ بازگشت", "callback_data": f"view:{uid}"}])
    return {"inline_keyboard": rows}

def _format_cfg_group(uid: str) -> str:
    link = LINKS.get(uid, {})
    sid = link.get("sub_id")
    if sid and sid in SUBS:
        s = SUBS[sid]
        return (
            f"🗂 کانفیگ «{_h(link.get('label','?'))}» توی گروه «{_h(s.get('name','?'))}» هست.\n\n"
            f"🔗 لینک ساب حرفه‌ای این گروه:\n<code>{_group_public_url(s)}</code>"
        )
    return (
        f"کانفیگ «{_h(link.get('label','?'))}» توی هیچ گروهی نیست، یعنی فقط لینک ساب ساده داره.\n\n"
        "برای گرفتن لینک ساب حرفه‌ای (صفحه‌ی زیبا)، این کانفیگ رو به یک گروه اضافه کن یا یه گروه جدید بساز:"
    )

# ── Update handling ──────────────────────────────────────────────────────────

def _progress_bar(pct: float, width: int = 10) -> str:
    pct = max(0, min(100, pct))
    filled = round((pct / 100) * width)
    return "█" * filled + "░" * (width - filled)

def _admin_welcome_text(base: str) -> str:
    total = len(LINKS)
    active = sum(1 for l in LINKS.values() if is_link_allowed(l))
    return f"{base}\n\n🌐 {total} کانفیگ ({active} فعال) · 🗂 {len(SUBS)} گروه ساب"

# ═════════════════════════════════════════════════════════════════════════════
#  قابلیت‌های حرفه‌ای: آدرس واقعی، کارت لینک + QR، ساخت سریع، ویرایش، هشدار، بکاپ
# ═════════════════════════════════════════════════════════════════════════════
import json as _json
import time as _time
from urllib.parse import quote as _urlquote

try:
    import psutil as _psutil
except Exception:
    _psutil = None

NO_HOST_MSG = (
    "⚠️ <b>آدرس واقعی پنل هنوز مشخص نیست.</b>\n"
    "برای اینکه لینک‌ها آدرس فیک (localhost) نداشته باشن، یکی از این دو کار رو بکن:\n\n"
    "۱) یک‌بار وارد پنل (داشبورد) بشو؛ آدرس خودکار ذخیره می‌شه.\n"
    "۲) همین‌جا بفرست:\n<code>/seturl https://panel.example.com</code>"
)

_alerts_enabled = True
_alert_keys: set = set()
_alert_task: asyncio.Task | None = None
_reach_cache: dict = {"t": 0.0, "host": "", "ok": None}

QUICK_PRESETS = [
    (10, 30), (30, 30), (50, 30), (100, 30), (200, 60), (0, 30), (0, 0),
]


def _real_host():
    return get_public_host_strict()


def _base_url():
    return get_public_base()


def _live_proto(proto: str) -> bool:
    return proto in LIVE_PROTOCOLS


def _real_link(uid: str, l: dict):
    # لینک واقعی با آدرس واقعی پنل؛ اگر آدرس معتبر نباشه هیچ لینک فیکی ساخته نمی‌شه.
    host = _real_host()
    if not host:
        return None, NO_HOST_MSG
    proto = l.get("protocol", DEFAULT_PROTOCOL)
    if proto == "vless-tcp" and not str(CONFIG.get("tcp_public_host") or "").strip():
        return None, ("⚠️ این کانفیگ «VLESS TCP خام» است و به آدرس TCP عمومی نیاز دارد؛ "
                      "در تنظیمات پنل «TCP Public Host/Port» رو وارد کن تا لینک واقعی ساخته بشه.")
    return vless_link_for_link(l, uid, host), None


def _qr_url(data: str) -> str:
    return "https://api.qrserver.com/v1/create-qr-code/?size=512x512&margin=12&data=" + _urlquote(data, safe="")


async def _send_photo(chat_id: int, url: str, caption: str = "", kb: dict | None = None):
    payload = {"chat_id": chat_id, "photo": url, "caption": caption[:1000], "parse_mode": "HTML"}
    if kb:
        payload["reply_markup"] = kb
    return await _call("sendPhoto", **payload)


async def _upload_document(chat_id: int, filename: str, content: bytes, caption: str = ""):
    if _client is None:
        return None
    try:
        r = await _client.post(
            f"{API_BASE}/sendDocument",
            data={"chat_id": str(chat_id), "caption": caption[:900], "parse_mode": "HTML"},
            files={"document": (filename, content, "application/octet-stream")},
            timeout=60,
        )
        return r.json()
    except Exception as e:
        logger.warning(f"Telegram sendDocument error: {e}")
        return None


async def _panel_reachable(base: str):
    # تست واقعی: آیا همین آدرس از بیرون (با HTTPS) جواب می‌ده؟ نتیجه ۶۰ ثانیه کش می‌شه.
    if _client is None or not base:
        return None
    now = _time.time()
    if _reach_cache["host"] == base and now - _reach_cache["t"] < 60:
        return _reach_cache["ok"]
    ok = None
    try:
        r = await _client.get(base + "/assets/ui.css", timeout=8, follow_redirects=True)
        ok = r.status_code == 200
    except Exception:
        ok = False
    _reach_cache.update({"t": now, "host": base, "ok": ok})
    return ok


def _online_count(uid: str) -> int:
    try:
        return len(unique_ips_for_uuid(uid))
    except Exception:
        return 0


def _days_left(l: dict):
    exp = l.get("expires_at")
    if not exp:
        return None
    try:
        return (datetime.fromisoformat(str(exp)) - datetime.now()).total_seconds() / 86400
    except Exception:
        return None


def _usage_pct(l: dict):
    limit = int(l.get("limit_bytes") or 0)
    if limit <= 0:
        return None
    return min(100.0, round(int(l.get("used_bytes") or 0) / limit * 100, 1))


def _live_badge(l: dict) -> str:
    return "✅ واقعی و فعال روی سرور" if _live_proto(l.get("protocol", DEFAULT_PROTOCOL)) else "🔗 فقط لینک (نیاز به هسته‌ی جدا)"


def _new_label(base: str | None = None) -> str:
    if base:
        return decorate_label(str(base).strip()[:40]) if CONFIG.get("name_style_enabled", True) else str(base).strip()[:60]
    return auto_display_name()


def _preferred_protocol() -> str:
    return "vless-ws" if "vless-ws" in LIVE_PROTOCOLS else DEFAULT_PROTOCOL


async def _create_real_config(label: str, gb: float, days: int, protocol: str | None = None, **extra):
    expires_at = (datetime.now() + timedelta(days=days)).isoformat() if days and days > 0 else None
    limit_bytes = int(parse_size_to_bytes(gb, "GB")) if gb and gb > 0 else 0
    return await make_link(
        label=label, limit_bytes=limit_bytes, expires_at=expires_at,
        protocol=protocol or _preferred_protocol(), **extra,
    )


def _link_card_text(uid: str, l: dict, base: str | None, link: str | None, warn: str | None, reach) -> str:
    host = _real_host() or "—"
    lines = [f"🔗 <b>{_h(l.get('label', '?'))}</b>", _live_badge(l),
             f"🌐 سرور: <code>{_h(host)}</code> · پورت {l.get('port', DEFAULT_PORT)}"]
    if reach is True:
        lines.append("🟢 آدرس پنل از بیرون در دسترسه")
    elif reach is False:
        lines.append("🟡 تست دسترسی آدرس انجام نشد؛ دامنه/Proxy رو بررسی کن")
    if warn:
        lines.append("\n" + warn)
    if link:
        lines.append(f"\n<b>لینک اتصال (بزن تا کپی بشه):</b>\n<code>{_h(link)}</code>")
    if base:
        lines.append(f"\n📄 صفحه‌ی اشتراک:\n<code>{base}/subscription/{uid}</code>")
        lines.append(f"📥 لینک ساب برای اپ:\n<code>{base}/sub/{uid}</code>")
    sid = l.get("sub_id")
    if sid and sid in SUBS:
        lines.append(f"\n✨ ساب حرفه‌ای گروه «{_h(SUBS[sid].get('name', '?'))}»:\n<code>{_group_public_url(SUBS[sid])}</code>")
    sup = get_support_username()
    lines.append(f"\n💬 پشتیبانی: {sup}")
    return "\n".join(lines)


async def _send_link_card(chat_id: int, uid: str, l: dict, with_qr: bool = True, prefix: str = ""):
    link, warn = _real_link(uid, l)
    base = _base_url()
    reach = await _panel_reachable(base) if base else None
    text = (prefix + "\n\n" if prefix else "") + _link_card_text(uid, l, base, link, warn, reach)
    kb = {"inline_keyboard": [
        [{"text": "✏️ ویرایش", "callback_data": f"edit:{uid}"}, {"text": "📋 جزئیات", "callback_data": f"view:{uid}"}],
        *([[{"text": "🌐 باز کردن صفحه‌ی اشتراک", "url": f"{base}/subscription/{uid}"}]] if base else []),
        [{"text": "⬅ منوی اصلی", "callback_data": "menu"}],
    ]}
    await _send(chat_id, text, kb)
    if with_qr and link:
        await _send_photo(chat_id, _qr_url(link), "📷 QR کانفیگ — با اپ اسکن کن")


def _quick_menu_kb():
    rows, row = [], []
    for gb, days in QUICK_PRESETS:
        vol = f"{gb}GB" if gb else "♾"
        dur = f"{days} روز" if days else "بدون انقضا"
        row.append({"text": f"{vol} · {dur}", "callback_data": f"qc:{gb}:{days}"})
        if len(row) == 2:
            rows.append(row); row = []
    if row:
        rows.append(row)
    rows.append([{"text": "🧩 ساخت پیشرفته (مرحله‌ای)", "callback_data": "newcfg"}])
    rows.append([{"text": "⬅ منوی اصلی", "callback_data": "menu"}])
    return {"inline_keyboard": rows}


def _edit_kb(uid: str):
    return {"inline_keyboard": [
        [{"text": "➕ 5GB", "callback_data": f"ed:gb:{uid}:5"}, {"text": "➕ 10GB", "callback_data": f"ed:gb:{uid}:10"},
         {"text": "➕ 50GB", "callback_data": f"ed:gb:{uid}:50"}],
        [{"text": "📅 +7 روز", "callback_data": f"ed:d:{uid}:7"}, {"text": "📅 +30 روز", "callback_data": f"ed:d:{uid}:30"},
         {"text": "📅 +90 روز", "callback_data": f"ed:d:{uid}:90"}],
        [{"text": "🔄 ریست مصرف", "callback_data": f"ed:reset:{uid}"}, {"text": "♾ حجم نامحدود", "callback_data": f"ed:unl:{uid}"}],
        [{"text": "🎲 اسم خفن جدید", "callback_data": f"ed:rname:{uid}"}, {"text": "✏️ تغییر نام", "callback_data": f"ed:name:{uid}"}],
        [{"text": "⬅ بازگشت", "callback_data": f"view:{uid}"}],
    ]}


def _alerts_label() -> str:
    return "🔔 هشدارها: روشن" if _alerts_enabled else "🔕 هشدارها: خاموش"


def _list_kb(items, back="menu", title_prefix=""):
    rows = []
    for uid, l in items[:12]:
        dot = "🟢" if is_link_allowed(l) else "🔴"
        rows.append([{"text": f"{dot} {str(l.get('label', '?'))[:30]}", "callback_data": f"view:{uid}"}])
    rows.append([{"text": "⬅ منوی اصلی", "callback_data": back}])
    return {"inline_keyboard": rows}


def _top_items(n=10):
    return sorted(LINKS.items(), key=lambda kv: int(kv[1].get("used_bytes") or 0), reverse=True)[:n]


def _expiring_items():
    out = []
    for uid, l in LINKS.items():
        if not l.get("active", True):
            continue
        d = _days_left(l)
        p = _usage_pct(l)
        if (d is not None and d <= 3) or (p is not None and p >= 85):
            out.append((uid, l))
    out.sort(key=lambda kv: (_days_left(kv[1]) if _days_left(kv[1]) is not None else 9999))
    return out


def _server_text() -> str:
    lines = ["🖥 <b>وضعیت سرور</b>\n"]
    if _psutil:
        try:
            vm = _psutil.virtual_memory()
            du = _psutil.disk_usage("/")
            lines.append(f"⚙️ CPU: <b>{_psutil.cpu_percent(interval=0.3)}%</b>")
            lines.append(f"🧠 RAM: <b>{vm.percent}%</b> ({fmt_bytes(vm.used)} / {fmt_bytes(vm.total)})")
            lines.append(f"💽 دیسک: <b>{du.percent}%</b> ({fmt_bytes(du.used)} / {fmt_bytes(du.total)})")
            net = _psutil.net_io_counters()
            lines.append(f"🌐 شبکه: ⬆ {fmt_bytes(net.bytes_sent)} · ⬇ {fmt_bytes(net.bytes_recv)}")
        except Exception:
            lines.append("اطلاعات سخت‌افزاری در دسترس نیست.")
    else:
        lines.append("ماژول psutil نصب نیست.")
    host = _real_host()
    lines.append(f"\n🌐 آدرس پنل: <code>{_h(host) if host else 'نامشخص'}</code>")
    return "\n".join(lines)


def _stats_text() -> str:
    total = len(LINKS)
    active = sum(1 for l in LINKS.values() if is_link_allowed(l))
    used = sum(int(l.get("used_bytes", 0) or 0) for l in LINKS.values())
    online = sum(_online_count(uid) for uid in LINKS)
    near = len(_expiring_items())
    top = _top_items(1)
    top_line = f"\n🔥 پرمصرف‌ترین: {_h(top[0][1].get('label', '?'))} ({fmt_bytes(int(top[0][1].get('used_bytes') or 0))})" if top and int(top[0][1].get("used_bytes") or 0) else ""
    return (
        "📊 <b>آمار کلی VodiWalker</b>\n\n"
        f"🌐 کل کانفیگ‌ها: <b>{total}</b>\n"
        f"🟢 فعال: <b>{active}</b> · 🔴 غیرفعال/منقضی: <b>{total - active}</b>\n"
        f"🟣 آنلاین همین الان: <b>{online}</b> اتصال\n"
        f"📦 مجموع کل ترافیک: <b>{fmt_bytes(used)}</b>\n"
        f"⏳ نزدیک انقضا/اتمام حجم: <b>{near}</b>\n"
        f"🗂 گروه‌های ساب: <b>{len(SUBS)}</b>"
        f"{top_line}"
    )


async def _do_backup(chat_id: int):
    try:
        if DATA_FILE.exists():
            content = DATA_FILE.read_bytes()
        else:
            content = _json.dumps({"links": dict(LINKS), "subs": dict(SUBS)}, ensure_ascii=False, indent=1).encode()
    except Exception as e:
        await _send(chat_id, f"❌ خواندن بکاپ ناموفق بود: {_h(e)}")
        return
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    res = await _upload_document(chat_id, f"vodiwalker-backup-{stamp}.json", content,
                                 f"💾 <b>بکاپ VodiWalker</b>\n{len(LINKS)} کانفیگ · {len(SUBS)} گروه\n⚠️ این فایل حاوی UUID همه‌ی کانفیگ‌هاست؛ جای امن نگهش دار.")
    if not res or not res.get("ok"):
        await _send(chat_id, "❌ ارسال فایل بکاپ ناموفق بود.")


async def _set_public_url(chat_id: int, raw: str):
    raw = (raw or "").strip()
    scheme, host = _split_base_url(raw)
    if not host or not _is_real_public_host(host):
        await _send(chat_id, "❌ آدرس معتبر نیست. نمونه:\n<code>/seturl https://panel.example.com</code>\n(localhost و آی‌پی داخلی قبول نمی‌شه)")
        return
    CONFIG["public_base_url"] = f"{scheme}://{host}"
    await save_state()
    _reach_cache["t"] = 0
    await _set_menu_button()
    await _send(chat_id, f"✅ آدرس پنل ذخیره شد:\n<code>{scheme}://{host}</code>\nاز این به بعد همه‌ی لینک‌ها با همین آدرس واقعی ساخته می‌شن.", _main_menu_kb())


async def _bulk_create(chat_id: int, args: list):
    # /bulk 10 30GB 30 [نام]
    try:
        n = int(args[0]); vol = args[1] if len(args) > 1 else "0"; days = int(args[2]) if len(args) > 2 else 30
    except Exception:
        await _send(chat_id, "فرمت: <code>/bulk تعداد حجم روز [نام]</code>\nمثال: <code>/bulk 10 30GB 30 Vodiwalker</code>\n(حجم 0 = نامحدود)")
        return
    if not (1 <= n <= 50):
        await _send(chat_id, "تعداد باید بین 1 تا 50 باشه.")
        return
    vb = _parse_volume_text(vol)
    if vb is None:
        await _send(chat_id, "❗️ فرمت حجم درسته نیست (مثلاً 30GB).")
        return
    if not _real_host():
        await _send(chat_id, NO_HOST_MSG)
        return
    base_name = " ".join(args[3:]).strip()[:30] or "VodiWalker"
    await _send(chat_id, f"⏳ در حال ساخت {n} کانفیگ واقعی…")
    sid, sub = await create_sub_group(name=f"{base_name} · {datetime.now().strftime('%m/%d %H:%M')}")
    lines, made = [], 0
    for i in range(n):
        label = style_config_name(base_name, index=i) if CONFIG.get("name_style_enabled", True) else f"{base_name} {i + 1}"
        expires_at = (datetime.now() + timedelta(days=days)).isoformat() if days > 0 else None
        uid, link = await make_link(label=label, limit_bytes=vb or 0, expires_at=expires_at, protocol=_preferred_protocol())
        await set_link_sub(uid, sid)
        real, _w = _real_link(uid, link)
        if real:
            lines.append(real)
            made += 1
    txt = "\n".join(lines).encode()
    await _upload_document(chat_id, f"configs-{made}.txt", txt, f"✅ <b>{made} کانفیگ واقعی</b> ساخته شد.")
    await _send(chat_id, f"✅ {made} کانفیگ ساخته و داخل یک گروه ساب گذاشته شد.\n\n✨ لینک ساب حرفه‌ای گروه (برای مشتری):\n<code>{_group_public_url(SUBS[sid])}</code>", _main_menu_kb())


def _alert_conditions():
    # شرایط هشدار فعلی → {key: text}
    out = {}
    for uid, l in LINKS.items():
        if not l.get("active", True):
            continue
        name = _h(l.get("label", "?"))
        d = _days_left(l)
        p = _usage_pct(l)
        if d is not None and d <= 0:
            out[f"{uid}:expired"] = f"⛔ «{name}» منقضی شد"
        elif d is not None and d <= 2:
            out[f"{uid}:exp2"] = f"⏳ «{name}» {max(0, int(d * 24))} ساعت دیگه منقضی می‌شه"
        if p is not None and p >= 100:
            out[f"{uid}:full"] = f"📦 «{name}» حجمش تموم شد"
        elif p is not None and p >= 90:
            out[f"{uid}:vol90"] = f"📉 «{name}» {p}% حجمش مصرف شده"
    return out


async def _alert_loop():
    global _alert_keys
    first = True
    while _running:
        try:
            cond = _alert_conditions()
            if first:
                _alert_keys = set(cond)          # بعد از ری‌استارت، هشدارهای قدیمی دوباره اسپم نشن
                first = False
            else:
                new = [t for k, t in cond.items() if k not in _alert_keys]
                _alert_keys = set(cond)
                if new and _alerts_enabled and ADMIN_IDS:
                    text = "🔔 <b>هشدار خودکار VodiWalker</b>\n\n" + "\n".join(new[:15])
                    kb = {"inline_keyboard": [[{"text": "⏳ نمایش لیست", "callback_data": "expiring"}]]}
                    for aid in ADMIN_IDS:
                        await _send(aid, text, kb)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.warning(f"Telegram alert loop error: {e}")
        try:
            await asyncio.sleep(600)
        except asyncio.CancelledError:
            break


BOT_COMMANDS = [
    ("start", "منوی اصلی"), ("new", "ساخت سریع کانفیگ"), ("find", "جستجوی کانفیگ"),
    ("online", "کاربران آنلاین"), ("top", "پرمصرف‌ترین‌ها"), ("expiring", "نزدیک انقضا"),
    ("server", "وضعیت سرور"), ("bulk", "ساخت دسته‌ای"), ("backup", "بکاپ"),
    ("seturl", "ثبت آدرس پنل"), ("id", "شناسه‌ی عددی من"), ("help", "راهنما"),
]

HELP_TEXT = (
    "📖 <b>راهنمای ربات VodiWalker</b>\n\n"
    "⚡ /new — ساخت سریع کانفیگ واقعی (یک‌کلیکی، با اسم خفن)\n"
    "🔎 /find نام — جستجو بین کانفیگ‌ها (یا مستقیم اسم رو بفرست)\n"
    "🟢 /online — کاربران آنلاین همین الان\n"
    "🔥 /top — پرمصرف‌ترین کانفیگ‌ها\n"
    "⏳ /expiring — نزدیک انقضا یا اتمام حجم\n"
    "🖥 /server — وضعیت CPU/RAM/دیسک\n"
    "📦 /bulk 10 30GB 30 نام — ساخت دسته‌ای + گروه ساب\n"
    "💾 /backup — دریافت فایل بکاپ\n"
    "🌐 /seturl https://دامنه — ثبت آدرس واقعی پنل\n"
    "🔔 /alerts on|off — هشدار خودکار انقضا و حجم\n"
    "🆔 /id — شناسه‌ی عددی تلگرام شما"
)


async def _handle_message(msg: dict):
    chat_id = msg.get("chat", {}).get("id")
    text = (msg.get("text") or "").strip()
    if chat_id is None:
        return

    cmd = text.split()[0].split("@")[0].lower() if text.startswith("/") else ""
    args = text.split()[1:] if cmd else []

    if cmd == "/start" and _is_admin(chat_id):
        await _set_menu_button()
    if cmd == "/id":
        await _send(chat_id, f"🆔 شناسه‌ی عددی شما: <code>{chat_id}</code>\nاین عدد رو توی تنظیمات پنل (آیدی ادمین‌ها) بذار.")
        return

    # این ربات فقط برای مدیریت پنل است؛ فقط ادمین‌های مجاز (TELEGRAM_ADMIN_IDS)
    # اجازه‌ی استفاده دارند.
    if not _is_admin(chat_id):
        return

    if cmd in ("/new", "/quick"):
        _pending.pop(chat_id, None)
        await _send(chat_id, "⚡ <b>ساخت سریع کانفیگ واقعی</b>\nحجم و مدت رو انتخاب کن؛ اسم خفن و لینک واقعی خودکار ساخته می‌شه:", _quick_menu_kb())
        return
    if cmd == "/help":
        await _send(chat_id, HELP_TEXT, _main_menu_kb())
        return
    if cmd == "/server":
        await _send(chat_id, _server_text(), _main_menu_kb())
        return
    if cmd == "/backup":
        await _do_backup(chat_id)
        return
    if cmd == "/online":
        items = [(u, l) for u, l in LINKS.items() if _online_count(u) > 0]
        await _send(chat_id, f"🟢 <b>آنلاین‌ها</b> ({len(items)} کانفیگ)" if items else "الان هیچ کاربری آنلاین نیست.", _list_kb(items))
        return
    if cmd == "/top":
        await _send(chat_id, "🔥 <b>پرمصرف‌ترین کانفیگ‌ها</b>", _list_kb(_top_items()))
        return
    if cmd == "/expiring":
        items = _expiring_items()
        await _send(chat_id, f"⏳ <b>نزدیک انقضا / اتمام حجم</b> ({len(items)})" if items else "✅ هیچ کانفیگی نزدیک انقضا یا اتمام حجم نیست.", _list_kb(items))
        return
    if cmd == "/seturl":
        await _set_public_url(chat_id, args[0] if args else "")
        return
    if cmd == "/bulk":
        await _bulk_create(chat_id, args)
        return
    if cmd == "/alerts":
        global _alerts_enabled
        if args and args[0].lower() in ("on", "off"):
            _alerts_enabled = args[0].lower() == "on"
        await _send(chat_id, f"{_alerts_label()}\nبرای تغییر: <code>/alerts on</code> یا <code>/alerts off</code>", _main_menu_kb())
        return
    if cmd == "/find":
        _pending.pop(chat_id, None)
        text = " ".join(args)
        if not text:
            await _send(chat_id, "اسم کانفیگ رو بعد از /find بنویس. مثال: <code>/find Tofan</code>")
            return
        cmd = ""

    if text.startswith("/start") or text == "/admin":
        _pending.pop(chat_id, None)
        await _send(chat_id, _admin_welcome_text(get_bot_text("welcome", "👋 <b>VodiWalker Control Center</b>\nمدیریت کامل سرویس:")), _main_menu_kb())
        return

    if text == "/menu":
        _pending.pop(chat_id, None)
        await _send(chat_id, _admin_welcome_text(get_bot_text("welcome", "🛠 <b>VodiWalker Control Center</b>")), _main_menu_kb())
        return

    if text == "/cancel":
        _pending.pop(chat_id, None)
        await _send(chat_id, "لغو شد.", _main_menu_kb())
        return

    pending = _pending.get(chat_id)

    if pending and pending.get("action") == "newsub" and pending.get("step") == "name" and text:
        name = text[:60]
        sid, s = await create_sub_group(name=name)
        link_uid = pending.get("link_uid")
        _pending.pop(chat_id, None)
        if link_uid and link_uid in LINKS:
            await set_link_sub(link_uid, sid)
            await _send(chat_id, f"✅ گروه ساخته شد و کانفیگ به اون اضافه شد.\n\n{_format_cfg_group(link_uid)}", _cfg_group_kb(link_uid))
        else:
            await _send(chat_id, f"✅ گروه ساخته شد.\n\n{_format_sub_detail(sid, s)}", _sub_detail_kb(sid))
        return

    if pending and pending.get("action") == "newclient" and text:
        step = pending["step"]
        data = pending["data"]

        if step == "label":
            data["label"] = text[:60] or "کاربر جدید"
            pending["step"] = "volume"
            await _send(chat_id, _wizard_client_prompt("volume", data), _wizard_client_skip_kb("volume", "♾ ارث‌بری از اینباند"))
            return

        if step == "volume":
            parsed = _parse_volume_text(text)
            if parsed is None:
                await _send(chat_id, "❗️ فرمت درست نیست. مثلاً بفرست: <code>10GB</code> یا <code>500MB</code>", _wizard_client_skip_kb("volume", "♾ ارث‌بری از اینباند"))
                return
            data["limit_bytes"] = parsed
            pending["step"] = "days"
            await _send(chat_id, _wizard_client_prompt("days", data), _wizard_client_skip_kb("days", "♾ ارث‌بری از اینباند"))
            return

        if step == "days":
            try:
                d = int(text.strip())
                if d < 0:
                    raise ValueError
            except ValueError:
                await _send(chat_id, "❗️ یه عدد صحیح (روز) بفرست:", _wizard_client_skip_kb("days", "♾ ارث‌بری از اینباند"))
                return
            data["expires_days"] = d
            pending["step"] = "confirm"
            await _send(chat_id, _wizard_client_prompt("confirm", data), _wizard_client_confirm_kb())
            return

    if pending and pending.get("action") == "wizard" and text:
        step = pending["step"]
        data = pending["data"]

        if step == "label":
            data["label"] = _new_label(text[:40]) if text else auto_display_name()
            pending["step"] = "protocol"
            await _send(chat_id, _wizard_prompt("protocol", data), _wizard_protocol_kb())
            return

        if step in ("protocol", "fingerprint"):
            # این دو مرحله فقط با دکمه انتخاب می‌شن
            kb = _wizard_protocol_kb() if step == "protocol" else _wizard_fp_kb()
            await _send(chat_id, "لطفاً از دکمه‌های بالا یکی رو انتخاب کن 👆", kb)
            return

        if step == "alpn":
            data["alpn"] = text.strip()[:100]
            pending["step"] = "port"
            await _send(chat_id, _wizard_prompt("port", data), _wizard_skip_kb("port", f"⏭ پیش‌فرض ({DEFAULT_PORT})"))
            return

        if step == "port":
            try:
                p = int(text.strip())
            except ValueError:
                p = None
            if p is None or not (MIN_PORT <= p <= MAX_PORT):
                await _send(chat_id, f"❗️ عدد پورت نامعتبره. یه عدد بین {MIN_PORT} تا {MAX_PORT} بفرست:", _wizard_skip_kb("port", f"⏭ پیش‌فرض ({DEFAULT_PORT})"))
                return
            data["port"] = p
            pending["step"] = "volume"
            await _send(chat_id, _wizard_prompt("volume", data), _wizard_unlimited_kb("volume"))
            return

        if step == "volume":
            parsed = _parse_volume_text(text)
            if parsed is None:
                await _send(chat_id, "❗️ فرمت درست نیست. مثلاً بفرست: <code>10GB</code> یا <code>500MB</code>", _wizard_unlimited_kb("volume"))
                return
            data["limit_bytes"] = parsed
            pending["step"] = "speed"
            await _send(chat_id, _wizard_prompt("speed", data), _wizard_unlimited_kb("speed"))
            return

        if step == "speed":
            parsed = _parse_speed_text(text)
            if parsed is None:
                await _send(chat_id, "❗️ فرمت درست نیست. یه عدد بفرست، مثلاً <code>20</code> (Mbps)", _wizard_unlimited_kb("speed"))
                return
            data["speed_limit_bytes"] = parsed
            pending["step"] = "iplimit"
            await _send(chat_id, _wizard_prompt("iplimit", data), _wizard_unlimited_kb("iplimit"))
            return

        if step == "iplimit":
            n = _parse_nonneg_int(text)
            if n is None:
                await _send(chat_id, "❗️ یه عدد صحیح بفرست:", _wizard_unlimited_kb("iplimit"))
                return
            data["ip_limit"] = n
            pending["step"] = "days"
            await _send(chat_id, _wizard_prompt("days", data), _wizard_unlimited_kb("days"))
            return

        if step == "days":
            n = _parse_nonneg_int(text)
            if n is None:
                await _send(chat_id, "❗️ یه عدد صحیح بفرست (تعداد روز):", _wizard_unlimited_kb("days"))
                return
            data["expires_days"] = n
            pending["step"] = "confirm"
            await _send(chat_id, _wizard_summary(data), _wizard_confirm_kb())
            return

    if pending and pending.get("action") == "rename" and text and not text.startswith("/"):
        uid = pending.get("uid")
        _pending.pop(chat_id, None)
        l = await update_link_fields(uid, label=_new_label(text[:40])) if uid in LINKS else None
        if not l:
            await _send(chat_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        await _send(chat_id, f"✅ نام عوض شد.\n\n{_format_detail(uid, l)}", _edit_kb(uid))
        return

    # جستجو: هر متنی که دستور نباشه = جستجو بین اسم کانفیگ‌ها
    if text and not text.startswith("/") and len(text) >= 2:
        q = text.lower()
        items = [(u, l) for u, l in LINKS.items() if q in str(l.get("label", "")).lower() or u.lower().startswith(q)]
        if items:
            await _send(chat_id, f"🔎 <b>{len(items)} نتیجه برای «{_h(text)}»</b>", _list_kb(sorted(items, key=lambda kv: str(kv[1].get('label', '')))))
            return

    # پیام ناشناخته → منو رو نشون بده
    await _send(chat_id, "از دکمه‌های زیر استفاده کن (یا بخشی از اسم کانفیگ رو بفرست تا پیداش کنم 🔎):", _main_menu_kb())

async def _handle_callback(cb: dict):
    chat_id = cb.get("message", {}).get("chat", {}).get("id")
    message_id = cb.get("message", {}).get("message_id")
    data = cb.get("data", "")
    cb_id = cb.get("id")

    if chat_id is None:
        return

    # ربات فقط برای مدیریت پنل است؛ فقط ادمین‌ها دسترسی دارند.
    if not _is_admin(chat_id):
        await _answer_cb(cb_id)
        return
    await _answer_cb(cb_id)

    if data == "quick":
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, "⚡ <b>ساخت سریع کانفیگ واقعی</b>\nحجم و مدت رو انتخاب کن؛ اسم خفن و لینک واقعی خودکار ساخته می‌شه:", _quick_menu_kb())
        return

    if data.startswith("qc:"):
        if not _real_host():
            await _edit(chat_id, message_id, NO_HOST_MSG, _main_menu_kb())
            return
        try:
            _, gb_s, days_s = data.split(":")
            gb, days = float(gb_s), int(days_s)
        except Exception:
            await _answer_cb(cb_id, "دکمه نامعتبر")
            return
        uid, link = await _create_real_config(auto_display_name(), gb, days)
        await _edit(chat_id, message_id, f"✅ کانفیگ واقعی ساخته شد.\n\n{_format_detail(uid, link)}", _link_detail_kb(uid, link["active"]))
        await _send_link_card(chat_id, uid, link)
        return

    if data == "online":
        items = [(u, l) for u, l in LINKS.items() if _online_count(u) > 0]
        await _edit(chat_id, message_id, f"🟢 <b>آنلاین‌ها</b> ({len(items)} کانفیگ)" if items else "الان هیچ کاربری آنلاین نیست.", _list_kb(items))
        return

    if data == "top":
        await _edit(chat_id, message_id, "🔥 <b>پرمصرف‌ترین کانفیگ‌ها</b>", _list_kb(_top_items()))
        return

    if data == "expiring":
        items = _expiring_items()
        await _edit(chat_id, message_id, f"⏳ <b>نزدیک انقضا / اتمام حجم</b> ({len(items)})" if items else "✅ هیچ کانفیگی نزدیک انقضا یا اتمام حجم نیست.", _list_kb(items))
        return

    if data == "server":
        await _edit(chat_id, message_id, _server_text(), _main_menu_kb())
        return

    if data == "backup":
        await _do_backup(chat_id)
        return

    if data == "help":
        await _edit(chat_id, message_id, HELP_TEXT, _main_menu_kb())
        return

    if data == "alerts:toggle":
        global _alerts_enabled
        _alerts_enabled = not _alerts_enabled
        await _edit(chat_id, message_id, _admin_welcome_text("🛠 <b>VodiWalker Control Center</b>"), _main_menu_kb())
        return

    if data.startswith("edit:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"✏️ <b>ویرایش سریع</b>\n\n{_format_detail(uid, l)}", _edit_kb(uid))
        return

    if data.startswith("ed:"):
        parts = data.split(":")
        kind, uid = parts[1], parts[2]
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        if kind == "name":
            _pending[chat_id] = {"action": "rename", "uid": uid}
            await _edit(chat_id, message_id, "✏️ اسم جدید رو بفرست (مثلاً <code>Vodiwalker</code>؛ خودم تبدیلش می‌کنم به <code>Vodiwalker|Tofan🚀</code>):", _wizard_cancel_kb())
            return
        if kind == "gb":
            if not int(l.get("limit_bytes") or 0):
                await _answer_cb(cb_id, "این کانفیگ حجم نامحدود دارد؛ اول یک سقف بگذار.")
                return
            l = await update_link_fields(uid, add_bytes=int(parse_size_to_bytes(float(parts[3]), "GB")))
        elif kind == "d":
            l = await update_link_fields(uid, extend_days=int(parts[3]))
        elif kind == "reset":
            l = await update_link_fields(uid, reset_usage=True)
        elif kind == "unl":
            l = await update_link_fields(uid, set_limit_bytes=0)
        elif kind == "rname":
            l = await update_link_fields(uid, label=auto_display_name())
        await _edit(chat_id, message_id, f"✅ انجام شد.\n\n{_format_detail(uid, l)}", _edit_kb(uid))
        return

    if data == "menu":
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, _admin_welcome_text(get_bot_text("admin_menu", "🛠 <b>VodiWalker Control Center</b>")), _main_menu_kb())
        return

    if data == "stats":
        await _edit(chat_id, message_id, _stats_text(), _main_menu_kb())
        return

    if data.startswith("list:"):
        page = int(data.split(":", 1)[1] or 0)
        if not LINKS:
            await _edit(chat_id, message_id, "هنوز هیچ کانفیگی ساخته نشده.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"📋 لیست کانفیگ‌ها ({len(LINKS)} مورد):", _links_list_kb(page))
        return

    # ── گروه‌های ساب (لینک حرفه‌ای) ────────────────────────────────────────────
    if data.startswith("subs:"):
        page = int(data.split(":", 1)[1] or 0)
        if not SUBS:
            await _edit(chat_id, message_id, "هنوز هیچ گروهی ساخته نشده.\n\nبرای گرفتن لینک ساب حرفه‌ای (صفحه‌ی زیبا)، اول یه گروه بساز و کانفیگ مورد نظرت رو داخلش بذار.", _subs_list_kb(0))
            return
        await _edit(chat_id, message_id, f"🗂 گروه‌های ساب ({len(SUBS)} مورد):", _subs_list_kb(page))
        return

    if data == "newsub":
        _pending[chat_id] = {"action": "newsub", "step": "name", "link_uid": None}
        await _edit(chat_id, message_id, "✏️ اسم گروه رو بفرست (این اسم فقط برای خودت توی مدیریت گروه‌هاست):", _wizard_cancel_kb())
        return

    if data.startswith("subview:"):
        sid = data.split(":", 1)[1]
        s = SUBS.get(sid)
        if not s:
            await _edit(chat_id, message_id, "این گروه دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_sub_detail(sid, s), _sub_detail_kb(sid))
        return

    if data.startswith("subaddlink:"):
        _, sid, page_s = data.split(":", 2)
        if sid not in SUBS:
            await _edit(chat_id, message_id, "این گروه دیگه وجود نداره.", _main_menu_kb())
            return
        if not LINKS:
            await _edit(chat_id, message_id, "هنوز هیچ کانفیگی نداری که به گروه اضافه کنی.", _sub_detail_kb(sid))
            return
        _pending[chat_id] = {"action": "subaddlink_ctx", "sid": sid}
        await _edit(chat_id, message_id, "کدوم کانفیگ رو به این گروه اضافه کنم؟\n(کانفیگ‌هایی که علامت ✅ دارن همین الان توی این گروهن)", _pick_link_for_group_kb(sid, int(page_s or 0)))
        return

    if data.startswith("subaddlinkdo:"):
        uid = data.split(":", 1)[1]
        ctx = _pending.get(chat_id) or {}
        sid = ctx.get("sid") if ctx.get("action") == "subaddlink_ctx" else None
        if not sid or sid not in SUBS:
            await _answer_cb(cb_id, "این عملیات منقضی شده، از منوی گروه‌ها دوباره امتحان کن.")
            return
        ok = await set_link_sub(uid, sid)
        if not ok:
            await _answer_cb(cb_id, "این کانفیگ دیگه وجود نداره")
            return
        _pending.pop(chat_id, None)
        s = SUBS.get(sid)
        await _edit(chat_id, message_id, f"✅ کانفیگ به گروه اضافه شد.\n\n{_format_sub_detail(sid, s)}", _sub_detail_kb(sid))
        return

    if data.startswith("subdel:"):
        sid = data.split(":", 1)[1]
        s = SUBS.get(sid)
        if not s:
            await _edit(chat_id, message_id, "این گروه دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"❗️ از حذف گروه «{_h(s.get('name'))}» مطمئنی؟ لینک ساب حرفه‌ای‌اش دیگه کار نمی‌کنه (کانفیگ‌ها حذف نمی‌شن، فقط از گروه خارج می‌شن).", _confirm_subdel_kb(sid))
        return

    if data.startswith("subdelok:"):
        sid = data.split(":", 1)[1]
        name = await remove_sub_group(sid)
        if name is None:
            await _edit(chat_id, message_id, "این گروه قبلاً حذف شده بود.", _main_menu_kb())
        else:
            await _edit(chat_id, message_id, f"🗑 گروه «{name}» حذف شد.", _main_menu_kb())
        return

    # ── گروه یک کانفیگ خاص (از صفحه‌ی جزئیات کانفیگ) ───────────────────────────
    if data.startswith("cfggroup:"):
        uid = data.split(":", 1)[1]
        if uid not in LINKS:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        _pending[chat_id] = {"action": "cfg_group_ctx", "uid": uid}
        await _edit(chat_id, message_id, _format_cfg_group(uid), _cfg_group_kb(uid))
        return

    if data.startswith("cfgungroup:"):
        uid = data.split(":", 1)[1]
        await set_link_sub(uid, None)
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_detail(uid, l), _link_detail_kb(uid, l["active"]))
        return

    if data.startswith("cfgaddgroup:"):
        sid = data.split(":", 1)[1]
        ctx = _pending.get(chat_id) or {}
        uid = ctx.get("uid") if ctx.get("action") == "cfg_group_ctx" else None
        if not uid or uid not in LINKS:
            await _answer_cb(cb_id, "این عملیات منقضی شده، از روی کانفیگ دوباره وارد این بخش شو.")
            return
        ok = await set_link_sub(uid, sid)
        if not ok:
            await _answer_cb(cb_id, "این گروه دیگه وجود نداره")
            return
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, f"✅ کانفیگ به گروه اضافه شد.\n\n{_format_cfg_group(uid)}", _cfg_group_kb(uid))
        return

    if data.startswith("cfgnewgroup:"):
        uid = data.split(":", 1)[1]
        if uid not in LINKS:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        _pending[chat_id] = {"action": "newsub", "step": "name", "link_uid": uid}
        await _edit(chat_id, message_id, "✏️ اسم گروه جدید رو بفرست؛ بعد از ساخته شدن، همین کانفیگ خودکار داخلش قرار می‌گیره:", _wizard_cancel_kb())
        return

    if data == "newcfg":
        _pending[chat_id] = {"action": "wizard", "step": "label", "data": {}}
        await _edit(chat_id, message_id, _wizard_prompt("label", {}), _wizard_label_kb())
        return

    if data == "w:cancel":
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, "ساخت کانفیگ لغو شد.", _main_menu_kb())
        return

    if data.startswith("w:"):
        pending = _pending.get(chat_id)
        if not pending or pending.get("action") != "wizard":
            await _edit(chat_id, message_id, "این مرحله دیگه معتبر نیست، از منوی زیر دوباره شروع کن.", _main_menu_kb())
            return

        step = pending["step"]
        wdata = pending["data"]

        if data == "w:autolabel" and step == "label":
            wdata["label"] = auto_display_name()
            pending["step"] = "protocol"
            await _edit(chat_id, message_id, f"🎲 اسم: <b>{_h(wdata['label'])}</b>\n\n" + _wizard_prompt("protocol", wdata), _wizard_protocol_kb())
            return

        if data.startswith("w:proto:") and step == "protocol":
            proto = data.split(":", 2)[2]
            wdata["protocol"] = proto if proto in PROTOCOLS else DEFAULT_PROTOCOL
            pending["step"] = "fingerprint"
            await _edit(chat_id, message_id, _wizard_prompt("fingerprint", wdata), _wizard_fp_kb())
            return

        if data.startswith("w:fp:") and step == "fingerprint":
            fp = data.split(":", 2)[2]
            wdata["fingerprint"] = fp if fp in FINGERPRINTS else DEFAULT_FINGERPRINT
            pending["step"] = "alpn"
            await _edit(chat_id, message_id, _wizard_prompt("alpn", wdata), _wizard_alpn_kb())
            return

        if data.startswith("w:alpnpreset:") and step == "alpn":
            code = data.split(":", 2)[2]
            wdata["alpn"] = ALPN_PRESET_MAP.get(code, "")
            pending["step"] = "port"
            await _edit(chat_id, message_id, _wizard_prompt("port", wdata), _wizard_skip_kb("port", f"⏭ پیش‌فرض ({DEFAULT_PORT})"))
            return

        if data == "w:skip:alpn" and step == "alpn":
            wdata["alpn"] = ""
            pending["step"] = "port"
            await _edit(chat_id, message_id, _wizard_prompt("port", wdata), _wizard_skip_kb("port", f"⏭ پیش‌فرض ({DEFAULT_PORT})"))
            return

        if data == "w:skip:port" and step == "port":
            wdata["port"] = DEFAULT_PORT
            pending["step"] = "volume"
            await _edit(chat_id, message_id, _wizard_prompt("volume", wdata), _wizard_unlimited_kb("volume"))
            return

        if data == "w:skip:volume" and step == "volume":
            wdata["limit_bytes"] = 0
            pending["step"] = "speed"
            await _edit(chat_id, message_id, _wizard_prompt("speed", wdata), _wizard_unlimited_kb("speed"))
            return

        if data == "w:skip:speed" and step == "speed":
            wdata["speed_limit_bytes"] = 0
            pending["step"] = "iplimit"
            await _edit(chat_id, message_id, _wizard_prompt("iplimit", wdata), _wizard_unlimited_kb("iplimit"))
            return

        if data == "w:skip:iplimit" and step == "iplimit":
            wdata["ip_limit"] = 0
            pending["step"] = "days"
            await _edit(chat_id, message_id, _wizard_prompt("days", wdata), _wizard_unlimited_kb("days"))
            return

        if data == "w:skip:days" and step == "days":
            wdata["expires_days"] = 0
            pending["step"] = "confirm"
            await _edit(chat_id, message_id, _wizard_summary(wdata), _wizard_confirm_kb())
            return

        if data == "w:confirm" and step == "confirm":
            expires_days = wdata.get("expires_days", 0)
            expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat() if expires_days > 0 else None
            uid, link = await make_link(
                label=wdata.get("label") or "کانفیگ جدید",
                limit_bytes=wdata.get("limit_bytes", 0),
                expires_at=expires_at,
                protocol=wdata.get("protocol", DEFAULT_PROTOCOL),
                fingerprint=wdata.get("fingerprint", DEFAULT_FINGERPRINT),
                alpn=wdata.get("alpn", ""),
                port=wdata.get("port", DEFAULT_PORT),
                ip_limit=wdata.get("ip_limit", 0),
                speed_limit_bytes=wdata.get("speed_limit_bytes", 0),
            )
            _pending.pop(chat_id, None)
            await _edit(chat_id, message_id, f"✅ کانفیگ ساخته شد.\n\n{_format_detail(uid, link)}", _link_detail_kb(uid, link["active"]))
            await _send_link_card(chat_id, uid, link)
            return

        # هیچ‌کدوم از حالت‌های بالا مچ نشد (مثلاً روی دکمه‌ی مرحله‌ی قبلی که دیگه معتبر نیست زده)
        await _answer_cb(cb_id, "این دکمه دیگه معتبر نیست.")
        return

    if data.startswith("view:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_detail(uid, l), _link_detail_kb(uid, l["active"]))
        return

    if data.startswith("toggle:"):
        uid = data.split(":", 1)[1]
        l = await set_link_active(uid, not LINKS.get(uid, {}).get("active", True))
        if not l:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_detail(uid, l), _link_detail_kb(uid, l["active"]))
        return

    if data.startswith("link:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _answer_cb(cb_id, "کانفیگ پیدا نشد")
            return
        await _send_link_card(chat_id, uid, l)
        return

    if data.startswith("del:"):
        uid = data.split(":", 1)[1]
        l = LINKS.get(uid)
        if not l:
            await _edit(chat_id, message_id, "این کانفیگ دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"❗️ از حذف «{_h(l.get('label'))}» مطمئنی؟ این عمل برگشت‌ناپذیره.", _confirm_delete_kb(uid))
        return

    if data.startswith("delok:"):
        uid = data.split(":", 1)[1]
        label = await remove_link(uid)
        if label is None:
            await _edit(chat_id, message_id, "این کانفیگ قبلاً حذف شده بود.", _main_menu_kb())
        else:
            await _edit(chat_id, message_id, f"🗑 کانفیگ «{label}» حذف شد.", _main_menu_kb())
        return

    # ── مدیریت کاربران (کلاینت‌های) یک اینباند ──────────────────────────────────
    if data.startswith("clients:"):
        _, uid, page_s = data.split(":", 2)
        if uid not in LINKS:
            await _edit(chat_id, message_id, "این اینباند دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, _format_clients_list(uid), _clients_list_kb(uid, int(page_s or 0)))
        return

    if data.startswith("addclient:"):
        uid = data.split(":", 1)[1]
        if uid not in LINKS:
            await _edit(chat_id, message_id, "این اینباند دیگه وجود نداره.", _main_menu_kb())
            return
        _pending[chat_id] = {"action": "newclient", "step": "label", "data": {"parent_uid": uid}}
        await _edit(chat_id, message_id, _wizard_client_prompt("label", {}), _wizard_client_cancel_kb())
        return

    if data.startswith("delclient:"):
        cid = data.split(":", 1)[1]
        child = LINKS.get(cid)
        uid = (child or {}).get("parent_inbound_id")
        if not child or not uid:
            await _edit(chat_id, message_id, "این کاربر دیگه وجود نداره.", _main_menu_kb())
            return
        await _edit(chat_id, message_id, f"❗️ از حذف کاربر «{_h(child.get('label'))}» مطمئنی؟", _confirm_delete_client_kb(uid, cid))
        return

    if data.startswith("delclientok:"):
        cid = data.split(":", 1)[1]
        uid = (LINKS.get(cid) or {}).get("parent_inbound_id")
        if not uid:
            await _edit(chat_id, message_id, "این کاربر قبلاً حذف شده بود.", _main_menu_kb())
            return
        try:
            await remove_inbound_client(uid, cid)
            await _edit(chat_id, message_id, "🗑 کاربر حذف شد.", _clients_list_kb(uid, 0))
        except ValueError:
            await _edit(chat_id, message_id, "این کاربر قبلاً حذف شده بود.", _clients_list_kb(uid, 0))
        return

    if data == "wc:cancel":
        _pending.pop(chat_id, None)
        await _edit(chat_id, message_id, "ساخت کاربر لغو شد.", _main_menu_kb())
        return

    if data.startswith("wc:"):
        pending = _pending.get(chat_id)
        if not pending or pending.get("action") != "newclient":
            await _edit(chat_id, message_id, "این مرحله دیگه معتبر نیست، از منوی کاربران دوباره شروع کن.", _main_menu_kb())
            return
        step = pending["step"]
        wdata = pending["data"]

        if data == "wc:skip:volume" and step == "volume":
            wdata["limit_bytes"] = 0
            pending["step"] = "days"
            await _edit(chat_id, message_id, _wizard_client_prompt("days", wdata), _wizard_client_skip_kb("days", "♾ ارث‌بری از اینباند"))
            return

        if data == "wc:skip:days" and step == "days":
            wdata["expires_days"] = 0
            pending["step"] = "confirm"
            await _edit(chat_id, message_id, _wizard_client_prompt("confirm", wdata), _wizard_client_confirm_kb())
            return

        if data == "wc:confirm" and step == "confirm":
            parent_uid = wdata["parent_uid"]
            try:
                cid, child = await add_client_to_inbound(
                    parent_uid,
                    label=wdata.get("label"),
                    limit_bytes=wdata.get("limit_bytes") or None,
                    expires_days=int(wdata.get("expires_days") or 0),
                )
            except ValueError as exc:
                await _edit(chat_id, message_id, f"❌ {exc}", _clients_list_kb(parent_uid, 0))
                _pending.pop(chat_id, None)
                return
            _pending.pop(chat_id, None)
            await _edit(chat_id, message_id, f"✅ کاربر جدید ساخته شد.\n\n{_format_detail(cid, child)}", _link_detail_kb(cid, child["active"]))
            await _send_link_card(chat_id, cid, child)
            return

        await _edit(chat_id, message_id, "این مرحله دیگه معتبر نیست.", _main_menu_kb())
        return

# ── Polling loop ─────────────────────────────────────────────────────────────
async def _poll_loop():
    global _running
    offset = 0
    logger.info(f"🤖 Telegram bot polling started (admins: {len(ADMIN_IDS)})")
    while _running:
        try:
            res = await _call("getUpdates", offset=offset, timeout=30, allowed_updates=["message", "callback_query"])
            if not res or not res.get("ok"):
                # علت شایع‌ترین «ربات جواب نمی‌ده»: یک وبهوک قبلاً روی این توکن ست شده
                # و getUpdates با خطای 409 Conflict رد می‌شه. هر بار یه‌بار دیگه هم
                # deleteWebhook رو امتحان می‌کنیم تا اگه بعداً یکی وبهوک ست کرد، خودش جمع بشه.
                if res and "Conflict" in str(res.get("description", "")):
                    logger.warning("Telegram bot: getUpdates conflict (webhook?) — deleting webhook and retrying")
                    await _call("deleteWebhook", drop_pending_updates=False)
                await asyncio.sleep(3)
                continue
            for upd in res.get("result", []):
                offset = upd["update_id"] + 1
                try:
                    if "message" in upd:
                        await _handle_message(upd["message"])
                    elif "callback_query" in upd:
                        await _handle_callback(upd["callback_query"])
                except Exception as e:
                    logger.warning(f"Telegram update handling error: {e}")
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.warning(f"Telegram poll loop error: {e}")
            await asyncio.sleep(3)

# ── Lifecycle ────────────────────────────────────────────────────────────────
async def start_bot():
    global _client, _poll_task, _running
    if _running:
        # از بالا اومدنِ چند حلقه‌ی polling هم‌زمان جلوگیری می‌کنه (مثلاً اگه از پنل
        # چند بار دکمه‌ی «شروع» زده بشه)
        logger.info("Telegram bot: از قبل در حال اجراست، دوباره استارت نشد.")
        return
    if not BOT_TOKEN:
        logger.info("Telegram bot: توکن تنظیم نشده، ربات غیرفعاله.")
        return
    if not ADMIN_IDS:
        logger.warning("Telegram bot: هیچ آیدی ادمینی تنظیم نشده، هیچ‌کس اجازه‌ی مدیریت نداره (ربات روشنه ولی همه رد می‌شن).")
    _client = httpx.AsyncClient(timeout=httpx.Timeout(40.0, connect=10.0))
    # نکته‌ی مهم: اگه قبلاً (حتی توسط یک دیپلوی قدیمی یا اسکریپت دیگه) روی همین توکن
    # webhook ست شده باشه، getUpdates همیشه با خطای 409 Conflict شکست می‌خوره و ربات
    # به /start هیچ جوابی نمی‌ده — بدون هیچ خطای قابل‌مشاهده‌ای در پنل. برای همین قبل
    # از شروع polling، هر وبهوکی که ست شده باشه رو پاک می‌کنیم.
    await _call("deleteWebhook", drop_pending_updates=False)
    _running = True
    _poll_task = asyncio.create_task(_poll_loop())
    global _alert_task
    _alert_task = asyncio.create_task(_alert_loop())
    await _set_menu_button()
    await _call("setMyCommands", commands=[{"command": c, "description": d} for c, d in BOT_COMMANDS])

async def stop_bot():
    global _running, _client, _poll_task
    _running = False
    global _alert_task
    if _alert_task:
        _alert_task.cancel()
        _alert_task = None
    if _poll_task:
        _poll_task.cancel()
        _poll_task = None
    if _client:
        await _client.aclose()
        _client = None

async def restart_bot():
    """برای اعمال توکن/آیدی جدید: ربات رو متوقف و با تنظیمات فعلی دوباره روشن می‌کنه."""
    await stop_bot()
    await start_bot()
