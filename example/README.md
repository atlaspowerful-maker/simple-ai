# example/demo-todo — démo de bout en bout

Un projet de démonstration qui montre à quoi ressemble un repo **utilisant** simple-ai :
un `simple-ai/backlog.md` rempli (epics, états, une remarque DEV→PO), son `backlog.html` généré,
et un `PROJECT.md` d'amorce. Ouvre `demo-todo/simple-ai/backlog.html` dans un navigateur.

## ⚠️ `demo-todo/simple-ai/` est un **snapshot du kit** — ne pas l'éditer à la main

Le dossier `demo-todo/simple-ai/` reproduit ce qu'un utilisateur obtient en installant simple-ai.
Ses fichiers d'**outillage** (`build.py`, `calibrate.py`, …) sont une **copie de `kit/`**, la source unique.
**Ne les édite jamais ici** : toute correction se fait dans `kit/`, puis on **régénère la copie** :

```sh
cp kit/build.py example/demo-todo/simple-ai/build.py     # resync depuis la source unique
python3 example/demo-todo/simple-ai/build.py example/demo-todo/simple-ai/backlog.md  # régénère le viewer
```

Seuls les fichiers **propres à la démo** (`backlog.md`, `PROJECT.md`) sont édités directement ici.

> Mécanisme assumé : **snapshot figé documenté** (décision PO, garde-fou « simple » — pas de script ni de
> hook). Si la copie redérive un jour, c'est qu'on a édité à la main au lieu de resynchroniser depuis `kit/`.
