# ui_portal.py — پورتال اشتراک مشتری (نسخه‌ی v18)
# placeholderها همان قرارداد قبلی main.subscription_portal هستند (__LABEL__, __USED__, ...)
PORTAL_V18 = r'''<!doctype html><html lang="fa" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#060912"><title>__LABEL__ · VodiWalker</title>
<link rel="stylesheet" href="/assets/ui.css"><script src="/assets/qr.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
:root{--bg:#060912;--card:rgba(15,21,44,.74);--card2:rgba(9,13,30,.8);--line:rgba(148,163,255,.14);--line2:rgba(148,163,255,.3);--text:#eef2ff;--muted:#94a3c8;--soft:#66739a;
--a:#7c5cff;--b:#22d3ee;--g:#34d399;--w:#fbbf24;--r:#fb7185;--ease:cubic-bezier(.22,.7,.2,1);--sh:0 24px 60px -30px rgba(0,0,0,.8)}
body[data-theme=light]{--bg:#eef2fb;--card:rgba(255,255,255,.86);--card2:rgba(244,247,255,.9);--line:rgba(30,41,90,.12);--line2:rgba(30,41,90,.25);--text:#0f1530;--muted:#4b5780;--soft:#7280a8;--sh:0 20px 50px -28px rgba(30,41,90,.35)}
html{-webkit-text-size-adjust:100%}
body{min-height:100dvh;background:var(--bg);color:var(--text);font-family:'Vazirmatn','Inter',sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden;transition:background .3s,color .3s}
body:before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;background:radial-gradient(50% 40% at 90% 0%,rgba(124,92,255,.28),transparent 70%),radial-gradient(45% 40% at 0% 100%,rgba(34,211,238,.18),transparent 70%);animation:drift 16s ease-in-out infinite alternate}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes drift{to{transform:translate3d(-22px,16px,0) scale(1.07)}}
button{font-family:inherit;cursor:pointer;border:0;color:inherit}a{color:inherit;text-decoration:none}
.wrap{position:relative;z-index:1;max-width:980px;margin:0 auto;padding:calc(16px + env(safe-area-inset-top,0px)) 16px calc(40px + env(safe-area-inset-bottom,0px))}
.nav{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:18px;direction:ltr}
.brand{display:flex;align-items:center;gap:11px}.brand img{width:40px;height:40px;border-radius:13px;box-shadow:0 0 0 1px var(--line2),0 10px 26px -8px rgba(124,92,255,.7)}
.brand b{font:800 15px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;letter-spacing:.14em}.brand small{display:block;font:500 9px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;letter-spacing:.25em;color:var(--soft)}
.tools{display:flex;gap:8px}.ib{width:42px;height:42px;border-radius:13px;background:var(--card);border:1px solid var(--line);display:grid;place-items:center;font-size:19px;color:var(--muted);backdrop-filter:blur(12px);transition:.2s var(--ease)}
.ib:hover{color:var(--text);border-color:var(--line2);transform:translateY(-2px)}
.hero{position:relative;overflow:hidden;padding:24px;border-radius:30px;border:1px solid var(--line2);background:linear-gradient(135deg,rgba(124,92,255,.22),rgba(15,21,44,.78) 45%,rgba(34,211,238,.12));backdrop-filter:blur(18px);box-shadow:var(--sh);animation:up .7s var(--ease) both}
body[data-theme=light] .hero{background:linear-gradient(135deg,rgba(124,92,255,.14),rgba(255,255,255,.9) 50%,rgba(34,211,238,.12))}
@keyframes up{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
.hero:before{content:"";position:absolute;inset:-1px;border-radius:inherit;padding:1px;background:conic-gradient(from var(--ang,0deg),transparent 0 72%,var(--a),var(--b),transparent);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;animation:ang 7s linear infinite;pointer-events:none}
@property --ang{syntax:'<angle>';initial-value:0deg;inherits:false}@keyframes ang{to{--ang:360deg}}
.hrow{display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.gauge{--pct:0;position:relative;width:148px;height:148px;flex:none;border-radius:50%;display:grid;place-items:center;
 background:conic-gradient(var(--gc,var(--b)) calc(var(--pct)*1%),rgba(148,163,255,.14) 0);transition:--pct .9s var(--ease)}
@property --pct{syntax:'<number>';initial-value:0;inherits:true}
.gauge:before{content:"";position:absolute;inset:11px;border-radius:50%;background:var(--bgc,#0a0f25)}
body[data-theme=light] .gauge:before{background:#fff}
.gauge>div{position:relative;text-align:center}.gauge b{display:block;font:900 30px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif}.gauge small{font-size:10.5px;color:var(--muted)}
.gauge:after{content:"";position:absolute;inset:-6px;border-radius:50%;box-shadow:0 0 38px -6px var(--gc,var(--b));opacity:.55;pointer-events:none}
.hinfo{flex:1;min-width:230px}
.who{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.av{width:50px;height:50px;border-radius:16px;display:grid;place-items:center;font:900 22px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;color:#fff;background:linear-gradient(135deg,var(--a),var(--b));box-shadow:0 12px 26px -10px var(--a)}
.who h1{font-size:19px;font-weight:900;word-break:break-word}.who small{color:var(--muted);font-size:11.5px;display:block;margin-top:2px}
.badge{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:99px;font-size:11.5px;font-weight:800;background:rgba(52,211,153,.14);color:var(--g);border:1px solid rgba(52,211,153,.35)}
.badge.off{background:rgba(251,113,133,.12);color:var(--r);border-color:rgba(251,113,133,.35)}
.badge i{width:8px;height:8px;border-radius:50%;background:currentColor;animation:pulse 1.8s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 currentColor}70%{box-shadow:0 0 0 8px transparent}100%{box-shadow:0 0 0 0 transparent}}
.mini{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.m{padding:12px;border-radius:16px;background:var(--card2);border:1px solid var(--line)}
.m small{display:block;font-size:10.5px;color:var(--soft);margin-bottom:4px}.m b{font:800 15px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif}
.grid{display:grid;grid-template-columns:1.25fr 1fr;gap:14px;margin-top:14px}
.card{padding:18px;border-radius:24px;background:var(--card);border:1px solid var(--line);backdrop-filter:blur(14px);box-shadow:var(--sh);animation:up .7s var(--ease) both}
.card h3{display:flex;align-items:center;gap:9px;font-size:14px;font-weight:800;margin-bottom:14px}.card h3 i{color:var(--b);font-size:19px}
.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.s{padding:14px;border-radius:18px;background:var(--card2);border:1px solid var(--line);transition:.2s var(--ease)}
.s:hover{transform:translateY(-3px);border-color:var(--line2)}.s i{font-size:20px;color:var(--c,var(--b))}.s small{display:block;color:var(--soft);font-size:10.5px;margin:7px 0 3px}.s b{font:800 17px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif}
.bar{height:9px;border-radius:9px;background:rgba(148,163,255,.14);overflow:hidden;margin:14px 0 4px}.bar i{display:block;height:100%;width:0;border-radius:9px;background:linear-gradient(90deg,var(--a),var(--b));transition:width .9s var(--ease)}
.chart{width:100%;height:150px;display:block}.chart .ln{fill:none;stroke:var(--b);stroke-width:2.4;stroke-linejoin:round;stroke-linecap:round}.chart .ar{fill:url(#cg)}.chart .gl{stroke:var(--line);stroke-width:1}.chart text{fill:var(--soft);font-size:10px;font-family:Inter}.chart .pt{fill:var(--b)}
.cs{font-size:10.5px;color:var(--soft);margin-top:6px}
.link{display:flex;align-items:center;gap:8px;padding:11px 12px;border-radius:15px;background:var(--card2);border:1px solid var(--line);direction:ltr;margin-bottom:12px}
.link code{flex:1;min-width:0;font:11.5px ui-monospace,Menlo,monospace;color:var(--b);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cp{height:38px;padding:0 14px;border-radius:11px;font-weight:800;font-size:12px;color:#fff;background:linear-gradient(100deg,#5b4bff,#7c5cff,#22a7e8);display:inline-flex;align-items:center;gap:6px;transition:.2s}
.cp:hover{filter:brightness(1.12)}.cp.ok{background:linear-gradient(100deg,#10b981,#34d399)}
.qrb{display:flex;gap:14px;align-items:center}
.qrb .qr{width:118px;height:118px;flex:none;border-radius:16px;background:#fff;padding:7px;box-shadow:0 14px 32px -14px rgba(124,92,255,.8)}
.qrb .qr img{width:100%;height:100%;display:block}.qrb p{font-size:11.5px;color:var(--muted);line-height:2}
.apps{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));gap:10px}.app{min-width:0}
.app{position:relative;display:flex;align-items:center;gap:12px;padding:13px;border-radius:18px;background:var(--card2);border:1px solid var(--line);transition:.22s var(--ease)}
.app:hover{transform:translateY(-3px);border-color:var(--line2)}
.app.rec{border-color:var(--a);box-shadow:0 14px 30px -18px var(--a)}.app.rec:after{content:"پیشنهادی";position:absolute;top:-9px;inset-inline-start:12px;font-size:9.5px;font-weight:800;padding:2px 9px;border-radius:99px;background:var(--a);color:#fff}
.app .ic{width:42px;height:42px;border-radius:13px;display:grid;place-items:center;font-size:22px;background:rgba(124,92,255,.15);color:var(--a);flex:none}
.app b{display:block;font-size:13.5px}.app small{font-size:10.5px;color:var(--soft)}
.app button{margin-inline-start:auto;height:34px;padding:0 14px;border-radius:10px;font-weight:800;font-size:12px;background:rgba(124,92,255,.18);color:var(--text);border:1px solid var(--line2);transition:.2s}
.app button:hover{background:var(--a);color:#fff}
.steps{counter-reset:s;display:grid;gap:10px}
.st{display:flex;gap:12px;align-items:flex-start;padding:12px;border-radius:16px;background:var(--card2);border:1px solid var(--line);font-size:12.5px;line-height:1.9;color:var(--muted)}
.st:before{counter-increment:s;content:counter(s);width:28px;height:28px;flex:none;border-radius:10px;display:grid;place-items:center;font:800 13px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;color:#fff;background:linear-gradient(135deg,var(--a),var(--b))}
.st b{color:var(--text)}
.sup{display:flex;align-items:center;gap:14px;flex-wrap:wrap;justify-content:space-between}
.sup p{font-size:12.5px;color:var(--muted);line-height:1.9}
.tg{display:inline-flex;align-items:center;gap:8px;padding:11px 20px;border-radius:14px;font-weight:800;font-size:13px;color:#fff;background:linear-gradient(100deg,#229ED9,#2aabee);box-shadow:0 14px 28px -14px #229ED9;transition:.2s}
.tg:hover{transform:translateY(-2px)}
.grid>*,.hinfo,.card,.hero{min-width:0}
.link code{display:block}
html,body{max-width:100%;overflow-x:hidden}
.m b,.s b,.gauge b{direction:ltr;unicode-bidi:isolate;display:block}
.m b{white-space:nowrap}
.foot{text-align:center;margin-top:22px;font:500 10px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;letter-spacing:.3em;color:var(--soft)}
.toast{position:fixed;bottom:calc(24px + env(safe-area-inset-bottom,0px));left:50%;transform:translate(-50%,30px);opacity:0;padding:11px 20px;border-radius:14px;background:#10b981;color:#fff;font-weight:800;font-size:13px;box-shadow:0 18px 40px -14px #10b981;transition:.3s var(--ease);z-index:50;pointer-events:none}
.toast.on{opacity:1;transform:translate(-50%,0)}
@media(max-width:760px){.grid{grid-template-columns:minmax(0,1fr)}.mini{grid-template-columns:1fr 1fr 1fr}.hero{padding:18px;border-radius:26px}.gauge{margin:0 auto}.hrow{justify-content:center}}
@media(max-width:420px){.mini{grid-template-columns:1fr 1fr}.mini .m:last-child{grid-column:1/-1}.who{flex-wrap:wrap}.who .badge{margin-inline-start:0!important}.qrb{flex-direction:column;text-align:center}.stats{grid-template-columns:1fr 1fr}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition-duration:.001ms!important}}

/* ---- v19.1 support card ---- */
.supc{position:relative;overflow:hidden;display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding:20px;border-radius:26px;border:1px solid var(--line2);background:linear-gradient(135deg,rgba(34,158,217,.18),rgba(15,21,44,.78) 48%,rgba(124,92,255,.16));backdrop-filter:blur(16px);box-shadow:var(--sh)}
body[data-theme=light] .supc{background:linear-gradient(135deg,rgba(34,158,217,.14),rgba(255,255,255,.92) 50%,rgba(124,92,255,.1))}
.supc:before{content:"";position:absolute;width:220px;height:220px;border-radius:50%;inset-inline-end:-70px;top:-90px;background:radial-gradient(circle,rgba(42,171,238,.35),transparent 70%);pointer-events:none}
.supc .si{position:relative;width:58px;height:58px;flex:none;border-radius:19px;display:grid;place-items:center;font-size:30px;color:#fff;background:linear-gradient(135deg,#229ED9,#7c5cff);box-shadow:0 14px 30px -12px #229ED9}
.supc .si:after{content:"";position:absolute;bottom:-3px;inset-inline-end:-3px;width:15px;height:15px;border-radius:50%;background:var(--g);border:3px solid var(--bgc,#0a0f25);animation:pulse 1.8s infinite;color:var(--g)}
.supc .sx{flex:1;min-width:200px;position:relative}
.supc .sx b{display:block;font-size:15px;font-weight:900;color:var(--text);margin-bottom:4px}
.supc .sx p{font-size:12.5px;color:var(--muted);line-height:1.9}
.supc .chips{display:flex;gap:7px;flex-wrap:wrap;margin-top:9px}
.supc .chips span{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:99px;font-size:10.5px;font-weight:700;color:var(--muted);background:var(--card2);border:1px solid var(--line)}
.supc .chips i{font-size:13px;color:var(--b)}
.supc .acts{position:relative;display:flex;gap:8px;flex-wrap:wrap}
.supc .tg{position:relative;overflow:hidden;padding:13px 24px;font-size:13.5px;direction:ltr}
.supc .tg:after{content:"";position:absolute;top:0;bottom:0;width:40%;left:-60%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.35),transparent);transform:skewX(-20deg);animation:shine 3.6s ease-in-out infinite}
@keyframes shine{0%,55%{left:-60%}100%{left:130%}}
.supc .tg.alt{background:rgba(124,92,255,.18);color:var(--text);border:1px solid var(--line2);box-shadow:none}
@media(max-width:560px){.supc{padding:16px;text-align:center;justify-content:center}.supc .sx{min-width:100%}.supc .chips,.supc .acts{justify-content:center}.supc .acts{width:100%}.supc .acts .tg{flex:1;justify-content:center}}
</style></head>
<body data-theme="dark"><div class="wrap">
 <div class="nav"><div class="brand"><img src="/assets/vw.png" alt=""><div><b>VODIWALKER</b><small>SUBSCRIPTION PORTAL</small></div></div>
  <div class="tools"><button class="ib" id="thBtn" title="Theme"><i class="ti ti-moon"></i></button><button class="ib" onclick="refresh(true)" title="Refresh"><i class="ti ti-refresh" id="rfI"></i></button></div></div>

 <section class="hero"><div class="hrow">
  <div class="gauge" id="gauge"><div><b id="pct">__PCT__%</b><small>مصرف حجم</small></div></div>
  <div class="hinfo">
   <div class="who"><div class="av">__INITIAL__</div><div><h1>__LABEL__</h1><small>__PROTOCOL__</small></div><span class="badge" id="stBadge" style="margin-inline-start:auto"><i></i><span id="stTxt">__STATUS__</span></span></div>
   <div class="mini"><div class="m"><small>مصرف‌شده</small><b id="used">__USED__</b></div><div class="m"><small>باقی‌مانده</small><b id="remaining">__REMAINING__</b></div><div class="m"><small>زمان باقی‌مانده</small><b id="left">—</b></div></div>
   <div class="bar"><i id="meter" style="width:__PCT__%"></i></div>
  </div></div></section>

 <div class="grid">
  <section class="card" style="animation-delay:.08s"><h3><i class="ti ti-chart-histogram"></i>روند مصرف</h3>
   <svg class="chart" id="chart" viewBox="0 0 900 170" preserveAspectRatio="none"><defs><linearGradient id="cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22d3ee" stop-opacity=".4"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></linearGradient></defs><g id="grid"></g><path class="ar" id="ar"/><path class="ln" id="ln"/><g id="pts"></g></svg>
   <div class="cs" id="cs">در حال دریافت داده…</div>
   <div class="stats" style="margin-top:14px">
    <div class="s" style="--c:var(--g)"><i class="ti ti-activity"></i><small>کاربر آنلاین</small><b id="live">__ACTIVE_CONN__</b></div>
    <div class="s" style="--c:var(--a)"><i class="ti ti-stack-2"></i><small>سشن فعال</small><b id="sess">__ACTIVE_SESSIONS__</b></div>
    <div class="s" style="--c:var(--w)"><i class="ti ti-database"></i><small>حجم کل</small><b>__LIMIT__</b></div>
    <div class="s" style="--c:var(--b)"><i class="ti ti-calendar-time"></i><small>انقضا</small><b style="font-size:13px" id="expTxt">__EXPIRES__</b></div>
    <div class="s"><i class="ti ti-device-mobile"></i><small>سقف اتصال</small><b style="font-size:12.5px">__CONN_LIMIT__</b></div>
    <div class="s" style="--c:var(--r)"><i class="ti ti-network"></i><small>سقف IP</small><b style="font-size:12.5px">__IP_LIMIT__</b></div>
   </div></section>

  <section class="card" style="animation-delay:.14s"><h3><i class="ti ti-link"></i>لینک اشتراک</h3>
   <div class="link"><code id="subUrl">__RAW__</code><button class="cp" id="cpBtn" onclick="copySub()"><i class="ti ti-copy"></i><span>کپی</span></button></div>
   <div class="qrb"><div class="qr"><img id="qrImg" alt="QR"></div><p>لینک را در برنامه‌ی کلاینت اضافه کن یا QR را اسکن کن. با هر بار بروزرسانی اشتراک، کانفیگ‌ها خودکار تازه می‌شوند.</p></div>
   <div style="margin-top:12px"><a class="cp" style="width:100%;justify-content:center;height:42px;background:var(--card2);color:var(--text);border:1px solid var(--line2)" href="__INFO_URL__" target="_blank" rel="noopener"><i class="ti ti-info-circle"></i>صفحه‌ی اطلاعات سرویس</a></div></section>
 </div>

 <section class="card" style="margin-top:14px;animation-delay:.2s"><h3><i class="ti ti-bolt"></i>اتصال سریع</h3>
  <div class="apps" id="apps"></div></section>

 <section class="card" style="margin-top:14px;animation-delay:.26s"><h3><i class="ti ti-info-circle"></i>راهنمای اتصال</h3>
  <div class="steps"><div class="st"><span>یکی از برنامه‌های بالا را نصب کن (برای اندروید <b>v2rayNG</b> یا <b>Hiddify</b>، برای iOS <b>Streisand</b> یا <b>Hiddify</b>).</span></div>
   <div class="st"><span>روی دکمه‌ی <b>اتصال</b> بزن، یا لینک اشتراک را کپی و در برنامه از بخش <b>Subscription / اشتراک</b> اضافه کن.</span></div>
   <div class="st"><span>بعد از افزودن، اشتراک را <b>بروزرسانی</b> کن و از میان کانفیگ‌ها یکی را انتخاب کن؛ اگر روی اینترنت‌تان وصل نشد، کانفیگ دیگری را امتحان کن (هر اپراتور ممکن است کانفیگ مخصوص خودش داشته باشد).</span></div></div></section>

 <section class="supc card" style="margin-top:14px;animation-delay:.32s"><div class="si"><i class="ti ti-headset"></i></div>
  <div class="sx"><b>پشتیبانی آنلاین VodiWalker</b><p>برای تمدید اشتراک، افزایش حجم یا هر مشکل در اتصال، مستقیم در تلگرام پیام بده.</p>
   <div class="chips"><span><i class="ti ti-clock-hour-4"></i>پاسخگویی سریع</span><span><i class="ti ti-refresh"></i>تمدید و ارتقا</span><span><i class="ti ti-plug-connected"></i>رفع مشکل اتصال</span></div></div>
  <div class="acts"><a class="tg" href="__SUPPORT_URL__" target="_blank" rel="noopener"><i class="ti ti-brand-telegram"></i>__SUPPORT__</a></div></section>
 <div class="foot">VODIWALKER · LIVE <span id="upd"></span></div>
</div><div class="toast" id="toast">کپی شد ✓</div>

<script>
const SUB_URL=__RAW_JS__,EXPIRES='__EXPIRES__',$=i=>document.getElementById(i);
const fmt=b=>{b=Number(b)||0;const u=['B','KB','MB','GB','TB'];let i=0;while(b>=1024&&i<4){b/=1024;i++}return (i>1?b.toFixed(2):Math.round(b))+' '+u[i]};
/* theme */
(function(){let t='dark';try{t=localStorage.getItem('vw_portal_theme')||(matchMedia('(prefers-color-scheme:light)').matches?'light':'dark')}catch(e){}apply(t);
 $('thBtn').onclick=function(){t=t==='dark'?'light':'dark';apply(t);try{localStorage.setItem('vw_portal_theme',t)}catch(e){}};
 function apply(x){document.body.dataset.theme=x;$('thBtn').firstChild.className='ti '+(x==='dark'?'ti-moon':'ti-sun');document.querySelector('meta[name=theme-color]').content=x==='dark'?'#060912':'#eef2fb'}})();
/* QR */
(function(){try{const q=qrcode(0,'M');q.addData(SUB_URL);q.make();$('qrImg').src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(q.createSvgTag(4,0))}catch(e){$('qrImg').src='https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=__QR__'}})();
/* copy */
function toast(t){const e=$('toast');e.textContent=t;e.classList.add('on');setTimeout(()=>e.classList.remove('on'),1800)}
function copyText(v){return(navigator.clipboard&&navigator.clipboard.writeText?navigator.clipboard.writeText(v):Promise.reject()).catch(()=>{const a=document.createElement('textarea');a.value=v;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove()})}
function copySub(){copyText(SUB_URL).then(()=>{const b=$('cpBtn');b.classList.add('ok');b.lastChild.textContent='کپی شد';toast('لینک اشتراک کپی شد ✓');setTimeout(()=>{b.classList.remove('ok');b.lastChild.textContent='کپی'},1800)})}
/* apps */
const UA=navigator.userAgent,OS=/android/i.test(UA)?'android':/iphone|ipad|ipod/i.test(UA)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1)?'ios':/windows/i.test(UA)?'win':/mac/i.test(UA)?'mac':'other';
const APPS=[{n:'Hiddify',t:'همه‌ی پلتفرم‌ها',os:['android','ios','win','mac'],ic:'ti-shield-bolt',u:()=>'hiddify://import/'+SUB_URL+'#VodiWalker'},
 {n:'v2rayNG',t:'اندروید',os:['android'],ic:'ti-brand-android',u:()=>'v2rayng://install-sub?url='+encodeURIComponent(SUB_URL)+'&name=VodiWalker'},
 {n:'Streisand',t:'iOS / macOS',os:['ios','mac'],ic:'ti-brand-apple',u:()=>'streisand://import/'+SUB_URL},
 {n:'Shadowrocket',t:'iOS',os:['ios'],ic:'ti-brand-apple',u:()=>'shadowrocket://add/sub://'+btoa(unescape(encodeURIComponent(SUB_URL)))},
 {n:'sing-box',t:'همه‌ی پلتفرم‌ها',os:['android','ios','win','mac'],ic:'ti-box',u:()=>'sing-box://import-remote-profile?url='+encodeURIComponent(SUB_URL)+'#VodiWalker'}];
$('apps').innerHTML=APPS.slice().sort((a,b)=>b.os.includes(OS)-a.os.includes(OS)).map((a,i)=>`<div class="app ${i===0&&a.os.includes(OS)?'rec':''}"><div class="ic"><i class="ti ${a.ic}"></i></div><div><b>${a.n}</b><small>${a.t}</small></div><button onclick="go(${APPS.indexOf(a)})">اتصال</button></div>`).join('');
function go(i){const u=APPS[i].u();copyText(SUB_URL);toast('لینک کپی شد؛ در حال باز کردن برنامه…');setTimeout(()=>{location.href=u},350)}
/* countdown */
function left(){const t=Date.parse(EXPIRES);if(isNaN(t)){$('left').textContent='نامحدود';return}
 let s=Math.floor((t-Date.now())/1000);if(s<=0){$('left').textContent='منقضی';return}const d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60);
 $('left').textContent=d>0?d+' روز '+h+' ساعت':h+':'+String(m).padStart(2,'0')+' ساعت'}
left();setInterval(left,30000);$('expTxt').textContent=isNaN(Date.parse(EXPIRES))?EXPIRES:EXPIRES.slice(0,10);
/* gauge colour */
function setGauge(p){const g=$('gauge');g.style.setProperty('--pct',p);g.style.setProperty('--gc',p>=90?'var(--r)':p>=70?'var(--w)':'var(--b)');
 g.style.setProperty('--bgc',document.body.dataset.theme==='light'?'#fff':'#0a0f25')}
/* chart */
function draw(h,limit){const clean=(h||[]).filter(x=>x&&isFinite(x.used)),grid=$('grid'),pts=$('pts');
 if(clean.length<2){$('ln').setAttribute('d','M0 158 L900 158');$('ar').setAttribute('d','');grid.innerHTML='';pts.innerHTML='';$('cs').textContent='در حال جمع‌آوری داده…';return}
 const v=clean.map(x=>+x.used),max=Math.max(+limit||0,...v,1),T=14,B=160,H=B-T;
 grid.innerHTML=[0,.5,1].map(r=>{const y=B-H*r;return `<line class="gl" x1="0" y1="${y}" x2="900" y2="${y}"/><text x="4" y="${y-4}">${fmt(max*r)}</text>`}).join('');
 const p=v.map((x,i)=>[i*(900/(v.length-1)),B-(x/max)*H]),d=p.map((q,i)=>(i?'L':'M')+q[0].toFixed(1)+' '+q[1].toFixed(1)).join(' ');
 $('ln').setAttribute('d',d);$('ar').setAttribute('d',d+' L900 '+B+' L0 '+B+' Z');const l=p[p.length-1];pts.innerHTML=`<circle class="pt" cx="${l[0]}" cy="${l[1]}" r="5"/>`;
 $('cs').textContent=clean.length+' نقطه · آخرین مقدار '+fmt(v[v.length-1])}
let _rb=false;async function refresh(manual){if(_rb)return;_rb=true;const ic=$('rfI');if(manual)ic.style.animation='spin .7s linear infinite';
 try{const r=await fetch('/api/subscription/__UUID__',{cache:'no-store'});if(!r.ok)throw 0;const d=await r.json(),lim=+d.traffic_limit||0,used=+d.traffic_used||0,p=lim?Math.min(100,Math.round(used/lim*1000)/10):0;
  setGauge(p);$('pct').textContent=lim?p+'%':'∞';$('used').textContent=fmt(used);$('remaining').textContent=lim?fmt(Math.max(0,lim-used)):'نامحدود';$('meter').style.width=(lim?p:0)+'%';
  $('live').textContent=d.active_connections||0;$('sess').textContent=d.active_sessions||0;
  $('stTxt').textContent=d.active?'فعال':'غیرفعال';$('stBadge').classList.toggle('off',!d.active);draw(d.usage_history,lim);
  $('upd').textContent='· '+new Date().toLocaleTimeString('fa-IR',{hour:'2-digit',minute:'2-digit'})}catch(e){$('cs').textContent='همگام‌سازی ناموفق'}
 ic.style.animation='';_rb=false}
setGauge(+'__PCT__'||0);refresh();setInterval(()=>{if(!document.hidden)refresh()},20000);
</script></body></html>'''


# ======================================================================
# صفحه‌ی عمومی «گروه اشتراک» (/p/{key}) — همان API قبلی: /api/public/sub/{key}
# ======================================================================
_css = PORTAL_V18[PORTAL_V18.index('<style>') + 7:PORTAL_V18.index('</style>')]

PUBLIC_SUB_V18 = r'''<!doctype html><html lang="fa" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#060912"><title>اشتراک · VodiWalker</title>
<link rel="stylesheet" href="/assets/ui.css"><script src="/assets/qr.js"></script>
<style>''' + _css + r'''
.cfgs{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:12px}
.cfg{position:relative;padding:15px;border-radius:20px;background:var(--card2);border:1px solid var(--line);transition:.22s var(--ease);overflow:hidden}
.cfg:before{content:"";position:absolute;top:0;inset-inline:16px;height:2px;background:linear-gradient(90deg,transparent,var(--oc,var(--a)),transparent)}
.cfg:hover{transform:translateY(-3px);border-color:var(--line2);box-shadow:0 20px 40px -26px var(--oc,var(--a))}
.cfg.off{opacity:.6}
.cfg-top{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.cfg-ic{width:40px;height:40px;border-radius:13px;display:grid;place-items:center;font-size:20px;flex:none;color:var(--oc,var(--a));background:color-mix(in srgb,var(--oc,var(--a)) 16%,transparent)}
.cfg-name{font-size:13.5px;font-weight:800;word-break:break-word}.cfg-sub{display:flex;gap:6px;align-items:center;margin-top:3px;font:600 10px 'Inter',system-ui,sans-serif;color:var(--soft)}
.opb{padding:2px 9px;border-radius:99px;font:800 10px 'Vazirmatn',sans-serif;color:var(--oc,var(--a));background:color-mix(in srgb,var(--oc,var(--a)) 15%,transparent);border:1px solid color-mix(in srgb,var(--oc,var(--a)) 40%,transparent)}
.cfg .badge{margin-inline-start:auto;padding:4px 10px;font-size:10.5px}
.cmeta{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin:10px 0 12px}.cmeta div{padding:8px;border-radius:12px;background:var(--card);border:1px solid var(--line);text-align:center}
.cmeta small{display:block;font-size:9.5px;color:var(--soft);margin-bottom:3px}.cmeta b{font:800 11.5px 'Inter',system-ui,sans-serif}
.cmeta b{direction:ltr;unicode-bidi:isolate}.cmeta div:last-child b{font-size:10px;white-space:nowrap}
.crow{display:flex;gap:7px}.crow button{flex:1;height:36px;border-radius:11px;font-weight:800;font-size:11.5px;display:inline-flex;align-items:center;justify-content:center;gap:5px;background:rgba(124,92,255,.14);border:1px solid var(--line2);color:var(--text);transition:.2s}
.crow button:hover{background:var(--a);color:#fff}
.lock{max-width:420px;margin:60px auto;text-align:center}
.lock input{width:100%;height:50px;border-radius:15px;border:1px solid var(--line2);background:var(--card2);color:var(--text);text-align:center;font-size:15px;margin:14px 0 10px;direction:ltr}
.lock input:focus{outline:none;border-color:var(--a);box-shadow:0 0 0 4px rgba(124,92,255,.2)}
.ov{position:fixed;inset:0;z-index:60;display:none;align-items:center;justify-content:center;background:rgba(3,5,14,.78);backdrop-filter:blur(7px);padding:16px}.ov.on{display:flex}
.mbox{width:100%;max-width:340px;padding:20px;border-radius:24px;background:var(--card);border:1px solid var(--line2);text-align:center;animation:up .3s var(--ease)}
.mbox img{width:220px;height:220px;border-radius:16px;background:#fff;padding:9px;margin:10px auto}.mbox b{font-size:14px}
.empty{padding:34px;text-align:center;color:var(--soft)}
</style></head>
<body data-theme="dark"><div class="wrap">
 <div class="nav"><div class="brand"><img src="/assets/vw.png" alt=""><div><b>VODIWALKER</b><small>SUBSCRIPTION CENTER</small></div></div>
  <div class="tools"><button class="ib" id="thBtn" title="Theme"><i class="ti ti-moon"></i></button><button class="ib" onclick="load(true)" title="Refresh"><i class="ti ti-refresh" id="rfI"></i></button></div></div>
 <div id="app"><div class="empty">در حال دریافت…</div></div>
 <div class="foot">VODIWALKER · LIVE <span id="upd"></span></div>
</div>
<div class="ov" id="qov" onclick="if(event.target===this)this.classList.remove('on')"><div class="mbox"><b id="qt"></b><img id="qimg" alt="QR"><button class="cp" style="width:100%;justify-content:center;height:42px" onclick="document.getElementById('qov').classList.remove('on')">بستن</button></div></div>
<div class="toast" id="toast">کپی شد ✓</div>
<script>
var KEY=location.pathname.split('/').pop(),QS=location.search||'',$=function(i){return document.getElementById(i)};
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function toast(t){var e=$('toast');e.textContent=t;e.classList.add('on');clearTimeout(toast._t);toast._t=setTimeout(function(){e.classList.remove('on')},1800)}
function copyText(v){function fb(){var a=document.createElement('textarea');a.value=v;a.style.cssText='position:fixed;opacity:0';document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(e){}a.remove()}
 if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(v).catch(fb)}else fb();toast('کپی شد ✓')}
function fmt(n){n=Number(n)||0;if(!n)return'0 B';var u=['B','KB','MB','GB','TB'],i=0;while(n>=1024&&i<4){n/=1024;i++}return(n>=100?Math.round(n):n>=10?n.toFixed(1):n.toFixed(2))+' '+u[i]}
function daysLeft(iso){if(!iso)return null;var t=new Date(String(iso).replace(' ','T')).getTime();return isNaN(t)?null:Math.ceil((t-Date.now())/864e5)}
function qrUrl(v){try{var q=qrcode(0,'M');q.addData(v);q.make();return'data:image/svg+xml;charset=utf-8,'+encodeURIComponent(q.createSvgTag(5,4))}catch(e){return''}}
function b64(s){try{return btoa(unescape(encodeURIComponent(s)))}catch(e){return''}}
(function(){var t='dark';try{t=localStorage.getItem('vw_portal_theme')||(matchMedia('(prefers-color-scheme:light)').matches?'light':'dark')}catch(e){}ap(t);
 $('thBtn').onclick=function(){t=t==='dark'?'light':'dark';ap(t);try{localStorage.setItem('vw_portal_theme',t)}catch(e){}};
 function ap(x){document.body.dataset.theme=x;$('thBtn').firstChild.className='ti '+(x==='dark'?'ti-moon':'ti-sun');if(window.G)setRing()}})();
var OPS=[['همراه اول','#38bdf8','ti-antenna-bars-5'],['ایرانسل','#facc15','ti-device-mobile'],['مخابرات','#a78bfa','ti-router'],['رایتل','#fb7185','ti-radio']];
function opOf(l){var n=l||'';for(var i=0;i<OPS.length;i++){if(n.indexOf(OPS[i][0])>-1)return OPS[i]}return null}
var UA=navigator.userAgent,OS=/android/i.test(UA)?'android':/iphone|ipad|ipod/i.test(UA)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1)?'ios':/windows/i.test(UA)?'win':/mac/i.test(UA)?'mac':'other';
function appsFor(url,name){var enc=encodeURIComponent(url),nm=encodeURIComponent(name||'VodiWalker');return[
 {n:'Hiddify',t:'همه‌ی پلتفرم‌ها',os:['android','ios','win','mac'],ic:'ti-shield-bolt',u:'hiddify://import/'+url+'#'+nm},
 {n:'v2rayNG',t:'اندروید',os:['android'],ic:'ti-brand-android',u:'v2rayng://install-sub?url='+enc+'&name='+nm},
 {n:'Streisand',t:'iOS / macOS',os:['ios','mac'],ic:'ti-brand-apple',u:'streisand://import/'+url},
 {n:'Shadowrocket',t:'iOS',os:['ios'],ic:'ti-brand-apple',u:'shadowrocket://add/sub://'+b64(url)},
 {n:'sing-box',t:'همه‌ی پلتفرم‌ها',os:['android','ios','win','mac'],ic:'ti-box',u:'sing-box://import-remote-profile?url='+enc+'#'+nm}]}
function goApp(i){var a=window.APPS[i];copyText(window.SUBURL);setTimeout(function(){location.href=a.u},350)}
function showQr(t,v){$('qt').textContent=t;$('qimg').src=qrUrl(v);$('qov').classList.add('on')}
function setRing(){var g=$('gauge');if(!g||!window.G)return;g.style.setProperty('--pct',G.pct);g.style.setProperty('--gc',G.pct>=90?'var(--r)':G.pct>=70?'var(--w)':'var(--b)');g.style.setProperty('--bgc',document.body.dataset.theme==='light'?'#fff':'#0a0f25')}
function render(d){var app=$('app');
 if(d.locked){app.innerHTML='<section class="card lock"><h3 style="justify-content:center"><i class="ti ti-lock"></i>'+esc(d.name||'اشتراک')+'</h3><p style="font-size:12.5px;color:var(--muted);line-height:2">این اشتراک با رمز محافظت می‌شود. رمز را وارد کن.</p><form id="pwF"><input id="pw" type="password" placeholder="رمز اشتراک" autocomplete="off"><button class="cp" style="width:100%;justify-content:center;height:46px">ورود</button></form></section>';
  $('pwF').onsubmit=function(e){e.preventDefault();location.search='?pw='+encodeURIComponent($('pw').value)};return}
 var links=d.links||[],url=d.sub_url||'';window.SUBURL=url;
 var used=+d.total_used_bytes||0,limit=+d.total_limit_bytes||0,pct=limit>0?Math.min(100,Math.round(used/limit*1000)/10):0,rem=limit>0?Math.max(0,limit-used):null;
 var dl=daysLeft(d.expires_at),act=links.filter(function(x){return x.active}).length,dead=(dl!==null&&dl<=0)||(limit>0&&used>=limit)||(links.length>0&&act===0);
 window.G={pct:pct};window.APPS=appsFor(url,d.name);
 var apps=window.APPS.slice().sort(function(a,b){return b.os.indexOf(OS)>-1?1:-1}).map(function(a,i){var rec=i===0&&a.os.indexOf(OS)>-1;return'<div class="app'+(rec?' rec':'')+'"><div class="ic"><i class="ti '+a.ic+'"></i></div><div><b>'+a.n+'</b><small>'+a.t+'</small></div><button onclick="goApp('+window.APPS.indexOf(a)+')">اتصال</button></div>'}).join('');
 var cf=links.length?links.map(function(l,i){var o=opOf(l.label),oc=o?o[1]:'#7c5cff',lp=+l.limit_bytes>0?Math.min(100,Math.round((+l.used_bytes||0)/(+l.limit_bytes)*100)):0;
  return'<article class="cfg'+(l.active?'':' off')+'" style="--oc:'+oc+'"><div class="cfg-top"><div class="cfg-ic"><i class="ti '+(o?o[2]:'ti-bolt')+'"></i></div><div><div class="cfg-name">'+esc(l.label||'Config')+'</div><div class="cfg-sub">'+(o?'<span class="opb">'+o[0]+'</span>':'')+'<span>'+esc(String(l.protocol||'vless').toUpperCase())+'</span></div></div><span class="badge'+(l.active?'':' off')+'"><i></i>'+(l.active?'فعال':'غیرفعال')+'</span></div>'
  +'<div class="bar" style="margin:0"><i style="width:'+(+l.limit_bytes>0?lp:100)+'%"></i></div>'
  +'<div class="cmeta"><div><small>مصرف</small><b>'+esc(l.used_fmt||'0 B')+' / '+esc(l.limit_fmt||'∞')+'</b></div><div><small>آنلاین</small><b>'+(+l.connections||0)+' / '+((+l.connection_limit||0)||'∞')+'</b></div><div><small>انقضا</small><b>'+esc(String(l.expires_at||'∞').slice(0,10))+'</b></div></div>'
  +'<div class="crow"><button data-c="'+i+'" data-k="v"><i class="ti ti-copy"></i>کانفیگ</button><button data-c="'+i+'" data-k="q"><i class="ti ti-qrcode"></i>QR</button><button data-c="'+i+'" data-k="s"><i class="ti ti-link"></i>ساب</button></div></article>'}).join(''):'<div class="empty">هنوز کانفیگی برای این اشتراک ثبت نشده است.</div>';
 app.innerHTML='<section class="hero"><div class="hrow"><div class="gauge" id="gauge"><div><b>'+(limit>0?pct+'%':'∞')+'</b><small>'+(limit>0?'مصرف حجم':'نامحدود')+'</small></div></div>'
  +'<div class="hinfo"><div class="who"><div class="av">'+esc((d.name||'V').trim().charAt(0).toUpperCase())+'</div><div><h1>'+esc(d.name||'اشتراک')+'</h1><small>'+esc(d.desc||'همه‌ی کانفیگ‌ها، مصرف و زمان باقی‌مانده در یک صفحه')+'</small></div><span class="badge'+(dead?' off':'')+'" style="margin-inline-start:auto"><i></i>'+(dead?'غیرفعال':'فعال')+'</span></div>'
  +'<div class="mini"><div class="m"><small>مصرف‌شده</small><b>'+fmt(used)+'</b></div><div class="m"><small>باقی‌مانده</small><b>'+(rem===null?'نامحدود':fmt(rem))+'</b></div><div class="m"><small>روز باقی‌مانده</small><b>'+(dl===null?'∞':(dl<=0?'0':dl))+'</b></div></div>'
  +'<div class="bar"><i style="width:'+(limit>0?pct:0)+'%"></i></div></div></div></section>'
  +'<div class="grid"><section class="card"><h3><i class="ti ti-link"></i>لینک اشتراک</h3><div class="link"><code>'+esc(url)+'</code><button class="cp" id="cpU"><i class="ti ti-copy"></i><span>کپی</span></button></div>'
  +'<div class="qrb"><div class="qr"><img alt="QR" src="'+qrUrl(url)+'"></div><p>این لینک شامل <b>'+links.length+'</b> کانفیگ ('+act+' فعال) است. در برنامه اضافه کن و بروزرسانی بزن؛ هر کانفیگ مخصوص یک اپراتور است، همانی را انتخاب کن که روی اینترنتت وصل می‌شود.</p></div></section>'
  +'<section class="card"><h3><i class="ti ti-chart-histogram"></i>وضعیت</h3><div class="stats"><div class="s" style="--c:var(--g)"><i class="ti ti-activity"></i><small>کاربر آنلاین</small><b>'+(+d.active_connections||0)+'</b></div><div class="s" style="--c:var(--a)"><i class="ti ti-stack-2"></i><small>کانفیگ فعال</small><b>'+act+'/'+links.length+'</b></div><div class="s" style="--c:var(--w)"><i class="ti ti-database"></i><small>حجم کل</small><b>'+(limit>0?fmt(limit):'∞')+'</b></div><div class="s" style="--c:var(--b)"><i class="ti ti-calendar-time"></i><small>انقضا</small><b style="font-size:13px">'+esc(String(d.expires_at||'نامحدود').slice(0,10))+'</b></div></div></section></div>'
  +'<section class="card" style="margin-top:14px"><h3><i class="ti ti-bolt"></i>اتصال سریع</h3><div class="apps">'+apps+'</div></section>'
  +'<section class="card" style="margin-top:14px"><h3><i class="ti ti-stack-2"></i>کانفیگ‌ها</h3><div class="cfgs">'+cf+'</div></section>'
  +'<section class="supc card" style="margin-top:14px"><div class="si"><i class="ti ti-headset"></i></div><div class="sx"><b>پشتیبانی آنلاین VodiWalker</b><p>برای تمدید اشتراک، افزایش حجم یا هر مشکل در اتصال، مستقیم در تلگرام پیام بده.</p><div class="chips"><span><i class="ti ti-clock-hour-4"></i>پاسخگویی سریع</span><span><i class="ti ti-refresh"></i>تمدید و ارتقا</span><span><i class="ti ti-plug-connected"></i>رفع مشکل اتصال</span></div></div><div class="acts"><a class="tg" href="'+esc(d.support_url||'#')+'" target="_blank" rel="noopener"><i class="ti ti-brand-telegram"></i>'+esc(d.support||'پشتیبانی')+'</a>'+(d.channel_url?'<a class="tg alt" href="'+esc(d.channel_url)+'" target="_blank" rel="noopener"><i class="ti ti-speakerphone"></i>کانال</a>':'')+'</div></section>';
 setRing();$('cpU').onclick=function(){copyText(url)};
 [].forEach.call(document.querySelectorAll('.crow button'),function(b){b.onclick=function(){var l=links[+b.dataset.c],k=b.dataset.k;if(k==='v')copyText(l.vless_link||'');else if(k==='s')copyText(l.sub_url||'');else showQr(l.label||'Config',l.vless_link||'')}})}
var busy=false;
async function load(manual){if(busy)return;busy=true;var ic=$('rfI');if(manual)ic.style.animation='spin .7s linear infinite';
 try{var r=await fetch('/api/public/sub/'+encodeURIComponent(KEY)+QS,{cache:'no-store'});if(!r.ok)throw 0;render(await r.json());$('upd').textContent='· '+new Date().toLocaleTimeString('fa-IR',{hour:'2-digit',minute:'2-digit'})}
 catch(e){if(!window.G)$('app').innerHTML='<div class="empty">گروه پیدا نشد یا در دسترس نیست.</div>'}
 ic.style.animation='';busy=false}
load();setInterval(function(){if(!document.hidden&&!document.querySelector('.ov.on')&&!document.activeElement.matches('input'))load()},20000);
</script></body></html>'''


# ======================================================================
# v19 · لایه‌ی انیمیشن و ظاهر حرفه‌ای (برای پورتال و صفحه‌ی گروه اشتراک)
# بدون دست‌زدن به placeholderها و منطق قبلی؛ فقط CSS/JS اضافه می‌شود.
# ======================================================================
FX_CSS = r'''
/* ===== v19 · FX layer ===== */
.fx-bg{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden;--px:0;--py:0}
.fx-bg canvas{position:absolute;inset:0}
.fx-bg .o{position:absolute;border-radius:50%;filter:blur(70px);opacity:.5;will-change:transform;translate:calc(var(--px)*46px) calc(var(--py)*34px)}
.fx-bg .o1{width:46vmax;height:46vmax;left:-12vmax;top:-14vmax;background:radial-gradient(circle,rgba(124,92,255,.55),transparent 65%);animation:fxF1 22s ease-in-out infinite alternate}
.fx-bg .o2{width:40vmax;height:40vmax;right:-14vmax;top:18vh;background:radial-gradient(circle,rgba(34,211,238,.38),transparent 65%);animation:fxF2 27s ease-in-out infinite alternate}
.fx-bg .o3{width:34vmax;height:34vmax;left:22vw;bottom:-18vmax;background:radial-gradient(circle,rgba(251,113,133,.26),transparent 65%);animation:fxF3 31s ease-in-out infinite alternate}
.fx-bg .gridl{position:absolute;inset:0;background-image:linear-gradient(rgba(148,163,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(148,163,255,.07) 1px,transparent 1px);background-size:56px 56px;
 -webkit-mask-image:radial-gradient(65% 55% at 50% 25%,#000,transparent 78%);mask-image:radial-gradient(65% 55% at 50% 25%,#000,transparent 78%);animation:fxGrid 18s linear infinite}
body[data-theme=light] .fx-bg .o{opacity:.26}
body[data-theme=light] .fx-bg .gridl{background-image:linear-gradient(rgba(60,70,140,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(60,70,140,.09) 1px,transparent 1px)}
@keyframes fxF1{to{transform:translate3d(8vw,10vh,0) scale(1.15)}}
@keyframes fxF2{to{transform:translate3d(-10vw,-8vh,0) scale(1.1)}}
@keyframes fxF3{to{transform:translate3d(12vw,-10vh,0) scale(1.2)}}
@keyframes fxGrid{to{background-position:56px 56px,56px 56px}}

/* nav شیشه‌ای و چسبان */
.nav{position:sticky;top:calc(8px + env(safe-area-inset-top,0px));z-index:30;padding:9px 12px;border-radius:20px;background:var(--card);border:1px solid var(--line);backdrop-filter:blur(18px) saturate(1.4);-webkit-backdrop-filter:blur(18px) saturate(1.4);box-shadow:var(--sh)}
.brand b{background:linear-gradient(90deg,var(--text),var(--b),var(--a),var(--text));background-size:300% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;animation:fxTxt 7s linear infinite}
@keyframes fxTxt{to{background-position:-300% 0}}
.brand img{animation:fxFloat 5s ease-in-out infinite}
@keyframes fxFloat{50%{transform:translateY(-4px)}}

/* hero */
.hero{background-size:220% 220%;animation:up .8s var(--ease) both,fxHero 14s ease-in-out infinite alternate}
@keyframes fxHero{from{background-position:0% 0%}to{background-position:100% 100%}}
.hero:after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(115deg,transparent 38%,rgba(255,255,255,.08) 50%,transparent 62%);transform:translateX(-110%);animation:fxSweep 7s ease-in-out infinite}
@keyframes fxSweep{55%,100%{transform:translateX(110%)}}
.av{animation:fxFloat 4.6s ease-in-out infinite}
.who h1{background:linear-gradient(90deg,var(--text) 0,var(--b) 38%,var(--a) 62%,var(--text) 100%);background-size:250% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;animation:fxTxt 9s linear infinite}
.gauge:after{animation:fxBreath 3.2s ease-in-out infinite}
@keyframes fxBreath{50%{opacity:.95;box-shadow:0 0 54px -2px var(--gc,var(--b))}}
.g-orbit{position:absolute;inset:-7px;border-radius:50%;pointer-events:none;animation:fxSpin 7s linear infinite}
.g-orbit:before{content:"";position:absolute;top:-3.5px;left:50%;width:7px;height:7px;margin-left:-3.5px;border-radius:50%;background:var(--gc,var(--b));box-shadow:0 0 14px 3px var(--gc,var(--b))}
.g-orbit:after{content:"";position:absolute;inset:0;border-radius:50%;border:1px dashed rgba(148,163,255,.3)}
@keyframes fxSpin{to{transform:rotate(360deg)}}
.bar i{position:relative;overflow:hidden}
.bar i:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.55),transparent);transform:translateX(-100%);animation:fxBar 2.4s ease-in-out infinite}
@keyframes fxBar{70%,100%{transform:translateX(100%)}}

/* کارت‌ها: نور دنبال‌کننده‌ی ماوس */
.card,.s,.m,.cfg{position:relative}
.card,.s,.app,.cfg,.m{background-image:radial-gradient(240px circle at var(--mx,-300px) var(--my,-300px),rgba(124,92,255,.16),transparent 66%)}
.card h3:after{content:"";flex:1;height:1px;margin-inline-start:6px;background:linear-gradient(90deg,var(--line2),transparent)}
html[dir=rtl] .card h3:after{background:linear-gradient(270deg,var(--line2),transparent)}
.s i,.cfg-ic,.app .ic{transition:transform .35s var(--ease)}
.s:hover i{transform:scale(1.2) rotate(-7deg)}.app:hover .ic{transform:scale(1.12) rotate(5deg)}.cfg:hover .cfg-ic{transform:scale(1.1) rotate(-5deg)}
.app.rec{animation:fxRec 2.6s ease-in-out infinite alternate}
@keyframes fxRec{to{box-shadow:0 16px 38px -14px var(--a)}}
.cp,.tg,.app button,.crow button{position:relative;overflow:hidden}
.cp:after,.tg:after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.4) 50%,transparent 70%);transform:translateX(-130%);animation:fxShine 4s ease-in-out infinite}
@keyframes fxShine{55%,100%{transform:translateX(130%)}}
.qrb .qr{position:relative;overflow:hidden}
.qrb .qr:after{content:"";position:absolute;left:0;right:0;height:28%;top:-32%;background:linear-gradient(180deg,transparent,rgba(124,92,255,.38),transparent);animation:fxScan 3.2s ease-in-out infinite}
@keyframes fxScan{to{top:112%}}
.chart .ln{stroke-dasharray:4000;stroke-dashoffset:4000;animation:fxDraw 2.4s .3s var(--ease) forwards}
.chart .ar{animation:fxFade 1.4s .9s both}
@keyframes fxDraw{to{stroke-dashoffset:0}}@keyframes fxFade{from{opacity:0}to{opacity:1}}
.st:before{box-shadow:0 8px 18px -8px var(--a)}

/* ظهور تدریجی هنگام اسکرول */
.fx-on .fx-rv{opacity:0;transform:translateY(22px) scale(.97)}
.fx-on .fx-rv.in{opacity:1;transform:none;transition:opacity .65s var(--ease),transform .65s var(--ease)}
.fx-settled .card{animation:none}
.fx-settled .hero{animation:fxHero 14s ease-in-out infinite alternate}

/* انفجار ذرات روی کلیک */
.fx-p{position:fixed;z-index:120;width:7px;height:7px;border-radius:50%;pointer-events:none;transform:translate(-50%,-50%);animation:fxBurst .75s cubic-bezier(.2,.8,.3,1) forwards}
@keyframes fxBurst{to{transform:translate(calc(-50% + var(--dx)),calc(-50% + var(--dy))) scale(.2);opacity:0}}
.toast{backdrop-filter:blur(10px);box-shadow:0 18px 40px -16px rgba(16,185,129,.7)}
.cmeta{grid-template-columns:1.7fr 1fr 1.25fr!important}.cmeta b{white-space:nowrap;font-size:10.5px!important}
::selection{background:rgba(124,92,255,.4)}
@media(max-width:560px){.fx-bg .gridl{display:none}.nav{border-radius:16px}}
'''

FX_JS = r'''
(function(){try{
var doc=document,body=doc.body,root=doc.documentElement;
var RM=!!(window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches);
function qa(s){return [].slice.call(doc.querySelectorAll(s))}
/* پس‌زمینه: orbها + گرید + ذرات متصل */
var bg=doc.createElement('div');bg.className='fx-bg';
bg.innerHTML='<i class="o o1"></i><i class="o o2"></i><i class="o o3"></i><i class="gridl"></i>'+'';
body.insertBefore(bg,body.firstChild);
var cv=doc.getElementById('fxc'),mx=-999,my=-999;
if(cv){var cx=cv.getContext('2d'),W=0,H=0,D=Math.min(window.devicePixelRatio||1,2),P=[],run=true;
 var size=function(){W=innerWidth;H=innerHeight;cv.width=W*D;cv.height=H*D;cv.style.width=W+'px';cv.style.height=H+'px';cx.setTransform(D,0,0,D,0,0);
  var n=Math.max(16,Math.min(60,Math.round(W*H/26000)));while(P.length<n)P.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.35,vy:(Math.random()-.5)*.35,r:Math.random()*1.5+.6});P.length=n};
 size();addEventListener('resize',size);
 doc.addEventListener('visibilitychange',function(){run=!doc.hidden;if(run)tick()});
 var tick=function(){if(!run)return;cx.clearRect(0,0,W,H);
  var c=body.dataset.theme==='light'?'79,70,229':'139,120,255',i,j,p,q,dx,dy,d;
  for(i=0;i<P.length;i++){p=P[i];p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;
   dx=p.x-mx;dy=p.y-my;d=dx*dx+dy*dy;if(d<14000){var f=(1-d/14000)*.7,s=Math.sqrt(d)+1;p.x+=dx/s*f;p.y+=dy/s*f}
   cx.beginPath();cx.arc(p.x,p.y,p.r,0,6.283);cx.fillStyle='rgba('+c+',.55)';cx.fill();
   for(j=i+1;j<P.length;j++){q=P[j];dx=p.x-q.x;dy=p.y-q.y;d=dx*dx+dy*dy;if(d<17000){cx.strokeStyle='rgba('+c+','+(0.2*(1-d/17000)).toFixed(3)+')';cx.lineWidth=1;cx.beginPath();cx.moveTo(p.x,p.y);cx.lineTo(q.x,q.y);cx.stroke()}}}
  requestAnimationFrame(tick)};
 tick()}
/* ماوس: نور کارت + پارالاکس orbها */
var pm=null,pq=false;doc.addEventListener('pointermove',function(e){if(e.pointerType==='touch')return;pm=e;if(pq)return;pq=true;requestAnimationFrame(function(){pq=false;var t=pm.target.closest&&pm.target.closest('.card,.s,.app,.cfg,.m');if(!t)return;var r=t.getBoundingClientRect();t.style.setProperty('--mx',(pm.clientX-r.left)+'px');t.style.setProperty('--my',(pm.clientY-r.top)+'px')})},{passive:true});
/* شمارش عددی */
function count(el){if(RM||el.children.length)return;var t=el.textContent.trim(),m=t.match(/^([^\d]*)(\d+(?:\.\d+)?)(.*)$/);if(!m)return;
 var pre=m[1],num=parseFloat(m[2]),suf=m[3],dec=(m[2].split('.')[1]||'').length;if(!isFinite(num)||num===0)return;
 var t0=null,last=null,dur=1100;
 (function st(ts){if(t0===null)t0=ts;if(last!==null&&el.textContent!==last)return;var k=Math.min(1,(ts-t0)/dur),e=1-Math.pow(1-k,3);
  if(k<1){last=pre+(num*e).toFixed(dec)+suf;el.textContent=last;requestAnimationFrame(st)}else{el.textContent=t}})(performance.now())}
/* ظهور تدریجی */
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){reveal(e.target);io.unobserve(e.target)}})},{threshold:.06,rootMargin:'0px 0px -24px 0px'}):null;
function reveal(el){el.classList.add('in');setTimeout(function(){el.classList.remove('fx-rv','in');el.style.transitionDelay=''},1400)}
var seen=new WeakSet(),settled=false,sched=false;
function scan(){sched=false;var hero=!!doc.querySelector('.hero'),anim=hero&&!settled&&io&&!RM;
 root.classList.add('fx-on');
 qa('.gauge').forEach(function(g){if(!g.querySelector('.g-orbit'))g.insertAdjacentHTML('beforeend','<i class="g-orbit"></i>')});
 qa('.s,.app,.cfg,.st,.m,.link,.qrb,.card h3').forEach(function(el,i){if(seen.has(el))return;seen.add(el);
  if(anim){el.classList.add('fx-rv');el.style.transitionDelay=(Math.min(i%9,8)*55)+'ms';io.observe(el)}});
 if(anim)qa('.gauge b,.m b,.s b').forEach(count);
 if(hero&&!settled){settled=true;setTimeout(function(){root.classList.add('fx-settled')},1800)}}
function queue(){if(sched)return;sched=true;requestAnimationFrame(scan)}
new MutationObserver(function(ms){for(var i=0;i<ms.length;i++){var a=ms[i].addedNodes;for(var j=0;j<a.length;j++){if(a[j].nodeType===1){queue();return}}}}).observe(body,{childList:true,subtree:true});
queue();setTimeout(queue,400);setTimeout(queue,1400);
/* انفجار ذرات روی دکمه‌ها */
doc.addEventListener('click',function(e){if(RM)return;var b=e.target.closest&&e.target.closest('.cp,.crow button,.app button,.ib');if(!b)return;
 var cols=['#7c5cff','#22d3ee','#34d399','#fbbf24','#fb7185'];
 for(var i=0;i<8;i++){(function(i){var s=doc.createElement('i');s.className='fx-p';var a=Math.PI*2*i/8+Math.random()*.4,d=34+Math.random()*46;
  s.style.cssText='left:'+e.clientX+'px;top:'+e.clientY+'px;background:'+cols[i%5]+';--dx:'+(Math.cos(a)*d).toFixed(1)+'px;--dy:'+(Math.sin(a)*d).toFixed(1)+'px';
  body.appendChild(s);setTimeout(function(){s.remove()},800)})(i)}},true);
}catch(err){try{console.warn('fx',err)}catch(e){}}})();
'''

LITE_CSS = r'''
/* ===== v19.2 · سبک‌سازی برای جلوگیری از هنگ ===== */
:root{--card:rgba(15,21,44,.92);--card2:rgba(9,13,30,.9)}
body[data-theme=light]{--card:rgba(255,255,255,.95);--card2:rgba(244,247,255,.96)}
*,*:before,*:after{backdrop-filter:none!important;-webkit-backdrop-filter:none!important}
.fx-bg .o{filter:none!important;animation:none!important;translate:none!important;will-change:auto!important}
.fx-bg .gridl{animation:none!important}
.brand b,.who h1,.brand img,.av,.app.rec,.gauge:after,.badge i,.supc .si:after,.hero:before{animation:none!important}
.hero,.fx-settled .hero{animation:up .7s var(--ease) both!important}
.hero:after,.cp:after,.tg:after,.supc .tg:after,.bar i:after,.qrb .qr:after{animation:none!important;display:none!important}
.card h3:after{display:none}
@media(max-width:760px){.fx-bg .o2,.fx-bg .o3,.fx-bg .gridl{display:none}.fx-bg .o1{opacity:.35}.g-orbit{display:none}.card,.s,.app,.cfg,.m{background-image:none!important}}
'''


def _fx(tpl: str) -> str:
    assert tpl.count('</style></head>') == 1 and tpl.count('</script></body></html>') == 1
    return (tpl.replace('</style></head>', FX_CSS + LITE_CSS + '\n</style></head>')
               .replace('</script></body></html>', '</script><script>' + FX_JS + '</script></body></html>'))


PORTAL_V18 = _fx(PORTAL_V18)
PUBLIC_SUB_V18 = _fx(PUBLIC_SUB_V18)
