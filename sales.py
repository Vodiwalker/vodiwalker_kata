# VodiWalker Sales Engine
import json, os, secrets, asyncio
from datetime import datetime, timedelta
from pathlib import Path

from main import DATA_DIR, LINKS, make_link, get_host, get_scheme, get_web_base, vless_link_for_link, fmt_bytes, save_state, bump_daily_stat

SALES_FILE = DATA_DIR / "vodiwalker_sales.json"
SALES_LOCK = asyncio.Lock()

PLANS_FILE = DATA_DIR / "vodiwalker_plans.json"
PLANS_LOCK = asyncio.Lock()

DEFAULT_PLANS = {
    "starter": {"id":"starter","name":"Starter","days":30,"volume_gb":50,"speed_mbps":30,"ip_limit":1,"stars":99,"badge":"شروع حرفه‌ای","featured":False,"order":1},
    "pro":     {"id":"pro","name":"Pro","days":90,"volume_gb":200,"speed_mbps":80,"ip_limit":2,"stars":249,"badge":"پیشنهاد ویژه","featured":True,"order":2},
    "ultra":   {"id":"ultra","name":"Ultra","days":180,"volume_gb":500,"speed_mbps":150,"ip_limit":3,"stars":499,"badge":"بیشترین ارزش","featured":False,"order":3},
}

PLANS = {}

def _load_plans_sync():
    global PLANS
    try:
        if PLANS_FILE.exists():
            data = json.loads(PLANS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data:
                PLANS.clear()
                PLANS.update(data)
                return
    except Exception:
        pass
    PLANS.clear()
    PLANS.update(json.loads(json.dumps(DEFAULT_PLANS)))
    _save_plans_sync()

def _save_plans_sync():
    PLANS_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = PLANS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(PLANS, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(PLANS_FILE)

def load_plans():
    _load_plans_sync()

async def save_plans():
    async with PLANS_LOCK:
        await asyncio.to_thread(_save_plans_sync)

def list_plans():
    return sorted(PLANS.values(), key=lambda p: p.get("order", 0))

async def upsert_plan(plan_id, data):
    data = dict(data)
    data["id"] = plan_id
    PLANS[plan_id] = data
    await save_plans()
    return data

async def delete_plan(plan_id):
    PLANS.pop(plan_id, None)
    await save_plans()

load_plans()

SALES = {"orders": [], "customers": {}}

def _load_sync():
    global SALES
    try:
        if SALES_FILE.exists():
            data=json.loads(SALES_FILE.read_text(encoding="utf-8"))
            if isinstance(data,dict):
                SALES.update(data)
    except Exception:
        pass

def _save_sync():
    SALES_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp=SALES_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(SALES,ensure_ascii=False,indent=2),encoding="utf-8")
    tmp.replace(SALES_FILE)

def load_sales():
    _load_sync()

async def save_sales():
    async with SALES_LOCK:
        await asyncio.to_thread(_save_sync)

def get_plan(plan_id):
    return PLANS.get(plan_id)

def create_payload(plan_id, user_id):
    return f"vw|{plan_id}|{user_id}|{secrets.token_hex(5)}"

async def fulfill_payment(user, plan_id, telegram_charge_id=""):
    plan=get_plan(plan_id)
    if not plan:
        raise ValueError("unknown plan")
    user_id=str(user.get("id"))
    username=user.get("username") or ""
    expires=(datetime.now()+timedelta(days=plan["days"])).isoformat()
    label=f"{plan['name']}-{username or user_id}"[:60]
    uid, link=await make_link(
        label=label,
        limit_bytes=plan["volume_gb"]*1024**3,
        expires_at=expires,
        protocol=os.environ.get("VODIWALKER_SALES_PROTOCOL","vless-ws"),
        fingerprint="chrome",
        alpn="http/1.1",
        port=int(os.environ.get("VODIWALKER_SALES_PORT","443")),
        ip_limit=plan["ip_limit"],
        speed_limit_bytes=int(plan["speed_mbps"]*1024*1024/8),
    )
    order={
        "id":secrets.token_urlsafe(9),
        "user_id":user_id,
        "username":username,
        "plan_id":plan_id,
        "amount_stars":plan["stars"],
        "telegram_charge_id":telegram_charge_id,
        "link_uid":uid,
        "created_at":datetime.now().isoformat(),
        "expires_at":expires,
        "status":"paid",
    }
    SALES["orders"].insert(0,order)
    SALES["orders"]=SALES["orders"][:5000]
    SALES["customers"].setdefault(user_id,{"user_id":user_id,"username":username,"orders":0})
    SALES["customers"][user_id]["username"]=username
    SALES["customers"][user_id]["orders"]+=1
    bump_daily_stat("orders")
    bump_daily_stat("stars", int(plan["stars"]))
    await save_sales()
    host=get_host()
    return order,link,uid,f"{get_web_base(host)}/subscription/{uid}"

def user_orders(user_id, limit=5):
    return [o for o in SALES.get("orders",[]) if str(o.get("user_id"))==str(user_id)][:limit]

def sales_stats():
    orders=[o for o in SALES.get("orders",[]) if o.get("status")=="paid"]
    return {"orders":len(orders),"stars":sum(int(o.get("amount_stars",0)) for o in orders),"customers":len(SALES.get("customers",{}))}
