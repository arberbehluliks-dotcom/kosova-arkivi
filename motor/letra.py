#!/usr/bin/env python3
"""Gjeneratori i letrave tremujore (PROVË, nuk dërgon asgjë).
Lexon PKZH dhe RZ nga site/index.html dhe krijon një letër për institucion.
Përdorimi: python3 motor/letra.py MASHTI MFPT -o dalja/   (pa argumente: të gjitha)"""
import re, sys, os, html, datetime, argparse

SRC = os.path.join(os.path.dirname(__file__), "..", "site", "index.html")
INST = {"MASHTI": "Ministria e Arsimit, Shkencës, Teknologjisë dhe Inovacionit", "MFPT": "Ministria e Financave, Punës dhe Transfereve",
        "MMPHI": "Ministria e Mjedisit, Planifikimit Hapësinor dhe Infrastrukturës", "ME": "Ministria e Ekonomisë",
        "MBPZHR": "Ministria e Bujqësisë, Pylltarisë dhe Zhvillimit Rural", "MSH": "Ministria e Shëndetësisë",
        "MKRS": "Ministria e Kulturës, Rinisë dhe Sportit", "MINT": "Ministria e Industrisë, Ndërmarrësisë dhe Tregtisë",
        "MAPL": "Ministria e Administrimit të Pushtetit Lokal", "DPTTIK": "Departamenti i Postës, Telekomunikacionit dhe TIK"}
UNK = {"Pa të dhëna", "Pretendim i Qeverisë, pa verifikim"}

def load():
    s = open(SRC, encoding="utf-8").read()
    i = s.index("var PKZH"); j = s.index("var RZ ="); e = s.index("var RZ_NONE")
    rows = []
    for m in re.finditer(r'\[\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"[^"]*"\s*(?:,\s*"(a)")?\s*\]', s[i:j]):
        rows.append(m.groups())
    rz = {m.group(1): (m.group(2), m.group(3)) for m in re.finditer(r'^  "([^"]+)": \["([^"]+)", "((?:[^"\\]|\\.)*)"\]', s[j:e], re.M)}
    return [r for r in rows if r[3] != "a"], rz

def letter(code, rows, rz):
    mine = [r for r in rows if r[0].split()[0] == code]
    if not mine: return None
    known = [r for r in mine if r[0] in rz and rz[r[0]][0] not in UNK]
    today = datetime.date.today().isoformat()
    o = [f"<!doctype html><meta charset=utf-8><title>Letër provë: {code}</title><body style='font:15px/1.5 system-ui;max-width:760px;margin:24px auto;padding:0 16px'>",
         f"<p><b>PROVË: nuk është dërguar.</b> Data e gjenerimit: {today}</p>",
         f"<h2>Njoftim tremujor për realizimin e planit: {html.escape(INST.get(code, code))}</h2>",
         "<p>Monitori i Planit është platformë qytetare që krahason Planin Strategjik dhe Operacional 2021-2025 me dëshmitë e pavarura. "
         "Më poshtë janë aktivitetet e institucionit tuaj dhe statusi ynë i tanishëm. Nëse keni dokument që e ndryshon një status, dërgojeni dhe do ta shqyrtojmë.</p>",
         f"<p><b>Mbulimi:</b> për {len(known)} nga {len(mine)} aktivitete të verifikuara me dokumentin kemi dëshmi të pavarur.</p>",
         "<table border=1 cellpadding=6 cellspacing=0 style='border-collapse:collapse;width:100%'><tr><th>Kodi</th><th>Aktiviteti</th><th>Buxheti</th><th>Statusi</th><th>Çka e ndryshon</th></tr>"]
    for r in sorted(mine, key=lambda x: x[0]):
        st, tx = rz.get(r[0], ("Pa të dhëna", ""))
        need = "Raport i pavarur ose dokument parësor për zbatimin" if st in UNK else "Dokument që e kundërshton burimin e cituar"
        o.append(f"<tr><td>{html.escape(r[0])}</td><td>{html.escape(r[1])}</td><td>{html.escape(r[2].split(' · ',1)[-1])}</td><td><b>{html.escape(st)}</b><br><small>{html.escape(tx)}</small></td><td>{need}</td></tr>")
    o += ["</table>", "<p><b>Rregulli:</b> „Realizuar“ jepet vetëm me dëshmi të pavarur. Raporti i vetë institucionit shfaqet si pretendim pa verifikim derisa të konfirmohet. Heshtja nuk numërohet si realizim.</p>",
          "<p>Afati i përgjigjes: 15 ditë pune. Përgjigjet shqyrtohen njësoj si çdo kërkesë korrigjimi dhe ruhen në historik.</p></body>"]
    return "\n".join(o)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("kodet", nargs="*"); ap.add_argument("-o", default="letra-prove")
    a = ap.parse_args(); rows, rz = load()
    codes = a.kodet or sorted({r[0].split()[0] for r in rows})
    os.makedirs(a.o, exist_ok=True)
    for c in codes:
        t = letter(c, rows, rz)
        if t: open(os.path.join(a.o, f"{c}.html"), "w", encoding="utf-8").write(t); print("OK", c)
