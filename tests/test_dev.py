from unittest import TestCase
from urllib.parse import urlparse

from canonicalwebteam.flask_vite.impl import (
    DevViteIntegration,
)
from tests.mocks import (
    MOCK_CONFIG,
    MOCK_ASSET_PATH,
)


class TestsDevViteIntegration(TestCase):
    def setUp(self):
        self.vite = DevViteIntegration(MOCK_CONFIG)

    def tests_get_asset_url(self):
        url = self.vite.get_asset_url(MOCK_ASSET_PATH)
        self.assertIn(MOCK_ASSET_PATH, url)

        parsed = urlparse(url)
        self.assertEqual(parsed.scheme, "http")
        self.assertTrue(parsed.netloc.startswith("localhost:"))
        self.assertEqual(parsed.path, f"/{MOCK_ASSET_PATH}")
        self.assertEqual(parsed.params, "")
        self.assertEqual(parsed.query, "")
        self.assertEqual(parsed.fragment, "")

    def tests_get_imported_chunks(self):
        self.assertEqual(
            len(self.vite.get_imported_chunks(MOCK_ASSET_PATH)), 0
        )

    def tests_get_imported_css(self):
        self.assertEqual(len(self.vite.get_imported_css(MOCK_ASSET_PATH)), 0)
