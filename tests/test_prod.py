from unittest import TestCase
import json
from shutil import rmtree
from typing import cast
from pathlib import Path

import canonicalwebteam.flask_vite.exceptions as vite_exceptions
from canonicalwebteam.flask_vite.impl import (
    ProdViteIntegration,
)
from tests.mocks import (
    MOCK_CONFIG,
    MOCK_MANIFEST,
    MOCK_ASSET_PATH,
    MOCK_SCSS_PATH,
)


class TestsProdViteIntegration(TestCase):
    def setUp(self):
        # create a fake Vite output directory
        manifest_path = Path(f'{MOCK_CONFIG["outdir"]}/.vite/manifest.json')
        manifest_path.parent.mkdir(exist_ok=True, parents=True)
        with manifest_path.open("w+") as file:
            file.write(json.dumps(MOCK_MANIFEST))

        for entry in MOCK_MANIFEST.values():
            file = cast(dict, entry).get("file", "")
            file_path = Path(f'{MOCK_CONFIG["outdir"]}/{file}')
            file_path.parent.mkdir(exist_ok=True, parents=True)
            with file_path.open("w+") as file:
                file.write("")

    def tearDown(self):
        rmtree(MOCK_CONFIG["outdir"])

    def tests_good_manifest_file(self):
        # attempt to init
        ProdViteIntegration(MOCK_CONFIG)

    def tests_bad_manifest_file(self):
        # try to init a ProdViteIntegration instance with a bad manifest file

        ProdViteIntegration.manifest = None  # reset the manifest instance
        old_manifest_name = ProdViteIntegration.BUILD_MANIFEST

        ProdViteIntegration.BUILD_MANIFEST = "file/that/does/not/exist"

        with self.assertRaises(vite_exceptions.ManifestPathException):
            self.vite = ProdViteIntegration(MOCK_CONFIG)

        # reset build manifest path to previous value
        ProdViteIntegration.BUILD_MANIFEST = old_manifest_name

    def tests_get_asset_url__bad_asset(self):
        vite = ProdViteIntegration(MOCK_CONFIG)
        with self.assertRaises(vite_exceptions.ManifestContentException):
            vite.get_asset_url("this_asset_does_not_exist.ts")

    def tests_get_asset_url__bad_path(self):
        # try to load an asset declared in the manifest but without a real
        # file backing it

        # load a proper manifest...
        ProdViteIntegration.manifest = MOCK_MANIFEST
        # but also load a broken OUT_DIR path
        vite = ProdViteIntegration({"outdir": "/tmp/path/does/not/exist"})
        with self.assertRaises(vite_exceptions.AssetPathException):
            vite.get_asset_url(MOCK_ASSET_PATH)

        # cleanup
        ProdViteIntegration.manifest = None

    def tests_get_asset_url__is_not_ts(self):
        vite = ProdViteIntegration(MOCK_CONFIG)
        url = vite.get_asset_url(MOCK_ASSET_PATH)
        assert MOCK_ASSET_PATH not in url  # source asset is a .ts file
        assert url.endswith(".js")  # dist asset is a .js file

    def tests_get_asset_url__is_not_scss(self):
        vite = ProdViteIntegration(MOCK_CONFIG)
        url = vite.get_asset_url(MOCK_SCSS_PATH)
        assert MOCK_SCSS_PATH not in url  # source asset is a .scss file
        assert url.endswith(".css")  # dist asset is a .css file

    def tests_get_imported_chunks__bad_asset(self):
        vite = ProdViteIntegration(MOCK_CONFIG)
        with self.assertRaises(vite_exceptions.ManifestContentException):
            vite.get_imported_chunks("this_asset_does_not_exist.ts")

    def tests_get_imported_chunks__bad_path(self):
        # try to load chunks for an asset declared in the manifest but
        # without a real file backing it
        # load a proper manifest...
        ProdViteIntegration.manifest = MOCK_MANIFEST
        # but also load a broken OUT_DIR path
        vite = ProdViteIntegration({"outdir": "/tmp/path/does/not/exist"})
        with self.assertRaises(vite_exceptions.AssetPathException):
            vite.get_imported_chunks(MOCK_ASSET_PATH)

        # cleanup
        ProdViteIntegration.manifest = None

    def tests_get_imported_chunks(self):
        vite = ProdViteIntegration(MOCK_CONFIG)
        js_entries = filter(
            lambda x: x["file"].endswith(".js"), MOCK_MANIFEST.values()
        )
        assert len(vite.get_imported_chunks(MOCK_ASSET_PATH)) == (
            len(list(js_entries)) - 1
        )

    def tests_get_imported_css(self):
        vite = ProdViteIntegration(MOCK_CONFIG)
        assert len(vite.get_imported_css(MOCK_ASSET_PATH)) == 1
