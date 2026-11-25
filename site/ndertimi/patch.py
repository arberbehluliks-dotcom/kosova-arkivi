def apply(s):
    def rep(a, b):
        nonlocal s
        assert a in s, a[:70]
        s = s.replace(a, b, 1)
    rep("""'<div class="in">' + esc(i.t) + '</div><div class="iv">' + esc(i.v) + '</div><div class="id">' + esc(i.d) + '</div>' +
    '<div class="is">Burimi: <a href="' + esc(i.url) + '" target="_blank" rel="noopener">' + esc(i.src) + '</a>' + alts + ' · ' + esc(i.when) + '</div></div>';""",
"""'<div class="in">' + esc(i.t) + '</div><div class="iv">' + esc(i.v) + '</div>' +
    '<details class="imore"><summary>Më shumë dhe burimi</summary><div class="id">' + esc(i.d) + '</div>' +
    '<div class="is">Burimi: <a href="' + esc(i.url) + '" target="_blank" rel="noopener">' + esc(i.src) + '</a>' + alts + ' · ' + esc(i.when) + '</div></details></div>';""")
    rep("""if (nd.length) parts.push("Plani i vitit 2024: " + nd[0][2] + " nga " + nd[0][3] + " aktivitete u realizuan.");
  else if (NDPN[SEC]) parts.push("Ministria nuk e raportoi statusin e " + NDPN[SEC] + " aktiviteteve të planit për 2024.");
  else if (NDPZ[SEC]) parts.push("Plani i publikuar për 2024 nuk ka aktivitete vjetore për këtë ministri.");""",
"""if (nd.length) parts.push("📋 Plani 2024: " + nd[0][2] + "/" + nd[0][3] + " aktivitete");
  else if (NDPN[SEC]) parts.push("📋 Plani 2024: statusi nuk u raportua");
  else if (NDPZ[SEC]) parts.push("📋 Plani 2024: pa aktivitete vjetore");""")
    rep("""parts.push("Lëvizja FOL: " + (c.done + c.late) + " nga " + fo.length + " objektiva kryesorë u realizuan" + (c.prog ? ", " + c.prog + " janë në proces" : "") + (c.fail ? ", " + c.fail + " kanë ngecur" : "") + ".");""",
"""parts.push("🎯 FOL: " + (c.done + c.late) + "/" + fo.length + " objektiva" + (c.fail ? " · " + c.fail + " ngecur" : ""));""")
    rep("""parts.push("Barometri i reformave evropiane: " + x[1] + " pikë nga 100.");""", """parts.push("🇪🇺 Reforma BE: " + x[1] + "/100");""")
    rep("""parts.push(n ? n + " tregues nga burime të tjera shihen më poshtë." : "Nuk ka ende tregues nga burime të tjera për këtë ministri.");
  $("sh-sum").textContent = parts.join(" ");""",
"""if (n) parts.push("📊 " + n + " tregues të tjerë");
  $("sh-sum").innerHTML = parts.map(function (t) { return '<span class="chipx">' + esc(t) + '</span>'; }).join("");""")
    rep("function applyData() { drawSectors(); drawMins(); drawEu(); drawInd(); drawClaims(); }",
"""function applyData() { drawSectors(); drawMins(); drawEu(); drawInd(); drawClaims();
  Array.prototype.forEach.call(document.querySelectorAll("#details .acc .cnt"), function (c) { if (c.textContent.trim() === "0") c.closest(".acc").hidden = true; });
}""")
    rep("</style>", """
#sh-sum{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 0}
.chipx{font-size:12.5px;font-weight:700;background:var(--brand-soft);color:var(--brand);border-radius:99px;padding:4px 10px}
body:not(.narr-on) .acc .body > .lead,body:not(.narr-on) #details > .lead,body:not(.narr-on) #details > section > .lead{display:none}
.ind .iv{font:800 17px/1.3 var(--font-display,inherit);color:var(--brand)}
.imore{font-size:12.5px;color:var(--muted)}.imore summary{cursor:pointer;font-weight:700}
.imore .id,.imore .is{margin-top:6px}
</style>""")

    for a, b in [
        ('<h3 class="p30sec" id="chh2">Objektivat e programit (FOL)</h3>', '<h3 class="p30sec" id="chh2">Objektivat e programit</h3>'),
        ('name: "Objektivat e programit (Lëvizja FOL)"', 'name: "Objektivat e programit"'),
        ('objektiva kryesorë të programit (Lëvizja FOL)"', 'objektiva kryesorë të programit"'),
        (' u realizuan (Lëvizja FOL)" }', ' u realizuan" }'),
        ('"🎯 FOL: "', '"🎯 Objektiva: "'),
        ('x.sec + " · FOL"', 'x.sec + " · Objektiv i programit"'),
        ('objektiva të ndjekur nga FOL</div>', 'objektiva të programit</div>'),
        ('ctx: "Lëvizja FOL · " + real', 'ctx: "Objektivat e programit · " + real'),
        ('ctx: s.n + " · Lëvizja FOL"', 'ctx: s.n + " · Objektiv i programit"'),
        ('<b>Objektivi përkatës i FOL:</b>', '<b>Objektivi përkatës i programit:</b>'),
        ('<p class="br-n">Objektivat kryesorë të ndjekur nga Lëvizja FOL, jo i gjithë programi.</p>', '<p class="br-n">Objektivat kryesorë të programit, jo i gjithë programi.</p>'),
        ("Sipas analizës së ' + x.via + '</div>'", "Burimi: ' + (x.via === 'FOL' ? 'Lëvizja FOL' : x.via) + ' · konfirmimi nga institucioni: në pritje</div>'"),
        ('<b>Mandat i arkivuar.</b> FOL e vlerësoi programin në fund të mandatit 2021-2025.', '<b>Mandat i arkivuar.</b> Statusi është vlerësuar në fund të mandatit 2021-2025 (burimi: Lëvizja FOL); konfirmimi nga institucionet shtohet kur të gjenden raportet e tyre.'),
    ]:
        if a in s: s = s.replace(a, b)
        else: print("MUNGON:", a[:60])
    return s

def apply2(s):
    def rep(a, b):
        nonlocal s
        assert a in s, a[:70]
        s = s.replace(a, b, 1)
    # burime të reja
    rep('var RS = {\n', 'var RS = {\n  vdem: ["V-Dem Institute, Democracy Report 2026", "https://www.v-dem.net/documents/75/V-Dem_Institute_Democracy_Report_2026_lowres.pdf"],\n  epi: ["Yale, Environmental Performance Index 2026", "https://epi.yale.edu/node/51152"],\n  heR: ["Heritage Foundation, Index of Economic Freedom 2026 (faqet e vendeve)", "https://static.heritage.org/index/pdf/2026/2026_indexofeconomicfreedom_kosovo.pdf"],\n  gpiR: ["Institute for Economics & Peace, Global Peace Index 2026", "https://www.visionofhumanity.org/wp-content/uploads/2026/06/Global-Peace-Index-2026-Report.pdf"],\n')
    # Heritage: krahasim rajonal
    rep('w: "Vendi 40 nga 44 në Evropë. Pika e fortë', 'hb: true, reg: [["Shqipëria", 68.0, "68.0"], ["Serbia", 65.0, "65.0"], ["Mali i Zi", 63.8, "63.8"], ["Maqedonia e Veriut", 63.3, "63.3"], ["Bosnja", 63.1, "63.1"], ["Kosova", 62.4, "62.4"]], w: "Vendi 40 nga 44 në Evropë. Pika e fortë')
    # GPI: krahasim rajonal (sipas vendit në botë)
    rep('rk: [54, 163], hb: false, s: "gpi"', 'rk: [54, 163], hb: false, reg: [["Mali i Zi", 30, "vendi 30"], ["Shqipëria", 36, "vendi 36"], ["Maqedonia e Veriut", 46, "vendi 46"], ["Bosnja", 48, "vendi 48"], ["Kosova", 54, "vendi 54"], ["Serbia", 70, "vendi 70"]], s: "gpi"')
    # kartë të re: V-Dem
    rep('''    { t: "Transparenca e buxhetit"''', '''    { t: "Lloji i regjimit", p: "V-Dem, Raporti 2026 (të dhëna 2025)", big: "Demokraci elektorale", of: "", sc: "Kosova është e vetmja në rajon e renditur pa shenjë paralajmëruese", tr: "", d: 0, w: "Mali i Zi: demokraci elektorale (me prirje përmirësimi). Maqedonia e Veriut: demokraci elektorale në zonë gri. Shqipëria dhe Bosnja: autokraci elektorale në zonë gri. Serbia: autokraci elektorale, me rënie të vazhdueshme që nga 2009.", s: "vdem" },
    { t: "Transparenca e buxhetit"''')
    # kartë të re: EPI
    rep('''  { g: "Mjedisi dhe ajri", ico: "🌫️", items: [''', '''  { g: "Mjedisi dhe ajri", ico: "🌫️", items: [
    { t: "Performanca mjedisore (EPI)", p: "Yale, EPI 2026", big: "–", of: "Kosova nuk përfshihet", sc: "Nuk është në tabelën e 177 vendeve", tr: "", d: 0, w: "Vendet e rajonit: Shqipëria 46., Mali i Zi 55., Maqedonia e Veriut 56., Serbia 69., Bosnja 76.", s: "epi" },''')
    return s

def apply3(s):
    def rep(a, b):
        nonlocal s
        assert a in s, a[:70]
        s = s.replace(a, b, 1)
    rep('var RS = {\n', 'var RS = {\n  btiR: ["Bertelsmann Stiftung, BTI 2026 (shifrat sipas përmbledhjes së European Western Balkans)", "https://europeanwesternbalkans.com/2026/03/27/serbia-classified-as-moderate-autocracy-other-wb-countries-as-defective-democracies/"],\n')
    def card(t, big, sc, reg, w):
        regs = ", ".join('["%s", %s, "%s"]' % (n, v, v) for n, v in reg)
        return '    { t: "%s", p: "Bertelsmann Stiftung, BTI 2026", big: "%s", of: "nga 10", sc: "%s", tr: "", d: 0, hb: true, reg: [%s], w: "%s", s: "btiR" },\n' % (t, big, sc, regs, w)
    new = (card("Transformimi politik në rajon (BTI)", "6.90", "Kosova: demokraci me të meta", [("Shqipëria",7.70),("Maqedonia e Veriut",7.65),("Mali i Zi",7.40),("Kosova",6.90),("Bosnja",5.95),("Serbia",5.18)], "Serbia klasifikohet autokraci e moderuar; Bosnja demokraci me shumë të meta; të tjerat demokraci me të meta.")
         + card("Transformimi ekonomik në rajon (BTI)", "6.21", "Kosova: i kufizuar", [("Mali i Zi",7.50),("Maqedonia e Veriut",7.18),("Shqipëria",7.11),("Serbia",6.79),("Bosnja",6.57),("Kosova",6.21)], "Kosova ka vlerësimin më të ulët në rajon për transformimin ekonomik.")
         + card("Qeverisja në rajon (BTI)", "4.81", "Kosova: qeverisje e moderuar", [("Shqipëria",6.71),("Maqedonia e Veriut",6.07),("Mali i Zi",5.90),("Kosova",4.81),("Bosnja",4.03),("Serbia",3.96)], "Vlerësimi i kapaciteteve të qeverisjes dhe i zbatimit të politikave."))
    rep('    { t: "Demokracia: vlerësimi 1-10"', new + '    { t: "Demokracia: vlerësimi 1-10"')
    return s
