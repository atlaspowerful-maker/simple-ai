#!/usr/bin/env python3
"""simple-ai — CLI d'installation (remplace le prompt /init).

    uvx simple-ai init [chemin]   # pose simple-ai/ dans le repo (défaut : .)

Pose le dossier `simple-ai/` (copie du kit empaqueté), rend les lanceurs exécutables,
et imprime les prochaines étapes. Zéro dépendance (stdlib). Le détail du workflow vit
ensuite dans simple-ai/PO.md · DEV.md · CONVENTION.md.
"""
from __future__ import annotations

import argparse
import shutil
import stat
import sys
from pathlib import Path

# Snapshot du kit empaqueté avec le CLI (synchronisé depuis kit/ au build — cf. sync-kit.sh).
KIT = Path(__file__).resolve().parent / "_kit"
EXECUTABLES = ("bin/po", "bin/dev", "build.py")


def _make_executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def init(target_root: Path) -> int:
    if not KIT.is_dir():
        print("Erreur : kit empaqueté introuvable. Build incomplet "
              "(lance cli/sync-kit.sh avant de packager).", file=sys.stderr)
        return 2
    dest = target_root / "simple-ai"
    if dest.exists():
        print(f"⚠️  {dest}/ existe déjà — rien d'écrasé. Supprime-le pour réinstaller.",
              file=sys.stderr)
        return 1
    shutil.copytree(KIT, dest)
    for rel in EXECUTABLES:
        p = dest / rel
        if p.exists():
            _make_executable(p)
    print(f"✓ simple-ai/ posé dans {target_root}")
    print("  Prochaines étapes :")
    print("  1. Remplis simple-ai/PROJECT.md (but, périmètre, stack) et CONFIG.md (backlog local/online).")
    print("  2. Génère le viewer : python3 simple-ai/build.py")
    print("  3. Solo (défaut) : demande à ta session IA d'être PO puis DEV. "
          "Deux sessions : simple-ai/bin/po · bin/dev.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="simple-ai", description="Installe simple-ai dans un repo.")
    sub = parser.add_subparsers(dest="cmd")
    p_init = sub.add_parser("init", help="pose le dossier simple-ai/ dans le repo")
    p_init.add_argument("path", nargs="?", default=".", help="racine du repo cible (défaut : .)")
    args = parser.parse_args(argv)

    if args.cmd == "init":
        return init(Path(args.path).resolve())
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
