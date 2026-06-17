#!/usr/bin/env bash
# make-release.sh — produit l'archive livrable de simple-ai.
#
# L'archive contient UNIQUEMENT le dossier `simple-ai/` (le contenu de kit/), prêt à déposer
# à la racine d'un projet. Elle est volontairement DÉNUÉE des fichiers méta du dépôt
# (README, init.md, example/, ce script) et de toute config propre à un projet — c'est un
# framework clean, générique, utilisable directement après extraction.
#
#   Usage : ./make-release.sh [chemin-de-sortie.zip]   (défaut : simple-ai.zip)
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

OUT="${1:-simple-ai.zip}"
rm -f "$OUT"

# git archive n'embarque que les fichiers SUIVIS et committés → pas de copie de travail parasite,
# pas de .session-*.lock, pas de backlog.html généré. Le bit +x des lanceurs est préservé.
git archive --format=zip --prefix=simple-ai/ -o "$OUT" HEAD:kit

echo "✓ $OUT généré."
echo "  Installation : extrais cette archive à la racine de ton projet → tu obtiens simple-ai/,"
echo "  puis suis simple-ai/PROJECT.md et lance simple-ai/bin/po | bin/dev."
echo "--- contenu ---"
unzip -l "$OUT" | awk 'NR>3 && $4 {print "   "$4}' | grep -v '/$' || true
