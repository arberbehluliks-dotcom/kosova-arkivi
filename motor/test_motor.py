"""Prova pa rrjet: kontrollon logjikën e nxjerrjes, krahasimit dhe shtimit vetëm-shtim."""
import json, os, shutil, tempfile, motor

TEKST = "Inflacioni mesatar në tremujorin e dytë arriti 6,8 % ndërsa kreditë u rritën 12,5 %."

def test_nxjerrja():
    r = {"regex": r"inflacion\w*[^.]{0,120}?(\d+[.,]\d)\s*%"}
    assert motor.nxirr(TEKST, r) == 6.8
    assert motor.nxirr("asgjë këtu", r) is None

def test_krahasimi():
    obs = [{"id": "a__00", "s": "a", "p": "T2", "v": 6.0, "collected": "2026-11-01", "seq": 1}]
    assert motor.krahaso(obs, "a", "T2", 6.0, "2026-11-24") is None
    n = motor.krahaso(obs, "a", "T2", 6.5, "2026-11-24")
    assert n["seq"] == 2 and n["shqyrtim"] is False
    assert motor.krahaso(obs, "a", "T2", 9.9, "2026-11-24")["shqyrtim"] is True
    assert motor.krahaso(obs, "a", "T3", 7.0, "2026-11-24")["lloji"] == "periudhë e re"

def test_vetem_shtim():
    d = tempfile.mkdtemp()
    obs = [{"id": "a__00", "s": "a", "p": "T2", "v": 6.0, "collected": "2026-11-01", "seq": 1}]
    nd = [{"lloji": "x", "seri": "a", "periudha": "T2", "e_vjetra": 6.0, "e_reja": 6.5, "data": "2026-11-24", "seq": 2, "shqyrtim": False,
           "burimi": "u", "burimi_emri": "B", "metodologjia": "m", "publikuar": None, "hash": "0" * 64},
          {"lloji": "x", "seri": "a", "periudha": "T3", "e_vjetra": None, "e_reja": 99.0, "data": "2026-11-24", "seq": 1, "shqyrtim": True,
           "burimi": "u", "burimi_emri": "B", "metodologjia": "m", "publikuar": None, "hash": "0" * 64}]
    motor.apliko(d, obs, nd, "2026-11-24")
    saved = json.load(open(f"{d}/observations.json"))
    assert len(saved) == 2 and saved[0]["v"] == 6.0 and saved[1]["v"] == 6.5   # e vjetra mbetet
    assert len(json.load(open(f"{d}/pending.json"))) == 1                       # e madhja pret miratim
    shutil.rmtree(d)

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print("OK", n)
