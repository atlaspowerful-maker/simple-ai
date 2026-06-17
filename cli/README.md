# simple-ai (CLI) — `uvx simple-ai init`

Remplace le prompt [`init.md`](../init.md) par une **vraie commande** : poser le dossier `simple-ai/`
dans un repo, sans rien copier à la main.

```sh
uvx simple-ai init           # pose simple-ai/ dans le repo courant
uvx simple-ai init chemin/   # ... dans un autre repo
```

Runtime **uvx** (Python) : cohérent avec un framework 100 % Python (`build.py`, `calibrate.py`),
**zéro dépendance** Node, zéro dépendance runtime (stdlib only).

## Source unique — pas de 3e copie du kit

Le CLI empaquette le kit dans `simple_ai/_kit/`, mais ce dossier est un **snapshot gitignoré**,
**jamais committé ni édité à la main**. La source unique reste `kit/`. On le régénère avant tout build :

```sh
cli/sync-kit.sh             # kit/ → cli/simple_ai/_kit/ (git archive, +x préservé)
```

Même principe que `example/` (cf. [`example/README.md`](../example/README.md)) : un seul `kit/`, des
snapshots régénérés, jamais de copie maintenue à la main.

## Build & publication (étape humaine)

```sh
cli/sync-kit.sh                       # 1. synchronise le snapshot du kit
python3 -m build cli/                 # 2. construit le wheel + sdist (force-include _kit/)
# 3. publication PyPI (twine upload) = étape humaine : compte + token PyPI requis.
```

Une fois publié, `uvx simple-ai init` fonctionne partout. En local, sans publier :

```sh
cli/sync-kit.sh && python3 -m simple_ai init /tmp/mon-repo
```
