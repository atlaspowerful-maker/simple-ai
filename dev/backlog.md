# Backlog — simple-ai (le framework se développe avec lui-même)

> Dogfooding : simple-ai est piloté par son propre framework. Format : `kit/CONVENTION.md`.
> Casquettes : `kit/PO.md` · `kit/DEV.md`. Régénère : `python3 kit/build.py dev/backlog.md`.
> `~Nh` = estimé (créateur), `=Nh` = réel (exécutant à la clôture). Les `done` avec réel nourrissent SA11.

[epic] core — Socle du framework
[epic] dx — Expérience & distribution

[P1][done] Squelette + commande /init (SA1) — point d'entrée unique ~3h @epic:core
[P1][done] Convention de ticket + backlog (SA2) — contrat partagé PO/DEV/viewer ~2h @epic:core
[P2][done] Casquette PO portable (SA3) — playbook générique sans réf serveur ~3h @epic:core
[P2][done] Casquette DEV portable (SA4) — context-loading + challenge-before-execute ~3h @epic:core
[P1][done] Viewer HTML + générateur (SA5) — backlog.md vers backlog.html statique ~4h @epic:core
[P1][done] Isolation + lanceurs worktree (SA6) — bin/po et bin/dev, pas de contamination ~3h @epic:core
[P2][done] README + exemple e2e (SA7) — demo-todo de bout en bout ~2h @epic:dx
[P3][done] Support Codex (SA8) — AGENTS.md miroir ~2h @epic:core
[P2][done] Mode TokenBurn (SA9) — DEV autonome avec filtre GO/SKIP ~2h @epic:core
[P2][done] Estimation estimé/réel + écart (SA10) — deux champs, viewer affiche l'écart ~2h @epic:core
[P1][done] Backlog online configurable (CONFIG.md) — local ou distant via pull/push/publish ~3h @epic:core
[P2][done] Workflow git documenté (WORKFLOW.md) — sessions, branches, merge, qui valide ~2h @epic:dx
[P2][done] Archive livrable + release v0.1 (make-release.sh + GitHub) — zip propre du dossier simple-ai/ ~2h @epic:dx
[P2][done] build.py accepte un chemin de backlog — rendre dev/backlog.md sans dupliquer le générateur ~1h @epic:core

[P3][done] Routine de calibration des estimations (SA11) — lit les done (~Nh + =Nh) via build.parse, médiane des ratios réel/estimé = facteur suggéré ; mesure et suggère, l'humain décide ~3h =2h @epic:core
[P3][todo] Clarifier WORKFLOW §4 : décision de merge vs exécution — le DEV ne sait pas qu'il peut enchaîner merge+cleanup après le go ~1h @epic:dx
  > Friction dogfood remontée pendant SA11. §4 dit « l'humain valide/merge », ce qui se lit comme « le DEV ne touche jamais au merge ».
  > Or la même section autorise déjà à déléguer une fois le go donné. Reco : distinguer explicitement (a) la DÉCISION de merger = toujours humaine
  > de (b) l'EXÉCUTION mécanique (merge --no-ff + cleanup worktree/branche) = délégable au DEV dès le go reçu. PO : arbitre la prio et reformule §4.
[P3][blocked] CLI simple-ai init (npx/uvx) — remplacer le prompt /init par une vraie commande qui pose le dossier simple-ai/ ~5h @epic:dx
  > @dev-note: décision produit avant exécution — quel runtime ? npx (Node) ou uvx (Python) ? Le framework est 100 % Python (build.py, calibrate.py), uvx serait cohérent et sans dépendance Node ; npx touche plus de monde mais ajoute un écosystème. Le distrib/nom de package en dépend. Tranche avant que je code.
[wishlist][todo] Calibration par priorité/taille, pas seulement globale — affiner SA11 ~2h @epic:core
[wishlist][todo] Publier le viewer en ligne en une commande — exploiter le hook publish de CONFIG.md ~2h @epic:dx
