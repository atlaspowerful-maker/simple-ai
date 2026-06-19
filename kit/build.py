#!/usr/bin/env python3
"""simple-ai — générateur du viewer.

Parse un `backlog.md` et produit le `backlog.html` correspondant (à côté du backlog),
un viewer statique : tickets, contexte dépliable, états, filtres prio/état, lien PROJECT.md.

Aucune dépendance externe (stdlib uniquement). À relancer après CHAQUE changement du backlog :
    python3 simple-ai/build.py                  # rend le backlog.md à côté du script
    python3 simple-ai/build.py chemin/backlog.md  # rend un backlog précis (→ chemin/backlog.html)
"""
from __future__ import annotations

import hashlib
import html
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Backlog : argument optionnel, sinon celui à côté du script. Le HTML est écrit à côté du backlog.
BACKLOG = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE / "backlog.md"
OUTPUT = BACKLOG.with_suffix(".html")

# Ordre des priorités (cf. CONVENTION.md §3). Inconnu = relégué en fin.
PRIO_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "wishlist": 4}
STATES = ["todo", "progress", "blocked", "done"]

TICKET_RE = re.compile(r"^\[(?P<prio>[^\]]+)\]\[(?P<state>[a-z]+)\]\s+(?P<rest>.*)$")
EPIC_RE = re.compile(r"^\[epic\]\s+(?P<id>\S+)\s+[—-]+\s+(?P<title>.*)$")
CONT_RE = re.compile(r"^\s{2,}>\s?(?P<text>.*)$")
EFFORT_RE = re.compile(r"\s*~([0-9.]+)h\s*$")   # estimé (créateur)
REAL_RE = re.compile(r"\s*=([0-9.]+)h\s*$")      # réel (exécutant, à la clôture)
EPICREF_RE = re.compile(r"\s*@epic:(?P<id>\S+)\s*")
TAG_RE = re.compile(r"\s*#(?P<tag>[\w-]+)\s*$")   # tag libre en FIN de ligne, cf. CONVENTION §7


def parse(text: str):
    epics: dict[str, dict] = {}
    tickets: list[dict] = []
    current = None

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            current = None
            continue

        m_epic = EPIC_RE.match(line)
        if m_epic:
            epics[m_epic["id"]] = {"id": m_epic["id"], "title": m_epic["title"].strip()}
            current = None
            continue

        m_cont = CONT_RE.match(raw)
        if m_cont and current is not None:
            txt = m_cont["text"].strip()
            current["context"].append({
                "text": txt,
                "devnote": txt.startswith("@dev-note:"),
            })
            continue

        m = TICKET_RE.match(line)
        if m:
            rest = m["rest"]
            # Ordre d'extraction : epic puis tags (n'importe où dans la zone méta),
            # puis réel (=Nh), puis estimé (~Nh) ancrés en fin de ce qui reste. On
            # retire epic/tags AVANT le split titre—pourquoi pour ne pas les y laisser.
            epic_id = ""
            mr = EPICREF_RE.search(rest)
            if mr:
                epic_id = mr["id"]
                rest = (rest[: mr.start()] + rest[mr.end():]).rstrip()
            # Tags ancrés en FIN, retirés un par un (de droite à gauche). L'ancrage `$`
            # évite de capturer un « #mot » présent dans le titre/pourquoi (ex. « (#tag) »).
            tags: list[str] = []
            while True:
                mt = TAG_RE.search(rest)
                if not mt:
                    break
                tags.insert(0, mt["tag"])
                rest = rest[: mt.start()].rstrip()
            real = ""
            mrl = REAL_RE.search(rest)
            if mrl:
                real = mrl.group(1)
                rest = rest[: mrl.start()].rstrip()
            est = ""
            me = EFFORT_RE.search(rest)
            if me:
                est = me.group(1)
                rest = rest[: me.start()].rstrip()
            if " — " in rest:
                title, why = rest.split(" — ", 1)
            else:
                title, why = rest, ""
            current = {
                "prio": m["prio"].strip(),
                "state": m["state"].strip(),
                "title": title.strip(),
                "why": why.strip(),
                "est": est,
                "real": real,
                "epic": epic_id,
                "tags": tags,
                "context": [],
            }
            tickets.append(current)
            continue

        current = None  # ligne libre = on coupe le rattachement

    return epics, tickets


def prio_key(t):
    return (PRIO_ORDER.get(t["prio"], 99), STATES.index(t["state"]) if t["state"] in STATES else 99)


def tag_hue(tag: str) -> int:
    """Teinte (0-359) déterministe dérivée du nom du tag — zéro config, stable entre runs.
    (hash() de Python est randomisé par PYTHONHASHSEED ; md5 garantit la stabilité.)"""
    return int(hashlib.md5(tag.encode("utf-8")).hexdigest(), 16) % 360


def render(epics, tickets) -> str:
    counts = {s: sum(1 for t in tickets if t["state"] == s) for s in STATES}
    total = len(tickets)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Regroupement par epic (ordre : epics déclarés, puis "sans epic").
    def _groups(subset):
        gs: list[tuple[str, str, list]] = []
        for eid in list(epics):
            items = sorted([t for t in subset if t["epic"] == eid], key=prio_key)
            if items:
                gs.append((eid, epics[eid]["title"], items))
        orphans = sorted([t for t in subset if t["epic"] not in epics], key=prio_key)
        if orphans:
            gs.append(("", "", orphans))
        return gs

    # Tickets actifs d'abord ; les « done » sortent du flux vers une section dédiée en bas
    # (SA17). Faute de date de clôture dans le format, la section suit le tri commun (epic+prio).
    active_groups = _groups([t for t in tickets if t["state"] != "done"])
    done_groups = _groups([t for t in tickets if t["state"] == "done"])
    groups = active_groups + done_groups
    n_active = len(active_groups)
    n_done = sum(1 for t in tickets if t["state"] == "done")

    cards = []
    for gi, (eid, etitle, items) in enumerate(groups):
        if gi == n_active and done_groups:
            cards.append(
                '<h2 class="epic section-done">Terminés '
                f'<span class="epic-id">{n_done} clos</span></h2>'
            )
        if eid:
            cards.append(
                f'<h2 class="epic">{html.escape(etitle)} '
                f'<span class="epic-id">@epic:{html.escape(eid)}</span></h2>'
            )
        for t in items:
            ctx = ""
            if t["context"]:
                rows = "".join(
                    f'<div class="ctx-row{" devnote" if c["devnote"] else ""}">'
                    f'{html.escape(c["text"])}</div>'
                    for c in t["context"]
                )
                ctx = f'<div class="ctx">{rows}</div>'
            why = f'<span class="why">{html.escape(t["why"])}</span>' if t["why"] else ""
            # Estimé (~Nh) / réel (=Nh) / écart — cf. CONVENTION §10. Les regex capturent
            # le nombre seul ; on ré-ajoute « ~ », « = » et « h » à l'affichage.
            metrics = ""
            if t["est"]:
                metrics += f'<span class="effort" title="estimé">~{html.escape(t["est"])}h</span>'
            if t["real"]:
                metrics += f'<span class="real" title="réel">={html.escape(t["real"])}h</span>'
                try:
                    e, r = float(t["est"]), float(t["real"])
                    if e > 0:
                        d = r - e
                        cls = "over" if d > 0 else ("under" if d < 0 else "spot")
                        metrics += f'<span class="ecart {cls}" title="réel − estimé">{("+" if d > 0 else "")}{d:g}h</span>'
                except ValueError:
                    pass
            # Carte repliable : seul le bloc contexte (.ctx) se replie au clic. Titre,
            # pourquoi et badges restent toujours visibles = ligne scannable. Le caret
            # n'apparaît que sur les cartes qui ont un contexte à dévoiler.
            has_ctx = bool(t["context"])
            cls = "card has-ctx collapsed" if has_ctx else "card"
            caret = '<span class="caret" aria-hidden="true">▸</span>' if has_ctx else ""
            # Chips tag (couche/nature), couleur déterministe par nom — cf. CONVENTION §7.
            tag_chips = "".join(
                f'<span class="tag" style="--h:{tag_hue(tg)}">#{html.escape(tg)}</span>'
                for tg in t["tags"]
            )
            data_tags = html.escape(" ".join(t["tags"]))
            cards.append(
                f'<div class="{cls}" data-state="{t["state"]}" data-prio="{html.escape(t["prio"])}"'
                f' data-tags="{data_tags}">'
                f'<div class="head">'
                f'{caret}'
                f'<span class="badge prio prio-{html.escape(t["prio"])}">{html.escape(t["prio"])}</span>'
                f'<span class="badge state state-{t["state"]}">{t["state"]}</span>'
                f'<span class="title">{html.escape(t["title"])}</span>'
                f'{tag_chips}'
                f'<span class="metrics">{metrics}</span>'
                f'</div>'
                f'<div class="body">{why}{ctx}</div>'
                f'</div>'
            )
    cards_html = "\n".join(cards) if cards else '<p class="empty">Backlog vide. Le PO ajoute des tickets dans <code>backlog.md</code>.</p>'

    prios_present = []
    for t in tickets:
        if t["prio"] not in prios_present:
            prios_present.append(t["prio"])
    prios_present.sort(key=lambda p: PRIO_ORDER.get(p, 99))

    state_chips = "".join(
        f'<button class="chip f-state" data-f="{s}">{s} <b>{counts[s]}</b></button>' for s in STATES
    )
    prio_chips = "".join(
        f'<button class="chip f-prio" data-f="{html.escape(p)}">{html.escape(p)}</button>' for p in prios_present
    )
    tags_present = sorted({tg for t in tickets for tg in t["tags"]})
    tag_chips = "".join(
        f'<button class="chip f-tag" data-f="{html.escape(tg)}" style="--h:{tag_hue(tg)}">#{html.escape(tg)}</button>'
        for tg in tags_present
    )

    return TEMPLATE.format(
        total=total,
        generated=generated,
        state_chips=state_chips,
        prio_chips=prio_chips,
        tag_chips=tag_chips,
        cards=cards_html,
    )


TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>simple-ai — backlog</title>
<style>
  :root {{
    --bg:#0f1115; --card:#181b22; --line:#262a33; --txt:#e6e8ec; --dim:#9aa0aa;
    --p0:#ef4444; --p1:#f59e0b; --p2:#3b82f6; --p3:#8b5cf6; --wish:#6b7280;
    --todo:#6b7280; --progress:#3b82f6; --blocked:#ef4444; --done:#22c55e;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--txt);
    font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }}
  header {{ padding:24px 28px 12px; border-bottom:1px solid var(--line); }}
  h1 {{ margin:0 0 4px; font-size:20px; }}
  .meta {{ color:var(--dim); font-size:13px; }}
  .meta a {{ color:var(--progress); text-decoration:none; }}
  .filters {{ display:flex; flex-wrap:wrap; gap:8px; padding:14px 28px; border-bottom:1px solid var(--line); }}
  .chip {{ background:var(--card); color:var(--txt); border:1px solid var(--line);
    border-radius:999px; padding:5px 12px; font-size:13px; cursor:pointer; }}
  .chip.off {{ opacity:.35; }}
  .chip b {{ color:var(--dim); }}
  main {{ padding:18px 28px 60px; max-width:920px; }}
  .epic {{ font-size:15px; color:var(--dim); margin:26px 0 10px; font-weight:600;
    text-transform:uppercase; letter-spacing:.04em; }}
  .epic-id {{ font-weight:400; opacity:.6; font-size:12px; }}
  .section-done {{ margin-top:34px; border-top:1px solid var(--line); padding-top:8px; color:var(--done); }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:10px;
    padding:12px 14px; margin:8px 0; }}
  .head {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; }}
  .badge {{ font-size:11px; font-weight:700; padding:2px 7px; border-radius:5px; text-transform:uppercase; }}
  .prio-P0 {{ background:var(--p0); }} .prio-P1 {{ background:var(--p1); color:#111; }}
  .prio-P2 {{ background:var(--p2); }} .prio-P3 {{ background:var(--p3); }}
  .prio-wishlist {{ background:var(--wish); }}
  .state-todo {{ background:var(--todo); }} .state-progress {{ background:var(--progress); }}
  .state-blocked {{ background:var(--blocked); }} .state-done {{ background:var(--done); color:#062b13; }}
  .title {{ font-weight:600; }}
  .tag {{ background:hsl(var(--h),45%,30%); color:#eceef2; font-size:11px; font-weight:600;
    padding:1px 7px; border-radius:999px; }}
  .chip.f-tag {{ background:hsl(var(--h),40%,22%); border-color:hsl(var(--h),40%,38%); }}
  .metrics {{ margin-left:auto; display:flex; gap:6px; align-items:center; font-size:12px; white-space:nowrap; }}
  .effort {{ background:rgba(245,158,11,.16); color:#fbbf24; padding:1px 6px; border-radius:5px; font-weight:600; }}
  .real {{ color:var(--txt); font-weight:600; }}
  .ecart {{ padding:1px 6px; border-radius:5px; font-weight:700; }}
  .ecart.over {{ background:rgba(239,68,68,.18); color:#fca5a5; }}
  .ecart.under {{ background:rgba(34,197,94,.18); color:#86efac; }}
  .ecart.spot {{ background:rgba(107,114,128,.25); color:var(--dim); }}
  .body {{ margin-top:6px; }}
  .why {{ color:var(--dim); font-size:14px; }}
  .ctx {{ margin-top:8px; border-left:2px solid var(--line); padding-left:10px; }}
  .ctx-row {{ color:var(--dim); font-size:13px; padding:1px 0; }}
  .ctx-row.devnote {{ color:var(--blocked); font-weight:500; }}
  .card.done {{ opacity:.55; }}
  .caret {{ color:var(--dim); font-size:11px; line-height:1; display:inline-block; transition:transform .15s; }}
  .card:not(.collapsed) .caret {{ transform:rotate(90deg); }}
  .card.has-ctx {{ cursor:pointer; }}
  .card.collapsed .ctx {{ display:none; }}
  .empty {{ color:var(--dim); }}
  code {{ background:var(--card); padding:1px 5px; border-radius:4px; }}
</style>
</head>
<body>
<header>
  <h1>📋 Backlog — {total} ticket(s)</h1>
  <div class="meta">Généré le {generated} · <a href="PROJECT.md">PROJECT.md</a> · source : <code>backlog.md</code></div>
</header>
<div class="filters">
  {state_chips}
  <span style="width:12px"></span>
  {prio_chips}
  <span style="width:12px"></span>
  {tag_chips}
</div>
<main id="list">
{cards}
</main>
<script>
  const active = {{ state:new Set(), prio:new Set(), tags:new Set() }};
  function apply() {{
    document.querySelectorAll('.card').forEach(c => {{
      const okS = active.state.size===0 || active.state.has(c.dataset.state);
      const okP = active.prio.size===0 || active.prio.has(c.dataset.prio);
      const ct = (c.dataset.tags || '').split(' ').filter(Boolean);
      const okT = active.tags.size===0 || ct.some(t => active.tags.has(t));
      c.style.display = (okS && okP && okT) ? '' : 'none';
    }});
  }}
  function wire(sel, bucket) {{
    document.querySelectorAll(sel).forEach(b => b.addEventListener('click', () => {{
      const v = b.dataset.f;
      if (active[bucket].has(v)) {{ active[bucket].delete(v); b.classList.add('off'); }}
      else {{ active[bucket].add(v); b.classList.remove('off'); }}
      apply();
    }}));
  }}
  wire('.f-state','state'); wire('.f-prio','prio'); wire('.f-tag','tags');
  document.querySelectorAll('.card[data-state=done]').forEach(c => c.classList.add('done'));
  // Repli/dépli du contexte au clic sur la carte (seules les cartes .has-ctx).
  document.querySelectorAll('.card.has-ctx').forEach(c =>
    c.addEventListener('click', () => c.classList.toggle('collapsed')));
</script>
</body>
</html>
"""


def main():
    if not BACKLOG.exists():
        raise SystemExit(f"Introuvable : {BACKLOG}. Crée d'abord simple-ai/backlog.md.")
    epics, tickets = parse(BACKLOG.read_text(encoding="utf-8"))
    OUTPUT.write_text(render(epics, tickets), encoding="utf-8")
    print(f"✓ {OUTPUT.name} généré — {len(tickets)} ticket(s), {len(epics)} epic(s).")


if __name__ == "__main__":
    main()
