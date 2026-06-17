# WORKFLOW — git, sessions, branches, merges

> Comment on travaille **à deux sessions concurrentes** sans se marcher dessus, et comment un changement
> passe du ticket au `main`. Le format des **tickets** est dans `CONVENTION.md` ; ici c'est le **git**.

## 1. Deux sessions en parallèle, pilotées par l'humain

Tu ouvres une **session PO** et une **session DEV** en même temps, et **tu pilotes les deux**. Elles ne
se parlent pas directement : leur seul canal commun est `backlog.md`.

**Piège central** : l'état git (`HEAD`, index, fichiers) est partagé **par dossier de travail**, pas par
session. Deux sessions dans le même dossier → un `git checkout`/commit de l'une **déplace** l'autre.
→ **Chaque session travaille dans son propre worktree**, créé par les lanceurs :

```
bin/po    # session PO  → worktree ../<repo>-po
bin/dev   # session DEV → worktree ../<repo>-dev
```

`HEAD`/index/fichiers isolés, `.git` partagé. git **refuse** le même checkout dans deux worktrees :
garde-fou natif. La session annonce son rôle dès le départ (« casquette PO/DEV »), **pas de switch en cours**.

## 2. Nommage

| Quoi | Convention | Exemple |
|------|-----------|---------|
| **Branche de session** | `session/AAAA-MM-JJ-<sujet-court>` | `session/2026-06-17-filtre-date` |
| **Worktree** | `../<repo>-<role>` (créé par les lanceurs) | `../mon-projet-dev` |
| **Commit** | impératif court + *pourquoi* | `ajoute le filtre par date — retrouver une entrée ancienne` |
| **Merge request / PR** | titre = ce que ça livre + l'ID du ticket si tu en as un | `Filtre par date (#12)` |

Un ticket en cours = une branche. Pas de fourre-tout multi-sujets sur une branche.

## 3. Cycle d'un changement (côté DEV)

1. **Prendre** le ticket : `todo` → `progress` (édition atomique du backlog, cf. `CONVENTION.md §8`).
2. **Coder** sur sa branche de session, dans son worktree. Commits **atomiques**, messages clairs.
3. **Prouver** : test / exécution / capture — selon le projet. Pas de `done` non prouvé.
4. **Ouvrir la merge request** vers `main` (voir §4).
5. Après merge validé : ticket → `done`, régénérer le viewer (`build.py`).

## 4. Merge request : qui valide, et comment

**Règle d'or : personne ne fusionne son propre travail sans relecture.**

- **Qui valide ?** → **l'humain** (c'est ton repo, tu pilotes les deux sessions). Tu donnes le **go** final.
  Tu peux **déléguer la relecture** à un agent dédié (« relis ce diff : bugs, secrets, cohérence, lint »),
  mais la décision de merger reste la tienne.
- **Sur quoi porte la relecture ?** : pas de secret/token commité, cohérence avec le reste, restes de debug,
  la preuve que ça marche, message de commit clair.
- **Forme de la merge request** :
  - **Repo hébergé (GitHub/GitLab…)** → une vraie **Pull/Merge Request** : ouvre-la, relis le diff, valide, merge.
  - **Local seul** → une **revue avant merge** : relis `git diff main...<branche>`, puis `merge` dans `main`.
- **Conflit** = du travail d'une autre session : **lire, intégrer les deux, ne jamais écraser**.

## 5. Après le merge

```
git worktree remove ../<repo>-<role>     # retire le worktree de la session
git branch -d session/AAAA-MM-JJ-<sujet> # supprime la branche fusionnée
```

Puis passe le ticket `done` (+ `push`/`publish` si le backlog est `online`, cf. `CONFIG.md`).

## 6. Résumé des rôles sur git

| | PO | DEV | Humain |
|--|----|-----|--------|
| Worktree | `../<repo>-po` (`bin/po`) | `../<repo>-dev` (`bin/dev`) | — |
| Écrit | tickets dans `backlog.md` | code + statuts `progress`/`done` | pilote les deux |
| Ouvre les merge requests | rarement (curation) | oui (le travail réalisé) | — |
| **Valide / merge** | — | — | **oui (go final)** |
