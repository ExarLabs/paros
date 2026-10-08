#!/usr/bin/env python3
"""Tests for the P07 secret scan in diagnose.py. Every value here is made up.

    python tools/test_diagnose.py
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import diagnose  # noqa: E402


def hits(text, suffix=".md"):
    return diagnose.credential_hits(text, suffix)


def scan_note(text):
    with tempfile.TemporaryDirectory() as d:
        Path(d, "note.md").write_text(text, encoding="utf-8")
        r = diagnose.scan(d)
        return r, diagnose.levels(r)["P07"]


class CredentialLabels(unittest.TestCase):
    def test_english(self):
        self.assertEqual(hits("Wi-Fi password: Spring2031!\n"), ["Credential label (English)"])
        self.assertEqual(hits('DB_PASSWORD="Kx7-made-up"\n', ".env"), ["Credential label (English)"])
        self.assertEqual(hits('{"api_key": "made-up-value-123"}\n', ".json"), ["Credential label (English)"])
        self.assertEqual(hits("Meeting passcode: 482913\n"), ["Credential label (English)"])

    def test_hungarian_with_accents(self):
        self.assertEqual(hits("Belépés e-maillel: anna@example.com, jelszó: Tavasz2031\n"),
                         ["Credential label (Hungarian)"])
        self.assertEqual(hits("- **Jelszava:** Kitalalt99\n"), ["Credential label (Hungarian)"])
        self.assertEqual(hits("titkos kulcs = abcd1234efgh\n"), ["Credential label (Hungarian)"])

    def test_hungarian_without_accents(self):
        self.assertEqual(hits("felhasznalonev: anna\njelszo: Tavasz2031\n"), ["Credential label (Hungarian)"])
        self.assertEqual(hits("JELSZO=Tavasz2031\n", ".env"), ["Credential label (Hungarian)"])

    def test_other_languages(self):
        self.assertEqual(hits("Passwort: Fruehling2031\n"), ["Credential label (German)"])
        self.assertEqual(hits("mot de passe : Printemps2031\n"), ["Credential label (French)"])
        self.assertEqual(hits("parolă: Primavara2031\n"), ["Credential label (Romanian)"])
        self.assertEqual(hits("contraseña: Primavera2031\n"), ["Credential label (Spanish)"])


class LoginBlock(unittest.TestCase):
    LABEL = ["Login block: password-shaped value next to an email, URL or login label"]

    def test_label_in_unknown_language_next_to_email(self):
        # a label the scanner has no word for; the shape gives it away
        self.assertEqual(hits("Konto: anna@example.com\nKodo: Xq7!made-up\n"), self.LABEL)

    def test_label_in_unknown_language_next_to_url(self):
        self.assertEqual(hits("https://portal.example.com\n\nsalasana: Kevat2031\n"), self.LABEL)

    def test_same_line(self):
        self.assertEqual(hits("anna@example.com | kodo: Kevat2031\n"), self.LABEL)

    def test_only_in_notes(self):
        self.assertEqual(hits("url = 'https://example.com'\nmodel = Model2031X\n", ".py"), [])


class Negatives(unittest.TestCase):
    def test_prose_and_placeholders(self):
        text = "\n".join([
            "Password: never stored in this vault, see the manager.",
            "jelszó: a jelszókezelőben van",
            "password: <from the keychain>",
            "password: ********",
            "api_key = os.environ['MADE_UP']",
            "password: str",
            "api_key: GROQ_API_KEY",
            "access_token: string",
            "'x-api-key': apiKey,",
            "jelszavakkal: soha",
            "db_password = settings.db.password",
            "A jelszavakat a jelszókezelő tárolja.",
        ])
        self.assertEqual(hits(text), [])
        self.assertEqual(hits(text, ".py"), [])

    def test_ordinary_notes_with_emails_and_links(self):
        text = "\n".join([
            "---", "id: 9d2f4e1a-7c3b-4a68-b0e5-1f6a8c2d9e47", "date: 2031-04-01", "version: 1.2.3", "---",
            "Owner: Anna Example", "Email: anna@example.com", "Ticket: OPS-1234", "Model: claude-opus-9",
            "Commit: 818620e", "Report: summary2031.pdf", "Docs: https://example.com/guide", "Phone: +40 700 000 000",
            "created_at: 2031-04-01T10:00:00Z", "video_id: Ab3dEf9hIj", "Spotify show ID: 4rOoJ6Egrf8K2IrywzwOMk",
            "Ma este 19: Kitalalt2031 utan", "Contact: 0A1B2-C3D-4E5-F6G7", "x: Ab.c9",
            "Kezdes: 10:30-ig", "CUI: RO12345678", "Csatolva: Szamla_2031.04.01", "Kapu: Demo-Smart-Gateway2",
        ])
        self.assertEqual(hits(text), [])

    def test_clean_vault_says_what_was_checked(self):
        r, (level, evidence) = scan_note("# Notes\nNothing sensitive here, see https://example.com\n")
        self.assertEqual(r["secret_hits"], [])
        self.assertEqual(level, 1)
        self.assertIn("not proof", evidence)
        self.assertIn("Hungarian", evidence)
        self.assertNotIn("no secret-like patterns found", evidence)


class Report(unittest.TestCase):
    def test_hit_reaches_p07(self):
        r, (level, evidence) = scan_note("Belépés: anna@example.com\njelszó: Tavasz2031\n")
        self.assertEqual([h["type"] for h in r["secret_hits"]], ["Credential label (Hungarian)"])
        self.assertEqual(level, 0)
        self.assertIn("1 secret-like patterns", evidence)


if __name__ == "__main__":
    unittest.main(verbosity=2)
