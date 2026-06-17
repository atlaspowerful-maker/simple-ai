# AGENTS.md — simple-ai

> Point d'entrée pour les agents qui lisent `AGENTS.md` (Codex et autres). Miroir de la doctrine
> portée par `CLAUDE.md` côté Claude Code : **mêmes règles**, deux casquettes PO / DEV.

Ce projet est piloté par un workflow **PO ⇄ DEV** coordonné par un backlog unique.

## Au démarrage : choisis ta casquette

- Si on te demande de **groomer / prioriser / cadrer / ajouter au backlog** → tu es **PO**.
  Lis et applique **`simple-ai/PO.md`**. Annonce « casquette PO ».
- Si on te demande d'**implémenter / corriger / faire un ticket** → tu es **DEV**.
  Lis et applique **`simple-ai/DEV.md`**. Annonce « casquette DEV ».

## Le contrat partagé

Le format des tickets, l'échelle de priorité, les états, le canal de remarque DEV→PO et la règle
d'édition atomique sont dans **`simple-ai/CONVENTION.md`**. Tout le monde s'y conforme.

## Le backlog & le viewer

- Backlog unique : `simple-ai/backlog.md`.
- Après **chaque** changement du backlog : `python3 simple-ai/build.py` pour régénérer `simple-ai/backlog.html`.
- Édition **atomique** impérative : relire avant d'écrire, temp + rename (PO et DEV écrivent dans le même fichier).

## Sessions concurrentes

Si une session PO et une session DEV tournent en parallèle, **isole-les par worktree git**
(voir `simple-ai/PO.md` / `simple-ai/DEV.md` et les lanceurs `simple-ai/bin/po` · `simple-ai/bin/dev`).
