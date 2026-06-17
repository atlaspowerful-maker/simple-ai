# RUNLOG — run réel sur projet jetable (2026-06-18)

> Ticket P1 « Run réel sur un projet jetable + journal de frictions ». But : sentir si la boucle
> simple-ai est vraiment plus simple que le baseline, en la déroulant sur un vrai mini-projet.
> Projet jetable : **citation-cli** (CLI Python qui affiche une citation au hasard), monté hors repo
> dans `/tmp/citation-cli`, installé via l'artefact de release réel (`simple-ai.zip`).

## Déroulé, étape par étape (fluide / a traîné / a manqué)

| Étape | Verdict | Note |
|------|---------|------|
| 1. Install (zip → `simple-ai/`) | **fluide** | `unzip simple-ai.zip` pose `simple-ai/` prêt, **bit +x préservé**. Rien à faire. |
| 1bis. …mais suivre `init.md §1` | **a manqué** | `init.md` décrit l'install par **copie manuelle depuis `kit/`** (qui perd le +x → d'où le `chmod`). Le **zip n'est mentionné nulle part** : deux réalités divergentes, le `chmod` ne sert que sur le chemin copie. → F1 |
| 1ter. manifeste `init.md §1` | **a manqué** | La liste de fichiers omet `calibrate.py` (SA11) et `test_build.py`, **pourtant dans le zip**. Un user qui suit la copie manuelle les rate. → F2 |
| 2. Amorce `PROJECT.md` / backlog | **fluide** | Gabarits clairs, remplis en 2 min. |
| 3. Génère le viewer | **fluide** | `python3 simple-ai/build.py` → `backlog.html` du premier coup (chemin par défaut = backlog voisin, OK). |
| 4. Brancher l'agent (`CLAUDE.md`) | **fluide-ish** | Étape soft, pas indispensable pour ce run solo. (déjà tracé par le ticket « Mode solo »). |
| 5. PO crée le backlog | **fluide** | 6 tickets écrits sans accroc. Bonus : les **`#tag`** tout juste livrés (`#core #test #doc`) servent immédiatement. |
| 6. DEV dépile + livrable | **a traîné (process)** | Le code est venu vite (CLI qui tourne, 3 `done`). MAIS pour « bien faire », `WORKFLOW` impose `bin/dev` + worktree : **cérémonie disproportionnée** pour un run solo jetable. J'ai dépilé dans le dossier. → F3 (valide « Mode solo ») |
| 7. Remarque DEV→PO | **fluide** | Ticket `--add` passé `blocked` + `@dev-note` (dédup ? validation ? écriture concurrente ?). Le canal marche. |
| 8. Estimé/réel | **fluide + signal** | Estimés 1h, réels 0.5h → cohérent avec le facteur de calibration **×0.50** mesuré sur le repo. Validation croisée. |

## Livrable atteint

CLI `citation.py` fonctionnelle (citation au hasard, `--author`), données séparées en `citations.json`,
3 tickets `done` avec réel loggé, 1 remarque DEV→PO. La boucle **tient** : amorce → PO → DEV → preuve → viewer.

## Verdict global

Le **cœur** (un seul fichier backlog, convention de ticket, viewer, estimé/réel, tags) est **fluide et
réellement plus léger** que monter un Jira jetable. Les frictions sont concentrées sur **l'onboarding**
(`init.md` a dérivé du vrai artefact) et sur **le poids 2-sessions/worktree imposé d'entrée** (le run solo
le confirme). Rien dans le cœur ne ralentit ; tout ce qui freine est en périphérie et déjà adressable.

## Frictions → tickets

- **F1** — `init.md` ignore l'install par zip (le vrai artefact) → nouveau ticket.
- **F2** — manifeste `init.md §1` stale (omet `calibrate.py`, `test_build.py`) → nouveau ticket.
- **F3** — run solo : cérémonie `bin/dev`/worktree disproportionnée → **valide le ticket P1 « Mode solo »** (pas de doublon).
- **F4** — `make-release` embarque `test_build.py` (test du framework) dans l'install utilisateur → nouveau ticket.
