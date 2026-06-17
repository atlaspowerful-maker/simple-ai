#!/usr/bin/env python3
"""simple-ai — routine de calibration des estimations (SA11).

Lit les tickets `done` qui portent un **estimé** (`~Nh`) ET un **réel** (`=Nh`),
calcule pour chacun le ratio `réel / estimé`, et propose comme **facteur de
calibration** la **médiane** de ces ratios (cf. CONVENTION.md §10).

On **mesure et on suggère** — l'humain décide. Aucun automatisme imposé.

Source des couples (estimé, réel) :
- le backlog passé en argument (ou `backlog.md` à côté du script),
- et, s'il existe à côté, un `backlog-archive.md` (les `done` archivés restent
  de la matière première — cf. CONVENTION.md §10 « Rétention »).

Aucune dépendance externe : stdlib + réutilisation de `build.parse` (importable).

    python3 simple-ai/calibrate.py                  # calibre le backlog.md voisin (+ archive)
    python3 simple-ai/calibrate.py chemin/backlog.md  # calibre un backlog précis
"""
from __future__ import annotations

import statistics
import sys
from pathlib import Path

import build  # réutilise le parseur de référence (CONVENTION.md §10)

HERE = Path(__file__).resolve().parent


def couples(tickets: list[dict]) -> list[dict]:
    """Garde les tickets `done` ayant un estimé ET un réel exploitables (>0)."""
    out = []
    for t in tickets:
        if t.get("state") != "done" or not t.get("est") or not t.get("real"):
            continue
        try:
            est, real = float(t["est"]), float(t["real"])
        except ValueError:
            continue
        if est <= 0 or real <= 0:
            continue
        out.append({"title": t["title"], "prio": t["prio"], "est": est,
                    "real": real, "ratio": real / est})
    return out


def factor(items: list[dict]) -> float | None:
    """Facteur de calibration suggéré = médiane des ratios (None si aucun couple)."""
    if not items:
        return None
    return statistics.median(c["ratio"] for c in items)


def breakdown(items: list[dict], keyfn) -> dict:
    """Groupe les couples par keyfn → {clé: (nombre, médiane des ratios)}.
    Sert au raffinement par priorité / par taille (CONVENTION §10)."""
    groups: dict = {}
    for c in items:
        groups.setdefault(keyfn(c), []).append(c["ratio"])
    return {k: (len(v), statistics.median(v)) for k, v in groups.items()}


def load_tickets(backlog: Path) -> list[dict]:
    """Tickets du backlog + ceux d'un éventuel `backlog-archive.md` voisin."""
    sources = [backlog]
    archive = backlog.with_name("backlog-archive.md")
    if archive.exists() and archive != backlog:
        sources.append(archive)
    tickets: list[dict] = []
    for src in sources:
        _, parsed = build.parse(src.read_text(encoding="utf-8"))
        tickets.extend(parsed)
    return tickets


def report(items: list[dict]) -> str:
    lines = ["Calibration des estimations — simple-ai", ""]
    if not items:
        lines += [
            "Aucun ticket `done` avec estimé (~Nh) ET réel (=Nh) — rien à calibrer.",
            "Logge le réel à la clôture de tes tickets (CONVENTION.md §10) pour amorcer.",
        ]
        return "\n".join(lines)

    f = factor(items)
    lines.append(f"{len(items)} ticket(s) done avec estimé + réel :")
    for c in sorted(items, key=lambda x: x["ratio"]):
        lines.append(
            f"  ~{c['est']:g}h → ={c['real']:g}h   ratio ×{c['ratio']:.2f}   "
            f"[{c['prio']}] {c['title']}"
        )
    lines += ["", f"Facteur de calibration suggéré (médiane des ratios) : ×{f:.2f}"]

    pct = abs(f - 1) * 100
    if f > 1:
        lines.append(
            f"→ Tes estimés sous-estiment d'environ {pct:.0f} %. "
            f"Pour t'ajuster, multiplie tes futurs ~Nh par {f:.2f}."
        )
    elif f < 1:
        lines.append(
            f"→ Tes estimés surestiment d'environ {pct:.0f} %. "
            f"Pour t'ajuster, multiplie tes futurs ~Nh par {f:.2f}."
        )
    else:
        lines.append("→ Tes estimés tombent juste en médiane. Rien à ajuster.")

    # Raffinements (CONVENTION §10 « on peut raffiner par priorité ») — secondaires au
    # facteur global, affichés seulement s'il y a de quoi distinguer (≥2 groupes).
    by_prio = breakdown(items, lambda c: c["prio"])
    if len(by_prio) > 1:
        lines.append("")
        lines.append("Par priorité :")
        for p in sorted(by_prio, key=lambda k: build.PRIO_ORDER.get(k, 99)):
            n, med = by_prio[p]
            lines.append(f"  {p:<9} ×{med:.2f}  ({n} ticket{'s' if n > 1 else ''})")
    by_size = breakdown(items, lambda c: "≤2h" if c["est"] <= 2 else ">2h")
    if len(by_size) > 1:
        lines.append("")
        lines.append("Par taille d'estimé :")
        for s in ("≤2h", ">2h"):
            if s in by_size:
                n, med = by_size[s]
                lines.append(f"  {s:<9} ×{med:.2f}  ({n} ticket{'s' if n > 1 else ''})")

    lines.append("")
    lines.append("  (mesure indicative — l'humain décide ; cf. CONVENTION.md §10)")
    return "\n".join(lines)


def main():
    backlog = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE / "backlog.md"
    if not backlog.exists():
        raise SystemExit(f"Introuvable : {backlog}. Crée d'abord simple-ai/backlog.md.")
    items = couples(load_tickets(backlog))
    print(report(items))


if __name__ == "__main__":
    main()
