# app.py — VodiWalker launcher (KataBump / Railway / هر هاست)
# main را به‌عنوان ماژول واقعی «main» لود می‌کند (حلقه‌ی import سالم می‌ماند) و
# MTProto تلگرام را روی همان پورت پنل سوار می‌کند (هاست‌های تک‌پورتی).
import os

from main import app   # ← main اینجا به‌عنوان ماژول لود می‌شود (نه __main__)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT") or os.environ.get("SERVER_PORT") or 8000)
    config = uvicorn.Config(app, host="0.0.0.0", port=port)
    config.load()
    try:
        import tg_proxy
        if tg_proxy.attach_mux(app, config):
            print("tg-proxy: single-port mux enabled")
    except Exception as exc:
        print("tg-proxy mux skipped:", exc)
    print(f"vodiwalker launcher → starting on 0.0.0.0:{port}")
    uvicorn.Server(config).run()
