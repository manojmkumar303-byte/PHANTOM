import base64
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class PasswordGeneratorTests(unittest.TestCase):
    def test_default_length_and_all_classes(self):
        value = main.generate_password(24)
        self.assertEqual(len(value), 24)
        self.assertTrue(any(c.isupper() for c in value))
        self.assertTrue(any(c.islower() for c in value))
        self.assertTrue(any(c.isdigit() for c in value))
        self.assertTrue(any(c in "!#$%&()*+,-./:;<=>?@[]^_{|}~" for c in value))

    def test_configurable_sets(self):
        value = main.generate_password(16, uppercase=False, lowercase=False, digits=True, symbols=False)
        self.assertTrue(value.isdigit())

    def test_ambiguous_characters_excluded(self):
        value = main.generate_password(64, exclude_ambiguous=True)
        for char in main.AMBIGUOUS:
            self.assertNotIn(char, value)

    def test_invalid_length_and_empty_sets(self):
        with self.assertRaises(ValueError):
            main.generate_password(7)
        with self.assertRaises(ValueError):
            main.generate_password(24, uppercase=False, lowercase=False, digits=False, symbols=False)

    def test_each_enabled_class_present(self):
        value = main.generate_password(8, uppercase=True, lowercase=True, digits=True, symbols=True)
        self.assertTrue(any(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in value))
        self.assertTrue(any(c in "abcdefghijklmnopqrstuvwxyz" for c in value))
        self.assertTrue(any(c in "0123456789" for c in value))
        self.assertTrue(any(c in "!#$%&()*+,-./:;<=>?@[]^_{|}~" for c in value))


class VaultTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.app_dir = self.directory / "app"
        self.vault_path = self.app_dir / "vault.pkv"
        self.patcher_dir = patch.object(main, "APP_DIR", self.app_dir)
        self.patcher_path = patch.object(main, "VAULT_PATH", self.vault_path)
        self.patcher_dir.start()
        self.patcher_path.start()
        self.addCleanup(self.patcher_dir.stop)
        self.addCleanup(self.patcher_path.stop)
        self.addCleanup(self.temp.cleanup)

    def test_create_unlock_save_round_trip(self):
        key, notes, token = main.create_vault("a sufficiently long test password")
        self.assertEqual(notes, [])
        note = {"id": "testid", "title": "Example", "content": "secret note", "category": "Study", "updated": "now"}
        token = main.save_vault(key, [note], token)
        envelope = main.read_envelope()
        self.assertNotIn(b"secret note", self.vault_path.read_bytes())
        unlocked_key, loaded, _ = main.unlock_vault("a sufficiently long test password", envelope)
        self.assertEqual(unlocked_key, key)
        self.assertEqual(loaded, [note])

    def test_wrong_password_rejected(self):
        main.create_vault("a sufficiently long test password")
        with self.assertRaises(PermissionError):
            main.unlock_vault("wrong password", main.read_envelope())

    def test_external_change_prevents_overwrite(self):
        key, _, token = main.create_vault("a sufficiently long test password")
        envelope = main.read_envelope()
        envelope["token"] = "externally changed"
        self.vault_path.write_text(json.dumps(envelope), encoding="utf-8")
        with self.assertRaises(RuntimeError):
            main.save_vault(key, [], token)

    def test_malformed_envelope_rejected(self):
        self.app_dir.mkdir(parents=True, exist_ok=True)
        self.vault_path.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8")
        with self.assertRaises(ValueError):
            main.read_envelope()


if __name__ == "__main__":
    unittest.main()
