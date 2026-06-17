#!/usr/bin/env python3
"""Tests de build.parse() — le parseur de référence du backlog.

calibrate.py (SA11) en dépend en prod et l'extraction fin-de-ligne est subtile
(epic @epic:id n'importe où, puis réel =Nh, puis estimé ~Nh, tous ancrés en fin).
Filet stdlib, aucune dépendance :

    python3 simple-ai/test_build.py            # ou : python3 -m unittest test_build
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402


def one(text: str) -> dict:
    """Parse un texte d'un seul ticket et renvoie ce ticket."""
    _, tickets = build.parse(text)
    assert len(tickets) == 1, f"attendu 1 ticket, obtenu {len(tickets)}"
    return tickets[0]


class TicketDeBase(unittest.TestCase):
    def test_champs_minimaux(self):
        t = one("[P1][todo] Titre court — pourquoi actionnable")
        self.assertEqual(t["prio"], "P1")
        self.assertEqual(t["state"], "todo")
        self.assertEqual(t["title"], "Titre court")
        self.assertEqual(t["why"], "pourquoi actionnable")
        self.assertEqual(t["est"], "")
        self.assertEqual(t["real"], "")
        self.assertEqual(t["epic"], "")

    def test_sans_pourquoi(self):
        t = one("[P3][done] Juste un titre")
        self.assertEqual(t["title"], "Juste un titre")
        self.assertEqual(t["why"], "")

    def test_etat_et_prio_varies(self):
        for prio in ("P0", "P1", "P2", "P3", "wishlist"):
            for state in ("todo", "progress", "blocked", "done"):
                t = one(f"[{prio}][{state}] X — y")
                self.assertEqual((t["prio"], t["state"]), (prio, state))


class ExtractionFinDeLigne(unittest.TestCase):
    """Le cœur du risque : ordre @epic → =Nh → ~Nh, chacun ancré en fin."""

    def test_estime_seul(self):
        t = one("[P2][todo] T — w ~2h")
        self.assertEqual(t["est"], "2")
        self.assertEqual(t["real"], "")
        self.assertEqual(t["why"], "w")

    def test_reel_seul_sans_estime(self):
        t = one("[P2][done] T — w =3h")
        self.assertEqual(t["est"], "")
        self.assertEqual(t["real"], "3")

    def test_estime_puis_reel(self):
        t = one("[P2][done] T — w ~5h =7h")
        self.assertEqual(t["est"], "5")
        self.assertEqual(t["real"], "7")
        self.assertEqual(t["why"], "w")

    def test_decimaux(self):
        t = one("[P3][done] T — w ~1.5h =0.5h")
        self.assertEqual(t["est"], "1.5")
        self.assertEqual(t["real"], "0.5")

    def test_epic_en_fin(self):
        t = one("[P1][todo] T — w @epic:core")
        self.assertEqual(t["epic"], "core")
        self.assertEqual(t["why"], "w")

    def test_combo_complet_epic_reel_estime(self):
        # L'ordre d'extraction doit donner exactement ces champs, sans fuite.
        t = one("[P3][done] Routine SA11 — médiane des ratios ~3h =2h @epic:core")
        self.assertEqual(t["epic"], "core")
        self.assertEqual(t["est"], "3")
        self.assertEqual(t["real"], "2")
        self.assertEqual(t["title"], "Routine SA11")
        self.assertEqual(t["why"], "médiane des ratios")

    def test_pas_de_fuite_dans_le_pourquoi(self):
        # Aucun résidu ~Nh/=Nh/@epic ne doit rester dans why.
        t = one("[P2][done] T — un pourquoi ~4h =6h @epic:dx")
        self.assertNotIn("~", t["why"])
        self.assertNotIn("=", t["why"])
        self.assertNotIn("@epic", t["why"])
        self.assertEqual(t["why"], "un pourquoi")


class TitreAvecTiret(unittest.TestCase):
    def test_split_sur_premier_separateur(self):
        # " — " (tiret cadratin entouré d'espaces) est le séparateur ; un "-" simple
        # dans le titre ne doit pas être confondu.
        t = one("[P1][todo] Filtre par date sur la liste — retrouver une entrée ancienne")
        self.assertEqual(t["title"], "Filtre par date sur la liste")
        self.assertEqual(t["why"], "retrouver une entrée ancienne")

    def test_plusieurs_separateurs(self):
        t = one("[P1][todo] A — B — C")
        self.assertEqual(t["title"], "A")
        self.assertEqual(t["why"], "B — C")


class TagsLibres(unittest.TestCase):
    """#tag : 0 / 1 / N tags + cohabitation avec epic, réel, estimé (cf. CONVENTION §7)."""

    def test_zero_tag(self):
        t = one("[P2][todo] T — w ~2h @epic:core")
        self.assertEqual(t["tags"], [])
        self.assertEqual(t["why"], "w")  # rien ne fuit

    def test_un_tag(self):
        t = one("[P2][todo] T — w #back")
        self.assertEqual(t["tags"], ["back"])
        self.assertEqual(t["why"], "w")

    def test_plusieurs_tags(self):
        t = one("[P2][todo] T — w #back #infra")
        self.assertEqual(t["tags"], ["back", "infra"])
        self.assertEqual(t["why"], "w")

    def test_tag_avec_tiret(self):
        t = one("[P3][todo] T — w #ci-cd")
        self.assertEqual(t["tags"], ["ci-cd"])

    def test_cohabitation_epic_estime_reel_tags(self):
        # Le cas qui couvre tout l'ordre d'extraction d'un coup.
        t = one("[P2][done] Titre — pourquoi ~2h =1h @epic:core #back #infra")
        self.assertEqual(t["tags"], ["back", "infra"])
        self.assertEqual(t["epic"], "core")
        self.assertEqual(t["est"], "2")
        self.assertEqual(t["real"], "1")
        self.assertEqual(t["title"], "Titre")
        self.assertEqual(t["why"], "pourquoi")
        for residu in ("#", "@epic", "~", "="):
            self.assertNotIn(residu, t["why"])

    def test_diese_dans_le_titre_nest_pas_un_tag(self):
        # Régression : un « #mot » DANS le titre (pas en fin de ligne) ne doit pas être
        # capturé comme tag — sinon le titre est corrompu. Cas vécu : « (#tag) ».
        t = one("[P3][done] Tags libres sur les tickets (#tag) — 2e axe ~3h")
        self.assertEqual(t["tags"], [])
        self.assertEqual(t["title"], "Tags libres sur les tickets (#tag)")
        self.assertEqual(t["why"], "2e axe")
        self.assertEqual(t["est"], "3")

    def test_tag_deterministe(self):
        # Couleur stable entre deux appels (zéro config, pas de hash randomisé).
        self.assertEqual(build.tag_hue("back"), build.tag_hue("back"))
        self.assertTrue(0 <= build.tag_hue("infra") < 360)


class ContexteEtEpics(unittest.TestCase):
    def test_lignes_de_contexte_rattachees(self):
        txt = ("[P2][todo] T — w\n"
               "  > Contexte ligne 1\n"
               "  > Contexte ligne 2")
        t = one(txt)
        self.assertEqual(len(t["context"]), 2)
        self.assertEqual(t["context"][0]["text"], "Contexte ligne 1")
        self.assertFalse(t["context"][0]["devnote"])

    def test_devnote_detectee(self):
        txt = ("[P1][blocked] T — w\n"
               "  > @dev-note: il manque une spec")
        t = one(txt)
        self.assertTrue(t["context"][0]["devnote"])
        self.assertEqual(t["context"][0]["text"], "@dev-note: il manque une spec")

    def test_ligne_vide_coupe_le_rattachement(self):
        txt = ("[P2][todo] T — w\n"
               "\n"
               "  > orpheline")
        t = one(txt)
        self.assertEqual(t["context"], [])

    def test_declaration_epic(self):
        epics, tickets = build.parse("[epic] core — Socle du framework")
        self.assertIn("core", epics)
        self.assertEqual(epics["core"]["title"], "Socle du framework")
        self.assertEqual(tickets, [])

    def test_epic_regroupe_les_tickets(self):
        txt = ("[epic] auth — Authentification\n"
               "[P1][todo] Inscription — pas de compte @epic:auth")
        epics, tickets = build.parse(txt)
        self.assertIn("auth", epics)
        self.assertEqual(tickets[0]["epic"], "auth")


class RobustesseParser(unittest.TestCase):
    def test_lignes_non_ticket_ignorees(self):
        txt = ("# Un titre markdown\n"
               "> une citation\n"
               "[P1][todo] Vrai ticket — w\n"
               "du texte libre")
        _, tickets = build.parse(txt)
        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0]["title"], "Vrai ticket")

    def test_plusieurs_tickets_ordre_preserve(self):
        txt = ("[P1][todo] Un — a\n"
               "[P2][done] Deux — b ~1h =2h")
        _, tickets = build.parse(txt)
        self.assertEqual([t["title"] for t in tickets], ["Un", "Deux"])

    def test_backlog_vide(self):
        epics, tickets = build.parse("")
        self.assertEqual((epics, tickets), ({}, []))


if __name__ == "__main__":
    unittest.main(verbosity=2)
