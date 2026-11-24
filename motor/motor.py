#!/usr/bin/env python3
"""Rregullat me "aktiv": true aplikohen. Të tjerat vetëm raportohen te "prova" në ndryshime.json, që të kontrollohen para aktivizimit.
Motori i mbledhjes: burimet -> leximi -> nxjerrja -> krahasimi -> version i ri.
Përdorim:  python3 motor.py --arkivi ../data --dalja ndryshime.json
Kërkon rrjet të hapur dhe, për PDF, pdfplumber (pip install pdfplumber requests).
Nuk shkruan asgjë në arkiv vetë: prodhon propozime që shqyrtohen para publikimit."""
import argparse, os, io, json, re, datetime, hashlib, sys
import requests
try: import pdfplumber
except ImportError: pdfplumber = None

def lexo(burimi):
    r = requests.get(burimi["url"], timeout=60, headers={"User-Agent": "MonitoriPlanit/1.0"})
    r.raise_for_status()
    hash_ = hashlib.sha256(r.content).hexdigest()
    if burimi["lloji"] == "pdf":
        if not pdfplumber: sys.exit("Mungon pdfplumber")
        with pdfplumber.open(io.BytesIO(r.content)) as p:
            tekst = "\n".join((pg.extract_text() or "") for pg in p.pages)
            tabela = [t for pg in p.pages for t in pg.extract_tables()]
    else:
        lidhje = "\n".join(f"{re.sub(r'<[^>]+>', ' ', t).strip()} => {h}" for h, t in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r.text, re.S))
        tekst, tabela = re.sub(r"<[^>]+>", " ", r.text) + "\n\nLIDHJET\n" + lidhje, []
    return tekst, tabela, hash_

def numri(s): return float(s.replace(",", "."))

def nxirr(tekst, rregulli):
    m = re.search(rregulli["regex"], tekst, re.I | re.S)
    return numri(m.group(1)) if m else None

def krahaso(obs, seria, periudha, vlera, sot):
    """Kthen një ndryshim ose None, sipas vlerës më të fundit për atë periudhë."""
    ekz = [o for o in obs if o["s"] == seria and o["p"] == periudha]
    if ekz:
        e = max(ekz, key=lambda o: (o["collected"], o["seq"]))
        if e["v"] == vlera: return None
        return {"lloji": "regjistrim i ri (korrigjim)", "seri": seria, "periudha": periudha, "e_vjetra": e["v"], "e_reja": vlera, "data": sot,
                "seq": e["seq"] + 1, "shqyrtim": abs(vlera - e["v"]) > max(1.0, abs(e["v"]) * 0.2)}
    return {"lloji": "periudhë e re", "seri": seria, "periudha": periudha, "e_vjetra": None, "e_reja": vlera, "data": sot, "seq": 1, "shqyrtim": False}

def main():
    a = argparse.ArgumentParser(); a.add_argument("--arkivi", default="../data"); a.add_argument("--dalja", default="ndryshime.json"); a.add_argument("--apliko", action="store_true")
    a = a.parse_args()
    sot = datetime.date.today().isoformat()
    obs = json.load(open(f"{a.arkivi}/observations.json", encoding="utf-8"))
    burimet = json.load(open("burimet.json", encoding="utf-8"))
    ndryshime, gabime, prova, perputhen = [], [], [], []
    for b in burimet:
        try: tekst, _, h = lexo(b)
        except Exception as e: gabime.append({"burimi": b["id"], "gabim": str(e)}); continue
        os.makedirs("../debug", exist_ok=True); open(f"../debug/{b['id']}.txt", "w", encoding="utf-8").write(tekst)
        for r in b["nxjerrjet"]:
            v = nxirr(tekst, r)
            if v is None: gabime.append({"burimi": b["id"], "seri": r["seri"], "gabim": "nuk u gjet vlera"}); continue
            if not r.get("aktiv"):
                prova.append({"burimi": b["id"], "seri": r["seri"], "periudha": r["periudha"], "vlera_e_gjetur": v}); continue
            nd = krahaso(obs, r["seri"], r["periudha"], v, sot)
            if nd is None: perputhen.append({"seri": r["seri"], "periudha": r["periudha"], "vlera": v})
            nd and nd.update(burimi_emri=b["emri"], metodologjia=b.get("metodologjia", "Sipas dokumentit të burimit"), publikuar=b.get("publikuar"))
            if nd: nd.update(burimi=b["url"], hash=h); ndryshime.append(nd)
    json.dump({"data": sot, "ndryshime": ndryshime, "prova": prova, "perputhen": perputhen, "gabime": gabime}, open(a.dalja, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(ndryshime), "ndryshime,", len(prova), "vlera prove (rregull jo aktiv),", len(gabime), "gabime")
    if a.apliko: apliko(a.arkivi, obs, ndryshime, sot)

def apliko(dir_, obs, ndryshime, sot):
    """Vetëm SHTON regjistrime. Asgjë nuk fshihet e nuk mbishkruhet. Të mëdhatë shkojnë te pending.json."""
    f = f"{dir_}/changes.json"
    log = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else []
    pending = [n for n in ndryshime if n["shqyrtim"]]
    for n in ndryshime:
        if n["shqyrtim"]: continue
        obs.append({"id": f'{n["seri"]}__{n["periudha"]}__{n["seq"]}', "s": n["seri"], "p": n["periudha"], "v": n["e_reja"], "f": 0,
                    "pub": n.get("publikuar"), "src": [{"t": n["burimi_emri"], "u": n["burimi"]}], "method": n["metodologjia"],
                    "collected": sot, "seq": n["seq"], "note": "Mbledhur nga motori; hash i dokumentit " + n["hash"][:12]})
        log.append({"ts": sot, "kind": n["lloji"], "target": n["seri"], "summary": f'{n["periudha"]}: {n["e_vjetra"]} -> {n["e_reja"]}'})
    if pending: log.append({"ts": sot, "kind": "për shqyrtim", "target": "Motori", "summary": f"{len(pending)} ndryshime të mëdha presin miratim në pending.json"})
    json.dump(pending, open(f"{dir_}/pending.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(obs, open(f"{dir_}/observations.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(log, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__": main()
