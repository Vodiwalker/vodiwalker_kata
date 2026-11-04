LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl" id="htmlRoot" translate="no">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="google" content="notranslate"><meta name="theme-color" content="#05030f"><title>VodiWalker | Login</title>
<link rel="stylesheet" href="/assets/ui.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{--bg:#05030f;--line:rgba(139,92,246,.26);--line2:rgba(167,139,250,.48);--accent:#8b5cf6;--accent2:#6366f1;--cyan:#22d3ee;--text:#f5f3ff;--sub:#a79dcb;--sub2:#7a709f;--ease:cubic-bezier(.22,.7,.2,1)}
html,body{background:var(--bg);color:var(--text);min-height:100%;-webkit-text-size-adjust:100%}
body{font-family:'Vazirmatn','Inter',sans-serif;min-height:100vh;min-height:100dvh;display:flex;justify-content:center;overflow-x:hidden;-webkit-font-smoothing:antialiased;position:relative;
background:radial-gradient(70% 38% at 50% 0%,rgba(99,60,220,.34),transparent 70%),radial-gradient(60% 30% at 50% 100%,rgba(124,58,237,.24),transparent 70%),var(--bg)}
html[data-lang=en] body{font-family:'Inter','Vazirmatn',sans-serif}
button{font-family:inherit;cursor:pointer}a{color:inherit;text-decoration:none}
:focus{outline:none}:focus-visible{outline:2px solid var(--cyan);outline-offset:2px}
::selection{background:rgba(139,92,246,.4);color:#fff}

/* ambient background */
.bg-fx{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.bg-fx:before{content:"";position:absolute;inset:0;opacity:.5;background-image:linear-gradient(rgba(139,92,246,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(139,92,246,.07) 1px,transparent 1px);background-size:44px 44px;-webkit-mask-image:radial-gradient(70% 60% at 50% 35%,#000,transparent 80%);mask-image:radial-gradient(70% 60% at 50% 35%,#000,transparent 80%)}
.bg-fx i{position:absolute;width:420px;height:420px;border-radius:50%;filter:blur(90px);opacity:.38;will-change:transform;animation:orb 18s ease-in-out infinite alternate}
.bg-fx i:nth-child(1){background:#6d3bff;top:-140px;right:-120px}
.bg-fx i:nth-child(2){background:#1fb6d4;bottom:-180px;left:-140px;opacity:.22;animation-duration:24s;animation-delay:-6s}
@keyframes orb{from{transform:translate3d(0,0,0) scale(1)}to{transform:translate3d(-40px,36px,0) scale(1.12)}}

.page{position:relative;z-index:1;width:100%;max-width:448px;margin:auto;padding:0 16px calc(28px + env(safe-area-inset-bottom,0px))}
.top{position:absolute;top:calc(14px + env(safe-area-inset-top,0px));left:16px;right:16px;z-index:5;display:flex;justify-content:space-between;align-items:center;direction:ltr}
.pill{display:flex;align-items:center;gap:8px;padding:8px 14px;border-radius:16px;background:rgba(15,10,40,.66);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);border:1px solid var(--line);font-size:11px;font-weight:600;line-height:1.25;color:var(--text)}
.pill i{font-size:22px;color:#a78bfa}
.lang{position:relative}
.lang>button{display:flex;align-items:center;gap:7px;padding:9px 13px;border-radius:16px;background:rgba(15,10,40,.66);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);border:1px solid var(--line);color:var(--text);font-size:12px;font-weight:700;transition:border-color .2s,background-color .2s}
.lang>button:hover{border-color:var(--line2);background:rgba(30,20,70,.7)}
.lang>button i{color:#a78bfa}
.lang-menu{position:absolute;top:calc(100% + 6px);right:0;min-width:120px;background:#0f0a28;border:1px solid var(--line2);border-radius:14px;overflow:hidden;z-index:9;box-shadow:0 20px 40px -12px rgba(0,0,0,.7);opacity:0;visibility:hidden;transform:translateY(-6px) scale(.98);transform-origin:top right;transition:opacity .18s var(--ease),transform .18s var(--ease),visibility 0s linear .18s}
.lang-menu.show{opacity:1;visibility:visible;transform:none;transition:opacity .18s var(--ease),transform .18s var(--ease),visibility 0s}
.lang-menu button{display:block;width:100%;padding:11px 14px;background:none;border:0;color:var(--sub);font-size:12.5px;font-weight:700;text-align:start;transition:background-color .15s,color .15s}
.lang-menu button.on,.lang-menu button:hover{color:#fff;background:rgba(139,92,246,.22)}

.hero{position:relative;margin:0 -16px;height:min(56vw,240px);overflow:hidden;-webkit-mask-image:linear-gradient(#000 78%,transparent);mask-image:linear-gradient(#000 78%,transparent);animation:rise .8s var(--ease) both}
.hero img{width:100%;height:100%;object-fit:cover;object-position:50% 30%;display:block}
h1{margin-top:-8px;text-align:center;font-size:31px;font-weight:900;line-height:1.5;letter-spacing:-.01em;animation:rise .7s .08s var(--ease) both}
h1 .g{background:linear-gradient(90deg,#c084fc,#818cf8,#67e8f9,#c084fc);background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;font-family:'Inter',sans-serif;font-weight:900;animation:shine 7s linear infinite}
@keyframes shine{to{background-position:220% 0}}
.subtitle{margin-top:4px;text-align:center;font-size:13px;color:var(--sub);line-height:1.9;animation:rise .7s .14s var(--ease) both}
.chips{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:16px;direction:ltr;animation:rise .7s .2s var(--ease) both}
.chip{display:flex;align-items:center;gap:6px;padding:9px 7px;border-radius:16px;border:1px solid;background:rgba(10,8,32,.62);min-width:0;overflow:hidden;transition:transform .2s var(--ease),background-color .2s}
.chip:hover{transform:translateY(-2px);background:rgba(20,14,50,.75)}
.chip>div{min-width:0}
.chip i{font-size:22px;flex:none}.chip b{display:block;font-size:9.5px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-family:'Inter',sans-serif}
.chip small{display:block;font-size:9.5px;opacity:.85;font-family:'Inter',sans-serif}
.chip.c1{border-color:rgba(52,211,153,.38)}.chip.c1 i,.chip.c1 small{color:#34d399}
.chip.c2{border-color:rgba(34,211,238,.38)}.chip.c2 i,.chip.c2 small{color:#22d3ee}
.chip.c3{border-color:rgba(167,139,250,.48)}.chip.c3 i,.chip.c3 small{color:#a78bfa}

.card{position:relative;margin-top:20px;padding:22px 18px 18px;border-radius:26px;border:1px solid var(--line2);
background:linear-gradient(180deg,rgba(22,14,54,.88),rgba(7,5,24,.94));-webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);
box-shadow:0 0 0 1px rgba(99,102,241,.08),0 34px 80px -30px rgba(124,58,237,.6),inset 0 1px 0 rgba(255,255,255,.07);animation:rise .8s .26s var(--ease) both}
.card:before{content:"";position:absolute;top:0;left:22px;right:22px;height:2px;border-radius:0 0 4px 4px;background:linear-gradient(90deg,transparent,#8b5cf6,#22d3ee,transparent);opacity:.8}
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.card-head{display:flex;align-items:center;gap:14px;margin-bottom:18px}
.shield{width:58px;height:58px;flex:none;border-radius:18px;display:grid;place-items:center;border:1px solid var(--line2);background:linear-gradient(145deg,rgba(139,92,246,.32),rgba(30,20,70,.6));color:#c4b5fd;font-size:30px;box-shadow:0 10px 28px -12px rgba(139,92,246,.7)}
.card-head small{display:block;font-size:12px;color:#9a8bea}.card-head b{display:block;margin-top:3px;font-size:18px;font-weight:800}

.inp{position:relative;margin-bottom:12px}
.inp input{width:100%;height:54px;padding:0 50px;border-radius:16px;border:1px solid var(--line);background:rgba(4,3,18,.82);color:var(--text);font-size:16px;font-family:inherit;outline:none;transition:border-color .18s,box-shadow .2s var(--ease),background-color .18s}
.inp input::placeholder{color:var(--sub2);font-size:14px}
.inp input:hover{border-color:var(--line2)}
.inp input:focus{border-color:var(--accent);box-shadow:0 0 0 4px rgba(139,92,246,.22);background:rgba(8,5,28,.95)}
.inp:focus-within .lead{color:#c4b5fd}
.inp .lead{position:absolute;right:16px;top:50%;transform:translateY(-50%);font-size:22px;color:#a78bfa;pointer-events:none;transition:color .18s}
.eye{position:absolute;left:10px;top:50%;transform:translateY(-50%);background:none;border:0;color:#a78bfa;font-size:22px;width:38px;height:38px;display:grid;place-items:center;border-radius:10px;transition:background-color .15s,color .15s}
.eye:hover{background:rgba(139,92,246,.16);color:#ddd6fe}
html[dir=ltr] .inp .lead{right:auto;left:16px}html[dir=ltr] .eye{left:auto;right:10px}
/* autofill: Chrome/Safari paint a light box with dark text by default */
.inp input:-webkit-autofill,.inp input:-webkit-autofill:hover,.inp input:-webkit-autofill:focus{-webkit-text-fill-color:var(--text);caret-color:var(--text);-webkit-box-shadow:0 0 0 1000px #0b0724 inset;transition:background-color 9999s ease-out 0s}
#capsWarn{display:none;align-items:center;gap:5px;margin:-4px 2px 10px;font-size:11.5px;color:#fbbf24}
.remember{display:flex;align-items:center;gap:10px;margin:6px 2px 16px;font-size:13px;color:var(--sub);cursor:pointer;user-select:none;min-height:28px}
.remember input{appearance:none;-webkit-appearance:none;width:22px;height:22px;border-radius:7px;background:rgba(4,3,18,.8);border:1px solid var(--line2);display:grid;place-items:center;flex:none;cursor:pointer;transition:background-color .15s,border-color .15s,box-shadow .15s}
.remember input:hover{border-color:var(--accent)}
.remember input:focus-visible{box-shadow:0 0 0 3px rgba(34,211,238,.35)}
.remember input:checked{background:linear-gradient(135deg,var(--accent),var(--accent2));border-color:transparent}
.remember input:checked:after{content:"";width:6px;height:11px;border:solid #fff;border-width:0 2.5px 2.5px 0;transform:rotate(45deg) translate(-1px,-1px)}

.btn-main{position:relative;overflow:hidden;width:100%;height:56px;border:1px solid rgba(147,197,253,.45);border-radius:16px;color:#fff;font-size:16px;font-weight:800;display:flex;align-items:center;justify-content:center;gap:10px;
background:linear-gradient(100deg,#4f46e5,#7c3aed 55%,#3b82f6);box-shadow:0 14px 34px -12px rgba(99,102,241,.85),inset 0 1px 0 rgba(255,255,255,.3);transition:filter .18s,transform .18s var(--ease),box-shadow .2s}
.btn-main:before{content:"";position:absolute;top:0;bottom:0;width:60%;left:-80%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.28),transparent);transform:skewX(-18deg);transition:left .6s var(--ease)}
.btn-main:hover:before{left:130%}
.btn-main:hover{filter:brightness(1.08);transform:translateY(-1px);box-shadow:0 18px 38px -12px rgba(99,102,241,.95),inset 0 1px 0 rgba(255,255,255,.3)}
.btn-main:active{transform:scale(.985)}.btn-main:disabled{opacity:.7;cursor:wait}
.btn-main i{font-size:22px;transition:transform .2s var(--ease)}
.btn-main:hover i{transform:translateX(3px)}html[dir=rtl] .btn-main:hover i{transform:translateX(-3px)}
.btn-main.loading{pointer-events:none;opacity:.88}.btn-main.loading>*{visibility:hidden}.btn-main.loading:after{content:"";position:absolute;width:22px;height:22px;border-radius:50%;border:3px solid rgba(255,255,255,.35);border-top-color:#fff;animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}.spin{animation:spin .7s linear infinite}

.error{display:flex;gap:8px;align-items:flex-start;margin:0 0 14px;padding:11px 13px;border-radius:14px;font-size:12.5px;line-height:1.8;background:rgba(239,68,68,.10);border:1px solid rgba(239,68,68,.34);color:#fca5a5;animation:shake .45s var(--ease)}
.error:before{content:"\ea05";font-family:tabler-icons;font-size:17px;flex:none;line-height:1.6}
@keyframes shake{10%,90%{transform:translateX(-1px)}20%,80%{transform:translateX(2px)}30%,50%,70%{transform:translateX(-4px)}40%,60%{transform:translateX(4px)}}

.feat{display:grid;grid-template-columns:repeat(3,1fr);margin-top:16px;padding:13px 6px;border-radius:16px;border:1px solid var(--line);background:rgba(10,8,32,.55);direction:ltr}
.feat div{display:flex;align-items:center;justify-content:center;gap:6px;font-size:10px;color:var(--sub);font-family:'Inter',sans-serif;padding:0 4px;border-inline-start:1px solid var(--line);text-align:start}
.feat div:first-child{border:0}.feat i{font-size:22px;color:#a78bfa;flex:none}
.notice{position:relative;margin-top:14px;padding:14px;border-radius:18px;border:1px solid var(--line);overflow:hidden;background:radial-gradient(120px 90px at 12% 90%,rgba(99,102,241,.32),transparent 70%),rgba(10,8,32,.66)}
.notice p{position:relative;font-size:12px;line-height:2.1;color:#93c5fd}.notice p b{display:block;color:#e9e5ff;font-weight:800;font-size:13px;margin-bottom:2px}
.tg{position:relative;display:inline-flex;align-items:center;gap:8px;margin-top:8px;padding:8px 18px;border-radius:99px;border:1px solid rgba(34,211,238,.5);background:rgba(34,211,238,.09);color:#67e8f9;font-size:12px;font-weight:800;transition:filter .18s,transform .18s var(--ease),background-color .18s}
.tg:hover{filter:brightness(1.2);background:rgba(34,211,238,.16);transform:translateY(-1px)}.tg:active{transform:scale(.97)}
.reg{width:100%;margin-top:14px;padding:15px 16px;border-radius:16px;border:1px solid var(--line);background:rgba(10,8,32,.55);color:var(--sub);font-size:13px;font-weight:700;display:flex;align-items:center;gap:12px;transition:border-color .18s,color .18s,background-color .18s,transform .18s var(--ease)}
.reg:hover{border-color:var(--line2);color:var(--text);background:rgba(20,14,50,.7)}.reg:active{transform:scale(.99)}
.reg i.a{font-size:24px;color:#a78bfa}.reg i.ch{margin-inline-start:auto;font-size:18px;transition:transform .2s var(--ease)}
html[dir=rtl] .reg i.ch{transform:scaleX(-1)}
.foot{margin-top:22px;text-align:center;font-size:10px;color:var(--sub2);font-family:'Inter',sans-serif}
.foot b{display:block;font-size:13px;letter-spacing:.42em;color:var(--sub);font-weight:600;margin-bottom:5px}

/* registration dialog: real fade + scale instead of display toggle */
.ov{position:fixed;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;background:rgba(3,2,10,.78);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);padding:18px;opacity:0;visibility:hidden;transition:opacity .22s var(--ease),visibility 0s linear .22s}
.ov.show{opacity:1;visibility:visible;transition:opacity .22s var(--ease),visibility 0s}
.box{width:100%;max-width:420px;max-height:90vh;max-height:90dvh;overflow:auto;padding:22px;border-radius:24px;background:linear-gradient(180deg,#120c2e,#0b0722);border:1px solid var(--line2);box-shadow:0 40px 90px -30px rgba(0,0,0,.85);transform:translateY(14px) scale(.97);transition:transform .28s var(--ease)}
.ov.show .box{transform:none}
.bh{display:flex;justify-content:space-between;gap:10px;margin-bottom:14px}
.bh h3{font-size:17px;font-weight:900;margin:8px 0 6px}.bh p{font-size:11.5px;color:var(--sub);line-height:1.9}
.badge{display:inline-flex;align-items:center;gap:6px;padding:5px 10px;border-radius:99px;font-size:10px;font-weight:800;color:#c4b5fd;background:rgba(139,92,246,.14);border:1px solid var(--line2)}
.x{width:36px;height:36px;flex:none;border-radius:11px;display:grid;place-items:center;background:rgba(255,255,255,.06);border:1px solid var(--line);color:var(--sub);transition:background-color .15s,color .15s,transform .15s}
.x:hover{background:rgba(255,255,255,.12);color:#fff}.x:active{transform:scale(.92)}
.msg{display:none;margin-bottom:12px;padding:10px 12px;border-radius:12px;font-size:12px;line-height:1.8}
.msg.ok{background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);color:#86efac}.msg.err{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.32);color:#fca5a5}
.hint{margin-top:12px;font-size:10.5px;color:var(--sub2);line-height:1.9;text-align:center}
.box .inp input{height:50px}

@media(min-width:700px){.page{max-width:460px}.hero{height:250px}}
@media(max-height:720px){.hero{height:min(40vw,170px)}h1{font-size:27px}}
@media(max-width:380px){h1{font-size:26px}.chip small{display:none}.feat div{font-size:9px}.card{padding:18px 14px 14px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition-duration:.001ms!important}}
</style>
</head>
<body>
<div class="bg-fx" aria-hidden="true"><i></i><i></i></div>
<div class="page">
  <div class="top">
    <div class="pill"><i class="ti ti-shield-check"></i><span>Secure<br>Connection</span></div>
    <div class="lang">
      <button type="button" id="langBtn" aria-haspopup="true" aria-expanded="false"><i class="ti ti-world"></i><span id="langCur">FA</span><i class="ti ti-chevron-down" style="font-size:14px"></i></button>
      <div class="lang-menu" id="langMenu"><button type="button" id="langFa" onclick="setLang('fa')">فارسی</button><button type="button" id="langEn" onclick="setLang('en')">English</button></div>
    </div>
  </div>
  <div class="hero"><img src="data:image/jpeg;base64,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" alt="VodiWalker" width="841" height="453" fetchpriority="high"></div>
  <h1 data-i18n="h1">ورود به <span class="g">VodiWalker</span></h1>
  <p class="subtitle" data-i18n="subtitle">مرکز کنترل امن VodiWalker برای مدیریت سرویس‌ها و شبکه</p>
  <div class="chips">
    <div class="chip c1"><i class="ti ti-activity"></i><div><b>System Monitor</b><small>Real-time</small></div></div>
    <div class="chip c2"><i class="ti ti-cookie"></i><div><b>Secure Cookie</b><small>Encrypted</small></div></div>
    <div class="chip c3"><i class="ti ti-shield-check"></i><div><b>Protected Session</b><small>Your Privacy</small></div></div>
  </div>
  <div class="card">
    <div class="card-head"><div class="shield"><i class="ti ti-shield-check"></i></div><div><small data-i18n="cardSmall">حساب کاربری مدیر</small><b data-i18n="cardTitle">ورود به مرکز کنترل</b></div></div>
    <form method="post" action="/login" id="loginForm" autocomplete="on">
      <div class="inp"><input type="text" name="username" id="username" placeholder="نام کاربری" data-i18n-placeholder="userPh" aria-label="username" required autocomplete="username" autocapitalize="none" autocorrect="off" spellcheck="false" maxlength="64"><i class="ti ti-user lead"></i></div>
      <div class="inp"><input type="password" name="password" id="password" placeholder="رمز عبور" data-i18n-placeholder="passPh" aria-label="password" autocomplete="current-password" autocapitalize="none" autocorrect="off" spellcheck="false" maxlength="256" required><i class="ti ti-lock lead"></i><button type="button" class="eye" id="pwToggle" aria-label="toggle password"><i class="ti ti-eye-off"></i></button></div>
      <div id="capsWarn"><i class="ti ti-alert-triangle"></i> Caps Lock</div>
      <!--LOGIN_ERROR-->
      <label class="remember"><input type="checkbox" name="remember" value="1" checked><span data-i18n="remember">مرا به خاطر بسپار</span></label>
      <button class="btn-main" type="submit" id="submitBtn"><span data-i18n="submit">ورود به پنل</span><i class="ti ti-login-2"></i></button>
    </form>
    <div class="feat"><div><i class="ti ti-stack-2"></i>Multi-Layer Security</div><div><i class="ti ti-lock"></i>Encrypted Traffic</div><div><i class="ti ti-headset"></i>24/7 Support</div></div>
    <div class="notice"><p><b data-i18n="freeNotice1">این پنل کاملاً رایگان است 💜</b><span data-i18n="freeNotice2">ساخته شده تا همه بتوانند بدون هزینه از یک اینترنت بهتر استفاده کنند؛ فروختنش دور از انسانیت است. اگر این پنل به کارت آمده، با عضویت در کانال رسمی ما هم از تمام بروزرسانی‌ها و خبرهای مهم باخبر می‌مانی و هم به رایگان ماندنش کمک می‌کنی.</span></p><a class="tg" href="https://t.me/vodiwalkervpn03" target="_blank" rel="noopener"><span data-i18n="freeNoticeBtn">عضویت در کانال تلگرام</span><i class="ti ti-brand-telegram"></i></a></div>
    <button type="button" class="reg" onclick="openReg()"><i class="ti ti-user-plus a"></i><span data-i18n="regBtn">ثبت‌نام ادمینی</span><i class="ti ti-chevron-right ch"></i></button>
  </div>
  <div class="foot"><b>VODIWALKER</b>CONNECT TO A BETTER INTERNET</div>
</div>

<div class="ov" id="ov"><div class="box" role="dialog" aria-modal="true">
  <div class="bh"><div><span class="badge"><i class="ti ti-user-shield"></i><span data-i18n="regBadge">درخواست همکاری</span></span><h3 data-i18n="regTitle">ثبت‌نام ادمینی VodiWalker</h3><p data-i18n="regDesc">اطلاعاتت رو بفرست؛ مالک پنل درخواستت رو بررسی می‌کنه و در صورت تایید، نام کاربری و رمز از طریق تلگرام برات ارسال می‌شه.</p></div><button type="button" class="x" onclick="closeReg()" aria-label="close"><i class="ti ti-x"></i></button></div>
  <div class="inp"><input type="text" id="aregName" placeholder="نام و نام خانوادگی" data-i18n-placeholder="regNamePh" maxlength="80"><i class="ti ti-id lead"></i></div>
  <div class="inp"><input type="text" id="aregTg" dir="ltr" placeholder="@username" data-i18n-placeholder="regTgPh" maxlength="64"><i class="ti ti-brand-telegram lead"></i></div>
  <div class="inp"><input type="text" id="aregNote" placeholder="توضیح (اختیاری)" data-i18n-placeholder="regNotePh" maxlength="300"><i class="ti ti-message lead"></i></div>
  <div id="aregMsg" class="msg"></div>
  <button class="btn-main" type="button" id="aregBtn" onclick="submitReg()" style="height:50px;font-size:14px"><span data-i18n="regSubmit">ارسال درخواست</span><i class="ti ti-send"></i></button>
  <p class="hint" data-i18n="regHint">پس از تایید مالک، اطلاعات ورود از طریق آیدی تلگرام برایت ارسال خواهد شد.</p>
</div></div>

<script>
var I18N={
fa:{title:"ورود | VodiWalker",h1:'ورود به <span class="g">VodiWalker</span>',subtitle:"مرکز کنترل امن VodiWalker برای مدیریت سرویس‌ها و شبکه",cardSmall:"حساب کاربری مدیر",cardTitle:"ورود به مرکز کنترل",userPh:"نام کاربری",passPh:"رمز عبور",remember:"مرا به خاطر بسپار",submit:"ورود به پنل",
freeNotice1:"این پنل کاملاً رایگان است 💜",freeNotice2:"ساخته شده تا همه بتوانند بدون هزینه از یک اینترنت بهتر استفاده کنند؛ فروختنش دور از انسانیت است. اگر این پنل به کارت آمده، با عضویت در کانال رسمی ما هم از تمام بروزرسانی‌ها و خبرهای مهم باخبر می‌مانی و هم به رایگان ماندنش کمک می‌کنی.",freeNoticeBtn:"عضویت در کانال تلگرام",regBtn:"ثبت‌نام ادمینی",
regBadge:"درخواست همکاری",regTitle:"ثبت‌نام ادمینی VodiWalker",regDesc:"اطلاعاتت رو بفرست؛ مالک پنل درخواستت رو بررسی می‌کنه و در صورت تایید، نام کاربری و رمز از طریق تلگرام برات ارسال می‌شه.",regNamePh:"نام و نام خانوادگی",regTgPh:"@username",regNotePh:"توضیح (اختیاری)",regSubmit:"ارسال درخواست",regHint:"پس از تایید مالک، اطلاعات ورود از طریق آیدی تلگرام برایت ارسال خواهد شد.",regSent:"درخواست شما ثبت شد ✓ منتظر تایید مالک پنل بمانید.",regNameErr:"نام و نام خانوادگی را کامل وارد کنید",regTgErr:"آیدی تلگرام معتبر وارد کنید",err:"خطا"},
en:{title:"Login | VodiWalker",h1:'Sign in to <span class="g">VodiWalker</span>',subtitle:"Secure VodiWalker control center for services and network",cardSmall:"Admin account",cardTitle:"Sign in to Control Center",userPh:"Username",passPh:"Password",remember:"Remember me",submit:"Sign in",
freeNotice1:"This panel is completely free 💜",freeNotice2:"It was built so everyone can enjoy a better internet at no cost — selling it would be inhumane. If it helps you, join our official channel to stay up to date with every update and important news.",freeNoticeBtn:"Join our Telegram channel",regBtn:"Register as admin",
regBadge:"Collaboration request",regTitle:"VodiWalker admin registration",regDesc:"Send your details. The owner will review your request and, if approved, send your username and password via Telegram.",regNamePh:"Full name",regTgPh:"@username",regNotePh:"Note (optional)",regSubmit:"Send request",regHint:"Once approved, your login details will be sent to your Telegram ID.",regSent:"Request submitted ✓ wait for the owner's approval.",regNameErr:"Please enter your full name",regTgErr:"Please enter a valid Telegram ID",err:"Error"}};
function $(i){return document.getElementById(i)}
function curLang(){try{var l=localStorage.getItem('vw_lang');return I18N[l]?l:'fa'}catch(e){return 'fa'}}
function applyLang(l){
  var d=I18N[l],h=$('htmlRoot');
  document.querySelectorAll('[data-i18n]').forEach(function(el){var k=el.getAttribute('data-i18n');if(d[k]!==undefined)el.innerHTML=d[k]});
  document.querySelectorAll('[data-i18n-placeholder]').forEach(function(el){var k=el.getAttribute('data-i18n-placeholder');if(d[k]!==undefined)el.placeholder=d[k]});
  document.title=d.title;h.lang=l;h.dir=l==='fa'?'rtl':'ltr';h.setAttribute('data-lang',l);
  $('langCur').textContent=l.toUpperCase();$('langFa').classList.toggle('on',l==='fa');$('langEn').classList.toggle('on',l==='en');
}
function setLang(l){try{localStorage.setItem('vw_lang',l)}catch(e){}applyLang(l);$('langMenu').classList.remove('show')}
if(curLang()!=='fa')applyLang(curLang());else{$('langFa').classList.add('on')}
$('langBtn').addEventListener('click',function(e){e.stopPropagation();$('langMenu').classList.toggle('show')});
document.addEventListener('click',function(){$('langMenu').classList.remove('show')});
$('pwToggle').addEventListener('click',function(){
  var p=$('password'),i=this.querySelector('i'),show=p.type==='password';
  p.type=show?'text':'password';i.className='ti '+(show?'ti-eye':'ti-eye-off');
});
(function(){var p=$('password'),w=$('capsWarn');function c(e){w.style.display=(e.getModifierState&&e.getModifierState('CapsLock'))?'flex':'none'}p.addEventListener('keydown',c);p.addEventListener('keyup',c)})();
$('loginForm').addEventListener('submit',function(){var b=$('submitBtn');setTimeout(function(){b.classList.add('loading')},0)});
window.addEventListener('pageshow',function(){$('submitBtn').classList.remove('loading')});
function openReg(){$('aregMsg').style.display='none';$('ov').classList.add('show')}
function closeReg(){$('ov').classList.remove('show')}
$('ov').addEventListener('click',function(e){if(e.target===this)closeReg()});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeReg()});
function regMsg(t,ok){var e=$('aregMsg');e.textContent=t;e.className='msg '+(ok?'ok':'err');e.style.display='block'}
async function submitReg(){
  var d=I18N[curLang()],n=$('aregName').value.trim(),tg=$('aregTg').value.trim().replace(/^@/,''),note=$('aregNote').value.trim();
  if(n.length<3){regMsg(d.regNameErr,false);return}
  if(!/^[A-Za-z0-9_]{3,64}$/.test(tg)){regMsg(d.regTgErr,false);return}
  var b=$('aregBtn');b.disabled=true;b.classList.add('loading');
  try{
    var r=await fetch('/api/admin-requests',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({full_name:n,telegram_id:tg,note:note})});
    var j={};try{j=await r.json()}catch(e){}
    if(!r.ok)throw new Error((typeof j.detail==='string'&&j.detail)||d.err);
    regMsg(d.regSent,true);$('aregName').value='';$('aregTg').value='';$('aregNote').value='';
  }catch(e){regMsg(e.message||d.err,false)}
  finally{b.disabled=false;b.classList.remove('loading')}
}

/* ===== UX polish ===== */
(function(){
  var u=$('username'),p=$('password');
  function syncAria(){var d=I18N[curLang()];u.setAttribute('aria-label',d.userPh);p.setAttribute('aria-label',d.passPh)}
  var _al=applyLang;applyLang=function(l){_al(l);syncAria()};syncAria();
  // language menu aria state
  var lb=$('langBtn'),lm=$('langMenu');
  new MutationObserver(function(){lb.setAttribute('aria-expanded',lm.classList.contains('show')?'true':'false')}).observe(lm,{attributes:true,attributeFilter:['class']});
  // after a failed login the server re-renders this page with .error: focus the password and select it
  var hasErr=!!document.querySelector('.error');
  if(hasErr){p.value='';setTimeout(function(){p.focus()},60)}
  else if(window.matchMedia&&matchMedia('(hover:hover) and (pointer:fine)').matches&&!u.value){setTimeout(function(){u.focus()},60)}
  // registration dialog: focus first field, Enter submits, focus returns to the button
  var _or=openReg,_cr=closeReg,opener=null;
  openReg=function(){opener=document.activeElement;_or();setTimeout(function(){$('aregName').focus()},120)};
  closeReg=function(){_cr();if(opener&&opener.focus)opener.focus()};
  ['aregName','aregTg','aregNote'].forEach(function(id){$(id).addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();submitReg()}})});
  // tiny shake on the password field when the browser blocks an empty submit
  $('loginForm').addEventListener('invalid',function(e){e.target.style.borderColor='#ef4444';setTimeout(function(){e.target.style.borderColor=''},1200)},true);
})();
</script>
</body>
</html>
"""


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VodiWalker Control Center</title>
<link rel="stylesheet" href="/assets/ui.css">
<script src="/assets/qr.js"></script>
<style>
:root{--accent-rgb:139,92,246;--accent-soft:#c4b5fd}
/* ===== VW inbound + dashboard polish ===== */
.ib-quickstats{display:grid!important;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.ib-quickstats .ibx-hl{border-color:rgba(34,211,238,.38)!important;background:linear-gradient(155deg,rgba(34,211,238,.10),rgba(var(--accent-rgb),.07))!important}
.ib-quickstats b{unicode-bidi:isolate;white-space:nowrap}
.ibx-filterbar{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin:0 0 12px}
.ibx-chips{display:flex;gap:6px;overflow-x:auto;padding-bottom:2px;scrollbar-width:none;max-width:100%}.ibx-chips::-webkit-scrollbar{display:none}
.ibx-chip{flex:none;display:inline-flex;align-items:center;gap:6px;padding:7px 13px;border-radius:999px;border:1px solid var(--line);background:var(--panel2);color:var(--sub2);font:700 11.5px inherit;font-family:inherit;cursor:pointer;transition:background-color .15s,border-color .15s,color .15s,box-shadow .15s,opacity .15s,transform .15s}
.ibx-chip em{font-style:normal;font-size:10px;padding:1px 7px;border-radius:99px;background:rgba(148,130,255,.14);color:var(--text)}
.ibx-chip:hover{border-color:var(--line2);color:var(--text)}
.ibx-chip.on{color:#fff;border-color:transparent;background:linear-gradient(120deg,#6366f1,#8b5cf6)}.ibx-chip.on em{background:rgba(255,255,255,.22);color:#fff}
#ibGrid.ib-grid{grid-template-columns:repeat(auto-fill,minmax(340px,1fr))!important;gap:14px}
@media(max-width:420px){#ibGrid.ib-grid{grid-template-columns:1fr!important}}
.ibx{gap:12px!important;transition:transform .18s,border-color .18s,box-shadow .18s}
.ibx:hover{transform:translateY(-2px)}
.ibx-head{display:flex;align-items:center;gap:11px}
.ibx-av{position:relative;width:42px;height:42px;flex:none;border-radius:14px;display:grid;place-items:center;font-size:21px;color:var(--accent-soft);background:linear-gradient(145deg,rgba(var(--accent-rgb),.28),rgba(99,102,241,.10));border:1px solid var(--line2)}
.ibx-av:after{content:"";position:absolute;bottom:-3px;inset-inline-end:-3px;width:11px;height:11px;border-radius:50%;border:2px solid var(--panel,#0d1120);background:#6b7280}
.ibx-av.on:after{background:#34d399;box-shadow:0 0 10px #34d399}.ibx-av.idle:after{background:#60a5fa}.ibx-av.bad:after{background:#f43f5e}.ibx-av.off:after{background:#6b7280}
.ibx-id{flex:1;min-width:0}.ibx-id b{display:block;font-size:13.5px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;unicode-bidi:plaintext}
.ibx-sub{display:flex;align-items:center;gap:7px;margin-top:3px}.ibx-sub .mono{font-size:9.5px;color:var(--sub2)}
.ibx-pill{font-size:9.5px;font-weight:800;padding:2px 9px;border-radius:99px;border:1px solid}
.ibx-pill.on{color:#34d399;border-color:rgba(52,211,153,.4);background:rgba(52,211,153,.10)}.ibx-pill.idle{color:#60a5fa;border-color:rgba(96,165,250,.4);background:rgba(96,165,250,.10)}
.ibx-pill.bad{color:#fb7185;border-color:rgba(251,113,133,.4);background:rgba(251,113,133,.10)}.ibx-pill.off{color:var(--sub2);border-color:var(--line);background:var(--panel2)}
.ibx-addr{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:7px 8px 7px 11px;border-radius:12px;background:var(--panel2);border:1px dashed var(--line2)}
.ibx-addr .mono{font-size:11px;direction:ltr;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ibx-traffic{display:flex;flex-direction:column;gap:6px}
.ibx-tt{display:flex;justify-content:space-between;gap:8px;font-size:11.5px}.ibx-tt span{color:var(--sub2)}.ibx-tt b{font-weight:800;unicode-bidi:isolate}
.ibx-tt.sm{font-size:10px}.ibx-tt.sm b{color:var(--text)}
.ibx-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.ibx-stats>div{padding:7px 4px;border-radius:11px;background:var(--panel2);border:1px solid var(--line);text-align:center;min-width:0}
.ibx-stats small{display:block;color:var(--sub2);font-size:8.5px;margin-bottom:2px;white-space:nowrap}.ibx-stats b{font-size:11.5px;font-weight:800;unicode-bidi:isolate}
.ibx-stats b.soon{color:var(--warn)}.ibx-stats b.expired{color:var(--bad)}
.ibx-foot{display:flex;align-items:center;gap:7px;flex-wrap:wrap;padding-top:10px;border-top:1px solid var(--line)}
.ibx-foot .ib-card-actions{margin-inline-start:auto;display:flex;gap:4px;flex-wrap:wrap}
.card,.stat-grid>*,.ib-card{transition:border-color .2s,box-shadow .2s}
.card:hover{border-color:var(--line2)}
.pg-head h1{letter-spacing:-.01em}
.pg-head .eyebrow{font-weight:800}

.name-studio{margin-top:8px;padding:10px;border-radius:14px;border:1px dashed var(--line2);background:rgba(var(--accent-rgb),.06)}
.ns-head{display:flex;align-items:center;justify-content:space-between;gap:8px;font-size:11px;color:var(--muted,#9aa3b5);margin-bottom:8px}
.ns-head i{color:var(--accent-soft)}.ns-more{border:1px solid var(--line);background:rgba(255,255,255,.04);color:inherit;border-radius:10px;padding:5px 10px;font-size:11px;cursor:pointer;font-family:inherit}
.ns-chips{display:flex;flex-wrap:wrap;gap:6px}.ns-chip{border:1px solid rgba(var(--accent-rgb),.35);background:rgba(var(--accent-rgb),.10);color:inherit;border-radius:999px;padding:6px 11px;font-size:12px;cursor:pointer;direction:ltr;font-family:inherit;transition:transform .12s,background .12s}
.ns-chip:hover{background:rgba(var(--accent-rgb),.25)}.ns-chip:active{transform:scale(.96)}

/* ===== VW overview polish: bidi-safe numbers, responsive stat grid ===== */
.ov-quickstats{display:grid!important;grid-template-columns:repeat(auto-fit,minmax(168px,1fr))!important;gap:10px!important;flex-direction:row!important}
.ov-quickstats>div{min-width:0}
.ov-quickstats>div:nth-child(3) i{background:rgba(34,211,238,.14);color:#22d3ee}
.ov-quickstats>div:nth-child(4) i{background:rgba(52,211,153,.14);color:#34d399}
.ov-quickstats>div:nth-child(5) i{background:rgba(53,214,255,.14);color:#35d6ff}
.ov-quickstats>div:nth-child(6) i{background:rgba(245,165,36,.14);color:#f5a524}
.ov-quickstats .qs-traffic{border-color:rgba(34,211,238,.35)!important;background:linear-gradient(155deg,rgba(34,211,238,.10),rgba(var(--accent-rgb),.06))!important}
.ov-quickstats b{unicode-bidi:isolate;white-space:nowrap}
@media(max-width:900px){.ov-quickstats{grid-template-columns:repeat(2,minmax(0,1fr))!important}.ib-quickstats.ov-quickstats{flex-direction:row!important}}
.rc-sub,.rc-head b,.health-row b,.traffic-foot b,.traffic-legend b,.otl-val,.connection-number,.conn-foot b,#ovBaseUrl{unicode-bidi:plaintext;white-space:nowrap}
.rc-sub{overflow:hidden;text-overflow:ellipsis}
.rc-head b{font-size:clamp(17px,4.6vw,26px)!important}
.health-row b{max-width:62%;overflow:hidden;text-overflow:ellipsis}

.perm-grid,.bot-text-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:12px}.perm-item{display:flex;align-items:center;gap:9px;padding:11px 12px;border:1px solid var(--line);background:var(--panel2);border-radius:13px;font-size:12px}.perm-item input{accent-color:var(--accent)}.bot-text-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.bot-text-grid textarea{width:100%;resize:vertical;min-height:90px;background:var(--panel2);border:1px solid var(--line);color:var(--text);border-radius:12px;padding:11px;font:inherit;line-height:1.8}@media(max-width:700px){.perm-grid,.bot-text-grid{grid-template-columns:1fr}}
.tpl-studio-head{display:flex;align-items:flex-start;justify-content:space-between;gap:14px;flex-wrap:wrap}
.tpl-badge{display:flex;align-items:center;gap:6px;padding:6px 11px;border-radius:99px;background:rgba(var(--accent-rgb),.12);color:#b79bff;border:1px solid rgba(var(--accent-rgb),.22);font-size:10.5px;font-weight:800;white-space:nowrap}
.tpl-grid{display:grid;grid-template-columns:1.2fr 1fr;gap:14px;margin-top:14px}
.tpl-fields{display:flex;flex-direction:column;gap:8px}
.tpl-row{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:11px 13px;border:1px solid var(--line);background:var(--panel2);border-radius:13px;cursor:pointer;transition:border-color .12s ease}
.tpl-row:hover{border-color:var(--line2)}
.tpl-row-main{display:flex;align-items:center;gap:10px;min-width:0}
.tpl-row-main i{width:32px;height:32px;flex-shrink:0;display:grid;place-items:center;border-radius:9px;background:rgba(var(--accent-rgb),.12);color:#a997ff;font-size:15px}
.tpl-row-main b{display:block;font-size:12px}
.tpl-row-main small{display:block;color:var(--sub2);font-size:9.5px;margin-top:2px}
input.tpl-switch{appearance:none;-webkit-appearance:none;width:36px;height:20px;border-radius:99px;background:var(--line2);border:1px solid var(--line);position:relative;cursor:pointer;flex-shrink:0;margin:0;transition:background-color .16s ease}
input.tpl-switch:after{content:'';position:absolute;width:14px;height:14px;top:2px;right:2px;border-radius:50%;background:#fff;transition:right .16s ease;box-shadow:0 1px 3px rgba(0,0,0,.3)}
input.tpl-switch:checked{background:linear-gradient(90deg,var(--accent),var(--accent-d));border-color:transparent}
input.tpl-switch:checked:after{right:18px}
.tpl-preview{padding:14px;border:1px dashed var(--line2);border-radius:14px;background:linear-gradient(155deg,rgba(var(--accent-rgb),.06),rgba(255,255,255,.015))}
.tpl-preview-label{display:flex;align-items:center;gap:7px;font-size:10.5px;color:var(--sub);font-weight:700;margin-bottom:10px}
.tpl-preview-row{display:flex;align-items:center;gap:9px;padding:11px 12px;border-radius:12px;background:var(--panel);border:1px solid var(--line)}
.tpl-preview-dot{width:9px;height:9px;border-radius:50%;background:var(--good);box-shadow:0 0 0 3px rgba(34,197,139,.18);flex-shrink:0}
.tpl-preview-text{flex:1;min-width:0;font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;direction:ltr;text-align:left}
.tpl-preview-proto{font-size:9px;font-weight:800;color:var(--accent);background:rgba(var(--accent-rgb),.12);padding:3px 8px;border-radius:99px;flex-shrink:0}
@media(max-width:760px){.tpl-grid{grid-template-columns:1fr}}
.admin-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.admin-card{position:relative;overflow:hidden;padding:18px;border:1px solid var(--line);background:linear-gradient(155deg,var(--panel) 0%,var(--panel2) 100%);border-radius:18px;box-shadow:var(--shadow-sm);transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease}
.admin-card:hover{transform:translateY(-2px);box-shadow:var(--shadow-md);border-color:var(--line2)}
.admin-card.is-owner{border-color:rgba(245,165,36,.35);background:linear-gradient(155deg,rgba(245,165,36,.08) 0%,var(--panel2) 60%)}
.admin-card.is-inactive{opacity:.62}
.admin-card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}
.admin-id{display:flex;align-items:center;gap:11px;min-width:0}
.admin-avatar{flex:none;width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;color:#fff;background:linear-gradient(135deg,var(--accent),var(--accent-d));box-shadow:0 6px 16px rgba(var(--accent-rgb),.28)}
.admin-card.is-owner .admin-avatar{background:linear-gradient(135deg,#f5a524,#c9820a);box-shadow:0 6px 16px rgba(245,165,36,.3)}
.admin-meta{min-width:0}
.admin-meta .admin-name{font-size:14px;font-weight:800;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.admin-meta .admin-sub{display:flex;align-items:center;gap:6px;margin-top:3px;font-size:11px;color:var(--sub)}
.admin-role-badge{flex:none;display:inline-flex;align-items:center;gap:4px;padding:3px 9px;border-radius:999px;font-size:10px;font-weight:700;letter-spacing:.02em}
.admin-role-badge.owner{color:#f5a524;background:rgba(245,165,36,.14);border:1px solid rgba(245,165,36,.3)}
.admin-role-badge.admin{color:var(--accent);background:rgba(var(--accent-rgb),.12);border:1px solid rgba(var(--accent-rgb),.28)}
.admin-status-dot{width:7px;height:7px;border-radius:50%;background:var(--good);box-shadow:0 0 0 3px rgba(34,197,139,.15)}
.admin-card.is-inactive .admin-status-dot{background:var(--bad);box-shadow:0 0 0 3px rgba(242,73,85,.15)}
.admin-perm-row{display:flex;flex-wrap:wrap;gap:5px;margin-top:14px}
.admin-perm-chip{font-size:10px;padding:3px 8px;border-radius:8px;background:var(--panel2);border:1px solid var(--line);color:var(--sub)}
.admin-perm-chip.all{color:#f5a524;border-color:rgba(245,165,36,.3);background:rgba(245,165,36,.1)}
.admin-card-foot{display:flex;align-items:center;justify-content:space-between;margin-top:16px;padding-top:12px;border-top:1px dashed var(--line)}
.admin-card-foot .admin-login{font-size:10.5px;color:var(--sub2)}
.admin-card-foot .row-actions{gap:6px}
.admins-hero{display:grid;grid-template-columns:1fr auto;gap:16px;align-items:center;margin-bottom:14px;padding:20px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(135deg,rgba(var(--accent-rgb),.11),rgba(57,214,255,.035));box-shadow:var(--shadow-sm)}.admins-hero h2{font-size:18px;margin:0 0 5px}.admins-hero p{font-size:10px;color:var(--sub);margin:0;line-height:1.9}.admins-summary{display:flex;gap:8px;flex-wrap:wrap}.admins-summary .sum{min-width:92px;padding:11px 13px;border:1px solid var(--line);border-radius:13px;background:rgba(255,255,255,.025);text-align:center}.admins-summary b{display:block;font-size:18px}.admins-summary small{display:block;color:var(--sub2);font-size:8px;margin-top:3px}.admin-card{min-height:188px;display:flex;flex-direction:column}.admin-card-top{padding-bottom:13px;border-bottom:1px dashed var(--line)}.admin-id{flex:1}.admin-avatar{position:relative;overflow:hidden}.admin-avatar:after{content:"";position:absolute;inset:0;background:linear-gradient(120deg,transparent 35%,rgba(255,255,255,.18) 50%,transparent 65%);transform:translateX(-130%);transition:transform .55s ease}.admin-card:hover .admin-avatar:after{transform:translateX(130%)}.admin-perm-row{min-height:45px;align-content:flex-start}.admin-perm-chip{transition:.15s ease}.admin-perm-chip:hover{border-color:var(--line2);color:var(--text)}.admin-card-foot{margin-top:auto}.admin-login{direction:ltr;text-align:left}.admin-actions-label{display:none}.admin-card-foot .row-actions{gap:8px}.admin-card-foot .iconbtn{width:38px;height:34px;border-radius:11px;font-size:15px;background:linear-gradient(145deg,var(--panel2),rgba(var(--accent-rgb),.08));border-color:var(--line2);box-shadow:0 7px 18px rgba(0,0,0,.10)}.admin-card-foot .iconbtn.danger{color:var(--bad)}.admin-card-foot .iconbtn.power{color:var(--accent)}.admin-card-foot .iconbtn:hover{transform:translateY(-1px);box-shadow:0 10px 24px rgba(var(--accent-rgb),.18)}.access-command-copy{min-width:0}.command-badge{display:inline-flex;align-items:center;gap:7px;padding:6px 10px;border-radius:999px;border:1px solid rgba(var(--accent-rgb),.28);background:rgba(var(--accent-rgb),.10);color:var(--accent);font-size:9px;font-weight:900;letter-spacing:.08em}.access-command-copy h2{font-size:22px;margin:12px 0 7px;letter-spacing:-.02em}.access-command-copy p{max-width:760px}.command-points{display:flex;flex-wrap:wrap;gap:7px;margin-top:13px}.command-points span{display:inline-flex;align-items:center;gap:5px;padding:6px 9px;border:1px solid var(--line);border-radius:9px;background:rgba(255,255,255,.025);font-size:9px;color:var(--sub)}.command-points i{color:var(--good)}.admin-directory{overflow:hidden}.directory-live{display:inline-flex;align-items:center;gap:6px;font-size:9px;color:var(--good);font-weight:800}.directory-live i{width:6px;height:6px;border-radius:50%;background:var(--good);box-shadow:0 0 0 4px rgba(34,197,139,.12)}.admin-directory .panel-head{border-bottom:1px solid var(--line)}@media(max-width:700px){.access-command-copy h2{font-size:18px}.command-points{display:grid;grid-template-columns:1fr}}.admin-login-block{display:flex;flex-direction:column;gap:4px}.admin-login-label{font-size:8px;color:var(--sub2)}.admin-card{position:relative;overflow:hidden}.admin-card:before{content:"";position:absolute;inset:0 0 auto 0;height:2px;background:linear-gradient(90deg,var(--accent),transparent);opacity:.7}.admin-card.is-owner:before{background:linear-gradient(90deg,#f5a524,transparent)}.feature-lock{text-align:center;padding:16px 6px 8px}.feature-lock-icon{width:68px;height:68px;margin:0 auto 14px;display:grid;place-items:center;border-radius:20px;background:linear-gradient(145deg,rgba(var(--accent-rgb),.18),rgba(53,214,255,.08));border:1px solid rgba(var(--accent-rgb),.28);font-size:28px;color:var(--accent)}.feature-lock h3{margin:0 0 8px;font-size:18px}.feature-lock p{margin:0 auto;max-width:520px;line-height:2;color:var(--sub);font-size:11px}.feature-lock-note{display:inline-flex;gap:7px;align-items:center;margin-top:16px;padding:8px 11px;border-radius:999px;border:1px solid var(--line);background:var(--panel2);font-size:9px;color:var(--sub2)}@media(max-width:700px){.admins-hero{grid-template-columns:1fr}.admins-summary{justify-content:flex-start}}
.areq-row{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:13px 14px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.02);margin-bottom:10px}
.areq-row:last-child{margin-bottom:0}
.areq-info{display:flex;flex-direction:column;gap:3px;min-width:0}
.areq-name{font-weight:800;font-size:12.5px}
.areq-meta{font-size:10px;color:var(--sub2);display:flex;gap:10px;flex-wrap:wrap}
.areq-meta span{display:inline-flex;align-items:center;gap:4px}
.areq-note{font-size:10.5px;color:var(--sub);margin-top:2px}
.areq-actions{display:flex;gap:8px;flex-shrink:0}
.areq-empty{text-align:center;padding:22px 10px;color:var(--sub2);font-size:11px}
.areq-status{font-size:9px;font-weight:800;padding:4px 9px;border-radius:999px}
.areq-status.approved{background:rgba(34,197,94,.10);color:#7cf0a8;border:1px solid rgba(34,197,94,.25)}
.areq-status.rejected{background:rgba(239,68,68,.10);color:#ff9b9b;border:1px solid rgba(239,68,68,.25)}
@media(max-width:700px){.admin-grid{grid-template-columns:1fr}}

.bot-lock-note{display:flex;align-items:center;gap:9px;margin:4px 0 12px;padding:10px 12px;border-radius:12px;border:1px solid rgba(245,165,36,.35);background:rgba(245,165,36,.09);color:#f5c76b;font-size:11.5px;line-height:1.9}
.bot-lock-note i{font-size:17px;flex:none}
#setBotToken:disabled,#setBotAdmins:disabled,.bot-text-grid textarea:disabled{opacity:.55;cursor:not-allowed}
</style>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:var(--font-ui,'Vazirmatn'),sans-serif}
:root{
  --bg:#080b14;--panel:#0f1420;--panel2:#141a2b;--line:#212a40;--line2:#2c3752;
  --accent:#9b5cff;--accent2:#37d6ff;--accent-d:#7b3ff0;--good:#22c58b;--warn:#f5a524;--bad:#f24955;
  --text:#eef1fb;--sub:#8b95b3;--sub2:#5c6786;
  --shadow-sm:0 2px 10px rgba(0,0,0,.22);--shadow-md:0 14px 34px rgba(0,0,0,.34);
  --glow-grad:linear-gradient(90deg,var(--accent),var(--accent2));
}
[data-theme="light"]{
  --bg:#ffffff;--panel:#ffffff;--panel2:#f7f8fb;--line:#e5e7eb;--line2:#d1d5db;
  --accent:#7c3aed;--accent2:#0ea5c4;--accent-d:#6425d6;--good:#17a673;--warn:#c9820a;--bad:#e0324a;
  --text:#191c2b;--sub:#666f8a;--sub2:#98a1b8;
  --shadow-sm:0 2px 8px rgba(30,34,60,.05);--shadow-md:0 14px 32px rgba(30,34,60,.08);
}
html{transition:background-color .2s ease}
html,body{background:var(--bg);color:var(--text);height:100%}
html{scrollbar-gutter:stable;overflow-anchor:none}
.body-wrap{overflow-anchor:none}
@media (prefers-reduced-motion: no-preference){
  /* Keep the original look, but avoid expensive perpetual compositor work. */
}
@media (max-width:1100px){
  *{scroll-behavior:auto!important}
}

/* Performance: never animate the entire DOM. Only interactive controls transition. */
button,.btn,.tab,.nav-btn,.icon-btn,input,select,textarea,.card,.drawer,.toast{
  transition:background-color .14s ease,border-color .14s ease,color .14s ease,box-shadow .14s ease;
}
a{color:inherit;text-decoration:none}
button{font-family:inherit;cursor:pointer}
::-webkit-scrollbar{width:8px;height:8px}
::-webkit-scrollbar-thumb{background:var(--line2);border-radius:8px}

/* ===== Shell ===== */
#app{display:flex;height:100vh;position:relative}

/* ============ SIDEBAR ============ */
.sidebar{
  width:252px;flex-shrink:0;height:100vh;display:flex;flex-direction:column;
  background:var(--panel);border-left:1px solid var(--line);position:relative;z-index:30;
  transition:transform .22s ease;
}
.sidebar-brand{display:flex;align-items:center;gap:10px;padding:20px 18px;border-bottom:1px solid var(--line)}
.sidebar-brand img{width:34px;height:34px;border-radius:9px;box-shadow:0 0 0 2px rgba(var(--accent-rgb),.35),0 0 18px rgba(55,214,255,.35)}
.sidebar-brand div{font-weight:800;font-size:14.5px;background:linear-gradient(90deg,var(--text),var(--accent2));-webkit-background-clip:text;background-clip:text;color:transparent}
.sidebar-brand small{display:block;font-weight:400;font-size:10.5px;color:var(--sub)}
.tabnav{flex:1;display:flex;flex-direction:column;gap:2px;padding:14px 12px;overflow-y:auto}
.tab{
  padding:10px 13px;border-radius:10px;font-size:13px;font-weight:600;color:var(--sub);
  display:flex;align-items:center;gap:10px;white-space:nowrap;transition:.14s;
  border:1px solid transparent;position:relative;
}
.tab i{font-size:17px;width:18px;text-align:center;flex-shrink:0}
.tab:hover{color:var(--text);background:rgba(255,255,255,.04)}
.tab.on{color:#fff;background:linear-gradient(90deg,rgba(var(--accent-rgb),.22),rgba(55,214,255,.10));box-shadow:inset 0 0 0 1px rgba(var(--accent-rgb),.35),0 6px 20px -6px rgba(var(--accent-rgb),.5)}
.tab.on:before{content:"";position:absolute;top:6px;bottom:6px;right:-1px;width:3px;border-radius:3px;background:linear-gradient(180deg,var(--accent),var(--accent2));box-shadow:0 0 10px rgba(var(--accent-rgb),.7)}
.tab.on i{color:var(--accent2)}
.tab .bd{background:rgba(255,255,255,.16);border-radius:100px;font-size:10px;padding:1px 7px;margin-right:auto}
.tab.on .bd{background:rgba(255,255,255,.28)}
.sidebar-foot{padding:14px 16px;border-top:1px solid var(--line);display:flex;flex-direction:column;gap:10px}
.lang-mini{display:flex;background:var(--panel2);border:1px solid var(--line);border-radius:100px;padding:3px;gap:2px}
.lang-mini button{flex:1;padding:6px 10px;border:0;background:transparent;color:var(--sub);font-size:11px;font-weight:700;border-radius:100px;cursor:pointer}
.lang-mini button.on{background:linear-gradient(90deg,var(--accent-d),var(--accent));color:#fff}

/* ============ TOP BAR (slim) ============ */
.main-col{flex:1;min-width:0;display:flex;flex-direction:column;height:100vh;position:relative}
.topbar{
  height:60px;flex-shrink:0;display:flex;align-items:center;gap:16px;padding:0 22px;
  background:var(--panel);border-bottom:1px solid var(--line);position:relative;z-index:20;
}
.topbar:after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:1px;background:linear-gradient(90deg,transparent,rgba(var(--accent-rgb),.5),rgba(55,214,255,.5),transparent)}
.hamburger{display:none;width:34px;height:34px;border-radius:8px;background:var(--panel2);border:1px solid var(--line);align-items:center;justify-content:center;color:var(--sub);font-size:17px}
.page-title{font-weight:800;font-size:14.5px;color:var(--text)}
.page-title span{display:block;font-weight:400;font-size:11px;color:var(--sub);margin-top:1px}
.top-right{display:flex;align-items:center;gap:10px;flex-shrink:0;margin-right:auto}
.user-chip{display:flex;align-items:center;gap:9px;background:var(--panel2);border:1px solid var(--line);padding:6px 12px 6px 8px;border-radius:100px;font-size:12.5px;cursor:pointer}
.user-chip .av{width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;color:#fff;box-shadow:0 0 12px rgba(var(--accent-rgb),.45)}
.user-chip .role-tag{font-size:9px;color:var(--sub2);display:block;margin-top:-1px}
.icon-btn{width:36px;height:36px;border-radius:9px;background:var(--panel2);border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--sub);font-size:16px}
.icon-btn:hover{color:var(--text);border-color:var(--line2)}
.sidebar-overlay{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:29;display:none}
.wide-sidebar .sidebar{width:292px}
.wide-sidebar .main-col{min-width:0}
@media(max-width:980px){
  .hamburger{display:flex}
  .sidebar{position:fixed;top:0;right:0;transform:translateX(105%)}
  #app.sb-open .sidebar{transform:translateX(0)}
  #app.sb-open .sidebar-overlay{display:block}
}

.body-wrap{flex:1;overflow:auto;padding:22px 26px 70px}
.news-hero{display:flex;gap:18px;align-items:flex-start;padding:22px;margin-bottom:16px}
.news-hero-icon{flex-shrink:0;width:54px;height:54px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:24px;color:#fff;background:linear-gradient(135deg,var(--accent),var(--accent2));box-shadow:0 8px 22px rgba(var(--accent-rgb),.35)}
.support-icon{background:linear-gradient(135deg,#ff5f7e,var(--warn));box-shadow:0 8px 22px rgba(255,95,126,.3)}
.news-hero-body h2{font-size:16px;margin-bottom:8px}
.news-hero-body p{font-size:12.5px;color:var(--sub);line-height:2;margin-bottom:14px;max-width:640px}
.news-join-btn{display:inline-flex}
.support-card-row{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.support-card-box{display:flex;flex-direction:column;gap:3px;padding:12px 18px;border-radius:14px;background:var(--panel2);border:1px solid var(--line)}
.support-card-label{font-size:9px;color:var(--sub2)}
.support-card-number{font-size:16px;font-weight:800;letter-spacing:.04em;direction:ltr;display:block}
.support-card-name{font-size:11px;color:var(--sub)}
@media(max-width:700px){.news-hero{flex-direction:column}}

.page{display:none;max-width:1320px;margin:0 auto}
.page.on{display:block;animation:fade .18s ease}
@keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
@keyframes spin{to{transform:rotate(360deg)}}
.spin{display:inline-block;animation:spin .7s linear infinite}
.no-motion .spin{animation:none}

.pg-head{display:flex;align-items:flex-end;justify-content:space-between;gap:14px;margin-bottom:20px;flex-wrap:wrap}
.pg-head h1{font-size:19px;font-weight:800}
.pg-head p{font-size:12.5px;color:var(--sub);margin-top:3px}
.toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.search{position:relative}
.search input{width:230px;padding:9px 34px 9px 12px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font-size:13px;outline:none}
.search input:focus{border-color:var(--accent)}
.search i{position:absolute;right:11px;top:50%;transform:translateY(-50%);color:var(--sub2);font-size:15px}
select.sel{padding:9px 12px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font-size:13px;outline:none}
.btn{padding:9px 16px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font-size:13px;font-weight:600;display:inline-flex;align-items:center;gap:7px}
.btn:hover{border-color:var(--line2)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.primary:hover{background:var(--accent-d)}
.btn.danger{color:var(--bad);border-color:rgba(242,73,85,.3)}
.btn.danger:hover{background:rgba(242,73,85,.08)}
.btn.sm{padding:6px 11px;font-size:12px}
.btn:disabled{opacity:.5;cursor:not-allowed}

/* stat cards */
.stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin-bottom:22px}
.stat-card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.stat-card .sc-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.stat-card .sc-icon{width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px}
.stat-card .sc-val{font-size:22px;font-weight:800}
.stat-card .sc-label{font-size:11.5px;color:var(--sub);margin-top:2px}

/* table */
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;position:relative}
.card:before{content:"";position:absolute;top:0;left:16px;right:16px;height:2px;border-radius:0 0 3px 3px;background:linear-gradient(90deg,var(--accent),var(--accent2));opacity:.55}
table{width:100%;border-collapse:collapse;font-size:13px}
thead th{text-align:right;padding:12px 14px;background:var(--panel2);color:var(--sub);font-weight:700;font-size:11.5px;border-bottom:1px solid var(--line)}
tbody td{padding:11px 14px;border-bottom:1px solid var(--line);vertical-align:middle}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:rgba(255,255,255,.015)}
.mono{font-family:ui-monospace,Consolas,monospace;direction:ltr;text-align:left;font-size:12px;color:var(--sub)}
.badge{display:inline-flex;align-items:center;gap:5px;padding:3px 9px;border-radius:100px;font-size:11px;font-weight:700}
.badge.green{background:rgba(34,197,139,.14);color:var(--good)}
.badge.red{background:rgba(242,73,85,.14);color:var(--bad)}
.badge.gray{background:rgba(135,146,168,.14);color:var(--sub)}
.badge.orange{background:rgba(245,165,36,.14);color:var(--warn)}
.row-actions{display:flex;gap:6px;justify-content:flex-end}
.iconbtn{width:29px;height:29px;border-radius:7px;background:var(--panel2);border:1px solid var(--line);display:inline-flex;align-items:center;justify-content:center;color:var(--sub);font-size:14px}
.iconbtn:hover{color:var(--text);border-color:var(--line2)}
.empty{padding:50px 20px;text-align:center;color:var(--sub2)}
.empty i{font-size:30px;display:block;margin-bottom:10px}
.bar-mini{width:70px;height:6px;background:var(--line2);border-radius:99px;overflow:hidden;display:inline-block;vertical-align:middle;margin-left:6px}
.bar-mini i{display:block;height:100%;background:linear-gradient(90deg,var(--accent),var(--good))}


/* ===== Appearance Studio ===== */
.appearance-studio{display:grid;grid-template-columns:1.25fr .75fr;gap:14px;margin-bottom:18px}.appearance-card{padding:18px;border:1px solid var(--line);border-radius:16px;background:linear-gradient(145deg,rgba(var(--accent-rgb),.07),rgba(255,255,255,.018));overflow:hidden}.appearance-card h3{font-size:14px;margin-bottom:4px}.appearance-card p{font-size:10.5px;color:var(--sub);line-height:1.8}.appearance-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:14px}.appearance-field{padding:11px;border:1px solid var(--line);border-radius:12px;background:var(--panel2)}.appearance-field label{display:block;color:var(--sub);font-size:10px;margin-bottom:7px}.appearance-field select{width:100%;padding:9px 10px;border-radius:9px;border:1px solid var(--line);background:var(--panel);color:var(--text);outline:none}.theme-pills,.accent-pills{display:flex;gap:7px;flex-wrap:wrap}.theme-pill,.accent-pill{border:1px solid var(--line);background:var(--panel);color:var(--sub);border-radius:9px;padding:8px 11px;font-size:10px;cursor:pointer}.theme-pill.on,.accent-pill.on{color:#fff;border-color:var(--accent);background:rgba(var(--accent-rgb),.14)}.accent-pill{display:flex;align-items:center;gap:6px}.accent-dot{width:10px;height:10px;border-radius:50%;display:inline-block}.appearance-preview{min-height:100%;position:relative;display:flex;align-items:center;justify-content:center}.preview-window{width:100%;max-width:330px;border:1px solid var(--line);border-radius:15px;background:var(--panel);overflow:hidden;box-shadow:0 25px 60px rgba(0,0,0,.22)}.preview-top{height:36px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:6px;padding:0 10px}.preview-top i{font-size:10px;color:var(--sub)}.preview-main{display:grid;grid-template-columns:82px 1fr;min-height:140px}.preview-side{padding:10px;border-left:1px solid var(--line);background:var(--panel2)}.preview-side div{height:22px;border-radius:6px;margin-bottom:6px;background:rgba(255,255,255,.04)}.preview-side div.active{background:linear-gradient(90deg,var(--accent),var(--accent-d))}.preview-content{padding:12px}.preview-content .pv-title{font-size:12px;font-weight:800}.preview-content .pv-sub{font-size:8px;color:var(--sub);margin-top:3px}.pv-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:14px}.pv-cards span{height:45px;border-radius:9px;border:1px solid var(--line);background:rgba(255,255,255,.02)}.appearance-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:13px}.appearance-toggle{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 11px;border:1px solid var(--line);border-radius:11px;background:var(--panel2);font-size:10.5px;color:var(--sub)}.switch{width:38px;height:21px;border-radius:99px;background:var(--line2);position:relative;cursor:pointer;border:0}.switch:after{content:'';position:absolute;width:15px;height:15px;top:2px;right:2px;border-radius:50%;background:#fff;transition:.16s}.switch.on{background:var(--accent)}.switch.on:after{right:21px}.density-compact .tab{padding-top:8px;padding-bottom:8px}.density-compact .body-wrap{padding-top:16px;padding-bottom:45px}.density-compact .card{border-radius:12px}.no-motion *, .no-motion *:before, .no-motion *:after{transition:none!important;animation:none!important;scroll-behavior:auto!important}
@media(max-width:900px){.appearance-studio{grid-template-columns:1fr}}@media(max-width:600px){.appearance-grid{grid-template-columns:1fr}.preview-window{max-width:none}}

.advanced-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:14px}.pro-action{border:1px solid var(--line);background:linear-gradient(145deg,var(--panel2),rgba(var(--accent-rgb),.05));color:var(--text);border-radius:14px;padding:15px;text-align:right;cursor:pointer;box-shadow:var(--ui-glow);}.pro-action i{font-size:20px;color:var(--accent);display:block;margin-bottom:10px}.pro-action b{display:block;font-size:11px}.pro-action small{display:block;color:var(--sub);font-size:9px;margin-top:4px}.accent-pills{max-height:92px;overflow:auto}.radius-sharp .card,.radius-sharp .appearance-card,.radius-sharp .appearance-field,.radius-sharp .btn,.radius-sharp .tab,.radius-sharp .search input{border-radius:6px}.radius-pill .card,.radius-pill .appearance-card,.radius-pill .appearance-field{border-radius:24px}.radius-pill .btn,.radius-pill .tab,.radius-pill .search input{border-radius:999px}.font-small{font-size:92%}.font-large{font-size:108%}.appearance-card,.card,.pro-action{box-shadow:var(--ui-glow)}
@media(max-width:900px){.advanced-grid{grid-template-columns:1fr 1fr}}@media(max-width:600px){.advanced-grid{grid-template-columns:1fr}}

.ib-quickstats{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 14px}.ib-quickstats>div{position:relative;overflow:hidden;display:flex;align-items:center;gap:10px;padding:12px 15px;border:1px solid var(--line);background:linear-gradient(155deg,rgba(255,255,255,.03),rgba(255,255,255,.01));border-radius:14px;flex:1;min-width:150px;transition:transform .15s ease,border-color .15s ease}.ib-quickstats>div:hover{transform:translateY(-2px);border-color:var(--line2)}.ib-quickstats i{width:32px;height:32px;display:grid;place-items:center;border-radius:9px;background:rgba(var(--accent-rgb),.12);color:#a997ff;font-size:15px;flex-shrink:0}.ib-quickstats b{display:block;font-size:17px;line-height:1.2}.ib-quickstats small{display:block;color:var(--sub2);font-size:9.5px;margin-top:2px}
/* ===== Inbound cards (grid) ===== */
.ib-listbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 12px;flex-wrap:wrap}
.ib-selectall{display:flex;align-items:center;gap:8px;font-size:11.5px;color:var(--sub);cursor:pointer;user-select:none}
.ib-selectall input{width:15px;height:15px;accent-color:var(--accent);cursor:pointer}
.ib-count{font-size:11px;color:var(--sub2)}
.ib-bulkbar{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:11px 16px;background:linear-gradient(90deg,rgba(var(--accent-rgb),.12),rgba(var(--accent-rgb),.04));border:1px solid rgba(var(--accent-rgb),.28);border-radius:13px;font-size:11.5px;color:var(--sub);flex-wrap:wrap;margin-bottom:12px}
.ib-bulkbar b{color:var(--text)}.ib-bulkactions{display:flex;gap:6px}
.ib-check{width:15px;height:15px;accent-color:var(--accent);cursor:pointer}

.ib-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(328px,1fr));gap:14px}
.ib-card{position:relative;display:flex;flex-direction:column;gap:13px;padding:16px;border:1px solid var(--line);border-radius:16px;background:linear-gradient(165deg,rgba(255,255,255,.035),rgba(255,255,255,.012));box-shadow:var(--shadow-sm);overflow:hidden;transition:transform .15s ease,border-color .15s ease,box-shadow .15s ease}
.ib-card:before{content:'';position:absolute;inset:0 0 auto 0;height:3px;background:linear-gradient(90deg,var(--accent),#39d6ff)}
.ib-card:hover{border-color:var(--line2);box-shadow:var(--shadow-md)}
.ib-card.ib-off{opacity:.58}
.ib-card.ib-off:before{background:var(--sub2)}
.ib-card.ib-off:hover{opacity:.85}
.ib-card.ib-selected{border-color:var(--accent);box-shadow:0 0 0 3px rgba(var(--accent-rgb),.14)}

.ib-card-head{display:flex;align-items:flex-start;gap:11px}
.ib-card-check{position:absolute;top:14px;left:14px;opacity:0;pointer-events:none;transition:opacity .15s ease}
.ib-card:hover .ib-card-check,.ib-card.ib-selected .ib-card-check{opacity:1;pointer-events:auto}
.ib-avatar{width:40px;height:40px;border-radius:12px;flex-shrink:0;display:grid;place-items:center;font-size:17px;background:rgba(var(--accent-rgb),.14);color:#b79bff;border:1px solid rgba(var(--accent-rgb),.22)}
.ib-card-id{flex:1;min-width:0;padding-left:20px}
.ib-card-id .ib-name-top{display:flex;align-items:center;gap:6px}
.ib-card-id b{font-size:13px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;display:block}
.ib-card-id .mono{font-size:9.5px;color:var(--sub2);margin-top:2px}
.ib-card-controls{display:flex;flex-direction:column;align-items:flex-end;gap:7px;flex-shrink:0}

.ib-tagrow{display:flex;flex-wrap:wrap;gap:5px}
.ib-tagrow span{padding:3px 8px;border-radius:7px;background:var(--panel2);border:1px solid var(--line);font-size:9.5px;font-weight:700;letter-spacing:.01em;color:var(--sub);white-space:nowrap;transition:border-color .12s ease}
.ib-card:hover .ib-tagrow span{border-color:var(--line2)}
.ib-live-tag{background:rgba(34,197,139,.14)!important;color:var(--good)!important;border-color:transparent!important;display:inline-flex!important;align-items:center;gap:4px}
.ib-live-tag i{width:5px;height:5px;border-radius:50%;background:var(--good);animation:ibLivePulse 1.6s ease-in-out infinite;flex-shrink:0}
@keyframes ibLivePulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.35);opacity:.6}}
.no-motion .ib-live-tag i{animation:none}
.ib-linkonly-tag{background:rgba(242,73,85,.12)!important;color:var(--bad)!important;border-color:transparent!important}

.ib-card-addr{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:8px 11px;border-radius:10px;background:var(--panel2);border:1px solid var(--line)}
.ib-card-addr span.mono{font-size:11px;color:var(--text)}
.ib-card-addr small{font-size:9px;color:var(--sub2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:110px}

.ib-card-traffic{display:flex;flex-direction:column;gap:6px}
.ib-card-traffic .ib-tf-top{display:flex;align-items:center;justify-content:space-between;font-size:9.5px;color:var(--sub2)}
.ib-card-traffic .ib-tf-top b{font-size:11.5px;color:var(--text);font-weight:800}
.ib-progress{height:6px;border-radius:99px;background:var(--line2);overflow:hidden;box-shadow:inset 0 0 0 1px var(--line)}
.ib-progress i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),#39d6ff);transition:width .3s ease}
.ib-progress i.warn{background:linear-gradient(90deg,#f5a524,#f59e0b)}
.ib-progress i.crit{background:linear-gradient(90deg,#f24955,#ef4444)}

.ib-card-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}
.ib-card-stats>div{padding:8px 9px;border-radius:10px;background:var(--panel2);border:1px solid var(--line);text-align:center}
.ib-card-stats small{display:block;color:var(--sub2);font-size:8.5px;margin-bottom:3px}
.ib-card-stats b{font-size:11px}
.ib-card-stats b.soon{color:var(--warn)}
.ib-card-stats b.expired{color:var(--bad)}

.ib-card-foot{display:flex;align-items:center;justify-content:space-between;gap:8px;padding-top:2px;border-top:1px dashed var(--line);padding-top:11px}
.ib-card-foot .ib-clientcell{display:flex;align-items:center;gap:7px;font-size:10.5px;color:var(--sub)}
.ib-card-foot .ib-clientcell .iconbtn{width:27px;height:27px;font-size:12px}
.ib-card-actions{display:flex;gap:5px}
.ib-card-actions .iconbtn{width:29px;height:29px;font-size:13px;border-radius:9px;transition:transform .12s ease,background-color .12s ease,color .12s ease}
.ib-card-actions .iconbtn:hover{transform:translateY(-1px);background:var(--panel2)}

.ib-switch{width:34px;height:19px;border-radius:99px;background:var(--line2);position:relative;cursor:pointer;border:0;flex-shrink:0;box-shadow:inset 0 0 0 1px var(--line)}
.ib-switch:after{content:'';position:absolute;width:13px;height:13px;top:3px;right:3px;border-radius:50%;background:#fff;transition:.16s}
.ib-switch.on{background:linear-gradient(90deg,var(--accent),#39d6ff);box-shadow:0 0 12px rgba(var(--accent-rgb),.35)}
.ib-switch.on:after{right:18px}
.ib-status-dot{width:8px;height:8px;border-radius:50%;background:#7688a9;flex-shrink:0}
.ib-status-dot.green{background:#22c58b;box-shadow:0 0 0 3px rgba(34,197,139,.18);animation:ibLivePulse 1.6s ease-in-out infinite}
.ib-status-dot.red{background:#f24955}
.no-motion .ib-status-dot{animation:none}
@media(max-width:560px){.ib-grid{grid-template-columns:1fr}}
.ov-quickstats>div{position:relative;overflow:hidden}
.ov-quickstats>div:nth-child(1) i{background:rgba(var(--accent-rgb),.14);color:#a997ff}
.ov-quickstats>div:nth-child(2) i{background:rgba(34,197,139,.14);color:#22c58b}
.ov-quickstats>div:nth-child(3) i{background:rgba(53,214,255,.14);color:#35d6ff}
.ov-quickstats>div:nth-child(4) i{background:rgba(245,165,36,.14);color:#f5a524}
.ov-toplinks{padding:14px 18px}
.ov-toplink-row{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px dashed var(--line)}
.ov-toplink-row:last-child{border-bottom:none}
.ov-toplink-row .otl-rank{width:20px;height:20px;border-radius:6px;background:var(--panel2);display:grid;place-items:center;font-size:10px;color:var(--sub2);flex-shrink:0}
.ov-toplink-row .otl-info{flex:1;min-width:0}
.ov-toplink-row .otl-info b{font-size:11.5px;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ov-toplink-row .otl-bar{height:4px;border-radius:99px;background:var(--line2);margin-top:5px;overflow:hidden}
.ov-toplink-row .otl-bar i{display:block;height:100%;background:linear-gradient(90deg,var(--accent),#39d6ff);border-radius:99px}
.ov-toplink-row .otl-val{font-size:10px;color:var(--sub2);white-space:nowrap;flex-shrink:0}
.ov-empty{padding:20px;text-align:center;color:var(--sub2);font-size:11px}
@media(max-width:900px){.ib-quickstats{flex-direction:column}}

/* drawer */
.overlay{position:fixed;inset:0;background:rgba(4,6,10,.55);backdrop-filter:blur(2px);z-index:90;display:none}
.overlay.show{display:block}
.drawer{position:fixed;top:0;left:0;bottom:0;width:680px;max-width:92vw;background:var(--panel);border-left:1px solid var(--line);z-index:91;transform:translateX(-105%);transition:transform .22s cubic-bezier(.4,0,.2,1);display:flex;flex-direction:column}
.drawer.show{transform:translateX(0)}
.dr-head{padding:18px 20px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between}
.dr-head h3{font-size:15px;font-weight:800}
.dr-body{flex:1;overflow:auto;padding:18px 20px}
.dr-foot{padding:16px 20px;border-top:1px solid var(--line);display:flex;gap:10px}
.grp{margin-bottom:16px}
.grp label{display:block;font-size:12px;font-weight:600;color:var(--sub);margin-bottom:6px}
.grp input,.grp select,.grp textarea{width:100%;padding:10px 12px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font-size:13px;outline:none}
.grp input:focus,.grp select:focus,.grp textarea:focus{border-color:var(--accent)}
.grp textarea{resize:vertical;min-height:64px;font-family:ui-monospace,monospace;direction:ltr;text-align:left}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.chk{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--text)}
.hint{font-size:11px;color:var(--sub2);margin-top:5px;line-height:1.7}
.divider{height:1px;background:var(--line);margin:18px 0}
.inbound-builder{display:flex;flex-direction:column;gap:16px}
.ib-hero{padding:16px;border:1px solid var(--line);border-radius:14px;background:linear-gradient(135deg,rgba(79,124,255,.10),rgba(var(--accent-rgb),.07));display:flex;align-items:center;justify-content:space-between;gap:12px}
.ib-hero .ib-title{display:flex;align-items:center;gap:12px}.ib-hero .ib-icon{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;background:linear-gradient(135deg,var(--accent),#6d5dfc);color:#fff;font-size:20px;box-shadow:0 10px 24px rgba(79,124,255,.22)}
.ib-hero b{display:block;font-size:14px}.ib-hero small{display:block;color:var(--sub);font-size:11px;margin-top:3px}
.ib-section{border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.018);overflow:hidden}.ib-section-head{padding:12px 14px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between}.ib-section-head b{font-size:12.5px}.ib-section-head small{font-size:10.5px;color:var(--sub2)}
.ib-section-body{padding:14px}.ib-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.ib-grid.three{grid-template-columns:1fr 1fr 1fr}.ib-full{grid-column:1/-1}
.ib-choice{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}
/* Professional inbound protocol/transport matrix — renamed to .ib-opt (was
   accidentally reusing the .ib-card class name used by the main inbound
   dashboard cards above; that collision was overriding the dashboard card
   layout with these small radio-tile rules). */
.ib-matrix{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px}
.ib-opt{position:relative;display:flex;align-items:center;gap:10px;padding:12px;border:1px solid var(--line);border-radius:12px;background:linear-gradient(145deg,rgba(255,255,255,.025),rgba(255,255,255,.01));cursor:pointer;transition:.16s;user-select:none}
.ib-opt:hover{border-color:rgba(var(--accent-rgb),.45);transform:translateY(-1px)}
.ib-opt.on{border-color:var(--accent);background:linear-gradient(145deg,rgba(124,58,237,.18),rgba(var(--accent-rgb),.08));box-shadow:0 8px 24px rgba(124,58,237,.12),inset 0 0 0 1px rgba(var(--accent-rgb),.18)}
.ib-opt.off{opacity:.42;cursor:not-allowed;filter:saturate(.5)}
.ib-opt input{position:absolute;opacity:0;pointer-events:none}
.ib-opt .ib-opt-icon{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:rgba(255,255,255,.05);color:var(--accent);font-size:17px;flex:0 0 auto}
.ib-opt b{display:block;font-size:11.5px}.ib-opt small{display:block;color:var(--sub2);font-size:8.5px;margin-top:2px}
.ib-step{display:flex;align-items:center;gap:8px;margin-bottom:11px}.ib-step .num{width:24px;height:24px;border-radius:8px;display:grid;place-items:center;background:rgba(124,58,237,.16);color:#c9a8ff;font-size:10px;font-weight:900}.ib-step b{font-size:12px}.ib-step small{display:block;color:var(--sub2);font-size:9px;margin-top:2px}
.ib-divider{height:1px;background:var(--line);margin:15px 0}
.ib-mode-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.ib-mini{padding:9px;border:1px solid var(--line);border-radius:10px;background:var(--panel2);font-size:10px;text-align:center;color:var(--sub)}
.ib-mini b{display:block;color:var(--text);font-size:11px;margin-bottom:2px}
.ib-mini.active{border-color:rgba(34,197,139,.35);background:rgba(34,197,139,.06)}
@media(max-width:700px){.ib-matrix{grid-template-columns:repeat(2,1fr)}.ib-mode-grid{grid-template-columns:repeat(2,1fr)}}
.ib-choice label{position:relative}.ib-choice input{position:absolute;opacity:0;pointer-events:none}.ib-choice span{display:flex;align-items:center;gap:8px;padding:10px 11px;border:1px solid var(--line);border-radius:10px;background:var(--panel2);font-size:12px;cursor:pointer;transition:.15s}.ib-choice span i{font-size:15px;color:var(--sub)}.ib-choice input:checked+span{border-color:var(--accent);background:rgba(79,124,255,.12);box-shadow:inset 0 0 0 1px rgba(79,124,255,.25)}.ib-choice input:checked+span i{color:var(--accent)}
.ib-status{padding:10px 12px;border-radius:10px;border:1px solid var(--line);background:rgba(0,0,0,.12);font-size:11px;line-height:1.8}.ib-status.ok{border-color:rgba(34,197,139,.3);background:rgba(34,197,139,.07)}.ib-status.warn{border-color:rgba(245,165,36,.3);background:rgba(245,165,36,.07)}
.ib-summary{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.ib-summary .sum{padding:9px 10px;border:1px solid var(--line);border-radius:9px;background:var(--panel2)}.ib-summary small{display:block;color:var(--sub2);font-size:9.5px}.ib-summary b{display:block;margin-top:3px;font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ib-advanced{display:none}.ib-advanced.open{display:block}.ib-advanced-toggle{width:100%;justify-content:space-between}.ib-help{font-size:10.5px;color:var(--sub2);line-height:1.8;margin-top:6px}.ib-danger{color:#ff9b9b}
@media(max-width:600px){.ib-grid,.ib-grid.three,.ib-choice,.ib-summary{grid-template-columns:1fr}.ib-full{grid-column:auto}}

.section-title{font-size:12px;font-weight:800;color:var(--sub);text-transform:uppercase;letter-spacing:.03em;margin-bottom:10px}

/* ===== Message Center ===== */
.message-center{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px}.message-stat{padding:15px;border:1px solid var(--line);border-radius:15px;background:linear-gradient(145deg,var(--panel),rgba(var(--accent-rgb),.04));position:relative;overflow:hidden}.message-stat:after{content:"";position:absolute;inset:auto -20px -30px auto;width:90px;height:90px;border-radius:50%;background:radial-gradient(circle,var(--accent),transparent 68%);opacity:.08}.message-stat .ms-icon{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:rgba(var(--accent-rgb),.12);color:var(--accent);margin-bottom:10px}.message-stat b{font-size:22px;display:block}.message-stat small{display:block;color:var(--sub);font-size:9px;margin-top:4px}.message-stat.danger .ms-icon{color:#fb7185;background:rgba(244,63,94,.11)}.message-stat.warn .ms-icon{color:#fbbf24;background:rgba(245,158,11,.11)}.message-stat.good .ms-icon{color:#34d399;background:rgba(16,185,129,.11)}.message-toolbar{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.message-filter{display:flex;gap:6px;flex-wrap:wrap}.message-filter button{padding:7px 10px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--sub);font-size:10px;cursor:pointer}.message-filter button.on{border-color:var(--accent);color:var(--text);background:rgba(var(--accent-rgb),.12)}.message-list{display:flex;flex-direction:column;gap:8px;padding:12px}.message-row{display:grid;grid-template-columns:38px 1fr auto;gap:10px;align-items:start;padding:12px;border:1px solid var(--line);border-radius:13px;background:rgba(255,255,255,.015)}.message-row:hover{border-color:color-mix(in srgb,var(--accent) 40%,var(--line));background:rgba(255,255,255,.025)}.message-row .mi{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:rgba(255,255,255,.04);color:var(--sub)}.message-row.err .mi{color:#fb7185;background:rgba(244,63,94,.09)}.message-row.warn .mi{color:#fbbf24;background:rgba(245,158,11,.09)}.message-row.ok .mi{color:#34d399;background:rgba(16,185,129,.09)}.message-row .mt{min-width:0}.message-row .mt b{font-size:11px;display:block;line-height:1.8}.message-row .mt p{font-size:9px;color:var(--sub);margin-top:3px;word-break:break-word;line-height:1.8}.message-row .meta{text-align:left;direction:ltr;color:var(--sub2);font-size:8px;white-space:nowrap}.message-row .meta strong{display:block;color:var(--sub);font-size:9px;margin-bottom:3px}.error-detail{margin-top:8px;padding:9px;border-radius:9px;background:rgba(0,0,0,.16);border:1px dashed var(--line);font-family:ui-monospace,Consolas,monospace;font-size:8px;line-height:1.8;direction:ltr;text-align:left;white-space:pre-wrap;word-break:break-word;color:#aeb9d2;max-height:120px;overflow:auto}.message-empty{padding:45px 20px;text-align:center;color:var(--sub);font-size:11px}.message-empty i{display:block;font-size:34px;color:var(--good);margin-bottom:10px}.message-auto{font-size:9px;color:var(--sub2);margin-right:auto}@media(max-width:900px){.message-center{grid-template-columns:repeat(2,1fr)}}@media(max-width:600px){.message-center{grid-template-columns:1fr 1fr}.message-row{grid-template-columns:34px 1fr}.message-row .meta{grid-column:2;text-align:right;direction:rtl}.message-auto{display:none}}
/* toast */
#toastWrap{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:200;display:flex;flex-direction:column;gap:8px}
.toast{background:var(--panel2);border:1px solid var(--line2);padding:11px 18px;border-radius:10px;font-size:13px;display:flex;align-items:center;gap:9px;box-shadow:0 10px 30px rgba(0,0,0,.4);animation:up .18s ease}
.toast.ok{border-color:rgba(34,197,139,.4)}.toast.ok i{color:var(--good)}
.toast.err{border-color:rgba(242,73,85,.4)}.toast.err i{color:var(--bad)}
@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

.qr-box{background:#fff;padding:10px;border-radius:12px;width:150px;height:150px;margin:0 auto 12px}
.qr-box img{width:100%;height:100%}
.copy-row{display:flex;gap:8px}
.copy-row input{flex:1}

.two-col{display:grid;grid-template-columns:1.1fr .9fr;gap:18px}
@media(max-width:980px){.two-col{grid-template-columns:1fr}}
.status-dot{width:9px;height:9px;border-radius:50%;display:inline-block;margin-left:6px}
.status-dot.on{background:var(--good);box-shadow:0 0 0 3px rgba(34,197,139,.18)}
.status-dot.off{background:var(--sub2)}
.settings-card{padding:20px}
.link-cell{display:flex;flex-direction:column;gap:2px}
.link-cell b{font-size:13px}
.link-cell span{font-size:11px;color:var(--sub2)}
.loading{opacity:.5;pointer-events:none}

/* VodiWalker 17 — original premium control-center skin */
body{background:radial-gradient(900px 500px at 75% -10%,rgba(var(--accent-rgb),.10),transparent 65%),var(--bg)}
/* رفع باگ اصلیِ «پوسته روشن»: پیش‌تر پس‌زمینه‌ی سایدبار و نوار بالا همیشه
   با رنگ ثابت تیره نوشته شده بود و data-theme را نادیده می‌گرفت؛ در نتیجه
   با فعال کردن پوسته‌ی روشن، فقط بدنه‌ی صفحه سفید می‌شد ولی سایدبار/تاپ‌بار
   تیره می‌ماند (ظاهر ناقص و دو رنگ). این‌جا هر دو حالت را صریحاً تعریف می‌کنیم. */
[data-theme="dark"] .sidebar,
:root:not([data-theme]) .sidebar{background:linear-gradient(180deg,#0d111b 0%,#0b0f17 100%);box-shadow:inset -1px 0 rgba(255,255,255,.04),20px 0 60px rgba(0,0,0,.16)}
[data-theme="light"] .sidebar{background:linear-gradient(180deg,#ffffff 0%,#f7f8fb 100%);box-shadow:inset -1px 0 rgba(0,0,0,.04),20px 0 50px rgba(30,34,60,.05)}
.sidebar{width:268px}
.sidebar-brand{padding:18px 20px 17px}.sidebar-brand img{width:38px;height:38px;border-radius:12px}.sidebar-brand div{font-size:15px}.sidebar-brand small{color:var(--sub2)}
.tab{padding:11px 14px;border-radius:11px;margin:2px 0}.tab-locked{opacity:.58}.tab-locked:hover{opacity:.85}.tab.on{background:linear-gradient(135deg,var(--accent),var(--accent-d));box-shadow:0 10px 25px -10px rgba(var(--accent-rgb),.55)}
[data-theme="dark"] .topbar,
:root:not([data-theme]) .topbar{height:68px;padding:0 26px;background:rgba(13,17,27,.88);backdrop-filter:none;box-shadow:0 1px 0 rgba(255,255,255,.025)}
[data-theme="light"] .topbar{height:68px;padding:0 26px;background:rgba(255,255,255,.88);backdrop-filter:none;box-shadow:0 1px 0 rgba(30,34,60,.04)}
.body-wrap{padding:24px 28px 70px}.page{max-width:1440px}
.pg-head{margin-bottom:18px}.pg-head h1{font-size:22px;letter-spacing:-.4px}.pg-head p{font-size:12px}
.eyebrow{font-size:10px;letter-spacing:.16em;color:#8d82c9;font-weight:800;margin-bottom:7px}.live-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#22c58b;box-shadow:0 0 0 4px rgba(34,197,139,.10);vertical-align:middle;margin-left:5px}
.stat-grid{gap:12px}.stat-card{border-radius:16px;padding:16px 18px;background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,.018));box-shadow:var(--shadow-sm)}
.card{border-radius:16px;background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,.018));box-shadow:var(--shadow-sm);position:relative}
.card:hover{box-shadow:var(--shadow-md)}
.inbound-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:0 0 16px}.inbound-strip>div{display:flex;align-items:center;gap:11px;padding:13px 15px;border:1px solid var(--line);background:rgba(255,255,255,.018);border-radius:13px}.inbound-strip i{width:34px;height:34px;display:grid;place-items:center;border-radius:10px;background:rgba(var(--accent-rgb),.12);color:#a997ff;font-size:17px}.inbound-strip b{display:block;font-size:12px}.inbound-strip small{display:block;color:var(--sub);font-size:10px;margin-top:2px}.btn-inbound{padding-left:20px;padding-right:20px;box-shadow:0 12px 30px -12px rgba(var(--accent-rgb),.75)}
.endpoint-input{display:flex;gap:7px;align-items:stretch}.endpoint-input input{flex:1;min-width:0}.endpoint-btn{white-space:nowrap;padding:9px 11px;font-size:11px}.endpoint-btn:disabled{opacity:.65}.ib-status.ok{border-color:rgba(34,197,139,.35)!important}.ib-status.warn{border-color:rgba(245,165,36,.35)!important}@media(max-width:800px){.inbound-strip{grid-template-columns:1fr}.body-wrap{padding:18px 14px 60px}}

.resource-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px}.resource-card{min-height:126px;padding:13px 15px;border:1px solid var(--line);border-radius:14px;background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,.015));overflow:hidden;position:relative;transition:border-color .15s ease}.resource-card:hover{border-color:rgba(var(--accent-rgb),.4)}.resource-card .rc-head i{background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;color:transparent}.rc-head{display:flex;justify-content:space-between;align-items:center;font-size:10px;color:var(--sub);font-weight:800;letter-spacing:.08em}.rc-head i{margin-left:5px;color:#7688a9}.rc-head b{font-size:21px;color:var(--text);letter-spacing:0}.rc-sub{font-size:9px;color:var(--sub2);margin-top:6px}.spark{display:block;width:100%;height:44px;margin-top:9px}.spark polyline{fill:none;stroke:#557bff;stroke-width:2;vector-effect:non-scaling-stroke}.spark path{fill:rgba(85,123,255,.08);stroke:none}.traffic-layout{display:grid;grid-template-columns:minmax(0,1.65fr) minmax(290px,.55fr);gap:14px;margin-bottom:14px}.traffic-card,.connection-card{padding:0}.panel-head{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid var(--line)}.panel-head b{display:block;font-size:10px;letter-spacing:.09em}.panel-head small{display:block;color:var(--sub2);font-size:9px;margin-top:4px}.panel-head>i{color:var(--sub2)}.traffic-legend{display:flex;gap:14px;font-size:10px;color:var(--sub)}.traffic-legend b{color:var(--text)}.big-chart{height:250px;padding:10px 14px 0}.big-chart svg{width:100%;height:100%}.big-chart polyline{fill:none;stroke:#5b78d9;stroke-width:2;vector-effect:non-scaling-stroke}.big-chart .area{fill:rgba(91,120,217,.07);stroke:none}.traffic-foot{display:grid;grid-template-columns:1fr 1fr 1.5fr;padding:12px 16px;border-top:1px solid var(--line)}.traffic-foot small{display:block;color:var(--sub2);font-size:8px}.traffic-foot b{font-size:12px}.connection-number{font-size:28px;font-weight:900;padding:16px 18px 0}.connection-label{font-size:8px;color:var(--sub2);padding:2px 18px}.conn-chart{width:100%;height:120px;padding:0 12px}.conn-chart polyline{fill:none;stroke:#4f7cff;stroke-width:2;vector-effect:non-scaling-stroke}.conn-chart .area{fill:rgba(79,124,255,.08);stroke:none}.conn-foot{display:flex;justify-content:space-between;padding:10px 16px;border-top:1px solid var(--line);font-size:9px;color:var(--sub)}.conn-foot b{color:var(--text)}.bottom-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}.mini-panel{padding-bottom:10px}.health-row{display:flex;justify-content:space-between;padding:10px 16px;border-bottom:1px solid var(--line);font-size:11px}.health-row:last-child{border-bottom:0}.health-row span{color:var(--sub)}.health-row b{max-width:68%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.health-gauge-wrap{display:flex;align-items:center;gap:14px;padding:14px 16px 4px}.health-gauge{--pct:0;width:76px;height:76px;border-radius:50%;flex-shrink:0;background:conic-gradient(var(--accent2) calc(var(--pct)*1%),var(--accent) calc(var(--pct)*1%) calc(var(--pct)*1% + 1%),var(--line) calc(var(--pct)*1% + 1%));display:flex;align-items:center;justify-content:center;position:relative;box-shadow:0 0 18px rgba(55,214,255,.18)}.health-gauge:before{content:"";position:absolute;inset:7px;border-radius:50%;background:var(--panel)}.health-gauge b{position:relative;font-size:16px;font-weight:900}.health-gauge-label{font-size:9px;color:var(--sub2);position:relative;margin-top:20px}.health-gauge-sub{font-size:11px;font-weight:800;color:var(--good)}.health-gauge-sub small{display:block;font-size:9px;color:var(--sub2);font-weight:400;margin-top:2px}.mono{direction:ltr;text-align:left}.mini-panel .panel-head .badge{font-size:8px}.inbound-head{align-items:center}@media(max-width:1050px){.resource-grid{grid-template-columns:repeat(2,1fr)}.traffic-layout{grid-template-columns:1fr}.bottom-grid{grid-template-columns:1fr}}@media(max-width:560px){.resource-grid{grid-template-columns:1fr}.traffic-foot{grid-template-columns:1fr;gap:10px}.big-chart{height:190px}}

.client-manager{display:flex;flex-direction:column;gap:12px}.client-hero{display:flex;justify-content:space-between;gap:12px;padding:14px;border:1px solid var(--line);border-radius:14px;background:linear-gradient(135deg,rgba(var(--accent-rgb),.12),rgba(57,214,255,.04))}.client-hero b{display:block;font-size:13px}.client-hero small{display:block;color:var(--sub);font-size:10px;line-height:1.8;margin-top:4px}.client-create{padding:14px;border:1px solid var(--line);border-radius:14px;background:var(--panel2)}.client-list{display:flex;flex-direction:column;gap:8px}.client-row{display:flex;align-items:center;gap:10px;padding:11px;border:1px solid var(--line);border-radius:13px;background:rgba(255,255,255,.018)}.client-avatar{width:38px;height:38px;display:grid;place-items:center;border-radius:11px;background:rgba(var(--accent-rgb),.12);color:var(--accent);font-size:17px}.client-main{flex:1;min-width:0}.client-main b{display:block;font-size:11px}.client-main small{display:block;color:var(--sub2);font-size:8px;margin-top:3px;overflow:hidden;text-overflow:ellipsis}.client-tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}.client-tags span{font-size:8px;color:var(--sub);padding:4px 6px;border:1px solid var(--line);border-radius:7px}.client-actions{display:flex;gap:5px}.empty-client{padding:24px;text-align:center;color:var(--sub2);font-size:10px}.danger-note{border-color:rgba(239,68,68,.3)!important}
.pro-diagnostics{overflow:hidden}.diag-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:14px}.diag-item{border:1px solid var(--line);border-radius:13px;padding:12px;background:rgba(255,255,255,.018)}.diag-item small,.diag-item span{display:block;color:var(--sub2);font-size:9px}.diag-item b{display:block;font-size:18px;margin:5px 0}.diag-empty{grid-column:1/-1;padding:22px;text-align:center;color:var(--sub2)}@media(max-width:900px){.diag-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:520px){.diag-grid{grid-template-columns:1fr}}

/* ===== VodiWalker neon-glass theme (lightweight: no backdrop-filter, no infinite animations) ===== */
:root:not([data-theme="light"]){--bg:#060714;--panel:#0b0c22;--panel2:#10122e;--line:rgba(var(--accent-rgb),.28);--line2:rgba(var(--accent-rgb),.45);--accent:#a855f7;--accent2:#22d3ee;--accent-d:#6d28d9;--text:#f1eeff;--sub:#9a94c4;--sub2:#6b6699}
:root:not([data-theme="light"]) body,:root:not([data-theme="light"]) html{background:radial-gradient(60% 40% at 80% 0%,rgba(124,58,237,.28),transparent 70%),radial-gradient(50% 40% at 0% 100%,rgba(34,211,238,.10),transparent 70%),#060714}
:root:not([data-theme="light"]) .sidebar{background:linear-gradient(180deg,#0d0a26,#080a1c);border-inline-end:1px solid var(--line);box-shadow:0 0 30px rgba(124,58,237,.15)}
:root:not([data-theme="light"]) .tab{border:1px solid transparent;color:var(--sub);font-weight:600}
:root:not([data-theme="light"]) .tab:hover{background:rgba(var(--accent-rgb),.10);color:var(--text)}
:root:not([data-theme="light"]) .tab.on{color:#fff;background:linear-gradient(135deg,#a855f7,#6d28d9);border-color:rgba(255,255,255,.18);box-shadow:0 8px 24px -8px rgba(var(--accent-rgb),.8),inset 0 1px 0 rgba(255,255,255,.2)}
:root:not([data-theme="light"]) .topbar{background:rgba(8,9,26,.94);border-bottom:1px solid var(--line)}
:root:not([data-theme="light"]) .card,:root:not([data-theme="light"]) .resource-card,:root:not([data-theme="light"]) .stat-card{background:linear-gradient(160deg,rgba(124,58,237,.14),rgba(11,12,34,.92) 55%);border:1px solid var(--line);border-radius:18px;box-shadow:0 0 0 1px rgba(255,255,255,.02) inset,0 10px 30px -14px rgba(124,58,237,.55)}
:root:not([data-theme="light"]) .resource-card:nth-child(2){background:linear-gradient(160deg,rgba(34,211,238,.13),rgba(11,12,34,.92) 55%);border-color:rgba(34,211,238,.30)}
:root:not([data-theme="light"]) .resource-card:nth-child(4){background:linear-gradient(160deg,rgba(59,130,246,.15),rgba(11,12,34,.92) 55%);border-color:rgba(59,130,246,.32)}
:root:not([data-theme="light"]) .resource-card .rc-head b{font-size:26px;font-weight:800;color:#fff}
:root:not([data-theme="light"]) .resource-card .rc-head span i{display:inline-grid;place-items:center;width:34px;height:34px;border-radius:11px;background:rgba(var(--accent-rgb),.18);border:1px solid var(--line2);color:#d8b4fe}
:root:not([data-theme="light"]) .spark polyline{stroke:var(--accent);stroke-width:2;fill:none;filter:none}
:root:not([data-theme="light"]) #trafficChart polyline,:root:not([data-theme="light"]) #connChart polyline{stroke:#38bdf8;stroke-width:2.2;fill:none}
:root:not([data-theme="light"]) #trafficChart .area,:root:not([data-theme="light"]) #connChart .area{fill:rgba(56,189,248,.16);stroke:none}
:root:not([data-theme="light"]) .connection-number{font-size:52px;font-weight:900;color:#fff;text-align:center}
:root:not([data-theme="light"]) .btn.primary{background:linear-gradient(135deg,#a855f7,#6d28d9);border:0;box-shadow:0 8px 22px -8px rgba(var(--accent-rgb),.8)}
:root:not([data-theme="light"]) .bottom-grid .mini-panel:nth-child(1){border-color:rgba(34,197,94,.35);background:linear-gradient(160deg,rgba(34,197,94,.12),rgba(11,12,34,.92) 60%)}
:root:not([data-theme="light"]) .bottom-grid .mini-panel:nth-child(2){border-color:rgba(var(--accent-rgb),.4)}
:root:not([data-theme="light"]) .bottom-grid .mini-panel:nth-child(3){border-color:rgba(34,211,238,.35);background:linear-gradient(160deg,rgba(34,211,238,.10),rgba(11,12,34,.92) 60%)}
.page.on{animation:none}
.live-dot,.ib-live-tag i,.ib-status-dot.green{animation:none!important}
.card,.resource-card{contain:layout paint}
@media(max-width:820px){.resource-grid{grid-template-columns:repeat(2,1fr)}.resource-card .rc-head b{font-size:20px}.body-wrap{padding:14px 12px 70px}.card,.resource-card{box-shadow:none}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}

.ov-shell{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:14px;align-items:start}
.ov-main{min-width:0}.ov-rail{display:flex;flex-direction:column;gap:14px}
.rail-card .panel-head b{font-size:13px}.rail-dot{width:8px;height:8px;border-radius:50%;background:var(--good)}
.rail-item{display:flex;align-items:center;gap:10px;padding:9px 16px;border-bottom:1px solid var(--line);font-size:11px}
.rail-item div{flex:1;min-width:0}.rail-item b{display:block;font-size:11.5px}.rail-item small{color:var(--sub2);font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:block}
.rail-item em{font-style:normal;color:var(--sub2);font-size:10px}
.ri-ic{width:30px;height:30px;border-radius:9px;flex-shrink:0;background:rgba(34,197,94,.16);border:1px solid rgba(34,197,94,.4)}
.ri-ic.warn{background:rgba(245,158,11,.16);border-color:rgba(245,158,11,.4)}.ri-ic.bad{background:rgba(242,73,85,.16);border-color:rgba(242,73,85,.4)}
.rail-more{display:block;text-align:center;padding:10px;font-size:11px;color:var(--accent);cursor:pointer}
.qa-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:14px}
.qa{display:flex;flex-direction:column;align-items:center;gap:6px;padding:12px 6px;border-radius:12px;border:1px solid var(--line2);background:rgba(var(--accent-rgb),.08);color:var(--text);font-size:10.5px;cursor:pointer}
.qa i{font-size:20px;color:var(--accent-soft)}.qa:hover{background:rgba(var(--accent-rgb),.2)}
.rail-health{display:flex;align-items:center;gap:16px;padding:16px}
.rail-health .health-gauge{width:96px;height:96px}
.rail-legend{flex:1;display:flex;flex-direction:column;gap:7px;font-size:11px}
.rail-legend div{display:flex;align-items:center;gap:7px}.rail-legend i{width:8px;height:8px;border-radius:50%}.rail-legend b{margin-inline-start:auto}
.chart-tabs{display:flex;gap:6px;padding:12px 16px 0;flex-wrap:wrap}
.chart-tabs button{display:inline-flex;align-items:center;gap:6px;padding:7px 14px;border-radius:10px;border:1px solid var(--line);background:transparent;color:var(--sub);font-size:11.5px;cursor:pointer}
.chart-tabs button.on{background:linear-gradient(135deg,#a855f7,#6d28d9);color:#fff;border-color:transparent;box-shadow:0 6px 18px -6px rgba(var(--accent-rgb),.8)}
@media(max-width:1180px){.ov-shell{grid-template-columns:1fr}.ov-rail{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}}
@media(max-width:820px){.traffic-layout,.bottom-grid{grid-template-columns:1fr}}

/* top row = 5 cards like mock */
.resource-grid{grid-template-columns:repeat(5,minmax(0,1fr))!important}
.resource-grid>:nth-child(5){order:1}.resource-grid>:nth-child(4){order:2}.resource-grid>:nth-child(6){order:3}.resource-grid>:nth-child(3){order:4}.resource-grid>:nth-child(1){order:5}.resource-grid>:nth-child(2){display:none}
@media(max-width:1180px){.resource-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}.resource-grid>:nth-child(6){grid-column:auto}}
/* admins */
.adm-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:0 18px 14px}
.adm-strip>div{display:flex;align-items:center;gap:8px;padding:10px 12px;border-radius:12px;border:1px solid var(--line);background:rgba(var(--accent-rgb),.07)}
.adm-strip i{font-size:18px;color:var(--accent-soft)}.adm-strip b{font-size:18px}.adm-strip small{color:var(--sub);font-size:10.5px;margin-inline-start:auto}
.admin-grid{display:grid!important;grid-template-columns:repeat(auto-fill,minmax(310px,1fr))!important;gap:14px!important}
.adm-pro{display:flex;flex-direction:column;gap:12px;padding:16px!important;border-radius:18px!important;border:1px solid var(--line)!important;background:linear-gradient(160deg,rgba(124,58,237,.16),rgba(11,12,34,.94) 60%)!important}
.adm-pro.is-owner{border-color:rgba(245,158,11,.5)!important;background:linear-gradient(160deg,rgba(245,158,11,.14),rgba(11,12,34,.94) 60%)!important}
.adm-pro.is-inactive{opacity:.6}
.adm-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.adm-stats>div{padding:9px 6px;text-align:center;border-radius:11px;background:rgba(255,255,255,.03);border:1px solid var(--line)}
.adm-stats b{display:block;font-size:14px}.adm-stats small{color:var(--sub2);font-size:9.5px}
.adm-scope{padding:11px;border-radius:12px;border:1px dashed var(--line2);background:rgba(0,0,0,.18)}
.adm-scope-head{display:flex;justify-content:space-between;font-size:11px;margin-bottom:8px}.adm-scope-head em{font-style:normal;color:var(--sub)}
.adm-bar{height:6px;border-radius:6px;background:var(--line);overflow:hidden}.adm-bar i{display:block;height:100%;background:linear-gradient(90deg,#a855f7,#22d3ee)}.adm-bar i.full{background:linear-gradient(90deg,#22c58b,#22d3ee)}
.adm-ibs{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.adm-ib{display:inline-flex;align-items:center;gap:5px;padding:4px 9px;border-radius:8px;font-size:10.5px;background:rgba(var(--accent-rgb),.14);border:1px solid var(--line2);max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.adm-ib.all{background:rgba(34,197,139,.14);border-color:rgba(34,197,139,.4);color:#5eead4}.adm-ib.more{background:transparent}.adm-ib.none{color:var(--bad)}
.adm-perms summary{cursor:pointer;font-size:11px;color:var(--sub)}.adm-perms .admin-perm-row{margin-top:8px}
@media(max-width:820px){.adm-strip{grid-template-columns:1fr}}
</style>
<style id="vw-pro">
/* ===================================================================
   VW PRO LAYER — polish, depth, smoothness, mobile fixes.
   Variable-driven: follows accent/theme/appearance settings, and does
   NOT touch border-radius of shared components (Appearance Studio owns it).
   =================================================================== */
:root{
  --ease:cubic-bezier(.22,.7,.2,1);
  --ring:0 0 0 3px rgba(var(--accent-rgb),.28);
  --glass:rgba(15,20,32,.80);
  --soft-shadow:0 1px 0 rgba(255,255,255,.03) inset,0 10px 30px -16px rgba(0,0,0,.55);
}
[data-theme="light"]{
  --bg:#f3f5fa;--panel:#ffffff;--panel2:#f6f7fb;--line:#e3e7f0;--line2:#ccd3e2;
  --glass:rgba(255,255,255,.86);
  --soft-shadow:0 1px 2px rgba(25,32,60,.04),0 12px 28px -18px rgba(25,32,60,.22);
  --ring:0 0 0 3px rgba(124,58,237,.20);
}
@supports(color:color-mix(in srgb,red,blue)){
  :root{--ring:0 0 0 3px color-mix(in srgb,var(--accent) 30%,transparent)}
}

/* ---- base feel ---- */
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
::selection{background:rgba(var(--accent-rgb),.35);color:#fff}
*{-webkit-tap-highlight-color:transparent}
:focus{outline:none}
:focus-visible{outline:2px solid var(--accent2);outline-offset:2px}
input:focus-visible,select:focus-visible,textarea:focus-visible{outline:none}
::-webkit-scrollbar{width:9px;height:9px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--line2);border-radius:99px;border:2px solid transparent;background-clip:content-box}
::-webkit-scrollbar-thumb:hover{background:var(--sub2);background-clip:content-box;border:2px solid transparent}
*{scrollbar-width:thin;scrollbar-color:var(--line2) transparent}

/* mobile browsers: 100vh includes the address bar → content got cut off */
@supports(height:100dvh){#app,.sidebar,.main-col{height:100dvh}}

/* ---- shell ---- */
.main-col{
  background:
    radial-gradient(900px 420px at 88% -8%,rgba(var(--accent-rgb),.10),transparent 62%),
    radial-gradient(720px 360px at 4% 2%,rgba(55,214,255,.06),transparent 60%),
    var(--bg);
}
[data-theme="light"] .main-col{
  background:
    radial-gradient(900px 420px at 88% -8%,rgba(124,58,237,.07),transparent 62%),
    radial-gradient(720px 360px at 4% 2%,rgba(14,165,196,.06),transparent 60%),
    var(--bg);
}
.body-wrap{scroll-padding-top:12px;padding-bottom:calc(70px + env(safe-area-inset-bottom,0px))}

/* ---- sidebar ---- */
.sidebar{background:linear-gradient(180deg,var(--panel) 0%,var(--panel) 55%,var(--bg) 100%);box-shadow:0 0 40px -24px rgba(0,0,0,.6)}
.sidebar-brand{padding:18px 18px 16px}
.sidebar-brand img{transition:transform .35s var(--ease)}
.sidebar-brand:hover img{transform:rotate(-6deg) scale(1.06)}
.tabnav{gap:3px;padding:14px 12px;scrollbar-width:none}
.tabnav::-webkit-scrollbar{display:none}
.tab{transition:background-color .18s var(--ease),color .18s var(--ease),transform .18s var(--ease),box-shadow .18s var(--ease);cursor:pointer;user-select:none}
.tab:hover{transform:translateX(-2px)}
.tab:active{transform:scale(.98)}
.tab i{transition:transform .2s var(--ease),color .18s}
.tab:hover i{transform:scale(1.12)}
.tab.on{transform:none}
[data-theme="light"] .tab:hover{background:rgba(124,58,237,.06)}
[data-theme="light"] .tab.on{color:var(--accent-d);background:linear-gradient(90deg,rgba(124,58,237,.14),rgba(14,165,196,.06));box-shadow:inset 0 0 0 1px rgba(124,58,237,.25)}
[data-theme="light"] .tab .bd{background:rgba(124,58,237,.12);color:var(--accent-d)}
.user-chip{transition:border-color .18s,box-shadow .18s}
.user-chip:hover{border-color:var(--line2);box-shadow:var(--soft-shadow)}

/* ---- topbar ---- */
.topbar{background:var(--glass);-webkit-backdrop-filter:saturate(1.5) blur(14px);backdrop-filter:saturate(1.5) blur(14px)}
.page-title{letter-spacing:-.01em}
.icon-btn,.iconbtn,.hamburger{transition:transform .15s var(--ease),border-color .15s,color .15s,background-color .15s,box-shadow .15s;cursor:pointer}
.icon-btn:hover,.iconbtn:hover{transform:translateY(-1px);box-shadow:var(--soft-shadow)}
.icon-btn:active,.iconbtn:active,.hamburger:active{transform:scale(.94)}

/* ---- page transitions ---- */
.page.on{animation:vwPage .28s var(--ease) both}
@keyframes vwPage{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.pg-head h1{letter-spacing:-.02em}

/* ---- buttons ---- */
.btn{transition:transform .15s var(--ease),box-shadow .2s var(--ease),border-color .15s,background-color .15s,color .15s,filter .15s;cursor:pointer;user-select:none;line-height:1.3}
.btn:hover{transform:translateY(-1px);box-shadow:var(--soft-shadow)}
.btn:active{transform:translateY(0) scale(.98);box-shadow:none}
.btn.primary{background:linear-gradient(135deg,var(--accent),var(--accent-d));border-color:transparent;box-shadow:0 10px 24px -12px var(--accent)}
.btn.primary:hover{filter:brightness(1.08);box-shadow:0 14px 28px -12px var(--accent)}
.btn.danger:hover{background:rgba(242,73,85,.10);border-color:rgba(242,73,85,.5)}
.btn:disabled,.btn[disabled]{transform:none!important;box-shadow:none!important;filter:none}
.btn .spin{margin:0}

/* ---- inputs ---- */
.grp input,.grp select,.grp textarea,.search input,select.sel,.copy-row input{
  transition:border-color .15s,box-shadow .18s var(--ease),background-color .15s;
}
.grp input:hover,.grp select:hover,.grp textarea:hover,.search input:hover,select.sel:hover{border-color:var(--line2)}
.grp input:focus,.grp select:focus,.grp textarea:focus,.search input:focus,select.sel:focus,.copy-row input:focus{
  border-color:var(--accent);box-shadow:var(--ring);background:var(--panel);
}
.grp input[readonly],.copy-row input[readonly]{cursor:text;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12px;direction:ltr;text-align:left}
input[type=checkbox],input[type=radio]{accent-color:var(--accent)}

/* ---- cards & depth ---- */
.card,.stat-card,.resource-card,.mini-panel,.rail-card,.ibx,.ib-card,.appearance-card{
  box-shadow:var(--soft-shadow);
  transition:border-color .22s var(--ease),box-shadow .28s var(--ease),transform .28s var(--ease),background-color .2s;
}
.stat-card:hover,.resource-card:hover,.ibx:hover,.ib-card:hover{transform:translateY(-2px);border-color:var(--line2);box-shadow:var(--shadow-md)}
.card:hover{border-color:var(--line2)}
.ibx:hover{transform:translateY(-3px)}
.stat-card .sc-val,.kpi .num,.rc-head b,.connection-number{font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.ib-progress i,.bar-mini i{transition:width .6s var(--ease)}

/* ---- tables ---- */
thead th{font-size:11px;letter-spacing:.02em}
tbody tr{transition:background-color .15s}
tbody tr:hover{background:rgba(var(--accent-rgb),.06)}
[data-theme="light"] tbody tr:hover{background:rgba(124,58,237,.05)}
td,th{word-break:break-word}
td.mono,.mono{word-break:break-all}

/* ---- badges ---- */
.badge{letter-spacing:.01em;white-space:nowrap}

/* ---- drawer / overlay (real fade instead of display:none pop) ---- */
.overlay{display:block!important;opacity:0;pointer-events:none;background:rgba(4,6,12,.55);-webkit-backdrop-filter:blur(5px);backdrop-filter:blur(5px);transition:opacity .25s var(--ease)}
.overlay.show{opacity:1;pointer-events:auto}
.drawer{box-shadow:30px 0 80px -30px rgba(0,0,0,.6);will-change:transform;visibility:hidden;transition:transform .32s var(--ease),visibility 0s linear .32s}
.drawer.show{visibility:visible;transition:transform .32s var(--ease),visibility 0s}
.dr-head{background:linear-gradient(180deg,var(--panel2),var(--panel));position:sticky;top:0;z-index:2}
.dr-foot{background:var(--panel);box-shadow:0 -12px 24px -20px rgba(0,0,0,.5);padding-bottom:calc(16px + env(safe-area-inset-bottom,0px))}
.dr-body{scrollbar-gutter:stable;overscroll-behavior:contain}
.dr-head h3{letter-spacing:-.01em}

/* ---- builder forms: 2 columns again (global .ib-grid !important had collapsed them) ---- */
.drawer .ib-grid:not(#ibGrid){display:grid;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:10px}
.drawer .ib-grid.three:not(#ibGrid){grid-template-columns:repeat(3,minmax(0,1fr))!important}
.drawer .ib-grid .ib-full,.drawer .ib-full{grid-column:1/-1}
@media(max-width:600px){
  .drawer .ib-grid:not(#ibGrid),.drawer .ib-grid.three:not(#ibGrid){grid-template-columns:1fr!important}
}

/* ---- sub link drawer ---- */
.qr-box{width:176px;height:176px;padding:12px;border-radius:18px;box-shadow:0 18px 40px -20px rgba(0,0,0,.6),0 0 0 1px var(--line);background:#fff}
.qr-box img{display:block;image-rendering:pixelated}
.one-link-tag{display:inline-flex;align-items:center;gap:4px;margin-inline-start:8px;padding:2px 9px;border-radius:99px;font-size:10px;font-weight:800;color:var(--good);background:rgba(34,197,139,.12);border:1px solid rgba(34,197,139,.28);vertical-align:middle}
.copy-row{align-items:stretch}
.copy-row .copy-ico{width:42px;height:auto;flex:none;font-size:16px;color:var(--accent)}
.copy-row .copy-ico:hover{color:#fff;background:var(--accent);border-color:var(--accent)}
.hint i{margin-inline-end:5px;color:var(--accent2)}

/* ---- toasts ---- */
#toastWrap{bottom:calc(20px + env(safe-area-inset-bottom,0px));align-items:center;pointer-events:none;max-width:calc(100vw - 24px)}
.toast{pointer-events:auto;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);background:var(--glass);animation:vwToast .3s var(--ease) both;max-width:100%}
.toast span{overflow-wrap:anywhere}
@keyframes vwToast{from{opacity:0;transform:translateY(14px) scale(.96)}to{opacity:1;transform:none}}

/* ---- empty states ---- */
.empty,.ov-empty{color:var(--sub2)}
.empty i{opacity:.6}

/* ---- skeleton for first load ---- */
.resource-card .rc-sub:empty,.ov-empty{min-height:1em}

/* ---- mobile ---- */
@media(max-width:980px){
  .sidebar{transition:transform .3s var(--ease);box-shadow:-30px 0 70px -20px rgba(0,0,0,.65)}
  .sidebar-overlay{-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px)}
}
@media(max-width:700px){
  .topbar{padding:0 12px;gap:10px}
  .body-wrap{padding:16px 12px calc(84px + env(safe-area-inset-bottom,0px))}
  .pg-head{margin-bottom:14px}
  .pg-head h1{font-size:17px}
  .toolbar{width:100%}
  .toolbar .search{flex:1 1 100%}
  .search input{width:100%}
  .toolbar .btn{flex:1 1 auto;justify-content:center}
  .card{overflow-x:auto;-webkit-overflow-scrolling:touch}
  .drawer{width:100vw;max-width:100vw}
  /* 16px inputs stop iOS Safari from zooming the page on focus */
  input,select,textarea{font-size:16px!important}
  .stat-grid{grid-template-columns:repeat(2,1fr);gap:10px}
}

/* ---- motion preferences ---- */
.no-motion *,.no-motion *:before,.no-motion *:after{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}
@media(prefers-reduced-motion:reduce){
  *,*:before,*:after{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}
}


/* ===== VW PRO: performance + glow layer (loaded last) ===== */
:root{--vw-glow:1}
.topbar,.toast,.overlay,.sidebar-overlay,.ob-ov,.ov,.pill,.lang>button{-webkit-backdrop-filter:none!important;backdrop-filter:none!important}
.topbar{background:var(--panel)!important}
.overlay,.sidebar-overlay,.ob-ov,.ov{background:rgba(4,6,12,.74)!important}
.toast{background:var(--panel2)!important}
:root:not([data-theme="light"]) body,:root:not([data-theme="light"]) html{background:
 radial-gradient(60% 40% at 80% 0%,rgba(124,58,237,calc(.28*var(--vw-glow))),transparent 70%),
 radial-gradient(50% 40% at 0% 100%,rgba(34,211,238,calc(.10*var(--vw-glow))),transparent 70%),#060714;background-attachment:scroll}
:root:not([data-theme="light"]) .sidebar{box-shadow:0 0 calc(30px*var(--vw-glow)) rgba(124,58,237,calc(.15*var(--vw-glow)))}
.ibx:hover,.ib-card:hover,.stat-card:hover{transform:none!important}
.ibx,.ib-card{content-visibility:auto;contain-intrinsic-size:auto 280px}
.stat-card b,.ov-quickstats b,.ibx-stats b,.connection-number,.health-row b{font-variant-numeric:tabular-nums}
*{scrollbar-width:thin;scrollbar-color:rgba(148,130,255,.35) transparent}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:8px}
html.vw-paused *{animation-play-state:paused!important}
html.vw-fx-off *,html.vw-fx-off *:before,html.vw-fx-off *:after{animation:none!important;transition:none!important}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
.vwfx-btn{position:fixed;z-index:70;bottom:16px;inset-inline-start:16px;width:42px;height:42px;border-radius:14px;border:1px solid var(--line2);background:var(--panel2);color:var(--accent);font-size:20px;display:grid;place-items:center;cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.35)}
.vwfx-pop{position:fixed;z-index:70;bottom:66px;inset-inline-start:16px;width:min(280px,calc(100% - 32px));padding:16px;border-radius:16px;background:var(--panel);border:1px solid var(--line2);box-shadow:0 18px 50px rgba(0,0,0,.45);opacity:0;visibility:hidden;transform:translateY(6px);transition:opacity .16s,transform .16s,visibility .16s}
.vwfx-pop.open{opacity:1;visibility:visible;transform:none}
.vwfx-pop h4{margin:0 0 12px;font-size:12px;display:flex;justify-content:space-between}.vwfx-pop h4 b{color:var(--accent);direction:ltr}
.vwfx-pop label{display:block;font-size:10.5px;color:var(--sub2);margin:10px 0 7px;font-weight:700}
.vwfx-range{-webkit-appearance:none;appearance:none;width:100%;height:6px;border-radius:99px;outline:0;direction:ltr;background:linear-gradient(90deg,var(--accent) var(--p,66%),var(--line) var(--p,66%))}
.vwfx-range::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;background:#fff;border:3px solid var(--accent);cursor:pointer}
.vwfx-range::-moz-range-thumb{width:16px;height:16px;border-radius:50%;background:#fff;border:3px solid var(--accent);cursor:pointer}
.vwfx-row{display:flex;justify-content:space-between;align-items:center;font-size:11.5px;font-weight:700;margin-top:12px}
.vwfx-tg{width:40px;height:22px;border-radius:99px;border:1px solid var(--line);background:var(--line);position:relative;padding:0;cursor:pointer;transition:.2s}
.vwfx-tg:after{content:"";position:absolute;top:2px;inset-inline-start:2px;width:16px;height:16px;border-radius:50%;background:#fff;transition:.2s}
.vwfx-tg.on{background:var(--accent);border-color:transparent}.vwfx-tg.on:after{inset-inline-start:20px}

/* ===== VW PRO v2: global search + design polish (loaded last) ===== */
*,*::before,*::after{-webkit-backdrop-filter:none!important;backdrop-filter:none!important}
.page.on{animation:vwFadeOnly .14s ease-out both!important}
html.vw-fx-off .page.on{animation:none!important}
@keyframes vwFadeOnly{from{opacity:0}to{opacity:1}}
.body-wrap{overscroll-behavior:contain}
::selection{background:rgba(var(--accent-rgb),.35)}
.topbar{height:62px}
#pageTitleMain{font-size:15px;font-weight:800;letter-spacing:-.01em}
#pageTitleSub{font-size:11.5px;color:var(--sub2)}
.card,.resource-card{border-radius:16px}
.card,.resource-card{border:1px solid var(--line)}
table tbody tr{transition:background-color .12s}
table tbody tr:hover td{background:rgba(var(--accent-rgb),.045)}
.btn:active,.icon-btn:active{transform:scale(.97)}
.btn,.icon-btn,.tab,.cmdk-it,.cmdk-trigger{-webkit-tap-highlight-color:transparent}
.tab:hover:not(.on){background:rgba(var(--accent-rgb),.07);color:var(--text)}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--accent)!important;box-shadow:0 0 0 3px rgba(var(--accent-rgb),.18)}
.toast{border-radius:12px}
.cmdk-flash{animation:cmdkFlash 1.6s ease-out}
@keyframes cmdkFlash{0%{box-shadow:0 0 0 2px var(--accent),0 0 28px rgba(var(--accent-rgb),.45)}100%{box-shadow:0 0 0 0 transparent}}

/* ---- trigger ---- */
.cmdk-trigger{display:flex;align-items:center;gap:9px;height:36px;min-width:250px;padding:0 8px 0 12px;border-radius:10px;background:var(--panel2);border:1px solid var(--line);color:var(--sub);font:inherit;font-size:12.5px;cursor:pointer;transition:border-color .15s,color .15s}
.cmdk-trigger:hover{border-color:var(--line2);color:var(--text)}
.cmdk-trigger i{font-size:15px}
.cmdk-trigger span{flex:1;text-align:start;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cmdk-trigger kbd,.cmdk-foot kbd{font:600 10px/1 ui-monospace,SFMono-Regular,Menlo,monospace;padding:3px 6px;border-radius:6px;background:var(--bg);border:1px solid var(--line);color:var(--sub2);direction:ltr;margin-inline-end:3px}
@media(max-width:900px){.cmdk-trigger{min-width:36px;width:36px;padding:0;justify-content:center}.cmdk-trigger span,.cmdk-trigger kbd{display:none}}

/* ---- palette ---- */
.cmdk-ov{position:fixed;inset:0;z-index:200;background:rgba(4,6,12,.68);display:flex;align-items:flex-start;justify-content:center;padding:min(12vh,110px) 14px 14px;opacity:0;transition:opacity .12s}
.cmdk-ov[hidden]{display:none}
.cmdk-ov.show{opacity:1}
.cmdk{width:min(700px,100%);max-height:min(78vh,660px);display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--line2);border-radius:18px;box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 0 1px rgba(var(--accent-rgb),.14);overflow:hidden;transform:translateY(-6px) scale(.985);transition:transform .14s ease-out}
.cmdk-ov.show .cmdk{transform:none}
.cmdk-top{display:flex;align-items:center;gap:10px;padding:0 14px;height:56px;border-bottom:1px solid var(--line);flex-shrink:0}
.cmdk-top>i{font-size:18px;color:var(--accent)}
.cmdk-top input{flex:1;min-width:0;height:100%;background:transparent;border:0!important;box-shadow:none!important;outline:0;color:var(--text);font:inherit;font-size:15px}
.cmdk-top input::placeholder{color:var(--sub2)}
.cmdk-x{font:600 10px/1 ui-monospace,monospace;padding:5px 8px;border-radius:7px;background:var(--panel2);border:1px solid var(--line);color:var(--sub);cursor:pointer}
.cmdk-chips{display:flex;gap:6px;padding:10px 12px 8px;overflow-x:auto;flex-shrink:0;scrollbar-width:none}
.cmdk-chips::-webkit-scrollbar{display:none}
.cmdk-chips button{flex:none;padding:6px 12px;border-radius:99px;border:1px solid var(--line);background:transparent;color:var(--sub);font:inherit;font-size:11.5px;font-weight:700;cursor:pointer;transition:background-color .12s,color .12s,border-color .12s}
.cmdk-chips button:hover{color:var(--text);border-color:var(--line2)}
.cmdk-chips button.on{background:linear-gradient(135deg,var(--accent),var(--accent-d));border-color:transparent;color:#fff}
.cmdk-list{flex:1;overflow-y:auto;padding:4px 8px 8px;overscroll-behavior:contain;min-height:120px}
.cmdk-grp{padding:10px 10px 5px;font-size:10.5px;font-weight:800;color:var(--sub2);letter-spacing:.04em}
.cmdk-it{display:flex;align-items:center;gap:11px;padding:9px 10px;border-radius:12px;cursor:pointer;border:1px solid transparent}
.cmdk-it.on{background:linear-gradient(90deg,rgba(var(--accent-rgb),.18),rgba(55,214,255,.07));border-color:rgba(var(--accent-rgb),.35)}
.cmdk-ic{flex:none;width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:var(--panel2);border:1px solid var(--line);color:var(--accent);font-size:16px}
.cmdk-it.on .cmdk-ic{background:rgba(var(--accent-rgb),.16);border-color:rgba(var(--accent-rgb),.4)}
.cmdk-tx{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.cmdk-tx b{font-size:13px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cmdk-tx small{font-size:11px;color:var(--sub);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;unicode-bidi:plaintext}
.cmdk-tx mark{background:rgba(245,165,36,.28);color:inherit;border-radius:3px;padding:0 1px}
.cmdk-meta{flex:none;font-size:11px;color:var(--sub);font-variant-numeric:tabular-nums;direction:ltr}
.cmdk-bd{flex:none;font-size:10px;font-weight:800;padding:3px 9px;border-radius:99px;background:rgba(135,146,168,.14);color:var(--sub);white-space:nowrap}
.cmdk-bd.on{background:rgba(34,197,139,.14);color:var(--good)}
.cmdk-bd.idle{background:rgba(55,214,255,.12);color:var(--accent2)}
.cmdk-bd.bad{background:rgba(242,73,85,.14);color:var(--bad)}
.cmdk-ty{flex:none;font-size:10px;font-weight:700;color:var(--sub2);min-width:52px;text-align:end}
.cmdk-empty{display:flex;flex-direction:column;align-items:center;gap:6px;padding:34px 12px;color:var(--sub);text-align:center}
.cmdk-empty i{font-size:28px;color:var(--sub2)}
.cmdk-empty small{font-size:11.5px;color:var(--sub2)}
.cmdk-foot{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:9px 14px;border-top:1px solid var(--line);font-size:11px;color:var(--sub2);flex-shrink:0}
.cmdk-count{margin-inline-start:auto;font-variant-numeric:tabular-nums}
@media(max-width:700px){.cmdk-ov{padding-top:7vh}.cmdk{max-height:84vh}.cmdk-ty,.cmdk-foot span:not(.cmdk-count){display:none}.cmdk-foot span.cmdk-count{margin:0}}
html.vw-fx-off .cmdk-ov,html.vw-fx-off .cmdk{transition:none!important;transform:none!important}

/* ===== Accent-consistent interaction states =====
   Whatever accent colour the user picks (e.g. red) is used for hover, focus,
   pressed and focus-ring states. Previously several of these fell back to the
   default cyan/purple, so a tapped red button flashed blue. */
:focus-visible{outline:2px solid var(--accent)!important;outline-offset:2px}
.btn,.icon-btn,.iconbtn,.tab,.theme-pill,.accent-pill,.chip,.switch,button{-webkit-tap-highlight-color:transparent}
.btn:focus,.btn:focus-visible,.icon-btn:focus-visible,.iconbtn:focus-visible,.theme-pill:focus-visible,.accent-pill:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.btn:hover:not(.primary):not(.danger),.btn:active:not(.primary):not(.danger),.btn:focus:not(.primary):not(.danger){border-color:var(--accent);background-color:rgba(var(--accent-rgb),.10)}
.btn.primary,.btn.primary:hover,.btn.primary:active,.btn.primary:focus,.btn.primary:focus-visible{background:linear-gradient(135deg,var(--accent),var(--accent-d))!important;border-color:transparent!important;color:#fff}
.btn.primary:active{filter:brightness(.94)}
.btn.primary:focus-visible{box-shadow:0 0 0 3px rgba(var(--accent-rgb),.35)}
input:focus,select:focus,textarea:focus{border-color:var(--accent)!important;box-shadow:0 0 0 3px rgba(var(--accent-rgb),.22)!important}
::selection{background:rgba(var(--accent-rgb),.35)}
input[type=checkbox],input[type=radio],input[type=range]{accent-color:var(--accent)}
</style>
</head>
<body>
<script>(function(){
  // نکته (رفع باگ): قبلاً این اسکریپت اولیه از کلید localStorage جداگانه‌ای
  // به‌نام «vw_theme» می‌خواند که هیچ‌جای برنامه هرگز در آن چیزی نمی‌نوشت
  // (تنظیمات واقعی همیشه زیر کلید «vw_appearance» ذخیره می‌شود)، پس همیشه
  // مقدار پیش‌فرض «dark» اعمال می‌شد و باعث یک فلاش کوتاهِ پوسته‌ی اشتباه
  // در بارگذاری اولیه‌ی صفحه می‌شد، تا وقتی اسکریپت اصلی اجرا شود.
  try{
    var raw = localStorage.getItem('vw_appearance');
    var pref = raw ? (JSON.parse(raw).theme || 'dark') : 'dark';
    var resolved = pref === 'system'
      ? (matchMedia('(prefers-color-scheme:light)').matches ? 'light' : 'dark')
      : pref;
    document.documentElement.setAttribute('data-theme', resolved);
  }catch(e){ document.documentElement.setAttribute('data-theme','dark'); }
})();</script>
<div id="app">
  <div class="sidebar-overlay" onclick="toggleSidebar()"></div>
  <div class="sidebar">
    <div class="sidebar-brand"><img src="data:image/png;base64,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"><div><span data-i18n="brand">VodiWalker</span><small>Control Center</small></div></div>
    <div class="tabnav" id="tabnav">
      <div class="tab on" data-pg="overview"><i class="ti ti-layout-dashboard"></i><span data-i18n="nav_overview">داشبورد</span></div>
      <div class="tab" data-pg="news"><i class="ti ti-speakerphone"></i><span data-i18n="nav_news">اخبار</span></div>
      <div class="tab" data-pg="links"><i class="ti ti-network"></i><span data-i18n="nav_links">اینباندها</span><span class="bd" id="nb-links">0</span></div>
      <div class="tab" data-pg="clientmgr"><i class="ti ti-user-plus"></i><span data-i18n="nav_clientmgr">ساخت کلاینت</span></div>
      <div class="tab" data-pg="categories"><i class="ti ti-category"></i><span data-i18n="nav_categories">دسته‌بندی‌ها</span></div>
      <div class="tab" data-pg="subgroups"><i class="ti ti-folders"></i><span data-i18n="nav_subgroups">گروه‌های ساب</span><span class="bd" id="nb-subs">0</span></div>
      <div class="tab" data-pg="reports"><i class="ti ti-chart-histogram"></i><span data-i18n="nav_reports">گزارش‌ها</span></div>
      <div class="tab" data-pg="nodes"><i class="ti ti-server-cog"></i><span data-i18n="nav_nodes">نودها</span></div>
      <div class="tab" data-pg="admins"><i class="ti ti-users-group"></i><span data-i18n="nav_admins">ادمین‌ها</span></div>
      <div class="tab" data-pg="activity"><i class="ti ti-history"></i><span data-i18n="nav_activity">فعالیت‌ها</span></div>
      <div class="tab" data-pg="messages"><i class="ti ti-bell-ringing"></i><span data-i18n="nav_messages">پیام‌ها</span><span class="bd danger-bd" id="nb-errors">0</span></div>
      <div class="tab" data-pg="settings"><i class="ti ti-settings"></i><span data-i18n="nav_settings">تنظیمات</span></div>
    </div>
    <div class="sidebar-foot">
      <div class="lang-mini">
        <button id="dashLangFa" class="on" onclick="setDashLang('fa')">فا</button>
        <button id="dashLangEn" onclick="setDashLang('en')">EN</button>
      </div>
      <div class="user-chip" id="userChip"><div class="av">V</div><div><span id="userName">...</span><span class="role-tag" id="userRoleTag"></span></div></div>
    </div>
  </div>

  <div class="main-col">
  <div class="topbar">
    <button class="hamburger" onclick="toggleSidebar()"><i class="ti ti-menu-2"></i></button>
    <div class="page-title"><span id="pageTitleMain" data-i18n="nav_overview">داشبورد</span><span id="pageTitleSub" data-i18n="pt_overview">وضعیت لحظه‌ای سرویس، کانفیگ‌ها و ربات فروش</span></div>
    <div class="top-right">
      <button class="cmdk-trigger" id="cmdkTrigger" type="button" onclick="cmdkOpen()" aria-label="جستجوی سراسری" title="جستجوی سراسری (Ctrl+K)"><i class="ti ti-search"></i><span>جستجو در پنل…</span><kbd>Ctrl K</kbd></button>
      <button class="nd-switch" id="nodeSwitchBtn" style="display:none" onclick="openNodeSwitcher()" title="انتخاب پنل/نود برای مدیریت"></button>
      <button class="icon-btn" id="themeToggle" onclick="toggleTheme()" title="تغییر پوسته"><i class="ti ti-moon"></i></button>
      <a class="icon-btn" href="/logout" title="خروج"><i class="ti ti-logout"></i></a>
    </div>
  </div>

  <div class="nd-banner" id="nodeBanner" style="display:none"></div>
  <div class="body-wrap">

    <!-- OVERVIEW -->
    <div class="page on" id="pg-overview">
      <div class="pg-head"><div><div class="eyebrow"><span class="live-dot"></span> مانیتور زنده سیستم</div><h1>مرکز کنترل VodiWalker</h1><p>نمای لحظه‌ای منابع سرور، ترافیک و اتصال‌ها.</p></div>
        <div class="toolbar"><button class="btn" onclick="refreshOverview()"><i class="ti ti-refresh"></i>بروزرسانی</button><button class="btn primary" onclick="gotoPage('links')"><i class="ti ti-network"></i>اینباندها</button></div></div>
      <div class="ov-shell"><div class="ov-main">
      <div class="ib-quickstats ov-quickstats" id="ovBizStats"></div>
      <div class="resource-grid" id="resourceGrid">
        <div class="resource-card"><div class="rc-head"><span><i class="ti ti-cpu"></i> پردازنده</span><b id="cpuVal">—</b></div><div class="rc-sub" id="cpuSub">در حال دریافت...</div><svg class="spark" id="cpuSpark" viewBox="0 0 240 46" preserveAspectRatio="none"></svg></div>
        <div class="resource-card"><div class="rc-head"><span><i class="ti ti-device-ram"></i> حافظه RAM</span><b id="ramVal">—</b></div><div class="rc-sub" id="ramSub">—</div><svg class="spark" id="ramSpark" viewBox="0 0 240 46" preserveAspectRatio="none"></svg></div>
        <div class="resource-card"><div class="rc-head"><span><i class="ti ti-bolt"></i> سواپ</span><b id="swapVal">—</b></div><div class="rc-sub" id="swapSub">—</div><svg class="spark" id="swapSpark" viewBox="0 0 240 46" preserveAspectRatio="none"></svg></div>
        <div class="resource-card"><div class="rc-head"><span><i class="ti ti-database"></i> فضای ذخیره‌سازی</span><b id="storageVal">—</b></div><div class="rc-sub" id="storageSub">—</div><svg class="spark" id="storageSpark" viewBox="0 0 240 46" preserveAspectRatio="none"></svg></div>
        <div class="resource-card"><div class="rc-head"><span><i class="ti ti-server"></i> اینباندها</span><b id="instVal">0</b></div><div class="rc-sub" id="instSub">فعال: 0 | متوقف: 0</div><svg class="spark" id="instSpark" viewBox="0 0 240 46" preserveAspectRatio="none"></svg></div>
        <div class="resource-card"><div class="rc-head"><span><i class="ti ti-world"></i> شبکه</span><b id="netVal">0</b></div><div class="rc-sub" id="netSub">↑ 0 · ↓ 0</div><svg class="spark" id="netSpark" viewBox="0 0 240 46" preserveAspectRatio="none"></svg></div>
      </div>
      <div class="traffic-layout">
        <div class="card traffic-card"><div class="panel-head"><div><b>سرعت کلی</b><small id="speedMeta">پهنای باند لحظه‌ای</small></div><div class="traffic-legend"><span>↑ <b id="txRate">0 B/s</b></span><span>↓ <b id="rxRate">0 B/s</b></span></div></div><div class="chart-tabs" id="chartTabs"><button class="on" data-k="net" onclick="setChartTab('net')"><i class="ti ti-activity"></i> شبکه</button><button data-k="cpu" onclick="setChartTab('cpu')"><i class="ti ti-cpu"></i> پردازنده</button><button data-k="mem" onclick="setChartTab('mem')"><i class="ti ti-device-ram"></i> حافظه</button><button data-k="disk" onclick="setChartTab('disk')"><i class="ti ti-database"></i> دیسک</button></div><div class="big-chart"><svg id="trafficChart" viewBox="0 0 900 260" preserveAspectRatio="none"></svg></div><div class="traffic-foot"><div><small>ارسال‌شده</small><b id="sentTotal">0 B</b></div><div><small>دریافت‌شده</small><b id="recvTotal">0 B</b></div><div><small>نرخ لحظه‌ای</small><b id="liveRate">↑ 0 B/s ↓ 0 B/s</b></div></div></div>
        <div class="card connection-card"><div class="panel-head"><div><b>وضعیت اتصال‌ها</b><small>سوکت‌های باز</small></div><i class="ti ti-plug-connected"></i></div><div class="connection-number" id="connVal">0</div><div class="connection-label">اتصال فعال</div><svg class="conn-chart" id="connChart" viewBox="0 0 340 150" preserveAspectRatio="none"></svg><div class="conn-foot"><span>درخواست‌ها <b id="reqVal">0</b></span><span>خطاها <b id="errVal">0</b></span></div></div>
      </div>
      <div class="bottom-grid">
        <div class="card mini-panel"><div class="panel-head"><div><b>سلامت سرویس</b><small>وضعیت اجرا</small></div><span class="badge green">آنلاین</span></div><div class="health-gauge-wrap"><div class="health-gauge" id="healthGauge"><b id="healthPct">—</b></div><div><div class="health-gauge-sub" id="healthLabel">در حال بررسی<small>سلامت کلی سیستم</small></div></div></div><div class="health-row"><span>مدت روشن بودن</span><b id="uptimeVal">—</b></div><div class="health-row"><span>هسته‌های پردازنده</span><b id="coresVal">—</b></div><div class="health-row"><span>رم مصرفی پنل</span><b id="procRamVal">—</b></div></div>
        <div class="card mini-panel"><div class="panel-head"><div><b>سرویس ربات</b><small>فروش و مدیریت</small></div><span id="ovBotStatus" class="badge gray">در حال بررسی</span></div><div class="health-row"><span>ربات تلگرام</span><b id="botStateText">—</b></div><div class="health-row"><span>آدرس عمومی پنل</span><b class="mono" id="ovBaseUrl">—</b></div></div>
        <div class="card mini-panel"><div class="panel-head"><div><b>شبکه و ترافیک</b><small>بار سرور و مصرف کل</small></div><i class="ti ti-world"></i></div><div class="health-row"><span>بار سیستم</span><b id="loadVal">—</b></div><div class="health-row"><span>مجموع کل ترافیک</span><b id="trafficTotalVal">0 B</b></div></div>
      </div>
      <div class="card mini-panel" style="margin-top:14px"><div class="panel-head"><div><b>پرمصرف‌ترین کانفیگ‌ها</b><small>پرمصرف‌ترین کانفیگ‌های ۷ روز اخیر</small></div><i class="ti ti-trending-up"></i></div><div id="ovTopLinks" class="ov-toplinks"></div></div>
      </div>
      <aside class="ov-rail">
        <div class="card rail-card"><div class="panel-head"><div><b><i class="ti ti-activity-heartbeat"></i> فعالیت لحظه‌ای</b></div><span class="rail-dot"></span></div><div id="railActivity" class="rail-list"><div class="ov-empty">…</div></div><a class="rail-more" onclick="gotoPage('activity')">مشاهده همه ›</a></div>
        <div class="card rail-card"><div class="panel-head"><div><b>دسترسی سریع</b></div></div><div class="qa-grid">
          <button class="qa" onclick="openLinkDrawer()"><i class="ti ti-plus"></i><span>ساخت کانفیگ</span></button>
          <button class="qa" onclick="openNodeDrawer()"><i class="ti ti-server-cog"></i><span>افزودن نود</span></button>
          <button class="qa" onclick="gotoPage('nodes')"><i class="ti ti-world"></i><span>نودها</span></button>
          <button class="qa" onclick="gotoPage('settings')"><i class="ti ti-shield-lock"></i><span>تنظیمات</span></button></div></div>
        <div class="card rail-card"><div class="panel-head"><div><b>Server Health</b></div></div><div class="rail-health"><div class="health-gauge" id="railGauge"><b id="railPct">—</b></div>
          <div class="rail-legend"><div><i style="background:#a855f7"></i>CPU<b id="rlCpu">—</b></div><div><i style="background:#3b82f6"></i>Memory<b id="rlRam">—</b></div><div><i style="background:#f59e0b"></i>Disk<b id="rlDisk">—</b></div><div><i style="background:#22d3ee"></i>Swap<b id="rlSwap">—</b></div></div></div></div>
      </aside></div>
    </div>

    <!-- LINKS -->
    <div class="page" id="pg-links">
      <div class="pg-head inbound-head"><div><div class="eyebrow"><span class="live-dot"></span> VODIWALKER CORE · <span id="ibLiveTag">LIVE</span></div><h1>اینباندها</h1><p>مرکز مدیریت اینباند، ساخت کلاینت و کنترل دسترسی؛ با پایش زنده هر ۵ ثانیه.</p></div>
        <div class="toolbar">
          <div class="search"><input id="linkSearch" placeholder="جستجوی اینباند / UUID..." oninput="vwDebounce('ls',renderLinks,120)"><i class="ti ti-search"></i></div>
          <select class="sel" id="linkFilterCat" onchange="renderLinks()"><option value="">همه دسته‌ها</option></select>
          <span id="ibUpdatedAt" style="font-size:9px;color:var(--sub2);align-self:center;white-space:nowrap">—</span>
          <button class="btn" id="ibRefreshBtn" onclick="refreshAllInbounds()"><i class="ti ti-refresh" id="ibRefreshIcon"></i>بروزرسانی همه</button>
          <button class="btn" onclick="openOutboundManager()" title="مدیریت پراکسی‌های SOCKS5 (خروجی)"><i class="ti ti-route"></i>اوتباند</button>
          <button class="btn" onclick="openAutoLink()"><i class="ti ti-bolt"></i>ساخت سریع</button>
          <button class="btn primary btn-inbound" onclick="openLinkDrawer()"><i class="ti ti-plus"></i>اینباند جدید</button>
        </div>
      </div>
      <div class="ib-quickstats" id="ibQuickStats"></div>
      <div class="ibx-filterbar">
        <div class="ibx-chips" id="ibChips">
          <button class="ibx-chip on" data-f="all" onclick="setIbFilter('all')">همه <em>0</em></button>
          <button class="ibx-chip" data-f="active" onclick="setIbFilter('active')">فعال <em>0</em></button>
          <button class="ibx-chip" data-f="online" onclick="setIbFilter('online')">آنلاین <em>0</em></button>
          <button class="ibx-chip" data-f="live" onclick="setIbFilter('live')">LIVE <em>0</em></button>
          <button class="ibx-chip" data-f="off" onclick="setIbFilter('off')">غیرفعال <em>0</em></button>
          <button class="ibx-chip" data-f="expired" onclick="setIbFilter('expired')">منقضی <em>0</em></button>
        </div>
        <select class="sel" id="ibSort" onchange="setIbSort(this.value)">
          <option value="new">جدیدترین</option><option value="usage">پرمصرف‌ترین</option><option value="exp">نزدیک انقضا</option><option value="name">نام (الفبا)</option>
        </select>
      </div>
      <div class="ib-listbar">
        <label class="ib-selectall"><input type="checkbox" id="ibSelAll" onchange="toggleAllLinks(this.checked)"><span>انتخاب همه</span></label>
        <span class="ib-count" id="ibCountLabel">0 اینباند</span>
      </div>
      <div class="ib-bulkbar" id="ibBulkBar" style="display:none">
        <span><b id="ibSelCount">0</b> مورد انتخاب شده</span>
        <div class="ib-bulkactions">
          <button class="btn sm" onclick="bulkOutbound()"><i class="ti ti-route"></i>خروجی (Outbound)</button>
          <button class="btn sm" onclick="bulkToggleLinks(true)"><i class="ti ti-power"></i>فعال‌سازی</button>
          <button class="btn sm" onclick="bulkToggleLinks(false)"><i class="ti ti-power"></i>غیرفعال‌سازی</button>
          <button class="btn sm" style="color:var(--bad)" onclick="bulkDeleteLinks()"><i class="ti ti-trash"></i>حذف</button>
        </div>
      </div>
      <div class="ib-grid" id="ibGrid"></div>
      <div class="empty" id="linksEmpty" style="display:none"><i class="ti ti-inbox"></i>کانفیگی یافت نشد</div>
    </div>

    <!-- CLIENT MANAGER (بخش جدای ساخت کلاینت از روی اینباند) -->
    <div class="page" id="pg-clientmgr">
      <div class="pg-head"><div><div class="eyebrow"><span class="live-dot"></span> VODIWALKER · CLIENT MANAGER</div><h1>ساخت کلاینت</h1><p>یک اینباند را انتخاب کن و از روی همان کلاینت‌های واقعی (زیرمجموعه) بساز؛ بدون نیاز به رفتن به صفحه اینباندها.</p></div>
        <div class="toolbar"><button class="btn" onclick="loadClientManager()"><i class="ti ti-refresh"></i>بروزرسانی</button></div>
      </div>
      <div class="card" style="padding:18px;margin-bottom:14px">
        <div class="grp"><label>انتخاب اینباند</label>
          <select class="sel" id="cmInboundSelect" style="width:100%" onchange="loadClientManagerClients(this.value)"><option value="">— انتخاب کنید —</option></select>
        </div>
        <div id="cmInboundInfo"></div>
      </div>
      <div id="cmBody"></div>
    </div>

    <!-- CATEGORIES -->
    <div class="page" id="pg-categories">
      <div class="pg-head"><div><h1>دسته‌بندی‌ها</h1><p>پیش‌فرض‌های حجم، انقضا و محدودیت برای گروه‌های کانفیگ</p></div>
        <div class="toolbar"><button class="btn primary" onclick="openCategoryDrawer()"><i class="ti ti-plus"></i>دسته جدید</button></div>
      </div>
      <div class="card"><table><thead><tr><th>نام</th><th>حجم پیش‌فرض</th><th>انقضا (روز)</th><th>محدودیت IP</th><th></th></tr></thead><tbody id="catsBody"></tbody></table></div>
    </div>

    <!-- SUBGROUPS -->
    <div class="page" id="pg-subgroups">
      <div class="pg-head"><div><h1>گروه‌های ساب</h1><p>ترکیب چند کانفیگ در یک لینک اشتراک واحد</p></div>
        <div class="toolbar"><button class="btn primary" onclick="openSubGroupDrawer()"><i class="ti ti-plus"></i>گروه جدید</button></div>
      </div>
      <div class="card"><table><thead><tr><th>نام گروه</th><th>تعداد کانفیگ</th><th>لینک عمومی</th><th></th></tr></thead><tbody id="subsBody"></tbody></table></div>
    </div>

    <!-- REPORTS -->
    <div class="page" id="pg-reports">
      <div class="pg-head"><div><h1>گزارش‌ها</h1><p>خلاصه‌ی عملکرد کانفیگ‌ها</p></div>
        <div class="toolbar">
          <select class="sel" id="repDays" onchange="loadReports()"><option value="7">۷ روز اخیر</option><option value="14" selected>۱۴ روز اخیر</option><option value="30">۳۰ روز اخیر</option></select>
          <a class="btn" href="/api/reports/export.csv"><i class="ti ti-download"></i>خروجی CSV</a>
        </div>
      </div>
      <div class="stat-grid" id="repStats"></div>
      <div class="card">
        <div style="padding:16px 18px;border-bottom:1px solid var(--line)"><b style="font-size:13px">پرمصرف‌ترین کانفیگ‌ها</b></div>
        <table><thead><tr><th>برچسب</th><th>پروتکل</th><th>مصرف</th></tr></thead><tbody id="repTopBody"></tbody></table>
      </div>
    </div>

    <!-- ADMINS -->
    <div class="page" id="pg-admins">
      <div class="pg-head"><div><div class="eyebrow"><span class="live-dot"></span> VODIWALKER · مدیریت حساب</div><h1>مدیریت حساب‌ها</h1><p>اینجا همه حساب‌های مدیریتی پنل را مرتب و دقیق مدیریت می‌کنیم؛ از ساخت ادمین تا تعیین دسترسی و کنترل وضعیت حساب.</p></div>
        <div class="toolbar"><button class="btn" onclick="loadAdmins()"><i class="ti ti-refresh"></i>همگام‌سازی</button><button class="btn primary" onclick="openAdminDrawer()"><i class="ti ti-user-plus"></i>ایجاد حساب مدیریتی</button></div>
      </div>
      <div class="admins-hero">
        <div class="access-command-copy"><div class="command-badge"><i class="ti ti-shield-lock"></i> مدیریت حساب‌ها</div><h2>مدیریت کامل ادمین‌ها</h2><p>حساب اصلی پنل دسترسی کامل دارد و برای هر ادمین می‌توان دسترسی‌های موردنیاز را جداگانه تعیین کرد. وضعیت هر حساب و آخرین ورود نیز از همین بخش قابل بررسی است.</p><div class="command-points"><span><i class="ti ti-check"></i> تفکیک دسترسی</span><span><i class="ti ti-check"></i> ثبت آخرین ورود</span><span><i class="ti ti-check"></i> امنیت حساب‌ها</span></div></div>
        <div class="admins-summary" id="adminsSummary"><div class="sum"><b id="adminTotal">—</b><small>حساب مدیریتی</small></div><div class="sum"><b id="adminActive">—</b><small>حساب فعال</small></div><div class="sum"><b id="adminOwner">1</b><small>مالک پنل</small></div></div>
      </div>
      <div class="card admin-directory" id="adminReqCard" style="margin-bottom:14px;display:none"><div class="panel-head"><div><b>درخواست‌های ثبت‌نام ادمینی</b><small>افرادی که از صفحه ورود درخواست همکاری داده‌اند؛ بررسی کن و تصمیم بگیر.</small></div><span class="command-badge" id="adminReqBadge">۰ درخواست</span></div><div id="adminReqBody" style="padding:14px 18px"></div></div>
      <div class="card admin-directory"><div class="panel-head"><div><b>فهرست ادمین‌ها</b><small>وضعیت، دسترسی و فعالیت هر ادمین را از یکجا بررسی و مدیریت کن.</small></div><span class="directory-live"><i></i> کنترل فعال</span></div><div class="adm-strip"><div><i class="ti ti-lock"></i><b id="adScoped">0</b><small>محدود به اینباند</small></div><div><i class="ti ti-lock-open"></i><b id="adFull">0</b><small>دسترسی به همه</small></div><div><i class="ti ti-network"></i><b id="adInb">0</b><small>کل اینباندها</small></div></div><div class="admin-grid" id="adminsBody"></div></div>
    </div>

    <!-- NODES -->
    <div class="page" id="pg-nodes">
      <div class="pg-head"><div><div class="eyebrow"><span class="live-dot"></span> VODIWALKER · NODES</div><h1>نودها</h1><p>چند پنل VodiWalker را به هم وصل کن و همه را از یک پنل مدیریت کن.</p></div>
        <div class="toolbar"><button class="btn" onclick="checkAllNodes()"><i class="ti ti-refresh"></i>بررسی همه</button><button class="btn primary" onclick="openNodeDrawer()"><i class="ti ti-plus"></i>افزودن نود</button></div>
      </div>
      <div class="card" style="margin-bottom:14px"><div class="panel-head"><div><b><i class="ti ti-key"></i> توکن این پنل (وقتی این پنل «نود» است)</b><small>توکن را کپی کن و در پنل اصلی، بخش نودها، بچسبان</small></div></div><div style="padding:0 18px 18px" id="nodeTokenBody"></div></div>
      <div class="card"><div class="panel-head"><div><b>نودهای متصل به این پنل</b><small>وضعیت هر ۳۰ ثانیه به‌روز می‌شود · «مدیریت» کل پنل را روی همان نود اجرا می‌کند</small></div></div><div style="padding:0 18px 18px" id="nodesList"></div></div>
    </div>

    <!-- ACTIVITY -->
    <div class="page" id="pg-activity">
      <div class="pg-head"><div><h1>لاگ فعالیت‌ها</h1><p>۱۵۰ رویداد اخیر پنل</p></div>
        <div class="toolbar"><button class="btn" onclick="loadActivity()"><i class="ti ti-refresh"></i>بروزرسانی</button></div>
      </div>
      <div class="card"><table><thead><tr><th>زمان</th><th>نوع</th><th>پیام</th></tr></thead><tbody id="activityBody"></tbody></table></div>
    </div>

    <!-- NEWS -->
    <div class="page" id="pg-news">
      <div class="pg-head"><div><div class="eyebrow"><span class="live-dot"></span> NEWS &amp; UPDATES</div><h1 data-i18n="nav_news">اخبار</h1><p data-i18n="pt_news">کانال رسمی، اطلاع‌رسانی بروزرسانی‌ها و حمایت از پروژه</p></div></div>
      <div class="news-hero card">
        <div class="news-hero-icon"><i class="ti ti-brand-telegram"></i></div>
        <div class="news-hero-body">
          <h2 data-i18n="newsChannelTitle">کانال رسمی VodiWalker</h2>
          <p data-i18n="newsChannelDesc">برای اطلاع از بروزرسانی‌های پنل، اخبار مهم، تغییرات سرویس و راهنمایی‌های استفاده، حتماً عضو کانال رسمی ما در تلگرام شو. هر اتفاق تازه‌ای اول از همه اونجا اعلام می‌شه.</p>
          <a class="btn primary news-join-btn" href="https://t.me/vodiwalkervpn03" target="_blank" rel="noopener"><i class="ti ti-brand-telegram"></i><span data-i18n="newsJoinBtn">عضویت در کانال</span></a>
        </div>
      </div>
      <div class="news-hero card support-hero">
        <div class="news-hero-icon support-icon"><i class="ti ti-heart-filled"></i></div>
        <div class="news-hero-body">
          <h2 data-i18n="newsSupportTitle">این پنل با عشق ساخته شده ❤️</h2>
          <p data-i18n="newsSupportDesc">VodiWalker به‌صورت کاملاً رایگان و با علاقه‌ی شخصی ساخته و نگه‌داری می‌شه. اگه این پروژه بهت کمک کرده و دوست داشتی به ادامه‌ی راهش کمک کنی، می‌تونی به دلخواه و اختیاری حمایت کنی؛ این حمایت هیچ تعهد یا امتیاز خاصی ایجاد نمی‌کنه.</p>
          <div class="support-card-row">
            <div class="support-card-box">
              <span class="support-card-label" data-i18n="newsCardLabel">شماره کارت</span>
              <span class="support-card-number mono" id="supportCardNumber">5022291584562472</span>
              <span class="support-card-name">محمد خاک‌نژادی</span>
            </div>
            <button type="button" class="btn" onclick="copySupportCard()"><i class="ti ti-copy"></i><span data-i18n="newsCopyBtn">کپی شماره کارت</span></button>
          </div>
        </div>
      </div>
    </div>

    <!-- MESSAGES -->
    <div class="page" id="pg-messages">
      <div class="pg-head"><div><div class="eyebrow"><span class="live-dot"></span> MESSAGE CENTER</div><h1>مرکز پیام و خطا</h1><p>تمام خطاهای سرور، خطاهای مرورگر و رویدادهای مهم اینجا جمع می‌شوند تا هیچ خطایی گم نشود.</p></div><div class="toolbar"><span class="message-auto" id="messageLastSync">همگام‌سازی خودکار</span><button class="btn" onclick="loadMessages()"><i class="ti ti-refresh"></i>بروزرسانی</button><button class="btn danger" onclick="clearErrors()"><i class="ti ti-trash"></i>پاک‌کردن خطاها</button></div></div>
      <div class="message-center" id="messageStats"></div>
      <div class="card">
        <div class="panel-head"><div><b>خطاهای ثبت‌شده</b><small>خطاهای Backend و Frontend با جزئیات مسیر و زمان</small></div><div class="message-filter"><button class="on" data-message-filter="all" onclick="setMessageFilter('all')">همه</button><button data-message-filter="err" onclick="setMessageFilter('err')">خطا</button><button data-message-filter="warn" onclick="setMessageFilter('warn')">هشدار</button><button data-message-filter="client" onclick="setMessageFilter('client')">مرورگر</button></div></div>
        <div class="message-list" id="messageList"></div>
      </div>
      <div class="card" style="margin-top:14px"><div class="panel-head"><div><b>رویدادهای مهم</b><small>آخرین فعالیت‌های پنل برای عیب‌یابی سریع</small></div></div><div class="message-list" id="messageActivityList"></div></div>
    </div>

    <!-- SETTINGS -->
    <div class="page" id="pg-settings">
      <div class="pg-head"><div><div class="eyebrow">CONTROL CENTER / PERSONALIZATION</div><h1>تنظیمات و استودیو ظاهر</h1><p>ظاهر، فونت، رنگ، تراکم، زبان و تنظیمات عملیاتی پنل را از یکجا کنترل کن.</p></div><div class="toolbar"><button class="btn" onclick="resetAppearance()"><i class="ti ti-refresh"></i>بازنشانی ظاهر</button></div></div>

      <div class="appearance-studio">
        <div class="appearance-card">
          <h3>Appearance Studio</h3><p>تنظیمات ظاهری فقط برای همین مرورگر ذخیره می‌شوند و بدون دست‌زدن به اطلاعات سرور قابل تغییرند.</p>
          <div class="appearance-grid">
            <div class="appearance-field"><label>فونت رابط کاربری</label><select id="appearanceFont" onchange="setFont(this.value)"><option value="Vazirmatn">Vazirmatn</option><option value="Estedad">Estedad</option><option value="IBM Plex Sans Arabic">IBM Plex Sans Arabic</option><option value="Shabnam">Shabnam</option><option value="Yekan Bakh">Yekan Bakh</option><option value="Inter">Inter</option></select></div>
            <div class="appearance-field"><label>اندازه متن</label><div class="theme-pills"><button class="theme-pill" data-font-size="small" onclick="setFontSize('small')">Small</button><button class="theme-pill" data-font-size="normal" onclick="setFontSize('normal')">Normal</button><button class="theme-pill" data-font-size="large" onclick="setFontSize('large')">Large</button></div></div>
            <div class="appearance-field"><label>تراکم پنل</label><div class="theme-pills"><button class="theme-pill" data-density="comfortable" onclick="setDensity('comfortable')">Comfort</button><button class="theme-pill" data-density="compact" onclick="setDensity('compact')">Compact</button></div></div>
            <div class="appearance-field"><label>گوشه‌ها</label><div class="theme-pills"><button class="theme-pill" data-radius="soft" onclick="setRadius('soft')">Soft</button><button class="theme-pill" data-radius="sharp" onclick="setRadius('sharp')">Sharp</button><button class="theme-pill" data-radius="pill" onclick="setRadius('pill')">Pill</button></div></div>
            <div class="appearance-field"><label>پوسته</label><div class="theme-pills"><button class="theme-pill" data-theme-choice="dark" onclick="setAppearanceTheme('dark')">Dark</button><button class="theme-pill" data-theme-choice="light" onclick="setAppearanceTheme('light')">Light</button><button class="theme-pill" data-theme-choice="system" onclick="setAppearanceTheme('system')">System</button></div></div>
            <div class="appearance-field"><label>رنگ اصلی</label><div class="accent-pills"><button class="accent-pill" data-accent="purple" onclick="setAccent('purple')"><span class="accent-dot" style="background:#8b5cf6"></span>Purple</button><button class="accent-pill" data-accent="blue" onclick="setAccent('blue')"><span class="accent-dot" style="background:#3b82f6"></span>Blue</button><button class="accent-pill" data-accent="cyan" onclick="setAccent('cyan')"><span class="accent-dot" style="background:#06b6d4"></span>Cyan</button><button class="accent-pill" data-accent="green" onclick="setAccent('green')"><span class="accent-dot" style="background:#10b981"></span>Green</button><button class="accent-pill" data-accent="orange" onclick="setAccent('orange')"><span class="accent-dot" style="background:#f59e0b"></span>Orange</button><button class="accent-pill" data-accent="pink" onclick="setAccent('pink')"><span class="accent-dot" style="background:#ec4899"></span>Pink</button><button class="accent-pill" data-accent="red" onclick="setAccent('red')"><span class="accent-dot" style="background:#ef4444"></span>Red</button><button class="accent-pill" data-accent="indigo" onclick="setAccent('indigo')"><span class="accent-dot" style="background:#6366f1"></span>Indigo</button><button class="accent-pill" data-accent="teal" onclick="setAccent('teal')"><span class="accent-dot" style="background:#14b8a6"></span>Teal</button><button class="accent-pill" data-accent="gold" onclick="setAccent('gold')"><span class="accent-dot" style="background:#eab308"></span>Gold</button><label class="accent-pill" data-accent="custom" title="Custom colour" style="cursor:pointer"><input type="color" id="accentCustom" value="#ef4444" style="width:16px;height:16px;border:0;padding:0;background:none;cursor:pointer" oninput="setCustomAccent(this.value)">Custom</label></div></div>
          </div>
          <div class="appearance-actions">
            <div class="appearance-toggle"><span>انیمیشن‌های پنل</span><button id="motionSwitch" class="switch" onclick="toggleMotion()"></button></div>
            <div class="appearance-toggle"><span>سایدبار باز در دسکتاپ</span><button id="wideSwitch" class="switch" onclick="toggleWideSidebar()"></button></div>
            <div class="appearance-toggle"><span>Glow / نورپردازی</span><button id="glowSwitch" class="switch" onclick="toggleGlow()"></button></div>
          </div>
        </div>
        <div class="appearance-card appearance-preview"><div class="preview-window"><div class="preview-top"><i class="ti ti-circle-filled"></i><i class="ti ti-circle-filled"></i><i class="ti ti-circle-filled"></i></div><div class="preview-main"><div class="preview-side"><div class="active"></div><div></div><div></div><div></div></div><div class="preview-content"><div class="pv-title">VodiWalker Control Center</div><div class="pv-sub">Live system overview</div><div class="pv-cards"><span></span><span></span><span></span></div></div></div></div></div>
      </div>

      <div class="card pro-diagnostics" style="margin-top:14px">
        <div class="panel-head"><div><b>SYSTEM HEALTH / LIVE DIAGNOSTICS</b><small>Live server, resource, object and security telemetry</small></div><div class="toolbar"><span id="diagStatus" class="badge green">READY</span><button class="btn" onclick="loadDiagnostics()"><i class="ti ti-activity"></i>Refresh</button></div></div>
        <div class="diag-grid" id="diagGrid"><div class="diag-empty">Press Refresh to inspect the live system.</div></div>
      </div>

      <div class="two-col">
        <div class="card settings-card">
          <div class="section-title">آدرس عمومی پنل</div>
          <p class="hint" style="margin-bottom:12px">برای لینک‌های Subscription، دامنه واقعی پنل را ثابت کن. روی Railway بهتر است دامنه عمومی سرویس را اینجا قرار بدهی.</p>
          <div class="grp"><input id="setBaseUrl" placeholder="https://panel.example.com"></div>
          <button class="btn primary" onclick="saveBaseUrl()"><i class="ti ti-device-floppy"></i>ذخیره آدرس</button>
          <div class="divider"></div><div class="section-title">امنیت حساب</div>
          <div class="grp"><label>نام کاربری پنل</label><div class="row2"><input type="text" id="adminUsername" autocomplete="username" maxlength="40" placeholder="admin"><button class="btn primary" onclick="changeUsername()"><i class="ti ti-user-edit"></i>تغییر نام کاربری</button></div><div class="hint">نام کاربری جدید بدون فاصله و بین ۳ تا ۴۰ کاراکتر.</div></div>
          <div class="divider"></div>
          <div class="grp"><label>رمز فعلی</label><div style="position:relative"><input type="password" id="curPass" autocomplete="current-password"><button type="button" class="iconbtn" style="position:absolute;left:7px;top:6px" onclick="toggleSettingsPass('curPass',this)"><i class="ti ti-eye"></i></button></div></div><div class="row2"><div class="grp"><label>رمز جدید</label><div style="position:relative"><input type="password" id="newPass" autocomplete="new-password" oninput="passwordMeter()"><button type="button" class="iconbtn" style="position:absolute;left:7px;top:6px" onclick="toggleSettingsPass('newPass',this)"><i class="ti ti-eye"></i></button></div><div id="passMeter" style="height:4px;background:var(--line);border-radius:99px;margin-top:7px;overflow:hidden"><i id="passMeterBar" style="display:block;height:100%;width:0;background:var(--bad);transition:.2s"></i></div><div id="passHint" class="hint">حداقل ۸ کاراکتر، ترجیحاً ترکیب حروف، عدد و نماد.</div></div><div class="grp"><label>تکرار رمز جدید</label><div style="position:relative"><input type="password" id="repPass" autocomplete="new-password"><button type="button" class="iconbtn" style="position:absolute;left:7px;top:6px" onclick="toggleSettingsPass('repPass',this)"><i class="ti ti-eye"></i></button></div></div></div>
          <button class="btn primary" onclick="changePassword()"><i class="ti ti-key"></i>تغییر امن رمز</button><button class="btn" style="margin-right:7px" onclick="revokeOtherSessions()"><i class="ti ti-shield-lock"></i>لغو نشست‌های قبلی</button>
        </div>
        <div class="card settings-card">
          <div class="section-title">Railway Network Center</div>
          <p class="hint" style="margin-bottom:12px">دامنه و پورت TCP عمومی Railway را اینجا مدیریت کن. Railway دامنه و پورت TCP Proxy را خودش تولید می‌کند و باید همان مقدار استفاده شود.</p>
          <div class="row2"><div class="grp"><label>TCP Host</label><input id="setTcpHost" placeholder="roundhouse.proxy.rlwy.net" class="mono" style="direction:ltr;text-align:left"></div><div class="grp"><label>TCP Port</label><input id="setTcpPort" placeholder="11105" class="mono" style="direction:ltr;text-align:left"></div></div>
          <p class="hint" id="tcpListenHint">—</p><button class="btn primary" onclick="saveTcpSettings()"><i class="ti ti-device-floppy"></i>ذخیره شبکه</button>
          <div class="divider"></div><div class="section-title">Sales & Management Bot</div>
          <div class="grp"><label>Bot Token</label><input id="setBotToken" placeholder="123456:ABC-DEF..." class="mono" style="direction:ltr;text-align:left"></div><div class="grp"><label>Admin IDs</label><input id="setBotAdmins" placeholder="123456789,987654321"></div>
          <div style="display:flex;gap:10px;align-items:center;margin-top:8px"><span class="status-dot off" id="botDot"></span><span id="botStatusText" style="font-size:13px">وضعیت نامشخص</span></div><div style="display:flex;gap:10px;margin-top:14px"><button class="btn primary" onclick="saveBotSettings()"><i class="ti ti-device-floppy"></i>ذخیره</button><button class="btn" id="botStartBtn" onclick="botStart()"><i class="ti ti-player-play"></i>شروع</button><button class="btn danger" id="botStopBtn" onclick="botStop()"><i class="ti ti-player-stop"></i>توقف</button></div>
        </div>
      </div>
      <div class="card settings-card" style="margin-top:14px">
        <div class="section-title">پشتیبانی و برند اشتراک</div>
        <p class="hint" style="margin-bottom:12px">آیدی تلگرام پشتیبانِ شما در صفحه‌ی اشتراک مشتری‌ها نمایش داده می‌شود و با یک کلیک مستقیم به همان آیدی در تلگرام می‌روند.</p>
        <div class="row2">
          <div class="grp"><label>آیدی تلگرام پشتیبان</label><input id="setSupportId" class="mono" dir="ltr" style="text-align:left" placeholder="@YourSupport" maxlength="60" oninput="updateBrandPreview()"></div>
          <div class="grp"><label>آیدی کانال اطلاع‌رسانی (اختیاری)</label><input id="setChannelId" class="mono" dir="ltr" style="text-align:left" placeholder="@YourChannel" maxlength="60"></div>
        </div>
        <label class="tpl-row" style="margin-top:6px"><div class="tpl-row-main"><i class="ti ti-sparkles"></i><div><b>استایل خودکار نام کانفیگ‌ها</b><small>اسم ساده مثل VodiWalker به‌صورت VodiWalker|Tofan🚀 با اسم و ایموجی خفن ساخته می‌شود (دستی و خودکار)</small></div></div><input type="checkbox" class="tpl-switch" id="nameStyleEnabled" onchange="updateBrandPreview()"></label>
        <div class="tpl-preview" style="margin-top:10px">
          <div class="tpl-preview-label"><i class="ti ti-device-mobile"></i> پیش‌نمایش در اپ کاربر</div>
          <div class="tpl-preview-row"><span class="tpl-preview-dot"></span><div class="tpl-preview-text" id="brandNamePreview">VodiWalker|Tofan🚀</div><span class="tpl-preview-proto">VLESS</span></div>
          <div class="tpl-preview-row" style="margin-top:8px"><span class="tpl-preview-dot"></span><div class="tpl-preview-text" id="brandSupportPreview">پشتیبانی: @VodiWalker</div><span class="tpl-preview-proto">Telegram</span></div>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:14px"><button class="btn primary" onclick="saveBrandSettings()"><i class="ti ti-device-floppy"></i> ذخیره پشتیبانی و نام‌ها</button><a class="btn" id="supportTestLink" href="https://t.me/vodiwalker02" target="_blank" rel="noopener"><i class="ti ti-brand-telegram"></i> تست لینک پشتیبان</a></div>
      </div>
      <div class="card settings-card tpl-studio" style="margin-top:14px">
        <div class="tpl-studio-head"><div><div class="section-title">Subscription Template</div><p class="hint">همان یک لینک ساب که به کاربر می‌دهی؛ فقط تعیین کن نام کانفیگ داخل اپ او دقیقاً چه چیزهایی را نشان دهد.</p></div><div class="tpl-badge"><i class="ti ti-wand"></i>Template Studio</div></div>
        <div class="tpl-grid">
          <div class="tpl-fields">
            <label class="tpl-row"><div class="tpl-row-main"><i class="ti ti-tag"></i><div><b>نام کانفیگ</b><small>نام دلخواه یا برند شما</small></div></div><input type="checkbox" class="tpl-switch" id="subTplName"></label>
            <label class="tpl-row"><div class="tpl-row-main"><i class="ti ti-database"></i><div><b>حجم اختصاص‌یافته</b><small>مثلاً ۵۰ گیگابایت</small></div></div><input type="checkbox" class="tpl-switch" id="subTplVolume"></label>
            <label class="tpl-row"><div class="tpl-row-main"><i class="ti ti-fingerprint"></i><div><b>شناسه کانفیگ (ID)</b><small>شناسه کوتاه یکتا</small></div></div><input type="checkbox" class="tpl-switch" id="subTplId"></label>
            <label class="tpl-row"><div class="tpl-row-main"><i class="ti ti-router"></i><div><b>نام اینباند</b><small>نام اینباند مادر این کانفیگ</small></div></div><input type="checkbox" class="tpl-switch" id="subTplInbound"></label>
          </div>
          <div class="tpl-preview">
            <div class="tpl-preview-label"><i class="ti ti-device-mobile"></i>پیش‌نمایش داخل اپ کاربر</div>
            <div class="tpl-preview-row"><span class="tpl-preview-dot"></span><div class="tpl-preview-text" id="subTplPreview">MyConfig</div><span class="tpl-preview-proto">VLESS</span></div>
            <p class="hint" style="margin-top:10px">ترتیب نمایش دقیقاً همین ترتیب بالاست؛ بین هر بخش یک خط جداکننده (|) قرار می‌گیرد.</p>
          </div>
        </div>
        <button class="btn primary" style="margin-top:14px" onclick="saveSubTemplate()"><i class="ti ti-device-floppy"></i>ذخیره الگوی ساب</button>
      </div>
      <div class="card settings-card tpl-studio" style="margin-top:14px">
        <div class="tpl-studio-head"><div><div class="section-title">سرور اطلاعاتی (Vodiwalkerpanel)</div><p class="hint">یک ردیف تزئینی و همیشه غیرقابل‌اتصال (آدرس 0.0.0.0) که در ابتدای هر لیست سرور اضافه می‌شود تا کاربر حجم/زمان باقی‌مانده‌اش را همان‌جا ببیند، بدون نیاز به باز کردن مرورگر.</p></div></div>
        <div class="tpl-grid">
          <div class="tpl-fields">
            <label class="tpl-row"><div class="tpl-row-main"><i class="ti ti-toggle-right"></i><div><b>نمایش سرور اطلاعاتی</b><small>خاموش کن تا اصلاً اضافه نشود</small></div></div><input type="checkbox" class="tpl-switch" id="infoLineEnabled"></label>
            <label class="tpl-row"><div class="tpl-row-main"><i class="ti ti-database"></i><div><b>نمایش حجم مصرفی</b><small>مصرف‌شده / کل / باقی‌مانده</small></div></div><input type="checkbox" class="tpl-switch" id="infoLineVolume"></label>
            <label class="tpl-row"><div class="tpl-row-main"><i class="ti ti-clock"></i><div><b>نمایش زمان باقی‌مانده</b><small>تا تاریخ انقضا</small></div></div><input type="checkbox" class="tpl-switch" id="infoLineExpiry"></label>
          </div>
          <div class="tpl-preview">
            <div class="tpl-preview-label"><i class="ti ti-device-mobile"></i>پیش‌نمایش داخل اپ کاربر</div>
            <div class="tpl-preview-row"><span class="tpl-preview-dot"></span><div class="tpl-preview-text" id="infoLinePreview">🌐 Vodiwalkerpanel</div><span class="tpl-preview-proto">0.0.0.0</span></div>
          </div>
        </div>
        <button class="btn primary" style="margin-top:14px" onclick="saveInfoLineSettings()"><i class="ti ti-device-floppy"></i>ذخیره تنظیمات سرور اطلاعاتی</button>
      </div>

      <div class="card settings-card" style="margin-top:14px">
        <div class="section-title">پراکسی IP (SOCKS) — مسیر خروجی</div>
        <p class="hint" style="margin-bottom:12px">وقتی یک SOCKS5 اینجا اضافه کنی، یک تونل واقعی از داخلش باز می‌شه و «پینگ واقعی» + «کشور و پرچم IP خروجی» نشون داده می‌شه. بعد هر بار که «ساخت سریع»، «اینباند جدید» یا «ساخت کلاینت» می‌زنی، می‌پرسه می‌خوای با این پراکسی (روی کشور دیگه) ساخته بشه یا مستقیم از خود Railway.</p>
        <div class="row2" style="align-items:flex-end">
          <div class="grp"><label>نام دلخواه</label><input id="pxName" placeholder="مثلاً آلمان-۱"></div>
          <div class="grp"><label>Host</label><input id="pxHost" class="mono" style="direction:ltr;text-align:left" placeholder="1.2.3.4  یا  socks5://user:pass@host:1080"></div>
        </div>
        <div class="row2" style="align-items:flex-end">
          <div class="grp"><label>Port</label><input id="pxPort" class="mono" style="direction:ltr;text-align:left" value="1080"></div>
          <div class="grp"><label>Username (اختیاری)</label><input id="pxUser" class="mono" style="direction:ltr;text-align:left"></div>
        </div>
        <div class="row2" style="align-items:flex-end">
          <div class="grp"><label>Password (اختیاری)</label><input id="pxPass" type="password" class="mono" style="direction:ltr;text-align:left"></div>
          <div class="grp" style="display:flex;align-items:flex-end"><button class="btn primary" onclick="addProxyForm()" style="width:100%"><i class="ti ti-plus"></i> افزودن و تست پینگ</button></div>
        </div>
        <div class="divider"></div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px"><b style="font-size:13px">پراکسی‌های ذخیره‌شده</b><button class="btn sm" onclick="testAllProxies()"><i class="ti ti-activity"></i> تست همه</button></div>
        <div id="proxiesListWrap"><div class="muted" style="padding:12px">در حال بارگذاری...</div></div>
      </div>

      <div class="card settings-card" style="margin-top:14px"><div class="section-title">Bot Text Studio <span class="badge red" style="margin-inline-start:8px"><i class="ti ti-lock"></i> LOCKED</span></div><div class="bot-lock-note"><i class="ti ti-lock"></i><span>ویرایش متن‌های ربات قفل شده است.</span></div><p class="hint">تمام پیام‌های کلیدی ربات را از همین پنل ویرایش کن؛ تغییرات روی ربات در اجرای بعدی/ری‌استارت اعمال می‌شوند.</p><div class="bot-text-grid"><div class="grp"><label>پیام خوش‌آمد</label><textarea id="botTxtWelcome" rows="4" disabled readonly></textarea></div><div class="grp"><label>منوی مدیریت</label><textarea id="botTxtAdmin" rows="4" disabled readonly></textarea></div><div class="grp"><label>پیام ساخت کانفیگ</label><textarea id="botTxtCreated" rows="3" disabled readonly></textarea></div></div><button class="btn primary" onclick="saveBotTexts()" disabled><i class="ti ti-device-floppy"></i>ذخیره متن‌های ربات</button></div>

      <div class="card advanced-settings" style="margin-top:14px"><div class="panel-head"><div><b>CONTROL CENTER PRO</b><small>ابزارهای حرفه‌ای برای شخصی‌سازی و نگهداری پنل</small></div><span class="badge green">PRO</span></div><div class="advanced-grid"><button class="pro-action" onclick="refreshOverview();toast('داده‌های زنده بروزرسانی شد ✓')"><i class="ti ti-activity-heartbeat"></i><b>Live Refresh</b><small>مانیتورینگ فوری منابع</small></button><button class="pro-action" onclick="loadSettings();toast('تنظیمات دوباره بارگذاری شد ✓')"><i class="ti ti-refresh"></i><b>Reload Settings</b><small>دریافت تنظیمات واقعی سرور</small></button><button class="pro-action" onclick="location.reload()"><i class="ti ti-reload"></i><b>Hard Reload</b><small>بارگذاری کامل رابط</small></button><button class="pro-action" onclick="navigator.clipboard?.writeText(location.origin);toast('دامنه پنل کپی شد ✓')"><i class="ti ti-world-copy"></i><b>Copy Panel URL</b><small>دامنه فعلی پنل</small></button></div></div>
    </div>

  </div>
  </div>
</div>

<div class="overlay" id="overlay" onclick="closeDrawer()"></div>
<div class="drawer" id="drawer">
  <div class="dr-head"><h3 id="drTitle">—</h3><button class="iconbtn" onclick="closeDrawer()"><i class="ti ti-x"></i></button></div>
  <div class="dr-body" id="drBody"></div>
  <div class="dr-foot" id="drFoot"></div>
</div>

<div id="toastWrap"></div>

<script>
// ============================================================
// Core helpers
// ============================================================
const $ = (id) => document.getElementById(id);
function toast(msg, ok=true){
  const t = document.createElement('div');
  t.className = 'toast ' + (ok?'ok':'err');
  const safeMsg = dashTranslateValue(String(msg ?? ''), typeof getDashLang === 'function' ? getDashLang() : 'fa');
  t.innerHTML = `<i class="ti ti-${ok?'circle-check':'alert-circle'}"></i><span>${escapeHtml(safeMsg)}</span>`;
  const _tw = $('toastWrap'); _tw.appendChild(t); while(_tw.children.length > 3) _tw.firstChild.remove();
  setTimeout(()=>t.remove(), 3800);
}
// وقتی یک «نود» برای مدیریت انتخاب شده، APIهای عملیاتی از طریق پنل اصلی روی نود اجرا می‌شن.
const ACTIVE_NODE = (()=>{ try{ return JSON.parse(sessionStorage.getItem('vw_active_node')||'null'); }catch(e){ return null; } })();
const NODE_FWD_PREFIXES = ['/api/links','/api/proxies','/api/subs','/api/categories','/api/protocols','/api/reality-keypair','/api/connections','/api/telemetry','/api/system','/api/network','/api/reports','/api/activity','/api/errors','/stats'];
function nodeRewrite(path){
  if(!ACTIVE_NODE) return path;
  const p = String(path).split('?')[0].replace(/\/+$/,'');
  return NODE_FWD_PREFIXES.some(x=>p===x || p.startsWith(x+'/')) ? `/api/nodes/${ACTIVE_NODE.id}/fwd${path}` : path;
}
async function api(path, opts={}){
  const ctl = new AbortController();
  const tm = setTimeout(()=>ctl.abort(), 30000);
  let res;
  try{
    res = await fetch(nodeRewrite(path), {credentials:'same-origin', headers:{'Content-Type':'application/json'}, signal: ctl.signal, ...opts});
  }catch(e){
    if(e && e.name==='AbortError') throw new Error('زمان درخواست تمام شد؛ اتصال را بررسی کن');
    throw e;
  }finally{ clearTimeout(tm); }
  let data = {};
  try{ data = await res.json(); }catch(e){}
  if(!res.ok){
    const message = data.detail || data.error || data.message || ('خطا ' + res.status);
    throw new Error(message);
  }
  return data;
}

let MESSAGE_FILTER='all';
let messageTimer=null;
let reportingClientError=false;
async function reportClientError(message, source='browser', extra={}){
  if(reportingClientError) return;
  reportingClientError=true;
  try{
    await fetch('/api/errors/client',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},keepalive:true,body:JSON.stringify({message:String(message||'Unknown client error').slice(0,1200),source:String(source||'browser').slice(0,40),path:location.pathname,stack:String(extra.stack||'').slice(0,4000),details:String(extra.details||'').slice(0,1500)})});
  }catch(e){} finally{reportingClientError=false;}
}
window.addEventListener('error',e=>{ if(e?.message) reportClientError(e.message,'browser',{stack:e.error?.stack,details:`${e.filename||''}:${e.lineno||''}:${e.colno||''}`}); });
window.addEventListener('unhandledrejection',e=>{ const r=e?.reason; reportClientError(r?.message||String(r||'Unhandled promise rejection'),'promise',{stack:r?.stack}); });
function fmtBytes(n){
  n = Number(n||0);
  if(n<=0) return '0';
  const u=['B','KB','MB','GB','TB']; let i=0;
  while(n>=1024 && i<u.length-1){n/=1024;i++;}
  return n.toFixed(n<10&&i>0?1:0)+' '+u[i];
}
function escapeHtml(s){ return String(s??'').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

// ============================================================
// Nav
// ============================================================
document.querySelectorAll('.tab').forEach(t=>{
  t.addEventListener('click', ()=> gotoPage(t.dataset.pg));
});
function gotoPage(pg){
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on', t.dataset.pg===pg));
  document.querySelectorAll('.page').forEach(p=>p.classList.toggle('on', p.id==='pg-'+pg));
  CURRENT_PAGE = pg;
  updatePageTitle(pg);
  document.getElementById('app').classList.remove('sb-open');
  const loaders = {overview:refreshOverview, links:loadLinks, clientmgr:loadClientManager, categories:loadCategories, subgroups:loadSubGroups, nodes:loadNodesPage,
    reports:loadReports, admins:()=>{loadAdmins();loadAdminRequests();}, activity:loadActivity, messages:loadMessages, settings:()=>{loadSettings();loadDiagnostics();}};
  if(loaders[pg]) loaders[pg]();
}

// ============================================================
// Drawer
// ============================================================

// QR محلی: لینک اشتراک هیچ‌وقت برای سرویس خارجی ارسال نمی‌شود و بدون اینترنت جهانی هم کار می‌کند
function qrSrc(text){
  try{
    if(typeof qrcode === 'function'){
      const q = qrcode(0, 'M'); q.addData(String(text||'')); q.make();
      return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(q.createSvgTag(4, 4));
    }
  }catch(e){}
  return 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=' + encodeURIComponent(String(text||''));
}
function openDrawer(title, bodyHtml, footHtml){
  $('drTitle').textContent = title;
  $('drBody').innerHTML = bodyHtml;
  $('drFoot').innerHTML = footHtml;
  $('overlay').classList.add('show');
  $('drawer').classList.add('show');
}
function closeDrawer(){
  $('overlay').classList.remove('show');
  $('drawer').classList.remove('show');
}

// ============================================================
// Appearance Studio
// ============================================================
const APPEARANCE_DEFAULTS={font:'Vazirmatn',theme:'dark',accent:'purple',density:'comfortable',motion:true,wide:false,radius:'soft',glow:true,fontSize:'normal'};
function hexToRgb(h){h=String(h||'').replace('#','');if(h.length===3)h=h.split('').map(x=>x+x).join('');const n=parseInt(h,16);return isNaN(n)?[139,92,246]:[(n>>16)&255,(n>>8)&255,n&255]}
function rgbToHex(r,g,b){return '#'+[r,g,b].map(x=>Math.max(0,Math.min(255,Math.round(x))).toString(16).padStart(2,'0')).join('')}
function mixHex(a,b,t){const x=hexToRgb(a),y=hexToRgb(b);return rgbToHex(x[0]+(y[0]-x[0])*t,x[1]+(y[1]-x[1])*t,x[2]+(y[2]-x[2])*t)}
const ACCENTS={purple:['#8b5cf6','#6d28d9'],blue:['#3b82f6','#1d4ed8'],cyan:['#06b6d4','#0e7490'],green:['#10b981','#047857'],orange:['#f59e0b','#b45309'],pink:['#ec4899','#be185d'],red:['#ef4444','#b91c1c'],indigo:['#6366f1','#4338ca'],teal:['#14b8a6','#0f766e'],gold:['#eab308','#a16207']};
function getAppearance(){try{return {...APPEARANCE_DEFAULTS,...JSON.parse(localStorage.getItem('vw_appearance')||'{}')}}catch(e){return {...APPEARANCE_DEFAULTS}}}
function saveAppearance(a){try{localStorage.setItem('vw_appearance',JSON.stringify(a))}catch(e){} applyAppearance()}
function loadFontLazy(n){try{if(!n||n==='Vazirmatn'||document.getElementById('f-'+n))return;const l=document.createElement('link');l.id='f-'+n;l.rel='stylesheet';l.href='https://fonts.googleapis.com/css2?family='+encodeURIComponent(n).replace(/%20/g,'+')+':wght@400;500;700&display=swap';document.head.appendChild(l);}catch(e){}}
function applyAppearance(){const a=getAppearance();loadFontLazy(a.font);const root=document.documentElement;root.style.setProperty('--font-ui',`'${a.font}',sans-serif`);const theme=a.theme==='system'?(matchMedia('(prefers-color-scheme:light)').matches?'light':'dark'):a.theme;root.setAttribute('data-theme',theme);const c=a.accent==='custom'?[a.accentHex||'#ef4444',mixHex(a.accentHex||'#ef4444','#000000',.35)]:(ACCENTS[a.accent]||ACCENTS.purple);root.style.setProperty('--accent',c[0]);root.style.setProperty('--accent-d',c[1]);
const rgb=hexToRgb(c[0]);root.style.setProperty('--accent-rgb',rgb.join(','));root.style.setProperty('--accent-soft',mixHex(c[0],'#ffffff',.45));
if(a.accent!=='purple'){const lt=mixHex(c[0],'#ffffff',.28);root.style.setProperty('--accent2',lt);root.style.setProperty('--cyan',lt);if(theme==='dark'){root.style.setProperty('--line','rgba('+rgb.join(',')+',.28)');root.style.setProperty('--line2','rgba('+rgb.join(',')+',.45)')}else{root.style.removeProperty('--line');root.style.removeProperty('--line2')}}else{['--accent2','--cyan','--line','--line2'].forEach(k=>root.style.removeProperty(k))}
if($('accentCustom')&&a.accent==='custom')$('accentCustom').value=c[0];root.style.setProperty('--ui-glow',a.glow?`0 14px 40px -18px ${c[0]}88`:'none');document.body.classList.toggle('density-compact',a.density==='compact');document.body.classList.toggle('no-motion',!a.motion);document.body.classList.toggle('wide-sidebar',!!a.wide);document.body.classList.toggle('radius-sharp',a.radius==='sharp');document.body.classList.toggle('radius-pill',a.radius==='pill');document.body.classList.toggle('font-small',a.fontSize==='small');document.body.classList.toggle('font-large',a.fontSize==='large');if($('appearanceFont'))$('appearanceFont').value=a.font;document.querySelectorAll('[data-theme-choice]').forEach(x=>x.classList.toggle('on',x.dataset.themeChoice===a.theme));document.querySelectorAll('[data-accent]').forEach(x=>x.classList.toggle('on',x.dataset.accent===a.accent));document.querySelectorAll('[data-density]').forEach(x=>x.classList.toggle('on',x.dataset.density===a.density));document.querySelectorAll('[data-radius]').forEach(x=>x.classList.toggle('on',x.dataset.radius===a.radius));document.querySelectorAll('[data-font-size]').forEach(x=>x.classList.toggle('on',x.dataset.fontSize===a.fontSize));if($('motionSwitch'))$('motionSwitch').classList.toggle('on',a.motion);if($('wideSwitch'))$('wideSwitch').classList.toggle('on',a.wide);if($('glowSwitch'))$('glowSwitch').classList.toggle('on',a.glow);updateThemeIcon()}
function setFont(v){const a=getAppearance();a.font=v;saveAppearance(a);toast('فونت پنل تغییر کرد ✓')}
function setAppearanceTheme(v){const a=getAppearance();a.theme=v;saveAppearance(a)}
function setCustomAccent(hex){const a=getAppearance();a.accent='custom';a.accentHex=hex;saveAppearance(a)}
function setAccent(v){const a=getAppearance();a.accent=v;saveAppearance(a)}
function setDensity(v){const a=getAppearance();a.density=v;saveAppearance(a)}
function setRadius(v){const a=getAppearance();a.radius=v;saveAppearance(a)}
function setFontSize(v){const a=getAppearance();a.fontSize=v;saveAppearance(a)}
function toggleMotion(){const a=getAppearance();a.motion=!a.motion;saveAppearance(a)}
function toggleWideSidebar(){const a=getAppearance();a.wide=!a.wide;saveAppearance(a)}
function toggleGlow(){const a=getAppearance();a.glow=!a.glow;saveAppearance(a)}
try{matchMedia('(prefers-color-scheme:light)').addEventListener('change',()=>{if(getAppearance().theme==='system')applyAppearance()})}catch(e){}
function resetAppearance(){try{localStorage.removeItem('vw_appearance');localStorage.removeItem('vw_theme')}catch(e){};applyAppearance();toast('ظاهر پنل به حالت پیش‌فرض برگشت ✓')}
applyAppearance();

// ============================================================
// Bootstrapping / current user
// ============================================================
let CATEGORIES = [];
let LINKS = [];
let PROTOCOLS = [];
let MANUAL_META = {};
let ADMIN_CACHE = [];

function toggleTheme(){
  const a=getAppearance(); a.theme=(a.theme==='light'?'dark':'light'); saveAppearance(a); toast(a.theme==='light'?'پوسته روشن و کاملاً سفید فعال شد ✓':'پوسته تیره فعال شد ✓');
}
function updateThemeIcon(){
  const btn = document.getElementById('themeToggle');
  if(!btn) return;
  const cur = document.documentElement.getAttribute('data-theme') || 'dark';
  btn.innerHTML = cur === 'light' ? '<i class="ti ti-sun"></i>' : '<i class="ti ti-moon"></i>';
}
updateThemeIcon();

function toggleSidebar(){
  document.getElementById('app').classList.toggle('sb-open');
}

var DASH_I18N = {
  fa: {
    dir:'rtl', brand:'VodiWalker',
    nav_overview:'داشبورد', nav_links:'اینباندها', nav_clientmgr:'ساخت کلاینت', nav_categories:'دسته‌بندی‌ها', nav_subgroups:'گروه‌های ساب',
    nav_reports:'گزارش‌ها', nav_admins:'ادمین‌ها', nav_nodes:'نودها', nav_activity:'فعالیت‌ها', nav_messages:'پیام‌ها', nav_settings:'تنظیمات', nav_news:'اخبار', pt_news:'کانال رسمی، اطلاع‌رسانی بروزرسانی‌ها و حمایت از پروژه',
    pt_overview:'وضعیت لحظه‌ای سرویس، کانفیگ‌ها و ربات تلگرام',
    pt_links:'مدیریت حرفه‌ای اینباندها، کلاینت‌ها و لینک‌های اشتراک',
    pt_clientmgr:'ساخت کلاینت واقعی از روی اینباند دلخواه، جدا از صفحه اینباندها',
    pt_categories:'پیش‌فرض‌های حجم، انقضا و محدودیت برای گروه‌های کانفیگ',
    pt_subgroups:'ترکیب چند کانفیگ در یک لینک اشتراک واحد',
    pt_reports:'خلاصه‌ی عملکرد کانفیگ‌ها',
    pt_admins:'حساب‌های دسترسی جانبی به پنل (فقط مالک)',
    pt_nodes:'اتصال چند پنل VodiWalker به هم و مدیریت یکجا',
    pt_activity:'۱۵۰ رویداد اخیر پنل',
    pt_messages:'مرکز خطاها، هشدارها و پیام‌های سیستم',
    pt_settings:'آدرس عمومی پنل، ربات تلگرام و رمز عبور'
  },
  en: {
    dir:'ltr', brand:'VodiWalker',
    nav_overview:'Overview', nav_links:'Inbounds', nav_clientmgr:'Create Client', nav_categories:'Categories', nav_subgroups:'Sub Groups',
    nav_plans:'Sale Plans', nav_reports:'Reports', nav_admins:'Admins', nav_nodes:'Nodes', nav_activity:'Activity', nav_messages:'Messages', nav_settings:'Settings',
    pt_overview:'Live status of the service, configs and Telegram bot',
    pt_links:'Manage inbounds, clients and subscription links',
    pt_clientmgr:'Create a real client from any inbound, separate from the inbounds page',
    pt_categories:'Default traffic, expiry and IP-limit presets for config groups',
    pt_subgroups:'Combine several configs into one subscription link',
    pt_reports:'Summary of sales and config performance',
    pt_admins:'Secondary panel access accounts (owner only)',
    pt_nodes:'Connect several VodiWalker panels and manage them from one place',
    pt_activity:'Last 150 panel events',
    pt_messages:'Errors, warnings and system messages',
    pt_settings:'Panel public URL, Telegram bot and password'
  }
};
var CURRENT_PAGE = 'overview';
const DASH_EN_TERMS = {
  // Navigation / pages
  'داشبورد':'Dashboard','اینباندها':'Inbounds','اینباند':'Inbound','دسته‌بندی‌ها':'Categories','دسته‌بندی':'Category',
  'گروه‌های ساب':'Subscription Groups','گروه ساب':'Subscription Group','گروه جدید':'New Group',
  'گزارش‌ها':'Reports','ادمین‌ها':'Admins','ادمین':'Admin','ادمین جدید':'New Admin','مالک':'Owner','فعالیت‌ها':'Activity','فعالیت':'Activity','اخبار':'News','کانال رسمی VodiWalker':'Official VodiWalker Channel','برای اطلاع از بروزرسانی‌های پنل، اخبار مهم، تغییرات سرویس و راهنمایی‌های استفاده، حتماً عضو کانال رسمی ما در تلگرام شو. هر اتفاق تازه‌ای اول از همه اونجا اعلام می‌شه.':'To stay updated on panel updates, important news, service changes and usage tips, be sure to join our official Telegram channel. Everything new is announced there first.','عضویت در کانال':'Join the channel','این پنل با عشق ساخته شده ❤️':'This panel was built with love ❤️','VodiWalker به‌صورت کاملاً رایگان و با علاقه‌ی شخصی ساخته و نگه‌داری می‌شه. اگه این پروژه بهت کمک کرده و دوست داشتی به ادامه‌ی راهش کمک کنی، می‌تونی به دلخواه و اختیاری حمایت کنی؛ این حمایت هیچ تعهد یا امتیاز خاصی ایجاد نمی‌کنه.':'VodiWalker is built and maintained completely for free, out of personal passion. If this project has helped you and you would like to support its future, you can optionally contribute; this support creates no obligation or special privilege.','شماره کارت':'Card number','کپی شماره کارت':'Copy card number','پیام‌ها':'Messages','تنظیمات':'Settings',
  'مرکز کنترل':'Control Center','مرکز پیام و خطا':'Message & Error Center','مدیریت حساب‌ها':'Admin Management','مدیریت حساب':'Admin Management',
  'تنظیمات و استودیو ظاهر':'Settings & Appearance Studio','استودیو ظاهر':'Appearance Studio',

  // Common actions / states
  'فعال':'Active','غیرفعال':'Inactive','فعال/غیرفعال':'Enable/Disable','خاموش':'Stopped','در حال اجرا':'Running','روشن':'Online','آنلاین':'Online','آفلاین':'Offline',
  'در دسترس نیست':'Unavailable','وضعیت نامشخص':'Unknown status','در حال دریافت...':'Loading...','بروزرسانی':'Refresh','بروزرسانی زنده':'Live Refresh',
  'ذخیره':'Save','ذخیره تغییرات':'Save Changes','ذخیره آدرس':'Save URL','ذخیره شبکه':'Save Network','ذخیره متن‌های ربات':'Save Bot Texts','حذف':'Delete','ویرایش':'Edit','ساخت':'Create','ساخت سریع':'Quick Create','لغو':'Cancel','تأیید':'Confirm','انصراف':'Cancel','بازگشت':'Back','نمایش':'View','کپی':'Copy','کپی لینک':'Copy Link','کپی لینک ساب':'Copy Subscription Link','دریافت فایل':'Download','خروجی CSV':'CSV Export','جستجو':'Search','فیلتر':'Filter','همه':'All','پاک‌کردن خطاها':'Clear Errors','لغو نشست‌های قبلی':'Revoke Previous Sessions',
  'شروع':'Start','توقف':'Stop','فعال‌سازی':'Enable','غیرفعال‌سازی':'Disable','عملیات':'Actions','کنترل':'Control','جزئیات':'Details','بستن':'Close','بارگذاری کامل رابط':'Hard Reload','بازنشانی ظاهر':'Reset Appearance','بارگذاری دوباره':'Reload',

  // Titles / descriptions
  'وضعیت لحظه‌ای سرویس، کانفیگ‌ها و ربات تلگرام':'Live service, configuration and Telegram bot status',
  'مدیریت حرفه‌ای اینباندها، کلاینت‌ها و لینک‌های اشتراک':'Professional inbound, client and subscription management',
  'پیش‌فرض‌های حجم، انقضا و محدودیت برای گروه‌های کانفیگ':'Traffic, expiry and limit presets for config groups',
  'ترکیب چند کانفیگ در یک لینک اشتراک واحد':'Combine multiple configs into one subscription link',
  'خلاصه‌ی عملکرد کانفیگ‌ها':'Configuration performance',
  'حساب‌های دسترسی جانبی به پنل (فقط مالک)':'Secondary panel access accounts (owner only)',
  '۱۵۰ رویداد اخیر پنل':'Latest 150 panel events',
  'مرکز خطاها، هشدارها و پیام‌های سیستم':'Errors, warnings and system messages',
  'آدرس عمومی پنل، ربات تلگرام و رمز عبور':'Panel public URL, Telegram bot and account security',
  'نمای لحظه‌ای منابع سرور، ترافیک، اتصال‌ها.':'Live server resources, traffic and connections.',
  'مرکز مدیریت اینباند، ساخت کلاینت و کنترل دسترسی؛ با پایش زنده هر ۵ ثانیه.':'Inbound management, client creation and access control with live monitoring every 5 seconds.',
  'تمام خطاهای سرور، خطاهای مرورگر و رویدادهای مهم اینجا جمع می‌شوند تا هیچ خطایی گم نشود.':'All server errors, browser errors and important events are collected here.',
  'ظاهر، فونت، رنگ، تراکم، زبان و تنظیمات عملیاتی پنل را از یکجا کنترل کن.':'Control appearance, font, colors, density, language and operational settings from one place.',
  'برای لینک‌های Subscription، دامنه واقعی پنل را ثابت کن. روی Railway بهتر است دامنه عمومی سرویس را اینجا قرار بدهی.':'Set the real panel domain for subscription links. On Railway, use the service public domain here.',
  'دامنه و پورت TCP عمومی Railway را اینجا مدیریت کن. Railway دامنه و پورت TCP Proxy را خودش تولید می‌کند و باید همان مقدار استفاده شود.':'Manage the public Railway TCP domain and port here. Railway generates the TCP Proxy values.',
  'تمام پیام‌های کلیدی ربات را از همین پنل ویرایش کن؛ تغییرات روی ربات در اجرای بعدی/ری‌استارت اعمال می‌شوند.':'Edit the bot messages here; changes apply on the next bot start/restart.',
  'حداقل ۸ کاراکتر، ترجیحاً ترکیب حروف، عدد و نماد.':'At least 8 characters; a mix of letters, numbers and symbols is recommended.',
  'نام کاربری جدید بدون فاصله و بین ۳ تا ۴۰ کاراکتر.':'New username without spaces, between 3 and 40 characters.',
  'ابزارهای حرفه‌ای برای شخصی‌سازی و نگهداری پنل':'Professional tools for panel personalization and maintenance',

  // Dashboard metrics
  'کل اینباندها':'Total Inbounds','پرمصرف‌ترین کانفیگ‌های ۷ روز اخیر':'Top configs from the last 7 days',
  'پرمصرف‌ترین کانفیگ‌ها':'Top Configs by Usage','خطاهای ثبت‌شده':'Recorded Errors','خطاهای Backend و Frontend با جزئیات مسیر و زمان':'Backend and frontend errors with route and time details',
  'رویدادهای مهم':'Important Events','آخرین فعالیت‌های پنل برای عیب‌یابی سریع':'Recent panel activity for quick troubleshooting',
  'وضعیت سیستم':'System Status','سیستم سالم است.':'System is healthy.','خطای ثبت‌شده‌ای وجود ندارد. سیستم سالم است.':'No recorded errors. System is healthy.','رویدادی وجود ندارد.':'No events found.','لاگی وجود ندارد':'No activity logs.','داده‌ای موجود نیست':'No data available.','هنوز داده‌ی مصرفی ثبت نشده':'No usage data recorded yet.','کانفیگی یافت نشد':'No configs found.','گروهی وجود ندارد':'No groups found.','پلنی وجود ندارد':'No plans found.',
  'همگام‌سازی خودکار':'Auto Sync','آخرین بروزرسانی':'Last Updated','۳۰ روز اخیر':'Last 30 days','۱۴ روز اخیر':'Last 14 days','۷ روز اخیر':'Last 7 days',
  'در حال ذخیره...':'Saving...','تغییر امن رمز':'Change Password','تغییر نام کاربری':'Change Username','نام کاربری پنل':'Panel Username','نام کاربری جدید':'New Username','رمز عبور':'Password','رمز فعلی':'Current Password','رمز جدید':'New Password','تکرار رمز جدید':'Repeat New Password','تکرار رمز عبور':'Repeat Password','امنیت حساب':'Account Security',
  'پیام خوش‌آمد':'Welcome Message','منوی مدیریت':'Admin Menu','پیام ساخت کانفیگ':'Config Created Message',
  'آدرس عمومی پنل':'Panel Public URL','دامنه فعلی پنل':'Current panel domain','ذخیره شد':'Saved','ذخیره شد ✓':'Saved ✓','ساخته شد':'Created','حذف شد':'Deleted','بروزرسانی شد':'Updated','کپی شد':'Copied','کپی شد ✓':'Copied ✓','تنظیمات دوباره بارگذاری شد ✓':'Settings reloaded ✓','داده‌های زنده بروزرسانی شد ✓':'Live data refreshed ✓','دامنه پنل کپی شد ✓':'Panel URL copied ✓','نام کاربری با موفقیت تغییر کرد ✓':'Username changed successfully ✓','رمز عبور با موفقیت تغییر کرد ✓':'Password changed successfully ✓',

  // Tables / forms
  'نام کاربری':'Username','نام':'Name','نام گروه':'Group Name','برچسب':'Label','نقش':'Role','وضعیت':'Status','زمان':'Time','نوع':'Type','پیام':'Message','تعداد':'Count','تعداد کانفیگ':'Config Count','لینک عمومی':'Public Link',
  'پروتکل':'Protocol','آدرس':'Address','آدرس / Domain':'Address / Domain','پورت':'Port','سرعت':'Speed','حجم':'Traffic','حجم مصرفی':'Usage','حجم پیش‌فرض (GB)':'Default Traffic (GB)','انقضا':'Expiry','انقضا (روز)':'Expiry (Days)','اعتبار (روز)':'Validity (Days)','زمان دقیق انقضا':'Exact Expiry','محدودیت IP':'IP Limit','Connection Limit':'Connection Limit','تعداد کاربر':'Client Limit','تعداد خروجی':'Output Count','توضیحات':'Description','یادداشت داخلی':'Internal Note',
  'مدت':'Duration','قیمت (⭐)':'Price (⭐)','ویژه':'Featured','آخرین ورود':'Last Login','کل':'Total','روز':'Days','ساعت':'Hours','دقیقه':'Minutes','نامحدود':'Unlimited','پیش‌فرض':'Default','اختیاری':'Optional','اجباری':'Required','مصرف':'Usage','اتصال':'Connection','اتصالات':'Connections','کلاینت‌ها':'Clients','کلاینت':'Client','مشتریان':'Customers','مشتری‌ها':'Customers',
  'کپی VLESS':'Copy VLESS','اشتراک':'Subscription','مدیریت کلاینت‌های واقعی':'Real Client Manager','ساخت کلاینت واقعی':'Create Client','کنترل پنل':'Panel Control','مدیریت ربات':'Bot Management','ربات':'Bot',

  // Inbound builder
  'ساخت اینباند':'Create Inbound','ویرایش اینباند':'Edit Inbound','ساخت کلاینت':'Create Client','ویرایش کلاینت':'Edit Client','انتخاب پروتکل':'Select Protocol','پروتکل پایه':'Base Protocol','انتقال':'Transport','لایه انتقال':'Transport Layer','امنیت':'Security','تنظیمات اتصال':'Connection Settings','تنظیمات پیشرفته':'Advanced Settings','خلاصه':'Summary','قبل از ذخیره ترکیب نهایی را بررسی کن':'Review the final combination before saving',
  'ترکیب نهایی':'Final Combination','شبکه':'Network','روش رمزنگاری':'Encryption Method','رمز / Secret':'Password / Secret','کلید عمومی':'Public Key','شناسه کوتاه':'Short ID','مسیر Spider':'Spider X','تولید کلید Reality':'Generate Reality Keypair','تست پینگ':'Ping Test','در حال تست':'Testing...','ابتدا آدرس یا دامنه را وارد کنید':'Enter an address or domain first','پورت نامعتبر است':'Invalid port','اتصال برقرار نشد':'Connection failed',
  'این ترکیب آماده استفاده است.':'This combination is ready to use.','این ترکیب برای ساخت لینک و مدیریت سرویس آماده شده است.':'This combination is prepared for link and service management.','Shadowsocks به‌صورت TCP-only در این Builder ارائه می‌شود.':'Shadowsocks is provided as TCP-only in this builder.','Transport فقط مسیر انتقال است و جدا از پروتکل پایه انتخاب می‌شود.':'Transport is only the transfer layer and is selected separately from the base protocol.',
  'VLESS':'VLESS','VMess':'VMess','Trojan':'Trojan','Shadowsocks':'Shadowsocks','TCP':'TCP','WebSocket':'WebSocket','WS':'WebSocket','gRPC':'gRPC','XHTTP':'XHTTP','TLS':'TLS','Reality':'Reality','None':'None','امنیت بدون رمزنگاری':'No encryption','بدون رمزنگاری':'No encryption',

  // Settings / appearance
  'فونت رابط کاربری':'Interface Font','اندازه متن':'Text Size','تراکم پنل':'Panel Density','گوشه‌ها':'Corners','پوسته':'Theme','رنگ اصلی':'Accent Color','انیمیشن‌های پنل':'Panel Animations','سایدبار باز در دسکتاپ':'Open sidebar on desktop','نورپردازی':'Glow','Appearance Studio':'Appearance Studio','ظاهر پنل به حالت پیش‌فرض برگشت ✓':'Appearance reset ✓','فونت پنل تغییر کرد ✓':'Panel font updated ✓',
  'پوسته تاریک':'Dark Theme','پوسته روشن':'Light Theme','سیستم':'System','فونت پیش‌فرض':'Default Font','کوچک':'Small','متوسط':'Medium','بزرگ':'Large','فشرده':'Compact','راحت':'Comfortable','گرد':'Rounded','تیز':'Sharp',

  // Messages / diagnostics
  'خطا':'Error','هشدار':'Warning','اطلاعات':'Info','مرورگر':'Browser','پاک‌کردن':'Clear','مرکز خطاها':'Error Center','مرکز پیام و خطا':'Message & Error Center','خطا در پردازش اطلاعات ورود.':'Login data could not be processed.',
  'آدرس TCP ذخیره شد':'TCP address saved','آدرس ذخیره شد':'Address saved','ربات روشن شد':'Bot started','ربات خاموش شد':'Bot stopped','ربات در حال اجراست':'Bot is running','ربات خاموش است':'Bot is stopped',
  'Caps Lock فعال است':'Caps Lock is on','قدرت رمز':'Password strength','حداقل ۸ کاراکتر، ترکیب حروف بزرگ/کوچک، عدد و نماد پیشنهاد می‌شود.':'At least 8 characters; uppercase/lowercase letters, numbers and symbols are recommended.',

  // Railway / service
  'دامنه عمومی Railway وارد شد؛ برای TCP خام باید TCP Proxy فعال باشد':'Railway public domain loaded; raw TCP requires TCP Proxy.','اطلاعات TCP Proxy ریل‌وی در این سرویس پیدا نشد':'Railway TCP Proxy information was not found for this service.',
  'همه دسته‌ها':'All categories','مورد انتخاب شده':'selected','اینباند جدید':'New Inbound','دسته جدید':'New Category','وضعیت':'Status','آدرس':'Address','ترافیک':'Traffic','کلاینت / اتصال':'Client / Connection','عملیات':'Actions','نام گروه':'Group Name','تعداد کانفیگ':'Config Count','لینک عمومی':'Public Link','حجم پیش‌فرض':'Default Traffic','قیمت (⭐)':'Price (⭐)','خروجی CSV':'CSV Export','برچسب':'Label','مدیریت حساب‌ها':'Admin Management','ادمین جدید':'New Admin','نقش':'Role','آخرین ورود':'Last Login','مرکز پیام و خطا':'Message & Error Center','پاک‌کردن خطاها':'Clear Errors','خطاهای ثبت‌شده':'Recorded Errors','خطاهای Backend و Frontend با جزئیات مسیر و زمان':'Backend and frontend errors with route and time details','همه':'All','هشدار':'Warning','مرورگر':'Browser','بازنشانی ظاهر':'Reset Appearance','اندازه متن':'Text Size','تراکم پنل':'Panel Density','گوشه‌ها':'Corners','پوسته':'Theme','رنگ اصلی':'Accent Color','انیمیشن‌های پنل':'Panel Animations','سایدبار باز در دسکتاپ':'Open sidebar on desktop','Glow / نورپردازی':'Glow / Lighting','امنیت حساب':'Account Security','رمز فعلی':'Current Password','رمز جدید':'New Password','تکرار رمز جدید':'Repeat New Password','تغییر امن رمز':'Change Password','لغو نشست‌های قبلی':'Revoke Previous Sessions','توقف':'Stop','منوی مدیریت':'Admin Menu','پیام ساخت کانفیگ':'Config Created Message','پیام فروشگاه':'Store Message','پیام پرداخت موفق':'Payment Success Message','مانیتورینگ فوری منابع':'Instant resource monitoring','دریافت تنظیمات واقعی سرور':'Load real server settings','بارگذاری کامل رابط':'Hard Reload','دامنه فعلی پنل':'Current panel domain','در حال دریافت...':'Loading...','بروزرسانی':'Refresh','ساخت سریع':'Quick Create','کانفیگی یافت نشد':'No configs found','دسته‌بندی‌ها':'Categories','پلن‌های فروش':'Sales Plans','گروه‌های ساب':'Subscription Groups','ادمین‌ها':'Admins','پیام‌ها':'Messages','تنظیمات':'Settings',

  // --- Added: fill remaining gaps found across dashboard toasts, confirm()
  // dialogs, inbound builder, client manager and admin permission matrix ---
  'اینباند حذف شود؟':'inbound(s) be deleted?','این کلاینت حذف شود؟':'Delete this client?','این کانفیگ حذف شود؟':'Delete this config?','این دسته حذف شود؟':'Delete this category?','این گروه حذف شود؟':'Delete this group?','این پلن حذف شود؟':'Delete this plan?','این ادمین حذف شود؟':'Delete this admin?','همه خطاهای ثبت‌شده پاک شوند؟':'Clear all recorded errors?','همه نشست‌های قبلی این حساب لغو شوند؟':'Revoke all previous sessions for this account?','دسته‌بندی‌ای وجود ندارد':'No categories found','بروزرسانی گروهی انجام شد':'Bulk update completed','حذف گروهی انجام شد':'Bulk delete completed','کانفیگ خودکار ساخته شد':'Auto config created','اینباند بروزرسانی شد':'Inbound updated','اینباند با موفقیت ساخته شد':'Inbound created successfully','خطا در ذخیره اینباند':'Error saving inbound','خطا در دریافت اطلاعات Railway':'Error fetching Railway information','کلاینت واقعی ساخته شد ✓':'Client created ✓','متن‌های ربات ذخیره شد ✓':'Bot texts saved ✓','خطاها پاک شدند ✓':'Errors cleared ✓','ذخیره شد و ربات با تنظیمات جدید ری‌استارت شد':'Saved — the bot restarted with the new settings','ذخیره شد — برای اعمال، ربات را روشن کنید':'Saved — turn the bot on to apply the changes','کلید Reality ساخته شد. Private Key را روی نود خودتان نگه دارید.':'Reality keypair generated. Keep the private key on your own node.','پورت باید بین 1 تا 65535 باشد':'Port must be between 1 and 65535','Shadowsocks فقط با TCP ساخته می‌شود':'Shadowsocks can only be created over TCP','رمز جدید باید حداقل ۸ کاراکتر باشد':'New password must be at least 8 characters','رمز جدید باید با رمز فعلی متفاوت باشد':'New password must be different from the current password','تکرار رمز یکسان نیست':'Password confirmation does not match','همه‌ی فیلدهای رمز عبور را پر کنید':'Please fill in all password fields','نام کاربری باید ۳ تا ۴۰ کاراکتر و بدون فاصله باشد':'Username must be 3–40 characters with no spaces','نام کاربری را وارد کنید':'Please enter a username','هر کلاینت UUID مستقل دارد و برای پروتکل‌های Live مستقیماً توسط Relay قابل احراز است.':'Each client has its own UUID and, for Live protocols, is authenticated directly by the relay.','این اینباند فعلاً فقط لینک تولید می‌کند. برای Client واقعی، ابتدا یک ترکیب Live مثل VLESS + WS/TCP/XHTTP انتخاب کنید.':'This inbound currently only generates links. For a real client, first choose a Live combination such as VLESS + WS/TCP/XHTTP.','مدیریت کلاینت‌ها':'Manage Clients','حجم (GB، خالی = والد)':'Traffic (GB, empty = parent)','انقضا (روز، 0 = والد)':'Expiry (days, 0 = parent)','بدون تغییر خالی بگذار':'Leave empty for no change','والد':'parent','ساخت اینباند حرفه‌ای':'Create Professional Inbound','پروتکل پایه، ترنسپورت و امنیت کاملاً تفکیک‌شده':'Base protocol, transport and security are fully separated','اول مشخص کن با چه پروتکلی کانفیگ ساخته شود':'First decide which protocol the config will use','حالا مسیر انتقال را جداگانه انتخاب کن':'Now choose the transport layer separately','TLS / Reality / None را مستقل از ترنسپورت انتخاب کن':'Choose TLS / Reality / None independently of the transport','فقط فیلدهای مرتبط با انتخاب بالا نمایش داده می‌شوند':'Only fields relevant to the selection above are shown','لینک اشتراک':'Subscription Link','اگر این لینک برای مشتری باز نمی‌شود، ابتدا از تب «تنظیمات» آدرس عمومی پنل را درست تنظیم کنید.':'If this link doesn\'t open for the customer, first set the panel\'s public URL correctly under the “Settings” tab.','دسته':'Category','گروه ساب جدید':'New Subscription Group','پلن':'Plan','پیشنهاد ویژه':'Featured offer','در حال اتصال':'Connecting','غیرفعال/منقضی':'Disabled/Expired','فعال - بدون اتصال':'Active – No connection','منقضی شده':'Expired','روز مانده':'days left','بدون انقضا':'No expiry','اتصال زنده':'Live connections','کل کانفیگ‌ها':'Total Configs','تعداد سفارش':'Order Count','ساخت و مدیریت اینباند':'Create & manage inbounds','سابسکریپشن':'Subscription','پیام‌ها و خطاها':'Messages & Errors','اینباند و کلاینت':'Inbounds & Clients','هشدارهای اخیر':'Recent Warnings','خطاهای مرورگر':'Browser Errors','خطای نامشخص':'Unknown error','سرور TCP روی پورت داخلی':'TCP server on internal port','گوش می‌دهد — این را در Railway به همین پورت داخلی متصل کن، نه به':'is listening — in Railway, point this at the same internal port, not at the main HTTP','مثلاً':'e.g.','اصلی':'main','همه‌ی اینباندها بروزرسانی شدند ✓':'All inbounds refreshed ✓','بروزرسانی همه':'Refresh All','الگوی نام کانفیگ‌های ساب ذخیره شد ✓':'Subscription remark template saved ✓','نام کانفیگ':'Config Name','حجم اختصاص‌یافته':'Assigned Traffic','شناسه کانفیگ (ID)':'Config ID','نام اینباند':'Inbound Name','پیش‌نمایش: ':'Preview: ','همان یک لینک ساب که به کاربر می‌دهی؛ فقط تعیین کن نام کانفیگ داخل اپ او دقیقاً چه چیزهایی را نشان دهد.':'It\'s still the same single subscription link you hand out — just choose exactly what shows in the config name inside their app.','ذخیره الگوی ساب':'Save Template','Subscription Template':'Subscription Template',
    "افزودن":"Add",
  "دسترسی":"Access",
// ── Extended coverage (auto-generated audit): full-sentence UI strings ──
  "جستجوی سراسری":"Global search",
  "جستجوی سراسری (Ctrl+K)":"Global search (Ctrl+K)",
  "جستجو در پنل…":"Search the panel…",
  "انتخاب پنل/نود برای مدیریت":"Choose panel/node to manage",
  "تغییر پوسته":"Toggle theme",
  "خروج":"Log out",
  "مانیتور زنده سیستم":"Live system monitor",
  "نمای لحظه‌ای منابع سرور، ترافیک و اتصال‌ها.":"Real-time view of server resources, traffic and connections.",
  "پردازنده":"CPU",
  "حافظه RAM":"RAM memory",
  "سواپ":"Swap",
  "فضای ذخیره‌سازی":"Storage",
  "فعال: 0 | متوقف: 0":"Active: 0 | Stopped: 0",
  "سرعت کلی":"Overall speed",
  "پهنای باند لحظه‌ای":"Live bandwidth",
  "حافظه":"Memory",
  "دیسک":"Disk",
  "ارسال‌شده":"Sent",
  "دریافت‌شده":"Received",
  "نرخ لحظه‌ای":"Current rate",
  "وضعیت اتصال‌ها":"Connection status",
  "سوکت‌های باز":"Open sockets",
  "درخواست‌ها":"Requests",
  "خطاها":"Errors",
  "سلامت سرویس":"Service health",
  "وضعیت اجرا":"Runtime status",
  "در حال بررسی":"Checking",
  "سلامت کلی سیستم":"Overall system health",
  "مدت روشن بودن":"Uptime",
  "هسته‌های پردازنده":"CPU cores",
  "رم مصرفی پنل":"Panel RAM usage",
  "سرویس ربات":"Bot service",
  "فروش و مدیریت":"Sales & management",
  "ربات تلگرام":"Telegram bot",
  "شبکه و ترافیک":"Network & traffic",
  "بار سرور و مصرف کل":"Server load & total usage",
  "بار سیستم":"System load",
  "مجموع کل ترافیک":"Total traffic",
  "فعالیت لحظه‌ای":"Live activity",
  "مشاهده همه ›":"View all ›",
  "دسترسی سریع":"Quick access",
  "ساخت کانفیگ":"Create config",
  "افزودن نود":"Add node",
  "نودها":"Nodes",
  "جستجوی اینباند / UUID...":"Search inbound / UUID...",
  "مدیریت پراکسی‌های SOCKS5 (خروجی)":"Manage SOCKS5 proxies (outbound)",
  "اوتباند":"Outbound",
  "منقضی":"Expired",
  "جدیدترین":"Newest",
  "پرمصرف‌ترین":"Highest usage",
  "نزدیک انقضا":"Expiring soon",
  "نام (الفبا)":"Name (A–Z)",
  "انتخاب همه":"Select all",
  "خروجی (Outbound)":"Outbound",
  "یک اینباند را انتخاب کن و از روی همان کلاینت‌های واقعی (زیرمجموعه) بساز؛ بدون نیاز به رفتن به صفحه اینباندها.":"Pick an inbound and create real clients (sub-users) from it, without going to the Inbounds page.",
  "انتخاب اینباند":"Select inbound",
  "— انتخاب کنید —":"— Select —",
  "اینجا همه حساب‌های مدیریتی پنل را مرتب و دقیق مدیریت می‌کنیم؛ از ساخت ادمین تا تعیین دسترسی و کنترل وضعیت حساب.":"Manage every panel admin account here, from creating admins to setting access and account status.",
  "همگام‌سازی":"Sync",
  "ایجاد حساب مدیریتی":"Create admin account",
  "مدیریت کامل ادمین‌ها":"Full admin management",
  "حساب اصلی پنل دسترسی کامل دارد و برای هر ادمین می‌توان دسترسی‌های موردنیاز را جداگانه تعیین کرد. وضعیت هر حساب و آخرین ورود نیز از همین بخش قابل بررسی است.":"The main account has full access, and each admin can be given separate permissions. Each account's status and last login can also be checked here.",
  "تفکیک دسترسی":"Permission separation",
  "ثبت آخرین ورود":"Last login tracking",
  "امنیت حساب‌ها":"Account security",
  "حساب مدیریتی":"Admin account",
  "حساب فعال":"Active account",
  "مالک پنل":"Panel owner",
  "درخواست‌های ثبت‌نام ادمینی":"Admin signup requests",
  "افرادی که از صفحه ورود درخواست همکاری داده‌اند؛ بررسی کن و تصمیم بگیر.":"People who requested to join from the login page; review and decide.",
  "۰ درخواست":"0 requests",
  "فهرست ادمین‌ها":"Admin list",
  "وضعیت، دسترسی و فعالیت هر ادمین را از یکجا بررسی و مدیریت کن.":"Review and manage every admin's status, permissions and activity in one place.",
  "محدود به اینباند":"Inbound-restricted",
  "دسترسی به همه":"Access to all",
  "چند پنل VodiWalker را به هم وصل کن و همه را از یک پنل مدیریت کن.":"Connect multiple VodiWalker panels together and manage them all from one panel.",
  "بررسی همه":"Check all",
  "توکن این پنل (وقتی این پنل «نود» است)":"This panel's token (when this panel is a \"node\")",
  "توکن را کپی کن و در پنل اصلی، بخش نودها، بچسبان":"Copy the token and paste it in the main panel, Nodes section",
  "نودهای متصل به این پنل":"Nodes connected to this panel",
  "وضعیت هر ۳۰ ثانیه به‌روز می‌شود · «مدیریت» کل پنل را روی همان نود اجرا می‌کند":"Status refreshes every 30 seconds · \"Manage\" runs the whole panel on that node",
  "لاگ فعالیت‌ها":"Activity log",
  "تنظیمات ظاهری فقط برای همین مرورگر ذخیره می‌شوند و بدون دست‌زدن به اطلاعات سرور قابل تغییرند.":"Appearance settings are stored only in this browser and can be changed without touching server data.",
  "پشتیبانی و برند اشتراک":"Support & subscription branding",
  "آیدی تلگرام پشتیبانِ شما در صفحه‌ی اشتراک مشتری‌ها نمایش داده می‌شود و با یک کلیک مستقیم به همان آیدی در تلگرام می‌روند.":"Your Telegram support ID is shown on customers' subscription page, and one click takes them straight to that ID in Telegram.",
  "آیدی تلگرام پشتیبان":"Support Telegram ID",
  "آیدی کانال اطلاع‌رسانی (اختیاری)":"Announcement channel ID (optional)",
  "استایل خودکار نام کانفیگ‌ها":"Automatic config name style",
  "اسم ساده مثل VodiWalker به‌صورت VodiWalker|Tofan🚀 با اسم و ایموجی خفن ساخته می‌شود (دستی و خودکار)":"A simple name like VodiWalker is turned into VodiWalker|Tofan🚀 with a stylish name and emoji (manual and automatic)",
  "پیش‌نمایش در اپ کاربر":"Preview in the user app",
  "پشتیبانی: @VodiWalker":"Support: @VodiWalker",
  "ذخیره پشتیبانی و نام‌ها":"Save support & names",
  "تست لینک پشتیبان":"Test support link",
  "نام دلخواه یا برند شما":"Custom name or your brand",
  "مثلاً ۵۰ گیگابایت":"e.g. 50 GB",
  "شناسه کوتاه یکتا":"Unique short ID",
  "نام اینباند مادر این کانفیگ":"This config's parent inbound name",
  "پیش‌نمایش داخل اپ کاربر":"Preview inside the user app",
  "ترتیب نمایش دقیقاً همین ترتیب بالاست؛ بین هر بخش یک خط جداکننده (|) قرار می‌گیرد.":"Display order is exactly the order above; a separator (|) is placed between sections.",
  "سرور اطلاعاتی (Vodiwalkerpanel)":"Info server (Vodiwalkerpanel)",
  "یک ردیف تزئینی و همیشه غیرقابل‌اتصال (آدرس 0.0.0.0) که در ابتدای هر لیست سرور اضافه می‌شود تا کاربر حجم/زمان باقی‌مانده‌اش را همان‌جا ببیند، بدون نیاز به باز کردن مرورگر.":"A decorative, always-unconnectable row (address 0.0.0.0) added at the top of every server list so users can see their remaining data/time right there without opening a browser.",
  "نمایش سرور اطلاعاتی":"Show info server",
  "خاموش کن تا اصلاً اضافه نشود":"Turn off to skip adding it entirely",
  "مصرف‌شده / کل / باقی‌مانده":"Used / Total / Remaining",
  "نمایش زمان باقی‌مانده":"Show remaining time",
  "تا تاریخ انقضا":"Until expiry date",
  "ذخیره تنظیمات سرور اطلاعاتی":"Save info server settings",
  "پراکسی IP (SOCKS) — مسیر خروجی":"IP proxy (SOCKS) — outbound route",
  "وقتی یک SOCKS5 اینجا اضافه کنی، یک تونل واقعی از داخلش باز می‌شه و «پینگ واقعی» + «کشور و پرچم IP خروجی» نشون داده می‌شه. بعد هر بار که «ساخت سریع»، «اینباند جدید» یا «ساخت کلاینت» می‌زنی، می‌پرسه می‌خوای با این پراکسی (روی کشور دیگه) ساخته بشه یا مستقیم از خود Railway.":"When you add a SOCKS5 here, a real tunnel is opened through it and the \"real ping\" + \"exit IP country and flag\" are shown. Then every time you press \"Quick create\", \"New inbound\" or \"Create client\", it asks whether to build it through this proxy (on another country) or directly from Railway itself.",
  "نام دلخواه":"Custom name",
  "مثلاً آلمان-۱":"e.g. Germany-1",
  "1.2.3.4  یا  socks5://user:pass@host:1080":"1.2.3.4  or  socks5://user:pass@host:1080",
  "افزودن و تست پینگ":"Add & test ping",
  "پراکسی‌های ذخیره‌شده":"Saved proxies",
  "تست همه":"Test all",
  "در حال بارگذاری...":"Loading...",
  "ویرایش متن‌های ربات قفل شده است.":"Editing bot texts is locked.",
  "زمان درخواست تمام شد؛ اتصال را بررسی کن":"Request timed out; check the connection",
  "پوسته روشن و کاملاً سفید فعال شد ✓":"Light theme (pure white) enabled ✓",
  "پوسته تیره فعال شد ✓":"Dark theme enabled ✓",
  "کانال رسمی، اطلاع‌رسانی بروزرسانی‌ها و حمایت از پروژه":"Official channel, update announcements and project support",
  "ساخت کلاینت واقعی از روی اینباند دلخواه، جدا از صفحه اینباندها":"Create a real client from any inbound, separate from the Inbounds page",
  "اتصال چند پنل VodiWalker به هم و مدیریت یکجا":"Connect several VodiWalker panels and manage them in one place",
  "پیش‌نمایش:":"Preview:",
  "کپی نشد؛ دستی انتخاب و کپی کن":"Copy failed; select and copy manually",
  "این پنل فعلاً به‌عنوان «نود» قابل‌اتصال نیست. برای اینکه پنل اصلی بتواند این پنل را مدیریت کند، یک توکن بساز.":"This panel can't be connected as a \"node\" yet. Generate a token so the main panel can manage this panel.",
  "ساخت توکن نود":"Generate node token",
  "آدرس این پنل":"This panel's URL",
  "توکن API نود":"Node API token",
  "توکن کپی شد ✓":"Token copied ✓",
  "کپی توکن":"Copy token",
  "۱) کپی":"1) Copy",
  "آدرس و توکن بالا را کپی کن.":"Copy the URL and token above.",
  "۲) پنل اصلی":"2) Main panel",
  "در پنل اصلی برو به «نودها» ← «افزودن نود».":"In the main panel go to \"Nodes\" ← \"Add node\".",
  "۳) پیست":"3) Paste",
  "آدرس و توکن را بچسبان و «تست اتصال» را بزن.":"Paste the URL and token, then press \"Test connection\".",
  "ساخت مجدد (توکن قبلی باطل می‌شود)":"Regenerate (the previous token is invalidated)",
  "توکن قبلی همین الان باطل می‌شود و پنل‌های اصلی که با آن وصل‌اند قطع می‌شوند. ادامه بدهم؟":"The previous token is revoked immediately and main panels connected with it will be disconnected. Continue?",
  "توکن جدید ساخته شد ✓":"New token generated ✓",
  "توکن ساخته شد ✓":"Token generated ✓",
  "با غیرفعال‌سازی، هیچ پنل اصلی‌ای دیگر به این پنل دسترسی ندارد. ادامه بدهم؟":"Once disabled, no main panel can access this panel anymore. Continue?",
  "توکن نود غیرفعال شد":"Node token disabled",
  "پینگ":"Ping",
  "آپتایم":"Uptime",
  "هنوز نودی اضافه نشده. روی «افزودن نود» بزن و آدرس + توکن پنل دیگر را بچسبان.":"No node added yet. Press \"Add node\" and paste the other panel's URL + token.",
  "در حال مدیریت":"Managing",
  "مدیریت":"Manage",
  "بررسی":"Check",
  "وضعیت نودها به‌روز شد ✓":"Node status updated ✓",
  "نود حذف شد":"Node removed",
  "ویرایش نود":"Edit node",
  "نام نود":"Node name",
  "مثلاً: آلمان-۱":"e.g. Germany-1",
  "آدرس پنل نود":"Node panel URL",
  "خالی = بدون تغییر (":"Empty = unchanged (",
  "از پنل نود: تب «نودها» ← «ساخت توکن نود» ← کپی.":"From the node panel: \"Nodes\" tab ← \"Generate node token\" ← copy.",
  "تست اتصال":"Test connection",
  "⚠️ با http توکن بدون رمزنگاری می‌رود؛ اگر نود روی اینترنت است حتماً https بگذار.":"⚠️ Over http the token travels unencrypted; if the node is on the internet, use https.",
  "اتصال ناموفق":"Connection failed",
  "نود اضافه شد و آنلاین است ✓":"Node added and online ✓",
  "نود ذخیره شد ولی آنلاین نیست:":"Node saved but not online:",
  "در حال مدیریت نود":"Managing node",
  "— همه‌ی تغییرات روی سرور آن نود اعمال می‌شود.":"— all changes are applied on that node's server.",
  "بازگشت به این پنل":"Back to this panel",
  "این پنل":"This panel",
  "پنل محلی (سرور فعلی)":"Local panel (current server)",
  "انتخاب پنل برای مدیریت":"Choose panel to manage",
  "با انتخاب یک نود، تمام صفحات (اینباند، ساب، پراکسی، آمار) روی همان نود کار می‌کنند.":"When you select a node, all pages (inbounds, subs, proxies, stats) work on that node.",
  "صفحه‌ی نودها":"Nodes page",
  "برو":"Go",
  "کپی نشد":"Copy failed",
  "سالم":"Healthy",
  "بار متوسط":"Medium load",
  "بار بالا":"High load",
  "متصل":"Connected",
  "آنلاین همین الان":"Online right now",
  "لینکی برای کپی وجود ندارد":"No link to copy",
  "آماده":"Ready",
  "⚠️ پراکسی نامعتبر":"⚠️ Invalid proxy",
  "خروجی مستقیم":"Direct outbound",
  "🚀 مستقیم":"🚀 Direct",
  "بدون دسته":"No category",
  "٪ مصرف‌شده":"% used",
  "بدون سقف حجم":"No data cap",
  "باقی‌مانده:":"Remaining:",
  "اشتراک و QR":"Subscription & QR",
  "تعویض لینک (UUID جدید)":"Replace link (new UUID)",
  "ریست حجم مصرفی":"Reset used traffic",
  "هنوز کلاینتی برای این اینباند ساخته نشده.":"No clients created for this inbound yet.",
  "این کلاینت از کجا خارج شود؟":"Where should this client exit?",
  "لینک اشتراک این کاربر (۱ WS + ۱ XHTTP)":"This user's subscription link (1 WS + 1 XHTTP)",
  "این اینباند بخشی از یک جفت WS+XHTTP است؛ برای همین به‌جای دو کلاینت جدا، هر دو در یک لینک اشتراک قرار گرفتند.":"This inbound is part of a WS+XHTTP pair; so instead of two separate clients, both were placed in one subscription link.",
  "یک لینک/UUID جدید برای این کلاینت صادر شود؟ لینک قبلی بلافاصله از کار می‌افتد و باید لینک جدید را دوباره برای کاربر بفرستید.":"Issue a new link/UUID for this client? The previous link stops working immediately and you must send the new link to the user again.",
  "لینک کلاینت تعویض شد ✓":"Client link replaced ✓",
  "حجم مصرفی این کلاینت از صفر شروع شود؟":"Restart this client's used traffic from zero?",
  "حجم مصرف ریست شد ✓":"Used traffic reset ✓",
  "ابتدا یک اینباند را از بالا انتخاب کن":"First select an inbound from the top",
  "کلاینت‌های این اینباند":"This inbound's clients",
  "کپی کنید:":"Copy:",
  "لینک ساب برای این کلاینت در دسترس نیست":"Sub link is not available for this client",
  "لینک ساب":"Sub link",
  "یک لینک برای اپ و مرورگر":"One link for app and browser",
  "داخل اپ (v2rayNG، Hiddify، …) همین لینک کانفیگ‌ها را بالا می‌آورد.":"Inside an app (v2rayNG, Hiddify, …) this link loads the configs.",
  "داخل مرورگر همین لینک صفحه‌ی گرافیکی حجم و زمان باقی‌مانده را نشان می‌دهد.":"In a browser this same link shows a graphical page with remaining data and time.",
  "حجم مصرفی این کانفیگ از صفر شروع شود؟":"Restart this config's used traffic from zero?",
  "حجم مصرف ریست شد":"Used traffic reset",
  "یک لینک/UUID جدید صادر شود؟ لینک قبلی بلافاصله از کار می‌افتد و باید لینک جدید را دوباره برای کاربر بفرستید.":"Issue a new link/UUID? The previous link stops working immediately and you must send the new link to the user again.",
  "لینک جدید صادر شد":"New link issued",
  "ساخت سریع — WS + XHTTP در یک اشتراک":"Quick create — WS + XHTTP in one subscription",
  "خروجی را انتخاب کن؛ می‌توانی چند خروجی هم‌زمان بزنی (برای هرکدام یک WS + یک XHTTP).":"Choose the outbound; you can pick several at once (one WS + one XHTTP for each).",
  "مستقیم":"Direct",
  "خود Railway":"Railway itself",
  "همین اشتراک در تب «گروه‌های ساب» هم دیده می‌شود.":"This subscription also appears in the \"Sub groups\" tab.",
  "خطا در دریافت لیست":"Error loading list",
  "تست‌نشده":"Untested",
  "قطع":"Down",
  "🚀 مستقیم (خود Railway)":"🚀 Direct (Railway itself)",
  "هنوز پراکسی‌ای اضافه نشده. با فرم بالا یک SOCKS5 اضافه کن.":"No proxy added yet. Add a SOCKS5 with the form above.",
  "کشور نامشخص":"Unknown country",
  "· IP خروجی:":"· Exit IP:",
  "TLS رهگیری‌شده ⚠":"TLS intercepted ⚠",
  "موقتاً قطع‌شده (circuit)":"Temporarily down (circuit)",
  "پینگ واقعی":"Real ping",
  "امتیاز کیفیت":"Quality score",
  "تست":"Test",
  "انتخاب پیش‌فرض در پنجره‌ی «ساخت سریع»":"Preselect in the \"Quick create\" window",
  "در حال تست تونل SOCKS5 و کشور خروجی...":"Testing SOCKS5 tunnel and exit country...",
  "تست ناموفق":"Test failed",
  "پراکسی‌ای برای تست نیست":"No proxy to test",
  "در حال تست همه‌ی پراکسی‌ها...":"Testing all proxies...",
  "این پراکسی حذف شود؟":"Delete this proxy?",
  "این پراکسی در پنجره‌ی «ساخت سریع» از قبل انتخاب می‌شود ✓":"This proxy will be preselected in the \"Quick create\" window ✓",
  "آدرس پراکسی را وارد کنید":"Enter the proxy address",
  "پراکسی اضافه شد — در حال تست...":"Proxy added — testing...",
  "هنوز پراکسی‌ای اضافه نشده؛ اول یک SOCKS5 اضافه کن":"No proxy added yet; add a SOCKS5 first",
  "مسیر خروجی":"Outbound route",
  "ترافیک از کجا خارج شود؟":"Where should traffic exit?",
  "ادامه":"Continue",
  "حداقل یک گزینه را انتخاب کن":"Select at least one option",
  "مستقیم (خود Railway)":"Direct (Railway itself)",
  "ترافیک از IP سرور Railway خارج می‌شود":"Traffic exits from the Railway server IP",
  "اوتباند — پراکسی‌ها (SOCKS5 · SOCKS4 · HTTP)":"Outbound — Proxies (SOCKS5 · SOCKS4 · HTTP)",
  "هر پراکسی که اینجا اضافه کنی تست واقعی می‌شود (پینگ از داخل تونل، کشور/پرچم/ISP خروجی، امتیاز کیفیت). بعد می‌توانی هر اینباند/کلاینت را روی آن بگذاری. برای افزودن تکیِ HTTP یا SOCKS4 آدرس کامل را بنویس، مثلاً http://user:pass@1.2.3.4:8080":"Every proxy you add here gets a real test (ping from inside the tunnel, exit country/flag/ISP, quality score). Then you can assign any inbound/client to it. To add a single HTTP or SOCKS4 proxy, write the full address, e.g. http://user:pass@1.2.3.4:8080",
  "افزودن تکی":"Add single",
  "اسکن و افزودن گروهی":"Scan & bulk add",
  "Host / آدرس کامل":"Host / full address",
  "افزودن و تست":"Add & test",
  "لیست پراکسی‌های خودت را (پیست یا لینک لیست سرویس‌دهنده‌ات) بده؛ همه موازی و زنده با تونل واقعی تست می‌شوند: پروتکل، پینگ و پایداری، کشور/شهر/ISP خروجی، رهگیری TLS و امتیاز کیفیت. پراکسی رایگان عمومی از اینترنت جمع‌آوری نمی‌کنیم و آدرس‌های داخلی/لوکال رد می‌شوند.":"Provide your own proxy list (paste it or a link from your provider); all are tested in parallel with a real live tunnel: protocol, ping and stability, exit country/city/ISP, TLS interception and quality score. We do not collect free public proxies from the internet, and internal/local addresses are rejected.",
  "پیست لیست":"Paste list",
  "از یک URL":"From a URL",
  "تشخیص خودکار":"Auto-detect",
  "دقت تست":"Test accuracy",
  "سریع (۱ نمونه)":"Fast (1 sample)",
  "متعادل (۳ نمونه)":"Balanced (3 samples)",
  "دقیق (۵ نمونه)":"Precise (5 samples)",
  "هم‌زمانی":"Concurrency",
  "کم (۲۰)":"Low (20)",
  "متوسط (۴۰)":"Medium (40)",
  "زیاد (۸۰)":"High (80)",
  "بررسی رهگیری TLS":"Check TLS interception",
  "تست سرعت دانلود":"Download speed test",
  "شروع اسکن":"Start scan",
  "لغو اسکن":"Cancel scan",
  "آدرس لیست را وارد کن":"Enter the list URL",
  "لیست پروکسی را پیست کن":"Paste the proxy list",
  "در حال شروع...":"Starting...",
  "در حال اسکن...":"Scanning...",
  "بررسی‌شده":"checked",
  "ناموفق":"Failed",
  "پرریسک":"High risk",
  "لیست بلندتر از سقف مجاز بود؛ فقط بخش اول بررسی می‌شود.":"The list exceeded the allowed limit; only the first part is checked.",
  "نتیجه‌ای نیست":"No results",
  "فقط سالم‌ها":"Healthy only",
  "فقط کیفیت A و B":"Quality A and B only",
  "همه‌ی نتیجه‌ها":"All results",
  "انتخاب A/B":"Select A/B",
  "همه/هیچ":"All/None",
  "کپی لیست سالم‌ها":"Copy healthy list",
  "افزودن انتخاب‌شده‌ها":"Add selected",
  "موردی با این فیلتر نیست":"No items match this filter",
  "حداقل یک پراکسی سالم را انتخاب کن":"Select at least one healthy proxy",
  "پراکسی سالمی برای کپی نیست":"No healthy proxy to copy",
  "WS + XHTTP (یک اشتراک)":"WS + XHTTP (one subscription)",
  "دستی پیشرفته":"Advanced manual",
  "مستقیم از Railway یا از پراکسی SOCKS5 — هر تعداد که بخواهی انتخاب کن":"Direct from Railway or via a SOCKS5 proxy — choose as many as you like",
  "مدیریت / افزودن پراکسی":"Manage / add proxy",
  "مشخصات":"Details",
  "برای هر کانفیگ WS و XHTTP جداگانه اعمال می‌شود (حجم، سرعت، محدودیت‌ها)":"Applied separately to each WS and XHTTP config (data, speed, limits)",
  "خالی = نام تصادفی":"Empty = random name",
  "تعداد کل کانفیگ (WS+XHTTP)":"Total config count (WS+XHTTP)",
  "مثلاً 4 یعنی داخل همین اشتراک ۲ تا WS و ۲ تا XHTTP باشد؛ برای هر خروجی جدا اعمال می‌شود.":"e.g. 4 means 2 WS and 2 XHTTP inside this subscription; applied separately for each outbound.",
  "محدودیت ادمین (اختیاری)":"Admin restriction (optional)",
  "این اینباند فقط برای یک ادمین مشخص باشد":"Restrict this inbound to one specific admin",
  "— بدون محدودیت —":"— No restriction —",
  "حالت":"Mode",
  "فقط همین اینباند (جایگزین محدودیت قبلی)":"This inbound only (replaces the previous restriction)",
  "علاوه بر دسترسی‌های فعلی":"In addition to current access",
  "⚠️ حداقل یک خروجی انتخاب کن":"⚠️ Select at least one outbound",
  "حداقل یک خروجی انتخاب کن":"Select at least one outbound",
  "خطا در ساخت اشتراک":"Error creating subscription",
  "خروجی این اینباند":"Outbound of this inbound",
  "کلاینت‌های زیرمجموعه هم همین خروجی را می‌گیرند. اتصال‌های فعلی از اتصال بعدی روی خروجی جدید می‌روند.":"Sub-clients get the same outbound. Existing connections move to the new outbound on their next connection.",
  "مسیر خروجی (Outbound) — مستقیم یا پراکسی؟":"Outbound route — direct or proxy?",
  "🚀 مستقیم (Railway)":"🚀 Direct (Railway)",
  "اگه یک پراکسی انتخاب کنی، اتصال به مقصد از طریق همون SOCKS5 رد می‌شه (روی کشور اون پراکسی ظاهر می‌شه). از تب «تنظیمات» پراکسی اضافه/تست کن.":"If you pick a proxy, the connection to the destination goes through that SOCKS5 (appearing from that proxy's country). Add/test proxies from the \"Settings\" tab.",
  "خالی = مسیر خودکار سرور (پیشنهادی)":"Empty = server auto route (recommended)",
  "Shadowsocks در این سازنده فقط با TCP پشتیبانی می‌شود":"Shadowsocks is supported in this builder over TCP only",
  "خطا در تست TCP":"TCP test error",
  "اعضا":"Members",
  "مثلاً: بسته-VIP":"e.g. VIP-bundle",
  "بعد از ساخت گروه، از دکمه‌ی «اعضا» می‌توانی اینباندهای این پنل و نودهای دیگر را داخلش بگذاری.":"After creating the group, use the \"Members\" button to add inbounds from this panel and other nodes.",
  "گروه پیدا نشد":"Group not found",
  "· این پنل":"· This panel",
  "هنوز اینباندی از این پنل اضافه نشده":"No inbound from this panel added yet",
  "هنوز اینباندی از نود دیگر وصل نشده":"No inbound from another node connected yet",
  "خروجی‌های این اشتراک (WS+XHTTP)":"This subscription's outbounds (WS+XHTTP)",
  "افزودن خروجی":"Add outbound",
  "هر پروکسی که تیک بزنی — یا «مستقیم» — یک WS و یک XHTTP تازه با همون تنظیمات به همین اشتراک اضافه می‌شود.":"Each proxy you tick — or \"Direct\" — adds a fresh WS and XHTTP with the same settings to this subscription.",
  "بروزرسانی از نود":"Refresh from node",
  "افزودن از نود":"Add from node",
  "این دقیقاً همان قابلیت «Nodes» است: یک اینباند اینجا + یک اینباند روی یک پنل دیگر، هر دو در یک لینک اشتراک.":"This is exactly the \"Nodes\" feature: one inbound here + one inbound on another panel, both in one subscription link.",
  "همه‌ی خروجی‌های موجود قبلاً روی این اشتراک هستند":"All available outbounds are already on this subscription",
  "افزودن خروجی به این اشتراک":"Add outbound to this subscription",
  "هرچقدر پروکسی می‌خواهی تیک بزن؛ اگر «مستقیم» را هم بخواهی علاوه بر پروکسی‌ها، همان بالا را هم تیک بزن.":"Tick as many proxies as you like; if you also want \"Direct\" in addition to the proxies, tick it at the top.",
  "حداقل یک خروجی تیک بزن":"Tick at least one outbound",
  "همه‌ی این خروجی‌ها قبلاً روی این اشتراک بودند":"All of these outbounds were already on this subscription",
  "اینباند دیگری در این پنل نیست":"No other inbound in this panel",
  "افزودن از این پنل":"Add from this panel",
  "حداقل یک اینباند انتخاب کن":"Select at least one inbound",
  "نودی آنلاین برای انتخاب نیست؛ اول از تب «نودها» یک نود وصل کن":"No online node to choose; first connect a node from the \"Nodes\" tab",
  "افزودن از نود — انتخاب نود":"Add from node — choose node",
  "بعدی: انتخاب اینباند":"Next: select inbound",
  "یک نود انتخاب کن":"Select a node",
  "این نود اینباند دیگری برای افزودن ندارد":"This node has no other inbound to add",
  "ساخت کلاینت (بخش جدا)":"Create client (separate section)",
  "بدون ورود":"No login",
  "دسترسی کامل":"Full access",
  "بدون دسترسی":"No access",
  "ویرایش دسترسی":"Edit access",
  "اینباند معتبری یافت نشد":"No valid inbound found",
  "اینباند مجاز":"Allowed inbound",
  "محدودیت اینباند":"Inbound restriction",
  "بدون محدودیت":"No restriction",
  "٪ از اینباندها":"% of inbounds",
  "دسترسی‌ها":"Permissions",
  "ابتدا حداقل یک اینباند بساز":"First create at least one inbound",
  "محدود به اینباند(های) خاص":"Restricted to specific inbound(s)",
  "(خالی = دسترسی به همه)":"(empty = access to all)",
  "ساخت اینباند جدید":"Create new inbound",
  "ویرایش/تغییر وضعیت کلاینت":"Edit / toggle client status",
  "ریست مصرف کلاینت":"Reset client usage",
  "مدیریت خروجی/پراکسی":"Manage outbound / proxy",
  "اتصال‌های زنده و IP":"Live connections & IPs",
  "درخواست":"Request",
  "تایید و ساخت ادمین":"Approve & create admin",
  "رد":"Reject",
  "تایید شده":"Approved",
  "رد شده":"Rejected",
  "درخواستی ثبت نشده است":"No requests registered",
  "تایید ادمین:":"Approve admin:",
  "درخواست‌کننده":"Requester",
  "شارژ اولیه (استارز)":"Initial credit (Stars)",
  "تایید و ساخت حساب":"Approve & create account",
  "اطلاعات ورود ادمین":"Admin login details",
  "این متن را برای":"Send this text to",
  "در تلگرام ارسال کن:":"on Telegram:",
  "کپی متن":"Copy text",
  "این درخواست رد شود؟":"Reject this request?",
  "درخواست رد شد":"Request rejected",
  "ویرایش متن‌های ربات قفل شده است و امکان تغییر ندارد":"Editing bot texts is locked and cannot be changed",
  "ربات روشن است":"Bot is on",
  "پشتیبانی: @":"Support: @",
  "پشتیبانی و استایل نام‌ها ذخیره شد ✓":"Support & name style saved ✓",
  "اسم‌های خفن (کلیک کن)":"Cool names (click)",
  "پیشنهاد جدید":"New suggestion",
  "اسم انتخاب شد ✓":"Name selected ✓",
  "(غیرفعال — هیچ ردیفی اضافه نمی‌شود)":"(disabled — no row is added)",
  "12 GB/50 GB (باقی 38 GB)":"12 GB/50 GB (38 GB left)",
  "۱۲د ۴س":"12d 4h",
  "تنظیمات سرور اطلاعاتی ذخیره شد ✓":"Info server settings saved ✓",
  "خیلی ضعیف":"Very weak",
  "ضعیف":"Weak",
  "خوب":"Good",
  "قوی":"Strong",
  "خیلی قوی":"Very strong",
  "نور و عملکرد":"Light & performance",
  "شدت نور پس‌زمینه":"Background glow intensity",
  "حالت سبک (بدون انیمیشن)":"Lite mode (no animations)",
  "جستجو در اینباندها، کلاینت‌ها، دسته‌ها، نودها، تنظیمات…":"Search inbounds, clients, categories, nodes, settings…",
  "دسته و ساب":"Categories & subs",
  "نود / پراکسی / ادمین":"Node / proxy / admin",
  "صفحه و تنظیمات":"Pages & settings",
  "اقدام‌ها":"Actions",
  "نتایج جستجو":"Search results",
  "حرکت":"Navigate",
  "باز کردن":"Open",
  "صفحه":"Page",
  "اقدام":"Action",
  "نود":"Node",
  "پراکسی":"Proxy",
  "بخش":"Section",
  "رفتن به صفحه":"Go to page",
  "WS + XHTTP در یک اشتراک":"WS + XHTTP in one subscription",
  "ساخت گروه اشتراک":"Create subscription group",
  "افزودن مدیر":"Add admin",
  "مدیریت پراکسی‌ها و اسکنر":"Manage proxies & scanner",
  "اوتباند SOCKS / HTTP":"Outbound SOCKS / HTTP",
  "تغییر پوسته (روشن / تیره)":"Toggle theme (light / dark)",
  "بروزرسانی داده‌های صفحه":"Refresh page data",
  "اخیراً":"Recent",
  "اقدام‌های سریع":"Quick actions",
  "صفحه‌ها":"Pages",
  "نتیجه‌ای پیدا نشد":"No results found",
  "چیزی برای نمایش نیست":"Nothing to show",
  "املای دیگری امتحان کن یا فیلتر را روی «همه» بگذار.":"Try a different spelling or set the filter to \"All\".",
  "نتیجه":"Result",
  "مورد قابل جستجو":"searchable items",
  "این توکن فقط به بخش‌های عملیاتی (اینباند، پراکسی، ساب، آمار) دسترسی می‌دهد؛ رمز، ادمین‌ها و تنظیمات را باز نمی‌کند. مثل رمز نگهش دار.":"This token only grants access to operational sections (inbounds, proxies, subs, stats); it does not unlock the password, admins or settings. Keep it like a password.",
  "· ساخته‌شده:":"· Created:",
  "· توکن":"· token",
  "نود «":"Node \"",
  "» از این پنل حذف شود؟ (خودِ سرور نود و کانفیگ‌هایش دست‌نخورده می‌مانند.)":"\" be removed from this panel? (The node server itself and its configs remain untouched.)",
  "اتصال موفق · پینگ":"Connection OK · ping",
  "ms · نسخه":"ms · version",
  "| متوقف:":"| Stopped:",
  "خروجی از طریق پراکسی «":"Outbound via proxy \"",
  "پراکسی «":"Proxy \"",
  "لینک اشتراک (":"Subscription link (",
  "کانفیگ)":"configs)",
  "لیست پراکسی‌ها از سرور گرفته نشد:":"Could not load the proxy list from the server:",
  "— مطمئن شو outbound_proxy.py و python-socks روی سرور نصب/دیپلوی شده‌اند.":"— make sure outbound_proxy.py and python-socks are installed/deployed on the server.",
  "کانفیگ از این پراکسی استفاده می‌کنند":"configs use this proxy",
  "پراکسی سالم است":"proxies are working",
  "کانفیگ از این پراکسی استفاده می‌کنند و به حالت «مستقیم» برمی‌گردند.":"configs use this proxy and will revert to \"Direct\" mode.",
  "هر خط یک پروکسی — فرمت‌ها:":"One proxy per line — formats:",
  "در حال اسکن":"Scanning",
  "پراکسی…":"proxies…",
  "آدرس داخلی/لوکال به‌دلیل امنیت رد شد.":"internal/local addresses rejected for security.",
  "اسکن لغو شد —":"Scan cancelled —",
  "سالم از":"healthy out of",
  "اسکن تمام شد —":"Scan finished —",
  "افزودن همه‌ی کیفیت A/B (":"Add all A/B quality (",
  "مورد بعدی (":"next items (",
  "باقی‌مانده)":"remaining)",
  "پراکسی اضافه شد":"proxies added",
  "مورد تکراری رد شد)":"duplicates skipped)",
  "پراکسی کپی شد ✓":"proxies copied ✓",
  "خروجی ×":"outbounds ×",
  "کانفیگ → یک اشتراک با":"configs → one subscription with",
  "محلی":"local",
  "از نود":"from node",
  "اعضای «":"Members of \"",
  "اینباندهای این پنل (":"This panel's inbounds (",
  "اینباندهای روی نودهای دیگر (":"Inbounds on other nodes (",
  "خروجی تازه (":"new outbound (",
  "کانفیگ) اضافه شد ✓":"configs) added ✓",
  "اینباند اضافه شد ✓":"inbounds added ✓",
  "افزودن از نود «":"Add from node \"",
  "اضافه شد،":"added,",
  "مورد ناموفق:":"failed:",
  "اینباند از نود اضافه شد ✓":"inbounds added from node ✓",
  "نشست قبلی لغو شد ✓":"previous sessions revoked ✓",
  "تنظیم شد ✓":"updated ✓",
};

// ============================================================
// Stable dashboard language engine
// ============================================================
// The dashboard contains both static DOM and HTML that is created later by
// drawers, tables, API responses and toast messages.  Translation therefore
// uses one stateful engine for the whole dashboard document (not only #app).
// Each text node/attribute remembers its Persian source and its last rendered
// value.  This prevents EN -> FA loss and also lets dynamically updated nodes
// refresh correctly while English mode is active.
const DASH_NODE_STATE = new WeakMap();
const DASH_ATTR_STATE = new WeakMap();
const DASH_TERM_LIST = Object.keys(DASH_EN_TERMS).sort((a,b)=>b.length-a.length);
const DASH_TRANSLATABLE_ATTRS = ['placeholder','title','aria-label'];
let DASH_TRANSLATING = false;

// Word-safe substring replace: a term is only replaced when the character
// right before/after it is NOT another Persian letter. Without this guard a
// short dictionary entry like 'کل' ("total") would also match *inside* an
// unrelated word such as 'کلید' ("key") -> 'Totalید', silently corrupting
// text that has nothing to do with the term. Persian suffixes attached with
// a ZWNJ (e.g. 'کلاینت‌ها') still match correctly because \u200c is not a
// Persian letter and is left outside this guard.
const DASH_FA_LETTER_RE = /[\u0600-\u06FF]/;
function dashReplaceTermSafely(out, term, replacement){
  if(!out.includes(term)) return out;
  let result = '';
  let i = 0;
  const len = term.length;
  while(i < out.length){
    if(out.startsWith(term, i)){
      const before = i > 0 ? out[i - 1] : '';
      const after = out[i + len] || '';
      if(!DASH_FA_LETTER_RE.test(before) && !DASH_FA_LETTER_RE.test(after)){
        result += replacement;
        i += len;
        continue;
      }
    }
    result += out[i];
    i++;
  }
  return result;
}

const DASH_TR_CACHE = new Map();
function dashTranslateValue(value, lang){
  if(lang !== 'en' || !value) return value || '';
  let out = String(value);
  if(!/[\u0600-\u06FF]/.test(out)) return out;
  if(DASH_TR_CACHE.has(out)) return DASH_TR_CACHE.get(out);
  const key = out;
  for(const term of DASH_TERM_LIST){
    out = dashReplaceTermSafely(out, term, DASH_EN_TERMS[term]);
  }
  out = out.replace(/(\d)\s*\u0627\u0632\s*(\d)/g,'$1 of $2').replace(/[\u06F0-\u06F9]/g,function(d){return String(d.charCodeAt(0)-0x06F0)});
  if(DASH_TR_CACHE.size > 3000) DASH_TR_CACHE.clear();
  DASH_TR_CACHE.set(key, out);
  return out;
}

// Shorthand for one-off strings that never live in the DOM long enough for
// the tree-walker/observer to reach them — native confirm()/prompt() dialogs
// in particular. Translates against the current dashboard language.
function t(fa){
  return dashTranslateValue(fa, typeof getDashLang === 'function' ? getDashLang() : 'fa');
}

function dashShouldTranslateElement(el){
  if(!el) return false;
  if(/^(SCRIPT|STYLE|NOSCRIPT)$/i.test(el.tagName)) return false;
  if(el.closest('[data-no-translate],.mono,[data-i18n]')) return false;
  return true;
}

function dashRenderTextNode(textNode, lang){
  if(!textNode || !textNode.parentElement || !dashShouldTranslateElement(textNode.parentElement)) return;
  const current = textNode.nodeValue || '';
  let state = DASH_NODE_STATE.get(textNode);
  if(!state){
    state = {fa: current, last: current};
    DASH_NODE_STATE.set(textNode, state);
  }else if(current !== state.last){
    // The node was changed by application code. Treat the new value as the
    // canonical Persian source rather than translating an old snapshot.
    state.fa = current;
  }
  const next = lang === 'en' ? dashTranslateValue(state.fa,'en') : state.fa;
  state.last = next;
  if(current !== next) textNode.nodeValue = next;
}

function dashRenderAttr(el, attr, lang){
  if(!el || el.matches('[data-no-translate],.mono,[data-i18n]')) return;
  if(!el.hasAttribute(attr)) return;
  const current = el.getAttribute(attr) || '';
  let attrs = DASH_ATTR_STATE.get(el);
  if(!attrs){ attrs = {}; DASH_ATTR_STATE.set(el, attrs); }
  let state = attrs[attr];
  if(!state){
    state = {fa: current, last: current};
    attrs[attr] = state;
  }else if(current !== state.last){
    state.fa = current;
  }
  const next = lang === 'en' ? dashTranslateValue(state.fa,'en') : state.fa;
  state.last = next;
  if(current !== next) el.setAttribute(attr,next);
}

function translateDashTree(lang){
  const root=document.body;
  if(!root || DASH_TRANSLATING) return;
  DASH_TRANSLATING = true;
  try{
    const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
    const nodes=[];
    let node;
    while((node=walker.nextNode())) nodes.push(node);
    for(const textNode of nodes) dashRenderTextNode(textNode,lang);

    root.querySelectorAll('input,textarea,button,[aria-label],select').forEach(el=>{
      for(const attr of DASH_TRANSLATABLE_ATTRS) dashRenderAttr(el,attr,lang);
    });

    root.querySelectorAll('option').forEach(option=>dashRenderTextNode(option.firstChild || option,lang));
  }finally{
    DASH_TRANSLATING = false;
  }
}

function setDashI18nElement(el, key, lang){
  if(!el || !key) return;
  const fa = DASH_I18N.fa?.[key];
  const en = DASH_I18N.en?.[key];
  if(fa === undefined && en === undefined) return;
  if(fa !== undefined) el.dataset.vwFa = String(fa);
  if(en !== undefined) el.dataset.vwEn = String(en);
  const next = lang === 'en' ? (en ?? fa ?? '') : (fa ?? '');
  el.textContent = String(next);
}

function updatePageTitle(pg){
  const mainEl = document.getElementById('pageTitleMain');
  const subEl = document.getElementById('pageTitleSub');
  const lang = getDashLang();
  if(mainEl) setDashI18nElement(mainEl, 'nav_'+pg, lang);
  if(subEl) setDashI18nElement(subEl, 'pt_'+pg, lang);
}

function applyDashLang(lang){
  lang = lang === 'en' ? 'en' : 'fa';
  const dictionary = DASH_I18N[lang] || DASH_I18N.fa;
  document.documentElement.setAttribute('dir', dictionary.dir || (lang==='fa'?'rtl':'ltr'));
  document.documentElement.setAttribute('lang', lang);
  document.body.classList.toggle('dash-en', lang==='en');
  document.getElementById('dashLangFa')?.classList.toggle('on', lang==='fa');
  document.getElementById('dashLangEn')?.classList.toggle('on', lang==='en');

  document.querySelectorAll('#app [data-i18n]').forEach(el=>{
    setDashI18nElement(el, el.getAttribute('data-i18n'), lang);
  });
  updatePageTitle(CURRENT_PAGE);
  translateDashTree(lang);
  try{ localStorage.setItem('vw_dash_lang',lang); }catch(e){}
}

function getDashLang(){
  try{ return localStorage.getItem('vw_dash_lang') === 'en' ? 'en' : 'fa'; }
  catch(e){ return 'fa'; }
}

function setDashLang(lang){
  applyDashLang(lang);
}

let dashTranslateObserver=null;
let dashTranslateQueued=false;
function enableDashTranslation(){
  if(dashTranslateObserver) dashTranslateObserver.disconnect();
  const root=document.getElementById('app') || document.body;
  if(!root) return;
  let pending=[];
  dashTranslateObserver=new MutationObserver(mutations=>{
    if(getDashLang()!=='en' || DASH_TRANSLATING) return;
    for(const m of mutations){ for(const n of m.addedNodes){ if(n.nodeType===1||n.nodeType===3) pending.push(n); } }
    if(!pending.length || dashTranslateQueued) return;
    dashTranslateQueued=true;
    const run=()=>{
      dashTranslateQueued=false;
      const list=pending; pending=[];
      if(getDashLang()!=='en') return;
      DASH_TRANSLATING=true;
      try{
        for(const n of list){
          if(!n.isConnected) continue;
          if(n.nodeType===3){ dashRenderTextNode(n,'en'); continue; }
          const w=document.createTreeWalker(n,NodeFilter.SHOW_TEXT); let t;
          while((t=w.nextNode())) dashRenderTextNode(t,'en');
          n.querySelectorAll('input,textarea,button,[aria-label],select').forEach(el=>{ for(const a of DASH_TRANSLATABLE_ATTRS) dashRenderAttr(el,a,'en'); });
        }
      }finally{ DASH_TRANSLATING=false; }
    };
    if(window.requestIdleCallback) requestIdleCallback(run,{timeout:400}); else setTimeout(run,60);
  });
  dashTranslateObserver.observe(root,{subtree:true,childList:true});
}

// Apply the saved language only after the dashboard DOM exists.
applyDashLang(getDashLang());
enableDashTranslation();

// ══════════════════════════════ نودها (اتصال چند پنل) ══════════════════════════════
// این پنل هم می‌تواند «نود» باشد (توکن می‌سازد و کپی می‌کنی) و هم «اصلی» (آدرس + توکن نودها را می‌گیرد).
let NODES_LIST = [];
let NODE_TOKEN = {enabled:false, token:null, created_at:null};
let NODE_TOKEN_SHOWN = false;
let NODES_TIMER = null;

function nodeStyle(){
  if(document.getElementById('ndStyle')) return;
  const st = document.createElement('style'); st.id = 'ndStyle';
  st.textContent = `
  .nd-banner{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 18px;background:linear-gradient(90deg,rgba(245,165,36,.18),rgba(245,165,36,.06));border-bottom:1px solid rgba(245,165,36,.4);font-size:13px}
  .nd-banner b{color:var(--warn)}
  .nd-banner .btn{margin-inline-start:auto}
  .nd-switch{display:inline-flex;align-items:center;gap:7px;padding:7px 12px;border:1px solid var(--line2);border-radius:11px;background:var(--panel2);color:var(--text);cursor:pointer;font-size:12.5px;font-weight:700;font-family:inherit}
  .nd-switch.remote{border-color:rgba(245,165,36,.6);color:var(--warn)}
  .nd-dot{width:9px;height:9px;border-radius:50%;background:var(--sub2);display:inline-block;flex:none}
  .nd-dot.on{background:var(--good);box-shadow:0 0 0 3px rgba(34,197,139,.18)}
  .nd-dot.off{background:var(--bad);box-shadow:0 0 0 3px rgba(242,73,85,.16)}
  .nd-tokenbox{display:flex;gap:8px;align-items:stretch;flex-wrap:wrap}
  .nd-tokenbox input{flex:1;min-width:220px;direction:ltr;text-align:left;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
  .nd-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin-top:14px}
  .nd-step{padding:11px 13px;border:1px dashed var(--line2);border-radius:12px;font-size:12px;color:var(--sub);line-height:1.8}
  .nd-step b{color:var(--text);display:block;margin-bottom:2px}
  .nd-row{display:flex;gap:14px;align-items:center;padding:14px;border:1px solid var(--line);border-radius:14px;background:var(--panel2);margin-bottom:10px;flex-wrap:wrap}
  .nd-main{flex:1;min-width:220px;display:flex;flex-direction:column;gap:5px}
  .nd-main b{font-size:14px;display:flex;align-items:center;gap:8px}
  .nd-main small{font-size:11.5px;color:var(--sub)}
  .nd-metrics{display:flex;gap:8px;flex-wrap:wrap}
  .nd-m{padding:6px 10px;border-radius:10px;background:var(--panel);border:1px solid var(--line);font-size:11px;color:var(--sub);display:flex;flex-direction:column;gap:1px;min-width:74px}
  .nd-m b{font-size:13px;color:var(--text)}
  .nd-acts{display:flex;gap:6px;flex-wrap:wrap}
  .nd-err{color:var(--bad)!important}
  `;
  document.head.appendChild(st);
}
nodeStyle();

const fmtUptime = s => { s = Number(s)||0; const d=Math.floor(s/86400), h=Math.floor(s%86400/3600), m=Math.floor(s%3600/60); return d?`${d}d ${h}h`:(h?`${h}h ${m}m`:`${m}m`); };
function nodeCopy(text, okMsg){
  const done = ()=>toast(okMsg || 'کپی شد ✓');
  if(navigator.clipboard && window.isSecureContext){ navigator.clipboard.writeText(text).then(done, ()=>nodeFallbackCopy(text, done)); }
  else nodeFallbackCopy(text, done);
}
function nodeFallbackCopy(text, done){
  const t = document.createElement('textarea'); t.value = text; t.style.position='fixed'; t.style.opacity='0'; document.body.appendChild(t); t.select();
  try{ document.execCommand('copy'); done(); }catch(e){ toast('کپی نشد؛ دستی انتخاب و کپی کن', false); }
  t.remove();
}

// ───────────── توکن این پنل (وقتی این پنل نود است) ─────────────
async function loadNodeToken(){
  try{ NODE_TOKEN = await api('/api/node/token'); }catch(e){ NODE_TOKEN = {enabled:false, token:null}; }
  renderNodeToken();
}
function renderNodeToken(){
  const box = document.getElementById('nodeTokenBody'); if(!box) return;
  const origin = location.origin;
  if(!NODE_TOKEN.enabled){
    box.innerHTML = `<p class="muted" style="margin-bottom:12px">این پنل فعلاً به‌عنوان «نود» قابل‌اتصال نیست. برای اینکه پنل اصلی بتواند این پنل را مدیریت کند، یک توکن بساز.</p>
      <button class="btn primary" onclick="createNodeToken()"><i class="ti ti-key"></i> ساخت توکن نود</button>`;
    return;
  }
  const tok = NODE_TOKEN.token || '';
  box.innerHTML = `
    <div class="grp"><label>آدرس این پنل</label><div class="nd-tokenbox"><input readonly id="ndOrigin" value="${escapeHtml(origin)}"><button class="btn" onclick="nodeCopy(document.getElementById('ndOrigin').value,'آدرس کپی شد ✓')"><i class="ti ti-copy"></i> کپی</button></div></div>
    <div class="grp" style="margin-top:10px"><label>توکن API نود</label><div class="nd-tokenbox">
      <input readonly id="ndToken" type="${NODE_TOKEN_SHOWN?'text':'password'}" value="${escapeHtml(tok)}">
      <button class="btn" onclick="toggleNodeToken()"><i class="ti ${NODE_TOKEN_SHOWN?'ti-eye-off':'ti-eye'}"></i></button>
      <button class="btn primary" onclick="nodeCopy(NODE_TOKEN.token,'توکن کپی شد ✓')"><i class="ti ti-copy"></i> کپی توکن</button>
    </div></div>
    <div class="nd-steps">
      <div class="nd-step"><b>۱) کپی</b>آدرس و توکن بالا را کپی کن.</div>
      <div class="nd-step"><b>۲) پنل اصلی</b>در پنل اصلی برو به «نودها» ← «افزودن نود».</div>
      <div class="nd-step"><b>۳) پیست</b>آدرس و توکن را بچسبان و «تست اتصال» را بزن.</div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:14px">
      <button class="btn sm" onclick="createNodeToken(true)"><i class="ti ti-refresh"></i> ساخت مجدد (توکن قبلی باطل می‌شود)</button>
      <button class="btn sm danger" onclick="disableNodeToken()"><i class="ti ti-lock"></i> غیرفعال‌سازی</button>
    </div>
    <p class="hint" style="margin-top:10px">این توکن فقط به بخش‌های عملیاتی (اینباند، پراکسی، ساب، آمار) دسترسی می‌دهد؛ رمز، ادمین‌ها و تنظیمات را باز نمی‌کند. مثل رمز نگهش دار.${NODE_TOKEN.created_at?` · ساخته‌شده: ${escapeHtml(String(NODE_TOKEN.created_at).slice(0,16).replace('T',' '))}`:''}</p>`;
}
function toggleNodeToken(){ NODE_TOKEN_SHOWN = !NODE_TOKEN_SHOWN; renderNodeToken(); }
async function createNodeToken(regen){
  if(regen && !confirm('توکن قبلی همین الان باطل می‌شود و پنل‌های اصلی که با آن وصل‌اند قطع می‌شوند. ادامه بدهم؟')) return;
  try{ NODE_TOKEN = await api('/api/node/token', {method:'POST'}); NODE_TOKEN_SHOWN = true; renderNodeToken(); toast(regen ? 'توکن جدید ساخته شد ✓' : 'توکن ساخته شد ✓'); }
  catch(e){ toast(e.message, false); }
}
async function disableNodeToken(){
  if(!confirm('با غیرفعال‌سازی، هیچ پنل اصلی‌ای دیگر به این پنل دسترسی ندارد. ادامه بدهم؟')) return;
  try{ NODE_TOKEN = await api('/api/node/token', {method:'DELETE'}); NODE_TOKEN_SHOWN = false; renderNodeToken(); toast('توکن نود غیرفعال شد'); }
  catch(e){ toast(e.message, false); }
}

// ───────────── لیست نودها (وقتی این پنل اصلی است) ─────────────
async function loadNodesPage(){
  loadNodeToken();
  await loadNodes();
  clearInterval(NODES_TIMER);
  NODES_TIMER = setInterval(()=>{ if(CURRENT_PAGE==='nodes') loadNodes(); else clearInterval(NODES_TIMER); }, 30000);
}
async function loadNodes(){
  try{ const r = await api('/api/nodes'); NODES_LIST = r.nodes || []; }
  catch(e){ NODES_LIST = []; const el = document.getElementById('nodesList'); if(el) el.innerHTML = `<div class="notice danger-note">${escapeHtml(e.message)}</div>`; return; }
  renderNodes(); updateNodeSwitchBtn();
}
function nodeMetricsHtml(s){
  if(!s || !s.online) return '';
  const m = (label, val)=>`<div class="nd-m"><small>${label}</small><b>${val}</b></div>`;
  return `<div class="nd-metrics">
    ${m('پینگ', Math.round(s.latency_ms||0)+'ms')}
    ${m('اینباند', s.inbounds ?? 0)}
    ${m('کلاینت', s.clients ?? 0)}
    ${m('اتصال فعال', s.connections ?? 0)}
    ${m('ترافیک', fmtBytes(s.total_bytes||0))}
    ${s.cpu!=null?m('CPU', Math.round(s.cpu)+'%'):''}
    ${s.mem!=null?m('RAM', Math.round(s.mem)+'%'):''}
    ${m('آپتایم', fmtUptime(s.uptime_seconds))}
  </div>`;
}
function renderNodes(){
  const el = document.getElementById('nodesList'); if(!el) return;
  if(!NODES_LIST.length){ el.innerHTML = '<div class="muted" style="padding:14px">هنوز نودی اضافه نشده. روی «افزودن نود» بزن و آدرس + توکن پنل دیگر را بچسبان.</div>'; return; }
  el.innerHTML = NODES_LIST.map(n=>{
    const s = n.status || null;
    const state = !n.enabled ? '' : (s ? (s.online ? 'on' : 'off') : '');
    const label = !n.enabled ? 'غیرفعال' : (s ? (s.online ? 'آنلاین' : 'آفلاین') : 'در حال بررسی');
    const active = ACTIVE_NODE && ACTIVE_NODE.id === n.id;
    return `<div class="nd-row">
      <div class="nd-main">
        <b><span class="nd-dot ${state}"></span>${escapeHtml(n.name)} <span class="badge ${s&&s.online&&n.enabled?'green':(n.enabled&&s?'red':'gray')}">${label}</span>${active?' <span class="badge gray">در حال مدیریت</span>':''}</b>
        <small class="mono" style="direction:ltr;text-align:left">${escapeHtml(n.url)} · توکن ${escapeHtml(n.token_hint||'')}${s&&s.version?` · v${escapeHtml(s.version)}`:''}</small>
        ${s && !s.online && s.error ? `<small class="nd-err">${escapeHtml(s.error)}</small>`:''}
        ${nodeMetricsHtml(s)}
      </div>
      <div class="nd-acts">
        <button class="btn primary sm" onclick="manageNode('${n.id}')" ${(!n.enabled||!(s&&s.online))?'disabled':''}><i class="ti ti-server-cog"></i> مدیریت</button>
        <button class="btn sm" onclick="checkNodeNow('${n.id}')"><i class="ti ti-activity"></i> بررسی</button>
        <button class="btn sm" onclick="openNodeDrawer('${n.id}')"><i class="ti ti-pencil"></i></button>
        <button class="btn sm" onclick="toggleNodeEnabled('${n.id}')" title="${n.enabled?'غیرفعال‌سازی':'فعال‌سازی'}"><i class="ti ${n.enabled?'ti-player-pause':'ti-player-play'}"></i></button>
        <button class="btn sm danger" onclick="deleteNode('${n.id}')"><i class="ti ti-trash"></i></button>
      </div>
    </div>`;
  }).join('');
}
async function checkAllNodes(){
  try{ const r = await api('/api/nodes/check-all', {method:'POST'}); NODES_LIST = r.nodes||[]; renderNodes(); updateNodeSwitchBtn(); toast('وضعیت نودها به‌روز شد ✓'); }
  catch(e){ toast(e.message, false); }
}
async function checkNodeNow(id){
  try{ const r = await api(`/api/nodes/${id}/check`, {method:'POST'}); NODES_LIST = NODES_LIST.map(n=>n.id===id?r.node:n); renderNodes(); updateNodeSwitchBtn(); }
  catch(e){ toast(e.message, false); }
}
async function toggleNodeEnabled(id){
  const n = NODES_LIST.find(x=>x.id===id); if(!n) return;
  try{ await api('/api/nodes', {method:'POST', body: JSON.stringify({id, name:n.name, url:n.url, enabled:!n.enabled})}); await loadNodes(); }
  catch(e){ toast(e.message, false); }
}
async function deleteNode(id){
  const n = NODES_LIST.find(x=>x.id===id); if(!n) return;
  if(!confirm(`نود «${n.name}» از این پنل حذف شود؟ (خودِ سرور نود و کانفیگ‌هایش دست‌نخورده می‌مانند.)`)) return;
  try{
    await api(`/api/nodes/${id}`, {method:'DELETE'});
    if(ACTIVE_NODE && ACTIVE_NODE.id===id){ exitNodeMode(); return; }
    await loadNodes(); toast('نود حذف شد');
  }catch(e){ toast(e.message, false); }
}

// ───────────── افزودن / ویرایش نود ─────────────
function openNodeDrawer(id){
  const n = id ? NODES_LIST.find(x=>x.id===id) : null;
  openDrawer(n ? 'ویرایش نود' : 'افزودن نود', `
    <div class="grp"><label>نام نود</label><input id="ndName" value="${escapeHtml(n?n.name:'')}" placeholder="مثلاً: آلمان-۱"></div>
    <div class="grp"><label>آدرس پنل نود</label><input id="ndUrl" class="mono" style="direction:ltr;text-align:left" value="${escapeHtml(n?n.url:'')}" placeholder="https://your-node.up.railway.app" oninput="ndUrlWarn()"><div class="hint" id="ndUrlHint"></div></div>
    <div class="grp"><label>توکن API نود</label><input id="ndTok" type="password" class="mono" style="direction:ltr;text-align:left" placeholder="${n?'خالی = بدون تغییر ('+escapeHtml(n.token_hint||'')+')':'vwn_...'}" autocomplete="off"><div class="hint">از پنل نود: تب «نودها» ← «ساخت توکن نود» ← کپی.</div></div>
    <div id="ndTestResult"></div>
  `, `<button class="btn" onclick="testNodeForm('${id||''}')"><i class="ti ti-plug-connected"></i> تست اتصال</button>
      <button class="btn primary" style="flex:1" id="ndSave" onclick="saveNode('${id||''}')"><i class="ti ti-device-floppy"></i> ذخیره</button>`);
  ndUrlWarn();
}
function ndUrlWarn(){
  const v = (document.getElementById('ndUrl')?.value||'').trim().toLowerCase(); const h = document.getElementById('ndUrlHint'); if(!h) return;
  h.innerHTML = v.startsWith('http://') ? '<span class="nd-err">⚠️ با http توکن بدون رمزنگاری می‌رود؛ اگر نود روی اینترنت است حتماً https بگذار.</span>' : '';
}
function ndFormBody(id){
  return {id: id||undefined, name: (document.getElementById('ndName')?.value||'').trim(), url: (document.getElementById('ndUrl')?.value||'').trim(), token: (document.getElementById('ndTok')?.value||'').trim()};
}
async function testNodeForm(id){
  const box = document.getElementById('ndTestResult'); if(box) box.innerHTML = '<div class="ob-note">در حال تست اتصال...</div>';
  try{
    const r = (await api('/api/nodes/test', {method:'POST', body: JSON.stringify(ndFormBody(id))})).status;
    box.innerHTML = r.online
      ? `<div class="ob-note ok"><i class="ti ti-circle-check"></i> اتصال موفق · پینگ ${Math.round(r.latency_ms)}ms · نسخه ${escapeHtml(r.version||'?')} · ${r.inbounds??0} اینباند</div>`
      : `<div class="ob-note"><i class="ti ti-alert-triangle"></i> <span class="nd-err">${escapeHtml(r.error||'اتصال ناموفق')}</span></div>`;
  }catch(e){ box.innerHTML = `<div class="ob-note"><span class="nd-err">${escapeHtml(e.message)}</span></div>`; }
}
async function saveNode(id){
  const btn = document.getElementById('ndSave'); if(btn) btn.disabled = true;
  try{
    const r = await api('/api/nodes', {method:'POST', body: JSON.stringify(ndFormBody(id))});
    closeDrawer(); await loadNodes();
    const s = r.node.status;
    toast(s && s.online ? 'نود اضافه شد و آنلاین است ✓' : 'نود ذخیره شد ولی آنلاین نیست: ' + ((s&&s.error)||''), !!(s&&s.online));
  }catch(e){ toast(e.message, false); if(btn) btn.disabled = false; }
}

// ───────────── مدیریت نود: کل پنل روی نود اجرا می‌شود ─────────────
function manageNode(id){
  const n = NODES_LIST.find(x=>x.id===id); if(!n) return;
  sessionStorage.setItem('vw_active_node', JSON.stringify({id:n.id, name:n.name, url:n.url}));
  location.reload();
}
function exitNodeMode(){
  sessionStorage.removeItem('vw_active_node');
  location.reload();
}
function initNodeMode(){
  if(!ACTIVE_NODE) return;
  ['admins','settings','nodes'].forEach(pg=>{ const t = document.querySelector(`.tab[data-pg="${pg}"]`); if(t) t.style.display='none'; });
  const b = document.getElementById('nodeBanner');
  if(b){
    b.style.display = 'flex';
    b.innerHTML = `<i class="ti ti-server-cog"></i><span>در حال مدیریت نود <b>${escapeHtml(ACTIVE_NODE.name)}</b> <span class="mono" style="direction:ltr;display:inline-block">${escapeHtml(ACTIVE_NODE.url)}</span> — همه‌ی تغییرات روی سرور آن نود اعمال می‌شود.</span><button class="btn sm" onclick="exitNodeMode()"><i class="ti ti-arrow-back-up"></i> بازگشت به این پنل</button>`;
  }
}
function updateNodeSwitchBtn(){
  const btn = document.getElementById('nodeSwitchBtn'); if(!btn) return;
  if(!ACTIVE_NODE && !NODES_LIST.length){ btn.style.display = 'none'; return; }
  btn.style.display = '';
  btn.classList.toggle('remote', !!ACTIVE_NODE);
  btn.innerHTML = `<i class="ti ${ACTIVE_NODE?'ti-server-cog':'ti-home'}"></i> ${ACTIVE_NODE?escapeHtml(ACTIVE_NODE.name):'این پنل'} <i class="ti ti-chevron-down"></i>`;
}
async function initNodeUi(){
  nodeStyle(); initNodeMode();
  try{ const r = await api('/api/nodes'); NODES_LIST = r.nodes||[]; }catch(e){ NODES_LIST = []; }
  updateNodeSwitchBtn();
}
function openNodeSwitcher(){
  ensureObStyle();
  const cur = ACTIVE_NODE ? ACTIVE_NODE.id : '';
  const rows = [`<label class="ob-row ${cur===''?'on':''}"><input type="radio" name="ndSw" value="" ${cur===''?'checked':''}><span class="ob-emoji">🏠</span><span class="ob-txt"><b>این پنل</b><small>پنل محلی (سرور فعلی)</small></span></label>`]
    .concat(NODES_LIST.map(n=>{
      const s = n.status, ok = n.enabled && s && s.online;
      return `<label class="ob-row ${cur===n.id?'on':''}" style="${ok?'':'opacity:.55'}"><input type="radio" name="ndSw" value="${n.id}" ${cur===n.id?'checked':''} ${ok?'':'disabled'}><span class="nd-dot ${ok?'on':(n.enabled?'off':'')}"></span><span class="ob-txt"><b>${escapeHtml(n.name)}</b><small>${ok?Math.round(s.latency_ms||0)+'ms · '+(s.inbounds??0)+' اینباند':(n.enabled?'آفلاین':'غیرفعال')}</small></span></label>`;
    })).join('');
  const ov = document.createElement('div'); ov.className = 'ob-ov';
  ov.innerHTML = `<div class="ob-box"><h3>انتخاب پنل برای مدیریت</h3><p>با انتخاب یک نود، تمام صفحات (اینباند، ساب، پراکسی، آمار) روی همان نود کار می‌کنند.</p><div class="ob-list ob-picker">${rows}</div>
    <div class="ob-foot"><button class="btn" data-a="cancel">انصراف</button><button class="btn" data-a="nodes"><i class="ti ti-server-cog"></i> صفحه‌ی نودها</button><button class="btn primary" data-a="ok"><i class="ti ti-check"></i> برو</button></div></div>`;
  const close = ()=>{ document.removeEventListener('keydown', onKey); ov.remove(); };
  const onKey = e=>{ if(e.key==='Escape') close(); };
  document.addEventListener('keydown', onKey);
  ov.addEventListener('click', e=>{
    if(e.target===ov) return close();
    const a = e.target.closest('[data-a]'); if(!a) return;
    if(a.dataset.a==='cancel') return close();
    if(a.dataset.a==='nodes'){ close(); if(ACTIVE_NODE){ sessionStorage.removeItem('vw_active_node'); location.reload(); } else gotoPage('nodes'); return; }
    const v = (ov.querySelector('input[name=ndSw]:checked')||{}).value || '';
    close();
    if(v==='') { if(ACTIVE_NODE) exitNodeMode(); } else manageNode(v);
  });
  document.body.appendChild(ov);
}

function copySupportCard(){
  const num = document.getElementById('supportCardNumber')?.textContent?.trim() || '';
  const lang=(typeof curLang==='function'?curLang():'fa');
  const done = ()=>toast(lang==='en' ? 'Card number copied' : 'شماره کارت کپی شد ✓');
  const fail = ()=>toast(lang==='en' ? 'Copy failed' : 'کپی نشد', false);
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(num).then(done).catch(fail);
  }else{
    try{ const ta=document.createElement('textarea'); ta.value=num; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); done(); }catch(e){ fail(); }
  }
}
async function boot(){
  try{
    const me = await api('/api/me');
    if(!me.authenticated){ location.href='/login'; return; }
    $('userName').textContent = me.admin.username;
    $('userChip').querySelector('.av').textContent = (me.admin.username||'?').slice(0,1).toUpperCase();
    const _rt=$('userRoleTag'); if(_rt){ const lang=(typeof curLang==='function'?curLang():'fa'); _rt.textContent = me.admin.role==='owner' ? (lang==='en'?'Owner':'مالک') : (lang==='en'?'Admin':'ادمین'); }
    if(me.admin.role !== 'owner'){
      document.querySelector('.tab[data-pg="admins"]').style.display='none';
      document.querySelector('.tab[data-pg="settings"]').style.display='none';
      if(!(me.admin.permissions||[]).includes('clients')){
        document.querySelector('.tab[data-pg="clientmgr"]').style.display='none';
      }
      const nt = document.querySelector('.tab[data-pg="nodes"]'); if(nt) nt.style.display='none';
    } else {
      loadAdminRequests();
      initNodeUi();
    }
  }catch(e){ location.href='/login'; return; }
  try{ const p = await api('/api/protocols'); PROTOCOLS = p.protocols||[]; MANUAL_META = p.manual||{}; }catch(e){}
  loadProxies();
  refreshOverview();
}
boot();

// ============================================================
// OVERVIEW
// ============================================================
async function refreshOverview(){
  try{
    const [stats, linksRes] = await Promise.all([api('/stats'), api('/api/links')]);
    LINKS = linksRes.links || [];
    $('nb-links').textContent = LINKS.filter(x=>!x.is_client).length;
    window.OV_STATS = stats || {};
    $('trafficTotalVal').textContent = fmtBytes(stats.total_traffic_bytes || 0);
    const _ib=LINKS.filter(x=>!x.is_client),_ac=_ib.filter(x=>x.active&&!x.expired).length;
    $('instVal').textContent=_ib.length;$('instSub').textContent='فعال: '+_ac+' | متوقف: '+(_ib.length-_ac);
  }catch(e){ toast(e.message, false); }
  if(!ACTIVE_NODE) try{
    const s = await api('/api/settings');
    $('ovBaseUrl').textContent = s.public_base_url || s.effective_host || '—';
    const running = !!s.bot_running;
    $('ovBotStatus').className = 'badge ' + (running?'green':'red');
    $('ovBotStatus').textContent = running?'آنلاین':'آفلاین';
    $('botStateText').textContent = running?'در حال اجرا':'خاموش';
  }catch(e){}
  try{
    const rep = await api('/api/reports/summary?days=7');
    const t = rep.totals || {};
    const _os = window.OV_STATS || {};
    $('ovBizStats').innerHTML = `
      <div><i class="ti ti-network"></i><span><b>${t.links||0}</b><small>کل اینباندها</small></span></div>
      <div><i class="ti ti-circle-check"></i><span><b>${t.active_links||0}</b><small>اینباند فعال</small></span></div>
      <div class="qs-traffic"><i class="ti ti-arrows-exchange"></i><span><b dir="ltr">${fmtBytes(_os.total_traffic_bytes||0)}</b><small>مجموع کل ترافیک</small></span></div>
      <div><i class="ti ti-plug-connected"></i><span><b>${_os.active_connections||0}</b><small>اتصال آنلاین</small></span></div>
      <div><i class="ti ti-folders"></i><span><b>${t.subs||0}</b><small>گروه‌های ساب</small></span></div>
      <div><i class="ti ti-users-group"></i><span><b>${t.admins||0}</b><small>ادمین‌ها</small></span></div>`;
    const top = (rep.top_links||[]).slice(0,6);
    if(!top.length){
      $('ovTopLinks').innerHTML = '<div class="ov-empty">هنوز داده‌ی مصرفی ثبت نشده</div>';
    }else{
      const maxUsed = Math.max(1, ...top.map(l=>l.used_bytes||0));
      $('ovTopLinks').innerHTML = top.map((l,i)=>{
        const pct = Math.round((l.used_bytes||0)/maxUsed*100);
        return `<div class="ov-toplink-row"><div class="otl-rank">${i+1}</div><div class="otl-info"><b>${escapeHtml(l.label||'—')}</b><div class="otl-bar"><i style="width:${pct}%"></i></div></div><div class="otl-val">${fmtBytes(l.used_bytes||0)}</div></div>`;
      }).join('');
    }
  }catch(e){}
  loadRailActivity();
  await refreshTelemetry();
}
let TEL={cpu:[],ram:[],swap:[],storage:[],traffic:[],conn:[]};
function pushSeries(arr,v,max=36){arr.push(Number(v)||0);while(arr.length>max)arr.shift();}
function drawSpark(id,arr){const el=$(id);if(!el||!arr.length)return;const max=Math.max(100, ...arr), min=Math.min(0,...arr);const pts=arr.map((v,i)=>{const x=(i/Math.max(1,arr.length-1))*240;const y=44-((v-min)/(max-min||1))*38;return `${x.toFixed(1)},${y.toFixed(1)}`}).join(' ');el.innerHTML=`<polyline points="${pts}"/>`; }
function drawChart(id,arr,maxY){const el=$(id);if(!el||!arr.length)return;const w=id==='trafficChart'?900:340,h=id==='trafficChart'?260:150;const max=maxY||Math.max(1,...arr);const pts=arr.map((v,i)=>{const x=(i/Math.max(1,arr.length-1))*w;const y=h-8-(Math.min(max,v)/max)*(h-20);return `${x.toFixed(1)},${y.toFixed(1)}`}).join(' ');const area=`0,${h} ${pts} ${w},${h}`;el.innerHTML=`<polygon class="area" points="${area}"/><polyline points="${pts}"/>`; }
async function refreshTelemetry(){
  try{const t=await api('/api/telemetry');
    $('cpuVal').textContent=t.cpu+'%'; $('cpuSub').textContent=(t.cpu_cores||1)+' logical cores';
    $('ramVal').textContent=t.ram.percent+'%'; $('ramSub').textContent=fmtBytes(t.ram.used)+' / '+fmtBytes(t.ram.total);
    $('swapVal').textContent=t.swap.percent+'%'; $('swapSub').textContent=fmtBytes(t.swap.used)+' / '+fmtBytes(t.swap.total);
    $('storageVal').textContent=t.storage.percent+'%'; $('storageSub').textContent=fmtBytes(t.storage.used)+' / '+fmtBytes(t.storage.total);
    $('txRate').textContent=fmtBytes(t.network.tx_bps)+'/s'; $('rxRate').textContent=fmtBytes(t.network.rx_bps)+'/s'; $('liveRate').textContent='↑ '+fmtBytes(t.network.tx_bps)+'/s ↓ '+fmtBytes(t.network.rx_bps)+'/s';
    $('connVal').textContent=t.connections; $('reqVal').textContent=t.requests; $('errVal').textContent=t.errors; $('uptimeVal').textContent=t.uptime; $('coresVal').textContent=t.cpu_cores; $('procRamVal').textContent=fmtBytes(t.process.rss); $('loadVal').textContent=(t.load||[]).join('  '); $('sentTotal').textContent=fmtBytes(t.network.bytes_sent); $('recvTotal').textContent=fmtBytes(t.network.bytes_recv);
    const hist=Array.isArray(t.history)?t.history:[];
    if(hist.length){
      TEL.cpu=hist.map(x=>Number(x.cpu)||0); TEL.ram=hist.map(x=>Number(x.ram)||0); TEL.swap=hist.map(x=>Number(x.swap)||0); TEL.storage=hist.map(x=>Number(x.storage)||0);
      TEL.traffic=hist.map(x=>(Number(x.tx_bps)||0)+(Number(x.rx_bps)||0)); TEL.conn=hist.map(x=>Number(x.connections)||0);
    }else{
      pushSeries(TEL.cpu,t.cpu);pushSeries(TEL.ram,t.ram.percent);pushSeries(TEL.swap,t.swap.percent);pushSeries(TEL.storage,t.storage.percent);pushSeries(TEL.traffic,(t.network.tx_bps+t.network.rx_bps));pushSeries(TEL.conn,t.connections);
    }
    drawSpark('cpuSpark',TEL.cpu);drawSpark('ramSpark',TEL.ram);drawSpark('swapSpark',TEL.swap);drawSpark('storageSpark',TEL.storage);drawSpark('netSpark',TEL.traffic);drawSpark('instSpark',TEL.conn);$('netVal').textContent=fmtBytes(t.network.tx_bps+t.network.rx_bps)+'/s';$('netSub').textContent='↑ '+fmtBytes(t.network.tx_bps)+' · ↓ '+fmtBytes(t.network.rx_bps);drawChart('trafficChart',chartSeries(),chartMax());drawChart('connChart',TEL.conn);
    const _hc=Number(t.cpu)||0,_hr=Number(t.ram.percent)||0,_hs=Number(t.storage.percent)||0;
    const healthPct=Math.max(0,Math.min(100,Math.round(100-((_hc*0.4)+(_hr*0.35)+(_hs*0.25)))));
    const hg=$('healthGauge'),hp=$('healthPct'),hl=$('healthLabel');
    if(hg){hg.style.setProperty('--pct',healthPct);}
    railUpdate(t,healthPct);
    if(hp){hp.textContent=healthPct+'%';}
    if(hl){const lang=(typeof curLang==='function'?curLang():'fa');const good=healthPct>=80,mid=healthPct>=50;
      hl.style.color=good?'var(--good)':(mid?'var(--warn)':'var(--bad)');
      hl.innerHTML=(good?(lang==='en'?'Healthy':'سالم'):(mid?(lang==='en'?'Moderate load':'بار متوسط'):(lang==='en'?'High load':'بار بالا')))+'<small>Overall system health</small>';
    }
  }catch(e){}
}
let CHART_TAB='net';
function chartSeries(){return CHART_TAB==='cpu'?TEL.cpu:CHART_TAB==='mem'?TEL.ram:CHART_TAB==='disk'?TEL.storage:TEL.traffic;}
function chartMax(){return CHART_TAB==='net'?0:100;}
function setChartTab(k){CHART_TAB=k;document.querySelectorAll('#chartTabs button').forEach(b=>b.classList.toggle('on',b.dataset.k===k));drawChart('trafficChart',chartSeries(),chartMax());}
function railUpdate(t,h){
  const g=$('railGauge');if(!g)return;g.style.setProperty('--pct',h);$('railPct').textContent=h+'%';
  $('rlCpu').textContent=t.cpu+'%';$('rlRam').textContent=t.ram.percent+'%';$('rlDisk').textContent=t.storage.percent+'%';$('rlSwap').textContent=t.swap.percent+'%';
}
async function loadRailActivity(){
  const el=$('railActivity');if(!el)return;
  try{
    const res=await api('/api/activity');const logs=(res.logs||[]).slice(-5).reverse();
    el.innerHTML=logs.map(l=>{const tm=(l.time||l.ts||'').toString();const hm=tm.length>=16?tm.slice(11,16):'';
      const cls=l.level==='err'?'bad':l.level==='warn'?'warn':'ok';
      return `<div class="rail-item"><i class="ri-ic ${cls}"></i><div><b>${escapeHtml(String(l.type||l.kind||'Event'))}</b><small>${escapeHtml(String(l.message||l.text||'')).slice(0,48)}</small></div><em>${hm}</em></div>`}).join('')||'<div class="ov-empty">No activity</div>';
  }catch(e){}
}
let telemetryTimer=null;
function startTelemetryLoop(){ if(telemetryTimer) clearInterval(telemetryTimer); telemetryTimer=setInterval(()=>{ if(!document.hidden && CURRENT_PAGE==='overview') refreshTelemetry(); },10000); }
startTelemetryLoop();

function statCard(icon,color,val,label){
  return `<div class="stat-card"><div class="sc-top"><div class="sc-icon" style="background:${color}22;color:${color}"><i class="ti ${icon}"></i></div></div>
    <div class="sc-val">${val ?? 0}</div><div class="sc-label">${label}</div></div>`;
}
function protoLabel(l){
  if(l && typeof l === 'object'){
    if(l.protocol_display) return l.protocol_display;
    const found = PROTOCOLS.find(x=>x.id===l.protocol);
    return found ? found.label : (l.protocol||'—');
  }
  const found = PROTOCOLS.find(x=>x.id===l);
  return found ? found.label : (l||'—');
}
function statusBadge(l){
  if(l.expired || !l.active) return `<span class="badge red">غیرفعال/منقضی</span>`;
  if(l.status_color==='green') return `<span class="badge green">متصل</span>`;
  return `<span class="badge gray">فعال</span>`;
}

// ============================================================
// LINKS
// ============================================================
async function loadLinks(silent){
  try{
    const [linksRes, catsRes] = await Promise.all([api('/api/links'), api('/api/categories')]);
    const selectedBefore = silent ? selectedLinkUuids() : [];
    LINKS = linksRes.links || [];
    CATEGORIES = catsRes.categories || [];
    const sel = $('linkFilterCat');
    const prevCatVal = sel.value;
    const _catHtml = '<option value="">همه دسته‌ها</option>' + CATEGORIES.map(c=>`<option value="${c.id}">${escapeHtml(c.name)}</option>`).join('');
    if(sel.__vwHtml !== _catHtml){ sel.innerHTML = _catHtml; sel.__vwHtml = _catHtml; }
    sel.value = prevCatVal;
    $('nb-links').textContent = LINKS.filter(x=>!x.is_client).length;
    renderLinks();
    if(silent && selectedBefore.length){
      selectedBefore.forEach(uid=>{const c=document.querySelector(`.ib-row-check[data-uid="${uid}"]`); if(c) c.checked=true;});
      updateLinksBulkBar();
    }
    if($('ibUpdatedAt')) $('ibUpdatedAt').textContent = 'بروزرسانی ' + new Date().toLocaleTimeString('fa-IR',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  }catch(e){ if(!silent) toast(e.message, false); }
}
let linksTimer=setInterval(()=>{if(!document.hidden && CURRENT_PAGE==='links') loadLinks(true)},12000);
async function refreshAllInbounds(){
  const btn=$('ibRefreshBtn'), icon=$('ibRefreshIcon');
  if(btn) btn.disabled=true;
  if(icon) icon.classList.add('spin');
  try{
    await loadLinks();
    await refreshOverview();
    toast('همه‌ی اینباندها بروزرسانی شدند ✓');
  }catch(e){ toast(e.message, false); }
  finally{ if(btn) btn.disabled=false; if(icon) icon.classList.remove('spin'); }
}
function renderQuickStats(list){
  const total=list.length, active=list.filter(l=>l.active && !l.expired).length, live=list.filter(l=>l.live_status==='live').length, clients=list.reduce((s,l)=>s+Number(l.client_count||0),0);
  const traffic=list.reduce((s,l)=>s+Number(l.used_bytes||0),0), online=list.reduce((s,l)=>s+Number(l.connected_ips||0),0);
  $('ibQuickStats').innerHTML = `
    <div><i class="ti ti-network"></i><span><b>${total}</b><small>کل اینباندها</small></span></div>
    <div><i class="ti ti-circle-check"></i><span><b>${active}</b><small>فعال</small></span></div>
    <div><i class="ti ti-bolt"></i><span><b>${live}</b><small>LIVE</small></span></div>
    <div><i class="ti ti-users"></i><span><b>${clients}</b><small>کل کلاینت‌ها</small></span></div>
    <div class="ibx-hl"><i class="ti ti-arrows-exchange"></i><span><b dir="ltr">${fmtBytes(traffic)}</b><small>مجموع کل ترافیک</small></span></div>
    <div><i class="ti ti-plug-connected"></i><span><b>${online}</b><small>آنلاین همین الان</small></span></div>`;
}
function copyLinkOf(uid){ const l=LINKS.find(x=>x.uuid===uid); const v=(l&&(l.vless_full||l.vless))||''; if(!v){ toast('لینکی برای کپی وجود ندارد', false); return; } copyText(v); }
function ibCardHtml(l){
  const limit=Number(l.limit_bytes||0), used=Number(l.used_bytes||0), port=l.port||443;
  const pct=limit>0?Math.min(100,Math.round(used/limit*100)):0;
  const pctClass=pct>=90?'crit':(pct>=70?'warn':'');
  const isLive=l.live_status==='live';
  const daysLeft=l.expires_at?Math.ceil((new Date(l.expires_at).getTime()-Date.now())/86400000):null;
  const expClass=l.expired?'expired':(daysLeft!==null&&daysLeft<=3?'soon':'');
  const expTxt=l.expires_at?(l.expired?'منقضی':(daysLeft!==null?daysLeft+' روز':'—')):'∞';
  const online=Number(l.connected_ips||0);
  const st=!l.active?['off','غیرفعال']:(l.expired?['bad','منقضی']:(online>0?['on','آنلاین']:['idle','آماده']));
  const ipl=Number(l.ip_limit||0);
  const addr=(l.address||location.hostname)+':'+port;
  const rem=limit>0?fmtBytes(Math.max(0,limit-used)):'نامحدود';
  const name=escapeHtml(l.label||'Unnamed Inbound');
  const ob=l.outbound?`<span class="ib-ob-tag" title="خروجی از طریق پراکسی «${escapeHtml(l.outbound.name||'')}»">${flagHtml(l.outbound)} ${escapeHtml(l.outbound.country||l.outbound.name||'')}</span>`:(l.outbound_proxy_id?'<span class="ib-ob-tag">⚠️ پراکسی نامعتبر</span>':'<span class="ib-ob-tag" title="خروجی مستقیم">🚀 مستقیم</span>');
  return `<article class="ib-card ibx ${l.active?'':'ib-off'}" data-uid="${l.uuid}">
    <label class="ib-card-check"><input type="checkbox" class="ib-check ib-row-check" data-uid="${l.uuid}" onchange="updateLinksBulkBar()"></label>
    <div class="ibx-head">
      <div class="ibx-av ${st[0]}"><i class="ti ti-router"></i></div>
      <div class="ibx-id">
        <b title="${name}">${name}</b>
        <div class="ibx-sub"><span class="ibx-pill ${st[0]}">${st[1]}</span><span class="mono">${escapeHtml((l.uuid||'').slice(0,8))}…</span></div>
      </div>
      <button class="ib-switch ${l.active?'on':''}" title="فعال/غیرفعال" onclick="toggleLink('${l.uuid}', ${!l.active})"></button>
    </div>
    <div class="ib-tagrow"><span>${protoLabel(l)}</span><span>${l.network||'tcp'}/${l.security||'none'}</span>${isLive?'<span class="ib-live-tag"><i></i>LIVE</span>':'<span class="ib-linkonly-tag">LINK-ONLY</span>'}<span>${escapeHtml(l.category_name||'بدون دسته')}</span>${ob}</div>
    <div class="ibx-addr"><span class="mono" dir="ltr">${escapeHtml(addr)}</span><button class="iconbtn" title="کپی آدرس" onclick="copyText('${escapeHtml(addr)}')"><i class="ti ti-copy"></i></button></div>
    <div class="ibx-traffic">
      <div class="ibx-tt"><span>مصرف</span><b dir="ltr">${fmtBytes(used)}${limit>0?' / '+fmtBytes(limit):' / ∞'}</b></div>
      <div class="ib-progress"><i class="${pctClass}" style="width:${limit>0?pct:100}%;${limit>0?'':'opacity:.35'}"></i></div>
      <div class="ibx-tt sm"><span>${limit>0?pct+'٪ مصرف‌شده':'بدون سقف حجم'}</span><span>باقی‌مانده: <b>${rem}</b></span></div>
    </div>
    <div class="ibx-stats">
      <div><small>کلاینت</small><b>${Number(l.client_count||0)}</b></div>
      <div><small>اتصال</small><b>${online}/${Number(l.connection_limit||0)||'∞'}</b></div>
      <div><small>محدودیت IP</small><b>${ipl||'∞'}</b></div>
      <div><small>انقضا</small><b class="${expClass}">${expTxt}</b></div>
    </div>
    <div class="ibx-foot">
      <button class="btn sm primary" onclick="openClients('${l.uuid}')"><i class="ti ti-users"></i>کلاینت‌ها</button>
      <button class="btn sm" onclick="copyLinkOf('${l.uuid}')"><i class="ti ti-copy"></i>کپی لینک</button>
      <div class="ib-card-actions">
        <button class="iconbtn" title="خروجی (Outbound)" onclick="changeOutbound(['${l.uuid}'])"><i class="ti ti-route"></i></button>
        <button class="iconbtn" title="اشتراک و QR" onclick="showSubLink('${l.uuid}')"><i class="ti ti-qrcode"></i></button>
        <button class="iconbtn" title="ویرایش" onclick="openLinkDrawer('${l.uuid}')"><i class="ti ti-pencil"></i></button>
        <button class="iconbtn" title="تعویض لینک (UUID جدید)" onclick="regenerateLink('${l.uuid}')"><i class="ti ti-replace"></i></button>
        <button class="iconbtn" title="ریست حجم مصرفی" onclick="resetLinkUsage('${l.uuid}')"><i class="ti ti-refresh"></i></button>
        <button class="iconbtn" title="حذف" onclick="deleteLink('${l.uuid}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button>
      </div>
    </div>
  </article>`;
}
let ibFilter='all', ibSort='new';
function setIbFilter(f){ ibFilter=f; document.querySelectorAll('#ibChips .ibx-chip').forEach(c=>c.classList.toggle('on',c.dataset.f===f)); renderLinks(); }
function setIbSort(v){ ibSort=v; renderLinks(); }
function ibMatch(l,f){
  switch(f){
    case 'active': return l.active && !l.expired;
    case 'off': return !l.active;
    case 'expired': return !!l.expired;
    case 'live': return l.live_status==='live';
    case 'online': return Number(l.connected_ips||0)>0;
    default: return true;
  }
}
function renderLinks(){
  const q = ($('linkSearch').value||'').toLowerCase(); const cat = $('linkFilterCat').value;
  const all = LINKS.filter(l=>!l.is_client);
  renderQuickStats(all);
  document.querySelectorAll('#ibChips .ibx-chip').forEach(c=>{ const em=c.querySelector('em'); if(em) em.textContent=all.filter(l=>ibMatch(l,c.dataset.f)).length; });
  let filtered = all.filter(l=>{ if(cat && String(l.category_id)!==String(cat)) return false; if(!ibMatch(l,ibFilter)) return false; if(q && !(`${l.label||''} ${l.uuid||''} ${l.protocol||''}`).toLowerCase().includes(q)) return false; return true; });
  if(ibSort==='usage') filtered=filtered.slice().sort((a,b)=>Number(b.used_bytes||0)-Number(a.used_bytes||0));
  else if(ibSort==='exp') filtered=filtered.slice().sort((a,b)=>(a.expires_at?new Date(a.expires_at).getTime():9e15)-(b.expires_at?new Date(b.expires_at).getTime():9e15));
  else if(ibSort==='name') filtered=filtered.slice().sort((a,b)=>String(a.label||'').localeCompare(String(b.label||''),'fa'));
  $('linksEmpty').style.display = filtered.length ? 'none' : 'block';
  const _ibHtml = filtered.map(ibCardHtml).join('');
  const _ibGrid = $('ibGrid');
  if(_ibGrid.__vwHtml !== _ibHtml){ _ibGrid.innerHTML = _ibHtml; _ibGrid.__vwHtml = _ibHtml; }
  if($('ibCountLabel')) $('ibCountLabel').textContent = `${filtered.length} اینباند`;
  updateLinksBulkBar();
}
function toggleAllLinks(checked){
  document.querySelectorAll('.ib-row-check').forEach(c=>c.checked=checked);
  updateLinksBulkBar();
}
function selectedLinkUuids(){
  return Array.from(document.querySelectorAll('.ib-row-check:checked')).map(c=>c.dataset.uid);
}
function updateLinksBulkBar(){
  const sel = selectedLinkUuids();
  $('ibBulkBar').style.display = sel.length ? 'flex' : 'none';
  if($('ibSelCount')) $('ibSelCount').textContent = sel.length;
  const all = document.querySelectorAll('.ib-row-check');
  if($('ibSelAll')) $('ibSelAll').checked = all.length>0 && sel.length===all.length;
  document.querySelectorAll('.ib-card').forEach(card=>{
    const cb = card.querySelector('.ib-row-check');
    card.classList.toggle('ib-selected', !!(cb && cb.checked));
  });
}
async function bulkToggleLinks(active){
  const sel = selectedLinkUuids(); if(!sel.length) return;
  try{ await Promise.all(sel.map(uid=>api(`/api/links/${uid}`, {method:'PATCH', body: JSON.stringify({active})}))); toast('بروزرسانی گروهی انجام شد'); loadLinks(); }
  catch(e){ toast(e.message, false); }
}
async function bulkDeleteLinks(){
  const sel = selectedLinkUuids(); if(!sel.length) return;
  if(!confirm(`${sel.length} ${t('اینباند حذف شود؟')}`)) return;
  try{ await Promise.all(sel.map(uid=>api(`/api/links/${uid}`, {method:'DELETE'}))); toast('حذف گروهی انجام شد'); loadLinks(); }
  catch(e){ toast(e.message, false); }
}
async function openClients(uid){
  const inbound=LINKS.find(x=>x.uuid===uid); if(!inbound) return;
  try{
    const d=await api(`/api/links/${uid}/clients`);
    const clients=d.clients||[];
    openDrawer(`Client Manager · ${escapeHtml(inbound.label||'Inbound')}`, `
      <div class="client-manager">
        <div class="client-hero"><div><b>مدیریت کلاینت‌های واقعی</b><small>هر کلاینت UUID مستقل دارد و برای پروتکل‌های Live مستقیماً توسط Relay قابل احراز است.</small></div><span class="badge ${inbound.live_status==='live'?'green':'red'}">${inbound.live_status==='live'?'LIVE':'LINK-ONLY'}</span></div>
        ${inbound.live_status!=='live'?`<div class="notice danger-note">این اینباند فعلاً فقط لینک تولید می‌کند. برای Client واقعی، ابتدا یک ترکیب Live مثل VLESS + WS/TCP/XHTTP انتخاب کنید.</div>`:''}
        <div class="client-create"><div class="grp"><label>نام کلاینت</label><input id="clientName" placeholder="مثلاً iPhone · User 01"></div><div class="row2"><div class="grp"><label>حجم (GB، خالی = والد)</label><input id="clientLimit" type="number" min="0" placeholder="0"></div><div class="grp"><label>انقضا (روز، 0 = والد)</label><input id="clientDays" type="number" min="0" placeholder="0"></div></div><button class="btn primary" style="width:100%" onclick="createClient('${uid}')"><i class="ti ti-user-plus"></i>ساخت کلاینت واقعی</button></div>
        <div class="client-list">${clients.length?clients.map(c=>`<article class="client-row"><div class="client-avatar"><i class="ti ti-device-laptop"></i></div><div class="client-main"><b>${escapeHtml(c.label||'Client')}</b><small class="mono">${escapeHtml(c.uuid)}</small><div class="client-tags"><span>${c.active?'فعال':'خاموش'}</span><span>${fmtBytes(c.used_bytes||0)}${c.limit_bytes?' / '+fmtBytes(c.limit_bytes):''}</span><span>${c.expires_at?escapeHtml(c.expires_at.slice(0,10)):'∞'}</span></div></div><div class="client-actions"><button class="iconbtn" title="لینک اشتراک" onclick="showClientSubLink(${escapeHtml(JSON.stringify(c.sub||''))})"><i class="ti ti-qrcode"></i></button><button class="iconbtn" title="کپی VLESS" onclick="copyText(${escapeHtml(JSON.stringify(c.vless_full||''))})"><i class="ti ti-copy"></i></button><button class="iconbtn" title="تعویض لینک (UUID جدید)" onclick="regenerateClient('${uid}','${c.uuid}')"><i class="ti ti-replace"></i></button><button class="iconbtn" title="ریست حجم مصرفی" onclick="resetClientUsage('${uid}','${c.uuid}')"><i class="ti ti-refresh"></i></button><button class="iconbtn" title="حذف" onclick="deleteClient('${uid}','${c.uuid}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button></div></article>`).join(''):'<div class="empty-client">هنوز کلاینتی برای این اینباند ساخته نشده.</div>'}</div>
      </div>
  `, `<button class="btn" style="width:100%" onclick="loadLinks();openClients('${uid}')"><i class="ti ti-refresh"></i>بروزرسانی</button>`);
  }catch(e){toast(e.message,false)}
}
async function createClient(uid){
  const label=$('clientName')?.value||''; const limit=Number($('clientLimit')?.value||0); const days=Number($('clientDays')?.value||0);
  const parent = LINKS.find(x=>x.uuid===uid) || {};
  const outbound_proxy_id = await askOutboundChoice({title:'ساخت کلاینت', sub:'این کلاینت از کجا خارج شود؟', current: parent.outbound_proxy_id||''});
  if(outbound_proxy_id===null) return;
  try{
    const r = await api(`/api/links/${uid}/clients`,{method:'POST',body:JSON.stringify({label,limit_bytes:limit?limit*1024*1024*1024:0,expires_days:days,outbound_proxy_id})});
    openClients(uid); loadLinks();
    if(r.combo){ showClientPairResult(r); } else { toast('کلاینت واقعی ساخته شد ✓'); }
  }catch(e){ toast(e.message,false); }
}
function showClientPairResult(r){
  const subUrl = r.sub_url || '';
  const qr = qrSrc(subUrl);
  const rows = (r.clients||[]).map(i=>`<div class="ob-item"><b>${escapeHtml(i.label||'')}</b><small>${escapeHtml(protoLabel(i))} · پورت ${i.port||443}</small></div>`).join('');
  openDrawer('کلاینت WS + XHTTP ساخته شد ✓', `
    <div class="qr-box"><img src="${qr}"></div>
    <div class="grp"><label>لینک اشتراک این کاربر (۱ WS + ۱ XHTTP)</label><div class="copy-row"><input readonly dir="ltr" value="${escapeHtml(subUrl)}" id="cliPairSubInp" onclick="this.select()"></div></div>
    <div class="ob-items">${rows}</div>
    <p class="hint">این اینباند بخشی از یک جفت WS+XHTTP است؛ برای همین به‌جای دو کلاینت جدا، هر دو در یک لینک اشتراک قرار گرفتند.</p>
  `, `<button class="btn primary" style="width:100%" onclick="copyInput('cliPairSubInp')"><i class="ti ti-copy"></i>کپی لینک اشتراک</button>`);
}
async function deleteClient(uid,cid){
  if(!confirm(t('این کلاینت حذف شود؟'))) return;
  try{await api(`/api/links/${uid}/clients/${cid}`,{method:'DELETE'});toast('کلاینت حذف شد');openClients(uid);loadLinks();}catch(e){toast(e.message,false)}
}
async function regenerateClient(uid,cid){
  if(!confirm(t('یک لینک/UUID جدید برای این کلاینت صادر شود؟ لینک قبلی بلافاصله از کار می‌افتد و باید لینک جدید را دوباره برای کاربر بفرستید.'))) return;
  try{await api(`/api/links/${cid}/regenerate`,{method:'POST'});toast('لینک کلاینت تعویض شد ✓');openClients(uid);loadLinks();}catch(e){toast(e.message,false)}
}
async function resetClientUsage(uid,cid){
  if(!confirm(t('حجم مصرفی این کلاینت از صفر شروع شود؟'))) return;
  try{await api(`/api/links/${cid}/reset-usage`,{method:'POST'});toast('حجم مصرف ریست شد ✓');openClients(uid);loadLinks();}catch(e){toast(e.message,false)}
}

// ============================================================
// Standalone Client Manager page (بخش جدای ساخت کلاینت)
// ============================================================
let CM_INBOUNDS = [];
let CM_SELECTED_UID = '';
async function loadClientManager(){
  try{
    const res = await api('/api/links');
    CM_INBOUNDS = res.links || [];
    const sel = $('cmInboundSelect');
    const keep = CM_SELECTED_UID;
    sel.innerHTML = '<option value="">— انتخاب کنید —</option>' + CM_INBOUNDS.map(l=>
      `<option value="${l.uuid}">${escapeHtml(l.label||'Inbound')} · ${escapeHtml(protoLabel(l))} ${l.live_status==='live'?'(LIVE)':'(LINK-ONLY)'}</option>`
    ).join('');
    if(keep && CM_INBOUNDS.some(l=>l.uuid===keep)){
      sel.value = keep;
      loadClientManagerClients(keep);
    } else {
      $('cmInboundInfo').innerHTML = '';
      $('cmBody').innerHTML = `<div class="empty"><i class="ti ti-router"></i>ابتدا یک اینباند را از بالا انتخاب کن</div>`;
    }
  }catch(e){ toast(e.message, false); }
}
async function loadClientManagerClients(uid){
  CM_SELECTED_UID = uid || '';
  if(!uid){
    $('cmInboundInfo').innerHTML = '';
    $('cmBody').innerHTML = `<div class="empty"><i class="ti ti-router"></i>ابتدا یک اینباند را از بالا انتخاب کن</div>`;
    return;
  }
  const inbound = CM_INBOUNDS.find(x=>x.uuid===uid);
  try{
    const d = await api(`/api/links/${uid}/clients`);
    const clients = d.clients || [];
    $('cmInboundInfo').innerHTML = inbound ? `
      <div class="client-hero" style="margin-top:12px"><div><b>${escapeHtml(inbound.label||'Inbound')}</b><small>${escapeHtml(protoLabel(inbound))} · ${escapeHtml(inbound.address||'')}:${inbound.port||443}</small></div><span class="badge ${inbound.live_status==='live'?'green':'red'}">${inbound.live_status==='live'?'LIVE':'LINK-ONLY'}</span></div>
      ${inbound.live_status!=='live'?`<div class="notice danger-note" style="margin-top:10px">این اینباند فعلاً فقط لینک تولید می‌کند. برای Client واقعی، ابتدا یک ترکیب Live مثل VLESS + WS/TCP/XHTTP انتخاب کنید.</div>`:''}
    ` : '';
    $('cmBody').innerHTML = `
      <div class="card" style="padding:16px;margin-bottom:14px">
        <div class="client-create">
          <div class="grp"><label>نام کلاینت</label><input id="cmClientName" placeholder="مثلاً iPhone · User 01"></div>
          <div class="row2">
            <div class="grp"><label>حجم (GB، خالی = والد)</label><input id="cmClientLimit" type="number" min="0" placeholder="0"></div>
            <div class="grp"><label>انقضا (روز، 0 = والد)</label><input id="cmClientDays" type="number" min="0" placeholder="0"></div>
          </div>
          <button class="btn primary" style="width:100%" onclick="createClientMgr('${uid}')"><i class="ti ti-user-plus"></i>ساخت کلاینت واقعی</button>
        </div>
      </div>
      <div class="card" style="padding:16px">
        <div class="panel-head" style="padding:0 0 12px;border:0"><div><b>کلاینت‌های این اینباند</b><small>${clients.length} کلاینت</small></div></div>
        <div class="client-list">${clients.length ? clients.map(c=>`<article class="client-row"><div class="client-avatar"><i class="ti ti-device-laptop"></i></div><div class="client-main"><b>${escapeHtml(c.label||'Client')}</b><small class="mono">${escapeHtml(c.uuid)}</small><div class="client-tags"><span>${c.active?'فعال':'خاموش'}</span><span>${fmtBytes(c.used_bytes||0)}${c.limit_bytes?' / '+fmtBytes(c.limit_bytes):''}</span><span>${c.expires_at?escapeHtml(c.expires_at.slice(0,10)):'∞'}</span></div></div><div class="client-actions"><button class="iconbtn" title="لینک اشتراک" onclick="showClientSubLink(${escapeHtml(JSON.stringify(c.sub||''))})"><i class="ti ti-qrcode"></i></button><button class="iconbtn" title="کپی VLESS" onclick="copyText(${escapeHtml(JSON.stringify(c.vless_full||''))})"><i class="ti ti-copy"></i></button><button class="iconbtn" title="تعویض لینک (UUID جدید)" onclick="regenerateClientMgr('${uid}','${c.uuid}')"><i class="ti ti-replace"></i></button><button class="iconbtn" title="ریست حجم مصرفی" onclick="resetClientMgrUsage('${uid}','${c.uuid}')"><i class="ti ti-refresh"></i></button><button class="iconbtn" title="حذف" onclick="deleteClientMgr('${uid}','${c.uuid}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button></div></article>`).join('') : '<div class="empty-client">هنوز کلاینتی برای این اینباند ساخته نشده.</div>'}</div>
      </div>
    `;
  }catch(e){ toast(e.message, false); }
}
async function createClientMgr(uid){
  const label = $('cmClientName').value.trim();
  const limit = Number($('cmClientLimit').value) || 0;
  const days = Number($('cmClientDays').value) || 0;
  const parent = (typeof CM_INBOUNDS!=='undefined' && CM_INBOUNDS.find(x=>x.uuid===uid)) || LINKS.find(x=>x.uuid===uid) || {};
  const outbound_proxy_id = await askOutboundChoice({title:'ساخت کلاینت', sub:'این کلاینت از کجا خارج شود؟', current: parent.outbound_proxy_id||''});
  if(outbound_proxy_id===null) return;
  try{
    const r = await api(`/api/links/${uid}/clients`, {method:'POST', body: JSON.stringify({label, limit_bytes: limit ? limit*1024*1024*1024 : 0, expires_days: days, outbound_proxy_id})});
    loadClientManagerClients(uid);
    if(r.combo){ showClientPairResult(r); } else { toast('کلاینت واقعی ساخته شد ✓'); }
  }catch(e){ toast(e.message, false); }
}
async function deleteClientMgr(uid, cid){
  if(!confirm(t('این کلاینت حذف شود؟'))) return;
  try{ await api(`/api/links/${uid}/clients/${cid}`, {method:'DELETE'}); toast('کلاینت حذف شد'); loadClientManagerClients(uid); }
  catch(e){ toast(e.message, false); }
}
async function regenerateClientMgr(uid, cid){
  if(!confirm(t('یک لینک/UUID جدید برای این کلاینت صادر شود؟ لینک قبلی بلافاصله از کار می‌افتد و باید لینک جدید را دوباره برای کاربر بفرستید.'))) return;
  try{ await api(`/api/links/${cid}/regenerate`, {method:'POST'}); toast('لینک کلاینت تعویض شد ✓'); loadClientManagerClients(uid); }
  catch(e){ toast(e.message, false); }
}
async function resetClientMgrUsage(uid, cid){
  if(!confirm(t('حجم مصرفی این کلاینت از صفر شروع شود؟'))) return;
  try{ await api(`/api/links/${cid}/reset-usage`, {method:'POST'}); toast('حجم مصرف ریست شد ✓'); loadClientManagerClients(uid); }
  catch(e){ toast(e.message, false); }
}
async function copyText(v, okMsg){
  v = v || '';
  const done = okMsg || 'کپی شد ✓';
  if(window.isSecureContext && navigator.clipboard && navigator.clipboard.writeText){
    try{ await navigator.clipboard.writeText(v); toast(done); return; }catch(e){ /* برو سراغ روش قدیمی */ }
  }
  if(legacyCopy(v)){ toast(done); } else { prompt('کپی کنید:', v); }
}
function showClientSubLink(subUrl){
  if(!subUrl){ toast('لینک ساب برای این کلاینت در دسترس نیست', false); return; }
  const qr = qrSrc(subUrl);
  openDrawer('لینک اشتراک کلاینت', `
    <div class="qr-box"><img src="${qr}"></div>
    <div class="grp"><label>لینک ساب</label><div class="copy-row"><input readonly dir="ltr" value="${escapeHtml(subUrl)}" id="clientSubLinkInp" onclick="this.select()"></div></div>
    <p class="hint">اگر این لینک برای مشتری باز نمی‌شود، ابتدا از تب «تنظیمات» آدرس عمومی پنل را درست تنظیم کنید.</p>
  `, `<button class="btn primary" style="width:100%" onclick="copyInput('clientSubLinkInp')"><i class="ti ti-copy"></i>کپی لینک ساب</button>`);
}

function showSubLink(uid){
  const l = LINKS.find(x=>x.uuid===uid);
  if(!l) return;
  const url = l.sub_url || l.sub || '';
  openDrawer('لینک اشتراک', `
    <div class="qr-box"><img src="${qrSrc(url)}" alt="QR"></div>
    <div class="grp"><label>لینک اشتراک <span class="one-link-tag">یک لینک برای اپ و مرورگر</span></label>
      <div class="copy-row"><input readonly dir="ltr" value="${escapeHtml(url)}" id="subLinkInp" onclick="this.select()"><button type="button" class="iconbtn copy-ico" title="کپی" onclick="copyInput('subLinkInp')"><i class="ti ti-copy"></i></button></div>
    </div>
    <p class="hint"><i class="ti ti-apps"></i> داخل اپ (v2rayNG، Hiddify، …) همین لینک کانفیگ‌ها را بالا می‌آورد.<br><i class="ti ti-browser"></i> داخل مرورگر همین لینک صفحه‌ی گرافیکی حجم و زمان باقی‌مانده را نشان می‌دهد.</p>
    <p class="hint">اگر این لینک برای مشتری باز نمی‌شود، ابتدا از تب «تنظیمات» آدرس عمومی پنل را درست تنظیم کنید.</p>
  `, `<button class="btn primary" style="width:100%" onclick="copyInput('subLinkInp')"><i class="ti ti-copy"></i>کپی لینک ساب</button>`);
}
function legacyCopy(text){
  // execCommand روی همه‌ی مرورگرها حتی بدون HTTPS (secure context) کار می‌کند.
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.top = '-9999px';
  ta.style.left = '-9999px';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  let ok = false;
  try{ ok = document.execCommand('copy'); }catch(e){ ok = false; }
  document.body.removeChild(ta);
  return ok;
}
async function copyInput(id){
  const el = $(id);
  if(!el) return;
  const value = el.value || '';
  el.focus();
  el.select();
  // navigator.clipboard فقط در HTTPS (secure context) در دسترسه؛ اگر پنل با HTTP
  // (بدون دامنه/SSL) باز شده باشه این آبجکت اصلاً وجود نداره و باید مستقیم به
  // روش قدیمی (execCommand) یا در آخرین حالت به prompt دستی سوییچ کنیم.
  if(window.isSecureContext && navigator.clipboard && navigator.clipboard.writeText){
    try{
      await navigator.clipboard.writeText(value);
      toast('کپی شد ✓');
      return;
    }catch(e){ /* برو سراغ روش قدیمی */ }
  }
  if(legacyCopy(value)){
    toast('کپی شد ✓');
  } else {
    prompt('کپی کنید:', value);
  }
}
async function toggleLink(uid, active){
  try{ await api(`/api/links/${uid}`, {method:'PATCH', body: JSON.stringify({active})}); toast('بروزرسانی شد'); loadLinks(); }
  catch(e){ toast(e.message, false); }
}
async function deleteLink(uid){
  if(!confirm(t('این کانفیگ حذف شود؟'))) return;
  try{ await api(`/api/links/${uid}`, {method:'DELETE'}); toast('حذف شد'); loadLinks(); }
  catch(e){ toast(e.message, false); }
}
async function resetLinkUsage(uid){
  if(!confirm(t('حجم مصرفی این کانفیگ از صفر شروع شود؟'))) return;
  try{ await api(`/api/links/${uid}/reset-usage`, {method:'POST'}); toast('حجم مصرف ریست شد'); loadLinks(); }
  catch(e){ toast(e.message, false); }
}
async function regenerateLink(uid){
  if(!confirm(t('یک لینک/UUID جدید صادر شود؟ لینک قبلی بلافاصله از کار می‌افتد و باید لینک جدید را دوباره برای کاربر بفرستید.'))) return;
  try{ const r = await api(`/api/links/${uid}/regenerate`, {method:'POST'}); toast('لینک جدید صادر شد'); loadLinks(); showSubLink(r.uuid); }
  catch(e){ toast(e.message, false); }
}
async function openAutoLink(){
  // ساخت سریع = یک اشتراک واحد؛ برای هر خروجی انتخاب‌شده «یک WS + یک XHTTP» داخلش می‌ره.
  const q = localStorage.getItem('vw_quick_outbound_proxy') || '';
  const exits = await askOutboundChoice({
    title: 'ساخت سریع — WS + XHTTP در یک اشتراک',
    sub: 'خروجی را انتخاب کن؛ می‌توانی چند خروجی هم‌زمان بزنی (برای هرکدام یک WS + یک XHTTP).',
    multi: true, current: [q]
  });
  if(exits === null) return;
  try{
    const r = await api('/api/links/auto', {method:'POST', body: JSON.stringify({combo:true, port:443, profile:'balanced', outbound_proxy_ids: exits})});
    loadLinks();
    showComboResult(r);
  }
  catch(e){ toast(e.message, false); }
}
function showComboResult(r){
  const subUrl = r.sub_url || '';
  const qr = qrSrc(subUrl);
  const byUid = Object.fromEntries((r.items||[]).map(i=>[i.uuid, i]));
  const exits = (r.exits && r.exits.length) ? r.exits : [{outbound: r.outbound}];
  const blocks = exits.map(e=>{
    const ob = e.outbound;
    const head = ob
      ? `${flagHtml(ob)} <b>${escapeHtml(ob.country||ob.name||'')}</b> <small>پراکسی «${escapeHtml(ob.name||'')}»</small>`
      : `<span class="ob-emoji">🚀</span> <b>مستقیم</b> <small>خود Railway</small>`;
    const rows = [['ws','VLESS · WebSocket'],['xhttp','VLESS · XHTTP']].map(([k,lbl])=>{
      const i = byUid[e[k]]; return i ? `<div class="ob-item"><b>${escapeHtml(i.label||'')}</b><small>${lbl} · پورت ${i.port||443}</small></div>` : '';
    }).join('');
    return `<div class="ob-note ${ob?'ok':''}">${head}</div><div class="ob-items">${rows}</div>`;
  }).join('');
  openDrawer('اشتراک ساخته شد ✓', `
    <div class="qr-box"><img src="${qr}"></div>
    <div class="grp"><label>لینک اشتراک (${(r.items||[]).length} کانفیگ) <span class="one-link-tag">یک لینک برای اپ و مرورگر</span></label><div class="copy-row"><input readonly dir="ltr" value="${escapeHtml(subUrl)}" id="comboSubInp" onclick="this.select()"><button type="button" class="iconbtn copy-ico" title="کپی" onclick="copyInput('comboSubInp')"><i class="ti ti-copy"></i></button></div></div>
    ${blocks}
    <p class="hint">همین اشتراک در تب «گروه‌های ساب» هم دیده می‌شود.</p>
  `, `<button class="btn primary" style="width:100%" onclick="copyInput('comboSubInp')"><i class="ti ti-copy"></i>کپی لینک اشتراک</button>`);
}

// ══════════════════════ پراکسی IP (SOCKS) — مسیر خروجی ══════════════════════
let PROXIES_CACHE = [];
let PROXIES_ERR = '';
async function loadProxies(){
  try{ const r = await api('/api/proxies'); PROXIES_CACHE = r.proxies||[]; PROXIES_ERR = ''; }
  catch(e){ PROXIES_ERR = e.message || 'خطا در دریافت لیست'; }
  renderProxiesSettings(); renderOutboundProxySelects(); refreshOutboundPickers();
}
function ensureObStyle(){
  if(document.getElementById('obStyle')) return;
  const st = document.createElement('style'); st.id = 'obStyle';
  st.textContent = `
  .ob-ov{position:fixed;inset:0;background:rgba(4,6,10,.62);backdrop-filter:blur(3px);z-index:150;display:flex;align-items:center;justify-content:center;padding:16px}
  .ob-box{width:min(460px,100%);max-height:88vh;display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--line2);border-radius:18px;box-shadow:var(--shadow-md);overflow:hidden}
  .ob-box h3{font-size:15px;padding:16px 18px 4px}
  .ob-box>p{font-size:12px;color:var(--sub);padding:0 18px 12px}
  .ob-list{overflow:auto;padding:0 14px 6px;display:flex;flex-direction:column;gap:8px}
  .ob-row{display:flex;align-items:center;gap:11px;padding:11px 12px;border:1px solid var(--line);border-radius:13px;cursor:pointer;background:var(--panel2);transition:.15s}
  .ob-row:hover{border-color:var(--line2)}
  .ob-row.on{border-color:var(--accent);background:rgba(var(--accent-rgb),.10)}
  .ob-row input{accent-color:var(--accent)}
  .ob-row .ob-txt{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
  .ob-row .ob-txt b{font-size:13px}
  .ob-row .ob-txt small,.ob-pmain small,.ob-item small{font-size:11px;color:var(--sub)}
  .ob-foot{display:flex;gap:8px;padding:14px 16px;border-top:1px solid var(--line);margin-top:8px}
  .ob-foot .btn{flex:1;justify-content:center}
  .ob-flagimg{width:26px;height:19px;border-radius:3px;object-fit:cover;box-shadow:0 0 0 1px rgba(255,255,255,.12);vertical-align:middle}
  .ob-emoji{font-size:20px;line-height:1}
  .ob-badge{display:inline-block;padding:3px 9px;border-radius:999px;font-size:11px;font-weight:700;background:rgba(135,146,168,.14);color:var(--sub);white-space:nowrap}
  .ob-badge.good{background:rgba(34,197,139,.14);color:var(--good)}
  .ob-badge.warn{background:rgba(245,165,36,.14);color:var(--warn)}
  .ob-badge.bad{background:rgba(242,73,85,.14);color:var(--bad)}
  .ob-prow{display:flex;align-items:center;gap:12px;padding:12px;border:1px solid var(--line);border-radius:13px;margin-bottom:9px;background:var(--panel2);flex-wrap:wrap}
  .ob-pflag{width:30px;text-align:center}
  .ob-pmain{flex:1;min-width:180px;display:flex;flex-direction:column;gap:3px}
  .ob-pmain b{font-size:13px}
  .ob-pping{display:flex;flex-direction:column;align-items:center;gap:3px;min-width:78px}
  .ob-pping small{font-size:10px;color:var(--sub2)}
  .ob-ok{color:var(--good)!important}.ob-bad{color:var(--bad)!important}
  .ib-ob-tag{display:inline-flex;align-items:center;gap:5px}
  .ib-ob-tag .ob-flagimg{width:16px;height:12px}
  .ob-note{padding:10px 12px;border-radius:11px;background:var(--panel2);border:1px solid var(--line);font-size:12px;margin:10px 0;display:flex;align-items:center;gap:8px}
  .ob-note.ok{border-color:rgba(34,197,139,.35)}
  .ob-items{display:flex;flex-direction:column;gap:6px;margin:8px 0}
  .ob-item{padding:9px 12px;border:1px solid var(--line);border-radius:10px;display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:12px}
  .ob-box.wide{width:min(640px,100%)}
  .ob-mgr-body{overflow:auto;padding:0 18px 4px}
  .ob-hint{margin:8px 16px 0;padding:9px 12px;border-radius:10px;background:var(--panel2);border:1px solid var(--line);font-size:11.5px;color:var(--sub);display:flex;gap:6px;align-items:flex-start}
  .ob-picker{display:flex;flex-direction:column;gap:8px;margin:8px 0}
  .ob-seg{display:flex;gap:6px;padding:4px;border:1px solid var(--line);border-radius:13px;background:var(--panel2);margin-bottom:14px}
  .ob-seg button{flex:1;padding:9px 10px;border:0;border-radius:10px;background:transparent;color:var(--sub);font-size:12.5px;font-weight:700;cursor:pointer;display:flex;gap:6px;align-items:center;justify-content:center;font-family:inherit}
  .ob-seg button.on{background:var(--accent);color:#fff}
  `;
  document.head.appendChild(st);
}
ensureObStyle();
function flagHtml(p){
  p = p || {};
  const cc = String(p.country_code||'').toLowerCase();
  const emoji = p.flag || '🏳️';
  if(!/^[a-z]{2}$/.test(cc)) return `<span class="ob-emoji">${emoji}</span>`;
  // ویندوز پرچم ایموجی رو نشون نمی‌ده، پس از تصویر پرچم استفاده می‌کنیم و اگه لود نشد ایموجی جایگزین می‌شه
  return `<img class="ob-flagimg" src="https://flagcdn.com/w40/${cc}.png" alt="${cc.toUpperCase()}" loading="lazy" onerror="this.outerHTML='<span class=&quot;ob-emoji&quot;>${emoji}</span>'">`;
}
function pingText(p){
  if(!p.tested_at) return 'تست‌نشده';
  if(!p.test_ok || p.ping_ms==null) return 'قطع';
  return `${Math.round(p.ping_ms)}ms`;
}
function pingClass(p){
  if(!p.tested_at) return '';
  if(!p.test_ok || p.ping_ms==null) return 'bad';
  return p.ping_ms < 300 ? 'good' : (p.ping_ms < 800 ? 'warn' : 'bad');
}
function proxyLabel(p){
  const flag = p.flag || '🏳️';
  return `${flag} ${p.name} — ${p.country||'?'} · ${pingText(p)}`;
}
function renderOutboundProxySelects(){
  document.querySelectorAll('[data-outbound-proxy-select]').forEach(sel=>{
    const cur = sel.value;
    sel.innerHTML = '<option value="">🚀 مستقیم (خود Railway)</option>' + PROXIES_CACHE.map(p=>`<option value="${escapeHtml(p.id)}">${escapeHtml(proxyLabel(p))}</option>`).join('');
    if([...sel.options].some(o=>o.value===cur)) sel.value = cur;
  });
}
function renderProxiesSettings(){
  const html = proxiesListHtml();
  ['proxiesListWrap','dProxiesListWrap'].forEach(id=>{ const w=document.getElementById(id); if(w) w.innerHTML = html; });
}
function proxiesListHtml(){
  if(PROXIES_ERR && !PROXIES_CACHE.length){ return `<div class="notice danger-note">لیست پراکسی‌ها از سرور گرفته نشد: ${escapeHtml(PROXIES_ERR)} — مطمئن شو outbound_proxy.py و python-socks روی سرور نصب/دیپلوی شده‌اند.</div>`; }
  if(!PROXIES_CACHE.length){ return '<div class="muted" style="padding:12px">هنوز پراکسی‌ای اضافه نشده. با فرم بالا یک SOCKS5 اضافه کن.</div>'; }
  const quick = localStorage.getItem('vw_quick_outbound_proxy') || '';
  return PROXIES_CACHE.map(p=>`
    <div class="ob-prow">
      <div class="ob-pflag">${flagHtml(p)}</div>
      <div class="ob-pmain">
        <b>${escapeHtml(p.name)}</b>
        <small class="mono" style="direction:ltr;text-align:left">${escapeHtml(String(p.scheme||'socks5').toUpperCase())} · ${escapeHtml(p.host)}:${p.port}${p.has_auth?' · 🔑':''}</small>
        <small>${p.country?escapeHtml(p.country):'کشور نامشخص'}${p.city?' · '+escapeHtml(p.city):''}${p.isp?' · '+escapeHtml(p.isp):''}${p.exit_ip?` · IP خروجی: <span class="mono">${escapeHtml(p.exit_ip)}</span>`:''}${p.tls_state==='intercepted'?' · <span class="ob-bad">TLS رهگیری‌شده ⚠</span>':''}${p.breaker_open?' · <span class="ob-bad">موقتاً قطع‌شده (circuit)</span>':''}</small>
        ${p.test_message?`<small class="${p.test_ok?'ob-ok':'ob-bad'}">${escapeHtml(p.test_message)}</small>`:''}
        ${p.in_use?`<small>${p.in_use} کانفیگ از این پراکسی استفاده می‌کنند</small>`:''}
      </div>
      <div class="ob-pping"><span class="ob-badge ${pingClass(p)}">${pingText(p)}</span><small>پینگ واقعی</small>${p.tcp_ms!=null?`<small>TCP ${Math.round(p.tcp_ms)}ms</small>`:''}${p.score!=null&&p.test_ok?`<span class="ob-badge ${scGradeClass(p.grade)}" title="امتیاز کیفیت">${p.score} · ${escapeHtml(p.grade||'')}</span>`:''}</div>
      <button class="btn sm" onclick="testProxyRow('${p.id}')"><i class="ti ti-activity"></i> تست</button>
      <button class="btn sm" onclick="setQuickProxy('${p.id}')" title="انتخاب پیش‌فرض در پنجره‌ی «ساخت سریع»" style="${quick===p.id?'border-color:var(--accent);color:var(--accent)':''}"><i class="ti ti-star"></i></button>
      <button class="btn sm danger" onclick="deleteProxyRow('${p.id}')"><i class="ti ti-trash"></i></button>
    </div>`).join('');
}
async function testProxyRow(id, silent){
  try{
    if(!silent) toast('در حال تست تونل SOCKS5 و کشور خروجی...');
    const r = await api(`/api/proxies/${id}/test`, {method:'POST'});
    await loadProxies();
    if(!silent){ const p=r.proxy||{}; toast(p.test_ok ? `${p.country||'?'} · ${Math.round(p.ping_ms)}ms ✓` : (p.test_message||'تست ناموفق'), !!p.test_ok); }
  }
  catch(e){ toast(e.message, false); }
}
async function testAllProxies(){
  if(!PROXIES_CACHE.length){ toast('پراکسی‌ای برای تست نیست', false); return; }
  toast('در حال تست همه‌ی پراکسی‌ها...');
  try{
    const r = await api('/api/proxies/scan/saved', {method:'POST', body: JSON.stringify({samples:2})});
    let j;
    do{ await scSleep(800); j = await api(`/api/proxies/scan/${r.job_id}?since=999999`); }while(j.state==='running');
    await loadProxies();
    toast(`${j.working} از ${j.total} پراکسی سالم است`, j.working>0);
  }catch(e){ toast(e.message, false); }
}
async function deleteProxyRow(id){
  const p = PROXIES_CACHE.find(x=>x.id===id);
  const warn = p && p.in_use ? `\n\n${p.in_use} کانفیگ از این پراکسی استفاده می‌کنند و به حالت «مستقیم» برمی‌گردند.` : '';
  if(!confirm('این پراکسی حذف شود؟' + warn)) return;
  try{ await api(`/api/proxies/${id}`, {method:'DELETE'}); if(localStorage.getItem('vw_quick_outbound_proxy')===id) localStorage.removeItem('vw_quick_outbound_proxy'); await loadProxies(); toast('حذف شد'); }
  catch(e){ toast(e.message, false); }
}
function setQuickProxy(id){
  localStorage.setItem('vw_quick_outbound_proxy', id);
  renderProxiesSettings();
  toast('این پراکسی در پنجره‌ی «ساخت سریع» از قبل انتخاب می‌شود ✓');
}
async function addProxyForm(prefix){
  prefix = prefix || 'px';
  const el = k => document.getElementById(prefix + k);
  const name = el('Name')?.value.trim();
  const host = el('Host')?.value.trim();
  const port = Number(el('Port')?.value || 1080);
  const username = el('User')?.value.trim();
  const password = el('Pass')?.value.trim();
  if(!host){ toast('آدرس پراکسی را وارد کنید', false); return; }
  try{
    const r = await api('/api/proxies', {method:'POST', body: JSON.stringify({name,host,port,username,password})});
    ['Name','Host','User','Pass'].forEach(k=>{ if(el(k)) el(k).value=''; }); if(el('Port')) el('Port').value='1080';
    await loadProxies();
    toast('پراکسی اضافه شد — در حال تست...');
    if(r.proxy?.id) testProxyRow(r.proxy.id);
  }catch(e){ toast(e.message, false); }
}

// پنجره‌ی انتخاب مسیر خروجی (Promise):
//   multi=false → '' (مستقیم) | id ;  multi=true → آرایه‌ای از '' / idها ;  انصراف → null
//   requireProxies=true → اگه هیچ پراکسی‌ای نیست، به‌جای پرسیدن مدیریت اوتباند رو باز می‌کنه.
async function askOutboundChoice(opts){
  opts = opts || {};
  await loadProxies();
  if(!PROXIES_CACHE.length){
    if(opts.requireProxies){ toast('هنوز پراکسی‌ای اضافه نشده؛ اول یک SOCKS5 اضافه کن', false); openOutboundManager(); return null; }
    return opts.multi ? [''] : '';
  }
  ensureObStyle();
  const cur = (Array.isArray(opts.current) ? opts.current : [opts.current || '']).filter(id=>id==='' || PROXIES_CACHE.some(p=>p.id===id));
  return new Promise(resolve=>{
    const ov = document.createElement('div'); ov.className = 'ob-ov';
    ov.innerHTML = `<div class="ob-box" role="dialog"><h3>${escapeHtml(opts.title||'مسیر خروجی')}</h3><p>${escapeHtml(opts.sub||'ترافیک از کجا خارج شود؟')}</p>
      <div class="ob-list ob-picker">${outboundPickerHtml('obChoice', !!opts.multi, cur.length ? cur : [''])}</div>
      ${opts.note?`<div class="ob-hint"><i class="ti ti-info-circle"></i> ${escapeHtml(opts.note)}</div>`:''}
      <div class="ob-foot"><button class="btn" data-a="cancel">انصراف</button><button class="btn primary" data-a="ok"><i class="ti ti-check"></i>ادامه</button></div></div>`;
    const done = v => { document.removeEventListener('keydown', onKey); ov.remove(); resolve(v); };
    const onKey = e => { if(e.key==='Escape') done(null); };
    document.addEventListener('keydown', onKey);
    ov.addEventListener('click', e=>{
      if(e.target===ov) return done(null);
      const a = e.target.closest('[data-a]'); if(!a) return;
      if(a.dataset.a==='cancel') return done(null);
      const vals = readOutboundPicker(ov, 'obChoice');
      if(!vals.length){ toast('حداقل یک گزینه را انتخاب کن', false); return; }
      done(opts.multi ? vals : vals[0]);
    });
    document.body.appendChild(ov);
  });
}

// انتخابگر خروجی (رادیو یا چندانتخابی) — هم داخل پنجره و هم داخل drawer استفاده می‌شود
function outboundPickerHtml(name, multi, selected){
  const sel = new Set(selected && selected.length ? selected : ['']);
  const type = multi ? 'checkbox' : 'radio';
  const items = [{id:'', direct:true}, ...PROXIES_CACHE];
  return items.map(x=>{
    const on = sel.has(x.id);
    const input = `<input type="${type}" name="${name}" value="${escapeHtml(x.id)}" ${on?'checked':''}>`;
    if(x.direct) return `<label class="ob-row ${on?'on':''}">${input}<span class="ob-emoji">🚀</span><span class="ob-txt"><b>مستقیم (خود Railway)</b><small>ترافیک از IP سرور Railway خارج می‌شود</small></span></label>`;
    return `<label class="ob-row ${on?'on':''}">${input}${flagHtml(x)}<span class="ob-txt"><b>${escapeHtml(x.name)}</b><small>${x.country?escapeHtml(x.country):'کشور نامشخص'}${x.exit_ip?' · '+escapeHtml(x.exit_ip):''}</small></span><span class="ob-badge ${pingClass(x)}">${pingText(x)}</span></label>`;
  }).join('');
}
function readOutboundPicker(root, name){
  return [...(root||document).querySelectorAll(`input[name="${name}"]:checked`)].map(i=>i.value);
}
function refreshOutboundPickers(){
  document.querySelectorAll('[data-ob-picker]').forEach(box=>{
    const name = box.dataset.obPicker;
    const cur = readOutboundPicker(box, name);
    box.innerHTML = outboundPickerHtml(name, box.dataset.multi==='1', cur);
  });
  if(typeof updateComboSummary==='function') updateComboSummary();
}
if(!window.__obPickerBound){
  window.__obPickerBound = true;
  document.addEventListener('change', e=>{
    const inp = e.target;
    if(!(inp && inp.matches && inp.matches('.ob-row input'))) return;
    const grp = inp.closest('.ob-picker');
    if(grp) grp.querySelectorAll('.ob-row').forEach(r=>r.classList.toggle('on', r.querySelector('input').checked));
    if(typeof updateComboSummary==='function') updateComboSummary();
  });
}

// ─────────────── مدیریت اوتباند (پنجره‌ی مستقل، از هر جا قابل‌باز شدن) ───────────────
function openOutboundManager(){
  ensureObStyle();
  if(document.getElementById('obMgr')) return;
  const ov = document.createElement('div'); ov.className = 'ob-ov'; ov.id = 'obMgr';
  ov.innerHTML = `<div class="ob-box wide" role="dialog">
    <h3><i class="ti ti-route"></i> اوتباند — پراکسی‌ها (SOCKS5 · SOCKS4 · HTTP)</h3>
    <p>هر پراکسی که اینجا اضافه کنی تست واقعی می‌شود (پینگ از داخل تونل، کشور/پرچم/ISP خروجی، امتیاز کیفیت). بعد می‌توانی هر اینباند/کلاینت را روی آن بگذاری. برای افزودن تکیِ HTTP یا SOCKS4 آدرس کامل را بنویس، مثلاً http://user:pass@1.2.3.4:8080</p>
    <div class="ob-mgr-body">
      <div class="ob-seg" style="margin-bottom:12px">
        <button type="button" id="obAddSingleBtn" class="on" onclick="setObAddMode('single')"><i class="ti ti-plus"></i> افزودن تکی</button>
        <button type="button" id="obAddScanBtn" onclick="setObAddMode('scan')"><i class="ti ti-radar-2"></i> اسکن و افزودن گروهی</button>
      </div>
      <div id="obAddSingle">
        <div class="row2"><div class="grp"><label>نام دلخواه</label><input id="dpxName" placeholder="مثلاً آلمان-۱"></div><div class="grp"><label>Host / آدرس کامل</label><input id="dpxHost" class="mono" style="direction:ltr;text-align:left" placeholder="1.2.3.4  یا  socks5://user:pass@host:1080"></div></div>
        <div class="row2"><div class="grp"><label>Port</label><input id="dpxPort" class="mono" style="direction:ltr;text-align:left" value="1080"></div><div class="grp"><label>Username (اختیاری)</label><input id="dpxUser" class="mono" style="direction:ltr;text-align:left"></div></div>
        <div class="row2"><div class="grp"><label>Password (اختیاری)</label><input id="dpxPass" type="password" class="mono" style="direction:ltr;text-align:left"></div><div class="grp" style="display:flex;align-items:flex-end"><button class="btn primary" style="width:100%" onclick="addProxyForm('dpx')"><i class="ti ti-plus"></i> افزودن و تست</button></div></div>
      </div>
      <div id="obAddScan" style="display:none">
        <p class="hint" style="margin-top:0">لیست پراکسی‌های خودت را (پیست یا لینک لیست سرویس‌دهنده‌ات) بده؛ همه موازی و زنده با تونل واقعی تست می‌شوند: پروتکل، پینگ و پایداری، کشور/شهر/ISP خروجی، رهگیری TLS و امتیاز کیفیت. پراکسی رایگان عمومی از اینترنت جمع‌آوری نمی‌کنیم و آدرس‌های داخلی/لوکال رد می‌شوند.</p>
        <div class="ob-seg" style="margin-bottom:8px">
          <button type="button" id="scanSrcTextBtn" class="on" onclick="setScanSource('text')"><i class="ti ti-clipboard-text"></i> پیست لیست</button>
          <button type="button" id="scanSrcUrlBtn" onclick="setScanSource('url')"><i class="ti ti-link"></i> از یک URL</button>
        </div>
        <div id="scanTextWrap"><textarea id="scanText" rows="4" class="mono" style="direction:ltr;text-align:left;width:100%;resize:vertical" placeholder="هر خط یک پروکسی — فرمت‌ها:&#10;1.2.3.4:1080&#10;1.2.3.4:1080:user:pass&#10;user:pass@1.2.3.4:1080&#10;socks5://user:pass@1.2.3.4:1080&#10;http://1.2.3.4:8080&#10;socks4://1.2.3.4:1080"></textarea></div>
        <div id="scanUrlWrap" style="display:none"><input id="scanUrl" class="mono" style="direction:ltr;text-align:left" placeholder="https://provider.com/my-proxy-list.txt"></div>
        <div class="sc-opts">
          <label class="sc-opt">پروتکل<select id="scanProto"><option value="socks5">SOCKS5</option><option value="auto">تشخیص خودکار</option><option value="http">HTTP (CONNECT)</option><option value="socks4">SOCKS4</option></select></label>
          <label class="sc-opt">دقت تست<select id="scanSamples"><option value="1">سریع (۱ نمونه)</option><option value="3" selected>متعادل (۳ نمونه)</option><option value="5">دقیق (۵ نمونه)</option></select></label>
          <label class="sc-opt">هم‌زمانی<select id="scanConc"><option value="20">کم (۲۰)</option><option value="40" selected>متوسط (۴۰)</option><option value="80">زیاد (۸۰)</option></select></label>
          <label class="sc-opt sc-chk"><input type="checkbox" id="scanTls" checked> بررسی رهگیری TLS</label>
          <label class="sc-opt sc-chk"><input type="checkbox" id="scanSpeed"> تست سرعت دانلود</label>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">
          <button class="btn primary sm" id="scanBtn" onclick="runProxyScan()"><i class="ti ti-radar-2"></i> شروع اسکن</button>
          <button class="btn sm danger" id="scanCancelBtn" style="display:none" onclick="cancelProxyScan()"><i class="ti ti-player-stop"></i> لغو اسکن</button>
        </div>
        <div id="scanResultsWrap" style="margin-top:12px"></div>
      </div>
      <div class="divider"></div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px"><b style="font-size:13px">پراکسی‌های ذخیره‌شده</b><button class="btn sm" onclick="testAllProxies()"><i class="ti ti-activity"></i> تست همه</button></div>
      <div id="dProxiesListWrap"></div>
    </div>
    <div class="ob-foot"><button class="btn" data-a="close">بستن</button></div></div>`;
  const close = () => { document.removeEventListener('keydown', onKey); ov.remove(); };
  const onKey = e => { if(e.key==='Escape') close(); };
  document.addEventListener('keydown', onKey);
  ov.addEventListener('click', e=>{ if(e.target===ov || e.target.closest('[data-a="close"]')) close(); });
  document.body.appendChild(ov);
  loadProxies();
}
function setObAddMode(mode){
  document.getElementById('obAddSingleBtn').classList.toggle('on', mode==='single');
  document.getElementById('obAddScanBtn').classList.toggle('on', mode==='scan');
  document.getElementById('obAddSingle').style.display = mode==='single' ? '' : 'none';
  document.getElementById('obAddScan').style.display = mode==='scan' ? '' : 'none';
}
function setScanSource(src){
  document.getElementById('scanSrcTextBtn').classList.toggle('on', src==='text');
  document.getElementById('scanSrcUrlBtn').classList.toggle('on', src==='url');
  document.getElementById('scanTextWrap').style.display = src==='text' ? '' : 'none';
  document.getElementById('scanUrlWrap').style.display = src==='url' ? '' : 'none';
}
/* ===== Pro proxy scanner UI (live progress via polling) ===== */
let SCAN_RESULTS = [];
let SCAN_JOB = null;
let SCAN_VIEW = [];
let SCAN_SHOWN = 0;
const SCAN_PAGE = 120;
function ensureScanStyle(){
  if(document.getElementById('scanStyle')) return;
  const st = document.createElement('style'); st.id = 'scanStyle';
  st.textContent = `
  .sc-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin:8px 0}
  .sc-opt{display:flex;flex-direction:column;gap:5px;font-size:11px;color:var(--sub2);font-weight:700}
  .sc-opt select{padding:8px 10px;border-radius:10px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font:inherit;font-size:12px}
  .sc-chk{flex-direction:row;align-items:center;gap:8px;padding:8px 10px;border:1px solid var(--line);border-radius:10px;background:var(--panel2);cursor:pointer;color:var(--text)}
  .sc-chk input{accent-color:var(--accent)}
  .sc-live{border:1px solid var(--line);border-radius:14px;padding:12px;background:var(--panel2)}
  .sc-head{display:flex;justify-content:space-between;align-items:center;font-size:12.5px;margin-bottom:8px}
  .sc-head span{color:var(--sub2);font-size:11px;direction:ltr}
  .sc-bar{height:8px;border-radius:99px;background:var(--line);overflow:hidden}
  .sc-bar i{display:block;height:100%;width:0;border-radius:99px;background:linear-gradient(90deg,#6366f1,#22d3ee);transition:width .35s}
  .sc-bar.done i{background:linear-gradient(90deg,#22c58b,#34d399)}
  .sc-stats{display:flex;gap:14px;flex-wrap:wrap;margin-top:10px;font-size:11.5px;color:var(--sub2)}
  .sc-stats b{font-variant-numeric:tabular-nums;color:var(--text)}
  .sc-stats .good b{color:var(--good)}.sc-stats .bad b{color:var(--bad)}.sc-stats .warn b{color:var(--warn)}
  .sc-ticker{margin-top:10px;display:flex;flex-direction:column;gap:4px;max-height:132px;overflow:hidden}
  .sc-tick{display:flex;align-items:center;gap:8px;font-size:11.5px;padding:5px 8px;border-radius:9px;background:rgba(52,211,153,.07)}
  .sc-tick .mono{direction:ltr;unicode-bidi:isolate}
  .sc-tick em{margin-inline-start:auto;font-style:normal;color:var(--good);font-weight:800}
  .sc-tools{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0 8px;align-items:center}
  .sc-tools select{padding:6px 9px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font:inherit;font-size:11.5px}
  .sc-row{align-items:flex-start!important}
  .sc-tags{display:flex;gap:4px;flex-wrap:wrap;margin-top:3px}
  .sc-tags em{font-style:normal;font-size:9.5px;font-weight:800;padding:1px 7px;border-radius:99px;background:rgba(135,146,168,.14);color:var(--sub);direction:ltr;unicode-bidi:isolate}
  .sc-tags em.good{background:rgba(34,197,139,.14);color:var(--good)}.sc-tags em.warn{background:rgba(245,165,36,.14);color:var(--warn)}.sc-tags em.bad{background:rgba(242,73,85,.14);color:var(--bad)}
  .sc-score{flex:none;min-width:44px;height:44px;border-radius:13px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900;font-size:15px;line-height:1;background:rgba(135,146,168,.14);color:var(--sub)}
  .sc-score small{font-size:9px;margin-top:3px;font-weight:800}
  .sc-score.good{background:rgba(34,197,139,.16);color:var(--good)}.sc-score.warn{background:rgba(245,165,36,.16);color:var(--warn)}.sc-score.bad{background:rgba(242,73,85,.14);color:var(--bad)}
  .ob-sc{display:inline-block;padding:2px 8px;border-radius:99px;font-size:10px;font-weight:800;margin-inline-start:6px}
  `;
  document.head.appendChild(st);
}
ensureScanStyle();
function scEl(id){ return document.getElementById(id); }
function scGradeClass(g){ return (g==='A'||g==='B') ? 'good' : (g==='C' ? 'warn' : 'bad'); }
function scFmtTime(s){ s = Math.round(s||0); return s>=60 ? `${Math.floor(s/60)}m ${s%60}s` : `${s}s`; }
function scSleep(ms){ return new Promise(r=>setTimeout(r,ms)); }
function scReset(){
  const btn = scEl('scanBtn'), cbtn = scEl('scanCancelBtn');
  if(btn){ btn.disabled = false; btn.innerHTML = '<i class="ti ti-radar-2"></i> شروع اسکن'; }
  if(cbtn) cbtn.style.display = 'none';
}
async function runProxyScan(){
  const isUrl = scEl('scanSrcUrlBtn').classList.contains('on');
  const body = isUrl ? {source:'url', url:(scEl('scanUrl').value||'').trim()} : {source:'text', text: scEl('scanText').value||''};
  if(isUrl && !body.url){ toast('آدرس لیست را وارد کن', false); return; }
  if(!isUrl && !body.text.trim()){ toast('لیست پروکسی را پیست کن', false); return; }
  body.protocol = scEl('scanProto').value;
  body.samples = Number(scEl('scanSamples').value) || 3;
  body.tls = scEl('scanTls').checked;
  body.speed = scEl('scanSpeed').checked;
  body.concurrency = Number(scEl('scanConc').value) || 40;
  const wrap = scEl('scanResultsWrap');
  SCAN_RESULTS = []; SCAN_VIEW = []; SCAN_SHOWN = 0;
  if(SCAN_JOB) SCAN_JOB.running = false;
  const btn = scEl('scanBtn');
  btn.disabled = true; btn.innerHTML = '<i class="ti ti-hourglass"></i> در حال شروع...';
  wrap.innerHTML = '';
  try{
    const r = await api('/api/proxies/scan/start', {method:'POST', body: JSON.stringify(body)});
    SCAN_JOB = {id:r.job_id, total:r.total, since:0, running:true, blocked:r.blocked||0, truncated:!!r.truncated};
    btn.innerHTML = '<i class="ti ti-loader-2"></i> در حال اسکن...';
    scEl('scanCancelBtn').style.display = '';
    wrap.innerHTML = `
      <div class="sc-live">
        <div class="sc-head"><b id="scTitle">در حال اسکن ${r.total} پراکسی…</b><span id="scElapsed">0s</span></div>
        <div class="sc-bar" id="scBarWrap"><i id="scBar"></i></div>
        <div class="sc-stats"><span>بررسی‌شده <b id="scDone">0</b>/<b>${r.total}</b></span><span class="good">سالم <b id="scOk">0</b></span><span class="bad">ناموفق <b id="scBad">0</b></span><span class="warn">پرریسک <b id="scRisky">0</b></span></div>
        ${r.blocked?`<div class="hint" style="margin:8px 0 0">${r.blocked} آدرس داخلی/لوکال به‌دلیل امنیت رد شد.</div>`:''}
        ${r.truncated?`<div class="hint" style="margin:8px 0 0">لیست بلندتر از سقف مجاز بود؛ فقط بخش اول بررسی می‌شود.</div>`:''}
        <div class="sc-ticker" id="scTicker"></div>
      </div>
      <div id="scFinal"></div>`;
    pollScan(SCAN_JOB);
  }catch(e){
    wrap.innerHTML = `<div class="ob-note"><span class="nd-err">${escapeHtml(e.message)}</span></div>`;
    scReset();
  }
}
async function pollScan(job){
  try{
    while(job.running){
      if(!scEl('scanResultsWrap')) return;
      const j = await api(`/api/proxies/scan/${job.id}?since=${job.since}`);
      if(!job.running) return;
      job.since = j.next;
      const fresh = [];
      for(const x of j.results){ SCAN_RESULTS[x.i] = x; if(x.ok) fresh.push(x); }
      updateScanLive(j, fresh);
      if(j.state !== 'running'){ job.running = false; finishScan(j); return; }
      await scSleep(document.hidden ? 2500 : 700);
    }
  }catch(e){
    job.running = false;
    const w = scEl('scanResultsWrap');
    if(w) w.insertAdjacentHTML('beforeend', `<div class="ob-note"><span class="nd-err">${escapeHtml(e.message)}</span></div>`);
    scReset();
  }
}
function updateScanLive(j, fresh){
  const pct = j.total ? Math.round(j.done / j.total * 100) : 0;
  const set = (id, v)=>{ const el = scEl(id); if(el) el.textContent = v; };
  const bar = scEl('scBar'); if(bar) bar.style.width = pct + '%';
  set('scDone', j.done); set('scOk', j.working); set('scBad', j.done - j.working); set('scRisky', j.risky);
  set('scElapsed', scFmtTime(j.elapsed));
  const tk = scEl('scTicker');
  if(tk && fresh.length){
    const html = fresh.slice(-5).reverse().map(x=>`<div class="sc-tick">${flagHtml(x)}<span class="mono">${escapeHtml(x.host)}:${x.port}</span><small>${escapeHtml(x.scheme.toUpperCase())}</small><em>${Math.round(x.ping_ms)}ms · ${x.score}</em></div>`).join('');
    tk.innerHTML = html + tk.innerHTML;
    while(tk.children.length > 6) tk.lastElementChild.remove();
  }
}
async function cancelProxyScan(){
  if(!SCAN_JOB) return;
  try{ await api(`/api/proxies/scan/${SCAN_JOB.id}/cancel`, {method:'POST'}); }catch(e){ toast(e.message, false); }
}
function finishScan(j){
  scReset();
  const title = scEl('scTitle'), bw = scEl('scBarWrap'), tk = scEl('scTicker');
  if(title) title.textContent = j.state === 'cancelled' ? `اسکن لغو شد — ${j.working} سالم از ${j.done} بررسی‌شده` : `اسکن تمام شد — ${j.working} سالم از ${j.total}`;
  if(bw) bw.classList.add('done');
  const bar = scEl('scBar'); if(bar && j.state !== 'cancelled') bar.style.width = '100%';
  if(tk) tk.remove();
  renderScanFinal();
}
function scFilteredView(){
  const mode = (scEl('scFilter')||{}).value || 'ok';
  const all = SCAN_RESULTS.filter(Boolean);
  let list = all;
  if(mode === 'ok') list = all.filter(x=>x.ok);
  else if(mode === 'ab') list = all.filter(x=>x.ok && (x.grade==='A'||x.grade==='B'));
  return list.sort((a,b)=> (b.ok - a.ok) || (b.score - a.score) || ((a.ping_ms??1e9) - (b.ping_ms??1e9)));
}
function scanRowHtml(x){
  const tags = [];
  if(x.ok){
    tags.push(`<em>${escapeHtml(x.scheme.toUpperCase())}</em>`);
    if(x.ping_ms != null) tags.push(`<em>${Math.round(x.ping_ms)}ms</em>`);
    if(x.jitter) tags.push(`<em>±${Math.round(x.jitter)}</em>`);
    if(x.loss) tags.push(`<em class="bad">loss ${x.loss}%</em>`);
    if(x.tls_state === 'clean') tags.push('<em class="good">TLS ✓</em>');
    else if(x.tls_state === 'intercepted') tags.push('<em class="bad">TLS رهگیری‌شده ⚠</em>');
    else if(x.tls_state === 'blocked') tags.push('<em class="warn">443 ✗</em>');
    if(x.hosting === true) tags.push('<em>Datacenter</em>');
    if(x.speed_mbps != null) tags.push(`<em>${x.speed_mbps} Mbps</em>`);
  }
  const sub = x.ok ? [x.country, x.city, x.isp].filter(Boolean).map(escapeHtml).join(' · ') || 'کشور نامشخص' : escapeHtml(x.message || 'ناموفق');
  const preset = x.ok && x.status === 'ok' && x.score >= 70;
  return `<label class="ob-row sc-row${preset?' on':''}" style="${x.ok?'':'opacity:.55'}">
      <input type="checkbox" name="scanPick" value="${x.i}" ${preset?'checked':''} ${x.ok?'':'disabled'} onchange="this.closest('.ob-row').classList.toggle('on',this.checked)">
      ${flagHtml(x)}
      <span class="ob-txt"><b class="mono" style="direction:ltr;text-align:left">${escapeHtml(x.host)}:${x.port}${x.has_auth?' 🔑':''}</b><small>${sub}</small><span class="sc-tags">${tags.join('')}</span></span>
      <span class="sc-score ${x.ok?scGradeClass(x.grade):'bad'}" title="امتیاز کیفیت">${x.ok?x.score:'—'}<small>${x.ok?escapeHtml(x.grade):''}</small></span>
    </label>`;
}
function renderScanFinal(){
  const box = scEl('scFinal'); if(!box) return;
  const all = SCAN_RESULTS.filter(Boolean);
  if(!all.length){ box.innerHTML = '<div class="sg-empty">نتیجه‌ای نیست</div>'; return; }
  const good = all.filter(x=>x.ok && (x.grade==='A'||x.grade==='B')).length;
  const keepMode = (scEl('scFilter')||{}).value || 'ok';
  box.innerHTML = `
    <div class="sc-tools">
      <select id="scFilter" onchange="renderScanList()">
        <option value="ok" ${keepMode==='ok'?'selected':''}>فقط سالم‌ها</option>
        <option value="ab" ${keepMode==='ab'?'selected':''}>فقط کیفیت A و B</option>
        <option value="all" ${keepMode==='all'?'selected':''}>همه‌ی نتیجه‌ها</option>
      </select>
      <button class="btn sm" onclick="selectGoodScan()"><i class="ti ti-sparkles"></i> انتخاب A/B</button>
      <button class="btn sm" onclick="toggleAllScanPicks()"><i class="ti ti-checks"></i> همه/هیچ</button>
      <button class="btn sm" onclick="copyScanList()"><i class="ti ti-copy"></i> کپی لیست سالم‌ها</button>
    </div>
    <div class="ob-list sg-picklist" id="scList"></div>
    <div id="scMore" style="margin-top:8px"></div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">
      <button class="btn primary" style="flex:1;min-width:190px" onclick="addScannedProxies()"><i class="ti ti-plus"></i> افزودن انتخاب‌شده‌ها</button>
      <button class="btn" style="flex:1;min-width:190px" onclick="addScannedProxies(true)" ${good?'':'disabled'}><i class="ti ti-rocket"></i> افزودن همه‌ی کیفیت A/B (${good})</button>
    </div>`;
  SCAN_SHOWN = 0;
  renderScanList();
}
function renderScanList(append){
  const list = scEl('scList'); if(!list) return;
  if(!append){ SCAN_VIEW = scFilteredView(); SCAN_SHOWN = 0; list.innerHTML = ''; }
  const next = SCAN_VIEW.slice(SCAN_SHOWN, SCAN_SHOWN + SCAN_PAGE);
  if(next.length) list.insertAdjacentHTML('beforeend', next.map(scanRowHtml).join(''));
  SCAN_SHOWN += next.length;
  if(!SCAN_VIEW.length) list.innerHTML = '<div class="sg-empty">موردی با این فیلتر نیست</div>';
  const left = SCAN_VIEW.length - SCAN_SHOWN;
  const more = scEl('scMore');
  if(more) more.innerHTML = left > 0 ? `<button class="btn sm" style="width:100%" onclick="renderScanList(true)">نمایش ${Math.min(SCAN_PAGE, left)} مورد بعدی (${left} باقی‌مانده)</button>` : '';
}
function toggleAllScanPicks(){
  const boxes = [...document.querySelectorAll('input[name=scanPick]:not(:disabled)')];
  const allChecked = boxes.length > 0 && boxes.every(b=>b.checked);
  boxes.forEach(b=>{ b.checked = !allChecked; b.closest('.ob-row').classList.toggle('on', b.checked); });
}
function selectGoodScan(){
  document.querySelectorAll('input[name=scanPick]:not(:disabled)').forEach(b=>{
    const x = SCAN_RESULTS[Number(b.value)];
    b.checked = !!x && (x.grade==='A' || x.grade==='B') && x.status==='ok';
    b.closest('.ob-row').classList.toggle('on', b.checked);
  });
}
async function addScannedProxies(allGood){
  if(!SCAN_JOB) return;
  let body;
  if(allGood){ body = {min_score:70, limit:200}; }
  else{
    const idxs = [...document.querySelectorAll('input[name=scanPick]:checked')].map(i=>Number(i.value));
    if(!idxs.length){ toast('حداقل یک پراکسی سالم را انتخاب کن', false); return; }
    body = {indexes: idxs};
  }
  try{
    const r = await api(`/api/proxies/scan/${SCAN_JOB.id}/import`, {method:'POST', body: JSON.stringify(body)});
    toast(`${r.added} پراکسی اضافه شد${r.skipped?` (${r.skipped} مورد تکراری رد شد)`:''} ✓`, r.added>0);
    await loadProxies();
  }catch(e){ toast(e.message, false); }
}
async function copyScanList(){
  if(!SCAN_JOB) return;
  try{
    const r = await api(`/api/proxies/scan/${SCAN_JOB.id}/export`, {method:'POST', body: JSON.stringify({min_score:0})});
    const text = (r.lines||[]).join('\n');
    if(!text){ toast('پراکسی سالمی برای کپی نیست', false); return; }
    try{ await navigator.clipboard.writeText(text); }
    catch(_){ const t = document.createElement('textarea'); t.value = text; document.body.appendChild(t); t.select(); document.execCommand('copy'); t.remove(); }
    toast(`${r.count} پراکسی کپی شد ✓`);
  }catch(e){ toast(e.message, false); }
}

// ─────────────── اینباند جدید: پیش‌فرض «یک WS + یک XHTTP در یک اشتراک» ───────────────
function builderModeSwitch(active){
  return `<div class="ob-seg"><button type="button" class="${active==='combo'?'on':''}" onclick="openComboDrawer()"><i class="ti ti-stack-2"></i> WS + XHTTP (یک اشتراک)</button><button type="button" class="${active==='manual'?'on':''}" onclick="openLinkDrawer('',true)"><i class="ti ti-adjustments-horizontal"></i> دستی پیشرفته</button></div>`;
}
async function openComboDrawer(){
  await loadProxies();
  try{ if(!ADMIN_CACHE.length) await loadAdmins(); }catch(e){}
  const q = localStorage.getItem('vw_quick_outbound_proxy') || '';
  const sel = PROXIES_CACHE.some(p=>p.id===q) ? [q] : [''];
  const cats = (typeof CATEGORIES!=='undefined' ? CATEGORIES : []).map(c=>`<option value="${c.id}">${escapeHtml(c.name)}</option>`).join('');
  const fps = (MANUAL_META.fingerprints||['chrome','firefox','safari','ios','android','edge','random']).map(x=>`<option value="${x}" ${x==='chrome'?'selected':''}>${x}</option>`).join('');
  openDrawer('ساخت اینباند', `
    ${builderModeSwitch('combo')}
    <div class="ib-section"><div class="ib-section-body">
      <div class="ib-step"><span class="num"><i class="ti ti-route" style="font-size:13px"></i></span><div><b>خروجی (Outbound)</b><small>مستقیم از Railway یا از پراکسی SOCKS5 — هر تعداد که بخواهی انتخاب کن</small></div></div>
      <div class="ob-picker" data-ob-picker="cbExit" data-multi="1">${outboundPickerHtml('cbExit', true, sel)}</div>
      <div class="ob-note" id="cbSummary"></div>
      <button type="button" class="btn sm" onclick="openOutboundManager()"><i class="ti ti-route"></i> مدیریت / افزودن پراکسی</button>
    </div></div>
    <div class="ib-section"><div class="ib-section-body">
      <div class="ib-step"><span class="num"><i class="ti ti-settings" style="font-size:13px"></i></span><div><b>مشخصات</b><small>برای هر کانفیگ WS و XHTTP جداگانه اعمال می‌شود (حجم، سرعت، محدودیت‌ها)</small></div></div>
      <div class="ib-grid">
        <div class="grp"><label>نام / Remark</label><input id="cbLabel" placeholder="خالی = نام تصادفی"></div>
        <div class="grp"><label>دسته‌بندی</label><select id="cbCategory"><option value="0">بدون دسته</option>${cats}</select></div>
        <div class="grp"><label>Port</label><input id="cbPort" type="number" min="1" max="65535" value="443"></div>
        <div class="grp"><label>Fingerprint</label><select id="cbFingerprint">${fps}</select></div>
        <div class="grp"><label>تعداد کل کانفیگ (WS+XHTTP)</label><input id="cbPairs" type="number" min="2" max="80" step="2" value="2" oninput="updateComboSummary()"><small class="hint">مثلاً 4 یعنی داخل همین اشتراک ۲ تا WS و ۲ تا XHTTP باشد؛ برای هر خروجی جدا اعمال می‌شود.</small></div>
        <div class="grp"><label>حجم (GB)</label><input id="cbLimit" type="number" min="0" placeholder="0 = نامحدود"></div>
        <div class="grp"><label>اعتبار (روز)</label><input id="cbDays" type="number" min="0" placeholder="0 = نامحدود"></div>
        <div class="grp"><label>IP Limit</label><input id="cbIp" type="number" min="0" value="0"></div>
        <div class="grp"><label>Connection Limit</label><input id="cbConn" type="number" min="0" value="0"></div>
        <div class="grp"><label>تعداد کاربر</label><input id="cbClients" type="number" min="0" max="1000" value="0" placeholder="0 = نامحدود"></div>
        <div class="grp"><label>Speed (Mbit/s)</label><input id="cbSpeed" type="number" min="0" placeholder="0 = نامحدود"></div>
        <div class="grp ib-full"><label>یادداشت داخلی</label><input id="cbNote" placeholder="توضیحات اختیاری"></div>
      </div>
    </div></div>
    <div class="ib-section"><div class="ib-section-body">
      <div class="ib-step"><span class="num"><i class="ti ti-user-shield" style="font-size:13px"></i></span><div><b>محدودیت ادمین (اختیاری)</b><small>این اینباند فقط برای یک ادمین مشخص باشد</small></div></div>
      <div class="ib-grid">
        <div class="grp"><label>ادمین</label><select id="cbRestrictAdmin"><option value="">— بدون محدودیت —</option>${(ADMIN_CACHE||[]).filter(x=>x.role!=='owner').map(a=>`<option value=\"${a.id}\">${escapeHtml(a.username)}</option>`).join('')}</select></div>
        <div class="grp"><label>حالت</label><select id="cbRestrictMode"><option value="only">فقط همین اینباند (جایگزین محدودیت قبلی)</option><option value="add">علاوه بر دسترسی‌های فعلی</option></select></div>
      </div>
    </div></div>
  `, `<button class="btn primary" style="flex:1" id="cbSubmit" onclick="submitCombo()"><i class="ti ti-device-floppy"></i>ساخت اشتراک</button>`);
  updateComboSummary();
}
function updateComboSummary(){
  const el = document.getElementById('cbSummary'); if(!el) return;
  const n = readOutboundPicker(document, 'cbExit').length;
  const rawCount = Number($('cbPairs')?.value || 2);
  const pairsPerExit = Math.max(1, Math.ceil(rawCount/2));
  const totalPairs = n * pairsPerExit;
  el.innerHTML = n
    ? `<i class="ti ti-info-circle"></i> ${n} خروجی × ${pairsPerExit*2} کانفیگ → یک اشتراک با <b>${totalPairs} WS + ${totalPairs} XHTTP</b> (${totalPairs*2} کانفیگ)`
    : '⚠️ حداقل یک خروجی انتخاب کن';
}
async function submitCombo(){
  const exits = readOutboundPicker(document, 'cbExit');
  if(!exits.length){ toast('حداقل یک خروجی انتخاب کن', false); return; }
  const port = Number($('cbPort')?.value || 443);
  if(!Number.isInteger(port) || port<1 || port>65535){ toast('پورت باید بین 1 تا 65535 باشد', false); return; }
  const num = id => Math.max(0, Number($(id)?.value || 0));
  const body = {
    label: ($('cbLabel')?.value||'').trim(), category_id: $('cbCategory')?.value || '0', port,
    fingerprint: $('cbFingerprint')?.value || 'chrome',
    limit_value: num('cbLimit'), limit_unit: 'GB', expires_days: num('cbDays'),
    ip_limit: num('cbIp'), connection_limit: num('cbConn'), client_limit: num('cbClients'),
    speed_limit_value: num('cbSpeed'), speed_limit_unit: 'MBIT',
    note: ($('cbNote')?.value||'').trim(), outbound_proxy_ids: exits,
    pairs_count: Math.max(2, Math.ceil(Number($('cbPairs')?.value||2)/2)*2),
    restrict_admin_id: $('cbRestrictAdmin')?.value || '', restrict_mode: $('cbRestrictMode')?.value || 'only'
  };
  const btn = $('cbSubmit'); if(btn) btn.disabled = true;
  try{
    const r = await api('/api/links/combo', {method:'POST', body: JSON.stringify(body)});
    loadLinks();
    showComboResult(r);
  }catch(e){ toast(e.message || 'خطا در ساخت اشتراک', false); if(btn) btn.disabled = false; }
}

// ─────────────── تغییر خروجی: تکی (دکمه‌ی روی کارت) یا گروهی (نوار انتخاب) ───────────────
async function changeOutbound(uuids){
  uuids = (uuids||[]).filter(Boolean);
  if(!uuids.length) return;
  const cur = uuids.length===1 ? ((LINKS.find(x=>x.uuid===uuids[0])||{}).outbound_proxy_id || '') : '';
  const pid = await askOutboundChoice({
    title: uuids.length===1 ? 'خروجی این اینباند' : `خروجی ${uuids.length} اینباند`,
    sub: 'ترافیک از کجا خارج شود؟', current: cur, requireProxies: true,
    note: 'کلاینت‌های زیرمجموعه هم همین خروجی را می‌گیرند. اتصال‌های فعلی از اتصال بعدی روی خروجی جدید می‌روند.'
  });
  if(pid===null) return;
  try{
    const r = await api('/api/links/outbound', {method:'POST', body: JSON.stringify({uuids, outbound_proxy_id: pid})});
    toast(`خروجی ${r.updated} اینباند${r.clients?` و ${r.clients} کلاینت`:''} تنظیم شد ✓`);
    loadLinks();
  }catch(e){ toast(e.message, false); }
}
function bulkOutbound(){ changeOutbound(selectedLinkUuids()); }
// Single source of truth for turning a link's stored fields into
// {base_protocol, network, security}. Both the builder's initial render and
// the edit-drawer's hidden-field sync must agree, or the visible transport
// card and the value that actually gets submitted can diverge (this used to
// happen for links whose `protocol` was a legacy shortcut like "vless-ws":
// the card correctly showed WebSocket, but the hidden #mNetwork field fell
// back to a stale/defaulted "tcp" a moment later).
function deriveManualParts(l){
  l = l || {};
  const proto = l.protocol || 'manual';
  if(proto === 'manual'){
    // Created by the advanced builder: base_protocol/network/security were
    // explicitly written by the backend and are always reliable.
    return {bp: l.base_protocol || 'vless', net: l.network || 'ws', sec: l.security || 'tls'};
  }
  if(proto==='vless-ws') return {bp:'vless',net:'ws',sec:'tls'};
  if(proto==='vless-tcp') return {bp:'vless',net:'tcp',sec:'none'};
  if(proto.startsWith('xhttp-')) return {bp:'vless',net:'xhttp',sec:'tls'};
  if(proto==='vmess-ws') return {bp:'vmess',net:'ws',sec:'tls'};
  if(proto==='trojan-ws') return {bp:'trojan',net:'ws',sec:'tls'};
  return {bp: l.base_protocol || 'vless', net: l.network || 'ws', sec: l.security || 'tls'};
}
function manualBuilderHtml(l){
  l = l || {};
  const parts = deriveManualParts(l);
  let bp = parts.bp, net = parts.net, sec = parts.sec;
  const methods = MANUAL_META.shadowsocks_methods || ['chacha20-ietf-poly1305','aes-128-gcm','aes-256-gcm'];
  const icons = {vless:'ti-bolt',vmess:'ti-brand-vscode',trojan:'ti-shield-lock',shadowsocks:'ti-brand-shield'};
  const bpLabels = {vless:'VLESS',vmess:'VMess',trojan:'Trojan',shadowsocks:'Shadowsocks'};
  const nets = [
    ['tcp','TCP','Raw / direct','ti-arrows-right-left'],
    ['ws','WebSocket','WS over HTTP','ti-world'],
    ['grpc','gRPC','HTTP/2 transport','ti-transfer'],
    ['xhttp','XHTTP','Modern HTTP transport','ti-brand-xamarin']
  ];
  const secs = (MANUAL_META.securities||[]);
  const fpOpts=(MANUAL_META.fingerprints||['chrome','firefox','safari','ios','android','edge','random']).map(x=>`<option value="${x}" ${(l.fingerprint||'chrome')===x?'selected':''}>${x}</option>`).join('');
  const methodOpts=methods.map(x=>`<option value="${x}" ${(l.ss_method||methods[0])===x?'selected':''}>${x}</option>`).join('');
  const conn=Number(l.connection_limit||0), speed=Number(l.speed_limit_bytes||0), speedMbit=speed?Math.max(1,Math.round(speed*8/1000000)):'';
  return `
    <div class="inbound-builder">
      ${l.uuid?'':builderModeSwitch('manual')}
      <div class="ib-hero">
        <div class="ib-title"><div class="ib-icon"><i class="ti ti-adjustments-horizontal"></i></div><div><b>${l.uuid?'ویرایش اینباند':'ساخت اینباند حرفه‌ای'}</b><small>پروتکل پایه، ترنسپورت و امنیت کاملاً تفکیک‌شده</small></div></div>
        <span class="badge gray">INBOUND BUILDER</span>
      </div>

      <div class="ib-section">
        <div class="ib-section-body">
          <div class="ib-step"><span class="num">1</span><div><b>پروتکل پایه</b><small>اول مشخص کن با چه پروتکلی کانفیگ ساخته شود</small></div></div>
          <div id="ibProtocolCards" class="ib-matrix">
            ${Object.entries(bpLabels).map(([id,label])=>`<label class="ib-opt ${bp===id?'on':''}" data-proto-card="${id}"><input type="radio" name="ibBaseProtocol" value="${id}" ${bp===id?'checked':''} onchange="selectBaseProtocol('${id}')"><span class="ib-opt-icon"><i class="ti ${icons[id]||'ti-network'}"></i></span><span><b>${label}</b><small>${id==='vless'?'UUID / XTLS ecosystem':id==='vmess'?'Legacy-compatible':id==='trojan'?'Password-style auth':'AEAD proxy'}</small></span></label>`).join('')}
          </div>
        </div>
      </div>

      <div class="ib-section">
        <div class="ib-section-body">
          <div class="ib-step"><span class="num">2</span><div><b>Transport / Network</b><small>حالا مسیر انتقال را جداگانه انتخاب کن</small></div></div>
          <div id="ibTransportCards" class="ib-matrix">
            ${nets.map(([id,label,sub,icon])=>`<label class="ib-opt ${net===id?'on':''}" data-net-card="${id}"><input type="radio" name="ibNetwork" value="${id}" ${net===id?'checked':''} onchange="selectTransport('${id}')"><span class="ib-opt-icon"><i class="ti ${icon}"></i></span><span><b>${label}</b><small>${sub}</small></span></label>`).join('')}
          </div>
          <div id="ibTransportNote" class="ib-status" style="margin-top:10px"></div>
        </div>
      </div>

      <div class="ib-section">
        <div class="ib-section-body">
          <div class="ib-step"><span class="num">3</span><div><b>Security</b><small>TLS / Reality / None را مستقل از ترنسپورت انتخاب کن</small></div></div>
          <div id="ibSecurityCards" class="ib-matrix">
            ${secs.map(x=>`<label class="ib-opt ${sec===x.id?'on':''}" data-sec-card="${x.id}"><input type="radio" name="ibSecurity" value="${x.id}" ${sec===x.id?'checked':''} onchange="selectSecurity('${x.id}')"><span class="ib-opt-icon"><i class="ti ${x.id==='reality'?'ti-key':x.id==='tls'?'ti-lock':'ti-lock-open'}"></i></span><span><b>${x.label}</b><small>${x.id==='reality'?'Reality public-key mode':x.id==='tls'?'Standard TLS':'No TLS wrapper'}</small></span></label>`).join('')}
          </div>
          <div id="mLiveHint" class="ib-status" style="margin-top:10px"></div>
        </div>
      </div>

      <div class="ib-section">
        <div class="ib-section-head"><div><b>4. Endpoint & Advanced Parameters</b><small>فقط فیلدهای مرتبط با انتخاب بالا نمایش داده می‌شوند</small></div><i class="ti ti-server-2"></i></div>
        <div class="ib-section-body">
          <div class="ib-grid">
            <div class="grp"><label>نام / Remark</label><input id="fLabel" value="${escapeHtml(l.label||'')}" placeholder="مثلاً: VIP-01"></div>
            <div class="grp"><label>دسته‌بندی</label><select id="fCategory"><option value="0">بدون دسته</option>${CATEGORIES.map(c=>`<option value="${c.id}" ${String(l.category_id)===String(c.id)?'selected':''}>${escapeHtml(c.name)}</option>`).join('')}</select></div>
            <div class="grp"><label>آدرس / Domain</label><div class="endpoint-input"><input id="mAddress" placeholder="example.com" value="${escapeHtml(l.address||'')}" oninput="updateBuilderSummary()"><button type="button" class="btn endpoint-btn" onclick="loadRailwayEndpoint()"><i class="ti ti-cloud"></i>Railway</button></div></div>
            <div class="grp"><label>Port</label><div class="endpoint-input"><input id="mPort" type="number" min="1" max="65535" value="${l.port||443}" oninput="updateBuilderSummary()"><button type="button" class="btn endpoint-btn" onclick="testCurrentTcp()"><i class="ti ti-activity"></i>Ping</button></div></div>
            <div class="grp"><label>Fingerprint</label><select id="mFingerprint">${fpOpts}</select></div>
            <div class="grp"><label>ALPN</label><input id="mAlpn" value="${escapeHtml(l.alpn||'')}" placeholder="h2,http/1.1"></div>
            <div class="grp ib-full"><label>مسیر خروجی (Outbound) — مستقیم یا پراکسی؟</label><select id="mOutboundProxy" data-outbound-proxy-select><option value="">🚀 مستقیم (Railway)</option></select><div class="hint">اگه یک پراکسی انتخاب کنی، اتصال به مقصد از طریق همون SOCKS5 رد می‌شه (روی کشور اون پراکسی ظاهر می‌شه). از تب «تنظیمات» پراکسی اضافه/تست کن.</div></div>
            <div id="mWsXhttpWrap" class="ib-grid ib-full">
              <div class="grp"><label>Path</label><input id="mPath" placeholder="خالی = مسیر خودکار سرور (پیشنهادی)" value="${escapeHtml(l.path||'')}"></div>
              <div class="grp"><label>Host Header</label><input id="mHost" placeholder="domain.com" value="${escapeHtml(l.host_header||'')}"></div>
            </div>
            <div id="mXhttpModeWrap" class="grp ib-full"><label>XHTTP Mode</label><select id="mXhttpMode">${(MANUAL_META.xhttp_modes||['auto','packet-up','stream-up','stream-one']).map(x=>`<option value="${x}" ${(l.xhttp_mode||'auto')===x?'selected':''}>${x}</option>`).join('')}</select></div>
            <div id="mGrpcWrap" class="ib-grid ib-full"><div class="grp"><label>Service Name</label><input id="mGrpcService" placeholder="service" value="${escapeHtml(l.grpc_service_name||'')}"></div><div class="grp"><label>gRPC Mode</label><select id="mGrpcMode"><option value="gun" ${(l.grpc_mode||'gun')==='gun'?'selected':''}>gun</option><option value="multi" ${l.grpc_mode==='multi'?'selected':''}>multi</option></select></div></div>
            <div id="mTcpWrap" class="ib-grid ib-full"><div class="grp"><label>Header Type</label><select id="mHeaderType"><option value="" ${!l.header_type?'selected':''}>none</option><option value="http" ${l.header_type==='http'?'selected':''}>http</option></select></div><div class="grp"><label>Flow</label><select id="mFlow"><option value="" ${!l.flow?'selected':''}>—</option><option value="xtls-rprx-vision" ${l.flow==='xtls-rprx-vision'?'selected':''}>xtls-rprx-vision</option></select></div></div>
            <div id="mTlsWrap" class="ib-grid ib-full"><div class="grp"><label>SNI</label><input id="mSni" value="${escapeHtml(l.sni||'')}" placeholder="example.com"></div><label class="chk" style="align-self:end;margin-bottom:16px"><input id="mAllowInsecure" type="checkbox" ${l.allow_insecure?'checked':''}> Allow Insecure</label></div>
            <div id="mRealityWrap" class="ib-grid ib-full"><div class="grp"><label>Reality SNI</label><input id="mRealitySni" value="${escapeHtml(l.sni||'')}" placeholder="www.example.com"></div><div class="grp"><label>Public Key</label><input id="mRealityPbk" value="${escapeHtml(l.reality_public_key||'')}" placeholder="public key"></div><div class="grp"><label>Short ID</label><input id="mRealitySid" value="${escapeHtml(l.reality_short_id||'')}" placeholder="short id"></div><div class="grp"><label>Spider X</label><input id="mRealitySpx" value="${escapeHtml(l.reality_spider_x||'/')}" placeholder="/"></div><div class="ib-full"><button type="button" class="btn" onclick="generateRealityKeys()"><i class="ti ti-key"></i>Generate Reality Keypair</button></div></div>
            <div id="mShadowWrap" class="ib-grid ib-full"><div class="grp"><label>Encryption Method</label><select id="mSsMethod">${methodOpts}</select></div><div class="grp"><label>Password</label><input id="mSsPassword" type="password" value="${escapeHtml(l.ss_password||'')}" placeholder="Password / secret"></div></div>
            <div class="grp"><label>حجم (GB)</label><input id="fLimitVal" type="number" min="0" value="${l.limit_bytes?Math.round(l.limit_bytes/1073741824):''}"></div>
            <div class="grp"><label>اعتبار (روز)</label><input id="fDays" type="number" min="0" value="${l.expires_at?Math.max(0,Math.ceil((new Date(l.expires_at).getTime()-Date.now())/86400000)):''}"></div>
            <div class="grp"><label>زمان دقیق انقضا</label><input id="fExpiresAt" type="datetime-local" value="${l.expires_at?new Date(l.expires_at).toISOString().slice(0,16):''}"></div>
            <div class="grp"><label>IP Limit</label><input id="fIpLimit" type="number" min="0" value="${l.ip_limit||0}"></div>
            <div class="grp"><label>Connection Limit</label><input id="fConnLimit" type="number" min="0" value="${conn}"></div>
            <div class="grp"><label>تعداد کاربر</label><input id="fClientLimit" type="number" min="0" max="1000" value="${l.client_limit||0}" placeholder="0 = نامحدود"></div>
            <div class="grp"><label>تعداد خروجی</label><input id="fConfigCount" type="number" min="1" max="40" value="${l.config_count||1}"></div>
            <div class="grp"><label>Speed (Mbit/s)</label><input id="fSpeed" type="number" min="0" value="${speedMbit}" placeholder="0 = نامحدود"></div>
            <div class="grp ib-full"><label>یادداشت داخلی</label><input id="fNote" value="${escapeHtml(l.note||'')}" placeholder="توضیحات اختیاری"></div>
          </div>
        </div>
      </div>

      <div class="ib-section">
        <div class="ib-section-body"><div class="ib-step"><span class="num">5</span><div><b>Summary</b><small>قبل از ذخیره ترکیب نهایی را بررسی کن</small></div></div>
          <div class="ib-summary"><div class="sum"><small>PROTOCOL</small><b id="sumProtocol">${bp.toUpperCase()}</b></div><div class="sum"><small>NETWORK</small><b id="sumNetwork">${net.toUpperCase()}</b></div><div class="sum"><small>SECURITY</small><b id="sumSecurity">${sec.toUpperCase()}</b></div><div class="sum"><small>PORT</small><b id="sumPort">${l.port||443}</b></div><div class="sum"><small>TRAFFIC</small><b id="sumTraffic">—</b></div><div class="sum"><small>LIMITS</small><b id="sumLimits">—</b></div></div>
        </div>
      </div>
    </div>`;
}

function refreshInboundCards(){
  const bp=$('mBase')?.value || document.querySelector('input[name="ibBaseProtocol"]:checked')?.value || 'vless';
  const net=$('mNetwork')?.value || document.querySelector('input[name="ibNetwork"]:checked')?.value || 'ws';
  const sec=$('mSecurity')?.value || document.querySelector('input[name="ibSecurity"]:checked')?.value || 'tls';
  document.querySelectorAll('[data-proto-card]').forEach(e=>e.classList.toggle('on',e.dataset.protoCard===bp));
  document.querySelectorAll('[data-net-card]').forEach(e=>e.classList.toggle('on',e.dataset.netCard===net));
  document.querySelectorAll('[data-sec-card]').forEach(e=>e.classList.toggle('on',e.dataset.secCard===sec));
}
function selectBaseProtocol(id){
  let hidden=document.getElementById('mBase'); if(!hidden){hidden=document.createElement('input');hidden.type='hidden';hidden.id='mBase';document.body.appendChild(hidden)} hidden.value=id;
  const ss=id==='shadowsocks';
  const secWrap=document.getElementById('ibSecurityCards');
  if(secWrap){document.querySelectorAll('[data-sec-card]').forEach(e=>{const sid=e.dataset.secCard; e.classList.toggle('off',ss && sid!=='none'); const inp=e.querySelector('input'); if(inp) inp.disabled=ss&&sid!=='none';}); if(ss){selectSecurity('none');}}
  if(ss && document.querySelector('input[name="ibNetwork"]:checked')?.value!=='tcp') selectTransport('tcp');
  document.getElementById('mShadowWrap')?.style.setProperty('display',ss?'':'none');
  refreshInboundCards(); onManualChange(); updateBuilderSummary();
}
function selectTransport(id){
  let hidden=document.getElementById('mNetwork'); if(!hidden){hidden=document.createElement('input');hidden.type='hidden';hidden.id='mNetwork';document.body.appendChild(hidden)} hidden.value=id;
  const ss=document.getElementById('mBase')?.value==='shadowsocks';
  if(ss && id!=='tcp'){toast('Shadowsocks در این سازنده فقط با TCP پشتیبانی می‌شود',false);hidden.value='tcp';return selectTransport('tcp');}
  refreshInboundCards(); onManualChange(); updateBuilderSummary();
}
function selectSecurity(id){
  let hidden=document.getElementById('mSecurity'); if(!hidden){hidden=document.createElement('input');hidden.type='hidden';hidden.id='mSecurity';document.body.appendChild(hidden)} hidden.value=id;
  refreshInboundCards(); onManualChange(); updateBuilderSummary();
}

function updateBuilderSummary(){
  const val=id=>$(id)?.value || '—'; const set=(id,v)=>{const e=$(id);if(e)e.textContent=v};
  set('sumProtocol',(val('mBase')||'vless').toUpperCase()); set('sumNetwork',(val('mNetwork')||'tcp').toUpperCase()); set('sumSecurity',(val('mSecurity')||'none').toUpperCase()); set('sumPort',val('mPort'));
  const traffic=Number(val('fLimitVal'))||0; set('sumTraffic',traffic?`${traffic} GB`:'نامحدود');
  const ip=Number(val('fIpLimit'))||0, conn=Number(val('fConnLimit'))||0; set('sumLimits',`IP ${ip||'∞'} / CONN ${conn||'∞'}`);
}
function onManualChange(){
  const base=$('mBase')?.value || 'vless', net=$('mNetwork')?.value || 'ws', sec=$('mSecurity')?.value || 'tls';
  const show=(id,yes)=>{const e=$(id);if(e)e.style.display=yes?'':'none'};
  show('mWsXhttpWrap',net==='ws'||net==='xhttp'); show('mXhttpModeWrap',net==='xhttp'); show('mGrpcWrap',net==='grpc'); show('mTcpWrap',net==='tcp'); show('mTlsWrap',sec==='tls'); show('mRealityWrap',sec==='reality'); show('mShadowWrap',base==='shadowsocks');
  if(base==='shadowsocks'){ if($('mNetwork') && $('mNetwork').value!=='tcp') $('mNetwork').value='tcp'; if($('mSecurity')) $('mSecurity').value='none'; }
  const hint=$('mLiveHint');
  if(hint){
    const live=base!=='shadowsocks' && (MANUAL_META.live_combos||[]).some(c=>c[0]===net&&c[1]===sec) && !(net==='xhttp'&&($('mXhttpMode')?.value||'auto')==='stream-one');
    hint.className='ib-status '+(live?'ok':'warn'); hint.innerHTML=live?'<i class="ti ti-circle-check"></i> این ترکیب آماده استفاده است.':'<i class="ti ti-alert-triangle"></i> این ترکیب برای ساخت لینک و مدیریت سرویس آماده شده است.';
  }
  const tn=$('ibTransportNote');
  if(tn){tn.innerHTML=base==='shadowsocks'?'<i class="ti ti-info-circle"></i> Shadowsocks به‌صورت TCP-only در این Builder ارائه می‌شود.':'<i class="ti ti-adjustments-horizontal"></i> Transport فقط مسیر انتقال است و جدا از پروتکل پایه انتخاب می‌شود.';}
  refreshInboundCards(); updateBuilderSummary();
}

async function testCurrentTcp(){
  const host=($('mAddress')?.value||'').trim();
  const port=Number($('mPort')?.value||0);
  if(!host){toast('ابتدا آدرس یا دامنه را وارد کنید',false);return}
  if(!Number.isInteger(port)||port<1||port>65535){toast('پورت نامعتبر است',false);return}
  const btn=document.querySelector('.endpoint-btn[onclick="testCurrentTcp()"]');
  if(btn){btn.disabled=true;btn.innerHTML='<i class="ti ti-loader-2 spin"></i> در حال تست'}
  try{
    const r=await api('/api/network/tcp-ping',{method:'POST',body:JSON.stringify({host,port,timeout:4})});
    if(r.ok) toast(`TCP OK • ${r.latency_ms}ms • ${host}:${port}`);
    else toast(r.message||'اتصال برقرار نشد',false);
  }catch(e){toast(e.message||'خطا در تست TCP',false)}
  finally{if(btn){btn.disabled=false;btn.innerHTML='<i class="ti ti-activity"></i> تست پینگ'}}
}

async function loadRailwayEndpoint(){
  try{
    const r=await api('/api/network/railway');
    if(!r.is_railway && !r.tcp_proxy_domain){toast('اطلاعات TCP Proxy ریل‌وی در این سرویس پیدا نشد',false);return}
    if(r.tcp_proxy_domain){$('mAddress').value=r.tcp_proxy_domain; if(r.tcp_proxy_port) $('mPort').value=r.tcp_proxy_port; updateBuilderSummary(); toast(`Railway TCP Proxy: ${r.tcp_proxy_domain}:${r.tcp_proxy_port||'?'}`)}
    else if(r.public_domain){$('mAddress').value=r.public_domain; updateBuilderSummary(); toast('دامنه عمومی Railway وارد شد؛ برای TCP خام باید TCP Proxy فعال باشد')}
  }catch(e){toast(e.message||'خطا در دریافت اطلاعات Railway',false)}
}

async function generateRealityKeys(){
  try{ const r=await api('/api/reality-keypair'); $('mRealityPbk').value=r.public_key; $('mRealitySid').value=r.short_id; toast('کلید Reality ساخته شد. Private Key را روی نود خودتان نگه دارید.'); }
  catch(e){ toast(e.message, false); }
}

function onProtocolModeChange(){
  // Kept for compatibility with older inline handlers; the new builder is always advanced.
  const wrap=$('manualBuilderWrap'); if(wrap) wrap.style.display='block'; const quick=$('quickFieldsWrap'); if(quick) quick.style.display='none';
}
function openLinkDrawer(uid, manual){
  if(!uid && !manual){ openComboDrawer(); return; }   // اینباند جدید: پیش‌فرض یک WS + یک XHTTP
  const editing=!!uid, l=editing?(LINKS.find(x=>x.uuid===uid)||{}):{};
  openDrawer(editing?'ویرایش اینباند':'ساخت اینباند', `${manualBuilderHtml(l)}`,
    `${editing?`<button class="btn danger" onclick="deleteLink('${uid}');closeDrawer()"><i class="ti ti-trash"></i>حذف</button>`:''}<button class="btn primary" style="flex:1" onclick="submitLink('${uid||''}')"><i class="ti ti-device-floppy"></i>${editing?'ذخیره تغییرات':'ساخت اینباند'}</button>`);
  setTimeout(()=>{
    let bp=document.getElementById('mBase'); if(!bp){bp=document.createElement('input');bp.type='hidden';bp.id='mBase';document.querySelector('.drawer .dr-body')?.appendChild(bp)}
    let net=document.getElementById('mNetwork'); if(!net){net=document.createElement('input');net.type='hidden';net.id='mNetwork';document.querySelector('.drawer .dr-body')?.appendChild(net)}
    let sec=document.getElementById('mSecurity'); if(!sec){sec=document.createElement('input');sec.type='hidden';sec.id='mSecurity';document.querySelector('.drawer .dr-body')?.appendChild(sec)}
    let proto=l.protocol||'manual'; const parts=deriveManualParts(l);
    bp.value=parts.bp;
    net.value=parts.net;
    sec.value=parts.sec;
    if(bp.value==='shadowsocks'){net.value='tcp';sec.value='none'}
    renderOutboundProxySelects();
    const opx=document.getElementById('mOutboundProxy'); if(opx) opx.value = l.outbound_proxy_id || '';
    loadProxies().then(()=>{ const o=document.getElementById('mOutboundProxy'); if(o) o.value = l.outbound_proxy_id || ''; });
    refreshInboundCards(); onManualChange(); updateBuilderSummary();
  },0);
}

async function submitLink(uid){
  const base=$('mBase')?.value || 'vless', net=$('mNetwork')?.value || 'ws', sec=$('mSecurity')?.value || 'tls';
  const port=Number($('mPort')?.value||443);
  if(!Number.isInteger(port)||port<1||port>65535){toast('پورت باید بین 1 تا 65535 باشد',false);return}
  if(base==='shadowsocks' && net!=='tcp'){toast('Shadowsocks فقط با TCP ساخته می‌شود',false);return}
  const num=id=>Math.max(0,Number($(id)?.value||0));
  const body={label:($('fLabel')?.value||'').trim(),protocol:'manual',category_id:$('fCategory')?.value||'0',limit_value:num('fLimitVal'),limit_unit:'GB',expires_days:num('fDays'),expires_at:$('fExpiresAt')?.value||'',ip_limit:num('fIpLimit'),connection_limit:num('fConnLimit'),client_limit:num('fClientLimit'),config_count:Math.max(1,Math.min(40,num('fConfigCount')||1)),speed_limit_value:num('fSpeed'),speed_limit_unit:'MBIT',note:($('fNote')?.value||'').trim(),port,fingerprint:$('mFingerprint')?.value||'chrome',alpn:$('mAlpn')?.value||'',outbound_proxy_id:$('mOutboundProxy')?.value||''};
  body.manual={base_protocol:base,network:net,security:base==='shadowsocks'?'none':sec,address:$('mAddress')?.value||'',path:$('mPath')?.value||'',host_header:$('mHost')?.value||'',sni:sec==='reality'?($('mRealitySni')?.value||''):($('mSni')?.value||''),alpn:$('mAlpn')?.value||'',flow:$('mFlow')?.value||'',grpc_service_name:$('mGrpcService')?.value||'',grpc_mode:$('mGrpcMode')?.value||'gun',xhttp_mode:$('mXhttpMode')?.value||'auto',header_type:$('mHeaderType')?.value||'',allow_insecure:!!$('mAllowInsecure')?.checked,reality_public_key:$('mRealityPbk')?.value||'',reality_short_id:$('mRealitySid')?.value||'',reality_spider_x:$('mRealitySpx')?.value||'/',ss_method:$('mSsMethod')?.value||'chacha20-ietf-poly1305',ss_password:$('mSsPassword')?.value||''};
  try{if(uid) await api(`/api/links/${uid}`,{method:'PATCH',body:JSON.stringify(body)});else await api('/api/links',{method:'POST',body:JSON.stringify(body)});toast(uid?'اینباند بروزرسانی شد':'اینباند با موفقیت ساخته شد');closeDrawer();loadLinks();}
  catch(e){toast(e.message||'خطا در ذخیره اینباند',false)}
}

// ============================================================
// CATEGORIES
// ============================================================
async function loadCategories(){
  try{
    const res = await api('/api/categories');
    CATEGORIES = res.categories||[];
    $('catsBody').innerHTML = CATEGORIES.map(c=>`
      <tr><td>${escapeHtml(c.name)}</td><td>${c.limit_bytes?fmtBytes(c.limit_bytes):'نامحدود'}</td>
      <td>${c.expires_days||'—'}</td><td>${c.ip_limit||'—'}</td>
      <td><div class="row-actions">
        <button class="iconbtn" onclick="openCategoryDrawer('${c.id}')"><i class="ti ti-pencil"></i></button>
        ${['0','1'].includes(String(c.id))?'':`<button class="iconbtn" onclick="deleteCategory('${c.id}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button>`}
      </div></td></tr>
    `).join('') || `<tr><td colspan="5" class="empty">دسته‌بندی‌ای وجود ندارد</td></tr>`;
  }catch(e){ toast(e.message, false); }
}
function openCategoryDrawer(cid){
  const editing = !!cid;
  const c = editing ? CATEGORIES.find(x=>String(x.id)===String(cid)) : {};
  openDrawer(editing?'ویرایش دسته':'دسته جدید', `
    <div class="grp"><label>نام</label><input id="cName" value="${escapeHtml(c.name||'')}"></div>
    <div class="row2">
      <div class="grp"><label>حجم پیش‌فرض (GB)</label><input id="cLimit" type="number" min="0" value="${c.limit_bytes?Math.round(c.limit_bytes/1073741824):''}"></div>
      <div class="grp"><label>انقضا (روز)</label><input id="cDays" type="number" min="0" value="${c.expires_days||''}"></div>
    </div>
    <div class="grp"><label>محدودیت IP</label><input id="cIp" type="number" min="0" value="${c.ip_limit||''}"></div>
  `, `<button class="btn primary" style="flex:1" onclick="submitCategory('${cid||''}')"><i class="ti ti-device-floppy"></i>ذخیره</button>`);
}
async function submitCategory(cid){
  const body = {name:$('cName').value, limit_value:$('cLimit').value||0, limit_unit:'GB', expires_days:$('cDays').value||0, ip_limit:$('cIp').value||0};
  try{
    if(cid){ await api(`/api/categories/${cid}`, {method:'PATCH', body:JSON.stringify(body)}); }
    else{ await api('/api/categories', {method:'POST', body:JSON.stringify(body)}); }
    toast('ذخیره شد'); closeDrawer(); loadCategories();
  }catch(e){ toast(e.message, false); }
}
async function deleteCategory(cid){
  if(!confirm(t('این دسته حذف شود؟'))) return;
  try{ await api(`/api/categories/${cid}`, {method:'DELETE'}); toast('حذف شد'); loadCategories(); }
  catch(e){ toast(e.message, false); }
}

// ============================================================
// SUB GROUPS
// ============================================================
// ============================================================
// SUB GROUPS  ·  اعضای محلی + اعضای «نود» (دقیقاً مثل Nodes در پنل سنایی:
// یک اینباند این پنل + یک اینباند روی یک پنل دیگر، هر دو در یک اشتراک)
// ============================================================
let SUBS_CACHE = [];
async function loadSubGroups(){
  try{
    const res = await api('/api/subs');
    SUBS_CACHE = res.subs || [];
    $('nb-subs').textContent = SUBS_CACHE.length;
    $('subsBody').innerHTML = SUBS_CACHE.map(s=>{
      const parts = [`${s.local_count||0} محلی`]; if(s.remote_count) parts.push(`${s.remote_count} از نود`);
      return `<tr><td>${escapeHtml(s.name||'—')}</td><td>${parts.join(' + ')}</td>
      <td class="mono">${escapeHtml(s.sub_url||'')}</td>
      <td><div class="row-actions">
        <button class="iconbtn" title="اعضا" onclick="openSubMembersDrawer('${s.sub_id}')"><i class="ti ti-stack-2"></i></button>
        <button class="iconbtn" onclick="deleteSubGroup('${s.sub_id}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button>
      </div></td></tr>`;
    }).join('') || `<tr><td colspan="4" class="empty">گروهی وجود ندارد</td></tr>`;
  }catch(e){ $('subsBody').innerHTML = `<tr><td colspan="4" class="empty">در دسترس نیست</td></tr>`; }
}
function openSubGroupDrawer(){
  openDrawer('گروه ساب جدید', `<div class="grp"><label>نام گروه</label><input id="sgName" placeholder="مثلاً: بسته-VIP"></div>
  <p class="hint">بعد از ساخت گروه، از دکمه‌ی «اعضا» می‌توانی اینباندهای این پنل و نودهای دیگر را داخلش بگذاری.</p>`,
  `<button class="btn primary" style="flex:1" onclick="submitSubGroup()"><i class="ti ti-device-floppy"></i>ساخت</button>`);
}
async function submitSubGroup(){
  try{ const r = await api('/api/subs', {method:'POST', body: JSON.stringify({name: $('sgName').value})}); toast('ساخته شد'); closeDrawer(); await loadSubGroups(); openSubMembersDrawer(r.sub_id); }
  catch(e){ toast(e.message, false); }
}
async function deleteSubGroup(id){
  if(!confirm(t('این گروه حذف شود؟'))) return;
  try{ await api(`/api/subs/${id}`, {method:'DELETE'}); toast('حذف شد'); loadSubGroups(); }
  catch(e){ toast(e.message, false); }
}

function sgStyle(){
  if(document.getElementById('sgStyle')) return;
  const st = document.createElement('style'); st.id = 'sgStyle';
  st.textContent = `
  .sg-sec{margin-bottom:16px}
  .sg-sec-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
  .sg-sec-head b{font-size:12.5px;color:var(--sub)}
  .sg-empty{padding:14px;text-align:center;color:var(--sub2);font-size:12px;border:1px dashed var(--line2);border-radius:12px}
  .sg-row{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:var(--panel2);margin-bottom:7px}
  .sg-row .sg-txt{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
  .sg-row .sg-txt b{font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .sg-row .sg-txt small{font-size:11px;color:var(--sub)}
  .sg-picklist{max-height:220px;overflow:auto;display:flex;flex-direction:column;gap:7px;margin:8px 0}
  `;
  document.head.appendChild(st);
}
sgStyle();

async function openSubMembersDrawer(subId){
  ensureObStyle(); sgStyle();
  let sub = SUBS_CACHE.find(s=>s.sub_id===subId);
  if(!sub){ await loadSubGroups(); sub = SUBS_CACHE.find(s=>s.sub_id===subId); }
  if(!sub){ toast('گروه پیدا نشد', false); return; }
  openDrawer(`اعضای «${escapeHtml(sub.name||'')}»`, subMembersBodyHtml(sub),
    `<button class="btn" style="flex:1" onclick="copyText('${escapeHtml(sub.sub_url||'')}','لینک اشتراک کپی شد ✓')"><i class="ti ti-copy"></i>کپی لینک اشتراک</button>`);
}
function subMembersBodyHtml(sub){
  const localIds = sub.link_ids || [];
  const localLinks = localIds.map(uid => (typeof LINKS!=='undefined' ? LINKS.find(x=>x.uuid===uid) : null));
  const isCombo = localLinks.some(l => l && l.combo_group_id === sub.sub_id);
  const usedExits = new Set(localLinks.filter(l => l && l.combo_group_id === sub.sub_id).map(l => l.outbound_proxy_id || ''));
  const localRows = localIds.map((uid,i)=>{
    const l = localLinks[i];
    const obTag = l && l.combo_group_id===sub.sub_id ? (l.outbound ? `${flagHtml(l.outbound)} ${escapeHtml(l.outbound.country||l.outbound.name||'')}` : '<span class="ob-emoji">🚀</span> مستقیم') : '';
    return `<div class="sg-row">${obTag?`<span style="flex:none">${obTag}</span>`:''}<div class="sg-txt"><b>${escapeHtml(l?l.label:uid)}</b><small>${l?escapeHtml(protoLabel(l))+' · این پنل':'این پنل'}</small></div>
      <button class="btn sm danger" onclick="removeLocalSubMember('${sub.sub_id}','${uid}')"><i class="ti ti-x"></i></button></div>`;
  }).join('') || '<div class="sg-empty">هنوز اینباندی از این پنل اضافه نشده</div>';
  const remoteRows = (sub.remote_links||[]).map(e=>`
    <div class="sg-row"><span class="nd-dot ${e.node_missing?'':(e.active?'on':'off')}"></span><div class="sg-txt">
      <b>${escapeHtml(e.label||e.uuid)}</b><small>${escapeHtml(e.protocol_display||'')} · نود «${escapeHtml(e.node_name||'')}»${e.last_error?` · <span class="nd-err">${escapeHtml(e.last_error)}</span>`:''}</small></div>
      <button class="btn sm danger" onclick="removeRemoteSubMember('${sub.sub_id}','${e.id}')"><i class="ti ti-x"></i></button></div>`).join('')
    || '<div class="sg-empty">هنوز اینباندی از نود دیگر وصل نشده</div>';
  const comboSec = isCombo ? `
    <div class="sg-sec"><div class="sg-sec-head"><b><i class="ti ti-route"></i> خروجی‌های این اشتراک (WS+XHTTP)</b>
      <button class="btn sm" onclick="openAddComboExits('${sub.sub_id}')"><i class="ti ti-plus"></i> افزودن خروجی</button></div>
      <p class="hint" style="margin:0 0 8px">هر پروکسی که تیک بزنی — یا «مستقیم» — یک WS و یک XHTTP تازه با همون تنظیمات به همین اشتراک اضافه می‌شود.</p>
    </div>` : '';
  return `
    ${comboSec}
    <div class="sg-sec"><div class="sg-sec-head"><b>اینباندهای این پنل (${localIds.length})</b><button class="btn sm" onclick="openAddLocalMember('${sub.sub_id}')"><i class="ti ti-plus"></i> افزودن</button></div>${localRows}</div>
    <div class="sg-sec"><div class="sg-sec-head"><b>اینباندهای روی نودهای دیگر (${(sub.remote_links||[]).length})</b><div style="display:flex;gap:6px">
      <button class="btn sm" onclick="refreshRemoteSubMembers('${sub.sub_id}')" title="بروزرسانی از نود"><i class="ti ti-refresh"></i></button>
      <button class="btn sm" onclick="openAddRemoteMember('${sub.sub_id}')"><i class="ti ti-plus"></i> افزودن از نود</button>
    </div></div>${remoteRows}</div>
    <p class="hint">این دقیقاً همان قابلیت «Nodes» است: یک اینباند اینجا + یک اینباند روی یک پنل دیگر، هر دو در یک لینک اشتراک.</p>`;
}
async function reopenSubMembers(subId){ await loadSubGroups(); openSubMembersDrawer(subId); }

// ── افزودن خروجی (پروکسی/مستقیم) به یک اشتراک WS+XHTTP از قبل موجود ──
async function openAddComboExits(subId){
  await loadProxies();
  const sub = SUBS_CACHE.find(s=>s.sub_id===subId);
  const usedExits = new Set((sub?.link_ids||[])
    .map(uid => (typeof LINKS!=='undefined' ? LINKS.find(x=>x.uuid===uid) : null))
    .filter(l => l && l.combo_group_id === subId)
    .map(l => l.outbound_proxy_id || ''));
  const items = [{id:'', direct:true}, ...PROXIES_CACHE].filter(x=>!usedExits.has(x.id));
  if(!items.length){ toast('همه‌ی خروجی‌های موجود قبلاً روی این اشتراک هستند', false); return; }
  const rows = items.map(x=>{
    if(x.direct) return `<label class="ob-row"><input type="checkbox" name="cbAddExit" value=""><span class="ob-emoji">🚀</span><span class="ob-txt"><b>مستقیم (خود Railway)</b><small>ترافیک از IP سرور Railway خارج می‌شود</small></span></label>`;
    return `<label class="ob-row"><input type="checkbox" name="cbAddExit" value="${escapeHtml(x.id)}">${flagHtml(x)}<span class="ob-txt"><b>${escapeHtml(x.name)}</b><small>${x.country?escapeHtml(x.country):'کشور نامشخص'}</small></span><span class="ob-badge ${pingClass(x)}">${pingText(x)}</span></label>`;
  }).join('');
  openDrawer('افزودن خروجی به این اشتراک', `<p class="hint" style="margin-top:0">هرچقدر پروکسی می‌خواهی تیک بزن؛ اگر «مستقیم» را هم بخواهی علاوه بر پروکسی‌ها، همان بالا را هم تیک بزن.</p><div class="ob-list ob-picker sg-picklist">${rows}</div>`,
    `<button class="btn primary" style="flex:1" id="addExitBtn" onclick="submitAddComboExits('${subId}')"><i class="ti ti-plus"></i>افزودن</button>`);
}
async function submitAddComboExits(subId){
  const ids = [...document.querySelectorAll('input[name=cbAddExit]:checked')].map(i=>i.value);
  if(!ids.length){ toast('حداقل یک خروجی تیک بزن', false); return; }
  try{
    const r = await api(`/api/subs/${subId}/combo-exits`, {method:'POST', body: JSON.stringify({outbound_proxy_ids: ids})});
    toast(r.added ? `${r.added} خروجی تازه (${r.added*2} کانفیگ) اضافه شد ✓` : 'همه‌ی این خروجی‌ها قبلاً روی این اشتراک بودند', r.added>0);
    await loadLinks();
    reopenSubMembers(subId);
  }catch(e){ toast(e.message, false); }
}

async function removeLocalSubMember(subId, uid){
  try{ await api(`/api/subs/${subId}/links`, {method:'POST', body: JSON.stringify({link_id: uid, action:'remove'})}); toast('حذف شد'); reopenSubMembers(subId); }
  catch(e){ toast(e.message, false); }
}
async function removeRemoteSubMember(subId, refId){
  try{ await api(`/api/subs/${subId}/remote-links/${refId}`, {method:'DELETE'}); toast('حذف شد'); reopenSubMembers(subId); }
  catch(e){ toast(e.message, false); }
}
async function refreshRemoteSubMembers(subId){
  try{ await api(`/api/subs/${subId}/remote-links/refresh`, {method:'POST'}); toast('وضعیت نودها به‌روز شد ✓'); reopenSubMembers(subId); }
  catch(e){ toast(e.message, false); }
}

// ── افزودن اینباند از همین پنل ──
function openAddLocalMember(subId){
  const sub = SUBS_CACHE.find(s=>s.sub_id===subId); const already = new Set(sub?.link_ids||[]);
  const options = (typeof LINKS!=='undefined' ? LINKS : []).filter(l=>!l.is_client && !already.has(l.uuid));
  const rows = options.map(l=>`<label class="ob-row"><input type="checkbox" name="addLocal" value="${escapeHtml(l.uuid)}"><span class="ob-txt"><b>${escapeHtml(l.label)}</b><small>${escapeHtml(protoLabel(l))} · پورت ${l.port||443}</small></span></label>`).join('')
    || '<div class="sg-empty">اینباند دیگری در این پنل نیست</div>';
  openDrawer('افزودن از این پنل', `<div class="ob-list ob-picker sg-picklist">${rows}</div>`,
    `<button class="btn primary" style="flex:1" id="addLocalBtn" onclick="submitAddLocalMembers('${subId}')" ${options.length?'':'disabled'}><i class="ti ti-plus"></i>افزودن</button>`);
}
async function submitAddLocalMembers(subId){
  const uids = [...document.querySelectorAll('input[name=addLocal]:checked')].map(i=>i.value);
  if(!uids.length){ toast('حداقل یک اینباند انتخاب کن', false); return; }
  try{
    for(const uid of uids){ await api(`/api/subs/${subId}/links`, {method:'POST', body: JSON.stringify({link_id: uid, action:'add'})}); }
    toast(`${uids.length} اینباند اضافه شد ✓`); reopenSubMembers(subId);
  }catch(e){ toast(e.message, false); }
}

// ── افزودن اینباند از یک نود دیگر ──
async function openAddRemoteMember(subId){
  await loadNodes();
  const usable = NODES_LIST.filter(n=>n.enabled && n.status && n.status.online);
  if(!usable.length){ toast('نودی آنلاین برای انتخاب نیست؛ اول از تب «نودها» یک نود وصل کن', false); openOutboundManager===undefined&&null; if(typeof openNodeSwitcher==='function') gotoPage('nodes'); return; }
  openDrawer('افزودن از نود — انتخاب نود', usable.map(n=>`<label class="ob-row"><input type="radio" name="pickNode" value="${n.id}"><span class="nd-dot on"></span><span class="ob-txt"><b>${escapeHtml(n.name)}</b><small>${escapeHtml(n.url)}</small></span></label>`).join(''),
    `<button class="btn primary" style="flex:1" onclick="loadNodeInboundsForAdd('${subId}')"><i class="ti ti-arrow-left"></i>بعدی: انتخاب اینباند</button>`);
}
async function loadNodeInboundsForAdd(subId){
  const nodeId = (document.querySelector('input[name=pickNode]:checked')||{}).value;
  if(!nodeId){ toast('یک نود انتخاب کن', false); return; }
  try{
    const r = await api(`/api/nodes/${nodeId}/inbounds`);
    const sub = SUBS_CACHE.find(s=>s.sub_id===subId);
    const already = new Set((sub?.remote_links||[]).filter(e=>e.node_id===nodeId).map(e=>e.uuid));
    const items = (r.inbounds||[]).filter(i=>!already.has(i.uuid));
    const rows = items.map(i=>`<label class="ob-row"><input type="checkbox" name="addRemote" value="${escapeHtml(i.uuid)}"><span class="ob-txt"><b>${escapeHtml(i.label)}</b><small>${escapeHtml(i.protocol_display||'')} · پورت ${i.port||443}${i.outbound?` · ${flagHtml(i.outbound)} ${escapeHtml(i.outbound.country||i.outbound.name||'')}`:''}</small></span></label>`).join('')
      || '<div class="sg-empty">این نود اینباند دیگری برای افزودن ندارد</div>';
    openDrawer(`افزودن از نود «${escapeHtml(r.node.name)}»`, `<div class="ob-list ob-picker sg-picklist">${rows}</div>`,
      `<button class="btn primary" style="flex:1" id="addRemoteBtn" onclick="submitAddRemoteMembers('${subId}','${nodeId}')" ${items.length?'':'disabled'}><i class="ti ti-plus"></i>افزودن</button>`);
  }catch(e){ toast(e.message, false); }
}
async function submitAddRemoteMembers(subId, nodeId){
  const uuids = [...document.querySelectorAll('input[name=addRemote]:checked')].map(i=>i.value);
  if(!uuids.length){ toast('حداقل یک اینباند انتخاب کن', false); return; }
  try{
    const r = await api(`/api/subs/${subId}/remote-links`, {method:'POST', body: JSON.stringify({node_id: nodeId, uuids})});
    if(r.failed && r.failed.length) toast(`${r.added} اضافه شد، ${r.failed.length} مورد ناموفق: ${r.failed[0].error}`, r.added>0);
    else toast(`${r.added} اینباند از نود اضافه شد ✓`);
    reopenSubMembers(subId);
  }catch(e){ toast(e.message, false); }
}

// ============================================================
// REPORTS
// ============================================================
async function loadReports(){
  try{
    const days = $('repDays').value;
    const res = await api(`/api/reports/summary?days=${days}`);
    const t = res.totals||{};
    $('repStats').innerHTML = `
      ${statCard('ti-link','#4f7cff', t.links, 'کل کانفیگ‌ها')}
      ${statCard('ti-circle-check','#22c58b', t.active_links, 'فعال')}
      ${statCard('ti-folders','#f5a524', t.subs, 'گروه‌های ساب')}
      ${statCard('ti-users-group','#4f7cff', t.admins, 'ادمین‌ها')}
    `;
    $('repTopBody').innerHTML = (res.top_links||[]).map(l=>`
      <tr><td>${escapeHtml(l.label)}</td><td><span class="badge gray">${protoLabel(l)}</span></td><td class="mono">${fmtBytes(l.used_bytes)}</td></tr>
    `).join('') || `<tr><td colspan="3" class="empty">داده‌ای موجود نیست</td></tr>`;
  }catch(e){ toast(e.message, false); }
}

// ============================================================
// ADMINS
// ============================================================
const ADMIN_PERM_LABELS = {dashboard:'داشبورد',inbounds:'اینباند و کلاینت',clients:'ساخت کلاینت (بخش جدا)',subscriptions:'سابسکریپشن',categories:'دسته‌بندی',reports:'گزارش‌ها',messages:'پیام‌ها و خطاها',bot:'ربات',admins:'مدیریت حساب',settings:'تنظیمات'};
async function loadAdmins(){
  try{
    const res = await api('/api/admins');
    if(!(LINKS||[]).length){try{const lr=await api('/api/links');LINKS=lr.links||[];}catch(e){}}
    ADMIN_CACHE = res.admins || [];
    const adminRows = res.admins || [];
    const activeAdmins = adminRows.filter(a=>a.active).length;
    if($('adminTotal')) $('adminTotal').textContent = adminRows.length;
    if($('adminActive')) $('adminActive').textContent = activeAdmins;
    const _n=adminRows.filter(x=>x.role!=='owner'&&(x.allowed_inbounds||[]).length).length;
    if($('adScoped')){$('adScoped').textContent=_n;$('adFull').textContent=adminRows.length-_n;$('adInb').textContent=(LINKS||[]).filter(x=>!x.is_client).length;}
    $('adminsBody').innerHTML = adminRows.map(a=>{
      const isOwner = a.role==='owner';
      const initials = (a.username||'?').replace(/[^A-Za-z0-9آ-ی]/g,'').slice(0,2).toUpperCase() || '?';
      const lastLogin = a.last_login_at ? a.last_login_at.slice(0,16).replace('T',' ') : 'بدون ورود';
      const chips = isOwner
        ? '<span class="admin-perm-chip all"><i class="ti ti-shield-star"></i> دسترسی کامل</span>'
        : ((a.permissions||[]).length
            ? (a.permissions||[]).map(p=>`<span class="admin-perm-chip">${ADMIN_PERM_LABELS[p]||p}</span>`).join('')
            : '<span class="admin-perm-chip">بدون دسترسی</span>');
      const actions = isOwner ? '' : `
        <button class="iconbtn edit" title="ویرایش دسترسی" aria-label="ویرایش دسترسی" onclick="editAdmin('${a.id}')"><i class="ti ti-edit"></i></button>
        <button class="iconbtn power" title="${a.active?'غیرفعال‌سازی':'فعال‌سازی'}" onclick="toggleAdmin('${a.id}', ${!a.active})"><i class="ti ti-power"></i></button>
        <button class="iconbtn danger" title="حذف ادمین" aria-label="حذف ادمین" onclick="deleteAdmin('${a.id}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button>`;
      const ibAll=(LINKS||[]).filter(x=>!x.is_client);
      const scope=isOwner?[]:(a.allowed_inbounds||[]);
      const full=isOwner||!scope.length;
      const picked=scope.map(u=>ibAll.find(x=>x.uuid===u)).filter(Boolean);
      const pct=full?100:Math.round(picked.length/Math.max(1,ibAll.length)*100);
      const ibChips=full
        ? '<span class="adm-ib all"><i class="ti ti-infinity"></i> همه اینباندها ('+ibAll.length+')</span>'
        : (picked.slice(0,4).map(x=>`<span class="adm-ib"><i class="ti ti-plug-connected"></i>${escapeHtml(x.label||x.name||x.uuid.slice(0,8))}</span>`).join('')+(picked.length>4?`<span class="adm-ib more">+${picked.length-4}</span>`:'')||'<span class="adm-ib none">اینباند معتبری یافت نشد</span>');
      const permN=isOwner?'∞':(a.permissions||[]).length;
      return `
      <div class="admin-card adm-pro ${isOwner?'is-owner':''} ${a.active?'':'is-inactive'}">
        <div class="admin-card-top">
          <div class="admin-id"><div class="admin-avatar">${escapeHtml(initials)}</div>
            <div class="admin-meta"><div class="admin-name">${escapeHtml(a.username)}</div>
            <div class="admin-sub"><span class="admin-status-dot"></span>${a.active?'فعال':'غیرفعال'}</div></div></div>
          <span class="admin-role-badge ${isOwner?'owner':'admin'}"><i class="ti ti-${isOwner?'crown':'shield-check'}"></i>${isOwner?'مالک':'ادمین'}</span>
        </div>
        <div class="adm-stats">
          <div><b>${full?'همه':picked.length+' / '+ibAll.length}</b><small>اینباند مجاز</small></div>
          <div><b>${permN}</b><small>دسترسی</small></div>
          <div><b class="mono" style="font-size:10.5px">${escapeHtml(lastLogin.slice(5))}</b><small>آخرین ورود</small></div>
        </div>
        <div class="adm-scope"><div class="adm-scope-head"><span><i class="ti ti-lock${full?'-open':''}"></i> محدودیت اینباند</span><em>${full?'بدون محدودیت':pct+'٪ از اینباندها'}</em></div>
          <div class="adm-bar"><i class="${full?'full':''}" style="width:${pct}%"></i></div>
          <div class="adm-ibs">${ibChips}</div></div>
        <details class="adm-perms"><summary>دسترسی‌ها</summary><div class="admin-perm-row">${chips}</div></details>
        <div class="admin-card-foot"><div class="row-actions">${actions}</div></div>
      </div>`;
    }).join('');
  }catch(e){ toast(e.message, false); }
}
function inboundScopePickerHtml(prefix, checkedUuids){
  const inbounds = (LINKS||[]).filter(x=>!x.is_client);
  checkedUuids = checkedUuids||[];
  if(!inbounds.length) return '<div class="hint">ابتدا حداقل یک اینباند بساز</div>';
  return `<div class="scope-picker" style="max-height:160px;overflow:auto;display:flex;flex-direction:column;gap:6px;margin-top:6px">${inbounds.map(x=>`<label class="perm-item"><input type="checkbox" data-${prefix}scope="${x.uuid}" ${checkedUuids.includes(x.uuid)?'checked':''}>${escapeHtml(x.label||x.name||x.uuid.slice(0,8))}</label>`).join('')}</div>`;
}
function openAdminDrawer(){
  openDrawer('ادمین جدید', `
    <div class="grp"><label>نام کاربری</label><input id="aUser"></div>
    <div class="grp"><label>رمز عبور</label><input type="password" id="aPass"></div>
    <div class="grp"><label>محدود به اینباند(های) خاص <small>(خالی = دسترسی به همه)</small></label>${inboundScopePickerHtml('a',[])}</div>
    <div class="perm-grid">${Object.entries({dashboard:'داشبورد',inbounds:'ساخت و مدیریت اینباند',clients:'ساخت کلاینت (بخش جدا)',subscriptions:'سابسکریپشن',categories:'دسته‌بندی',reports:'گزارش‌ها',messages:'پیام‌ها و خطاها',bot:'ربات',admins:'مدیریت حساب',settings:'تنظیمات',inbound_create:'ساخت اینباند جدید',inbound_edit:'ویرایش اینباند',inbound_delete:'حذف اینباند',client_create:'ساخت کلاینت',client_edit:'ویرایش/تغییر وضعیت کلاینت',client_delete:'حذف کلاینت',client_reset:'ریست مصرف کلاینت',outbound_manage:'مدیریت خروجی/پراکسی',live_connections:'اتصال‌های زنده و IP'}).map(([k,v])=>`<label class="perm-item"><input type="checkbox" data-perm="${k}" ${['dashboard','inbounds','subscriptions'].includes(k)?'checked':''}>${v}</label>`).join('')}</div>
  `, `<button class="btn primary" style="flex:1" onclick="submitAdmin()"><i class="ti ti-device-floppy"></i>ساخت</button>`);
}
function editAdmin(id){
  const a = ADMIN_CACHE.find(x=>x.id===id); if(!a || a.role==='owner') return;
  const perms=['dashboard','inbounds','clients','subscriptions','categories','reports','messages','bot','admins','settings','inbound_create','inbound_edit','inbound_delete','client_create','client_edit','client_delete','client_reset','outbound_manage','live_connections'];
  const labels={dashboard:'داشبورد',inbounds:'اینباند و کلاینت',clients:'ساخت کلاینت (بخش جدا)',subscriptions:'سابسکریپشن',categories:'دسته‌بندی',reports:'گزارش‌ها',messages:'پیام‌ها و خطاها',bot:'ربات',admins:'مدیریت حساب',settings:'تنظیمات',inbound_create:'ساخت اینباند جدید',inbound_edit:'ویرایش اینباند',inbound_delete:'حذف اینباند',client_create:'ساخت کلاینت',client_edit:'ویرایش/تغییر وضعیت کلاینت',client_delete:'حذف کلاینت',client_reset:'ریست مصرف کلاینت',outbound_manage:'مدیریت خروجی/پراکسی',live_connections:'اتصال‌های زنده و IP'};
  openDrawer('ویرایش ادمین', `
    <div class="grp"><label>نام کاربری</label><input id="eUser" value="${escapeHtml(a.username||'')}"></div>
    <div class="grp"><label>رمز جدید <small>(اختیاری)</small></label><input type="password" id="ePass" placeholder="بدون تغییر خالی بگذار"></div>
    <div class="grp"><label>محدود به اینباند(های) خاص <small>(خالی = دسترسی به همه)</small></label>${inboundScopePickerHtml('e',a.allowed_inbounds||[])}</div>
    <div class="perm-grid">${perms.map(k=>`<label class="perm-item"><input type="checkbox" data-eperm="${k}" ${((a.permissions||[]).includes(k)?'checked':'')}>${labels[k]}</label>`).join('')}</div>
  `, `<button class="btn primary" style="flex:1" onclick="saveAdminEdit('${a.id}')"><i class="ti ti-device-floppy"></i>ذخیره تغییرات</button>`);
}
async function saveAdminEdit(id){
  try{
    const permissions=[...document.querySelectorAll('[data-eperm]:checked')].map(x=>x.dataset.eperm);
    const allowed_inbounds=[...document.querySelectorAll('[data-escope]:checked')].map(x=>x.dataset.escope);
    const body={username:$('eUser').value.trim(),permissions,allowed_inbounds}; if($('ePass').value) body.password=$('ePass').value;
    await api(`/api/admins/${id}`,{method:'PATCH',body:JSON.stringify(body)}); toast('اطلاعات ادمین بروزرسانی شد ✓'); closeDrawer(); loadAdmins();
  }catch(e){toast(e.message,false)}
}

async function submitAdmin(){
  try{
    const allowed_inbounds=[...document.querySelectorAll('[data-ascope]:checked')].map(x=>x.dataset.ascope);
    await api('/api/admins', {method:'POST', body: JSON.stringify({username:$('aUser').value, password:$('aPass').value, permissions:[...document.querySelectorAll('[data-perm]:checked')].map(x=>x.dataset.perm), allowed_inbounds})});
    toast('ساخته شد'); closeDrawer(); loadAdmins();
  }
  catch(e){ toast(e.message, false); }
}
async function toggleAdmin(id, active){
  try{ await api(`/api/admins/${id}`, {method:'PATCH', body:JSON.stringify({active})}); loadAdmins(); }
  catch(e){ toast(e.message, false); }
}
async function deleteAdmin(id){
  if(!confirm(t('این ادمین حذف شود؟'))) return;
  try{ await api(`/api/admins/${id}`, {method:'DELETE'}); toast('حذف شد'); loadAdmins(); }
  catch(e){ toast(e.message, false); }
}

// ============================================================
// Admin registration requests
// ============================================================
let ADMIN_REQ_CACHE = [];
async function loadAdminRequests(){
  try{
    const res = await api('/api/admin-requests');
    ADMIN_REQ_CACHE = res.requests || [];
    const card = $('adminReqCard');
    const pending = ADMIN_REQ_CACHE.filter(r=>r.status==='pending');
    $('adminReqBadge').textContent = pending.length + ' درخواست';
    if(!ADMIN_REQ_CACHE.length){ card.style.display='none'; return; }
    card.style.display = '';
    const rows = [...pending, ...ADMIN_REQ_CACHE.filter(r=>r.status!=='pending')].slice(0, 30);
    $('adminReqBody').innerHTML = rows.length ? rows.map(r=>{
      const date = r.created_at ? r.created_at.slice(0,16).replace('T',' ') : '';
      let statusHtml = '';
      let actions = '';
      if(r.status==='pending'){
        actions = `<button class="btn primary" style="padding:8px 12px;font-size:11px" onclick="approveAdminReq('${r.id}')"><i class="ti ti-check"></i>تایید و ساخت ادمین</button>
                   <button class="btn" style="padding:8px 12px;font-size:11px" onclick="rejectAdminReq('${r.id}')"><i class="ti ti-x"></i>رد</button>`;
      } else {
        statusHtml = `<span class="areq-status ${r.status}">${r.status==='approved'?'تایید شده':'رد شده'}</span>`;
      }
      return `<div class="areq-row">
        <div class="areq-info">
          <div class="areq-name">${escapeHtml(r.full_name||'-')}</div>
          <div class="areq-meta"><span><i class="ti ti-brand-telegram"></i>@${escapeHtml(r.telegram_id||'-')}</span><span><i class="ti ti-clock"></i>${escapeHtml(date)}</span></div>
          ${r.note ? `<div class="areq-note">${escapeHtml(r.note)}</div>` : ''}
        </div>
        <div class="areq-actions">${actions}${statusHtml}</div>
      </div>`;
    }).join('') : `<div class="areq-empty">درخواستی ثبت نشده است</div>`;
  }catch(e){ /* silent: پنل قدیمی‌تر ممکنه این endpoint رو نداشته باشه */ }
}
function approveAdminReq(id){
  const r = ADMIN_REQ_CACHE.find(x=>x.id===id); if(!r) return;
  const suggestedUser = (r.telegram_id||'admin').replace(/[^A-Za-z0-9_]/g,'').toLowerCase() || 'admin';
  openDrawer('تایید ادمین: ' + r.full_name, `
    <div class="grp"><label>درخواست‌کننده</label><input value="${escapeHtml(r.full_name)} (@${escapeHtml(r.telegram_id)})" disabled></div>
    <div class="grp"><label>نام کاربری</label><input id="arUser" value="${escapeHtml(suggestedUser)}"></div>
    <div class="grp"><label>رمز عبور</label><input id="arPass" value="${Math.random().toString(36).slice(-8)}"></div>
    <div class="grp"><label>شارژ اولیه (استارز)</label><input id="arCredit" type="number" min="0" value="0"></div>
    <div class="perm-grid">${Object.entries({dashboard:'داشبورد',inbounds:'ساخت و مدیریت اینباند',clients:'ساخت کلاینت (بخش جدا)',subscriptions:'سابسکریپشن',categories:'دسته‌بندی',reports:'گزارش‌ها',messages:'پیام‌ها و خطاها',bot:'ربات',admins:'مدیریت حساب',settings:'تنظیمات',inbound_create:'ساخت اینباند جدید',inbound_edit:'ویرایش اینباند',inbound_delete:'حذف اینباند',client_create:'ساخت کلاینت',client_edit:'ویرایش/تغییر وضعیت کلاینت',client_delete:'حذف کلاینت',client_reset:'ریست مصرف کلاینت',outbound_manage:'مدیریت خروجی/پراکسی',live_connections:'اتصال‌های زنده و IP'}).map(([k,v])=>`<label class="perm-item"><input type="checkbox" data-arperm="${k}" ${['dashboard','inbounds','subscriptions'].includes(k)?'checked':''}>${v}</label>`).join('')}</div>
  `, `<button class="btn primary" style="flex:1" onclick="confirmApproveAdminReq('${r.id}')"><i class="ti ti-check"></i>تایید و ساخت حساب</button>`);
}
async function confirmApproveAdminReq(id){
  try{
    const permissions=[...document.querySelectorAll('[data-arperm]:checked')].map(x=>x.dataset.arperm);
    const body={
      username: $('arUser').value.trim(),
      password: $('arPass').value,
      permissions,
      credit_stars: Number($('arCredit').value)||0,
    };
    const res = await api(`/api/admin-requests/${id}/approve`, {method:'POST', body: JSON.stringify(body)});
    closeDrawer();
    const msg = res.delivery_message || '';
    openDrawer('اطلاعات ورود ادمین', `
      <p style="font-size:11.5px;color:var(--sub);line-height:1.9">این متن را برای <b>@${escapeHtml(res.telegram_id||'')}</b> در تلگرام ارسال کن:</p>
      <textarea id="arDeliveryMsg" readonly style="width:100%;min-height:150px;background:var(--panel2);border:1px solid var(--line);color:var(--text);border-radius:12px;padding:12px;font:inherit;line-height:1.9">${escapeHtml(msg)}</textarea>
    `, `<button class="btn primary" style="flex:1" onclick="copyDeliveryMsg()"><i class="ti ti-copy"></i>کپی متن</button><button class="btn" style="flex:1" onclick="closeDrawer()">بستن</button>`);
    loadAdmins(); loadAdminRequests();
  }catch(e){ toast(e.message, false); }
}
function copyDeliveryMsg(){
  const el = document.getElementById('arDeliveryMsg');
  if(!el) return;
  el.select();
  try{ navigator.clipboard.writeText(el.value); toast('کپی شد ✓'); }catch(e){ document.execCommand('copy'); toast('کپی شد ✓'); }
}
async function rejectAdminReq(id){
  if(!confirm('این درخواست رد شود؟')) return;
  try{ await api(`/api/admin-requests/${id}/reject`, {method:'POST', body: JSON.stringify({})}); toast('درخواست رد شد'); loadAdminRequests(); }
  catch(e){ toast(e.message, false); }
}

// ============================================================
// ACTIVITY
// ============================================================
async function loadActivity(){
  try{
    const res = await api('/api/activity');
    $('activityBody').innerHTML = (res.logs||[]).slice().reverse().map(l=>`
      <tr><td class="mono">${(l.time||l.ts||'').toString().slice(0,16).replace('T',' ')}</td>
      <td><span class="badge ${l.level==='err'?'red':l.level==='warn'?'orange':'green'}">${l.type||l.kind||'—'}</span></td>
      <td>${escapeHtml(l.message||l.text||'')}</td></tr>
    `).join('') || `<tr><td colspan="3" class="empty">لاگی وجود ندارد</td></tr>`;
  }catch(e){ toast(e.message, false); }
}

// ============================================================
// MESSAGE CENTER
// ============================================================
function setMessageFilter(filter){
  MESSAGE_FILTER=filter;
  document.querySelectorAll('[data-message-filter]').forEach(b=>b.classList.toggle('on',b.dataset.messageFilter===filter));
  loadMessages();
}
function messageIcon(level, source){
  if(source==='client') return 'browser';
  if(level==='warn') return 'alert-triangle';
  if(level==='err') return 'alert-circle';
  return 'info-circle';
}
async function clearErrors(){
  if(!confirm(t('همه خطاهای ثبت‌شده پاک شوند؟'))) return;
  try{await api('/api/errors/clear',{method:'POST'});toast('خطاها پاک شدند ✓');loadMessages();}
  catch(e){toast(e.message,false);}
}
async function loadMessages(){
  try{
    const [er,act]=await Promise.all([api('/api/errors'),api('/api/activity')]);
    const errors=(er.errors||[]).slice().reverse();
    const filtered=errors.filter(x=>MESSAGE_FILTER==='all' || x.level===MESSAGE_FILTER || x.source===MESSAGE_FILTER);
    $('messageStats').innerHTML=`
      <div class="message-stat ${er.total_errors?'danger':'good'}"><div class="ms-icon"><i class="ti ti-alert-circle"></i></div><b>${Number(er.total_errors||0)}</b><small>کل خطاهای ثبت‌شده</small></div>
      <div class="message-stat warn"><div class="ms-icon"><i class="ti ti-alert-triangle"></i></div><b>${Number(er.warnings||0)}</b><small>هشدارهای اخیر</small></div>
      <div class="message-stat"><div class="ms-icon"><i class="ti ti-browser"></i></div><b>${Number(er.client_errors||0)}</b><small>خطاهای مرورگر</small></div>
      <div class="message-stat good"><div class="ms-icon"><i class="ti ti-heartbeat"></i></div><b>${er.healthy?'OK':'CHECK'}</b><small>وضعیت سیستم</small></div>`;
    $('nb-errors').textContent=String(Math.min(99,Number(er.total_errors||0)));
    $('nb-errors').style.display=Number(er.total_errors||0)?'inline-flex':'none';
    $('messageLastSync').textContent='آخرین بروزرسانی '+new Date().toLocaleTimeString('fa-IR',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
    $('messageList').innerHTML=filtered.length?filtered.map(x=>{
      const lvl=x.level||'err'; const src=x.source||'server';
      return `<article class="message-row ${lvl}"><div class="mi"><i class="ti ti-${messageIcon(lvl,src)}"></i></div><div class="mt"><b>${escapeHtml(x.error||x.message||'خطای نامشخص')}</b><p>${escapeHtml(src==='client'?'Frontend / Browser':(x.method||'SERVER')+' · '+(x.path||''))}</p>${x.stack||x.details?`<div class="error-detail">${escapeHtml(x.stack||x.details||'')}</div>`:''}</div><div class="meta"><strong>${escapeHtml(x.time||'—')}</strong><span>${escapeHtml(src)}</span></div></article>`;
    }).join(''):`<div class="message-empty"><i class="ti ti-shield-check"></i>خطای ثبت‌شده‌ای وجود ندارد. سیستم سالم است.</div>`;
    const logs=(act.logs||[]).slice().reverse().slice(0,25);
    $('messageActivityList').innerHTML=logs.length?logs.map(l=>`<article class="message-row ${l.level==='err'?'err':l.level==='warn'?'warn':'ok'}"><div class="mi"><i class="ti ti-${l.level==='err'?'alert-circle':l.level==='warn'?'alert-triangle':'circle-check'}"></i></div><div class="mt"><b>${escapeHtml(l.message||l.text||'')}</b><p>${escapeHtml(l.kind||l.type||'system')}</p></div><div class="meta"><strong>${escapeHtml((l.time||l.ts||'').toString().replace('T',' ').slice(0,19))}</strong></div></article>`).join(''):'<div class="message-empty">رویدادی وجود ندارد.</div>';
  }catch(e){toast(e.message,false);reportClientError(e.message,'messages',{stack:e.stack});}
}
if(messageTimer) clearInterval(messageTimer);
let messagesTimer=setInterval(()=>{if(!document.hidden && CURRENT_PAGE==='messages') loadMessages()},15000);

// ============================================================
// SETTINGS
// ============================================================
const BOT_LOCKED_MSG = 'ویرایش متن‌های ربات قفل شده است و امکان تغییر ندارد';
function setBotDot(running){
  $('botDot').className = 'status-dot ' + (running?'on':'off');
  $('botStatusText').textContent = running ? 'ربات روشن است' : 'ربات خاموش است';
  $('botStartBtn').disabled = !!running;
  $('botStopBtn').disabled = !running;
}
async function loadSettings(){
  try{
    const s = await api('/api/settings');
    $('setBaseUrl').value = s.public_base_url || '';
    if($('adminUsername')) $('adminUsername').value = s.admin_username || '';
    $('setTcpHost').value = s.tcp_public_host || '';
    $('setTcpPort').value = s.tcp_public_port || '';
    $('tcpListenHint').textContent = `سرور TCP روی پورت داخلی ${s.tcp_listen_port} گوش می‌دهد — این را در Railway به همین پورت داخلی متصل کن، نه به PORT اصلی HTTP.`;
    $('setBotToken').value = s.bot_token || '';
    $('setBotAdmins').value = s.bot_admin_ids || '';
    setBotDot(s.bot_running);
    if($('subTplName')) $('subTplName').checked = s.sub_remark_show_name !== false;
    if($('subTplVolume')) $('subTplVolume').checked = !!s.sub_remark_show_volume;
    if($('subTplId')) $('subTplId').checked = !!s.sub_remark_show_id;
    if($('subTplInbound')) $('subTplInbound').checked = !!s.sub_remark_show_inbound;
    if($('infoLineEnabled')) $('infoLineEnabled').checked = s.sub_info_line_enabled !== false;
    if($('infoLineVolume')) $('infoLineVolume').checked = s.sub_info_line_show_volume !== false;
    if($('infoLineExpiry')) $('infoLineExpiry').checked = s.sub_info_line_show_expiry !== false;
    updateSubTemplatePreview();
    updateInfoLinePreview();
    if($('setSupportId')) $('setSupportId').value = s.support_username ? '@'+s.support_username : '';
    if($('setChannelId')) $('setChannelId').value = s.channel_username ? '@'+s.channel_username : '';
    if($('nameStyleEnabled')) $('nameStyleEnabled').checked = s.name_style_enabled !== false;
    updateBrandPreview();
    try{ const bt=await api('/api/bot/texts'); const x=bt.texts||{}; if($('botTxtWelcome'))$('botTxtWelcome').value=x.welcome||''; if($('botTxtAdmin'))$('botTxtAdmin').value=x.admin_menu||''; if($('botTxtCreated'))$('botTxtCreated').value=x.config_created||''; }catch(_){}
    loadProxies();
  }catch(e){ toast(e.message, false); }
}

// ===== پشتیبانی + استایل نام کانفیگ =====
function updateBrandPreview(){
  const id=($('setSupportId')?.value||'').trim().replace(/^https?:\/\/t\.me\//i,'').replace(/^@/,'')||'VodiWalker';
  if($('brandSupportPreview')) $('brandSupportPreview').textContent='پشتیبانی: @'+id;
  if($('supportTestLink')) $('supportTestLink').href='https://t.me/'+id;
  if($('brandNamePreview')) $('brandNamePreview').textContent=$('nameStyleEnabled')?.checked?'VodiWalker|Tofan🚀':'VodiWalker';
}
async function saveBrandSettings(){
  try{
    await api('/api/settings', {method:'POST', body: JSON.stringify({
      support_username: ($('setSupportId')?.value||'').trim(),
      channel_username: ($('setChannelId')?.value||'').trim(),
      name_style_enabled: !!$('nameStyleEnabled')?.checked,
    })});
    toast('پشتیبانی و استایل نام‌ها ذخیره شد ✓');
    loadSettings();
  }catch(e){ toast(e.message, false); }
}
const NAME_STUDIO_INPUTS=['fLabel','cbLabel','clientName','cmClientName'];
document.addEventListener('focusin',e=>{const el=e.target;if(el&&NAME_STUDIO_INPUTS.includes(el.id))attachNameStudio(el)});
function attachNameStudio(input){
  if(input.dataset.nsAttached) return; input.dataset.nsAttached='1';
  const box=document.createElement('div'); box.className='name-studio';
  box.innerHTML='<div class="ns-head"><span><i class="ti ti-sparkles"></i> اسم‌های خفن (کلیک کن)</span><button type="button" class="ns-more"><i class="ti ti-dice-5"></i> پیشنهاد جدید</button></div><div class="ns-chips"></div>';
  input.insertAdjacentElement('afterend',box);
  const chips=box.querySelector('.ns-chips');
  async function load(){
    chips.innerHTML='<span class="ns-wait">…</span>';
    try{
      const base=(input.value||'').split('|')[0].replace(/[^\p{L}\p{N} _-]/gu,'').trim()||'VodiWalker';
      const r=await api('/api/name-suggestions?base='+encodeURIComponent(base)+'&n=8');
      chips.innerHTML='';
      (r.suggestions||[]).forEach(n=>{const b=document.createElement('button');b.type='button';b.className='ns-chip';b.textContent=n;b.onclick=()=>{input.value=n;input.dispatchEvent(new Event('input',{bubbles:true}));toast('اسم انتخاب شد ✓');};chips.appendChild(b);});
    }catch(err){chips.innerHTML='';}
  }
  box.querySelector('.ns-more').onclick=load; load();
}
function updateSubTemplatePreview(){
  const parts=[];
  if($('subTplName')?.checked) parts.push('MyConfig');
  if($('subTplVolume')?.checked) parts.push('50 GB');
  if($('subTplId')?.checked) parts.push('a1b2c3d4');
  if($('subTplInbound')?.checked) parts.push('Inbound-1');
  const el=$('subTplPreview'); if(el) el.textContent = parts.join(' | ') || 'MyConfig';
}
document.addEventListener('change', e=>{ if(['subTplName','subTplVolume','subTplId','subTplInbound'].includes(e.target?.id)) updateSubTemplatePreview(); if(['infoLineEnabled','infoLineVolume','infoLineExpiry'].includes(e.target?.id)) updateInfoLinePreview(); });
function updateInfoLinePreview(){
  const el=$('infoLinePreview'); if(!el) return;
  if(!$('infoLineEnabled')?.checked){ el.textContent='(غیرفعال — هیچ ردیفی اضافه نمی‌شود)'; return; }
  const parts=['🌐 Vodiwalkerpanel'];
  if($('infoLineVolume')?.checked) parts.push('12 GB/50 GB (باقی 38 GB)');
  if($('infoLineExpiry')?.checked) parts.push('۱۲د ۴س');
  el.textContent = parts.join(' | ');
}
async function saveInfoLineSettings(){
  try{
    await api('/api/settings', {method:'POST', body: JSON.stringify({
      sub_info_line_enabled: !!$('infoLineEnabled')?.checked,
      sub_info_line_show_volume: !!$('infoLineVolume')?.checked,
      sub_info_line_show_expiry: !!$('infoLineExpiry')?.checked,
    })});
    toast('تنظیمات سرور اطلاعاتی ذخیره شد ✓');
  }catch(e){ toast(e.message, false); }
}
async function saveSubTemplate(){
  try{
    await api('/api/settings', {method:'POST', body: JSON.stringify({
      sub_remark_show_name: !!$('subTplName')?.checked,
      sub_remark_show_volume: !!$('subTplVolume')?.checked,
      sub_remark_show_id: !!$('subTplId')?.checked,
      sub_remark_show_inbound: !!$('subTplInbound')?.checked,
    })});
    toast('الگوی نام کانفیگ‌های ساب ذخیره شد ✓');
  }catch(e){ toast(e.message, false); }
}
async function saveTcpSettings(){
  try{
    await api('/api/settings', {method:'POST', body: JSON.stringify({tcp_public_host: $('setTcpHost').value, tcp_public_port: $('setTcpPort').value})});
    toast('آدرس TCP ذخیره شد');
  }catch(e){ toast(e.message, false); }
}
async function saveBaseUrl(){
  try{ await api('/api/settings', {method:'POST', body: JSON.stringify({public_base_url: $('setBaseUrl').value})}); toast('آدرس ذخیره شد'); refreshOverview(); }
  catch(e){ toast(e.message, false); }
}
async function saveBotSettings(){
  try{
    const r = await api('/api/settings', {method:'POST', body: JSON.stringify({bot_token: $('setBotToken').value, bot_admin_ids: $('setBotAdmins').value})});
    toast(r.bot_restarted ? 'ذخیره شد و ربات با تنظیمات جدید ری‌استارت شد' : 'ذخیره شد — برای اعمال، ربات را روشن کنید');
    setBotDot(r.running);
  }catch(e){ toast(e.message, false); }
}
async function botStart(){
  try{ const r = await api('/api/settings/bot/start', {method:'POST'}); toast('ربات روشن شد'); setBotDot(r.running); }
  catch(e){ toast(e.message, false); }
}
async function botStop(){
  try{ const r = await api('/api/settings/bot/stop', {method:'POST'}); toast('ربات خاموش شد'); setBotDot(r.running); }
  catch(e){ toast(e.message, false); }
}
async function saveBotTexts(){
  toast(BOT_LOCKED_MSG, false); return;
  try{ await api('/api/bot/texts',{method:'POST',body:JSON.stringify({texts:{welcome:$('botTxtWelcome').value,admin_menu:$('botTxtAdmin').value,config_created:$('botTxtCreated').value}})}); toast('متن‌های ربات ذخیره شد ✓'); }catch(e){toast(e.message,false)}
}
function toggleSettingsPass(id, btn){
  const inp = $(id);
  if(!inp) return;
  const icon = btn ? btn.querySelector('i') : null;
  if(inp.type === 'password'){ inp.type = 'text'; if(icon) icon.className = 'ti ti-eye-off'; }
  else { inp.type = 'password'; if(icon) icon.className = 'ti ti-eye'; }
}
function passwordMeter(){
  const val = $('newPass') ? $('newPass').value : '';
  const bar = $('passMeterBar'), hint = $('passHint');
  if(!bar) return;
  let score = 0;
  if(val.length >= 8) score++;
  if(val.length >= 12) score++;
  if(/[a-z]/.test(val) && /[A-Z]/.test(val)) score++;
  if(/[0-9]/.test(val)) score++;
  if(/[^A-Za-z0-9]/.test(val)) score++;
  const levels = [
    {pct:4,  color:'var(--bad)',  label:'خیلی ضعیف'},
    {pct:25, color:'var(--bad)',  label:'ضعیف'},
    {pct:50, color:'var(--warn)', label:'متوسط'},
    {pct:75, color:'var(--warn)', label:'خوب'},
    {pct:100,color:'var(--good)', label:'قوی'},
    {pct:100,color:'var(--good)', label:'خیلی قوی'},
  ];
  const lv = levels[Math.min(score, levels.length-1)];
  bar.style.width = (val ? lv.pct : 0) + '%';
  bar.style.background = lv.color;
  if(hint) hint.textContent = val ? `قدرت رمز: ${lv.label} — حداقل ۸ کاراکتر، ترکیب حروف بزرگ/کوچک، عدد و نماد پیشنهاد می‌شود.` : 'حداقل ۸ کاراکتر، ترجیحاً ترکیب حروف، عدد و نماد.';
}
async function revokeOtherSessions(){
  if(!confirm(t('همه نشست‌های قبلی این حساب لغو شوند؟'))) return;
  try{const r=await api('/api/security/revoke-other-sessions',{method:'POST'});toast(`${r.revoked||0} نشست قبلی لغو شد ✓`)}catch(e){toast(e.message,false)}
}
function fmtDiagBytes(n){return fmtBytes(Number(n||0))}
async function loadDiagnostics(){
  const box=$('diagGrid'), st=$('diagStatus'); if(!box) return;
  st.textContent='CHECKING'; st.className='badge orange';
  try{
    const d=await api('/api/system/diagnostics'); const r=d.resources||{}, o=d.objects||{}, b=d.bot||{}, sec=d.security||{};
    box.innerHTML=`<div class="diag-item"><small>Service</small><b>${escapeHtml(d.service?.status||'—')}</b><span>${escapeHtml(d.uptime||'—')}</span></div><div class="diag-item"><small>CPU</small><b>${Number(r.cpu_percent||0).toFixed(1)}%</b><span>Process load</span></div><div class="diag-item"><small>Memory</small><b>${Number(r.memory_percent||0).toFixed(1)}%</b><span>${fmtDiagBytes(r.memory_rss)}</span></div><div class="diag-item"><small>Disk</small><b>${Number(r.disk_percent||0).toFixed(1)}%</b><span>Root filesystem</span></div><div class="diag-item"><small>Inbounds</small><b>${o.inbounds||0}</b><span>${o.active_links||0} active</span></div><div class="diag-item"><small>Clients</small><b>${o.clients||0}</b><span>${o.subscriptions||0} subscriptions</span></div><div class="diag-item"><small>Bot</small><b>${b.running?'ONLINE':'OFFLINE'}</b><span>${b.admin_count||0} bot admins</span></div><div class="diag-item"><small>Sessions</small><b>${sec.session_count||0}</b><span>${escapeHtml(sec.username||'—')}</span></div>`;
    st.textContent='HEALTHY'; st.className='badge green';
  }catch(e){box.innerHTML=`<div class="diag-empty">${escapeHtml(e.message||'Diagnostics unavailable')}</div>`;st.textContent='ERROR';st.className='badge red';}
}

async function changeUsername(){
  const username = ($('adminUsername')?.value || '').trim();
  if(!username){ toast('نام کاربری را وارد کنید', false); return; }
  if(username.length < 3 || username.length > 40 || /\s/.test(username)){ toast('نام کاربری باید ۳ تا ۴۰ کاراکتر و بدون فاصله باشد', false); return; }
  const btn = document.activeElement && document.activeElement.tagName === 'BUTTON' ? document.activeElement : null; const originalHtml = btn ? btn.innerHTML : '';
  if(btn){ btn.disabled=true; btn.innerHTML='<i class="ti ti-loader-2 spin"></i>در حال ذخیره...'; }
  try{
    const r = await api('/api/change-username',{method:'POST',body:JSON.stringify({username})});
    if($('userName')) $('userName').textContent=r.username;
    if($('userChip')?.querySelector('.av')) $('userChip').querySelector('.av').textContent=(r.username||'?').slice(0,1).toUpperCase();
    toast('نام کاربری با موفقیت تغییر کرد ✓');
  }catch(e){ toast(e.message,false); }
  finally{ if(btn){btn.disabled=false;btn.innerHTML=originalHtml;} }
}
async function changePassword(){
  const current_password = $('curPass').value, new_password = $('newPass').value, repeat_password = $('repPass').value;
  if(!current_password || !new_password || !repeat_password){ toast('همه‌ی فیلدهای رمز عبور را پر کنید', false); return; }
  if(new_password.length < 8){ toast('رمز جدید باید حداقل ۸ کاراکتر باشد', false); return; }
  if(new_password !== repeat_password){ toast('تکرار رمز یکسان نیست', false); return; }
  if(new_password === current_password){ toast('رمز جدید باید با رمز فعلی متفاوت باشد', false); return; }
  const btn = document.activeElement && document.activeElement.tagName === 'BUTTON' ? document.activeElement : null;
  const originalHtml = btn ? btn.innerHTML : '';
  if(btn){ btn.disabled = true; btn.innerHTML = '<i class="ti ti-loader-2 spin"></i>در حال ذخیره...'; }
  try{
    await api('/api/change-password', {method:'POST', body: JSON.stringify({current_password, new_password, repeat_password})});
    toast('رمز عبور با موفقیت تغییر کرد ✓');
    $('curPass').value=$('newPass').value=$('repPass').value='';
    passwordMeter();
  }catch(e){ toast(e.message, false); }
  finally{ if(btn){ btn.disabled = false; btn.innerHTML = originalHtml; } }
}

// ===== VW pro: small UX helpers =====
(function(){
  document.addEventListener('keydown', function(e){
    if(e.key !== 'Escape') return;
    const d = document.getElementById('drawer');
    if(d && d.classList.contains('show')) closeDrawer();
  });
  if(typeof gotoPage === 'function'){
    const _orig = gotoPage;
    window.gotoPage = function(pg){
      const r = _orig.apply(this, arguments);
      const bw = document.querySelector('.body-wrap');
      if(bw && bw.scrollTo) bw.scrollTo({top:0, behavior:'auto'});
      return r;
    };
  }
})();
</script>

<button class="vwfx-btn" id="vwfxBtn" type="button" onclick="vwfxToggle(event)" aria-label="Glow & Performance"><i class="ti ti-sun"></i></button>
<div class="vwfx-pop" id="vwfxPop" onclick="event.stopPropagation()">
  <h4><span>نور و عملکرد</span><b id="vwfxVal">100%</b></h4>
  <label>شدت نور پس‌زمینه</label>
  <input class="vwfx-range" id="vwfxRange" type="range" min="0" max="150" step="5" value="100" oninput="vwfxGlow(this.value)" onchange="vwfxSave()">
  <div class="vwfx-row"><span>حالت سبک (بدون انیمیشن)</span><button class="vwfx-tg" id="vwfxLite" type="button" onclick="vwfxLiteToggle()" aria-label="Lite mode"></button></div>
</div>
<script>
(function(){
  var d=document.documentElement,raf=0;
  function get(k,def){try{var v=localStorage.getItem(k);return v===null?def:v}catch(e){return def}}
  function set(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  window.vwfxGlow=function(v){v=+v;cancelAnimationFrame(raf);raf=requestAnimationFrame(function(){
    d.style.setProperty('--vw-glow',v/100);
    document.getElementById('vwfxVal').textContent=v+'%';
    document.getElementById('vwfxRange').style.setProperty('--p',(v/150*100)+'%');});};
  window.vwfxSave=function(){set('vw_glow',document.getElementById('vwfxRange').value)};
  window.vwfxToggle=function(e){if(e)e.stopPropagation();document.getElementById('vwfxPop').classList.toggle('open')};
  function lite(on){d.classList.toggle('vw-fx-off',on);document.getElementById('vwfxLite').classList.toggle('on',on);set('vw_lite',on?'1':'0')}
  window.vwfxLiteToggle=function(){lite(!d.classList.contains('vw-fx-off'))};
  var g=+get('vw_glow',100);document.getElementById('vwfxRange').value=g;vwfxGlow(g);
  var on=get('vw_lite','0')==='1';d.classList.toggle('vw-fx-off',on);document.getElementById('vwfxLite').classList.toggle('on',on);
  document.addEventListener('click',function(){document.getElementById('vwfxPop').classList.remove('open')});
  document.addEventListener('visibilitychange',function(){d.classList.toggle('vw-paused',document.hidden)});
  /* mobile / low-end devices: start in lite mode once if the user never chose */
  if(get('vw_lite',null)===null&&(navigator.hardwareConcurrency||8)<=4&&matchMedia('(max-width:700px)').matches)lite(true);
})();
</script>
<div class="cmdk-ov" id="cmdkOv" hidden aria-hidden="true">
  <div class="cmdk" role="dialog" aria-modal="true" aria-label="جستجوی سراسری">
    <div class="cmdk-top">
      <i class="ti ti-search"></i>
      <input id="cmdkInput" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="go" placeholder="جستجو در اینباندها، کلاینت‌ها، دسته‌ها، نودها، تنظیمات…" role="combobox" aria-expanded="true" aria-controls="cmdkList" aria-autocomplete="list">
      <button class="cmdk-x" id="cmdkClose" type="button" aria-label="بستن">Esc</button>
    </div>
    <div class="cmdk-chips" id="cmdkChips">
      <button type="button" data-f="all" class="on">همه</button>
      <button type="button" data-f="inbound">اینباند / کلاینت</button>
      <button type="button" data-f="manage">دسته و ساب</button>
      <button type="button" data-f="infra">نود / پراکسی / ادمین</button>
      <button type="button" data-f="page">صفحه و تنظیمات</button>
      <button type="button" data-f="action">اقدام‌ها</button>
    </div>
    <div class="cmdk-list" id="cmdkList" role="listbox" aria-label="نتایج جستجو"></div>
    <div class="cmdk-foot"><span><kbd>↑</kbd><kbd>↓</kbd> حرکت</span><span><kbd>Enter</kbd> باز کردن</span><span><kbd>Tab</kbd> فیلتر</span><span><kbd>Esc</kbd> بستن</span><span class="cmdk-count" id="cmdkCount"></span></div>
  </div>
</div>
<script>
/* ===== VW PRO v2: helpers ===== */
(function(){
  var T={};
  window.vwDebounce=function(key,fn,ms){ clearTimeout(T[key]); T[key]=setTimeout(fn,ms||120); };
})();
</script>
<script>
/* ===== VW PRO: global search / command palette (Ctrl+K) ===== */
(function(){
  'use strict';
  var OV = document.getElementById('cmdkOv'), INP = document.getElementById('cmdkInput'),
      LIST = document.getElementById('cmdkList'), CNT = document.getElementById('cmdkCount'),
      CHIPS = document.getElementById('cmdkChips');
  if(!OV || !INP || !LIST) return;

  var TYPES = {
    page:{l:'صفحه',i:'ti-layout-dashboard',w:12}, action:{l:'اقدام',i:'ti-bolt',w:10},
    inbound:{l:'اینباند',i:'ti-network',w:8}, client:{l:'کلاینت',i:'ti-user',w:6},
    cat:{l:'دسته',i:'ti-category',w:5}, sub:{l:'گروه ساب',i:'ti-folders',w:5},
    node:{l:'نود',i:'ti-server-cog',w:5}, proxy:{l:'پراکسی',i:'ti-route',w:4},
    admin:{l:'ادمین',i:'ti-users-group',w:4}, section:{l:'بخش',i:'ti-settings',w:2}
  };
  var GROUPS = {
    all:null, inbound:['inbound','client'], manage:['cat','sub'],
    infra:['node','proxy','admin'], page:['page','section'], action:['action']
  };
  var PAGES = [
    ['overview','داشبورد','dashboard home overview مانیتور منابع cpu ram ترافیک','ti-layout-dashboard'],
    ['news','اخبار','news updates اطلاعیه','ti-news'],
    ['links','اینباندها','inbounds links کانفیگ vless vmess trojan','ti-network'],
    ['clientmgr','ساخت کلاینت','client manager کاربر مشتری','ti-user-plus'],
    ['categories','دسته‌بندی‌ها','categories category دسته محدودیت','ti-category'],
    ['subgroups','گروه‌های ساب','subscription subgroups اشتراک ساب','ti-folders'],
    ['reports','گزارش‌ها','reports stats آمار نمودار','ti-chart-histogram'],
    ['nodes','نودها','nodes servers سرور پنل','ti-server-cog'],
    ['admins','ادمین‌ها','admins users مدیر دسترسی','ti-users-group'],
    ['activity','فعالیت‌ها','activity log history لاگ تاریخچه','ti-history'],
    ['messages','پیام‌ها','messages errors notifications خطا اعلان','ti-bell-ringing'],
    ['settings','تنظیمات','settings appearance backup بکاپ ظاهر پوسته پراکسی','ti-settings']
  ];

  var open = false, items = [], results = [], active = 0, filter = 'all', lastFocus = null,
      fetching = false, timer = 0, pending = false, rowsHtmlKey = '';

  /* ---------- helpers ---------- */
  var NM = {'ك':'ک','ي':'ی','ى':'ی','ۀ':'ه','ة':'ه','أ':'ا','إ':'ا','آ':'ا','ؤ':'و'};
  // نرمال‌سازی یک‌به‌یک (طول رشته ثابت می‌ماند تا هایلایت درست بیفتد)
  function nz(s){
    return String(s == null ? '' : s)
      .replace(/[\u06F0-\u06F9\u0660-\u0669]/g, function(c){ return String(c.charCodeAt(0) & 15); })
      .replace(/[كيىۀةأإآؤ]/g, function(c){ return NM[c]; })
      .replace(/[\u200c\u200e\u200f\u0640]/g, ' ')
      .toLowerCase();
  }
  function esc(s){ return (typeof escapeHtml === 'function') ? escapeHtml(String(s == null ? '' : s)) : String(s == null ? '' : s).replace(/[&<>"']/g, function(c){ return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]; }); }
  function lsGet(k, d){ try{ var v = localStorage.getItem(k); return v == null ? d : v; }catch(e){ return d; } }
  function lsSet(k, v){ try{ localStorage.setItem(k, v); }catch(e){} }
  function tokens(q){ return nz(q).split(/\s+/).filter(Boolean).slice(0, 6); }
  function safe(fn){ try{ return fn(); }catch(e){ if(window.console) console.warn('cmdk:', e); } }
  var GET = {
    LINKS:function(){ return typeof LINKS !== 'undefined' ? LINKS : []; },
    CATEGORIES:function(){ return typeof CATEGORIES !== 'undefined' ? CATEGORIES : []; },
    SUBS_CACHE:function(){ return typeof SUBS_CACHE !== 'undefined' ? SUBS_CACHE : []; },
    NODES_LIST:function(){ return typeof NODES_LIST !== 'undefined' ? NODES_LIST : []; },
    PROXIES_CACHE:function(){ return typeof PROXIES_CACHE !== 'undefined' ? PROXIES_CACHE : []; },
    ADMIN_CACHE:function(){ return typeof ADMIN_CACHE !== 'undefined' ? ADMIN_CACHE : []; }
  };
  function g(name){ try{ return GET[name]() || []; }catch(e){ return []; } }   // کش‌های سراسری صفحه

  function mk(type, key, title, sub, extra, act, o){
    o = o || {};
    return {
      type:type, key:type + ':' + key, title:String(title || '—'), sub:sub || '',
      t:nz(title), h:nz([title, sub, extra].join(' ')), icon:o.icon || TYPES[type].i,
      badge:o.badge || null, meta:o.meta || '', w:TYPES[type].w + (o.boost || 0), act:act
    };
  }

  /* ---------- index ---------- */
  function visibleTab(pg){
    var t = document.querySelector('.tab[data-pg="' + pg + '"]');
    return !!t && t.style.display !== 'none' && !t.hidden && !(t.closest && t.closest('[hidden]'));
  }
  function linkStatus(l){
    if(!l.active) return {c:'off', t:'غیرفعال', w:'غیرفعال disabled off'};
    if(l.expired) return {c:'bad', t:'منقضی', w:'منقضی expired'};
    if(Number(l.connected_ips || 0) > 0) return {c:'on', t:'آنلاین', w:'آنلاین online فعال active'};
    return {c:'idle', t:'آماده', w:'فعال active آماده'};
  }
  function build(){
    var out = [], seen = {};
    function add(it){ if(it && !seen[it.key]){ seen[it.key] = 1; out.push(it); } }

    PAGES.forEach(function(p){
      if(!visibleTab(p[0])) return;
      add(mk('page', p[0], p[1], 'رفتن به صفحه', p[2], function(){ gotoPage(p[0]); }, {icon:p[3]}));
    });

    // اقدام‌های سریع
    safe(function(){
      add(mk('action','new-inbound','ساخت اینباند جدید','WS + XHTTP در یک اشتراک','new create add inbound ساخت جدید افزودن',
        function(){ gotoPage('links'); openComboDrawer(); }, {icon:'ti-plus'}));
      add(mk('action','new-cat','دسته جدید','ساخت دسته‌بندی','new category دسته جدید',
        function(){ gotoPage('categories'); openCategoryDrawer(); }, {icon:'ti-plus'}));
      add(mk('action','new-sub','گروه ساب جدید','ساخت گروه اشتراک','new subscription گروه ساب جدید',
        function(){ gotoPage('subgroups'); openSubGroupDrawer(); }, {icon:'ti-plus'}));
      if(visibleTab('admins')) add(mk('action','new-admin','ادمین جدید','افزودن مدیر','new admin ادمین جدید',
        function(){ gotoPage('admins'); openAdminDrawer(); }, {icon:'ti-user-plus'}));
      add(mk('action','proxies','مدیریت پراکسی‌ها و اسکنر','اوتباند SOCKS / HTTP','proxy scanner outbound پراکسی اسکنر اوتباند خروجی',
        function(){ openOutboundManager(); }, {icon:'ti-route'}));
      add(mk('action','theme','تغییر پوسته (روشن / تیره)','','theme dark light dark-mode پوسته تم تاریک روشن',
        function(){ toggleTheme(); }, {icon:'ti-sun-moon'}));
      add(mk('action','refresh','بروزرسانی داده‌های صفحه','','refresh reload بروزرسانی ریفرش',
        function(){ gotoPage((typeof CURRENT_PAGE === 'string' && CURRENT_PAGE) || 'overview'); }, {icon:'ti-refresh'}));
    });

    // اینباند / کلاینت
    safe(function(){
      (g('LINKS') || []).forEach(function(l){
        if(!l || !l.uuid) return;
        var st = linkStatus(l), limit = Number(l.limit_bytes || 0), used = Number(l.used_bytes || 0);
        var addr = (l.address || location.hostname) + ':' + (l.port || 443);
        var proto = [l.protocol, l.network, l.security].filter(Boolean).join('/');
        var sub = [proto, addr, l.category_name].filter(Boolean).join(' · ');
        var extra = [l.uuid, l.address, l.port, l.protocol, l.network, l.security, l.category_name, st.w,
                     l.outbound && (l.outbound.country || l.outbound.name)].join(' ');
        var isC = !!l.is_client;
        add(mk(isC ? 'client' : 'inbound', l.uuid, l.label || 'Unnamed', sub, extra,
          (function(u){ return function(){ if(!isC) gotoPage('links'); openLinkDrawer(u, true); }; })(l.uuid),
          {badge:st, meta: limit > 0 ? Math.min(100, Math.round(used / limit * 100)) + '%' : ''}));
      });
    });
    safe(function(){
      (g('CATEGORIES') || []).forEach(function(c){
        add(mk('cat', c.id, c.name, 'دسته‌بندی', 'category دسته', (function(id){ return function(){ gotoPage('categories'); openCategoryDrawer(id); }; })(c.id)));
      });
      (g('SUBS_CACHE') || []).forEach(function(s){
        add(mk('sub', s.sub_id, s.name || '—', (s.local_count || 0) + ' اینباند', [s.sub_url, s.sub_id].join(' '),
          (function(id){ return function(){ gotoPage('subgroups'); openSubMembersDrawer(id); }; })(s.sub_id)));
      });
      (g('NODES_LIST') || []).forEach(function(n){
        var b = !n.enabled ? {c:'off', t:'غیرفعال'} : (n.status ? (n.status.online ? {c:'on', t:'آنلاین'} : {c:'bad', t:'آفلاین'}) : null);
        add(mk('node', n.id, n.name || n.id, n.url || 'نود', [n.url, n.id].join(' '),
          (function(id){ return function(){ gotoPage('nodes'); openNodeDrawer(id); }; })(n.id), {badge:b}));
      });
      (g('PROXIES_CACHE') || []).forEach(function(p){
        var ok = p.tested_at ? (p.test_ok ? {c:'on', t:p.ping_ms != null ? Math.round(p.ping_ms) + 'ms' : 'سالم'} : {c:'bad', t:'قطع'}) : null;
        add(mk('proxy', p.id, p.name || p.host, [(p.scheme || 'socks5').toUpperCase(), p.host + ':' + p.port, p.country].filter(Boolean).join(' · '),
          [p.host, p.port, p.country, p.city, p.isp, p.exit_ip, p.grade].join(' '),
          function(){ openOutboundManager(); }, {badge:ok}));
      });
      (g('ADMIN_CACHE') || []).forEach(function(a){
        add(mk('admin', a.id, a.username, a.role === 'owner' ? 'مالک پنل' : 'ادمین', [a.role, a.id].join(' '),
          (function(id, owner){ return function(){ gotoPage('admins'); if(!owner) editAdmin(id); }; })(a.id, a.role === 'owner')));
      });
    });

    // بخش‌های داخل صفحه‌ها (تنظیمات، گزارش‌ها، ...) از روی عنوان‌های DOM
    safe(function(){
      document.querySelectorAll('.page').forEach(function(pgEl){
        var pg = pgEl.id.replace(/^pg-/, '');
        if(!visibleTab(pg)) return;
        var pgName = (PAGES.filter(function(p){ return p[0] === pg; })[0] || [0, pg])[1];
        pgEl.querySelectorAll('.section-title, .panel-head b, .card > h3, .sec-title').forEach(function(el, idx){
          var t = (el.textContent || '').replace(/\s+/g, ' ').trim();
          if(t.length < 3 || t.length > 70) return;
          add(mk('section', pg + ':' + t, t, pgName, '', function(){
            gotoPage(pg);
            setTimeout(function(){
              if(!el.isConnected) return;
              var host = el.closest('.card') || el;
              host.scrollIntoView({block:'center', behavior:'smooth'});
              host.classList.remove('cmdk-flash'); void host.offsetWidth; host.classList.add('cmdk-flash');
              setTimeout(function(){ host.classList.remove('cmdk-flash'); }, 1800);
            }, 160);
          }));
        });
      });
    });
    return out;
  }

  /* ---------- search ---------- */
  function subseq(t, tok){
    var j = 0, gaps = 0, last = -1;
    for(var i = 0; i < t.length && j < tok.length; i++){
      if(t[i] === tok[j]){ if(last >= 0 && i - last > 1) gaps++; last = i; j++; }
    }
    return j === tok.length ? gaps : -1;
  }
  function score(it, toks){
    var s = 0;
    for(var k = 0; k < toks.length; k++){
      var t = toks[k], ti = it.t.indexOf(t);
      if(ti >= 0){ s += ti === 0 ? 100 : (it.t.charAt(ti - 1) === ' ' ? 80 : 55); continue; }
      var hi = it.h.indexOf(t);
      if(hi < 0) return -1;
      s += (hi === 0 || it.h.charAt(hi - 1) === ' ') ? 30 : 14;
    }
    return s + it.w - Math.min(it.t.length, 60) * 0.05;
  }
  function inFilter(it){
    var gset = GROUPS[filter]; return !gset || gset.indexOf(it.type) >= 0;
  }
  function recents(){ try{ return JSON.parse(lsGet('vw_cmdk_recent', '[]')) || []; }catch(e){ return []; } }
  function pushRecent(key){
    var r = recents().filter(function(k){ return k !== key; }); r.unshift(key);
    lsSet('vw_cmdk_recent', JSON.stringify(r.slice(0, 6)));
  }
  function search(q){
    var toks = tokens(q), pool = items.filter(inFilter), res = [];
    if(!toks.length){
      var byKey = {}; pool.forEach(function(it){ byKey[it.key] = it; });
      var seen = {}, out = [];
      recents().forEach(function(k){ if(byKey[k]){ out.push({it:byKey[k], grp:'اخیراً'}); seen[k] = 1; } });
      ['action','page'].forEach(function(ty){
        pool.filter(function(it){ return it.type === ty && !seen[it.key]; }).slice(0, ty === 'action' ? 6 : 12)
          .forEach(function(it){ out.push({it:it, grp:ty === 'action' ? 'اقدام‌های سریع' : 'صفحه‌ها'}); });
      });
      if(filter !== 'all' && filter !== 'action' && filter !== 'page'){
        out = pool.slice(0, 60).map(function(it){ return {it:it, grp:TYPES[it.type].l + '‌ها'}; });
      }
      return out;
    }
    pool.forEach(function(it){ var s = score(it, toks); if(s >= 0) res.push({it:it, s:s}); });
    if(!res.length && toks.length === 1 && toks[0].length >= 3){
      pool.forEach(function(it){ var gp = subseq(it.t, toks[0]); if(gp >= 0 && gp <= 3) res.push({it:it, s:5 - gp}); });
    }
    res.sort(function(a, b){ return b.s - a.s; });
    return res.slice(0, 60).map(function(r){ return {it:r.it, grp:''}; });
  }
  function hl(text, toks){
    var raw = String(text), n = nz(raw), marks = [];
    toks.forEach(function(t){ var i = n.indexOf(t); if(i >= 0) marks.push([i, i + t.length]); });
    if(!marks.length) return esc(raw);
    marks.sort(function(a, b){ return a[0] - b[0]; });
    var merged = [marks[0]];
    for(var i = 1; i < marks.length; i++){
      var l = merged[merged.length - 1];
      if(marks[i][0] <= l[1]) l[1] = Math.max(l[1], marks[i][1]); else merged.push(marks[i]);
    }
    var html = '', pos = 0;
    merged.forEach(function(m){ html += esc(raw.slice(pos, m[0])) + '<mark>' + esc(raw.slice(m[0], m[1])) + '</mark>'; pos = m[1]; });
    return html + esc(raw.slice(pos));
  }

  /* ---------- render ---------- */
  function render(){
    pending = false;
    var q = INP.value, toks = tokens(q);
    results = search(q);
    if(active >= results.length) active = Math.max(0, results.length - 1);
    var html = '', lastGrp = null;
    results.forEach(function(r, i){
      var it = r.it;
      if(r.grp && r.grp !== lastGrp){ html += '<div class="cmdk-grp">' + esc(r.grp) + '</div>'; lastGrp = r.grp; }
      html += '<div class="cmdk-it' + (i === active ? ' on' : '') + '" role="option" id="cmdk-o' + i + '" data-i="' + i + '" aria-selected="' + (i === active) + '">' +
        '<span class="cmdk-ic"><i class="ti ' + esc(it.icon) + '"></i></span>' +
        '<span class="cmdk-tx"><b>' + hl(it.title, toks) + '</b>' + (it.sub ? '<small>' + hl(it.sub, toks) + '</small>' : '') + '</span>' +
        (it.meta ? '<span class="cmdk-meta">' + esc(it.meta) + '</span>' : '') +
        (it.badge ? '<span class="cmdk-bd ' + esc(it.badge.c) + '">' + esc(it.badge.t) + '</span>' : '') +
        '<span class="cmdk-ty">' + esc(TYPES[it.type].l) + '</span></div>';
    });
    if(!results.length){
      html = '<div class="cmdk-empty"><i class="ti ti-search"></i><b>' + (toks.length ? 'نتیجه‌ای پیدا نشد' : 'چیزی برای نمایش نیست') + '</b>' +
        (toks.length ? '<small>املای دیگری امتحان کن یا فیلتر را روی «همه» بگذار.</small>' : '') + '</div>';
    }
    if(html !== rowsHtmlKey){ LIST.innerHTML = html; rowsHtmlKey = html; }
    INP.setAttribute('aria-activedescendant', results.length ? 'cmdk-o' + active : '');
    if(CNT) CNT.textContent = toks.length ? (results.length + ' نتیجه') : (items.length + ' مورد قابل جستجو');
  }
  function setActive(i, scroll){
    if(!results.length) return;
    i = (i + results.length) % results.length;
    var prev = LIST.querySelector('.cmdk-it.on'); if(prev){ prev.classList.remove('on'); prev.setAttribute('aria-selected', 'false'); }
    active = i;
    var el = document.getElementById('cmdk-o' + i);
    if(el){ el.classList.add('on'); el.setAttribute('aria-selected', 'true'); if(scroll) el.scrollIntoView({block:'nearest'}); }
    INP.setAttribute('aria-activedescendant', 'cmdk-o' + i);
    rowsHtmlKey = '';
  }
  function run(i){
    var r = results[i]; if(!r) return;
    pushRecent(r.it.key); api_close(true);
    setTimeout(function(){ safe(function(){ r.it.act(); }); }, 30);
  }

  /* ---------- data freshness (فقط چیزی که هنوز خالی است) ---------- */
  var tried = {};
  function ensureData(){
    if(fetching || typeof api !== 'function') return;
    var jobs = [], now = Date.now();
    function need(name){ var v = g(name); return (!v || !v.length) && now - (tried[name] || 0) > 20000; }
    function load(name, url, assign){ tried[name] = now; jobs.push(api(url).then(assign)); }
    if(need('LINKS')) load('LINKS', '/api/links', function(r){ LINKS = r.links || []; });
    if(need('CATEGORIES')) load('CATEGORIES', '/api/categories', function(r){ CATEGORIES = r.categories || []; });
    if(need('SUBS_CACHE')) load('SUBS_CACHE', '/api/subs', function(r){ SUBS_CACHE = r.subs || []; });
    if(need('NODES_LIST')) load('NODES_LIST', '/api/nodes', function(r){ NODES_LIST = r.nodes || []; });
    if(need('PROXIES_CACHE')) load('PROXIES_CACHE', '/api/proxies', function(r){ PROXIES_CACHE = r.proxies || []; });
    if(need('ADMIN_CACHE')) load('ADMIN_CACHE', '/api/admins', function(r){ ADMIN_CACHE = r.admins || []; });
    if(!jobs.length) return;
    fetching = true;
    Promise.all(jobs.map(function(p){ return p.catch(function(){}); })).then(function(){
      fetching = false;
      if(open){ items = build(); rowsHtmlKey = ''; render(); }
    });
  }

  /* ---------- open / close ---------- */
  function api_open(prefill){
    if(open) { INP.focus(); INP.select(); return; }
    open = true; lastFocus = document.activeElement;
    items = build(); active = 0; filter = 'all'; rowsHtmlKey = '';
    INP.value = prefill || '';
    setChips();
    OV.hidden = false; OV.setAttribute('aria-hidden', 'false');
    requestAnimationFrame(function(){ OV.classList.add('show'); });
    render();
    INP.focus();
    ensureData();
  }
  function api_close(noRestore){
    if(!open) return;
    open = false; OV.classList.remove('show'); OV.setAttribute('aria-hidden', 'true');
    setTimeout(function(){ if(!open) OV.hidden = true; }, 140);
    if(!noRestore && lastFocus && lastFocus.focus) safe(function(){ lastFocus.focus(); });
  }
  function setChips(){
    if(!CHIPS) return;
    CHIPS.querySelectorAll('button').forEach(function(b){ b.classList.toggle('on', b.dataset.f === filter); });
  }

  /* ---------- events ---------- */
  INP.addEventListener('input', function(){
    pending = true; clearTimeout(timer); timer = setTimeout(function(){ active = 0; render(); }, 60);
  });
  INP.addEventListener('keydown', function(e){
    if(e.isComposing) return;
    var k = e.key;
    if(k === 'ArrowDown'){ e.preventDefault(); setActive(active + 1, true); }
    else if(k === 'ArrowUp'){ e.preventDefault(); setActive(active - 1, true); }
    else if(k === 'PageDown'){ e.preventDefault(); setActive(Math.min(results.length - 1, active + 6), true); }
    else if(k === 'PageUp'){ e.preventDefault(); setActive(Math.max(0, active - 6), true); }
    else if(k === 'Home' && !INP.value){ e.preventDefault(); setActive(0, true); }
    else if(k === 'End' && !INP.value){ e.preventDefault(); setActive(results.length - 1, true); }
    else if(k === 'Enter'){ e.preventDefault(); if(pending){ clearTimeout(timer); active = 0; render(); } run(active); }
    else if(k === 'Tab'){
      e.preventDefault();
      var keys = Object.keys(GROUPS), i = keys.indexOf(filter);
      filter = keys[(i + (e.shiftKey ? -1 : 1) + keys.length) % keys.length]; active = 0; setChips(); render();
    }
  });
  LIST.addEventListener('mousemove', function(e){
    var el = e.target.closest ? e.target.closest('.cmdk-it') : null;
    if(el && Number(el.dataset.i) !== active) setActive(Number(el.dataset.i), false);
  });
  LIST.addEventListener('click', function(e){
    var el = e.target.closest ? e.target.closest('.cmdk-it') : null; if(el) run(Number(el.dataset.i));
  });
  if(CHIPS) CHIPS.addEventListener('click', function(e){
    var b = e.target.closest ? e.target.closest('button') : null; if(!b) return;
    filter = b.dataset.f; active = 0; setChips(); render(); INP.focus();
  });
  OV.addEventListener('mousedown', function(e){ if(e.target === OV) api_close(); });
  var closeBtn = document.getElementById('cmdkClose'); if(closeBtn) closeBtn.addEventListener('click', function(){ api_close(); });

  function typing(el){
    if(!el) return false;
    var tag = (el.tagName || '').toLowerCase();
    return tag === 'input' || tag === 'textarea' || tag === 'select' || el.isContentEditable;
  }
  document.addEventListener('keydown', function(e){
    var k = (e.key || '').toLowerCase();
    if((e.ctrlKey || e.metaKey) && !e.altKey && !e.shiftKey && k === 'k'){
      e.preventDefault(); open ? api_close() : api_open(); return;
    }
    if(!open && k === '/' && !e.ctrlKey && !e.metaKey && !e.altKey && !typing(e.target)){
      e.preventDefault(); api_open(); return;
    }
    if(open && k === 'escape'){ e.preventDefault(); e.stopImmediatePropagation(); api_close(); }
  }, true);

  window.cmdkOpen = api_open;
  window.cmdkClose = api_close;
  window.__cmdk = {nz:nz, tokens:tokens, build:function(){ return build(); }, search:function(q, f){ items = build(); filter = f || 'all'; return search(q).map(function(r){ return r.it; }); }, score:score};
})();
</script>
</body>
</html>
"""


# ============================================================
# LOCAL ASSETS (no CDN needed: works even when jsdelivr/google are blocked)
# ============================================================
ASSET_ICONS_B64 = "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"
ASSET_VAZIR_B64 = "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"
UI_CSS = r""":root{--accent-rgb:139,92,246}
@font-face{font-family:'tabler-icons';src:url(/assets/icons.woff2) format('woff2');font-weight:normal;font-style:normal;font-display:block}
@font-face{font-family:'Vazirmatn';src:url(/assets/vazir.woff2) format('woff2');font-weight:100 900;font-style:normal;font-display:swap}
.ti{font-family:'tabler-icons'!important;speak:none;font-style:normal;font-weight:normal;font-variant:normal;text-transform:none;line-height:1;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;display:inline-block}
.ti-activity:before{content:"\ed23"}
.ti-activity-heartbeat:before{content:"\f0db"}
.ti-adjustments-horizontal:before{content:"\ec38"}
.ti-alert-circle:before{content:"\ea05"}
.ti-alert-triangle:before{content:"\ea06"}
.ti-antenna-bars-5:before{content:"\eccb"}
.ti-api:before{content:"\effd"}
.ti-apps:before{content:"\ebb6"}
.ti-arrow-back-up:before{content:"\eb77"}
.ti-arrow-down:before{content:"\ea16"}
.ti-arrow-left:before{content:"\ea19"}
.ti-arrow-right:before{content:"\ea1f"}
.ti-arrow-up:before{content:"\ea25"}
.ti-arrows-exchange:before{content:"\f1f4"}
.ti-arrows-right-left:before{content:"\edb2"}
.ti-badge:before{content:"\efc2"}
.ti-ban:before{content:"\ea2e"}
.ti-bell-ringing:before{content:"\ed07"}
.ti-bolt:before{content:"\ea38"}
.ti-box:before{content:"\ea45"}
.ti-brand-android:before{content:"\ec16"}
.ti-brand-apple:before{content:"\ec17"}
.ti-brand-telegram:before{content:"\ec26"}
.ti-brand-vscode:before{content:"\f3a0"}
.ti-brand-xamarin:before{content:"\fa7a"}
.ti-browser:before{content:"\ebb7"}
.ti-calendar:before{content:"\ea53"}
.ti-calendar-due:before{content:"\f621"}
.ti-calendar-time:before{content:"\ee21"}
.ti-cancel:before{content:"\ff11"}
.ti-category:before{content:"\f1f6"}
.ti-chart-bar:before{content:"\ea59"}
.ti-chart-histogram:before{content:"\f65c"}
.ti-check:before{content:"\ea5e"}
.ti-checkbox:before{content:"\eba6"}
.ti-checks:before{content:"\ebaa"}
.ti-chevron-down:before{content:"\ea5f"}
.ti-chevron-left:before{content:"\ea60"}
.ti-chevron-right:before{content:"\ea61"}
.ti-circle-check:before{content:"\ea67"}
.ti-circle-filled:before{content:"\f671"}
.ti-circle-x:before{content:"\ea6a"}
.ti-click:before{content:"\ebbc"}
.ti-clipboard-text:before{content:"\f089"}
.ti-clock:before{content:"\ea70"}
.ti-cloud:before{content:"\ea76"}
.ti-cookie:before{content:"\fdb1"}
.ti-copy:before{content:"\ea7a"}
.ti-copy-check:before{content:"\fdb0"}
.ti-cpu:before{content:"\ef8e"}
.ti-crown:before{content:"\ed12"}
.ti-dashboard:before{content:"\ea87"}
.ti-database:before{content:"\ea88"}
.ti-details:before{content:"\ee71"}
.ti-device-desktop:before{content:"\ea89"}
.ti-device-floppy:before{content:"\eb62"}
.ti-device-laptop:before{content:"\eb64"}
.ti-device-mobile:before{content:"\ea8a"}
.ti-dice-5:before{content:"\f08f"}
.ti-disabled:before{content:"\ea8f"}
.ti-download:before{content:"\ea96"}
.ti-edit:before{content:"\ea98"}
.ti-external-link:before{content:"\ea99"}
.ti-eye:before{content:"\ea9a"}
.ti-eye-off:before{content:"\ecf0"}
.ti-fingerprint:before{content:"\ebd1"}
.ti-flag:before{content:"\eaa6"}
.ti-flame:before{content:"\ec2c"}
.ti-folders:before{content:"\eaae"}
.ti-function:before{content:"\f225"}
.ti-gauge:before{content:"\eab1"}
.ti-headset:before{content:"\eb90"}
.ti-heart-filled:before{content:"\f67c"}
.ti-heartbeat:before{content:"\ef92"}
.ti-history:before{content:"\ebea"}
.ti-home:before{content:"\eac1"}
.ti-hourglass:before{content:"\ef93"}
.ti-id:before{content:"\eac3"}
.ti-inbox:before{content:"\eac4"}
.ti-infinity:before{content:"\eb69"}
.ti-info-circle:before{content:"\eac5"}
.ti-key:before{content:"\eac7"}
.ti-label:before{content:"\ff38"}
.ti-layout:before{content:"\eadb"}
.ti-layout-dashboard:before{content:"\f02c"}
.ti-leaf:before{content:"\ed4f"}
.ti-line:before{content:"\ec40"}
.ti-link:before{content:"\eade"}
.ti-loader-2:before{content:"\f226"}
.ti-lock:before{content:"\eae2"}
.ti-lock-open:before{content:"\eae1"}
.ti-login-2:before{content:"\fc76"}
.ti-logout:before{content:"\eba8"}
.ti-logs:before{content:"\fea7"}
.ti-menu-2:before{content:"\ec42"}
.ti-message:before{content:"\eaef"}
.ti-messages:before{content:"\eb6c"}
.ti-minus:before{content:"\eaf2"}
.ti-moon:before{content:"\eaf8"}
.ti-network:before{content:"\f09f"}
.ti-news:before{content:"\eafd"}
.ti-note:before{content:"\eb6d"}
.ti-number:before{content:"\f1fe"}
.ti-outbound:before{content:"\f249"}
.ti-palette:before{content:"\eb01"}
.ti-password:before{content:"\f4ca"}
.ti-pencil:before{content:"\eb04"}
.ti-pill:before{content:"\ec44"}
.ti-placeholder:before{content:"\f626"}
.ti-player-pause:before{content:"\ed45"}
.ti-player-play:before{content:"\ed46"}
.ti-player-stop:before{content:"\ed4a"}
.ti-plug-connected:before{content:"\f00a"}
.ti-plus:before{content:"\eb0b"}
.ti-power:before{content:"\eb0d"}
.ti-protocol:before{content:"\fd81"}
.ti-qrcode:before{content:"\eb11"}
.ti-radar-2:before{content:"\f016"}
.ti-radio:before{content:"\ef2d"}
.ti-refresh:before{content:"\eb13"}
.ti-reload:before{content:"\f3ae"}
.ti-replace:before{content:"\ebc7"}
.ti-rocket:before{content:"\ec45"}
.ti-route:before{content:"\eb17"}
.ti-router:before{content:"\eb18"}
.ti-rss:before{content:"\eb19"}
.ti-scan:before{content:"\ebc8"}
.ti-search:before{content:"\eb1c"}
.ti-send:before{content:"\eb1e"}
.ti-server:before{content:"\eb1f"}
.ti-server-2:before{content:"\f07c"}
.ti-server-cog:before{content:"\f321"}
.ti-settings:before{content:"\eb20"}
.ti-share:before{content:"\eb21"}
.ti-shield:before{content:"\eb24"}
.ti-shield-bolt:before{content:"\f9c0"}
.ti-shield-check:before{content:"\eb22"}
.ti-shield-lock:before{content:"\ed58"}
.ti-shield-star:before{content:"\f9cf"}
.ti-sparkles:before{content:"\f6d7"}
.ti-speakerphone:before{content:"\ed61"}
.ti-stack:before{content:"\eb2d"}
.ti-stack-2:before{content:"\eef7"}
.ti-star:before{content:"\eb2e"}
.ti-stars:before{content:"\ed38"}
.ti-sum:before{content:"\eb73"}
.ti-sun:before{content:"\eb30"}
.ti-sun-moon:before{content:"\f4a3"}
.ti-switch:before{content:"\eb33"}
.ti-tag:before{content:"\eb34"}
.ti-toggle-right:before{content:"\eb3f"}
.ti-transfer:before{content:"\fc1f"}
.ti-trash:before{content:"\eb41"}
.ti-trending-up:before{content:"\eb43"}
.ti-user:before{content:"\eb4d"}
.ti-user-edit:before{content:"\f7cc"}
.ti-user-plus:before{content:"\eb4b"}
.ti-user-shield:before{content:"\f7d0"}
.ti-users:before{content:"\ebf2"}
.ti-users-group:before{content:"\fa21"}
.ti-wand:before{content:"\ebcb"}
.ti-world:before{content:"\eb54"}
.ti-x:before{content:"\eb55"}
.ti-brand-shield:before{content:"\eb24"}
.ti-device-ram:before{content:"\ef8e"}
.ti-world-copy:before{content:"\eb54"}
"""

ASSET_QR_JS_B64 = "dmFyIHFyY29kZT1mdW5jdGlvbigpe3ZhciB0PWZ1bmN0aW9uKHQscil7dmFyIGU9dCxuPWdbcl0sbz1udWxsLGk9MCxhPW51bGwsdT1bXSxmPXt9LGM9ZnVuY3Rpb24odCxyKXtvPWZ1bmN0aW9uKHQpe2Zvcih2YXIgcj1uZXcgQXJyYXkodCksZT0wO2U8dDtlKz0xKXtyW2VdPW5ldyBBcnJheSh0KTtmb3IodmFyIG49MDtuPHQ7bis9MSlyW2VdW25dPW51bGx9cmV0dXJuIHJ9KGk9NCplKzE3KSxsKDAsMCksbChpLTcsMCksbCgwLGktNykscygpLGgoKSxkKHQsciksZT49NyYmdih0KSxudWxsPT1hJiYoYT1wKGUsbix1KSksdyhhLHIpfSxsPWZ1bmN0aW9uKHQscil7Zm9yKHZhciBlPS0xO2U8PTc7ZSs9MSlpZighKHQrZTw9LTF8fGk8PXQrZSkpZm9yKHZhciBuPS0xO248PTc7bis9MSlyK248PS0xfHxpPD1yK258fChvW3QrZV1bcituXT0wPD1lJiZlPD02JiYoMD09bnx8Nj09bil8fDA8PW4mJm48PTYmJigwPT1lfHw2PT1lKXx8Mjw9ZSYmZTw9NCYmMjw9biYmbjw9NCl9LGg9ZnVuY3Rpb24oKXtmb3IodmFyIHQ9ODt0PGktODt0Kz0xKW51bGw9PW9bdF1bNl0mJihvW3RdWzZdPXQlMj09MCk7Zm9yKHZhciByPTg7cjxpLTg7cis9MSludWxsPT1vWzZdW3JdJiYob1s2XVtyXT1yJTI9PTApfSxzPWZ1bmN0aW9uKCl7Zm9yKHZhciB0PUIuZ2V0UGF0dGVyblBvc2l0aW9uKGUpLHI9MDtyPHQubGVuZ3RoO3IrPTEpZm9yKHZhciBuPTA7bjx0Lmxlbmd0aDtuKz0xKXt2YXIgaT10W3JdLGE9dFtuXTtpZihudWxsPT1vW2ldW2FdKWZvcih2YXIgdT0tMjt1PD0yO3UrPTEpZm9yKHZhciBmPS0yO2Y8PTI7Zis9MSlvW2krdV1bYStmXT0tMj09dXx8Mj09dXx8LTI9PWZ8fDI9PWZ8fDA9PXUmJjA9PWZ9fSx2PWZ1bmN0aW9uKHQpe2Zvcih2YXIgcj1CLmdldEJDSFR5cGVOdW1iZXIoZSksbj0wO248MTg7bis9MSl7dmFyIGE9IXQmJjE9PShyPj5uJjEpO29bTWF0aC5mbG9vcihuLzMpXVtuJTMraS04LTNdPWF9Zm9yKG49MDtuPDE4O24rPTEpe2E9IXQmJjE9PShyPj5uJjEpO29bbiUzK2ktOC0zXVtNYXRoLmZsb29yKG4vMyldPWF9fSxkPWZ1bmN0aW9uKHQscil7Zm9yKHZhciBlPW48PDN8cixhPUIuZ2V0QkNIVHlwZUluZm8oZSksdT0wO3U8MTU7dSs9MSl7dmFyIGY9IXQmJjE9PShhPj51JjEpO3U8Nj9vW3VdWzhdPWY6dTw4P29bdSsxXVs4XT1mOm9baS0xNSt1XVs4XT1mfWZvcih1PTA7dTwxNTt1Kz0xKXtmPSF0JiYxPT0oYT4+dSYxKTt1PDg/b1s4XVtpLXUtMV09Zjp1PDk/b1s4XVsxNS11LTErMV09ZjpvWzhdWzE1LXUtMV09Zn1vW2ktOF1bOF09IXR9LHc9ZnVuY3Rpb24odCxyKXtmb3IodmFyIGU9LTEsbj1pLTEsYT03LHU9MCxmPUIuZ2V0TWFza0Z1bmN0aW9uKHIpLGM9aS0xO2M+MDtjLT0yKWZvcig2PT1jJiYoYy09MSk7Oyl7Zm9yKHZhciBnPTA7ZzwyO2crPTEpaWYobnVsbD09b1tuXVtjLWddKXt2YXIgbD0hMTt1PHQubGVuZ3RoJiYobD0xPT0odFt1XT4+PmEmMSkpLGYobixjLWcpJiYobD0hbCksb1tuXVtjLWddPWwsLTE9PShhLT0xKSYmKHUrPTEsYT03KX1pZigobis9ZSk8MHx8aTw9bil7bi09ZSxlPS1lO2JyZWFrfX19LHA9ZnVuY3Rpb24odCxyLGUpe2Zvcih2YXIgbj1BLmdldFJTQmxvY2tzKHQsciksbz1iKCksaT0wO2k8ZS5sZW5ndGg7aSs9MSl7dmFyIGE9ZVtpXTtvLnB1dChhLmdldE1vZGUoKSw0KSxvLnB1dChhLmdldExlbmd0aCgpLEIuZ2V0TGVuZ3RoSW5CaXRzKGEuZ2V0TW9kZSgpLHQpKSxhLndyaXRlKG8pfXZhciB1PTA7Zm9yKGk9MDtpPG4ubGVuZ3RoO2krPTEpdSs9bltpXS5kYXRhQ291bnQ7aWYoby5nZXRMZW5ndGhJbkJpdHMoKT44KnUpdGhyb3ciY29kZSBsZW5ndGggb3ZlcmZsb3cuICgiK28uZ2V0TGVuZ3RoSW5CaXRzKCkrIj4iKzgqdSsiKSI7Zm9yKG8uZ2V0TGVuZ3RoSW5CaXRzKCkrNDw9OCp1JiZvLnB1dCgwLDQpO28uZ2V0TGVuZ3RoSW5CaXRzKCklOCE9MDspby5wdXRCaXQoITEpO2Zvcig7IShvLmdldExlbmd0aEluQml0cygpPj04KnV8fChvLnB1dCgyMzYsOCksby5nZXRMZW5ndGhJbkJpdHMoKT49OCp1KSk7KW8ucHV0KDE3LDgpO3JldHVybiBmdW5jdGlvbih0LHIpe2Zvcih2YXIgZT0wLG49MCxvPTAsaT1uZXcgQXJyYXkoci5sZW5ndGgpLGE9bmV3IEFycmF5KHIubGVuZ3RoKSx1PTA7dTxyLmxlbmd0aDt1Kz0xKXt2YXIgZj1yW3VdLmRhdGFDb3VudCxjPXJbdV0udG90YWxDb3VudC1mO249TWF0aC5tYXgobixmKSxvPU1hdGgubWF4KG8sYyksaVt1XT1uZXcgQXJyYXkoZik7Zm9yKHZhciBnPTA7ZzxpW3VdLmxlbmd0aDtnKz0xKWlbdV1bZ109MjU1JnQuZ2V0QnVmZmVyKClbZytlXTtlKz1mO3ZhciBsPUIuZ2V0RXJyb3JDb3JyZWN0UG9seW5vbWlhbChjKSxoPWsoaVt1XSxsLmdldExlbmd0aCgpLTEpLm1vZChsKTtmb3IoYVt1XT1uZXcgQXJyYXkobC5nZXRMZW5ndGgoKS0xKSxnPTA7ZzxhW3VdLmxlbmd0aDtnKz0xKXt2YXIgcz1nK2guZ2V0TGVuZ3RoKCktYVt1XS5sZW5ndGg7YVt1XVtnXT1zPj0wP2guZ2V0QXQocyk6MH19dmFyIHY9MDtmb3IoZz0wO2c8ci5sZW5ndGg7Zys9MSl2Kz1yW2ddLnRvdGFsQ291bnQ7dmFyIGQ9bmV3IEFycmF5KHYpLHc9MDtmb3IoZz0wO2c8bjtnKz0xKWZvcih1PTA7dTxyLmxlbmd0aDt1Kz0xKWc8aVt1XS5sZW5ndGgmJihkW3ddPWlbdV1bZ10sdys9MSk7Zm9yKGc9MDtnPG87Zys9MSlmb3IodT0wO3U8ci5sZW5ndGg7dSs9MSlnPGFbdV0ubGVuZ3RoJiYoZFt3XT1hW3VdW2ddLHcrPTEpO3JldHVybiBkfShvLG4pfTtmLmFkZERhdGE9ZnVuY3Rpb24odCxyKXt2YXIgZT1udWxsO3N3aXRjaChyPXJ8fCJCeXRlIil7Y2FzZSJOdW1lcmljIjplPU0odCk7YnJlYWs7Y2FzZSJBbHBoYW51bWVyaWMiOmU9eCh0KTticmVhaztjYXNlIkJ5dGUiOmU9bSh0KTticmVhaztjYXNlIkthbmppIjplPUwodCk7YnJlYWs7ZGVmYXVsdDp0aHJvdyJtb2RlOiIrcn11LnB1c2goZSksYT1udWxsfSxmLmlzRGFyaz1mdW5jdGlvbih0LHIpe2lmKHQ8MHx8aTw9dHx8cjwwfHxpPD1yKXRocm93IHQrIiwiK3I7cmV0dXJuIG9bdF1bcl19LGYuZ2V0TW9kdWxlQ291bnQ9ZnVuY3Rpb24oKXtyZXR1cm4gaX0sZi5tYWtlPWZ1bmN0aW9uKCl7aWYoZTwxKXtmb3IodmFyIHQ9MTt0PDQwO3QrKyl7Zm9yKHZhciByPUEuZ2V0UlNCbG9ja3ModCxuKSxvPWIoKSxpPTA7aTx1Lmxlbmd0aDtpKyspe3ZhciBhPXVbaV07by5wdXQoYS5nZXRNb2RlKCksNCksby5wdXQoYS5nZXRMZW5ndGgoKSxCLmdldExlbmd0aEluQml0cyhhLmdldE1vZGUoKSx0KSksYS53cml0ZShvKX12YXIgZz0wO2ZvcihpPTA7aTxyLmxlbmd0aDtpKyspZys9cltpXS5kYXRhQ291bnQ7aWYoby5nZXRMZW5ndGhJbkJpdHMoKTw9OCpnKWJyZWFrfWU9dH1jKCExLGZ1bmN0aW9uKCl7Zm9yKHZhciB0PTAscj0wLGU9MDtlPDg7ZSs9MSl7YyghMCxlKTt2YXIgbj1CLmdldExvc3RQb2ludChmKTsoMD09ZXx8dD5uKSYmKHQ9bixyPWUpfXJldHVybiByfSgpKX0sZi5jcmVhdGVUYWJsZVRhZz1mdW5jdGlvbih0LHIpe3Q9dHx8Mjt2YXIgZT0iIjtlKz0nPHRhYmxlIHN0eWxlPSInLGUrPSIgYm9yZGVyLXdpZHRoOiAwcHg7IGJvcmRlci1zdHlsZTogbm9uZTsiLGUrPSIgYm9yZGVyLWNvbGxhcHNlOiBjb2xsYXBzZTsiLGUrPSIgcGFkZGluZzogMHB4OyBtYXJnaW46ICIrKHI9dm9pZCAwPT09cj80KnQ6cikrInB4OyIsZSs9JyI+JyxlKz0iPHRib2R5PiI7Zm9yKHZhciBuPTA7bjxmLmdldE1vZHVsZUNvdW50KCk7bis9MSl7ZSs9Ijx0cj4iO2Zvcih2YXIgbz0wO288Zi5nZXRNb2R1bGVDb3VudCgpO28rPTEpZSs9Jzx0ZCBzdHlsZT0iJyxlKz0iIGJvcmRlci13aWR0aDogMHB4OyBib3JkZXItc3R5bGU6IG5vbmU7IixlKz0iIGJvcmRlci1jb2xsYXBzZTogY29sbGFwc2U7IixlKz0iIHBhZGRpbmc6IDBweDsgbWFyZ2luOiAwcHg7IixlKz0iIHdpZHRoOiAiK3QrInB4OyIsZSs9IiBoZWlnaHQ6ICIrdCsicHg7IixlKz0iIGJhY2tncm91bmQtY29sb3I6ICIsZSs9Zi5pc0RhcmsobixvKT8iIzAwMDAwMCI6IiNmZmZmZmYiLGUrPSI7IixlKz0nIi8+JztlKz0iPC90cj4ifXJldHVybiBlKz0iPC90Ym9keT4iLGUrPSI8L3RhYmxlPiJ9LGYuY3JlYXRlU3ZnVGFnPWZ1bmN0aW9uKHQscixlLG4pe3ZhciBvPXt9OyJvYmplY3QiPT10eXBlb2YgYXJndW1lbnRzWzBdJiYodD0obz1hcmd1bWVudHNbMF0pLmNlbGxTaXplLHI9by5tYXJnaW4sZT1vLmFsdCxuPW8udGl0bGUpLHQ9dHx8MixyPXZvaWQgMD09PXI/NCp0OnIsKGU9InN0cmluZyI9PXR5cGVvZiBlP3t0ZXh0OmV9OmV8fHt9KS50ZXh0PWUudGV4dHx8bnVsbCxlLmlkPWUudGV4dD9lLmlkfHwicXJjb2RlLWRlc2NyaXB0aW9uIjpudWxsLChuPSJzdHJpbmciPT10eXBlb2Ygbj97dGV4dDpufTpufHx7fSkudGV4dD1uLnRleHR8fG51bGwsbi5pZD1uLnRleHQ/bi5pZHx8InFyY29kZS10aXRsZSI6bnVsbDt2YXIgaSxhLHUsYyxnPWYuZ2V0TW9kdWxlQ291bnQoKSp0KzIqcixsPSIiO2ZvcihjPSJsIit0KyIsMCAwLCIrdCsiIC0iK3QrIiwwIDAsLSIrdCsieiAiLGwrPSc8c3ZnIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIicsbCs9by5zY2FsYWJsZT8iIjonIHdpZHRoPSInK2crJ3B4IiBoZWlnaHQ9IicrZysncHgiJyxsKz0nIHZpZXdCb3g9IjAgMCAnK2crIiAiK2crJyIgJyxsKz0nIHByZXNlcnZlQXNwZWN0UmF0aW89InhNaW5ZTWluIG1lZXQiJyxsKz1uLnRleHR8fGUudGV4dD8nIHJvbGU9ImltZyIgYXJpYS1sYWJlbGxlZGJ5PSInK3koW24uaWQsZS5pZF0uam9pbigiICIpLnRyaW0oKSkrJyInOiIiLGwrPSI+IixsKz1uLnRleHQ/Jzx0aXRsZSBpZD0iJyt5KG4uaWQpKyciPicreShuLnRleHQpKyI8L3RpdGxlPiI6IiIsbCs9ZS50ZXh0Pyc8ZGVzY3JpcHRpb24gaWQ9IicreShlLmlkKSsnIj4nK3koZS50ZXh0KSsiPC9kZXNjcmlwdGlvbj4iOiIiLGwrPSc8cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ3aGl0ZSIgY3g9IjAiIGN5PSIwIi8+JyxsKz0nPHBhdGggZD0iJyxhPTA7YTxmLmdldE1vZHVsZUNvdW50KCk7YSs9MSlmb3IodT1hKnQrcixpPTA7aTxmLmdldE1vZHVsZUNvdW50KCk7aSs9MSlmLmlzRGFyayhhLGkpJiYobCs9Ik0iKyhpKnQrcikrIiwiK3UrYyk7cmV0dXJuIGwrPSciIHN0cm9rZT0idHJhbnNwYXJlbnQiIGZpbGw9ImJsYWNrIi8+JyxsKz0iPC9zdmc+In0sZi5jcmVhdGVEYXRhVVJMPWZ1bmN0aW9uKHQscil7dD10fHwyLHI9dm9pZCAwPT09cj80KnQ6cjt2YXIgZT1mLmdldE1vZHVsZUNvdW50KCkqdCsyKnIsbj1yLG89ZS1yO3JldHVybiBJKGUsZSxmdW5jdGlvbihyLGUpe2lmKG48PXImJnI8byYmbjw9ZSYmZTxvKXt2YXIgaT1NYXRoLmZsb29yKChyLW4pL3QpLGE9TWF0aC5mbG9vcigoZS1uKS90KTtyZXR1cm4gZi5pc0RhcmsoYSxpKT8wOjF9cmV0dXJuIDF9KX0sZi5jcmVhdGVJbWdUYWc9ZnVuY3Rpb24odCxyLGUpe3Q9dHx8MixyPXZvaWQgMD09PXI/NCp0OnI7dmFyIG49Zi5nZXRNb2R1bGVDb3VudCgpKnQrMipyLG89IiI7cmV0dXJuIG8rPSI8aW1nIixvKz0nIHNyYz0iJyxvKz1mLmNyZWF0ZURhdGFVUkwodCxyKSxvKz0nIicsbys9JyB3aWR0aD0iJyxvKz1uLG8rPSciJyxvKz0nIGhlaWdodD0iJyxvKz1uLG8rPSciJyxlJiYobys9JyBhbHQ9Iicsbys9eShlKSxvKz0nIicpLG8rPSIvPiJ9O3ZhciB5PWZ1bmN0aW9uKHQpe2Zvcih2YXIgcj0iIixlPTA7ZTx0Lmxlbmd0aDtlKz0xKXt2YXIgbj10LmNoYXJBdChlKTtzd2l0Y2gobil7Y2FzZSI8IjpyKz0iJmx0OyI7YnJlYWs7Y2FzZSI+IjpyKz0iJmd0OyI7YnJlYWs7Y2FzZSImIjpyKz0iJmFtcDsiO2JyZWFrO2Nhc2UnIic6cis9IiZxdW90OyI7YnJlYWs7ZGVmYXVsdDpyKz1ufX1yZXR1cm4gcn07cmV0dXJuIGYuY3JlYXRlQVNDSUk9ZnVuY3Rpb24odCxyKXtpZigodD10fHwxKTwyKXJldHVybiBmdW5jdGlvbih0KXt0PXZvaWQgMD09PXQ/Mjp0O3ZhciByLGUsbixvLGksYT0xKmYuZ2V0TW9kdWxlQ291bnQoKSsyKnQsdT10LGM9YS10LGc9eyLilojilogiOiLilogiLCLiloggIjoi4paAIiwiIOKWiCI6IuKWhCIsIiAgIjoiICJ9LGw9eyLilojilogiOiLiloAiLCLiloggIjoi4paAIiwiIOKWiCI6IiAiLCIgICI6IiAifSxoPSIiO2ZvcihyPTA7cjxhO3IrPTIpe2ZvcihuPU1hdGguZmxvb3IoKHItdSkvMSksbz1NYXRoLmZsb29yKChyKzEtdSkvMSksZT0wO2U8YTtlKz0xKWk9IuKWiCIsdTw9ZSYmZTxjJiZ1PD1yJiZyPGMmJmYuaXNEYXJrKG4sTWF0aC5mbG9vcigoZS11KS8xKSkmJihpPSIgIiksdTw9ZSYmZTxjJiZ1PD1yKzEmJnIrMTxjJiZmLmlzRGFyayhvLE1hdGguZmxvb3IoKGUtdSkvMSkpP2krPSIgIjppKz0i4paIIixoKz10PDEmJnIrMT49Yz9sW2ldOmdbaV07aCs9IlxuIn1yZXR1cm4gYSUyJiZ0PjA/aC5zdWJzdHJpbmcoMCxoLmxlbmd0aC1hLTEpK0FycmF5KGErMSkuam9pbigi4paAIik6aC5zdWJzdHJpbmcoMCxoLmxlbmd0aC0xKX0ocik7dC09MSxyPXZvaWQgMD09PXI/Mip0OnI7dmFyIGUsbixvLGksYT1mLmdldE1vZHVsZUNvdW50KCkqdCsyKnIsdT1yLGM9YS1yLGc9QXJyYXkodCsxKS5qb2luKCLilojilogiKSxsPUFycmF5KHQrMSkuam9pbigiICAiKSxoPSIiLHM9IiI7Zm9yKGU9MDtlPGE7ZSs9MSl7Zm9yKG89TWF0aC5mbG9vcigoZS11KS90KSxzPSIiLG49MDtuPGE7bis9MSlpPTEsdTw9biYmbjxjJiZ1PD1lJiZlPGMmJmYuaXNEYXJrKG8sTWF0aC5mbG9vcigobi11KS90KSkmJihpPTApLHMrPWk/ZzpsO2ZvcihvPTA7bzx0O28rPTEpaCs9cysiXG4ifXJldHVybiBoLnN1YnN0cmluZygwLGgubGVuZ3RoLTEpfSxmLnJlbmRlclRvMmRDb250ZXh0PWZ1bmN0aW9uKHQscil7cj1yfHwyO2Zvcih2YXIgZT1mLmdldE1vZHVsZUNvdW50KCksbj0wO248ZTtuKyspZm9yKHZhciBvPTA7bzxlO28rKyl0LmZpbGxTdHlsZT1mLmlzRGFyayhuLG8pPyJibGFjayI6IndoaXRlIix0LmZpbGxSZWN0KG4qcixvKnIscixyKX0sZn07dC5zdHJpbmdUb0J5dGVzPSh0LnN0cmluZ1RvQnl0ZXNGdW5jcz17ZGVmYXVsdDpmdW5jdGlvbih0KXtmb3IodmFyIHI9W10sZT0wO2U8dC5sZW5ndGg7ZSs9MSl7dmFyIG49dC5jaGFyQ29kZUF0KGUpO3IucHVzaCgyNTUmbil9cmV0dXJuIHJ9fSkuZGVmYXVsdCx0LmNyZWF0ZVN0cmluZ1RvQnl0ZXM9ZnVuY3Rpb24odCxyKXt2YXIgZT1mdW5jdGlvbigpe2Zvcih2YXIgZT1TKHQpLG49ZnVuY3Rpb24oKXt2YXIgdD1lLnJlYWQoKTtpZigtMT09dCl0aHJvdyJlb2YiO3JldHVybiB0fSxvPTAsaT17fTs7KXt2YXIgYT1lLnJlYWQoKTtpZigtMT09YSlicmVhazt2YXIgdT1uKCksZj1uKCk8PDh8bigpO2lbU3RyaW5nLmZyb21DaGFyQ29kZShhPDw4fHUpXT1mLG8rPTF9aWYobyE9cil0aHJvdyBvKyIgIT0gIityO3JldHVybiBpfSgpLG49Ij8iLmNoYXJDb2RlQXQoMCk7cmV0dXJuIGZ1bmN0aW9uKHQpe2Zvcih2YXIgcj1bXSxvPTA7bzx0Lmxlbmd0aDtvKz0xKXt2YXIgaT10LmNoYXJDb2RlQXQobyk7aWYoaTwxMjgpci5wdXNoKGkpO2Vsc2V7dmFyIGE9ZVt0LmNoYXJBdChvKV07Im51bWJlciI9PXR5cGVvZiBhPygyNTUmYSk9PWE/ci5wdXNoKGEpOihyLnB1c2goYT4+PjgpLHIucHVzaCgyNTUmYSkpOnIucHVzaChuKX19cmV0dXJuIHJ9fTt2YXIgcixlLG4sbyxpLGE9MSx1PTIsZj00LGM9OCxnPXtMOjEsTTowLFE6MyxIOjJ9LGw9MCxoPTEscz0yLHY9MyxkPTQsdz01LHA9Nix5PTcsQj0ocj1bW10sWzYsMThdLFs2LDIyXSxbNiwyNl0sWzYsMzBdLFs2LDM0XSxbNiwyMiwzOF0sWzYsMjQsNDJdLFs2LDI2LDQ2XSxbNiwyOCw1MF0sWzYsMzAsNTRdLFs2LDMyLDU4XSxbNiwzNCw2Ml0sWzYsMjYsNDYsNjZdLFs2LDI2LDQ4LDcwXSxbNiwyNiw1MCw3NF0sWzYsMzAsNTQsNzhdLFs2LDMwLDU2LDgyXSxbNiwzMCw1OCw4Nl0sWzYsMzQsNjIsOTBdLFs2LDI4LDUwLDcyLDk0XSxbNiwyNiw1MCw3NCw5OF0sWzYsMzAsNTQsNzgsMTAyXSxbNiwyOCw1NCw4MCwxMDZdLFs2LDMyLDU4LDg0LDExMF0sWzYsMzAsNTgsODYsMTE0XSxbNiwzNCw2Miw5MCwxMThdLFs2LDI2LDUwLDc0LDk4LDEyMl0sWzYsMzAsNTQsNzgsMTAyLDEyNl0sWzYsMjYsNTIsNzgsMTA0LDEzMF0sWzYsMzAsNTYsODIsMTA4LDEzNF0sWzYsMzQsNjAsODYsMTEyLDEzOF0sWzYsMzAsNTgsODYsMTE0LDE0Ml0sWzYsMzQsNjIsOTAsMTE4LDE0Nl0sWzYsMzAsNTQsNzgsMTAyLDEyNiwxNTBdLFs2LDI0LDUwLDc2LDEwMiwxMjgsMTU0XSxbNiwyOCw1NCw4MCwxMDYsMTMyLDE1OF0sWzYsMzIsNTgsODQsMTEwLDEzNiwxNjJdLFs2LDI2LDU0LDgyLDExMCwxMzgsMTY2XSxbNiwzMCw1OCw4NiwxMTQsMTQyLDE3MF1dLGU9MTMzNSxuPTc5NzMsaT1mdW5jdGlvbih0KXtmb3IodmFyIHI9MDswIT10OylyKz0xLHQ+Pj49MTtyZXR1cm4gcn0sKG89e30pLmdldEJDSFR5cGVJbmZvPWZ1bmN0aW9uKHQpe2Zvcih2YXIgcj10PDwxMDtpKHIpLWkoZSk+PTA7KXJePWU8PGkociktaShlKTtyZXR1cm4gMjE1MjJeKHQ8PDEwfHIpfSxvLmdldEJDSFR5cGVOdW1iZXI9ZnVuY3Rpb24odCl7Zm9yKHZhciByPXQ8PDEyO2kociktaShuKT49MDspcl49bjw8aShyKS1pKG4pO3JldHVybiB0PDwxMnxyfSxvLmdldFBhdHRlcm5Qb3NpdGlvbj1mdW5jdGlvbih0KXtyZXR1cm4gclt0LTFdfSxvLmdldE1hc2tGdW5jdGlvbj1mdW5jdGlvbih0KXtzd2l0Y2godCl7Y2FzZSBsOnJldHVybiBmdW5jdGlvbih0LHIpe3JldHVybih0K3IpJTI9PTB9O2Nhc2UgaDpyZXR1cm4gZnVuY3Rpb24odCxyKXtyZXR1cm4gdCUyPT0wfTtjYXNlIHM6cmV0dXJuIGZ1bmN0aW9uKHQscil7cmV0dXJuIHIlMz09MH07Y2FzZSB2OnJldHVybiBmdW5jdGlvbih0LHIpe3JldHVybih0K3IpJTM9PTB9O2Nhc2UgZDpyZXR1cm4gZnVuY3Rpb24odCxyKXtyZXR1cm4oTWF0aC5mbG9vcih0LzIpK01hdGguZmxvb3Ioci8zKSklMj09MH07Y2FzZSB3OnJldHVybiBmdW5jdGlvbih0LHIpe3JldHVybiB0KnIlMit0KnIlMz09MH07Y2FzZSBwOnJldHVybiBmdW5jdGlvbih0LHIpe3JldHVybih0KnIlMit0KnIlMyklMj09MH07Y2FzZSB5OnJldHVybiBmdW5jdGlvbih0LHIpe3JldHVybih0KnIlMysodCtyKSUyKSUyPT0wfTtkZWZhdWx0OnRocm93ImJhZCBtYXNrUGF0dGVybjoiK3R9fSxvLmdldEVycm9yQ29ycmVjdFBvbHlub21pYWw9ZnVuY3Rpb24odCl7Zm9yKHZhciByPWsoWzFdLDApLGU9MDtlPHQ7ZSs9MSlyPXIubXVsdGlwbHkoayhbMSxDLmdleHAoZSldLDApKTtyZXR1cm4gcn0sby5nZXRMZW5ndGhJbkJpdHM9ZnVuY3Rpb24odCxyKXtpZigxPD1yJiZyPDEwKXN3aXRjaCh0KXtjYXNlIGE6cmV0dXJuIDEwO2Nhc2UgdTpyZXR1cm4gOTtjYXNlIGY6Y2FzZSBjOnJldHVybiA4O2RlZmF1bHQ6dGhyb3cibW9kZToiK3R9ZWxzZSBpZihyPDI3KXN3aXRjaCh0KXtjYXNlIGE6cmV0dXJuIDEyO2Nhc2UgdTpyZXR1cm4gMTE7Y2FzZSBmOnJldHVybiAxNjtjYXNlIGM6cmV0dXJuIDEwO2RlZmF1bHQ6dGhyb3cibW9kZToiK3R9ZWxzZXtpZighKHI8NDEpKXRocm93InR5cGU6IityO3N3aXRjaCh0KXtjYXNlIGE6cmV0dXJuIDE0O2Nhc2UgdTpyZXR1cm4gMTM7Y2FzZSBmOnJldHVybiAxNjtjYXNlIGM6cmV0dXJuIDEyO2RlZmF1bHQ6dGhyb3cibW9kZToiK3R9fX0sby5nZXRMb3N0UG9pbnQ9ZnVuY3Rpb24odCl7Zm9yKHZhciByPXQuZ2V0TW9kdWxlQ291bnQoKSxlPTAsbj0wO248cjtuKz0xKWZvcih2YXIgbz0wO288cjtvKz0xKXtmb3IodmFyIGk9MCxhPXQuaXNEYXJrKG4sbyksdT0tMTt1PD0xO3UrPTEpaWYoIShuK3U8MHx8cjw9bit1KSlmb3IodmFyIGY9LTE7Zjw9MTtmKz0xKW8rZjwwfHxyPD1vK2Z8fDA9PXUmJjA9PWZ8fGE9PXQuaXNEYXJrKG4rdSxvK2YpJiYoaSs9MSk7aT41JiYoZSs9MytpLTUpfWZvcihuPTA7bjxyLTE7bis9MSlmb3Iobz0wO288ci0xO28rPTEpe3ZhciBjPTA7dC5pc0RhcmsobixvKSYmKGMrPTEpLHQuaXNEYXJrKG4rMSxvKSYmKGMrPTEpLHQuaXNEYXJrKG4sbysxKSYmKGMrPTEpLHQuaXNEYXJrKG4rMSxvKzEpJiYoYys9MSksMCE9YyYmNCE9Y3x8KGUrPTMpfWZvcihuPTA7bjxyO24rPTEpZm9yKG89MDtvPHItNjtvKz0xKXQuaXNEYXJrKG4sbykmJiF0LmlzRGFyayhuLG8rMSkmJnQuaXNEYXJrKG4sbysyKSYmdC5pc0RhcmsobixvKzMpJiZ0LmlzRGFyayhuLG8rNCkmJiF0LmlzRGFyayhuLG8rNSkmJnQuaXNEYXJrKG4sbys2KSYmKGUrPTQwKTtmb3Iobz0wO288cjtvKz0xKWZvcihuPTA7bjxyLTY7bis9MSl0LmlzRGFyayhuLG8pJiYhdC5pc0RhcmsobisxLG8pJiZ0LmlzRGFyayhuKzIsbykmJnQuaXNEYXJrKG4rMyxvKSYmdC5pc0Rhcmsobis0LG8pJiYhdC5pc0Rhcmsobis1LG8pJiZ0LmlzRGFyayhuKzYsbykmJihlKz00MCk7dmFyIGc9MDtmb3Iobz0wO288cjtvKz0xKWZvcihuPTA7bjxyO24rPTEpdC5pc0RhcmsobixvKSYmKGcrPTEpO3JldHVybiBlKz1NYXRoLmFicygxMDAqZy9yL3ItNTApLzUqMTB9LG8pLEM9ZnVuY3Rpb24oKXtmb3IodmFyIHQ9bmV3IEFycmF5KDI1Nikscj1uZXcgQXJyYXkoMjU2KSxlPTA7ZTw4O2UrPTEpdFtlXT0xPDxlO2ZvcihlPTg7ZTwyNTY7ZSs9MSl0W2VdPXRbZS00XV50W2UtNV1edFtlLTZdXnRbZS04XTtmb3IoZT0wO2U8MjU1O2UrPTEpclt0W2VdXT1lO3ZhciBuPXtnbG9nOmZ1bmN0aW9uKHQpe2lmKHQ8MSl0aHJvdyJnbG9nKCIrdCsiKSI7cmV0dXJuIHJbdF19LGdleHA6ZnVuY3Rpb24ocil7Zm9yKDtyPDA7KXIrPTI1NTtmb3IoO3I+PTI1Njspci09MjU1O3JldHVybiB0W3JdfX07cmV0dXJuIG59KCk7ZnVuY3Rpb24gayh0LHIpe2lmKHZvaWQgMD09PXQubGVuZ3RoKXRocm93IHQubGVuZ3RoKyIvIityO3ZhciBlPWZ1bmN0aW9uKCl7Zm9yKHZhciBlPTA7ZTx0Lmxlbmd0aCYmMD09dFtlXTspZSs9MTtmb3IodmFyIG49bmV3IEFycmF5KHQubGVuZ3RoLWUrciksbz0wO288dC5sZW5ndGgtZTtvKz0xKW5bb109dFtvK2VdO3JldHVybiBufSgpLG49e2dldEF0OmZ1bmN0aW9uKHQpe3JldHVybiBlW3RdfSxnZXRMZW5ndGg6ZnVuY3Rpb24oKXtyZXR1cm4gZS5sZW5ndGh9LG11bHRpcGx5OmZ1bmN0aW9uKHQpe2Zvcih2YXIgcj1uZXcgQXJyYXkobi5nZXRMZW5ndGgoKSt0LmdldExlbmd0aCgpLTEpLGU9MDtlPG4uZ2V0TGVuZ3RoKCk7ZSs9MSlmb3IodmFyIG89MDtvPHQuZ2V0TGVuZ3RoKCk7bys9MSlyW2Urb11ePUMuZ2V4cChDLmdsb2cobi5nZXRBdChlKSkrQy5nbG9nKHQuZ2V0QXQobykpKTtyZXR1cm4gayhyLDApfSxtb2Q6ZnVuY3Rpb24odCl7aWYobi5nZXRMZW5ndGgoKS10LmdldExlbmd0aCgpPDApcmV0dXJuIG47Zm9yKHZhciByPUMuZ2xvZyhuLmdldEF0KDApKS1DLmdsb2codC5nZXRBdCgwKSksZT1uZXcgQXJyYXkobi5nZXRMZW5ndGgoKSksbz0wO288bi5nZXRMZW5ndGgoKTtvKz0xKWVbb109bi5nZXRBdChvKTtmb3Iobz0wO288dC5nZXRMZW5ndGgoKTtvKz0xKWVbb11ePUMuZ2V4cChDLmdsb2codC5nZXRBdChvKSkrcik7cmV0dXJuIGsoZSwwKS5tb2QodCl9fTtyZXR1cm4gbn12YXIgQT1mdW5jdGlvbigpe3ZhciB0PVtbMSwyNiwxOV0sWzEsMjYsMTZdLFsxLDI2LDEzXSxbMSwyNiw5XSxbMSw0NCwzNF0sWzEsNDQsMjhdLFsxLDQ0LDIyXSxbMSw0NCwxNl0sWzEsNzAsNTVdLFsxLDcwLDQ0XSxbMiwzNSwxN10sWzIsMzUsMTNdLFsxLDEwMCw4MF0sWzIsNTAsMzJdLFsyLDUwLDI0XSxbNCwyNSw5XSxbMSwxMzQsMTA4XSxbMiw2Nyw0M10sWzIsMzMsMTUsMiwzNCwxNl0sWzIsMzMsMTEsMiwzNCwxMl0sWzIsODYsNjhdLFs0LDQzLDI3XSxbNCw0MywxOV0sWzQsNDMsMTVdLFsyLDk4LDc4XSxbNCw0OSwzMV0sWzIsMzIsMTQsNCwzMywxNV0sWzQsMzksMTMsMSw0MCwxNF0sWzIsMTIxLDk3XSxbMiw2MCwzOCwyLDYxLDM5XSxbNCw0MCwxOCwyLDQxLDE5XSxbNCw0MCwxNCwyLDQxLDE1XSxbMiwxNDYsMTE2XSxbMyw1OCwzNiwyLDU5LDM3XSxbNCwzNiwxNiw0LDM3LDE3XSxbNCwzNiwxMiw0LDM3LDEzXSxbMiw4Niw2OCwyLDg3LDY5XSxbNCw2OSw0MywxLDcwLDQ0XSxbNiw0MywxOSwyLDQ0LDIwXSxbNiw0MywxNSwyLDQ0LDE2XSxbNCwxMDEsODFdLFsxLDgwLDUwLDQsODEsNTFdLFs0LDUwLDIyLDQsNTEsMjNdLFszLDM2LDEyLDgsMzcsMTNdLFsyLDExNiw5MiwyLDExNyw5M10sWzYsNTgsMzYsMiw1OSwzN10sWzQsNDYsMjAsNiw0NywyMV0sWzcsNDIsMTQsNCw0MywxNV0sWzQsMTMzLDEwN10sWzgsNTksMzcsMSw2MCwzOF0sWzgsNDQsMjAsNCw0NSwyMV0sWzEyLDMzLDExLDQsMzQsMTJdLFszLDE0NSwxMTUsMSwxNDYsMTE2XSxbNCw2NCw0MCw1LDY1LDQxXSxbMTEsMzYsMTYsNSwzNywxN10sWzExLDM2LDEyLDUsMzcsMTNdLFs1LDEwOSw4NywxLDExMCw4OF0sWzUsNjUsNDEsNSw2Niw0Ml0sWzUsNTQsMjQsNyw1NSwyNV0sWzExLDM2LDEyLDcsMzcsMTNdLFs1LDEyMiw5OCwxLDEyMyw5OV0sWzcsNzMsNDUsMyw3NCw0Nl0sWzE1LDQzLDE5LDIsNDQsMjBdLFszLDQ1LDE1LDEzLDQ2LDE2XSxbMSwxMzUsMTA3LDUsMTM2LDEwOF0sWzEwLDc0LDQ2LDEsNzUsNDddLFsxLDUwLDIyLDE1LDUxLDIzXSxbMiw0MiwxNCwxNyw0MywxNV0sWzUsMTUwLDEyMCwxLDE1MSwxMjFdLFs5LDY5LDQzLDQsNzAsNDRdLFsxNyw1MCwyMiwxLDUxLDIzXSxbMiw0MiwxNCwxOSw0MywxNV0sWzMsMTQxLDExMyw0LDE0MiwxMTRdLFszLDcwLDQ0LDExLDcxLDQ1XSxbMTcsNDcsMjEsNCw0OCwyMl0sWzksMzksMTMsMTYsNDAsMTRdLFszLDEzNSwxMDcsNSwxMzYsMTA4XSxbMyw2Nyw0MSwxMyw2OCw0Ml0sWzE1LDU0LDI0LDUsNTUsMjVdLFsxNSw0MywxNSwxMCw0NCwxNl0sWzQsMTQ0LDExNiw0LDE0NSwxMTddLFsxNyw2OCw0Ml0sWzE3LDUwLDIyLDYsNTEsMjNdLFsxOSw0NiwxNiw2LDQ3LDE3XSxbMiwxMzksMTExLDcsMTQwLDExMl0sWzE3LDc0LDQ2XSxbNyw1NCwyNCwxNiw1NSwyNV0sWzM0LDM3LDEzXSxbNCwxNTEsMTIxLDUsMTUyLDEyMl0sWzQsNzUsNDcsMTQsNzYsNDhdLFsxMSw1NCwyNCwxNCw1NSwyNV0sWzE2LDQ1LDE1LDE0LDQ2LDE2XSxbNiwxNDcsMTE3LDQsMTQ4LDExOF0sWzYsNzMsNDUsMTQsNzQsNDZdLFsxMSw1NCwyNCwxNiw1NSwyNV0sWzMwLDQ2LDE2LDIsNDcsMTddLFs4LDEzMiwxMDYsNCwxMzMsMTA3XSxbOCw3NSw0NywxMyw3Niw0OF0sWzcsNTQsMjQsMjIsNTUsMjVdLFsyMiw0NSwxNSwxMyw0NiwxNl0sWzEwLDE0MiwxMTQsMiwxNDMsMTE1XSxbMTksNzQsNDYsNCw3NSw0N10sWzI4LDUwLDIyLDYsNTEsMjNdLFszMyw0NiwxNiw0LDQ3LDE3XSxbOCwxNTIsMTIyLDQsMTUzLDEyM10sWzIyLDczLDQ1LDMsNzQsNDZdLFs4LDUzLDIzLDI2LDU0LDI0XSxbMTIsNDUsMTUsMjgsNDYsMTZdLFszLDE0NywxMTcsMTAsMTQ4LDExOF0sWzMsNzMsNDUsMjMsNzQsNDZdLFs0LDU0LDI0LDMxLDU1LDI1XSxbMTEsNDUsMTUsMzEsNDYsMTZdLFs3LDE0NiwxMTYsNywxNDcsMTE3XSxbMjEsNzMsNDUsNyw3NCw0Nl0sWzEsNTMsMjMsMzcsNTQsMjRdLFsxOSw0NSwxNSwyNiw0NiwxNl0sWzUsMTQ1LDExNSwxMCwxNDYsMTE2XSxbMTksNzUsNDcsMTAsNzYsNDhdLFsxNSw1NCwyNCwyNSw1NSwyNV0sWzIzLDQ1LDE1LDI1LDQ2LDE2XSxbMTMsMTQ1LDExNSwzLDE0NiwxMTZdLFsyLDc0LDQ2LDI5LDc1LDQ3XSxbNDIsNTQsMjQsMSw1NSwyNV0sWzIzLDQ1LDE1LDI4LDQ2LDE2XSxbMTcsMTQ1LDExNV0sWzEwLDc0LDQ2LDIzLDc1LDQ3XSxbMTAsNTQsMjQsMzUsNTUsMjVdLFsxOSw0NSwxNSwzNSw0NiwxNl0sWzE3LDE0NSwxMTUsMSwxNDYsMTE2XSxbMTQsNzQsNDYsMjEsNzUsNDddLFsyOSw1NCwyNCwxOSw1NSwyNV0sWzExLDQ1LDE1LDQ2LDQ2LDE2XSxbMTMsMTQ1LDExNSw2LDE0NiwxMTZdLFsxNCw3NCw0NiwyMyw3NSw0N10sWzQ0LDU0LDI0LDcsNTUsMjVdLFs1OSw0NiwxNiwxLDQ3LDE3XSxbMTIsMTUxLDEyMSw3LDE1MiwxMjJdLFsxMiw3NSw0NywyNiw3Niw0OF0sWzM5LDU0LDI0LDE0LDU1LDI1XSxbMjIsNDUsMTUsNDEsNDYsMTZdLFs2LDE1MSwxMjEsMTQsMTUyLDEyMl0sWzYsNzUsNDcsMzQsNzYsNDhdLFs0Niw1NCwyNCwxMCw1NSwyNV0sWzIsNDUsMTUsNjQsNDYsMTZdLFsxNywxNTIsMTIyLDQsMTUzLDEyM10sWzI5LDc0LDQ2LDE0LDc1LDQ3XSxbNDksNTQsMjQsMTAsNTUsMjVdLFsyNCw0NSwxNSw0Niw0NiwxNl0sWzQsMTUyLDEyMiwxOCwxNTMsMTIzXSxbMTMsNzQsNDYsMzIsNzUsNDddLFs0OCw1NCwyNCwxNCw1NSwyNV0sWzQyLDQ1LDE1LDMyLDQ2LDE2XSxbMjAsMTQ3LDExNyw0LDE0OCwxMThdLFs0MCw3NSw0Nyw3LDc2LDQ4XSxbNDMsNTQsMjQsMjIsNTUsMjVdLFsxMCw0NSwxNSw2Nyw0NiwxNl0sWzE5LDE0OCwxMTgsNiwxNDksMTE5XSxbMTgsNzUsNDcsMzEsNzYsNDhdLFszNCw1NCwyNCwzNCw1NSwyNV0sWzIwLDQ1LDE1LDYxLDQ2LDE2XV0scj1mdW5jdGlvbih0LHIpe3ZhciBlPXt9O3JldHVybiBlLnRvdGFsQ291bnQ9dCxlLmRhdGFDb3VudD1yLGV9LGU9e307cmV0dXJuIGUuZ2V0UlNCbG9ja3M9ZnVuY3Rpb24oZSxuKXt2YXIgbz1mdW5jdGlvbihyLGUpe3N3aXRjaChlKXtjYXNlIGcuTDpyZXR1cm4gdFs0KihyLTEpKzBdO2Nhc2UgZy5NOnJldHVybiB0WzQqKHItMSkrMV07Y2FzZSBnLlE6cmV0dXJuIHRbNCooci0xKSsyXTtjYXNlIGcuSDpyZXR1cm4gdFs0KihyLTEpKzNdO2RlZmF1bHQ6cmV0dXJufX0oZSxuKTtpZih2b2lkIDA9PT1vKXRocm93ImJhZCBycyBibG9jayBAIHR5cGVOdW1iZXI6IitlKyIvZXJyb3JDb3JyZWN0aW9uTGV2ZWw6IituO2Zvcih2YXIgaT1vLmxlbmd0aC8zLGE9W10sdT0wO3U8aTt1Kz0xKWZvcih2YXIgZj1vWzMqdSswXSxjPW9bMyp1KzFdLGw9b1szKnUrMl0saD0wO2g8ZjtoKz0xKWEucHVzaChyKGMsbCkpO3JldHVybiBhfSxlfSgpLGI9ZnVuY3Rpb24oKXt2YXIgdD1bXSxyPTAsZT17Z2V0QnVmZmVyOmZ1bmN0aW9uKCl7cmV0dXJuIHR9LGdldEF0OmZ1bmN0aW9uKHIpe3ZhciBlPU1hdGguZmxvb3Ioci84KTtyZXR1cm4gMT09KHRbZV0+Pj43LXIlOCYxKX0scHV0OmZ1bmN0aW9uKHQscil7Zm9yKHZhciBuPTA7bjxyO24rPTEpZS5wdXRCaXQoMT09KHQ+Pj5yLW4tMSYxKSl9LGdldExlbmd0aEluQml0czpmdW5jdGlvbigpe3JldHVybiByfSxwdXRCaXQ6ZnVuY3Rpb24oZSl7dmFyIG49TWF0aC5mbG9vcihyLzgpO3QubGVuZ3RoPD1uJiZ0LnB1c2goMCksZSYmKHRbbl18PTEyOD4+PnIlOCkscis9MX19O3JldHVybiBlfSxNPWZ1bmN0aW9uKHQpe3ZhciByPWEsZT10LG49e2dldE1vZGU6ZnVuY3Rpb24oKXtyZXR1cm4gcn0sZ2V0TGVuZ3RoOmZ1bmN0aW9uKHQpe3JldHVybiBlLmxlbmd0aH0sd3JpdGU6ZnVuY3Rpb24odCl7Zm9yKHZhciByPWUsbj0wO24rMjxyLmxlbmd0aDspdC5wdXQobyhyLnN1YnN0cmluZyhuLG4rMykpLDEwKSxuKz0zO248ci5sZW5ndGgmJihyLmxlbmd0aC1uPT0xP3QucHV0KG8oci5zdWJzdHJpbmcobixuKzEpKSw0KTpyLmxlbmd0aC1uPT0yJiZ0LnB1dChvKHIuc3Vic3RyaW5nKG4sbisyKSksNykpfX0sbz1mdW5jdGlvbih0KXtmb3IodmFyIHI9MCxlPTA7ZTx0Lmxlbmd0aDtlKz0xKXI9MTAqcitpKHQuY2hhckF0KGUpKTtyZXR1cm4gcn0saT1mdW5jdGlvbih0KXtpZigiMCI8PXQmJnQ8PSI5IilyZXR1cm4gdC5jaGFyQ29kZUF0KDApLSIwIi5jaGFyQ29kZUF0KDApO3Rocm93ImlsbGVnYWwgY2hhciA6Iit0fTtyZXR1cm4gbn0seD1mdW5jdGlvbih0KXt2YXIgcj11LGU9dCxuPXtnZXRNb2RlOmZ1bmN0aW9uKCl7cmV0dXJuIHJ9LGdldExlbmd0aDpmdW5jdGlvbih0KXtyZXR1cm4gZS5sZW5ndGh9LHdyaXRlOmZ1bmN0aW9uKHQpe2Zvcih2YXIgcj1lLG49MDtuKzE8ci5sZW5ndGg7KXQucHV0KDQ1Km8oci5jaGFyQXQobikpK28oci5jaGFyQXQobisxKSksMTEpLG4rPTI7bjxyLmxlbmd0aCYmdC5wdXQobyhyLmNoYXJBdChuKSksNil9fSxvPWZ1bmN0aW9uKHQpe2lmKCIwIjw9dCYmdDw9IjkiKXJldHVybiB0LmNoYXJDb2RlQXQoMCktIjAiLmNoYXJDb2RlQXQoMCk7aWYoIkEiPD10JiZ0PD0iWiIpcmV0dXJuIHQuY2hhckNvZGVBdCgwKS0iQSIuY2hhckNvZGVBdCgwKSsxMDtzd2l0Y2godCl7Y2FzZSIgIjpyZXR1cm4gMzY7Y2FzZSIkIjpyZXR1cm4gMzc7Y2FzZSIlIjpyZXR1cm4gMzg7Y2FzZSIqIjpyZXR1cm4gMzk7Y2FzZSIrIjpyZXR1cm4gNDA7Y2FzZSItIjpyZXR1cm4gNDE7Y2FzZSIuIjpyZXR1cm4gNDI7Y2FzZSIvIjpyZXR1cm4gNDM7Y2FzZSI6IjpyZXR1cm4gNDQ7ZGVmYXVsdDp0aHJvdyJpbGxlZ2FsIGNoYXIgOiIrdH19O3JldHVybiBufSxtPWZ1bmN0aW9uKHIpe3ZhciBlPWYsbj10LnN0cmluZ1RvQnl0ZXMociksbz17Z2V0TW9kZTpmdW5jdGlvbigpe3JldHVybiBlfSxnZXRMZW5ndGg6ZnVuY3Rpb24odCl7cmV0dXJuIG4ubGVuZ3RofSx3cml0ZTpmdW5jdGlvbih0KXtmb3IodmFyIHI9MDtyPG4ubGVuZ3RoO3IrPTEpdC5wdXQobltyXSw4KX19O3JldHVybiBvfSxMPWZ1bmN0aW9uKHIpe3ZhciBlPWMsbj10LnN0cmluZ1RvQnl0ZXNGdW5jcy5TSklTO2lmKCFuKXRocm93InNqaXMgbm90IHN1cHBvcnRlZC4iOyFmdW5jdGlvbigpe3ZhciB0PW4oIuWPiyIpO2lmKDIhPXQubGVuZ3RofHwzODcyNiE9KHRbMF08PDh8dFsxXSkpdGhyb3cic2ppcyBub3Qgc3VwcG9ydGVkLiJ9KCk7dmFyIG89bihyKSxpPXtnZXRNb2RlOmZ1bmN0aW9uKCl7cmV0dXJuIGV9LGdldExlbmd0aDpmdW5jdGlvbih0KXtyZXR1cm5+fihvLmxlbmd0aC8yKX0sd3JpdGU6ZnVuY3Rpb24odCl7Zm9yKHZhciByPW8sZT0wO2UrMTxyLmxlbmd0aDspe3ZhciBuPSgyNTUmcltlXSk8PDh8MjU1JnJbZSsxXTtpZigzMzA4ODw9biYmbjw9NDA5NTYpbi09MzMwODg7ZWxzZXtpZighKDU3NDA4PD1uJiZuPD02MDM1MSkpdGhyb3ciaWxsZWdhbCBjaGFyIGF0ICIrKGUrMSkrIi8iK247bi09NDk0NzJ9bj0xOTIqKG4+Pj44JjI1NSkrKDI1NSZuKSx0LnB1dChuLDEzKSxlKz0yfWlmKGU8ci5sZW5ndGgpdGhyb3ciaWxsZWdhbCBjaGFyIGF0ICIrKGUrMSl9fTtyZXR1cm4gaX0sRD1mdW5jdGlvbigpe3ZhciB0PVtdLHI9e3dyaXRlQnl0ZTpmdW5jdGlvbihyKXt0LnB1c2goMjU1JnIpfSx3cml0ZVNob3J0OmZ1bmN0aW9uKHQpe3Iud3JpdGVCeXRlKHQpLHIud3JpdGVCeXRlKHQ+Pj44KX0sd3JpdGVCeXRlczpmdW5jdGlvbih0LGUsbil7ZT1lfHwwLG49bnx8dC5sZW5ndGg7Zm9yKHZhciBvPTA7bzxuO28rPTEpci53cml0ZUJ5dGUodFtvK2VdKX0sd3JpdGVTdHJpbmc6ZnVuY3Rpb24odCl7Zm9yKHZhciBlPTA7ZTx0Lmxlbmd0aDtlKz0xKXIud3JpdGVCeXRlKHQuY2hhckNvZGVBdChlKSl9LHRvQnl0ZUFycmF5OmZ1bmN0aW9uKCl7cmV0dXJuIHR9LHRvU3RyaW5nOmZ1bmN0aW9uKCl7dmFyIHI9IiI7cis9IlsiO2Zvcih2YXIgZT0wO2U8dC5sZW5ndGg7ZSs9MSllPjAmJihyKz0iLCIpLHIrPXRbZV07cmV0dXJuIHIrPSJdIn19O3JldHVybiByfSxTPWZ1bmN0aW9uKHQpe3ZhciByPXQsZT0wLG49MCxvPTAsaT17cmVhZDpmdW5jdGlvbigpe2Zvcig7bzw4Oyl7aWYoZT49ci5sZW5ndGgpe2lmKDA9PW8pcmV0dXJuLTE7dGhyb3cidW5leHBlY3RlZCBlbmQgb2YgZmlsZS4vIitvfXZhciB0PXIuY2hhckF0KGUpO2lmKGUrPTEsIj0iPT10KXJldHVybiBvPTAsLTE7dC5tYXRjaCgvXlxzJC8pfHwobj1uPDw2fGEodC5jaGFyQ29kZUF0KDApKSxvKz02KX12YXIgaT1uPj4+by04JjI1NTtyZXR1cm4gby09OCxpfX0sYT1mdW5jdGlvbih0KXtpZig2NTw9dCYmdDw9OTApcmV0dXJuIHQtNjU7aWYoOTc8PXQmJnQ8PTEyMilyZXR1cm4gdC05NysyNjtpZig0ODw9dCYmdDw9NTcpcmV0dXJuIHQtNDgrNTI7aWYoNDM9PXQpcmV0dXJuIDYyO2lmKDQ3PT10KXJldHVybiA2Mzt0aHJvdyJjOiIrdH07cmV0dXJuIGl9LEk9ZnVuY3Rpb24odCxyLGUpe2Zvcih2YXIgbj1mdW5jdGlvbih0LHIpe3ZhciBlPXQsbj1yLG89bmV3IEFycmF5KHQqciksaT17c2V0UGl4ZWw6ZnVuY3Rpb24odCxyLG4pe29bciplK3RdPW59LHdyaXRlOmZ1bmN0aW9uKHQpe3Qud3JpdGVTdHJpbmcoIkdJRjg3YSIpLHQud3JpdGVTaG9ydChlKSx0LndyaXRlU2hvcnQobiksdC53cml0ZUJ5dGUoMTI4KSx0LndyaXRlQnl0ZSgwKSx0LndyaXRlQnl0ZSgwKSx0LndyaXRlQnl0ZSgwKSx0LndyaXRlQnl0ZSgwKSx0LndyaXRlQnl0ZSgwKSx0LndyaXRlQnl0ZSgyNTUpLHQud3JpdGVCeXRlKDI1NSksdC53cml0ZUJ5dGUoMjU1KSx0LndyaXRlU3RyaW5nKCIsIiksdC53cml0ZVNob3J0KDApLHQud3JpdGVTaG9ydCgwKSx0LndyaXRlU2hvcnQoZSksdC53cml0ZVNob3J0KG4pLHQud3JpdGVCeXRlKDApO3ZhciByPWEoMik7dC53cml0ZUJ5dGUoMik7Zm9yKHZhciBvPTA7ci5sZW5ndGgtbz4yNTU7KXQud3JpdGVCeXRlKDI1NSksdC53cml0ZUJ5dGVzKHIsbywyNTUpLG8rPTI1NTt0LndyaXRlQnl0ZShyLmxlbmd0aC1vKSx0LndyaXRlQnl0ZXMocixvLHIubGVuZ3RoLW8pLHQud3JpdGVCeXRlKDApLHQud3JpdGVTdHJpbmcoIjsiKX19LGE9ZnVuY3Rpb24odCl7Zm9yKHZhciByPTE8PHQsZT0xKygxPDx0KSxuPXQrMSxpPXUoKSxhPTA7YTxyO2ErPTEpaS5hZGQoU3RyaW5nLmZyb21DaGFyQ29kZShhKSk7aS5hZGQoU3RyaW5nLmZyb21DaGFyQ29kZShyKSksaS5hZGQoU3RyaW5nLmZyb21DaGFyQ29kZShlKSk7dmFyIGYsYyxnLGw9RCgpLGg9KGY9bCxjPTAsZz0wLHt3cml0ZTpmdW5jdGlvbih0LHIpe2lmKHQ+Pj5yIT0wKXRocm93Imxlbmd0aCBvdmVyIjtmb3IoO2Mrcj49ODspZi53cml0ZUJ5dGUoMjU1Jih0PDxjfGcpKSxyLT04LWMsdD4+Pj04LWMsZz0wLGM9MDtnfD10PDxjLGMrPXJ9LGZsdXNoOmZ1bmN0aW9uKCl7Yz4wJiZmLndyaXRlQnl0ZShnKX19KTtoLndyaXRlKHIsbik7dmFyIHM9MCx2PVN0cmluZy5mcm9tQ2hhckNvZGUob1tzXSk7Zm9yKHMrPTE7czxvLmxlbmd0aDspe3ZhciBkPVN0cmluZy5mcm9tQ2hhckNvZGUob1tzXSk7cys9MSxpLmNvbnRhaW5zKHYrZCk/dis9ZDooaC53cml0ZShpLmluZGV4T2YodiksbiksaS5zaXplKCk8NDA5NSYmKGkuc2l6ZSgpPT0xPDxuJiYobis9MSksaS5hZGQoditkKSksdj1kKX1yZXR1cm4gaC53cml0ZShpLmluZGV4T2YodiksbiksaC53cml0ZShlLG4pLGguZmx1c2goKSxsLnRvQnl0ZUFycmF5KCl9LHU9ZnVuY3Rpb24oKXt2YXIgdD17fSxyPTAsZT17YWRkOmZ1bmN0aW9uKG4pe2lmKGUuY29udGFpbnMobikpdGhyb3ciZHVwIGtleToiK247dFtuXT1yLHIrPTF9LHNpemU6ZnVuY3Rpb24oKXtyZXR1cm4gcn0saW5kZXhPZjpmdW5jdGlvbihyKXtyZXR1cm4gdFtyXX0sY29udGFpbnM6ZnVuY3Rpb24ocil7cmV0dXJuIHZvaWQgMCE9PXRbcl19fTtyZXR1cm4gZX07cmV0dXJuIGl9KHQsciksbz0wO288cjtvKz0xKWZvcih2YXIgaT0wO2k8dDtpKz0xKW4uc2V0UGl4ZWwoaSxvLGUoaSxvKSk7dmFyIGE9RCgpO24ud3JpdGUoYSk7Zm9yKHZhciB1PWZ1bmN0aW9uKCl7dmFyIHQ9MCxyPTAsZT0wLG49IiIsbz17fSxpPWZ1bmN0aW9uKHQpe24rPVN0cmluZy5mcm9tQ2hhckNvZGUoYSg2MyZ0KSl9LGE9ZnVuY3Rpb24odCl7aWYodDwwKTtlbHNle2lmKHQ8MjYpcmV0dXJuIDY1K3Q7aWYodDw1MilyZXR1cm4gdC0yNis5NztpZih0PDYyKXJldHVybiB0LTUyKzQ4O2lmKDYyPT10KXJldHVybiA0MztpZig2Mz09dClyZXR1cm4gNDd9dGhyb3cibjoiK3R9O3JldHVybiBvLndyaXRlQnl0ZT1mdW5jdGlvbihuKXtmb3IodD10PDw4fDI1NSZuLHIrPTgsZSs9MTtyPj02OylpKHQ+Pj5yLTYpLHItPTZ9LG8uZmx1c2g9ZnVuY3Rpb24oKXtpZihyPjAmJihpKHQ8PDYtciksdD0wLHI9MCksZSUzIT0wKWZvcih2YXIgbz0zLWUlMyxhPTA7YTxvO2ErPTEpbis9Ij0ifSxvLnRvU3RyaW5nPWZ1bmN0aW9uKCl7cmV0dXJuIG59LG99KCksZj1hLnRvQnl0ZUFycmF5KCksYz0wO2M8Zi5sZW5ndGg7Yys9MSl1LndyaXRlQnl0ZShmW2NdKTtyZXR1cm4gdS5mbHVzaCgpLCJkYXRhOmltYWdlL2dpZjtiYXNlNjQsIit1fTtyZXR1cm4gdH0oKTtxcmNvZGUuc3RyaW5nVG9CeXRlc0Z1bmNzWyJVVEYtOCJdPWZ1bmN0aW9uKHQpe3JldHVybiBmdW5jdGlvbih0KXtmb3IodmFyIHI9W10sZT0wO2U8dC5sZW5ndGg7ZSsrKXt2YXIgbj10LmNoYXJDb2RlQXQoZSk7bjwxMjg/ci5wdXNoKG4pOm48MjA0OD9yLnB1c2goMTkyfG4+PjYsMTI4fDYzJm4pOm48NTUyOTZ8fG4+PTU3MzQ0P3IucHVzaCgyMjR8bj4+MTIsMTI4fG4+PjYmNjMsMTI4fDYzJm4pOihlKyssbj02NTUzNisoKDEwMjMmbik8PDEwfDEwMjMmdC5jaGFyQ29kZUF0KGUpKSxyLnB1c2goMjQwfG4+PjE4LDEyOHxuPj4xMiY2MywxMjh8bj4+NiY2MywxMjh8NjMmbikpfXJldHVybiByfSh0KX0sZnVuY3Rpb24odCl7ImZ1bmN0aW9uIj09dHlwZW9mIGRlZmluZSYmZGVmaW5lLmFtZD9kZWZpbmUoW10sdCk6Im9iamVjdCI9PXR5cGVvZiBleHBvcnRzJiYobW9kdWxlLmV4cG9ydHM9dCgpKX0oZnVuY3Rpb24oKXtyZXR1cm4gcXJjb2RlfSk7"


# ============================================================
# VodiWalker v18 — UI overrides (login, dashboard theme, telegram proxy, operators)
# ============================================================
try:
    from ui_login import LOGIN_V18 as LOGIN_HTML  # noqa: F811
    from ui_dash import patch_dashboard as _patch_dashboard
    DASHBOARD_HTML = _patch_dashboard(DASHBOARD_HTML)  # noqa: F811
except Exception as _e:  # اگر چیزی خراب بود، UI قدیمی سالم بالا بیاید
    import logging as _lg
    _lg.getLogger("vodiwalker").warning("v18 UI override skipped: %s", _e)
