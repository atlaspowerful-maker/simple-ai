# /init — installer simple-ai dans un repo

> **Comment s'en servir** : ouvre ce fichier dans une session IA agentique (Claude Code, Codex…)
> lancée **à la racine du repo cible**, et demande à l'IA d'exécuter ce protocole.
> (Prompt-driven aujourd'hui ; une CLI `init` pourra l'automatiser plus tard.)

Tu es l'IA chargée d'installer **simple-ai** dans le repo courant. Déroule ces étapes :

## 1. Pose l'arborescence `simple-ai/`

**Le plus simple — l'archive (ou la CLI).** Extrais `simple-ai.zip` (page Releases, ou `./make-release.sh`)
**à la racine du repo** → tu obtiens un dossier `simple-ai/` **prêt**, bit `+x` des lanceurs **préservé**.
Rien à copier, pas de `chmod`. (Équivalent : `uvx simple-ai init`.)

**Sinon — copie manuelle** depuis ce dépôt simple-ai (dossier `kit/`). Crée `simple-ai/` et copie-y :

```
simple-ai/
├── PO.md            ← kit/PO.md         (playbook casquette PO)
├── DEV.md           ← kit/DEV.md        (playbook casquette DEV)
├── CONVENTION.md    ← kit/CONVENTION.md (le contrat de format)
├── CONFIG.md        ← kit/CONFIG.md     (où vit le backlog : local ou online)
├── WORKFLOW.md      ← kit/WORKFLOW.md   (git : sessions, branches, merge, qui valide)
├── AGENTS.md        ← kit/AGENTS.md     (point d'entrée Codex & co)
├── build.py         ← kit/build.py      (générateur du viewer)
├── calibrate.py     ← kit/calibrate.py  (calibration des estimations, SA11)
├── backlog.md       ← kit/backlog.md    (gabarit vide, à personnaliser)
├── PROJECT.md       ← kit/PROJECT.md    (doc d'amorce, à remplir)
└── bin/
    ├── po           ← kit/bin/po        (lanceur session PO)
    └── dev          ← kit/bin/dev       (lanceur session DEV)
```

> `kit/test_build.py` (test interne du parser) **n'est pas livré** : il reste au dépôt simple-ai.

⚠️ **Copie manuelle uniquement** : une copie via un outil d'écriture **perd le `+x`** des lanceurs (sinon
`bin/po` / `bin/dev` refuseront de se lancer). L'archive et la CLI, elles, le préservent. Rends-les exécutables :
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

## 4. Branche-toi à l'agent du repo (ne saute pas cette étape)

C'est le **pivot** : sans elle, le kit est posé mais **invisible** pour tes futures sessions. **Fais-la
systématiquement.**
- **Claude Code** : ajoute dans le `CLAUDE.md` du repo (crée-le s'il n'existe pas) ces deux lignes :
  *« Workflow PO/DEV piloté par simple-ai : voir `simple-ai/PO.md`, `simple-ai/DEV.md`, `simple-ai/CONVENTION.md`. Backlog : `simple-ai/backlog.md`. »*
  *« Par défaut **solo** : une session porte les deux casquettes tour à tour (annonce la casquette, relis le backlog avant d'écrire). Deux sessions = montée en puissance via `simple-ai/bin/po` · `bin/dev`. »*
- **Codex** : `simple-ai/AGENTS.md` joue déjà ce rôle ; pointe le `AGENTS.md` racine vers lui si besoin.

## 5. Rends la main

Résume en 3 lignes ce qui a été installé, et indique comment démarrer :
- **Solo (le défaut)** — reste dans cette session (ou ouvre-en une à la racine) et demande-lui d'être
  **PO** pour cadrer le backlog, puis **DEV** pour dépiler. Rien d'autre à lancer, pas de worktree.
- **Deux sessions** (seulement si besoin de parallélisme) :
  ```
  simple-ai/bin/po     # session PO (cadrer, prioriser)
  simple-ai/bin/dev    # session DEV (dépiler, réaliser)
  ```

C'est tout. Le reste du workflow vit dans `PO.md`, `DEV.md` et `CONVENTION.md`.
