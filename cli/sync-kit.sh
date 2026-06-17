#!/usr/bin/env bash
# sync-kit.sh — synchronise le snapshot du kit empaqueté avec le CLI depuis la SOURCE UNIQUE (kit/).
# À lancer avant tout build/publish. simple_ai/_kit/ est gitignoré : jamais édité à la main, toujours
# régénéré ici (même principe que example/, cf. example/README.md).
set -euo pipefail
ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
DEST="$(dirname "$0")/simple_ai/_kit"
rm -rf "$DEST"
mkdir -p "$DEST"
# git archive = uniquement les fichiers suivis (pas de .pyc, lock, html généré), +x préservé.
git -C "$ROOT" archive HEAD:kit | tar -x -C "$DEST"
echo "✓ snapshot kit/ → $DEST ($(find "$DEST" -type f | wc -l | tr -d ' ') fichiers)"
