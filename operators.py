# operators.py — پروفایل اپراتورها برای ساخت کلاینت
# هر اپراتور یک «پریست» دارد: fragment / fingerprint / alpn / clean IP ها.
# مقادیر پیش‌فرض فقط نقطه‌ی شروع‌اند و از داخل پنل (صفحه‌ی «ساخت کلاینت» ← ویرایش پریست)
# قابل تغییرند؛ شرایط فیلترینگ در هر شهر/زمان فرق می‌کند، پس با تست واقعی تنظیمشان کن.

import json
import os
from pathlib import Path

FRAGMENTS = ("off", "safe", "balanced", "aggressive")
FINGERPRINTS = ("chrome", "firefox", "safari", "ios", "android", "edge", "random", "randomized")

DEFAULTS = {
    "mci": {"name": "همراه اول", "name_en": "MCI (Hamrah-e Aval)", "icon": "ti-antenna-bars-5",
            "color": "#38bdf8", "fragment": "balanced", "fingerprint": "chrome", "alpn": "", "clean_ips": [], "enabled": True},
    "irancell": {"name": "ایرانسل", "name_en": "Irancell", "icon": "ti-device-mobile",
                 "color": "#facc15", "fragment": "safe", "fingerprint": "chrome", "alpn": "", "clean_ips": [], "enabled": True},
    "tci": {"name": "مخابرات / ثابت", "name_en": "TCI / Fixed-line", "icon": "ti-router",
            "color": "#a78bfa", "fragment": "safe", "fingerprint": "firefox", "alpn": "", "clean_ips": [], "enabled": True},
    "rightel": {"name": "رایتل", "name_en": "Rightel", "icon": "ti-radio",
                "color": "#fb7185", "fragment": "balanced", "fingerprint": "android", "alpn": "", "clean_ips": [], "enabled": True},
}
ALL_KEY = "all"


class Operators:
    def __init__(self, data_dir: Path):
        self.file = Path(data_dir) / "operators.json"
        self.data = json.loads(json.dumps(DEFAULTS))
        try:
            saved = json.loads(self.file.read_text(encoding="utf-8"))
            for k, v in saved.items():
                if k in self.data and isinstance(v, dict):
                    self.data[k].update({kk: vv for kk, vv in v.items() if kk in self.data[k]})
        except Exception:
            pass

    def save(self):
        try:
            self.file.write_text(json.dumps(self.data, ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception:
            pass

    def keys_for(self, key: str) -> list[str]:
        """all → همه‌ی اپراتورهای فعال؛ وگرنه فقط همان یکی."""
        if key == ALL_KEY:
            return [k for k, v in self.data.items() if v.get("enabled", True)]
        return [key] if key in self.data else []

    def preset(self, key: str) -> dict | None:
        return self.data.get(key)

    def update(self, key: str, body: dict) -> dict:
        p = self.data[key]
        if "fragment" in body and str(body["fragment"]) in FRAGMENTS:
            p["fragment"] = str(body["fragment"])
        if "fingerprint" in body and str(body["fingerprint"]) in FINGERPRINTS:
            p["fingerprint"] = str(body["fingerprint"])
        if "alpn" in body:
            p["alpn"] = str(body["alpn"] or "").strip()[:100]
        if "enabled" in body:
            p["enabled"] = bool(body["enabled"])
        if "clean_ips" in body:
            raw = body["clean_ips"]
            if isinstance(raw, str):
                raw = raw.replace(",", "\n").split()
            p["clean_ips"] = [str(x).strip()[:120] for x in raw if str(x).strip()][:40]
        self.save()
        return p


def register(app, require_auth, data_dir):
    from fastapi import Depends, HTTPException, Request

    ops = Operators(data_dir)
    app.state.operators = ops

    @app.get("/api/operators")
    async def api_operators(_=Depends(require_auth)):
        return {"ok": True, "operators": ops.data, "fragments": FRAGMENTS, "fingerprints": FINGERPRINTS}

    @app.post("/api/operators/{key}")
    async def api_operator_update(key: str, request: Request, _=Depends(require_auth)):
        if key not in ops.data:
            raise HTTPException(404, "اپراتور پیدا نشد")
        return {"ok": True, "preset": ops.update(key, await request.json())}

    return ops
