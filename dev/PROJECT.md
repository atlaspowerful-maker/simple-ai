# PROJECT — simple-ai (dev du framework)

## But

Le framework **simple-ai** lui-même : un mini-framework PO/DEV partageable, piloté par IA, coordonné
par un backlog unique + un viewer HTML statique. Voir le [README](../README.md).

## Périmètre

- **Dans le périmètre** : le kit livrable (`kit/`), sa doc, sa distribution.
- **Hors périmètre** : tout ce qui complexifie sans gain net — **simple-ai doit rester *simple***.

## Stack & comment lancer

- **Langage** : Python 3 (stdlib only) pour le générateur ; Bash pour les lanceurs ; Markdown pour le reste.
- **Tester le viewer** : `python3 kit/build.py dev/backlog.md` → ouvrir `dev/backlog.html`.
- **Construire l'archive** : `./make-release.sh` → `simple-ai.zip`.
- **Pas de secret** dans ce repo.

## Décisions & contraintes

- Le livrable (`kit/`) reste **clean** : aucune config/donnée de projet (le dogfood vit dans `dev/`).
- Le merge sur `main` est **validé par l'humain** (cf. `kit/WORKFLOW.md`).
