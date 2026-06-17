# simple-ai

Un mini-framework **partageable** qui transforme n'importe quel repo en un workflow **PO ⇄ DEV**
piloté par une IA agentique. On l'ajoute à son projet, on lance **une session PO et une session DEV
en parallèle** (Claude Code, Codex…), et le tout est coordonné par **un backlog unique** + un
**viewer HTML** des tickets et de leur avancement.

Le nom dit la philosophie : **simple**. Le moins de machinerie possible — des fichiers Markdown
lisibles, un viewer HTML statique, **zéro serveur** qui tourne.

## Les deux casquettes

- **Session PO** — *ordonne, structure, rédige*. Transforme les demandes (floues) en tickets clairs,
  priorise, dédup, et traite les remarques que lui renvoie le DEV. → [`kit/PO.md`](kit/PO.md)
- **Session DEV** — *dépile les tickets par priorité et les réalise*. Ne fonce pas en aveugle :
  charge le contexte, **challenge** (manque de détails, incohérence, risque) et remonte ses remarques
  au PO. → [`kit/DEV.md`](kit/DEV.md)

```
   Humain ──demande──▶  Session PO  ──tickets priorisés──▶  backlog.md
                            ▲                                   │
                            └────remarque @dev-note────┐        ▼
                                                       └─ Session DEV ──dépile──▶ réalise
                                                          └─ régénère backlog.html à chaque changement
```

## Installation

`simple-ai` s'installe via le prompt [`init.md`](init.md) : ouvre-le dans une session IA lancée
à la racine de ton repo et demande à l'IA de l'exécuter. Elle dépose `simple-ai/` dans ton projet :

| Fichier | Rôle | Édité par |
|---------|------|-----------|
| `simple-ai/PO.md` | Playbook casquette **PO** | l'humain (rare) |
| `simple-ai/DEV.md` | Playbook casquette **DEV** | l'humain (rare) |
| `simple-ai/CONVENTION.md` | **Le contrat** : format de ticket, prio, états, remarque DEV→PO, édition atomique | l'humain (rare) |
| `simple-ai/AGENTS.md` | Point d'entrée pour Codex & agents lisant `AGENTS.md` | l'humain (rare) |
| `simple-ai/backlog.md` | **Le backlog unique** — canal de coordination PO ⇄ DEV | PO + DEV (à chaud) |
| `simple-ai/build.py` | Générateur `backlog.md` → `backlog.html` | jamais (outil) |
| `simple-ai/backlog.html` | **Le viewer** (tickets, contexte, avancement) — régénéré à chaque changement | jamais (artefact) |
| `simple-ai/PROJECT.md` | Doc projet d'amorce, accessible depuis le viewer | PO / humain |
| `simple-ai/bin/po`, `bin/dev` | Lanceurs de session (worktree isolé + bannière de rôle) | jamais (outil) |

## Lancer le workflow

```bash
simple-ai/bin/po     # session PO  : cadrer, prioriser, traiter les @dev-note
simple-ai/bin/dev    # session DEV : dépiler par priorité, réaliser, prouver
```

Le lanceur **DEV** isole sa session dans un **worktree git dédié** (`../<repo>-dev` : HEAD/fichiers
séparés ; git interdit le même checkout deux fois → garde-fou natif contre la contamination entre
sessions) ; la **PO** travaille dans la racine — donc un checkout **distinct** de celui du DEV.
Chaque lanceur affiche une **bannière de rôle** et signale (best-effort) si une autre session du même rôle tourne déjà.

## Le viewer

Après **chaque** changement du backlog, l'agent relance le générateur :

```bash
python3 simple-ai/build.py        # → simple-ai/backlog.html
```

Ouvre `simple-ai/backlog.html` dans un navigateur : tickets groupés par epic, badges prio/état,
contexte dépliable, remarques `@dev-note` mises en évidence, filtres cliquables. Statique, zéro dépendance.

## Mode TokenBurn (optionnel)

Un run où le DEV **dépile tout le backlog en autonomie, sans interaction humaine**, jusqu'à épuisement
des crédits. Les tickets qui demandent une décision, une action humaine, ou qui manquent de détails sont
**skippés** (passés `blocked` + `@dev-note`), jamais exécutés en aveugle. Détail : [`kit/DEV.md`](kit/DEV.md) §6.

## Exemple

[`example/demo-todo/`](example/demo-todo/) est un projet de démonstration de bout en bout :
un `backlog.md` rempli (epics, états, une remarque DEV→PO) et son `backlog.html` généré.

## Distribution

Aujourd'hui : **repo template** — clone ce dépôt, puis suis [`init.md`](init.md) dans ton projet.
Évolution prévue : une CLI `init` (`npx`/`uvx simple-ai init`).

## Cibles IA

**Claude Code** d'abord (via `CLAUDE.md` + les playbooks), **Codex** ensuite (via `AGENTS.md`, miroir).
Tout agent capable de lire des fichiers et d'éditer le backlog peut porter une casquette.
