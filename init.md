# /init — installer simple-ai dans un repo

> **Comment s'en servir** : ouvre ce fichier dans une session IA agentique (Claude Code, Codex…)
> lancée **à la racine du repo cible**, et demande à l'IA d'exécuter ce protocole.
> (Prompt-driven aujourd'hui ; une CLI `init` pourra l'automatiser plus tard.)

Tu es l'IA chargée d'installer **simple-ai** dans le repo courant. Déroule ces étapes :

## 1. Crée l'arborescence `simple-ai/`

À la racine du repo, crée le dossier `simple-ai/` et **copie-y** les fichiers du kit
(depuis ce dépôt simple-ai, dossier `kit/`) :

```
simple-ai/
├── PO.md            ← kit/PO.md         (playbook casquette PO)
├── DEV.md           ← kit/DEV.md        (playbook casquette DEV)
├── CONVENTION.md    ← kit/CONVENTION.md (le contrat de format)
├── CONFIG.md        ← kit/CONFIG.md     (où vit le backlog : local ou online)
├── AGENTS.md        ← kit/AGENTS.md     (point d'entrée Codex & co)
├── build.py         ← kit/build.py      (générateur du viewer)
├── backlog.md       ← kit/backlog.md    (gabarit vide, à personnaliser)
├── PROJECT.md       ← kit/PROJECT.md    (doc d'amorce, à remplir)
└── bin/
    ├── po           ← kit/bin/po        (lanceur session PO)
    └── dev          ← kit/bin/dev       (lanceur session DEV)
```

⚠️ **Rends les lanceurs exécutables après copie** (une copie via un outil d'écriture perd le bit `+x`) :
```
chmod +x simple-ai/bin/po simple-ai/bin/dev simple-ai/build.py
```

## 2. Amorce la doc projet

Interviewe brièvement l'humain (but, périmètre, stack, comment lancer/tester/déployer) et **remplis
`simple-ai/PROJECT.md`** avec ses réponses. Remplace `<NOM DU PROJET>` dans `PROJECT.md` et `backlog.md`.

## 2bis. Choisis où vit le backlog (`CONFIG.md`)

Demande à l'humain : **backlog local ou en ligne ?**
- **Local** (défaut) — laisse `CONFIG.md` tel quel (`backlog: local`). Le backlog vit dans le repo. Rien de plus.
- **En ligne** — le backlog est partagé/distant (serveur, gist, doc partagé…). Passe `CONFIG.md` en
  `backlog: online` et renseigne avec l'humain les commandes `pull` / `push` / `publish` (ses accès à lui).
  N'écris **jamais** de secret dans `CONFIG.md` (utilise ses clés/CLI déjà configurées).

## 3. Génère le viewer une première fois

```
python3 simple-ai/build.py
```

→ crée `simple-ai/backlog.html` (vide pour l'instant). Vérifie qu'il s'ouvre dans un navigateur.

## 4. Branche-toi à l'agent du repo

Pour que les sessions futures sachent qu'il y a un workflow PO/DEV :
- **Claude Code** : ajoute dans le `CLAUDE.md` du repo (crée-le s'il n'existe pas) une ligne :
  *« Workflow PO/DEV : voir `simple-ai/PO.md` et `simple-ai/DEV.md`. Backlog : `simple-ai/backlog.md`. »*
- **Codex** : `simple-ai/AGENTS.md` joue déjà ce rôle ; pointe le `AGENTS.md` racine vers lui si besoin.

## 5. Rends la main

Résume en 3 lignes ce qui a été installé, et indique comment lancer les deux sessions :
```
simple-ai/bin/po     # session PO (cadrer, prioriser)
simple-ai/bin/dev    # session DEV (dépiler, réaliser)
```

C'est tout. Le reste du workflow vit dans `PO.md`, `DEV.md` et `CONVENTION.md`.
