# Backlog — Demo To-Do

> Exemple de bout en bout pour simple-ai. Format : voir CONVENTION.md.
> Après chaque édition : `python3 simple-ai/build.py`.

[epic] core — Fonctions de base de la liste
[epic] sync — Synchronisation multi-appareils

[P0][done] Afficher la liste des tâches — sans ça l'app ne sert à rien ~2h @epic:core
[P1][progress] Ajouter une tâche — l'utilisateur doit pouvoir créer une entrée ~1h @epic:core
[P1][todo] Cocher une tâche comme faite — feedback de complétion, base de l'usage quotidien ~1h @epic:core
[P2][todo] Filtrer par statut (toutes / actives / faites) — confort sur les longues listes ~2h @epic:core
[P2][blocked] Synchroniser entre appareils — les utilisateurs changent de device ~8h @epic:sync
  > @dev-note: backend requis, aucun choix de stack ni budget. Décision produit avant exécution.
  > Pistes : service managé (Firebase) vs API maison. À cadrer avec le PO.

[P3][todo] Thème sombre — demandé par plusieurs utilisateurs ~2h
[wishlist][todo] Rappels par notification — nice-to-have, pas prioritaire ~4h
