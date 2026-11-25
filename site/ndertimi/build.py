import json,os,runpy,re
os.chdir('../ballina'); g=runpy.run_path('gen.py'); os.chdir('../v4')
D=json.dumps(g['data'],ensure_ascii=False)
s=open('../monitori-v3.html',encoding='utf-8').read()
css='''
#paswrap{--pg-good:#177a45;--pg-goodbg:#e0f3e8;--pg-bad:#c2372d;--pg-badbg:#fbe4e1;--pg-same:#7a6a2a;--pg-samebg:#f4eed3;display:grid;gap:26px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) #paswrap{--pg-good:#6fd69a;--pg-goodbg:#173a28;--pg-bad:#ff8a7e;--pg-badbg:#42201d;--pg-same:#e4cf7c;--pg-samebg:#3a3519}}
:root[data-theme="dark"] #paswrap{--pg-good:#6fd69a;--pg-goodbg:#173a28;--pg-bad:#ff8a7e;--pg-badbg:#42201d;--pg-same:#e4cf7c;--pg-samebg:#3a3519}
#paswrap h2.pz-s{font:800 20px/1.2 var(--font-display,inherit);margin:0 0 10px}
.pz-calc,.pz-ans{background:var(--surface);border:1.5px solid var(--line);border-radius:18px;padding:18px;display:grid;grid-template-columns:minmax(0,1fr);gap:14px}
.pz-in{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.pz-in input{flex:1;min-width:120px;font:800 28px var(--font-display,inherit);color:var(--fg);background:var(--bg);border:1.5px solid var(--line);border-radius:14px;padding:10px 14px}
.pz-seg{display:flex;border:1.5px solid var(--line);border-radius:12px;overflow:hidden}
.pz-seg button{border:0;background:transparent;color:var(--muted);font:inherit;font-size:14px;font-weight:700;padding:10px 12px;cursor:pointer}
.pz-seg button.on{background:var(--brand);color:#fff}
.pz-split{display:flex;height:18px;border-radius:99px;overflow:hidden;background:var(--track)}
.pz-split i{display:block}
.pz-ln{display:grid;gap:6px;font-size:15px}.pz-ln div{display:flex;justify-content:space-between;gap:10px}
.pz-ln .tot{font-weight:800;font-size:18px;border-top:1px solid var(--line);padding-top:8px}
.pz-dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
.pz-sub{color:var(--muted);font-size:13px}
.pz-tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.pz-tile{background:var(--surface);border:1.5px solid var(--line);border-radius:16px;padding:14px;text-align:left;font:inherit;color:inherit;cursor:pointer;display:grid;gap:5px;min-width:0}
.pz-tile:hover{border-color:var(--brand)}
.pz-tile .ic{font-size:24px}.pz-tile .t{font-size:13px;color:var(--muted)}.pz-tile .n{font:800 26px var(--font-display,inherit);color:var(--brand)}
.pz-v{display:inline-flex;border-radius:999px;padding:5px 11px;font-weight:700;font-size:13px;width:fit-content}
.pz-v.good{background:var(--pg-goodbg);color:var(--pg-good)}.pz-v.bad{background:var(--pg-badbg);color:var(--pg-bad)}.pz-v.same,.pz-v.na{background:var(--pg-samebg);color:var(--pg-same)}
.pz-ans h2{margin:0;font-size:16px;color:var(--muted);font-weight:700}
.pz-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px}
.pz-big{font:800 clamp(38px,11vw,60px)/1 var(--font-display,inherit);color:var(--brand)}
#paswrap details{font-size:13px;color:var(--muted);border-top:1px solid var(--line);padding-top:10px}
#paswrap summary{cursor:pointer;font-weight:700}
.pz-news{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.pz-news button{background:var(--surface);border:1.5px solid var(--line);border-radius:16px;padding:14px;text-align:left;font:inherit;color:inherit;cursor:pointer}
.pz-news .t{font-size:12px;color:var(--muted)}.pz-news .n{font:800 24px var(--font-display,inherit);color:var(--brand);margin:4px 0}
</style>'''
s=s.replace('</style>',css,1)
tiles='''      <button type="button" class="tile" data-m="pas"><span class="ti" aria-hidden="true">💶</span><h2>Sa më mbetet nga paga?</h2><div class="tn"><span id="t-pas">639</span><small> € neto nga paga mesatare</small></div><div class="tl">Llogaritës nga bruto në neto, me pensionin dhe tatimin sipas ligjit në fuqi.</div><span class="tg">Llogarit →</span></button>
      <button type="button" class="tile" data-m="pas"><span class="ti" aria-hidden="true">🛒</span><h2>Sa po shtrenjtohet jeta?</h2><div class="tn">__INFL__<small>% inflacioni vjetor, tetor 2026</small></div><div class="tl">Çmimet, punësimi dhe tregtia, të dhënat e fundit nga ASK dhe BQK.</div><span class="tg">Shiko →</span></button>
'''
tiles=tiles.replace('__INFL__',str(g['data']['tiles'][0]['v']))
i0=s.index('<button type="button" class="tile" data-m="krah">'); i1=s.index('\n',i0)+1
s=s[:i1]+tiles+s[i1:]
s=s.replace('      <button type="button" data-m="eco" aria-pressed="false">Ekonomia</button>','      <button type="button" data-m="pas" aria-pressed="false">Paga dhe çmimet</button>\n      <button type="button" data-m="eco" aria-pressed="false">Ekonomia</button>',1)
sec='''  <section id="paswrap" hidden>
    <div><h1>Paga dhe çmimet</h1><p class="lead">Çfarë të mbetet nga paga dhe si po ecën çmimet, puna dhe tregtia.</p></div>
    <div><h2 class="pz-s">Sa më mbetet nga paga?</h2><div class="pz-calc">
      <div class="pz-in"><input id="pz-pg" type="number" inputmode="decimal" min="0" value="713" aria-label="Paga mujore në euro"><span>€ në muaj</span><div class="pz-seg" id="pz-mode"><button type="button" data-m="g" class="on">Kam bruto</button><button type="button" data-m="n">Kam neto</button></div></div>
      <div class="pz-split" id="pz-spl"></div><div class="pz-ln" id="pz-ln"></div>
      <details><summary>Si llogaritet dhe nga vjen</summary><div>Paga bruto minus kontributi pensional i punëtorit (5%) jep pagën e tatueshme. Tatimi: 0% deri në 250 €, 8% nga 250 € deri në 450 €, 10% mbi 450 € në muaj (Ligji nr. 05/L-028 për Tatimin në të Ardhurat Personale, ndryshuar me Ligjin nr. 08/L-142). Punëdhënësi paguan veç 5% kontribut pensional. Llogaritja është indikative: nuk përfshin lehtësira të veçanta, punë të dyta apo shtetas të huaj. Burime: <a href="https://crmm.atk-ks.org/sq/Public/CalculatorDetail?id=17" target="_blank" rel="noopener">Administrata Tatimore e Kosovës</a>, <a href="https://taxsummaries.pwc.com/kosovo/individual/taxes-on-personal-income" target="_blank" rel="noopener">PwC Worldwide Tax Summaries (rishikuar 07.08.2026)</a>. Për shumat zyrtare përdor llogaritësin e ATK-së.</div></details>
    </div></div>
    <div><h2 class="pz-s">Si po ecën jeta</h2><div class="pz-tiles" id="pz-tiles"></div></div>
    <div id="pz-ans"></div>
    <div><h2 class="pz-s">E reja në të dhëna</h2><div class="pz-news" id="pz-news"></div><p class="pz-sub" id="pz-ft"></p></div>
  </section>
'''
s=s.replace('  <section id="ecowrap" hidden>',sec+'  <section id="ecowrap" hidden>',1)
s=s.replace('  $("ecowrap").hidden = searching || M !== "eco";','  $("ecowrap").hidden = searching || M !== "eco";\n  $("paswrap").hidden = searching || M !== "pas";',1)
s=s.replace('|min|kom|','|min|pas|kom|',1) if '|min|kom|' in s else s
s=s.replace('(min|kom|eu|','(min|pas|kom|eu|',1)
s=s.replace('home || M === "about"','home || M === "pas" || M === "about"',1)
js='''
(function(){
var D='''+D+''';
var g=function(i){return document.getElementById(i)};
var esc=function(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};
var IC={price:"🛒",work:"💼",wage:"💶",growth:"📈",export:"🚢"};
var VT={good:"↗ Më mirë se një vit më parë",bad:"↘ Më keq se një vit më parë",same:"→ Pothuajse njësoj si një vit më parë",na:"Pa krahasim të besueshëm"};
function fmt(v,u){var n=(+v).toLocaleString("sq",{maximumFractionDigits:v>=1000?0:1});return u==="%"?n+"%":u==="€"?n+" €":u==="mln €"?n+" mln €":u==="mld €"?n+" mld €":n+(u?" "+esc(u):"")}
function src(a){return '<details><summary>Burimi dhe metodologjia</summary><div>'+esc(a.src)+' · periudha '+esc(a.p)+(a.pub?' · publikuar '+esc(a.pub):' · data e publikimit nuk është e verifikuar')+'.<br>'+esc(a.m)+(a.url?'<br><a href="'+esc(a.url)+'" target="_blank" rel="noopener">Hap burimin</a>':'')+'</div></details>'}
function answer(q,items){g("pz-ans").innerHTML='<div class="pz-ans"><h2>'+esc(q)+'</h2><div class="pz-row">'+items.map(function(a){return '<div style="display:grid;gap:8px"><div class="pz-sub">'+esc(a.title||a.t)+'</div><div class="pz-big">'+fmt(a.v,a.u)+'</div>'+(a.st?'<span class="pz-v '+a.st+'">'+VT[a.st]+'</span>':'')+'<div class="pz-sub">'+esc(a.p)+(a.prev?' · '+esc(a.prev.p)+': '+fmt(a.prev.v,a.u):'')+'</div>'+src(a)+'</div>'}).join('')+'</div></div>';g("pz-ans").scrollIntoView({behavior:"smooth",block:"nearest"})}
g("pz-tiles").innerHTML=D.tiles.map(function(t,i){return '<button type="button" class="pz-tile" data-i="'+i+'"><span class="ic">'+IC[t.ik]+'</span><span class="t">'+esc(t.title)+'</span><span class="n">'+fmt(t.v,t.u)+'</span><span class="pz-v '+t.st+'">'+{good:"↗ më mirë",bad:"↘ më keq",same:"→ njësoj",na:"—"}[t.st]+'</span></button>'}).join("");
g("pz-tiles").onclick=function(e){var b=e.target.closest(".pz-tile");if(b){var t=D.tiles[b.dataset.i];answer(t.title,[t])}};
g("pz-news").innerHTML=D.news.map(function(a,i){return '<button type="button" data-i="'+i+'"><div class="t">'+esc(a.t)+'</div><div class="n">'+fmt(a.v,a.u)+'</div><div class="pz-sub">'+esc(a.p)+'</div></button>'}).join("");
g("pz-news").onclick=function(e){var b=e.target.closest("button");if(b){var a=D.news[b.dataset.i];answer(a.t,[a])}};
g("pz-ft").textContent=D.n_obs+" vëzhgime nga "+D.n_ser+" tregues · përditësuar "+D.upd+" · çdo shifër ka burim, periudhë dhe metodologji";
function bn(G){var pen=G*.05,tx=G-pen,t=tx<=250?0:tx<=450?(tx-250)*.08:16+(tx-450)*.10;return{g:G,pen:pen,t:t,n:G-pen-t,emp:G*.05}}
function ng(n){var lo=n,hi=n*2+500;for(var i=0;i<60;i++){var m=(lo+hi)/2;bn(m).n<n?lo=m:hi=m}return(lo+hi)/2}
var MD="g";
function calc(){var v=Math.max(0,parseFloat(g("pz-pg").value)||0),r=bn(MD==="g"?v:ng(v));var f=function(x){return x.toLocaleString("sq",{minimumFractionDigits:2,maximumFractionDigits:2})+" €"};var p=function(x){return r.g?x/r.g*100:0};
g("pz-spl").innerHTML='<i style="width:'+p(r.n)+'%;background:var(--pg-good)"></i><i style="width:'+p(r.pen)+'%;background:var(--gold)"></i><i style="width:'+p(r.t)+'%;background:var(--pg-bad)"></i>';
g("pz-ln").innerHTML='<div><span><span class="pz-dot" style="background:var(--pg-good)"></span>Të mbeten (neto)</span><b>'+f(r.n)+'</b></div><div><span><span class="pz-dot" style="background:var(--gold)"></span>Pensioni yt (5%)</span><span>'+f(r.pen)+'</span></div><div><span><span class="pz-dot" style="background:var(--pg-bad)"></span>Tatimi në pagë</span><span>'+f(r.t)+'</span></div><div class="tot"><span>Paga bruto</span><span>'+f(r.g)+'</span></div><div class="pz-sub"><span>Kosto totale për punëdhënësin (bruto + 5% pension)</span><span>'+f(r.g+r.emp)+'</span></div>'}
g("pz-pg").oninput=calc;
g("pz-mode").onclick=function(e){var b=e.target.closest("button");if(!b)return;MD=b.dataset.m;Array.prototype.forEach.call(g("pz-mode").children,function(x){x.classList.toggle("on",x===b)});calc()};
calc();
})();
'''
i=s.rindex('</script>')
s=s[:i]+js+s[i:]
import patch
s=patch.apply3(patch.apply2(patch.apply(s)))
open('monitori-v4.html','w',encoding='utf-8').write(s)
print(len(s))
