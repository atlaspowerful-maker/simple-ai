# CONFIG — où vit le backlog

> Ce fichier déclare **où vit le backlog** du projet et, s'il est en ligne, **comment le synchroniser**.
> Le PO, le DEV et le viewer le consultent. C'est le **seul** endroit qui contient une config propre à
> ton projet — le reste du framework est générique.

## Mode

```
backlog: local
```

- **`local`** (défaut) — le backlog est le fichier `simple-ai/backlog.md` versionné dans ce repo.
  Rien d'autre à configurer. Le viewer (`backlog.html`) se génère et se lit localement.
- **`online`** — le backlog vit dans une **source distante partagée** (un fichier sur un serveur, un
  gist, un document partagé, une API…). Plusieurs projets/sessions peuvent le lire ; le viewer peut être
  publié sur le web. Dans ce cas, remplis la section ci-dessous.

> Pour passer en ligne : remplace `local` par `online` et renseigne les 3 commandes ci-dessous.

## Mode `online` — commandes de synchronisation

Le framework reste agnostique : **toi** tu fournis les commandes shell qui parlent à ta source distante.
`simple-ai/backlog.md` sert alors de **copie de travail** locale (on tire avant de lire, on pousse après écriture).

```
# pull — récupère le backlog distant et écrit simple-ai/backlog.md
pull:    # ex. scp user@host:/chemin/backlog.md simple-ai/backlog.md

# push — renvoie simple-ai/backlog.md (modifié) vers la source distante (écriture ATOMIQUE côté distant)
push:    # ex. scp simple-ai/backlog.md user@host:/chemin/backlog.md

# publish — (optionnel) publie le viewer simple-ai/backlog.html en ligne
publish: # ex. scp simple-ai/backlog.html user@host:/var/www/backlog/index.html
```

### Boucle de travail en mode `online`
1. **Avant de lire/éditer** le backlog : lance la commande `pull` (la copie locale peut être périmée).
2. Édite `simple-ai/backlog.md` (PO ou DEV), puis `python3 simple-ai/build.py`.
3. **Après écriture** : lance `push` (et `publish` si défini).
4. **Édition atomique** : la source distante est partagée → tes commandes `push` doivent écrire
   atomiquement (temp + rename côté distant) et, si possible, `pull` juste avant pour ne pas écraser
   une modif concurrente. C'est la même règle que `CONVENTION.md §8`, étendue au distant.

> ⚠️ Ne mets **jamais** de secret (mot de passe, token) dans ce fichier. Utilise des accès déjà
> configurés sur ta machine (clé SSH, profil CLI…). Si tu versionnes ce projet, ce `CONFIG.md` peut
> contenir un host/chemin — assure-toi que ce n'est pas sensible, ou garde-le hors du repo.
