# AGENTS.md — repo simple-ai

Point d'entrée pour les agents lisant `AGENTS.md` (Codex & co). Mêmes règles que [`CLAUDE.md`](CLAUDE.md).

Ce repo héberge le framework **simple-ai** et **se développe avec lui** (dogfooding) :
- **Livrable** : `kit/` — à garder **clean** (gabarits, aucune donnée/config de projet ; c'est ce que livre `make-release.sh`).
- **Dev** : backlog réel dans `dev/backlog.md` ; casquettes `kit/PO.md` / `kit/DEV.md` ; convention `kit/CONVENTION.md`.
- **Viewer** : `python3 kit/build.py dev/backlog.md` après chaque changement.
- **Merge** validé par l'humain (`kit/WORKFLOW.md`). **Garde-fou : rester simple.**
