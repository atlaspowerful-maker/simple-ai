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
[P1][done] Run réel sur un projet jetable + journal de frictions — seule façon de savoir si la boucle est VRAIMENT plus simple que le baseline ~5h =2h @epic:dx
  > Problème : aucune preuve. dev/backlog.md est rempli rétroactivement (presque tout en done). On construit à l'aveugle.
  > Cible : mener un mini-projet jetable (non simple-ai, ~5-8 tickets, assez réel pour des remarques DEV→PO, assez petit pour finir) de zéro à un livrable minimal, via la boucle simple-ai.
  > Scope : installer le kit via init.md TEL QUEL (tester l'onboarding réel, noter chaque friction). Dérouler PO crée → DEV dépile → ≥1 remarque DEV→PO → estimé/réel loggés. Produire dev/RUNLOG.md : à chaque étape, fluide / a traîné / a manqué.
  > Sortie : frictions converties en nouveaux tickets backlog (c'est CE run qui dira ce qui manque vraiment).
  > Décidé (PO) : run en 2-sessions (mode existant ; le solo n'est pas encore livré) ; B passe AVANT A pour révéler les frictions qui justifient le solo ; on garde dev/RUNLOG.md seul, le projet jetable reste hors repo.
  > Preuve : un livrable jetable réellement atteint + dev/RUNLOG.md daté + au moins 3 frictions transformées en tickets.
  > Fait (DEV) : run citation-cli mené (install zip → PO → DEV → livrable + RUNLOG). Frictions F1/F2/F4 → tickets ci-dessous ; F3 (poids worktree en solo) valide le ticket « Mode solo ». Voir dev/RUNLOG.md.
[P2][done] init.md ignore l'install par zip (le vrai artefact de release) — §1 décrit la copie manuelle depuis kit/ (qui perd le +x → chmod), le zip n'est mentionné nulle part ~1h =0.5h @epic:dx #doc
  > Friction F1 du run réel : `unzip simple-ai.zip` pose `simple-ai/` prêt, bit +x préservé → le chemin le plus simple. init.md décrit l'autre chemin (copie kit/) et son piège chmod, sans jamais citer le zip. Reco : documenter le zip comme chemin d'install par défaut, reléguer la copie manuelle.
  > Fait (DEV) : init.md §1 présente archive/CLI en défaut, copie manuelle reléguée + chmod cadré « copie uniquement ». README aligné (3 façons dont uvx).
[P2][done] Manifeste de fichiers d'init.md §1 a dérivé — omet calibrate.py et test_build.py pourtant livrés ; une install par copie manuelle les rate ~0.5h =0.25h @epic:dx #doc
  > Friction F2 du run réel. Reco : compléter la liste, ou mieux, la dériver d'une source unique (le contenu réel de kit/) pour qu'elle ne redérive pas — cf. esprit du ticket « garde anti-dérive ».
  > Fait (DEV) : ajouté calibrate.py au manifeste init.md + table README. test_build.py volontairement EXCLU du manifeste car F4 l'exclut désormais du livrable.
[P3][done] make-release embarque test_build.py dans l'install utilisateur — le test du framework atterrit dans le simple-ai/ de chaque projet (clutter) ~0.5h =0.5h @epic:dx #test
  > Fait (DEV) : kit/.gitattributes (export-ignore sur test_build.py + .gitattributes lui-même). git archive l'exclut → zip ET snapshot CLI propres. Prouvé : zip ne contient plus test_build.py. calibrate.py (outil user) reste livré.
  > Friction F4 du run réel : le zip livre test_build.py (test interne de build.parse). calibrate.py, lui, est un outil user légitime → garder. Reco : exclure test_build.py de l'archive (git archive sur un sous-ensemble, ou .gitattributes export-ignore).
[P1][done] Mode solo par défaut — une session, deux casquettes, sans worktree : le mode 2-sessions devient une montée en puissance, pas le point d'entrée ~3h =1.5h @epic:dx
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
[P3][done] Tags libres sur les tickets (#tag) — 2e axe de catégorisation transverse à @epic: (couche/nature : #front #back #infra…), vocabulaire LIBRE choisi par le projet ~3h =1.5h @epic:core
  > Décidé (humain) : tag GÉNÉRIQUE et LIBRE (#token alphanum/-), PAS de liste figée Front/Back/Infra ; le framework reste agnostique. Orthogonal à @epic: (epic = thème/feature ; tag = couche/nature).
  > Syntaxe (reco) : #token dans la zone méta de fin de ligne, au même endroit que @epic: / ~Nh / =Nh, plusieurs autorisés. Ex : [P2][todo] Titre — pourquoi ~2h @epic:core #back #infra
  > Travail : (1) CONVENTION.md documente le token = contrat ; (2) kit/build.py : le parser extrait les #tags (ancrage fin de ligne comme @epic, AVANT le split titre—pourquoi — attention à l'extraction subtile signalée par C1), render en chips, filtre tag réutilisant le mécanisme f-state/f-prio ; (3) tests parse() (on en a maintenant) : 0 / 1 / N tags + cohabitation epic+réel+estimé ; (4) mention courte PO.md/DEV.md.
  > Couleur des chips : palette déterministe par hash du nom (zéro config, pas de setup).
  > Scope (garde-fou) : zéro dépendance, ADDITIF (un ticket sans #tag marche comme avant). Livrable public → générique. Régénérer le viewer après.
  > Preuve : un ticket #back s'affiche avec sa chip ; le filtre tag masque/montre ; parse() renvoie la liste des tags ; CONVENTION à jour.
[P3][done] CLI simple-ai init (uvx, Python) — remplacer le prompt /init par une vraie commande qui pose le dossier simple-ai/ ~5h =2h @epic:dx
  > Décidé (PO) : runtime = uvx. Cohérent avec un framework 100 % Python (build.py, calibrate.py), zéro dépendance Node. Pas de variante npx (garde-fou simple). Le nom de package / distrib suit ce choix.
  > Fait (DEV) : cli/ (pyproject « simple-ai » + simple_ai/cli.py, stdlib, `uvx simple-ai init` pose simple-ai/ + chmod +x + garde idempotence). Source unique préservée : le kit est un snapshot gitignoré régénéré par cli/sync-kit.sh (pas de 3e copie committée). Prouvé : scaffold dans /tmp fonctionnel. Reste : publication PyPI (étape humaine, token requis).
[P3][done] build.py dupliqué dans example/ a dérivé — copie antérieure au support du chemin (pourtant done) ; viole la source unique kit/ ~1h =0.5h @epic:dx
  > Confirmé divergent (diff kit/build.py ↔ example/demo-todo/simple-ai/build.py : l'exemple est l'ancienne version sans argument de chemin).
  > Décision de fond (PO/DEV) : snapshot figé assumé / lien / génération au release. Reco : régénérer la copie depuis kit/ (pas de copie éditée à la main) pour préserver la source unique.
  > Fait (DEV) : copie resynchronisée depuis kit/build.py (identique) + backlog.html de l'exemple régénéré. Reste : choisir le mécanisme durable → ticket de suivi ci-dessous.
[P3][done] Garde anti-dérive de la copie kit→example — la resync est manuelle, elle redérivera ; décider le mécanisme (snapshot régénéré / lien / check) ~1h =0.5h @epic:dx
  > Né de la friction « build.py dupliqué a dérivé » : on a corrigé la copie, pas la cause. Sans garde, toute évol de kit/build.py re-divergera.
  > Pistes (PO tranche) : (a) script de regen example/ depuis kit/ appelé à la release ; (b) check qui échoue si copie ≠ kit/ ; (c) assumer un snapshot figé documenté. Garder simple : pas de machinerie si (c) suffit.
  > Fait (DEV) : choix (c) — example/README.md documente que demo-todo/simple-ai/ est un snapshot du kit (ne pas éditer à la main, resync depuis kit/). Zéro machinerie, garde-fou « simple » respecté.

[P1][todo] Boucle git locale et multi-worktrees (SA12) — séquence canonique pull→relire→éditer atomiquement→build→commit→push→merge ff-only ; cycle court par session ; l'atomicité fichier ne propage rien entre worktrees ~3h @epic:core
[P2][todo] Vérifier le redéploiement après MAJ du framework (SA13) — preuve e2e : update repo → projet consommateur → viewer + backlog OK ~2h @epic:dx
[P2][todo] Trancher le statut de backlog.html (SA14) — versionné/commité OU local ignoré (.gitignore) ; appliquer au template + workflow ~1h @epic:core
[P2][todo] Garde-fou DEV contre backlog vide périmé (SA15) — si le backlog ressemble au template/est vide alors que le PO a annoncé des tickets : git status/log, fetch/merge, challenger avant « rien à dépiler » ~1h @epic:core
[P3][todo] Aide-mémoire git dans bin/po et bin/dev + sync local (SA16) — pull au démarrage, bannière commit+merge avant sortie, trap EXIT du WIP non commité, évaluer bin/sync ~2h @epic:dx
[P2][todo] Section terminés en bas du viewer (SA17) — sortir les done du flux, section dédiée triée par date de clôture ~1.5h @epic:dx
[P1][todo] Nettoyage sûr des branches et worktrees (SA18) — avant toute suppression, git log main..branche ; si non vide STOP + surfacer ; ne retirer que le worktree ~2h @epic:core
[P2][todo] Pré-sync repo→hub : rendre dev/backlog.md lossless (SA19) — porter ici les tickets hub-only (ci-dessus) ; vérifier le mapping de convention ; ajouter au DEV.md le garde-fou changelog atomique (RUNLOG commité avec le code) ~2h @epic:core
[P1][done] Garde-fou anti-fuite : le backlog atlas ne doit JAMAIS finir dans le livrable (SA20) — sync strictement repo→hub en lecture seule ; kit/ et example/ neutres ; check make-release.sh qui échoue si marqueurs atlas (#infra, IP, domaine) ~1.5h =1h @epic:core
  > Fait (DEV) : make-release.sh scanne le CONTENU de l'archive (= kit/) — motifs génériques (IP, email) + .release-denylist locale gitignorée pour les marqueurs propres au projet (ex. « atlas ») ; toute correspondance → release refusée (exit 1) + zip supprimé. Prouvé : kit/ neutre passe (14 fichiers), marqueur injecté échoue, denylist non versionnée. kit/ et example/ vérifiés neutres.
  > Note (DEV) : « #infra » écarté comme marqueur — présent légitimement dans kit/CONVENTION.md (exemple de tag) → faux positif. D'où scan du contenu réel + denylist curée, pas de liste figée.
  > Reste hors-repo : le volet « sync repo→hub en lecture seule » vit dans l'outillage du hub (hors de ce repo public) — non traité ici. SA20 livre le filet côté release ; durcir le sens du sync côté hub = ticket séparé si besoin.

[wishlist][done] Calibration par priorité/taille, pas seulement globale — affiner SA11 ~2h =0.5h @epic:core
[wishlist][todo] Publier le viewer en ligne en une commande — exploiter le hook publish de CONFIG.md ~2h @epic:dx
