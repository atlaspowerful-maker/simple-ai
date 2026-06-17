# CONVENTION — le contrat partagé PO ⇄ DEV ⇄ viewer

> Ce fichier est **la source de vérité du format**. Le PO, le DEV et le générateur (`build.py`)
> s'y réfèrent tous. Si tu changes un format ici, mets à jour `build.py` dans la même tâche.

## 1. Le backlog est un seul fichier

Tout vit dans **`simple-ai/backlog.md`**. C'est l'unique canal de coordination entre la session
PO et la session DEV. Pas de base de données, pas de serveur : un fichier Markdown lisible.

## 2. Format d'un ticket (une ligne)

```
[PRIO][état] Titre court — pourquoi (contexte actionnable à froid) ~Nh
```

- **`[PRIO]`** — priorité (voir §3).
- **`[état]`** — `todo` · `progress` · `done` · `blocked` (voir §4).
- **`Titre court`** — l'action, à l'impératif.
- **`— pourquoi`** — la justification + assez de contexte pour être **fait sans la conversation d'origine**.
  Un ticket doit être actionnable à froid. Si ça ne tient pas sur la ligne, ajoute un bloc contexte (§6).
- **`~Nh`** — **estimé** : l'estimation d'effort donnée par **le créateur** du ticket (proxy de priorisation), facultative.
- **`=Nh`** — **réel** : le temps **réellement passé**, loggé par **l'exécutant à la clôture** (voir §10), facultatif.

Exemple (à la création, puis une fois fait) :
```
[P1][todo] Ajouter le filtre par date sur la liste — l'utilisateur ne retrouve pas une entrée ancienne ~2h
[P1][done] Ajouter le filtre par date sur la liste — l'utilisateur ne retrouve pas une entrée ancienne ~2h =3h
```

## 3. Échelle de priorité (ordonnée)

`P0` (critique, bloque tout) → `P1` → `P2` → `P3` → `wishlist` (souhait, après tout le reste).

Le DEV dépile **toujours dans cet ordre**. Adapte l'échelle à ton projet si besoin, mais garde-la
**ordonnée et documentée ici** — c'est elle qui décide quoi faire ensuite.

## 4. États

| État | Sens | Qui le pose |
|------|------|-------------|
| `todo` | à faire, prêt à dépiler | PO |
| `progress` | en cours | DEV (quand il prend le ticket) |
| `done` | fini **et prouvé** | DEV (jamais un ticket non prouvé) |
| `blocked` | en attente d'un arbitrage PO (voir §5) | DEV |

## 5. Canal de remarque DEV → PO

Le DEV **n'exécute jamais une story bancale en silence**. S'il manque des détails, si une re-priorisation
s'impose, ou s'il détecte une incohérence/un risque, il passe le ticket en `blocked` et ajoute **juste en
dessous** une ligne de continuation :

```
[P1][blocked] Migrer la base vers le nouveau schéma — perf des requêtes ~4h
  > @dev-note: quel schéma cible ? pas de spec. Décision produit nécessaire avant exécution.
```

- Le préfixe `  > @dev-note:` (2 espaces, chevron) marque la remarque. Le PO la lit, arbitre, révise le ticket.
- **Pas de blocage dur** : tant que le PO n'a pas répondu, le DEV prend le **ticket suivant**.

## 6. Bloc contexte multi-lignes (optionnel)

Pour un ticket qui mérite plus que sa ligne, ajoute des lignes de continuation `  > …` juste en dessous.
Elles sont **rattachées au ticket** par le parser (affichées en panneau dépliable dans le viewer) et
**ignorées du tri**.

```
[P2][todo] Refondre l'écran de connexion — taux d'abandon élevé ~5h
  > Contexte : 30 % des users abandonnent à l'étape mot de passe.
  > Pistes : magic link, ou réduire les champs requis. À cadrer avec le PO.
```

## 7. Epics et stories (optionnel)

- Une story porte un token **`@epic:<id>`** en fin de ligne pour la rattacher à un epic.
- Un epic se déclare par une ligne **`[epic] <id> — <titre de l'epic>`**.
- Le viewer regroupe les stories sous leur epic.

```
[epic] auth — Authentification et comptes
[P1][todo] Page d'inscription — pas de moyen de créer un compte ~3h @epic:auth
[P2][todo] Reset mot de passe — support submergé de demandes ~2h @epic:auth
```

## 8. Édition atomique (impératif)

Deux sessions (PO et DEV) écrivent dans `backlog.md`. **Toute écriture doit être atomique** :
écrire dans un fichier temporaire puis `rename` (atomique sur POSIX), jamais une réécriture en place
qui peut s'entrelacer. Avant d'écrire, **relis le fichier** (il a pu changer depuis ta dernière lecture).

## 9. Régénération du viewer

Après **chaque changement** de `backlog.md`, l'agent (PO ou DEV) relance le générateur :

```
python3 simple-ai/build.py
```

→ régénère `simple-ai/backlog.html`. C'est une consigne portée par `PO.md` et `DEV.md`.
Pas de serveur qui tourne : le viewer est un fichier statique qu'on ouvre dans un navigateur
(ou qu'on **publie en ligne** si le backlog est en mode `online` — cf. `CONFIG.md`).

> **Où vit le backlog** (local dans le repo, ou online/partagé) est déclaré dans `CONFIG.md`.
> En mode `online`, `backlog.md` est une copie de travail : `pull` avant de lire, `push` après écriture.

## 10. Estimation : estimé (`~Nh`) + réel (`=Nh`)

Système d'estimation **volontairement minimal**, en deux temps — aucune méthode imposée :

1. **À la création** — le créateur du ticket (PO ou quiconque) pose un **estimé** `~Nh` selon **ses propres critères**.
2. **À la clôture** — l'exécutant (DEV ou quiconque) logge le **réel** `=Nh` en fin de ligne, au moment de passer `done`.

```
[P2][done] Refondre l'écran de connexion — taux d'abandon élevé ~5h =7h
```

Le viewer affiche les deux et signale l'**écart** (réel vs estimé). On ne cherche pas l'estimation
parfaite du premier coup : on **mesure l'écart**. Plus tard, une routine de calibration (story SA11)
exploite l'historique des écarts pour affiner la méthode — sans alourdir le système.

### Rétention (à respecter dès maintenant)

Les tickets **`done` qui portent un réel `=Nh` sont la matière première de la calibration** : **ne les
supprime pas**. Si tu veux désencombrer le backlog actif, **archive-les** (déplace-les sous une section
`## Archive` à la fin de `backlog.md`, ou dans un `backlog-archive.md`) plutôt que de les effacer —
ils restent parsables, donc exploitables par SA11.

### La calibration (SA11) — `calibrate.py`

La routine existe : **`python3 simple-ai/calibrate.py [chemin/backlog.md]`**. Elle s'appuie sur ce format :
- **Source** : les tickets `done` avec `~Nh` **et** `=Nh` (dans `backlog.md` + un éventuel `backlog-archive.md` voisin).
- **Extraction** : `build.py` expose une fonction `parse(text)` **importable** qui renvoie, par ticket,
  les champs `est` et `real`. `calibrate.py` fait `import build` et filtre les couples non vides —
  pas de parseur dupliqué.
- **Calcul** : pour chaque couple, ratio `réel / estimé` ; la **médiane** des ratios = **facteur de
  calibration suggéré** (coefficient d'ajustement global ; raffiner par priorité est une suite séparée).
- **Sortie** : affiche les couples et propose le facteur (le créateur s'en sert pour ajuster ses futurs
  estimés). Pas d'automatisme imposé — on **mesure et on suggère**, l'humain décide. Si aucun couple
  exploitable, elle le dit clairement et n'invente rien.

