# Arkivi i të dhënave të Kosovës: sistem automatik
- `index.html` + `data/` = faqja (statike, hapet pa server; mund të hostohet në GitHub Pages).
- `motor/` = mbledhësi. `burimet.json` është regjistri i burimeve dhe rregullave të nxjerrjes.
- `.github/workflows/perditeso.yml` e ekzekuton motorin çdo javë. Ndryshimet e vogla shkruhen vetë në `data/`, të mëdhatë shkojnë te `data/pending.json`.
- Historiku i plotë i versioneve është historiku i git (çdo commit = një version i të dhënave).
Hapat: 1) krijo repo në GitHub, 2) ngarko këto skedarë, 3) Settings > Pages > Deploy from branch, 4) Actions > "Përditëso të dhënat" > Run workflow për provë.
Para përdorimit provo rregullat regex të `burimet.json` me një PDF real: janë të pa provuara.
