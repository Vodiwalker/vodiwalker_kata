# ui_login.py — صفحه‌ی ورود جدید (Aurora). placeholder خطا: <!--LOGIN_ERROR-->
LOGIN_V18 = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl" id="htmlRoot" translate="no">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="google" content="notranslate"><meta name="theme-color" content="#060912"><title>VodiWalker | Login</title>
<link rel="stylesheet" href="/assets/ui.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{--bg:#060912;--text:#eef2ff;--sub:#94a3c8;--sub2:#66739a;--line:rgba(148,163,255,.16);--line2:rgba(148,163,255,.34);
--a:#7c5cff;--b:#22d3ee;--c:#34d399;--ease:cubic-bezier(.22,.7,.2,1)}
html,body{min-height:100%;background:var(--bg);color:var(--text)}
body{font-family:'Vazirmatn','Inter',sans-serif;min-height:100dvh;display:grid;grid-template-columns:1.15fr 1fr;overflow-x:hidden;-webkit-font-smoothing:antialiased}
html[data-lang=en] body{font-family:'Inter','Vazirmatn',sans-serif}
button,input{font-family:inherit}button{cursor:pointer}:focus{outline:none}:focus-visible{outline:2px solid var(--b);outline-offset:2px}
#fx{position:fixed;inset:0;z-index:0;width:100%;height:100%;pointer-events:none}
.mesh{position:fixed;inset:0;z-index:0;pointer-events:none;background:
 radial-gradient(55% 45% at 85% 8%,rgba(124,92,255,.34),transparent 70%),
 radial-gradient(45% 40% at 10% 92%,rgba(34,211,238,.20),transparent 70%),
 radial-gradient(40% 35% at 55% 55%,rgba(52,211,153,.08),transparent 70%)}
.show{position:relative;z-index:1;display:flex;flex-direction:column;justify-content:center;padding:56px clamp(28px,6vw,90px);gap:30px}
.brand{display:flex;align-items:center;gap:14px;direction:ltr;width:max-content}
.brand img{width:52px;height:52px;border-radius:16px;box-shadow:0 0 0 1px var(--line2),0 12px 36px -8px rgba(124,92,255,.7)}
.brand b{font:800 20px 'Inter',sans-serif;letter-spacing:.14em}.brand small{display:block;font:500 10px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;letter-spacing:.28em;color:var(--sub2);margin-top:3px}
.show h2{font-size:clamp(26px,2.8vw,40px);font-weight:900;line-height:1.5}
.show h2 .g{background:linear-gradient(90deg,#a78bfa,#22d3ee,#34d399,#a78bfa);background-size:240% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:shine 7s linear infinite}
@keyframes shine{to{background-position:240% 0}}
.show p.lead{color:var(--sub);line-height:2.1;max-width:520px;font-size:14px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:540px;direction:ltr}
.st{padding:16px 14px;border-radius:20px;border:1px solid var(--line);background:rgba(14,19,40,.55);backdrop-filter:blur(12px);transition:transform .25s var(--ease),border-color .25s}
.st:hover{transform:translateY(-4px);border-color:var(--line2)}
.st i{font-size:24px;display:block;margin-bottom:10px}.st b{display:block;font:800 20px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif}.st small{font:500 10.5px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--sub2)}
.st:nth-child(1) i{color:var(--c)}.st:nth-child(2) i{color:var(--b)}.st:nth-child(3) i{color:#a78bfa}
.feats{display:flex;flex-wrap:wrap;gap:8px;max-width:560px;direction:ltr}
.feats span{display:inline-flex;align-items:center;gap:7px;padding:8px 13px;border-radius:99px;border:1px solid var(--line);background:rgba(14,19,40,.5);font:600 11.5px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--sub)}
.feats i{color:var(--b);font-size:15px}
.heroimg{position:relative;width:100%;max-width:560px;border-radius:26px;overflow:hidden;border:1px solid var(--line2);box-shadow:0 30px 70px -30px rgba(124,92,255,.8),0 0 0 6px rgba(124,92,255,.07);animation:rise .9s var(--ease) both}
.heroimg img{display:block;width:100%;height:auto;transform:scale(1.02);transition:transform 1.2s var(--ease)}
.heroimg:hover img{transform:scale(1.07)}
.heroimg:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(6,9,18,.55));pointer-events:none}
.mhero{display:none;margin:-8px -8px 18px;border-radius:22px;overflow:hidden;border:1px solid var(--line2)}
.mhero img{display:block;width:100%;height:auto}
.float{position:absolute;inset-inline-end:7%;top:12%;width:200px;height:200px;border-radius:50%;border:1px dashed var(--line2);animation:spin 40s linear infinite;opacity:.6}
.float:after{content:"";position:absolute;top:-6px;left:50%;width:12px;height:12px;border-radius:50%;background:var(--b);box-shadow:0 0 18px var(--b)}
@keyframes spin{to{transform:rotate(360deg)}}
.side{position:relative;z-index:2;display:flex;align-items:center;justify-content:center;padding:28px 20px}
.top{position:fixed;top:calc(14px + env(safe-area-inset-top,0px));inset-inline:16px;z-index:9;display:flex;justify-content:space-between;pointer-events:none;direction:ltr}
.top>*{pointer-events:auto}
.pill,.lang>button{display:flex;align-items:center;gap:8px;padding:9px 14px;border-radius:14px;background:rgba(10,14,30,.7);backdrop-filter:blur(12px);border:1px solid var(--line);color:var(--sub);font:600 12px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif}
.pill i{color:var(--c);font-size:18px}.lang{position:relative}.lang>button:hover{border-color:var(--line2);color:#fff}
.lang-menu{position:absolute;top:calc(100% + 6px);right:0;min-width:130px;background:#0b1024;border:1px solid var(--line2);border-radius:14px;overflow:hidden;opacity:0;visibility:hidden;transform:translateY(-6px);transition:.18s var(--ease)}
.lang-menu.on{opacity:1;visibility:visible;transform:none}
.lang-menu button{display:block;width:100%;padding:11px 14px;background:none;border:0;color:var(--sub);font:700 12.5px inherit;text-align:start}
.lang-menu button.cur,.lang-menu button:hover{background:rgba(124,92,255,.2);color:#fff}
.card{position:relative;width:100%;max-width:430px;padding:30px 24px 22px;border-radius:30px;border:1px solid var(--line2);
 background:linear-gradient(180deg,rgba(18,24,52,.82),rgba(8,11,28,.9));backdrop-filter:blur(22px);
 box-shadow:0 40px 90px -34px rgba(124,92,255,.65),inset 0 1px 0 rgba(255,255,255,.07);animation:rise .8s var(--ease) both}
.card:before{content:"";position:absolute;inset:-1px;border-radius:inherit;padding:1px;background:conic-gradient(from var(--ang,0deg),transparent 0 70%,var(--a),var(--b),transparent);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;animation:ang 6s linear infinite;pointer-events:none}
@property --ang{syntax:'<angle>';initial-value:0deg;inherits:false}@keyframes ang{to{--ang:360deg}}
@keyframes rise{from{opacity:0;transform:translateY(22px) scale(.985)}to{opacity:1;transform:none}}
.mhead{display:none!important;align-items:center;gap:12px;margin-bottom:18px;direction:ltr}
.mhead img{width:42px;height:42px;border-radius:13px}.mhead b{font:800 17px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;letter-spacing:.12em}
.hd small{font-size:12px;color:var(--b);font-weight:700}.hd h1{font-size:25px;font-weight:900;margin:5px 0 4px}.hd p{font-size:12.5px;color:var(--sub);line-height:1.9;margin-bottom:20px}
.inp{position:relative;margin-bottom:12px}
.inp input{width:100%;height:56px;padding:0 50px;border-radius:17px;border:1px solid var(--line);background:rgba(4,7,20,.75);color:var(--text);font-size:15.5px;transition:.2s}
.inp input::placeholder{color:var(--sub2);font-size:13.5px}.inp input:hover{border-color:var(--line2)}
.inp input:focus{border-color:var(--a);box-shadow:0 0 0 4px rgba(124,92,255,.22);background:rgba(8,11,30,.95)}
.inp .lead{position:absolute;inset-inline-start:16px;top:50%;transform:translateY(-50%);font-size:21px;color:#8b7cff;pointer-events:none;transition:.2s}
.inp:focus-within .lead{color:var(--b)}
.eye{position:absolute;inset-inline-end:8px;top:50%;transform:translateY(-50%);width:40px;height:40px;display:grid;place-items:center;background:none;border:0;border-radius:11px;color:#8b7cff;font-size:21px}
.eye:hover{background:rgba(124,92,255,.16);color:#fff}
html[dir=rtl] .inp .lead{inset-inline-start:auto;right:16px}html[dir=rtl] .eye{inset-inline-end:auto;left:8px}
.inp input:-webkit-autofill{-webkit-text-fill-color:var(--text);-webkit-box-shadow:0 0 0 1000px #0a1028 inset;caret-color:#fff}
#capsWarn{display:none;align-items:center;gap:6px;margin:-2px 2px 10px;font-size:11.5px;color:#fbbf24}
.remember{display:flex;align-items:center;gap:10px;margin:6px 2px 18px;font-size:13px;color:var(--sub);cursor:pointer;user-select:none}
.remember input{appearance:none;-webkit-appearance:none;width:22px;height:22px;border-radius:7px;background:rgba(4,7,20,.8);border:1px solid var(--line2);display:grid;place-items:center;cursor:pointer;transition:.18s}
.remember input:checked{background:linear-gradient(135deg,var(--a),#4f8bff);border-color:transparent}
.remember input:checked:after{content:"";width:6px;height:11px;border:solid #fff;border-width:0 2.5px 2.5px 0;transform:rotate(45deg) translate(-1px,-1px)}
.go{position:relative;overflow:hidden;width:100%;height:58px;border:0;border-radius:17px;color:#fff;font-size:16px;font-weight:800;display:flex;align-items:center;justify-content:center;gap:10px;
 background:linear-gradient(100deg,#5b4bff,#7c5cff 45%,#22a7e8);background-size:200% 100%;box-shadow:0 16px 36px -12px rgba(100,90,255,.9),inset 0 1px 0 rgba(255,255,255,.3);transition:.25s var(--ease)}
.go:before{content:"";position:absolute;top:0;bottom:0;width:55%;left:-80%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.3),transparent);transform:skewX(-18deg);transition:left .6s}
.go:hover:before{left:130%}.go:hover{background-position:100% 0;transform:translateY(-2px)}.go:active{transform:scale(.985)}
.go i{font-size:22px}
.go.loading{pointer-events:none;opacity:.9}.go.loading>*{visibility:hidden}.go.loading:after{content:"";position:absolute;width:22px;height:22px;border-radius:50%;border:3px solid rgba(255,255,255,.35);border-top-color:#fff;animation:spin .7s linear infinite}
.error{display:flex;gap:8px;align-items:flex-start;margin:0 0 14px;padding:12px 14px;border-radius:14px;font-size:12.5px;line-height:1.8;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.35);color:#fca5a5;animation:shake .5s}
.error:before{content:"\ea05";font-family:tabler-icons;font-size:17px;flex:none}
@keyframes shake{10%,90%{transform:translateX(-1px)}20%,80%{transform:translateX(2px)}30%,50%,70%{transform:translateX(-4px)}40%,60%{transform:translateX(4px)}}
.sep{display:flex;align-items:center;gap:12px;margin:18px 0 12px;color:var(--sub2);font-size:11px}.sep:before,.sep:after{content:"";flex:1;height:1px;background:var(--line)}
.reg{width:100%;padding:14px 16px;border-radius:16px;border:1px solid var(--line);background:rgba(10,14,32,.6);color:var(--sub);font-size:13px;font-weight:700;display:flex;align-items:center;gap:12px;transition:.2s}
.reg:hover{border-color:var(--line2);color:#fff;background:rgba(20,26,58,.7)}.reg .a{font-size:22px;color:#8b7cff}.reg .ch{margin-inline-start:auto}
html[dir=rtl] .reg .ch{transform:scaleX(-1)}
.notice{margin-top:14px;padding:12px 14px;border-radius:16px;border:1px solid var(--line);background:rgba(34,211,238,.05);font-size:11.5px;line-height:2;color:#9ec5ff}
.notice b{color:#fff;display:block;font-size:12.5px}
.tg{display:inline-flex;align-items:center;gap:7px;margin-top:6px;padding:7px 15px;border-radius:99px;border:1px solid rgba(34,211,238,.5);background:rgba(34,211,238,.08);color:#67e8f9;font:700 12px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif}
.foot{margin-top:18px;text-align:center;font:500 10px 'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;letter-spacing:.3em;color:var(--sub2)}
.ov{position:fixed;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;background:rgba(3,5,14,.8);backdrop-filter:blur(7px);padding:18px;opacity:0;visibility:hidden;transition:opacity .22s,visibility 0s .22s}
.ov.on{opacity:1;visibility:visible;transition:opacity .22s}
.box{width:100%;max-width:420px;max-height:90dvh;overflow:auto;padding:24px;border-radius:26px;background:linear-gradient(180deg,#121a3a,#0a0f26);border:1px solid var(--line2);transform:translateY(14px) scale(.97);transition:.25s var(--ease)}
.ov.on .box{transform:none}
.bh{display:flex;justify-content:space-between;gap:10px;margin-bottom:14px}.bh h3{font-size:17px;font-weight:900;margin:8px 0 6px}.bh p{font-size:11.5px;color:var(--sub);line-height:1.9}
.badge{display:inline-flex;gap:6px;align-items:center;padding:5px 11px;border-radius:99px;font-size:10px;font-weight:800;color:#c4b5fd;background:rgba(124,92,255,.15);border:1px solid var(--line2)}
.x{width:38px;height:38px;flex:none;border-radius:12px;display:grid;place-items:center;background:rgba(255,255,255,.06);border:1px solid var(--line);color:var(--sub)}
.x:hover{background:rgba(255,255,255,.13);color:#fff}
.msg{display:none;margin-bottom:12px;padding:10px 12px;border-radius:12px;font-size:12px;line-height:1.8}
.msg.ok{background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);color:#86efac}.msg.err{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.32);color:#fca5a5}
.hint{margin-top:12px;font-size:10.5px;color:var(--sub2);line-height:1.9;text-align:center}
@media(max-width:960px){body{grid-template-columns:1fr}.show{display:none}.mhero{display:block}.side{padding-top:70px;min-height:100dvh}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition-duration:.001ms!important}}
</style>
</head>
<body>
<canvas id="fx" aria-hidden="true"></canvas><div class="mesh" aria-hidden="true"></div>
<div class="top">
  <div class="pill"><i class="ti ti-shield-lock"></i><span data-i18n="secure">اتصال امن</span></div>
  <div class="lang"><button type="button" id="langBtn" aria-haspopup="true" aria-expanded="false"><i class="ti ti-world"></i><span id="langCur">FA</span><i class="ti ti-chevron-down" style="font-size:13px"></i></button>
    <div class="lang-menu" id="langMenu"><button type="button" id="langFa" onclick="setLang('fa')">فارسی</button><button type="button" id="langEn" onclick="setLang('en')">English</button></div></div>
</div>
<section class="show">
  <div class="float" aria-hidden="true"></div>
  <div class="heroimg"><img src="/assets/vw-hero.jpg" alt="VodiWalker"></div>
  <h2 data-i18n="hero">کنترل کامل شبکه‌ات،<br><span class="g">حرفه‌ای و زنده</span></h2>
  <p class="lead" data-i18n="heroP">مدیریت اینباندها، کلاینت‌ها، اشتراک‌ها و پروکسی تلگرام در یک پنل واحد؛ با پریست مخصوص هر اپراتور (همراه اول، ایرانسل، مخابرات) و مانیتورینگ لحظه‌ای.</p>
  <div class="stats"><div class="st"><i class="ti ti-activity"></i><b>Live</b><small>Real-time monitor</small></div><div class="st"><i class="ti ti-antenna-bars-5"></i><b>MCI · IRC · TCI</b><small>Operator presets</small></div><div class="st"><i class="ti ti-brand-telegram"></i><b>MTProto</b><small>Telegram proxy</small></div></div>
  <div class="feats"><span><i class="ti ti-lock"></i>Encrypted sessions</span><span><i class="ti ti-qrcode"></i>Smart subscription</span><span><i class="ti ti-gauge"></i>Speed &amp; quota limits</span><span><i class="ti ti-users-group"></i>Multi-admin</span></div>
</section>
<main class="side">
  <div class="card">
    <div class="mhero"><img src="/assets/vw-hero.jpg" alt="VodiWalker"></div>
    <div class="hd"><small data-i18n="cardSmall">حساب کاربری مدیر</small><h1 data-i18n="cardTitle">ورود به مرکز کنترل</h1><p data-i18n="cardP">برای ادامه نام کاربری و رمز عبور خود را وارد کنید.</p></div>
    <form method="post" action="/login" id="loginForm" autocomplete="on">
      <div class="inp"><input type="text" name="username" id="username" placeholder="نام کاربری" data-i18n-placeholder="userPh" required autocomplete="username" autocapitalize="none" spellcheck="false" dir="ltr"><i class="ti ti-user lead"></i></div>
      <div class="inp"><input type="password" name="password" id="password" placeholder="رمز عبور" data-i18n-placeholder="passPh" required autocomplete="current-password" dir="ltr"><i class="ti ti-lock lead"></i>
        <button type="button" class="eye" id="pwToggle" aria-label="show password"><i class="ti ti-eye-off"></i></button></div>
      <div id="capsWarn"><i class="ti ti-alert-triangle"></i> Caps Lock</div>
      <!--LOGIN_ERROR-->
      <label class="remember"><input type="checkbox" name="remember" value="1" checked><span data-i18n="remember">مرا به خاطر بسپار</span></label>
      <button class="go" type="submit" id="submitBtn"><span data-i18n="submit">ورود به پنل</span><i class="ti ti-login-2" id="goI"></i></button>
    </form>
    <div class="sep"><span data-i18n="or">یا</span></div>
    <button type="button" class="reg" onclick="openReg()"><i class="ti ti-user-plus a"></i><span data-i18n="regBtn">ثبت‌نام ادمینی</span><i class="ti ti-chevron-right ch"></i></button>
    <div class="notice"><b data-i18n="freeNotice1">این پنل رایگان است 💜</b><span data-i18n="freeNotice2">اگر به کارت آمد، به کانال رسمی بپیوند و حمایتش کن.</span><br><a class="tg" href="https://t.me/vodiwalkervpn03" target="_blank" rel="noopener"><i class="ti ti-brand-telegram"></i>Telegram Channel</a></div>
    <div class="foot">VODIWALKER · v18</div>
  </div>
</main>

<div class="ov" id="ov"><div class="box" role="dialog" aria-modal="true">
  <div class="bh"><div><span class="badge"><i class="ti ti-user-shield"></i><span data-i18n="regBadge">درخواست همکاری</span></span><h3 data-i18n="regTitle">ثبت‌نام ادمینی</h3><p data-i18n="regDesc">اطلاعاتت را بفرست؛ پس از تایید مالک، نام کاربری و رمز از طریق تلگرام برایت ارسال می‌شود.</p></div><button type="button" class="x" onclick="closeReg()" aria-label="close"><i class="ti ti-x"></i></button></div>
  <div class="inp"><input type="text" id="aregName" placeholder="نام و نام خانوادگی" data-i18n-placeholder="regNamePh" maxlength="80"><i class="ti ti-id lead"></i></div>
  <div class="inp"><input type="text" id="aregTg" dir="ltr" placeholder="@username" maxlength="64"><i class="ti ti-brand-telegram lead"></i></div>
  <div class="inp"><input type="text" id="aregNote" placeholder="توضیح (اختیاری)" data-i18n-placeholder="regNotePh" maxlength="300"><i class="ti ti-message lead"></i></div>
  <div id="aregMsg" class="msg"></div>
  <button class="go" type="button" id="aregBtn" onclick="submitReg()" style="height:52px;font-size:14px"><span data-i18n="regSubmit">ارسال درخواست</span><i class="ti ti-send"></i></button>
</div></div>

<script>
var I18N={
fa:{title:"ورود | VodiWalker",secure:"اتصال امن",hero:'کنترل کامل شبکه‌ات،<br><span class="g">حرفه‌ای و زنده</span>',heroP:"مدیریت اینباندها، کلاینت‌ها، اشتراک‌ها و پروکسی تلگرام در یک پنل واحد؛ با پریست مخصوص هر اپراتور (همراه اول، ایرانسل، مخابرات) و مانیتورینگ لحظه‌ای.",
 cardSmall:"حساب کاربری مدیر",cardTitle:"ورود به مرکز کنترل",cardP:"برای ادامه نام کاربری و رمز عبور خود را وارد کنید.",userPh:"نام کاربری",passPh:"رمز عبور",remember:"مرا به خاطر بسپار",submit:"ورود به پنل",or:"یا",regBtn:"ثبت‌نام ادمینی",
 freeNotice1:"این پنل رایگان است 💜",freeNotice2:"اگر به کارت آمد، به کانال رسمی بپیوند و حمایتش کن.",regBadge:"درخواست همکاری",regTitle:"ثبت‌نام ادمینی",regDesc:"اطلاعاتت را بفرست؛ پس از تایید مالک، نام کاربری و رمز از طریق تلگرام برایت ارسال می‌شود.",
 regNamePh:"نام و نام خانوادگی",regNotePh:"توضیح (اختیاری)",regSubmit:"ارسال درخواست",regNameErr:"نام را کامل وارد کن (حداقل ۳ حرف)",regTgErr:"آیدی تلگرام معتبر نیست",regSent:"درخواستت ارسال شد ✓",err:"خطایی رخ داد"},
en:{title:"Login | VodiWalker",secure:"Secure connection",hero:'Full control of your network,<br><span class="g">professional &amp; live</span>',heroP:"Manage inbounds, clients, subscriptions and your Telegram proxy from one panel — with per-operator presets (MCI, Irancell, TCI) and real-time monitoring.",
 cardSmall:"Admin account",cardTitle:"Sign in to Control Center",cardP:"Enter your username and password to continue.",userPh:"Username",passPh:"Password",remember:"Remember me",submit:"Sign in",or:"or",regBtn:"Admin registration",
 freeNotice1:"This panel is free 💜",freeNotice2:"If it helps you, join the official channel and support it.",regBadge:"Collaboration request",regTitle:"Admin registration",regDesc:"Send your details. If approved, your credentials arrive via Telegram.",
 regNamePh:"Full name",regNotePh:"Note (optional)",regSubmit:"Send request",regNameErr:"Enter your full name (min 3 chars)",regTgErr:"Invalid Telegram username",regSent:"Request sent ✓",err:"Something went wrong"}};
function $(i){return document.getElementById(i)}
function curLang(){try{var l=localStorage.getItem('vw_lang');return I18N[l]?l:'fa'}catch(e){return 'fa'}}
function applyLang(l){var d=I18N[l],h=$('htmlRoot');
 document.querySelectorAll('[data-i18n]').forEach(function(e){var k=e.getAttribute('data-i18n');if(d[k]!==undefined)e.innerHTML=d[k]});
 document.querySelectorAll('[data-i18n-placeholder]').forEach(function(e){var k=e.getAttribute('data-i18n-placeholder');if(d[k]!==undefined)e.placeholder=d[k]});
 document.title=d.title;h.lang=l;h.dir=l==='fa'?'rtl':'ltr';h.setAttribute('data-lang',l);$('langCur').textContent=l.toUpperCase();
 $('langFa').classList.toggle('cur',l==='fa');$('langEn').classList.toggle('cur',l==='en');$('goI').className='ti '+(l==='fa'?'ti-login-2':'ti-login-2')}
function setLang(l){try{localStorage.setItem('vw_lang',l)}catch(e){}applyLang(l);$('langMenu').classList.remove('on')}
applyLang(curLang());
$('langBtn').addEventListener('click',function(e){e.stopPropagation();var m=$('langMenu');m.classList.toggle('on');this.setAttribute('aria-expanded',m.classList.contains('on'))});
document.addEventListener('click',function(){$('langMenu').classList.remove('on')});
$('pwToggle').addEventListener('click',function(){var p=$('password'),s=p.type==='password';p.type=s?'text':'password';this.firstChild.className='ti '+(s?'ti-eye':'ti-eye-off')});
(function(){var p=$('password'),w=$('capsWarn');function c(e){w.style.display=(e.getModifierState&&e.getModifierState('CapsLock'))?'flex':'none'}p.addEventListener('keydown',c);p.addEventListener('keyup',c);p.addEventListener('blur',function(){w.style.display='none'})})();
$('loginForm').addEventListener('submit',function(){setTimeout(function(){$('submitBtn').classList.add('loading')},0)});
window.addEventListener('pageshow',function(){$('submitBtn').classList.remove('loading')});
function openReg(){$('aregMsg').style.display='none';$('ov').classList.add('on');setTimeout(function(){$('aregName').focus()},150)}
function closeReg(){$('ov').classList.remove('on')}
$('ov').addEventListener('click',function(e){if(e.target===this)closeReg()});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeReg()});
function regMsg(t,ok){var e=$('aregMsg');e.textContent=t;e.className='msg '+(ok?'ok':'err');e.style.display='block'}
async function submitReg(){var d=I18N[curLang()],n=$('aregName').value.trim(),tg=$('aregTg').value.trim().replace(/^@/,''),note=$('aregNote').value.trim();
 if(n.length<3){regMsg(d.regNameErr,false);return}if(!/^[A-Za-z0-9_]{3,64}$/.test(tg)){regMsg(d.regTgErr,false);return}
 var b=$('aregBtn');b.disabled=true;b.classList.add('loading');
 try{var r=await fetch('/api/admin-requests',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({full_name:n,telegram_id:tg,note:note})});
  var j={};try{j=await r.json()}catch(e){}if(!r.ok)throw new Error((typeof j.detail==='string'&&j.detail)||d.err);
  regMsg(d.regSent,true);$('aregName').value='';$('aregTg').value='';$('aregNote').value=''}
 catch(e){regMsg(e.message||d.err,false)}finally{b.disabled=false;b.classList.remove('loading')}}
['aregName','aregTg','aregNote'].forEach(function(id){$(id).addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();submitReg()}})});
(function(){var u=$('username'),p=$('password');if(document.querySelector('.error')){p.value='';setTimeout(function(){p.focus()},60)}
 else if(matchMedia('(hover:hover) and (pointer:fine)').matches){setTimeout(function(){u.focus()},80)}})();
/* animated network background */
(function(){var c=$('fx'),x=c.getContext('2d'),W,H,P=[],mx=-999,my=-999,rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
 function size(){W=c.width=innerWidth;H=c.height=innerHeight;var n=Math.min(70,Math.floor(W*H/22000));P=[];for(var i=0;i<n;i++)P.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.35,vy:(Math.random()-.5)*.35})}
 addEventListener('resize',size);addEventListener('pointermove',function(e){mx=e.clientX;my=e.clientY});size();
 function f(){x.clearRect(0,0,W,H);for(var i=0;i<P.length;i++){var a=P[i];if(!rm){a.x+=a.vx;a.y+=a.vy;if(a.x<0||a.x>W)a.vx*=-1;if(a.y<0||a.y>H)a.vy*=-1}
  x.fillStyle='rgba(167,139,250,.7)';x.beginPath();x.arc(a.x,a.y,1.4,0,6.3);x.fill();
  for(var j=i+1;j<P.length;j++){var b=P[j],dx=a.x-b.x,dy=a.y-b.y,d=dx*dx+dy*dy;if(d<17000){x.strokeStyle='rgba(124,92,255,'+(.22*(1-d/17000))+')';x.beginPath();x.moveTo(a.x,a.y);x.lineTo(b.x,b.y);x.stroke()}}
  var dx=a.x-mx,dy=a.y-my,d=dx*dx+dy*dy;if(d<24000){x.strokeStyle='rgba(34,211,238,'+(.4*(1-d/24000))+')';x.beginPath();x.moveTo(a.x,a.y);x.lineTo(mx,my);x.stroke()}}
  if(!rm)requestAnimationFrame(f)}f()})();
</script>
</body>
</html>
"""
