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
[P1][todo] Run réel sur un projet jetable + journal de frictions — seule façon de savoir si la boucle est VRAIMENT plus simple que le baseline ~5h @epic:dx
  > Problème : aucune preuve. dev/backlog.md est rempli rétroactivement (presque tout en done). On construit à l'aveugle.
  > Cible : mener un mini-projet jetable (non simple-ai, ~5-8 tickets, assez réel pour des remarques DEV→PO, assez petit pour finir) de zéro à un livrable minimal, via la boucle simple-ai.
  > Scope : installer le kit via init.md TEL QUEL (tester l'onboarding réel, noter chaque friction). Dérouler PO crée → DEV dépile → ≥1 remarque DEV→PO → estimé/réel loggés. Produire dev/RUNLOG.md : à chaque étape, fluide / a traîné / a manqué.
  > Sortie : frictions converties en nouveaux tickets backlog (c'est CE run qui dira ce qui manque vraiment).
  > Décidé (PO) : run en 2-sessions (mode existant ; le solo n'est pas encore livré) ; B passe AVANT A pour révéler les frictions qui justifient le solo ; on garde dev/RUNLOG.md seul, le projet jetable reste hors repo.
  > Preuve : un livrable jetable réellement atteint + dev/RUNLOG.md daté + au moins 3 frictions transformées en tickets.
[P1][todo] Mode solo par défaut — une session, deux casquettes, sans worktree : le mode 2-sessions devient une montée en puissance, pas le point d'entrée ~3h @epic:dx
  > Problème : aujourd'hui tout (README, bin/, WORKFLOW) impose 2 sessions + 2 worktrees + pilotage parallèle dès le départ → plus lourd que « j'ouvre une session Claude ». Menace directe l'objectif « simple ».
  > Cible : une voie d'entrée où UNE session porte PO puis DEV tour à tour, sur le backlog local, dans la racine, zéro worktree. On monte vers 2-sessions seulement quand le parallélisme est réellement utile.
  > Scope (rester simple) : surtout de la DOC. README présente le solo comme DÉFAUT (décision actée) ; CLAUDE.md + AGENTS.md disent comment une même session bascule de casquette (annoncer le changement, relire le backlog avant d'écrire). PAS de script bin/solo (décision actée : solo = on lance sa session IA à la racine, rien à exécuter).
  > Inclut (fusion du candidat « durcir init.md ») : étape 4 de init.md (brancher l'agent) est le pivot « simple » mais reste un soft, et le chmod +x est un piège → la durcir fait partie de cette story.
  > Critère de bascule à documenter : quand passer solo → 2-sessions (taille, besoin réel de parallélisme).
  > Preuve : un nouvel utilisateur démarre et produit un ticket réalisé SANS créer de worktree, en suivant uniquement le README.
[P2][done] Tests sur build.parse() — calibrate.py (SA11) en dépend déjà en prod et le repo n'a AUCUN test ; le parser a une extraction fin-de-ligne subtile (epic → =Nh → ~Nh) sans filet ~2h =1h @epic:core
[P2][done] Clarifier WORKFLOW §4 : décision de merge vs exécution — le DEV ne sait pas qu'il peut enchaîner merge+cleanup après le go ~1h =0.5h @epic:dx
  > Friction dogfood remontée pendant SA11. §4 dit « l'humain valide/merge », ce qui se lit comme « le DEV ne touche jamais au merge ».
  > Décidé (humain, confirmé) : distinguer explicitement (a) la DÉCISION de merger = TOUJOURS humaine, de (b) l'EXÉCUTION mécanique
  > (merge --no-ff + cleanup worktree/branche) = DÉLÉGABLE au DEV dès le go reçu. Plus de « reco » à trancher : c'est la doctrine à inscrire.
  > Travail (DEV) : reformuler kit/WORKFLOW.md §4 selon (a)/(b). C'est le livrable public → relire avec ce regard (générique, sans réf interne).
  > Prio P2 (PO) : friction confirmée + récurrente, ~1h, et elle frappera le run B (P1, 2-sessions) si §4 reste ambigu → à lever tôt, pas à enterrer en P3.
  > Preuve : §4 lue par un nouveau DEV → il sait qu'il peut exécuter merge+cleanup seul après le go, sans re-demander.
[P2][done] Viewer : détails repliables au clic + estimé plus lisible — combler l'écart CONVENTION §6 (« dépliable » promis, rendu à plat) et sortir l'estimé du gris atténué ~2h =1h @epic:dx
  > Au clic : carte repliée par défaut (titre + pourquoi + badges prio/état/métriques restent visibles = ligne scannable) ; le bloc contexte .ctx se déplie/replie au clic sur la carte. Avec ≥6 lignes de contexte par ticket, le rendu à plat actuel est devenu illisible.
  > Estimé : ~Nh est rendu en gris atténué (.effort color:dim) → le rendre lisible (badge aligné avec prio/état) ; réel =Nh et écart déjà visibles, garder la cohérence.
  > Scope : uniquement kit/build.py (TEMPLATE + CSS + petit JS de toggle, stdlib, zéro dépendance). Régénérer dev/backlog.html après. Livrable public → générique, sans réf interne.
  > Preuve : backlog.html ouvert → liste compacte scannable ; un clic ouvre/ferme le détail d'un ticket ; l'estimé saute aux yeux.
[P3][todo] Tags libres sur les tickets (#tag) — 2e axe de catégorisation transverse à @epic: (couche/nature : #front #back #infra…), vocabulaire LIBRE choisi par le projet ~3h @epic:core
  > Décidé (humain) : tag GÉNÉRIQUE et LIBRE (#token alphanum/-), PAS de liste figée Front/Back/Infra ; le framework reste agnostique. Orthogonal à @epic: (epic = thème/feature ; tag = couche/nature).
  > Syntaxe (reco) : #token dans la zone méta de fin de ligne, au même endroit que @epic: / ~Nh / =Nh, plusieurs autorisés. Ex : [P2][todo] Titre — pourquoi ~2h @epic:core #back #infra
  > Travail : (1) CONVENTION.md documente le token = contrat ; (2) kit/build.py : le parser extrait les #tags (ancrage fin de ligne comme @epic, AVANT le split titre—pourquoi — attention à l'extraction subtile signalée par C1), render en chips, filtre tag réutilisant le mécanisme f-state/f-prio ; (3) tests parse() (on en a maintenant) : 0 / 1 / N tags + cohabitation epic+réel+estimé ; (4) mention courte PO.md/DEV.md.
  > Couleur des chips : palette déterministe par hash du nom (zéro config, pas de setup).
  > Scope (garde-fou) : zéro dépendance, ADDITIF (un ticket sans #tag marche comme avant). Livrable public → générique. Régénérer le viewer après.
  > Preuve : un ticket #back s'affiche avec sa chip ; le filtre tag masque/montre ; parse() renvoie la liste des tags ; CONVENTION à jour.
[P3][todo] CLI simple-ai init (uvx, Python) — remplacer le prompt /init par une vraie commande qui pose le dossier simple-ai/ ~5h @epic:dx
  > Décidé (PO) : runtime = uvx. Cohérent avec un framework 100 % Python (build.py, calibrate.py), zéro dépendance Node. Pas de variante npx (garde-fou simple). Le nom de package / distrib suit ce choix.
[P3][done] build.py dupliqué dans example/ a dérivé — copie antérieure au support du chemin (pourtant done) ; viole la source unique kit/ ~1h =0.5h @epic:dx
  > Confirmé divergent (diff kit/build.py ↔ example/demo-todo/simple-ai/build.py : l'exemple est l'ancienne version sans argument de chemin).
  > Décision de fond (PO/DEV) : snapshot figé assumé / lien / génération au release. Reco : régénérer la copie depuis kit/ (pas de copie éditée à la main) pour préserver la source unique.
  > Fait (DEV) : copie resynchronisée depuis kit/build.py (identique) + backlog.html de l'exemple régénéré. Reste : choisir le mécanisme durable → ticket de suivi ci-dessous.
[P3][todo] Garde anti-dérive de la copie kit→example — la resync est manuelle, elle redérivera ; décider le mécanisme (snapshot régénéré / lien / check) ~1h @epic:dx
  > Né de la friction « build.py dupliqué a dérivé » : on a corrigé la copie, pas la cause. Sans garde, toute évol de kit/build.py re-divergera.
  > Pistes (PO tranche) : (a) script de regen example/ depuis kit/ appelé à la release ; (b) check qui échoue si copie ≠ kit/ ; (c) assumer un snapshot figé documenté. Garder simple : pas de machinerie si (c) suffit.
[wishlist][todo] Calibration par priorité/taille, pas seulement globale — affiner SA11 ~2h @epic:core
[wishlist][todo] Publier le viewer en ligne en une commande — exploiter le hook publish de CONFIG.md ~2h @epic:dx
