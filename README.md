# simple-ai

Un mini-framework **partageable** qui transforme n'importe quel repo en un workflow **PO ⇄ DEV**
piloté par une IA agentique. On l'ajoute à son projet, on ouvre **une session IA qui porte les deux
casquettes tour à tour** (Claude Code, Codex…) — c'est le **mode solo, le défaut** — et le tout est
coordonné par **un backlog unique** + un **viewer HTML** des tickets et de leur avancement. Quand le
parallélisme devient vraiment utile, on **monte à deux sessions en parallèle** (voir plus bas).

Le nom dit la philosophie : **simple**. Le moins de machinerie possible — des fichiers Markdown
lisibles, un viewer HTML statique, **zéro serveur** qui tourne.

## Les deux casquettes

**Deux casquettes — pas forcément deux sessions.** Par défaut (**solo**), **une seule session** les porte
**tour à tour** : tu lui demandes d'être PO pour cadrer, puis DEV pour réaliser. Quand le parallélisme
devient utile, tu **montes à deux sessions** que tu pilotes toi-même. Dans les deux cas, les casquettes
ne communiquent **pas** directement entre elles : leur **seul** point de rendez-vous est `backlog.md`.

- **Session PO** — *ordonne, structure, rédige*. Transforme les demandes (floues) en tickets clairs,
  priorise, dédup, et traite les remarques que lui renvoie le DEV. → [`kit/PO.md`](kit/PO.md)
- **Session DEV** — *dépile les tickets par priorité et les réalise*. Ne fonce pas en aveugle :
  charge le contexte, **challenge** (manque de détails, incohérence, risque) et remonte ses remarques
  au PO. → [`kit/DEV.md`](kit/DEV.md)

```
                    Humain  ── pilote les 2 sessions en parallèle ──┐
                       │                                            │
                  parle au PO                                 parle au DEV
                       ▼                                            ▼
                  Session PO                                   Session DEV
            cadre · priorise · dédup                    dépile · challenge · réalise
                       │                                            │
                       └──────────────▶  backlog.md  ◀──────────────┘
                                       canal partagé UNIQUE
                                       (viewer backlog.html régénéré à chaque maj)
                                              ▲
                            remarque DEV → PO : ticket [blocked] + @dev-note
                            (le PO la lit dans le backlog et arbitre)
```

> **Le schéma ci-dessus, c'est le mode deux sessions.** En **solo** (le défaut), une seule session fait
> tout dans la racine du repo — rien à isoler. Si tu **montes à deux sessions** parallèles, chacune tourne
> alors **dans son worktree git** (`bin/po` / `bin/dev`) pour ne pas se contaminer. Détail : [`kit/WORKFLOW.md`](kit/WORKFLOW.md).

## Installation

> **Ce que tu déposes dans ton projet = le dossier `simple-ai/` (11 fichiers), PAS tout ce dépôt.**
> Ce repo contient aussi le développement de simple-ai (`dev/`, `example/`, `make-release.sh`…) qui
> **ne va jamais** dans ton projet. Passe par l'**archive `simple-ai.zip`** (page Releases) : elle ne
> contient que le dossier `simple-ai/`. Ne clone pas le repo pour l'installer.

Deux façons, au choix :

- **Archive (le plus simple)** — télécharge `simple-ai.zip` (page Releases, ou `./make-release.sh`),
  **extrais-la à la racine de ton projet** → tu obtiens un dossier `simple-ai/` prêt à l'emploi. Puis
  ouvre une session IA et demande-lui de remplir `simple-ai/PROJECT.md` + `CONFIG.md` (mini-interview).
- **Prompt `/init`** — ouvre [`init.md`](init.md) dans une session IA lancée à la racine de ton repo et
  demande-lui de l'exécuter : elle dépose `simple-ai/`, t'interviewe, génère le viewer.

Dans les deux cas, `simple-ai/` contient :

| Fichier | Rôle | Édité par |
|---------|------|-----------|
| `simple-ai/PO.md` | Playbook casquette **PO** | l'humain (rare) |
| `simple-ai/DEV.md` | Playbook casquette **DEV** | l'humain (rare) |
| `simple-ai/CONVENTION.md` | **Le contrat** : format de ticket, prio, états, remarque DEV→PO, édition atomique | l'humain (rare) |
| `simple-ai/CONFIG.md` | **Où vit le backlog** : `local` (dans le repo) ou `online` (distant/partagé) | l'humain (à l'install) |
| `simple-ai/WORKFLOW.md` | **Git** : sessions concurrentes, branches, merge requests, qui valide | l'humain (rare) |
| `simple-ai/AGENTS.md` | Point d'entrée pour Codex & agents lisant `AGENTS.md` | l'humain (rare) |
| `simple-ai/backlog.md` | **Le backlog unique** — canal de coordination PO ⇄ DEV | PO + DEV (à chaud) |
| `simple-ai/build.py` | Générateur `backlog.md` → `backlog.html` | jamais (outil) |
| `simple-ai/backlog.html` | **Le viewer** (tickets, contexte, avancement) — régénéré à chaque changement | jamais (artefact) |
| `simple-ai/PROJECT.md` | Doc projet d'amorce, accessible depuis le viewer | PO / humain |
| `simple-ai/bin/po`, `bin/dev` | Lanceurs de session (worktree isolé + bannière de rôle) | jamais (outil) |

## Lancer le workflow

**Solo (le défaut)** — ouvre **une** session IA à la racine de ton repo et pilote-la par casquette :
demande-lui d'être **PO** pour cadrer/prioriser, puis **DEV** pour dépiler et réaliser. Elle **annonce**
la casquette qu'elle porte, **relit le backlog avant d'écrire**, et régénère le viewer. **Rien à lancer** :
pas de worktree, pas de script — juste ta session IA habituelle.

**Deux sessions (quand le parallélisme est utile)** — pour cadrer et coder *en même temps*, monte à deux
sessions isolées par worktree :

```bash
simple-ai/bin/po     # session PO  : cadrer, prioriser, traiter les @dev-note
simple-ai/bin/dev    # session DEV : dépiler par priorité, réaliser, prouver
```

Le lanceur **DEV** isole sa session dans un **worktree git dédié** (`../<repo>-dev` : HEAD/fichiers
séparés ; git interdit le même checkout deux fois → garde-fou natif contre la contamination entre
sessions) ; la **PO** travaille dans la racine. Chaque lanceur affiche une **bannière de rôle** et
signale (best-effort) si une autre session du même rôle tourne déjà.

### Solo ou deux sessions ?

Commence **solo** : une session, zéro worktree — ça suffit à la majorité des projets. **Monte à deux
sessions** seulement quand tu as un vrai besoin de **parallélisme** : cadrer le prochain lot pendant que
le code avance, ou un backlog assez gros pour que PO et DEV travaillent sans s'attendre.

## Le viewer

Après **chaque** changement du backlog, l'agent relance le générateur :

```bash
python3 simple-ai/build.py        # → simple-ai/backlog.html
```

Ouvre `simple-ai/backlog.html` dans un navigateur : tickets groupés par epic, badges prio/état,
**estimé `~Nh` / réel `=Nh` + écart** (cf. ci-dessous), contexte dépliable, remarques `@dev-note`
mises en évidence, filtres cliquables. Statique, zéro dépendance.

## Estimation : estimé + réel

Système minimal en deux temps (détail : [`kit/CONVENTION.md`](kit/CONVENTION.md) §10) : le créateur pose
un **estimé** `~Nh`, l'exécutant logge le **réel** `=Nh` à la clôture. Le viewer affiche l'**écart**
(réel − estimé). On ne vise pas l'estimation parfaite — on mesure l'écart pour s'auto-corriger (calibration : SA11).

## Backlog local ou en ligne

Par défaut le backlog est **local** : le fichier `simple-ai/backlog.md` dans ton repo. Mais il peut vivre
**en ligne** — une source distante partagée (un fichier sur un serveur, un gist, un doc partagé…) que
plusieurs projets/sessions lisent, avec un viewer publiable. Tu déclares ça dans
[`kit/CONFIG.md`](kit/CONFIG.md) : passe en `backlog: online` et renseigne **tes** commandes `pull` /
`push` / `publish`. Le framework reste agnostique — il ne connaît que `backlog.md` (copie de travail) ;
c'est toi qui le branches à ta source. **Aucune config de ce genre n'est livrée dans l'archive** : elle
part clean en `local`, tu la configures chez toi.

## Mode TokenBurn (optionnel)

Un run où le DEV **dépile tout le backlog en autonomie, sans interaction humaine**, jusqu'à épuisement
des crédits. Les tickets qui demandent une décision, une action humaine, ou qui manquent de détails sont
**skippés** (passés `blocked` + `@dev-note`), jamais exécutés en aveugle. Détail : [`kit/DEV.md`](kit/DEV.md) §6.

## Exemple

[`example/demo-todo/`](example/demo-todo/) est un projet de démonstration de bout en bout :
un `backlog.md` rempli (epics, états, une remarque DEV→PO) et son `backlog.html` généré.

## Dogfooding

simple-ai **se développe avec simple-ai**. Son propre backlog vit dans [`dev/backlog.md`](dev/backlog.md),
géré par les casquettes du kit (`kit/PO.md` / `kit/DEV.md`) et rendu par son propre générateur
(`python3 kit/build.py dev/backlog.md`). C'est à la fois le meilleur test du framework et un exemple réel.
Le livrable `kit/` reste **clean** : le dogfood vit dans `dev/`, jamais dans `kit/`.

## Distribution

- **Archive** (recommandé) : `./make-release.sh` produit `simple-ai.zip` = le seul dossier `simple-ai/`,
  clean et générique, à extraire dans n'importe quel projet. C'est le livrable.
- **Repo template** : clone ce dépôt et suis [`init.md`](init.md).
- Évolution prévue : une CLI `init` (`npx`/`uvx simple-ai init`).

Le livrable est **dénué de toute config propre à un projet** (le backlog part en `local`, `CONFIG.md` est
un gabarit) : on télécharge, on dépose, on configure chez soi.

## Cibles IA

**Claude Code** d'abord (via `CLAUDE.md` + les playbooks), **Codex** ensuite (via `AGENTS.md`, miroir).
Tout agent capable de lire des fichiers et d'éditer le backlog peut porter une casquette.
