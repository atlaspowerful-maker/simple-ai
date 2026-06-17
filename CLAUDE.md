# Instructions — repo simple-ai

Ce repo **héberge** le framework `simple-ai` **et se développe avec lui** (dogfooding).
Deux zones, à ne pas confondre :

## 1. Le livrable — `kit/` (rester CLEAN)

`kit/` est le framework distribué : c'est exactement ce que `make-release.sh` empaquette en `simple-ai.zip`
(`git archive HEAD:kit`). Règles :
- **Aucune config ni donnée de projet dans `kit/`.** `kit/backlog.md` et `kit/CONFIG.md` restent des **gabarits**
  (backlog vide, mode `local`). Ne jamais y mettre de vrais tickets ni de réf à un serveur.
- Toute modif de `kit/` change le produit livré → relire avec ce regard (générique, sans réf interne).

## 2. Le dogfood — `dev/` (le dev de simple-ai)

On pilote le développement de simple-ai **avec simple-ai** :
- **Backlog réel** : [`dev/backlog.md`](dev/backlog.md) (format : `kit/CONVENTION.md`).
- **Casquettes** : `kit/PO.md` (cadrer/prioriser) · `kit/DEV.md` (dépiler/réaliser/challenge).
- **Viewer** : `python3 kit/build.py dev/backlog.md` → `dev/backlog.html` (régénérer après chaque changement).
- **Sessions concurrentes** : worktree par rôle via `kit/bin/po` / `kit/bin/dev` (cf. `kit/WORKFLOW.md`).

## 3. Règles

- On développe le framework **en suivant ses propres règles** (c'est le but du dogfood : sentir les frictions).
- **Merge sur `main` validé par l'humain** (`kit/WORKFLOW.md`) — surtout : c'est un livrable public.
- **Garde-fou cardinal : simple-ai doit rester *simple*.** La casquette PO refuse le feature creep.
- Estimation : `~Nh` estimé / `=Nh` réel ; les `done` avec réel nourrissent la calibration (SA11).
