# KUJDES: mos e ri-ndërto faqen nga këtu

Që nga nëntori 2026, **`site/index.html` është burimi i vërtetë**. Ndryshimet e shumta të mëvonshme
(shtresa e realizimit, matësi i mbulimit, treguesit e rinj, korrigjimet e auditimit) janë bërë vetëm atje.
`baza-v3.html`, `build.py`, `gen.py` dhe `patch.py` janë të vjetruara: nëse ekzekutohen dhe shkruajnë mbi
`site/index.html`, do të humbasin ato ndryshime.

Para çdo rindërtimi: krahaso me `git diff` dhe sill ndryshimet e `site/index.html` në ndërtues së pari.
