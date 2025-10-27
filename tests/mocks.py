MOCK_CONFIG = {
    "mode": "development",
    "port": 9999,
    "outdir": "/tmp/python_vite_test",
}

MOCK_ASSET_PATH = "test/path/for/asset.ts"

MOCK_SCSS_PATH = "test/path/for/styles.scss"

MOCK_MANIFEST = {
    "_dependency.js": {"file": "chunks/dependency.js", "name": "dependency"},
    "_chunk.js": {
        "file": "chunks/chunk.js",
        "name": "chunk",
        "imports": ["_dependency.js"],
        "css": ["assets/styles.css"],
    },
    "test/path/for/asset.ts": {
        "file": "asset.js",
        "name": "asset",
        "src": "test/path/for/asset.ts",
        "isEntry": True,
        "imports": [
            "_chunk.js",
        ],
    },
    "test/path/for/styles.scss": {
        "file": "assets/styles.css",
        "src": "test/path/for/styles.scss",
        "isEntry": True,
        "names": ["styles.css"],
    },
}
