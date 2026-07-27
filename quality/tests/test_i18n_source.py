from __future__ import annotations

import json
import unittest
from pathlib import Path

from gmc_bridge.i18n import CATALOGS, SUPPORTED_UI_LANGUAGES, validate_catalogs
from gmc_bridge.i18n.catalog import CATALOG_SOURCE_PATH, load_catalogs


class TranslationSourceTests(unittest.TestCase):
    def test_single_json_source_matches_runtime_catalogs(self) -> None:
        self.assertTrue(CATALOG_SOURCE_PATH.is_file())
        raw = json.loads(CATALOG_SOURCE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(tuple(raw), tuple(sorted(raw)))
        self.assertEqual(set(raw), set(SUPPORTED_UI_LANGUAGES))
        self.assertEqual(load_catalogs(), CATALOGS)
        self.assertEqual(validate_catalogs(), [])

    def test_generated_language_modules_are_not_runtime_sources(self) -> None:
        directory = CATALOG_SOURCE_PATH.parent
        obsolete = [directory / f"{language}.py" for language in SUPPORTED_UI_LANGUAGES]
        self.assertFalse([path for path in obsolete if path.exists()])
        self.assertFalse(list(directory.glob("release_*.json")))


if __name__ == "__main__":
    unittest.main()
