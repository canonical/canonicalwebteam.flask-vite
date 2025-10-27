from unittest import TestCase
import json
from shutil import rmtree
from typing import cast
from urllib.parse import urlparse
from pathlib import Path

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
        assert MOCK_ASSET_PATH in url
        parsed = urlparse(url)
        assert parsed.scheme == "http"
        assert parsed.netloc.startswith("localhost:")
        assert parsed.path == f"/{MOCK_ASSET_PATH}"
        assert parsed.params == ""
        assert parsed.query == ""
        assert parsed.fragment == ""

    def tests_get_imported_chunks(self):
        assert len(self.vite.get_imported_chunks(MOCK_ASSET_PATH)) == 0

    def tests_get_imported_css(self):
        assert len(self.vite.get_imported_css(MOCK_ASSET_PATH)) == 0
