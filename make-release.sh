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

# --- Garde-fou anti-fuite (SA20) ----------------------------------------------------------
# Le livrable doit rester GÉNÉRIQUE : aucune référence interne à un projet ne doit s'y glisser.
# On scanne le CONTENU RÉEL de l'archive (= kit/) contre des motifs de fuite : adresses IP et
# emails/domaines (génériques), plus d'éventuels marqueurs propres au projet listés dans
# .release-denylist (1 motif ERE par ligne, '#' = commentaire). Ce fichier est gitignoré : on y
# met ses marqueurs internes (nom de code, domaine, IP du hub…) sans jamais les publier ici.
scan_dir="$(mktemp -d)"
pat_file="$(mktemp)"
trap 'rm -rf "$scan_dir" "$pat_file"' EXIT
unzip -q "$OUT" -d "$scan_dir"

printf '%s\n' \
  '([0-9]{1,3}\.){3}[0-9]{1,3}' \
  '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' \
  > "$pat_file"
if [ -f .release-denylist ]; then
  grep -vE '^[[:space:]]*(#|$)' .release-denylist >> "$pat_file" || true
fi

if leaks="$(grep -rinEf "$pat_file" "$scan_dir")"; then
  echo "✗ Release REFUSÉE — référence interne détectée dans l'archive :" >&2
  printf '%s\n' "$leaks" | sed "s#^$scan_dir/#   #" >&2
  echo "  → corrige kit/ (le livrable doit rester générique), ou ajuste .release-denylist." >&2
  rm -f "$OUT"
  exit 1
fi
# ------------------------------------------------------------------------------------------

echo "✓ $OUT généré (garde-fou anti-fuite : aucune réf interne détectée)."
echo "  Installation : extrais cette archive à la racine de ton projet → tu obtiens simple-ai/,"
echo "  puis suis simple-ai/PROJECT.md et lance simple-ai/bin/po | bin/dev."
echo "--- contenu ---"
unzip -l "$OUT" | awk 'NR>3 && $4 {print "   "$4}' | grep -v '/$' || true
