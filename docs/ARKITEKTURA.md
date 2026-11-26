# Monitori i Planit: arkitektura

## Parimi
Të dhënat dhe kodi jetojnë këtu (GitHub), jo në bisedë. Faqja është vetëm një pamje e të dhënave.

## Shtresat
1. **Të dhënat** (`data/`): vëzhgime të shtuara pa fshirë historikun; çdo vlerë ka burim, periudhë, metodologji.
2. **Motori** (`motor/` + `.github/workflows/`): çdo javë lexon burimet zyrtare (ASK, BQK, vendimet e Qeverisë), krahason me periudhat e mëparshme, ruan versionet e reja.
3. **Ndërtuesi** (`site/ndertimi/`): ndërton faqen nga të dhënat. Sot është gjysmë manual, synimi është të ekzekutohet vetë pas çdo përditësimi të motorit. **Kujdes:** `site/index.html` është tani burimi i vërtetë; shih `site/ndertimi/LEXOMA.md` para çdo rindërtimi.
4. **Faqja** (`site/index.html`): faqe statike, e hapshme në çdo telefon; mund të instalohet si aplikacion (PWA).

## Gjendja
- `site/index.html` është kopja e fundit e faqes së publikuar në claude.ai.
- Shifrat e disa moduleve janë ende të ngulitura në faqe, jo të lexuara nga `data/`. Kjo është hapi tjetër.

## Hapat tjetër
1. Aktivizo GitHub Pages (Settings, Pages, Branch main, folder / (root)) që faqja të ketë adresë publike.
2. Faqja lexon `data/*.json` në vend të numrave të ngulitur.
3. Ndërtimi automatik në Actions pas çdo përditësimi.
