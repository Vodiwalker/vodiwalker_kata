# ui_dash.py — تم Aurora برای داشبورد + صفحه‌ی پروکسی تلگرام + انتخاب اپراتور
# patch_dashboard(html) روی DASHBOARD_HTML اصلی اعمال می‌شود.

THEME_CSS = r"""
/* ================= VodiWalker v18 · Aurora theme ================= */
:root{--accent:#7c5cff;--accent2:#22d3ee;--accent-d:#6246ea;--accent-rgb:124,92,255;--accent-soft:#c4b5fd;--ease:cubic-bezier(.22,.7,.2,1)}
html:not([data-theme="light"]){--bg:#060912;--panel:#0b1022;--panel2:#10172e;--line:#1a2342;--line2:#2b3868;
--good:#34d399;--warn:#fbbf24;--bad:#fb7185;--text:#eef2ff;--sub:#94a3c8;--sub2:#66739a;--glass:rgba(11,16,34,.72);
--card1:rgba(17,24,50,.78);--card2:rgba(10,15,34,.88);--tile:rgba(22,31,62,.72);--tile2:rgba(14,20,44,.82);--field:#0a1126;
--modal:linear-gradient(180deg,#141d3c,#0b1022);--side1:rgba(13,19,42,.92);--side2:rgba(7,10,24,.96);--hero-solid:rgb(10,15,34);--aurora:1;--shine:rgba(255,255,255,.04);--cardsh:rgba(0,0,0,.7)}
html[data-theme="light"]{--accent:#7c3aed;--card1:rgba(255,255,255,.96);--card2:rgba(250,251,255,.98);--tile:rgba(244,246,253,.95);--tile2:rgba(238,241,250,.95);--field:#ffffff;
--modal:linear-gradient(180deg,#ffffff,#f6f7fd);--side1:#ffffff;--side2:#f7f8fc;--hero-solid:rgb(246,247,255);--aurora:.0;--shine:rgba(255,255,255,.7);--cardsh:rgba(30,34,60,.18);--glass:rgba(255,255,255,.82)}
body{background:var(--bg)!important;position:relative}
body:before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;background:
 radial-gradient(50% 40% at 92% 0%,rgba(124,92,255,.20),transparent 70%),
 radial-gradient(45% 40% at 0% 100%,rgba(34,211,238,.12),transparent 70%);opacity:var(--aurora);animation:auroraShift 18s ease-in-out infinite alternate}
@keyframes auroraShift{to{transform:translate3d(-24px,18px,0) scale(1.06);opacity:.85}}
#app,.main,.sidebar,.topbar,.content{position:relative;z-index:1}
.sidebar{background:linear-gradient(180deg,var(--side1),var(--side2))!important;backdrop-filter:blur(18px);border-left:1px solid var(--line)!important}
html[dir=ltr] .sidebar{border-left:0!important;border-right:1px solid var(--line)!important}
.topbar{background:var(--glass)!important;backdrop-filter:blur(16px);border-bottom:1px solid var(--line)!important}
.tab{border-radius:14px!important;transition:transform .2s var(--ease),background .2s,color .2s!important}
.tab:hover{color:var(--text)!important;background:rgba(124,92,255,.10)!important;transform:translateX(-3px)}
html[dir=ltr] .tab:hover{transform:translateX(3px)}
.tab.on{background:linear-gradient(90deg,rgba(124,92,255,.30),rgba(34,211,238,.10))!important;box-shadow:inset 0 0 0 1px rgba(124,92,255,.45),0 10px 26px -10px rgba(124,92,255,.7)!important}
.tab i{transition:transform .25s var(--ease)}.tab:hover i,.tab.on i{transform:scale(1.14)}
.card{background:linear-gradient(180deg,var(--card1),var(--card2))!important;border:1px solid var(--line)!important;border-radius:20px!important;backdrop-filter:blur(10px);
 box-shadow:0 18px 44px -26px var(--cardsh),inset 0 1px 0 var(--shine);transition:transform .25s var(--ease),border-color .25s,box-shadow .25s}
.card:hover{border-color:var(--line2)!important;box-shadow:0 24px 54px -26px rgba(124,92,255,.45),inset 0 1px 0 rgba(255,255,255,.05)}
.btn{border-radius:12px!important;transition:transform .18s var(--ease),border-color .18s,background .18s,box-shadow .18s!important}
.btn:hover{transform:translateY(-1px)}.btn:active{transform:scale(.97)}
.btn.primary{background:linear-gradient(100deg,#5b4bff,#7c5cff 55%,#22a7e8)!important;border-color:transparent!important;box-shadow:0 12px 26px -12px rgba(100,90,255,.9)}
.btn.primary:hover{filter:brightness(1.1)}
.grp input,.grp select,.grp textarea,.sel{border-radius:12px!important;background:var(--field)!important;transition:border-color .18s,box-shadow .18s!important}
.grp input:focus,.grp select:focus,.grp textarea:focus,.sel:focus{border-color:var(--accent)!important;box-shadow:0 0 0 4px rgba(124,92,255,.2)!important}
.badge{backdrop-filter:blur(6px)}
.page.on{animation:pgIn .45s var(--ease) both}
@keyframes pgIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.live-dot{animation:pulseDot 1.8s ease-in-out infinite}
@keyframes pulseDot{50%{box-shadow:0 0 0 7px rgba(52,211,153,0)}0%{box-shadow:0 0 0 0 rgba(52,211,153,.55)}}
::-webkit-scrollbar{width:9px;height:9px}::-webkit-scrollbar-thumb{background:#243060;border-radius:9px}::-webkit-scrollbar-thumb:hover{background:#34448a}
@media(prefers-reduced-motion:reduce){body:before,.page.on,.live-dot{animation:none!important}}

/* ---- overview hero + polish ---- */
.vw-hero{position:relative;display:grid;grid-template-columns:1.1fr 1fr;gap:0;margin-bottom:16px;border-radius:26px;overflow:hidden;border:1px solid var(--line2);
 background:linear-gradient(120deg,rgba(124,92,255,.22),var(--hero-solid) 55%);box-shadow:0 30px 70px -36px rgba(124,92,255,.7);animation:pgIn .6s var(--ease) both}
.vw-hero .vh-txt{padding:26px 26px 22px;display:flex;flex-direction:column;justify-content:center;gap:12px;position:relative;z-index:1}
.vw-hero h2{font-size:24px;font-weight:900;line-height:1.6}.vw-hero h2 span{background:linear-gradient(90deg,#a78bfa,#22d3ee);-webkit-background-clip:text;background-clip:text;color:transparent}
.vw-hero p{font-size:12.5px;color:var(--sub);line-height:2}
.vh-actions{display:flex;flex-wrap:wrap;gap:8px}.vh-actions .btn{padding:9px 14px;font-size:12.5px}
.vh-chips{display:flex;flex-wrap:wrap;gap:8px}.vh-chips span{display:inline-flex;gap:6px;align-items:center;padding:6px 11px;border-radius:99px;font-size:11px;color:var(--sub);background:rgba(255,255,255,.05);border:1px solid var(--line)}
.vh-chips i{color:var(--accent2);font-size:15px}
.vw-hero .vh-img{position:relative;min-height:190px}
.vw-hero .vh-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 30%}
.vw-hero .vh-img:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,var(--hero-solid),transparent 45%)}
html[dir=ltr] .vw-hero .vh-img:before{background:linear-gradient(270deg,var(--hero-solid),transparent 45%)}
@media(max-width:820px){.vw-hero{grid-template-columns:1fr}.vw-hero .vh-img{order:-1;min-height:150px}.vw-hero .vh-img:before{background:linear-gradient(0deg,var(--hero-solid),transparent 60%)}}
.resource-card{position:relative;overflow:hidden;border-radius:18px!important;transition:transform .25s var(--ease),border-color .25s!important}
.resource-card:hover{transform:translateY(-4px);border-color:var(--line2)!important}
.resource-card:before{content:"";position:absolute;top:0;inset-inline:16px;height:2px;background:linear-gradient(90deg,transparent,var(--rcc,#7c5cff),transparent)}
.resource-card:nth-child(1){--rcc:#a78bfa}.resource-card:nth-child(2){--rcc:#22d3ee}.resource-card:nth-child(3){--rcc:#fbbf24}.resource-card:nth-child(4){--rcc:#34d399}.resource-card:nth-child(5){--rcc:#fb7185}.resource-card:nth-child(6){--rcc:#60a5fa}
.rc-head b{font-size:clamp(15px,1.5vw,21px)!important;white-space:nowrap}
.rc-head span i{color:var(--rcc,#a78bfa)}
.ov-quickstats>*{transition:transform .25s var(--ease),box-shadow .25s}.ov-quickstats>*:hover{transform:translateY(-3px);box-shadow:0 18px 36px -22px var(--accent)}
.pg-head h1{background:linear-gradient(90deg,#fff,#c4b5fd);-webkit-background-clip:text;background-clip:text;color:transparent}
html[data-theme=light] .pg-head h1{background:none;-webkit-background-clip:border-box;background-clip:border-box;color:var(--text)}

/* ---- default proxy banner ---- */
.tp-def{position:relative;display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center;margin-bottom:14px;padding:20px;border-radius:24px;border:1px solid rgba(124,92,255,.55);
 background:linear-gradient(120deg,rgba(124,92,255,.26),rgba(34,211,238,.10) 70%,var(--hero-solid));box-shadow:0 26px 60px -34px var(--accent)}
.tp-def h3{font-size:16px;font-weight:900;margin-bottom:4px;display:flex;align-items:center;gap:8px}.tp-def p{font-size:12px;color:var(--sub);line-height:1.9;margin-bottom:12px}
.tp-def .qr{width:132px;height:132px;border-radius:16px;background:#fff;padding:7px}.tp-def .qr img{width:100%;height:100%;display:block}
.tp-test{margin-bottom:14px}.tp-test .row2{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.tp-test .dc{padding:6px 11px;border-radius:99px;font-size:11px;border:1px solid var(--line);background:rgba(255,255,255,.04)}
.tp-test .dc.ok{color:#6ee7b7;border-color:rgba(52,211,153,.4)}.tp-test .dc.bad{color:#fda4af;border-color:rgba(251,113,133,.4)}
.tp-tip{margin-top:8px;padding:10px 12px;border-radius:12px;font-size:12px;line-height:1.9;background:rgba(251,191,36,.1);border:1px solid rgba(251,191,36,.35);color:#fde68a}
@media(max-width:640px){.tp-def{grid-template-columns:1fr}.tp-def .qr{margin:0 auto}}

/* ---- v18.2 professional polish ---- */
.nav-sec{margin:16px 14px 6px;font:700 10px 'Inter',system-ui,sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--sub2);display:flex;align-items:center;gap:8px}
.nav-sec:after{content:"";flex:1;height:1px;background:linear-gradient(90deg,var(--line),transparent)}
.nav-sec:first-child{margin-top:6px}
.tab{position:relative}
.tab.on:before{content:"";position:absolute;inset-block:9px;inset-inline-end:-1px;width:3px;border-radius:3px;background:linear-gradient(180deg,var(--accent),var(--accent2));box-shadow:0 0 12px var(--accent)}
.sidebar-brand{padding-bottom:14px;border-bottom:1px solid var(--line)}
.sidebar-brand img{border-radius:14px;box-shadow:0 0 0 1px var(--line2),0 10px 26px -10px var(--accent)}
.content{max-width:1560px;margin-inline:auto}
.pg-head{padding-bottom:14px;margin-bottom:16px;border-bottom:1px solid var(--line)}
.pg-head p{max-width:760px}
.eyebrow{width:max-content;max-width:100%;display:inline-flex;align-items:center;gap:8px;padding:5px 12px;border-radius:99px;background:rgba(var(--accent-rgb),.12);border:1px solid rgba(var(--accent-rgb),.28);font-size:10px!important;letter-spacing:.12em;color:var(--accent-soft)!important}
html[data-theme="light"] .eyebrow{color:var(--accent)!important}
.ib-quickstats>div{position:relative;overflow:hidden;border-radius:18px!important;transition:transform .25s var(--ease),border-color .25s,box-shadow .25s}
.ib-quickstats>div:hover{transform:translateY(-3px);border-color:var(--line2)!important;box-shadow:0 18px 38px -24px var(--qc,#7c5cff)}
.ib-quickstats>div>i{width:42px;height:42px;display:grid!important;place-items:center;border-radius:13px;font-size:21px!important;color:var(--qc,#a78bfa)!important;background:color-mix(in srgb,var(--qc,#7c5cff) 16%,transparent)!important}
.ib-quickstats>div:nth-child(1){--qc:#a78bfa}.ib-quickstats>div:nth-child(2){--qc:#34d399}.ib-quickstats>div:nth-child(3){--qc:#22d3ee}.ib-quickstats>div:nth-child(4){--qc:#fbbf24}.ib-quickstats>div:nth-child(5){--qc:#fb7185}.ib-quickstats>div:nth-child(6){--qc:#60a5fa}
.ib-quickstats b{font-size:21px!important;font-weight:900}
table{border-collapse:separate!important;border-spacing:0}
table thead th{position:sticky;top:0;z-index:2;background:var(--panel2)!important;font-size:11px!important;letter-spacing:.04em;color:var(--sub)!important;border-bottom:1px solid var(--line2)!important;padding-block:12px!important}
table tbody td{border-bottom:1px solid var(--line)!important}
table tbody tr:last-child td{border-bottom:0!important}
.badge{font-weight:800;letter-spacing:.02em}
.btn.danger:hover{box-shadow:0 10px 24px -12px var(--bad)}
.iconbtn{transition:transform .18s var(--ease),background .18s!important}.iconbtn:hover{transform:translateY(-2px) scale(1.06)}
.toast,#toast{border-radius:14px!important;backdrop-filter:blur(10px)}
.mini-panel,.rail-card,.traffic-card,.connection-card{border-radius:22px!important}
.panel-head b{font-weight:800}
.big-chart svg path[stroke]{filter:drop-shadow(0 4px 10px rgba(124,92,255,.45))}
.pg-head .toolbar .btn{padding:9px 14px}
::selection{background:rgba(var(--accent-rgb),.4)}

/* ---- operator picker ---- */
.op-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin:2px 0 6px}
.op-card{position:relative;padding:14px 10px 12px;border-radius:16px;border:1px solid var(--line);background:var(--tile);text-align:center;color:var(--sub);cursor:pointer;transition:.22s var(--ease)}
.op-card i{display:block;font-size:26px;margin-bottom:6px;color:var(--oc,#a78bfa);transition:transform .25s var(--ease)}
.op-card b{display:block;font-size:12.5px;color:var(--text)}.op-card small{display:block;font-size:10px;margin-top:3px;color:var(--sub2)}
.op-card:hover{transform:translateY(-3px);border-color:var(--oc,#7c5cff)}.op-card:hover i{transform:scale(1.15) rotate(-5deg)}
.op-card.on{border-color:var(--oc,#7c5cff);background:linear-gradient(180deg,color-mix(in srgb,var(--oc,#7c5cff) 22%,transparent),var(--tile));box-shadow:0 12px 28px -14px var(--oc,#7c5cff);color:var(--text)}
.op-card.on:after{content:"\eb7a";font-family:tabler-icons;position:absolute;top:6px;inset-inline-end:8px;font-size:15px;color:var(--oc,#7c5cff)}
.op-card .ed{position:absolute;top:5px;inset-inline-start:6px;width:24px;height:24px;display:grid;place-items:center;border-radius:8px;font-size:13px;color:var(--sub2);background:transparent;border:0}
.op-card .ed:hover{background:rgba(255,255,255,.1);color:#fff}
.op-note{font-size:11px;color:var(--sub2);line-height:1.9;margin-bottom:12px}

/* ---- telegram proxy page ---- */
.tp-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:14px}
.tp-stat{padding:16px;border-radius:18px;display:flex;align-items:center;gap:13px;border:1px solid var(--line);background:linear-gradient(180deg,var(--card1),var(--card2))}
.tp-stat .ic{width:46px;height:46px;border-radius:14px;display:grid;place-items:center;font-size:23px;background:rgba(124,92,255,.14);color:var(--c,#a78bfa)}
.tp-stat b{display:block;font-size:20px;font-weight:900}.tp-stat small{color:var(--sub2);font-size:11px}
.tp-srv{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:14px}
.tp-chip{display:flex;align-items:center;gap:8px;padding:9px 14px;border-radius:14px;border:1px solid var(--line);background:var(--tile);font-size:12px;color:var(--sub)}
.tp-chip i{font-size:17px}.tp-chip.ok i{color:var(--good)}.tp-chip.off i{color:var(--sub2)}.tp-chip.bad i{color:var(--bad)}
.tp-err{padding:11px 14px;border-radius:14px;margin-bottom:12px;font-size:12px;line-height:1.9;background:rgba(251,113,133,.1);border:1px solid rgba(251,113,133,.35);color:#fda4af}
.tp-kind{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}
.tp-kind label{display:flex;align-items:center;gap:10px;padding:12px;border-radius:14px;border:1px solid var(--line);background:var(--tile);cursor:pointer;font-size:12.5px;color:var(--sub);transition:.2s}
.tp-kind input{display:none}.tp-kind i{font-size:22px;color:#a78bfa}
.tp-kind label:has(input:checked){border-color:var(--accent);color:var(--text);background:rgba(124,92,255,.16);box-shadow:0 10px 24px -14px var(--accent)}
.tp-kind small{display:block;font-size:10px;color:var(--sub2)}
.tp-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:12px}
.tp-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px}
.tp-item{padding:16px;border-radius:20px;border:1px solid var(--line);background:linear-gradient(180deg,var(--card1),var(--card2));transition:.25s var(--ease);position:relative;overflow:hidden}
.tp-item:hover{transform:translateY(-3px);border-color:var(--line2);box-shadow:0 24px 50px -28px rgba(124,92,255,.6)}
.tp-item.dead{opacity:.62}
.tp-item:before{content:"";position:absolute;top:0;inset-inline:18px;height:2px;background:linear-gradient(90deg,transparent,var(--kc,#7c5cff),transparent)}
.tp-h{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.tp-h .av{width:42px;height:42px;border-radius:13px;display:grid;place-items:center;font-size:21px;background:rgba(124,92,255,.15);color:var(--kc,#a78bfa)}
.tp-h b{display:block;font-size:14px}.tp-h small{font-size:10.5px;color:var(--sub2)}
.tp-h .badge{margin-inline-start:auto}
.tp-bar{height:7px;border-radius:9px;background:rgba(255,255,255,.07);overflow:hidden;margin:6px 0 10px}
.tp-bar i{display:block;height:100%;border-radius:9px;background:linear-gradient(90deg,#7c5cff,#22d3ee);transition:width .6s var(--ease)}
.tp-bar.hi i{background:linear-gradient(90deg,#fbbf24,#fb7185)}
.tp-meta{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.tp-meta span{direction:ltr;unicode-bidi:isolate;font-size:10.5px;padding:4px 9px;border-radius:99px;background:rgba(255,255,255,.05);border:1px solid var(--line);color:var(--sub)}
.tp-link{display:flex;align-items:center;gap:8px;padding:9px 11px;border-radius:12px;background:var(--tile2);border:1px solid var(--line);margin-bottom:10px;direction:ltr}
.tp-link code{flex:1;min-width:0;font:11px ui-monospace,Menlo,monospace;color:#9ec5ff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tp-act{display:flex;flex-wrap:wrap;gap:7px}
.tp-act .btn{padding:7px 11px;font-size:11.5px}
.tp-qr{display:none;text-align:center;padding:10px 0 4px}.tp-qr.on{display:block}
.tp-qr img{width:176px;height:176px;border-radius:14px;background:#fff;padding:8px}
.tp-empty{grid-column:1/-1;text-align:center;padding:44px 16px;color:var(--sub2)}
.tp-empty i{font-size:46px;display:block;margin-bottom:10px;color:#4a5694}
.vw-ov{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;background:rgba(3,5,14,.78);backdrop-filter:blur(7px);padding:16px;animation:pgIn .25s both}
.vw-box{width:100%;max-width:440px;max-height:90vh;overflow:auto;padding:22px;border-radius:24px;background:var(--modal);border:1px solid var(--line2)}
.vw-box h3{font-size:16px;font-weight:900;margin-bottom:4px}.vw-box p{font-size:11.5px;color:var(--sub);line-height:1.9;margin-bottom:14px}
.vw-box .row{display:flex;gap:10px;margin-top:14px}.vw-box .row .btn{flex:1;justify-content:center}
/* ================= v19 · Pro layer + Telegram auto ================= */
.page.on>*{animation:pgIn .55s var(--ease) both}
.page.on>*:nth-child(2){animation-delay:.05s}.page.on>*:nth-child(3){animation-delay:.1s}.page.on>*:nth-child(4){animation-delay:.15s}.page.on>*:nth-child(n+5){animation-delay:.2s}
.rc-head b,.ib-quickstats b,.tp-stat b,.ov-quickstats b{font-variant-numeric:tabular-nums;letter-spacing:-.01em}
.btn:focus-visible,.tab:focus-visible,.iconbtn:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--accent2);outline-offset:2px}
.card,.resource-card,.tp-item,.tp-stat{position:relative}
.card:after{content:"";position:absolute;inset:0;border-radius:inherit;padding:1px;pointer-events:none;opacity:0;transition:opacity .35s;
 background:linear-gradient(135deg,rgba(var(--accent-rgb),.7),transparent 40%,rgba(34,211,238,.5));-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude}
.card:hover:after{opacity:1}
.sidebar{box-shadow:inset -1px 0 0 rgba(255,255,255,.03),24px 0 60px -40px rgba(0,0,0,.8)}
.tab{font-weight:700;letter-spacing:.005em}
.tab.on i{color:var(--accent2)}
.topbar{box-shadow:0 10px 30px -24px rgba(0,0,0,.8)}
.pg-head h1{letter-spacing:-.01em}
.badge.green{box-shadow:0 0 0 1px rgba(52,211,153,.25) inset}.badge.red{box-shadow:0 0 0 1px rgba(251,113,133,.25) inset}
table tbody tr{transition:background .18s}table tbody tr:hover td{background:rgba(var(--accent-rgb),.06)!important}
html[data-theme="light"] ::-webkit-scrollbar-thumb{background:#c5cbe0}
.vw-ov{position:fixed;inset:0;z-index:80;display:grid;place-items:center;padding:16px;background:rgba(3,6,16,.62);backdrop-filter:blur(8px);animation:pgIn .25s var(--ease) both}
.vw-box{width:min(480px,100%);max-height:90vh;overflow:auto;padding:22px;border-radius:22px;border:1px solid var(--line2);background:var(--modal);box-shadow:0 40px 90px -30px rgba(0,0,0,.85)}
.vw-box h3{font-size:16px;font-weight:900;margin-bottom:6px}.vw-box p{font-size:12px;color:var(--sub);line-height:1.9;margin-bottom:12px}
.vw-box .row{display:flex;gap:8px;justify-content:flex-end;margin-top:16px}

/* ---- Telegram proxy · AUTO ---- */
.tp-auto{position:relative;display:grid;grid-template-columns:auto 1fr;gap:28px;align-items:center;padding:28px;margin-bottom:14px;border-radius:28px;overflow:hidden;
 border:1px solid rgba(var(--accent-rgb),.5);background:radial-gradient(90% 140% at 0% 0%,rgba(var(--accent-rgb),.30),transparent 62%),radial-gradient(70% 100% at 100% 100%,rgba(34,211,238,.14),transparent 60%),linear-gradient(180deg,var(--card1),var(--card2));
 box-shadow:0 34px 80px -42px var(--accent)}
.tp-auto:before{content:"";position:absolute;inset:-40%;background:conic-gradient(from 0deg,transparent 0 70%,rgba(var(--accent-rgb),.16) 85%,transparent);animation:taSweep 9s linear infinite;pointer-events:none}
@keyframes taSweep{to{transform:rotate(360deg)}}
.ta-orb{position:relative;width:132px;height:132px;display:grid;place-items:center;flex:none;z-index:1}
.ta-orb:before{content:"";position:absolute;inset:20px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));box-shadow:0 0 46px rgba(var(--accent-rgb),.75),inset 0 2px 0 rgba(255,255,255,.35)}
.ta-orb i{position:relative;font-size:52px;color:#fff;filter:drop-shadow(0 6px 14px rgba(0,0,0,.35));transition:transform .4s var(--ease)}
.ta-orb .r{position:absolute;inset:0;border-radius:50%;border:1.5px solid rgba(var(--accent-rgb),.55);animation:taPulse 3.2s ease-out infinite}
.ta-orb .r2{animation-delay:1.06s}.ta-orb .r3{animation-delay:2.12s}
@keyframes taPulse{0%{transform:scale(.6);opacity:.95}100%{transform:scale(1.4);opacity:0}}
.tp-auto.busy .ta-orb:before{animation:taSpin 1.1s linear infinite;background:conic-gradient(from 0deg,var(--accent2),var(--accent),var(--accent2))}
.tp-auto.busy .ta-orb i{transform:scale(.88)}
@keyframes taSpin{to{transform:rotate(360deg)}}
.ta-body{position:relative;z-index:1;min-width:0}
.ta-body h2{font-size:22px;font-weight:900;margin-bottom:6px;display:flex;align-items:center;gap:10px}
.ta-body h2 em{font-style:normal;font-size:10px;font-weight:800;letter-spacing:.14em;padding:4px 10px;border-radius:99px;color:#fff;background:linear-gradient(90deg,var(--accent),var(--accent2))}
.ta-body>p{font-size:12.5px;color:var(--sub);line-height:2;max-width:620px;margin-bottom:14px}
.ta-actions{display:flex;flex-wrap:wrap;gap:10px}
.ta-go{padding:13px 22px!important;font-size:14px!important;font-weight:900;gap:10px;display:inline-flex;align-items:center;position:relative;overflow:hidden}
.ta-go:after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.35) 50%,transparent 70%);transform:translateX(-120%);animation:taShine 3.4s ease-in-out infinite}
@keyframes taShine{60%,100%{transform:translateX(120%)}}
.ta-go[disabled]{opacity:.8;cursor:progress}
.ta-steps{display:grid;gap:8px;margin-top:16px;max-width:620px}
.ta-step{display:flex;align-items:center;gap:10px;padding:10px 13px;border-radius:13px;font-size:12px;color:var(--sub);background:var(--tile);border:1px solid var(--line);opacity:0;transform:translateY(8px);animation:taIn .5s var(--ease) forwards}
.ta-step i{font-size:18px;flex:none}.ta-step.ok i{color:var(--good)}.ta-step.bad i{color:var(--bad)}.ta-step.bad{border-color:rgba(251,113,133,.4)}
.ta-dcs{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}
.ta-dcs span{padding:3px 9px;border-radius:99px;font-size:10.5px;direction:ltr;border:1px solid var(--line)}.ta-dcs .ok{color:#6ee7b7;border-color:rgba(52,211,153,.4)}.ta-dcs .bad{color:#fda4af;border-color:rgba(251,113,133,.4)}
@keyframes taIn{to{opacity:1;transform:none}}
@media(max-width:700px){.tp-auto{grid-template-columns:1fr;text-align:center;padding:22px}.ta-orb{margin:0 auto}.ta-body h2,.ta-actions{justify-content:center}.ta-step{text-align:start}}
@media(prefers-reduced-motion:reduce){.tp-auto:before,.ta-orb .r,.ta-go:after,.page.on>*{animation:none!important}.ta-step{opacity:1;transform:none;animation:none}}

"""

OVERVIEW_HERO = '''
      <div class="vw-hero"><div class="vh-txt"><div class="eyebrow"><span class="live-dot"></span> VODIWALKER · CONTROL CENTER</div>
        <h2>خوش آمدی به <span>مرکز کنترل VodiWalker</span></h2>
        <p>اینباندها، کلاینت‌ها (با پریست اپراتور)، اشتراک‌ها و پروکسی تلگرام را از یک‌جا مدیریت کن.</p>
        <div class="vh-actions"><button class="btn primary" onclick="gotoPage('clientmgr')"><i class="ti ti-user-plus"></i>ساخت کلاینت</button><button class="btn" onclick="gotoPage('tgproxy')"><i class="ti ti-brand-telegram"></i>پروکسی تلگرام</button><button class="btn" onclick="gotoPage('links')"><i class="ti ti-network"></i>اینباندها</button></div>
        <div class="vh-chips"><span><i class="ti ti-antenna-bars-5"></i>پریست اپراتورها</span><span><i class="ti ti-shield-lock"></i>MTProto داخلی</span><span><i class="ti ti-activity"></i>مانیتورینگ زنده</span></div></div>
        <div class="vh-img"><img src="/assets/vw-hero.jpg" alt="VodiWalker"></div></div>
'''

TGPROXY_TAB = '''<div class="tab" data-pg="tgproxy"><i class="ti ti-brand-telegram"></i><span data-i18n="nav_tgproxy">پروکسی تلگرام</span></div>
      '''

TGPROXY_PAGE = r'''
    <!-- TELEGRAM PROXY · AUTO -->
    <div class="page" id="pg-tgproxy">
      <div class="pg-head"><div><div class="eyebrow"><span class="live-dot"></span> VODIWALKER · TELEGRAM PROXY</div><h1>پروکسی تلگرام</h1>
        <p>فقط حالت خودکار: یک دکمه بزن و بهترین پروکسی ممکن برای همین سرور ساخته و آماده‌ی اتصال می‌شود.</p></div>
        <div class="toolbar"><button class="btn" onclick="loadTgProxy()"><i class="ti ti-refresh"></i>بروزرسانی</button></div></div>
      <div id="tpTop"></div>
      <section class="tp-auto" id="tpAuto">
        <div class="ta-orb"><span class="r r1"></span><span class="r r2"></span><span class="r r3"></span><i class="ti ti-brand-telegram"></i></div>
        <div class="ta-body">
          <h2>حالت خودکار <em>AUTO</em></h2>
          <p>سرور اتصال خودش به دیتاسنترهای تلگرام را می‌سنجد، بهترین پورت را انتخاب و فعال می‌کند، یک secret اختصاصی (dd · padded) می‌سازد و لینک «اتصال در تلگرام» را همراه QR تحویل می‌دهد. نیازی به تنظیم دستی نیست.</p>
          <div class="ta-actions">
            <button class="btn primary ta-go" id="taGo" onclick="tpAuto(false)"><i class="ti ti-wand"></i><span>خودکار — بهترین پروکسی را بساز</span></button>
            <button class="btn" id="taNew" onclick="tpAuto(true)"><i class="ti ti-plus"></i>پروکسی جدید (برای کاربر دیگر)</button>
          </div>
          <div class="ta-steps" id="taSteps"></div>
        </div>
      </section>
      <div id="tpDefault"></div>
      <div class="tp-list" id="tpList"></div>
    </div>
'''

DASH_JS = r'''
<script>
/* ===================== v18 · operators + telegram proxy ===================== */
let OPS = {}, OP_SEL = 'all';
async function loadOperators(){ try{ const r = await api('/api/operators'); OPS = r.operators || {}; }catch(e){} }
function opName(k){ return k==='all' ? 'همه' : ((OPS[k]||{}).name || k); }
function opPickerHtml(){
  const keys = Object.keys(OPS);
  const card = (k,name,sub,icon,color)=>`<div class="op-card ${OP_SEL===k?'on':''}" style="--oc:${color}" data-op="${k}" onclick="pickOp('${k}')"><i class="ti ${icon}"></i><b>${name}</b><small>${sub}</small>${k!=='all'?`<button class="ed" title="ویرایش پریست" onclick="event.stopPropagation();editOpPreset('${k}')"><i class="ti ti-settings"></i></button>`:''}</div>`;
  return `<div class="grp"><label>اپراتور کاربر</label><div class="op-grid">
    ${card('all','همه اپراتورها','یک ساب · چند کانفیگ','ti-world','#34d399')}
    ${keys.map(k=>{const o=OPS[k];return card(k,escapeHtml(o.name),'fragment: '+o.fragment,o.icon,o.color)}).join('')}
  </div><div class="op-note">«همه اپراتورها» برای هر اپراتورِ فعال یک کانفیگ با پریست مخصوصش می‌سازد و همه را در یک لینک اشتراک می‌گذارد؛ برنامه‌ی کاربر خودش بهترین را انتخاب می‌کند. پریست‌ها (fragment، fingerprint، Clean IP) با دکمه‌ی ⚙ قابل ویرایش‌اند.</div></div>`;
}
function pickOp(k){ OP_SEL = k; document.querySelectorAll('.op-card').forEach(c=>c.classList.toggle('on', c.dataset.op===k)); }
function vwModal(html){ const o=document.createElement('div'); o.className='vw-ov'; o.innerHTML=`<div class="vw-box">${html}</div>`; o.addEventListener('click',e=>{if(e.target===o)o.remove()}); document.body.appendChild(o); return o; }
async function editOpPreset(k){
  const o = OPS[k]; if(!o) return;
  const fr = ['off','safe','balanced','aggressive'], fp = ['chrome','firefox','safari','ios','android','edge','random','randomized'];
  const m = vwModal(`<h3>پریست ${escapeHtml(o.name)}</h3><p>این مقادیر روی هر کلاینتِ جدید این اپراتور اعمال می‌شود. شرایط شبکه در هر شهر فرق دارد؛ با تست واقعی تنظیم کن.</p>
   <div class="grp"><label>Fragment</label><select id="opFr">${fr.map(x=>`<option ${x===o.fragment?'selected':''}>${x}</option>`).join('')}</select></div>
   <div class="grp" style="margin-top:10px"><label>Fingerprint</label><select id="opFp">${fp.map(x=>`<option ${x===o.fingerprint?'selected':''}>${x}</option>`).join('')}</select></div>
   <div class="grp" style="margin-top:10px"><label>ALPN (اختیاری)</label><input id="opAlpn" dir="ltr" value="${escapeHtml(o.alpn||'')}" placeholder="h2,http/1.1"></div>
   <div class="grp" style="margin-top:10px"><label>Clean IP ها (هر خط یکی، اختیاری)</label><textarea id="opIps" dir="ltr" rows="4" style="resize:vertical">${escapeHtml((o.clean_ips||[]).join('\n'))}</textarea></div>
   <label class="remember" style="display:flex;gap:8px;align-items:center;margin-top:10px;font-size:12px;color:var(--sub)"><input type="checkbox" id="opEn" ${o.enabled!==false?'checked':''}> فعال (در «همه اپراتورها» لحاظ شود)</label>
   <div class="row"><button class="btn" id="opCancel">انصراف</button><button class="btn primary" id="opSave">ذخیره</button></div>`);
  m.querySelector('#opCancel').onclick = ()=>m.remove();
  m.querySelector('#opSave').onclick = async ()=>{
    try{
      await api('/api/operators/'+k, {method:'POST', body: JSON.stringify({fragment:m.querySelector('#opFr').value, fingerprint:m.querySelector('#opFp').value, alpn:m.querySelector('#opAlpn').value, clean_ips:m.querySelector('#opIps').value, enabled:m.querySelector('#opEn').checked})});
      await loadOperators(); m.remove(); toast('پریست ذخیره شد ✓');
      if(CM_SELECTED_UID) loadClientManagerClients(CM_SELECTED_UID);
    }catch(e){ toast(e.message,false); }
  };
}
/* createClientMgr با انتخاب اپراتور */
createClientMgr = async function(uid){
  const label = $('cmClientName').value.trim();
  const limit = Number($('cmClientLimit').value) || 0;
  const days = Number($('cmClientDays').value) || 0;
  const parent = (typeof CM_INBOUNDS!=='undefined' && CM_INBOUNDS.find(x=>x.uuid===uid)) || {};
  const outbound_proxy_id = await askOutboundChoice({title:'ساخت کلاینت', sub:'این کلاینت از کجا خارج شود؟', current: parent.outbound_proxy_id||''});
  if(outbound_proxy_id===null) return;
  try{
    const r = await api(`/api/links/${uid}/clients`, {method:'POST', body: JSON.stringify({label, limit_bytes: limit ? limit*1024*1024*1024 : 0, expires_days: days, outbound_proxy_id, operator: OP_SEL})});
    loadClientManagerClients(uid);
    if(r.combo){ showClientPairResult(r); } else { toast('کلاینت برای '+opName(OP_SEL)+' ساخته شد ✓'); }
  }catch(e){ toast(e.message,false); }
};

/* ---------------- Telegram proxy page ---------------- */
let TP = null, TP_LAST = null;
const tpFmt = b => (typeof fmtBytes==='function') ? fmtBytes(b||0) : (b||0)+' B';
async function loadTgProxy(){
  try{ TP = await api('/api/tgproxy'); renderTgProxy(); }catch(e){ toast(e.message,false); }
}
function renderTgProxy(){
  const s = TP.settings, st = TP.stats, run = TP.running, errs = Object.values(TP.errors||{});
  $('tpTop').innerHTML = `
   ${errs.map(e=>`<div class="tp-err"><i class="ti ti-alert-triangle"></i> ${escapeHtml(e)}</div>`).join('')}
   <div class="tp-stats">
     <div class="tp-stat" style="--c:#a78bfa"><div class="ic"><i class="ti ti-brand-telegram"></i></div><div><b>${st.total}</b><small>کل پروکسی‌ها</small></div></div>
     <div class="tp-stat" style="--c:#34d399"><div class="ic"><i class="ti ti-circle-check"></i></div><div><b>${st.active}</b><small>فعال</small></div></div>
     <div class="tp-stat" style="--c:#22d3ee"><div class="ic"><i class="ti ti-activity"></i></div><div><b>${st.live}</b><small>اتصال زنده</small></div></div>
     <div class="tp-stat" style="--c:#fbbf24"><div class="ic"><i class="ti ti-arrows-exchange"></i></div><div><b>${tpFmt(st.used_bytes)}</b><small>ترافیک کل</small></div></div>
   </div>
   <div class="tp-srv">
     <div class="tp-chip ${run.mtproto?'ok':'bad'}"><i class="ti ti-${run.mtproto?'circle-check':'circle-x'}"></i>MTProto · ${run.shared?'روی پورت پنل (مشترک)':'پورت '+(s.mt_port||'—')} · ${run.mtproto?'در حال اجرا':'خاموش'}</div>
     <div class="tp-chip ${run.socks?'ok':'off'}"><i class="ti ti-${run.socks?'circle-check':'power'}"></i>SOCKS5 · ${s.socks_port?('پورت '+s.socks_port):'غیرفعال'}</div>
     <div class="tp-chip"><i class="ti ti-server"></i>${escapeHtml(s.public_host||TP.host)}</div>
   </div>`;
  const def = (TP_LAST && TP.items.find(x=>x.id===TP_LAST)) || TP.items.find(x=>x.auto && x.usable) || TP.items.find(x=>x.default && x.kind==='mtproto') || TP.items.find(x=>x.kind==='mtproto' && x.usable);
  $('tpDefault').innerHTML = def ? `<div class="tp-def"><div><h3><i class="ti ti-brand-telegram" style="color:#22d3ee"></i>پروکسی آماده · ${escapeHtml(def.label)}</h3>
      <p>روی دکمه بزن، تلگرام باز می‌شود و پروکسی را با یک «Connect» اضافه می‌کنی. همین لینک را برای کاربرها هم می‌توانی بفرستی.</p>
      <div class="tp-act"><a class="btn primary" href="${escapeHtml(def.links.tg)}"><i class="ti ti-brand-telegram"></i>افزودن به تلگرام</a><a class="btn" href="${escapeHtml(def.links.web)}" target="_blank" rel="noopener"><i class="ti ti-external-link"></i>لینک t.me</a><button class="btn" onclick="copyText('${escapeHtml(def.links.tg)}','لینک کپی شد ✓')"><i class="ti ti-copy"></i>کپی</button></div>
      <div style="margin-top:10px;font:11px ui-monospace,monospace;color:var(--sub2);direction:ltr">${escapeHtml(def.links.server)}:${def.links.port}</div></div>
      <div class="qr"><img alt="QR" src="${qrSrc(def.links.web)}"></div></div>` : '';
  const items = TP.items;
  $('tpList').innerHTML = items.length ? items.map(tpCard).join('') : `<div class="tp-empty"><i class="ti ti-brand-telegram"></i>هنوز پروکسی نساختی. دکمه‌ی «خودکار» را بزن.</div>`;
}
function tpCard(p){
  const lim = p.limit_bytes||0, pct = lim ? Math.min(100, Math.round((p.used_bytes||0)/lim*100)) : 0, isMt = p.kind==='mtproto';
  const exp = p.expires_at ? p.expires_at.slice(0,10) : '∞';
  const st = !p.enabled ? ['gray','خاموش'] : p.expired ? ['red','منقضی'] : (lim && p.used_bytes>=lim) ? ['red','حجم تمام'] : ['green','فعال'];
  const L = p.links;
  return `<article class="tp-item ${p.usable?'':'dead'}" style="--kc:${isMt?'#7c5cff':'#22d3ee'}">
    <div class="tp-h"><div class="av"><i class="ti ti-${isMt?'shield-lock':'plug-connected'}"></i></div><div><b>${escapeHtml(p.label)}</b><small>${isMt?'MTProto':'SOCKS5'} · ${p.created_at.slice(0,10)}</small></div><span class="badge ${st[0]}">${st[1]}</span></div>
    <div class="tp-meta"><span><i class="ti ti-arrows-exchange"></i> ${tpFmt(p.used_bytes)}${lim?' / '+tpFmt(lim):' / ∞'}</span><span><i class="ti ti-calendar"></i> ${exp}</span><span><i class="ti ti-activity"></i> ${p.live} زنده${p.max_conn?' / '+p.max_conn:''}</span></div>
    ${lim?`<div class="tp-bar ${pct>85?'hi':''}"><i style="width:${pct}%"></i></div>`:''}
    <div class="tp-link"><code>${escapeHtml(L.tg)}</code><button class="iconbtn" title="کپی" onclick="copyText('${escapeHtml(L.tg)}','لینک کپی شد ✓')"><i class="ti ti-copy"></i></button></div>
    <div class="tp-qr" id="tpqr-${p.id}"><img alt="QR" src="${qrSrc(L.web)}"></div>
    <div class="tp-act">
      <a class="btn primary" href="${escapeHtml(L.web)}" target="_blank" rel="noopener"><i class="ti ti-brand-telegram"></i>اتصال در تلگرام</a>
      <button class="btn" onclick="copyText('${escapeHtml(L.web)}','لینک t.me کپی شد ✓')"><i class="ti ti-link"></i>t.me</button>
      <button class="btn" onclick="document.getElementById('tpqr-${p.id}').classList.toggle('on')"><i class="ti ti-qrcode"></i>QR</button>
      <button class="btn" onclick="tpToggle('${p.id}',${!p.enabled})"><i class="ti ti-power"></i>${p.enabled?'خاموش':'روشن'}</button>
      <button class="btn" onclick="tpEdit('${p.id}')"><i class="ti ti-edit"></i></button>
      <button class="btn" title="ریست حجم" onclick="tpReset('${p.id}')"><i class="ti ti-refresh"></i></button>
      <button class="btn" title="${isMt?'secret':'پسورد'} جدید" onclick="tpRegen('${p.id}')"><i class="ti ti-key"></i></button>
      <button class="btn danger" onclick="tpDel('${p.id}')"><i class="ti ti-trash"></i></button>
    </div></article>`;
}
async function tpCreate(){
  const kind = document.querySelector('input[name=tpKind]:checked').value;
  try{
    const r = await api('/api/tgproxy',{method:'POST',body:JSON.stringify({kind,label:$('tpLabel').value.trim(),limit_gb:Number($('tpGb').value)||0,days:Number($('tpDays').value)||0,max_conn:Number($('tpConn').value)||0})});
    $('tpLabel').value=''; toast(r.warning||'پروکسی ساخته شد ✓', !r.warning); loadTgProxy();
  }catch(e){ toast(e.message,false); }
}

async function tpAuto(fresh){
  const box = $('tpAuto'), go = $('taGo'), nw = $('taNew'), out = $('taSteps');
  if(box.classList.contains('busy')) return;
  box.classList.add('busy'); go.disabled = true; nw.disabled = true;
  const label = go.querySelector('span'); const keep = label.textContent; label.textContent = 'در حال بررسی و ساخت…';
  out.innerHTML = `<div class="ta-step" style="animation-delay:0s"><i class="ti ti-loader-2"></i><span>سنجش اتصال به تلگرام و انتخاب بهترین مسیر…</span></div>`;
  try{
    const r = await api('/api/tgproxy/auto',{method:'POST',body:JSON.stringify({fresh:!!fresh})});
    TP_LAST = r.item && r.item.id;
    out.innerHTML = r.steps.map((st,i)=>`<div class="ta-step ${st.ok?'ok':'bad'}" style="animation-delay:${(i*0.28).toFixed(2)}s"><i class="ti ti-${st.ok?'circle-check':'alert-triangle'}"></i><div style="min-width:0"><span>${escapeHtml(st.text)}</span>${st.dcs?`<div class="ta-dcs">${st.dcs.map(d=>`<span class="${d.ok?'ok':'bad'}">DC${d.dc} · ${d.ok?d.ms+'ms':'ناموفق'}</span>`).join('')}</div>`:''}</div></div>`).join('')
      + (r.healthy ? '' : `<div class="tp-tip"><i class="ti ti-alert-triangle"></i> اتصال کامل نیست؛ اگر دیتاسنترها ناموفق‌اند، این هاست خروجی تلگرام را بسته و MTProto روی آن کار نمی‌کند. روی سرور دیگری امتحان کن.</div>`);
    await loadTgProxy();
    toast(r.healthy ? 'بهترین پروکسی آماده شد ✓' : 'پروکسی ساخته شد، اما اتصال سرور مشکل دارد', !!r.healthy);
    const d = $('tpDefault'); if(d && d.firstElementChild) setTimeout(()=>d.scrollIntoView({behavior:'smooth',block:'nearest'}), r.steps.length*280+200);
  }catch(e){ out.innerHTML = `<div class="ta-step bad" style="animation-delay:0s"><i class="ti ti-alert-triangle"></i><span>${escapeHtml(e.message)}</span></div>`; toast(e.message,false); }
  box.classList.remove('busy'); go.disabled = false; nw.disabled = false; label.textContent = keep;
}
async function tpToggle(id,en){ try{ await api('/api/tgproxy/'+id,{method:'PATCH',body:JSON.stringify({enabled:en})}); loadTgProxy(); }catch(e){toast(e.message,false)} }
async function tpReset(id){ if(!confirm('حجم مصرفی صفر شود؟'))return; try{ await api('/api/tgproxy/'+id+'/reset',{method:'POST'}); toast('ریست شد ✓'); loadTgProxy(); }catch(e){toast(e.message,false)} }
async function tpRegen(id){ if(!confirm('لینک قبلی از کار می‌افتد و باید لینک جدید را برای کاربر بفرستی. ادامه؟'))return; try{ await api('/api/tgproxy/'+id+'/regenerate',{method:'POST'}); toast('لینک جدید صادر شد ✓'); loadTgProxy(); }catch(e){toast(e.message,false)} }
async function tpDel(id){ if(!confirm('این پروکسی حذف شود؟'))return; try{ await api('/api/tgproxy/'+id,{method:'DELETE'}); toast('حذف شد'); loadTgProxy(); }catch(e){toast(e.message,false)} }
function tpEdit(id){
  const p = TP.items.find(x=>x.id===id); if(!p) return;
  const m = vwModal(`<h3>ویرایش پروکسی</h3><p>حجم و انقضا را دوباره تنظیم کن (انقضا از «امروز» محاسبه می‌شود).</p>
   <div class="grp"><label>نام</label><input id="teL" value="${escapeHtml(p.label)}"></div>
   <div class="grp" style="margin-top:10px"><label>حجم GB (0 = نامحدود)</label><input id="teG" type="number" min="0" step="0.5" value="${p.limit_bytes?(p.limit_bytes/1073741824).toFixed(2):0}"></div>
   <div class="grp" style="margin-top:10px"><label>انقضا از امروز (روز، 0 = ندارد)</label><input id="teD" type="number" min="0" value="0"></div>
   <div class="grp" style="margin-top:10px"><label>سقف اتصال هم‌زمان</label><input id="teC" type="number" min="0" value="${p.max_conn||0}"></div>
   <div class="row"><button class="btn" id="teX">انصراف</button><button class="btn primary" id="teS">ذخیره</button></div>`);
  m.querySelector('#teX').onclick=()=>m.remove();
  m.querySelector('#teS').onclick=async()=>{ try{
    const b={label:m.querySelector('#teL').value,limit_gb:Number(m.querySelector('#teG').value)||0,max_conn:Number(m.querySelector('#teC').value)||0};
    const d=Number(m.querySelector('#teD').value)||0; if(d>0||!p.expires_at) b.days=d;
    await api('/api/tgproxy/'+id,{method:'PATCH',body:JSON.stringify(b)}); m.remove(); toast('ذخیره شد ✓'); loadTgProxy();
  }catch(e){toast(e.message,false)} };
}
async function tpSelfTest(btn){
  btn.disabled=true; $('tpTestOut').innerHTML='<div style="margin-top:10px;color:var(--sub2);font-size:12px">در حال تست…</div>';
  try{
    const r=await api('/api/tgproxy-selftest');
    $('tpTestOut').innerHTML=`<div class="row2"><span class="tp-chip ${r.listening?'ok':'bad'}"><i class="ti ti-${r.listening?'circle-check':'circle-x'}"></i>سرور پروکسی ${r.listening?'فعال':'خاموش'} ${r.shared?'(پورت پنل)':''}</span><span class="tp-chip"><i class="ti ti-plug-connected"></i>پورت در لینک: ${r.link_port||'—'}</span>${r.dcs.map(d=>`<span class="dc ${d.ok?'ok':'bad'}">DC${d.dc} · ${d.ok?d.ms+'ms':'ناموفق'}</span>`).join('')}</div>${(r.tips||[]).map(t=>`<div class="tp-tip"><i class="ti ti-alert-triangle"></i> ${escapeHtml(t)}</div>`).join('')||'<div style="margin-top:10px;color:var(--good);font-size:12px"><i class="ti ti-circle-check"></i> همه چیز سالم است؛ لینک را در تلگرام امتحان کن.</div>'}`;
  }catch(e){ $('tpTestOut').innerHTML=`<div class="tp-tip">${escapeHtml(e.message)}</div>`; }
  btn.disabled=false;
}
function tpSettings(){
  const s = TP.settings;
  const m = vwModal(`<h3>تنظیمات سرور پروکسی</h3><p>پورت‌ها باید روی هاستت باز و از بیرون قابل دسترس باشند (روی هاست‌های تک‌پورتی، پورت اضافه از پنل هاست بگیر). همه‌ی پروکسی‌ها روی همین پورت مشترک سرو می‌شوند.</p>
   <label style="display:flex;gap:8px;align-items:center;margin-bottom:12px;font-size:12px;color:var(--sub)"><input type="checkbox" id="tsSh" ${s.share_panel_port!==false?'checked':''}> MTProto روی همان پورت پنل سرو شود (برای هاست‌های تک‌پورتی مثل KataBump؛ پیشنهادی)</label>
   <div class="grp"><label>پورت MTProto جدا (فقط وقتی اشتراک پورت خاموش است)</label><input id="tsM" type="number" value="${s.mt_port||0}"></div>
   <div class="grp" style="margin-top:10px"><label>پورت عمومی در لینک (0 = خودکار از آدرس پنل)</label><input id="tsPP" type="number" value="${s.public_port||0}"></div>
   <div class="grp" style="margin-top:10px"><label>پورت SOCKS5 (0 = غیرفعال)</label><input id="tsS" type="number" value="${s.socks_port||0}"></div>
   <div class="grp" style="margin-top:10px"><label>آدرس عمومی سرور (دامنه یا IP؛ خالی = آدرس فعلی پنل)</label><input id="tsH" dir="ltr" value="${escapeHtml(s.public_host||'')}" placeholder="${escapeHtml(TP.host)}"></div>
   <label style="display:flex;gap:8px;align-items:center;margin-top:12px;font-size:12px;color:var(--sub)"><input type="checkbox" id="tsT" ${s.socks_tg_only!==false?'checked':''}> SOCKS5 فقط به سرورهای تلگرام وصل شود (امن‌تر)</label>
   <label style="display:flex;gap:8px;align-items:center;margin-top:8px;font-size:12px;color:var(--sub)"><input type="checkbox" id="tsE" ${s.enabled?'checked':''}> سرویس پروکسی تلگرام فعال باشد</label>
   <div class="row"><button class="btn" id="tsX">انصراف</button><button class="btn primary" id="tsOk">ذخیره و اعمال</button></div>`);
  m.querySelector('#tsX').onclick=()=>m.remove();
  m.querySelector('#tsOk').onclick=async()=>{ try{
    await api('/api/tgproxy-settings',{method:'POST',body:JSON.stringify({share_panel_port:m.querySelector('#tsSh').checked,public_port:Number(m.querySelector('#tsPP').value)||0,mt_port:Number(m.querySelector('#tsM').value)||0,socks_port:Number(m.querySelector('#tsS').value)||0,public_host:m.querySelector('#tsH').value,socks_tg_only:m.querySelector('#tsT').checked,enabled:m.querySelector('#tsE').checked})});
    m.remove(); toast('تنظیمات اعمال شد ✓'); loadTgProxy();
  }catch(e){toast(e.message,false)} };
}
loadOperators();
(function navSections(){
  const map={overview:'نمای کلی',links:'سرویس‌ها',nodes:'زیرساخت',admins:'مدیریت'};
  document.querySelectorAll('.sidebar .tab[data-pg]').forEach(t=>{
    const k=t.getAttribute('data-pg'); if(map[k] && !t.previousElementSibling?.classList?.contains('nav-sec')){
      const d=document.createElement('div'); d.className='nav-sec'; d.textContent=map[k]; t.parentNode.insertBefore(d,t);
    }
  });
})();
</script>
'''


def patch_dashboard(html: str) -> str:
    def rep(old, new, count=1):
        nonlocal html
        if html.count(old) != count:
            raise RuntimeError(f"dashboard anchor not unique/missing ({html.count(old)}): {old[:60]!r}")
        html = html.replace(old, new)

    # theme (آخرین <style> قبل از </head> تا override کند)
    rep("</head>", "<style>" + THEME_CSS + "</style>\n</head>")
    rep('<div class="ov-shell"><div class="ov-main">', OVERVIEW_HERO + '<div class="ov-shell"><div class="ov-main">')
    # nav tab + page
    rep('<div class="tab" data-pg="admins">', TGPROXY_TAB + '<div class="tab" data-pg="admins">')
    rep('<div class="page" id="pg-settings">', TGPROXY_PAGE + '\n    <div class="page" id="pg-settings">')
    # loader / titles / search index
    rep("settings:()=>{loadSettings();loadDiagnostics();}};",
        "settings:()=>{loadSettings();loadDiagnostics();}, tgproxy:()=>{loadTgProxy();}};")
    rep("nav_overview:'داشبورد',",
        "nav_overview:'داشبورد', nav_tgproxy:'پروکسی تلگرام', pt_tgproxy:'ساخت و مدیریت پروکسی MTProto / SOCKS5 تلگرام برای کاربران',")
    rep("nav_overview:'Overview',",
        "nav_overview:'Overview', nav_tgproxy:'Telegram Proxy', pt_tgproxy:'Create and manage MTProto / SOCKS5 Telegram proxies',")
    rep("['clientmgr','ساخت کلاینت','client manager کاربر مشتری','ti-user-plus'],",
        "['clientmgr','ساخت کلاینت','client manager کاربر مشتری','ti-user-plus'],\n    ['tgproxy','پروکسی تلگرام','telegram proxy mtproto socks پروکسی تلگرام','ti-brand-telegram'],")
    # operator picker داخل فرم ساخت کلاینت
    rep("""onclick="createClientMgr('${uid}')"><i class="ti ti-user-plus"></i>ساخت کلاینت واقعی</button>""",
        """onclick="createClientMgr('${uid}')"><i class="ti ti-user-plus"></i>ساخت کلاینت</button>""")
    rep("""          <button class="btn primary" style="width:100%" onclick="createClientMgr('${uid}')">""",
        """          ${opPickerHtml()}
          <button class="btn primary" style="width:100%" onclick="createClientMgr('${uid}')">""")
    # نمایش اپراتور در لیست کلاینت‌ها (فقط لیست مدیریت کلاینت)
    rep("""<div class="client-tags"><span>${c.active?'فعال':'خاموش'}</span>""",
        """<div class="client-tags">${c.operator?`<span style="color:${(OPS[c.operator]||{}).color||'#a78bfa'}">${escapeHtml(opName(c.operator))}</span>`:''}<span>${c.active?'فعال':'خاموش'}</span>""", count=_count_client_tags(html))
    # script
    rep("</body>", DASH_JS + "\n</body>")
    return html


def _count_client_tags(html: str) -> int:
    return html.count("""<div class="client-tags"><span>${c.active?'فعال':'خاموش'}</span>""")
