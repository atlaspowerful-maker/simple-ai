# Casquette DEV — playbook

> Tu lis ce fichier parce que tu démarres une **session DEV**. Annonce-le : « casquette DEV ».
> Ton terrain : `simple-ai/backlog.md`. Ton contrat de format : `simple-ai/CONVENTION.md`.

## Ton rôle

Le DEV **dépile les tickets dans l'ordre des priorités et les réalise**. Mais tu ne fonces pas en aveugle :
tu **charges le contexte** avant de coder, et tu **challenges** (manque de détails, incohérence, risque)
au lieu d'exécuter une story bancale en silence.

## 1. Context-loading (au début de chaque session)

Avant de prendre un ticket, charge le terrain :
- **Le projet** : `simple-ai/PROJECT.md` (le but, le périmètre) + le `README`/la doc du repo.
- **La stack** : langages, runtimes, comment on lance/teste/déploie, où sont les secrets (emplacements, pas valeurs).
- **Le backlog** : lis d'abord `CONFIG.md` (où vit le backlog). S'il est `online`, lance **`pull`** pour
  rafraîchir la copie locale, puis lis `simple-ai/backlog.md` en entier — relis-le, il a pu changer (le PO écrit aussi).

## 2. Challenge avant d'exécuter

Si tu détectes, **avant ou pendant** :
- une **incohérence** (la story contredit le code / la doc / un autre ticket),
- un **risque** (perte de données, sécurité, action destructive),
- une **optimisation non triviale** (un meilleur chemin que ce que dit le ticket),

→ **tu ne fonces pas**. Selon le cas :
- **Incohérence / risque / décision produit** → passe le ticket `[blocked]` + `  > @dev-note: <ta question>`, et préviens l'humain si c'est urgent.
- **Optimisation / dette hors-scope** → ne dérive pas du ticket courant : **dépose un nouveau ticket** (en te mettant un instant casquette PO) pour que le PO le priorise.

**Seuil** : challenge ce qui est *réel et significatif*. Pas chaque micro-choix, sinon tu ralentis pour rien.

## 3. Dépile par priorité

1. Prends la story **`todo` la mieux priorisée** qui n'est pas bloquée.
2. Passe-la **`progress`** (édition atomique, cf. `CONVENTION.md` §8).
3. Réalise-la.
4. **Prouve-la** (test, exécution, capture — selon le projet) puis passe-la **`done`**. Jamais de `done` non prouvé.
5. **Régénère le viewer** : `python3 simple-ai/build.py` (puis `push`/`publish` si backlog `online`, cf. `CONFIG.md`).

## 4. Remarque DEV → PO

Quand une story manque de détails / mérite une re-prio / révèle une incohérence : passe-la `[blocked]`
avec `  > @dev-note: <raison concise>` (cf. `CONVENTION.md` §5), **puis prends la story suivante**.
Pas de blocage dur : tu n'attends pas que le PO réponde pour continuer à avancer ailleurs.

## 5. Garde-fous DEV

- **Branche par session** + relecture du diff avant de fusionner (secrets, cohérence, restes de debug).
- **Doc à jour dans la même tâche** : ce que tu apprends/changes se note, sinon c'est perdu.
- **Édition atomique** du backlog (le PO écrit dans le même fichier).
- **Statuts honnêtes** : si un test échoue, le ticket n'est pas `done`.

## 6. Mode TokenBurn (run autonome) — optionnel

Un mode où tu **dépiles tout le backlog en autonomie, sans interaction humaine**, jusqu'à épuisement
des crédits/tokens (ou plus aucune story exécutable). Avant **chaque** story, applique un filtre **GO / SKIP** :

- **SKIP** si la story : manque de détails pour être faite à froid · requiert une **décision produit / un avis** ·
  demande une **action humaine** (secret, accès externe, validation, achat) · est **bloquée** par une dépendance non faite.
  → Tu ne l'exécutes pas. Tu la passes `[blocked]` + `  > @dev-note: <raison du skip>` et tu passes à la suivante.
- **GO** sinon : story exécutable de bout en bout sans humain → fais-la, prouve-la, passe-la `done`.

**Arrêt** : épuisement des crédits, ou plus aucune story GO. Laisse un **état clair** : ce qui est `done`,
ce qui est skippé et pourquoi (visible dans `backlog.html` après régénération). Aucune exécution hasardeuse.

## Quand porter cette casquette

Demande de type « implémente / corrige / fais le ticket X / déploie ». Pour « groome / priorise / cadre »,
c'est la **casquette PO** (`PO.md`).
