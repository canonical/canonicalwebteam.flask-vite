# Canonical Webteam Flask-Vite integration

A Flask extension that integrates with Vite, enabling use of Vite's dev server and static builds with as little configuration as possible.

## Features
- easy to configure
- simple API
- supports custom Vite configurations
- supports multiple JS entry points
- supports all Vite-compatible JS frameworks
- supports all Vite-compatible stylesheet languages
- hot reloading in development mode
- `modulepreload` hints for JS chunks in production mode
- injects `nonce` attributes into `script` and `link` tags automatically (if `flask.request.CSP_NONCE` is set)


## How to use the extension

### Install
To install this extension as a requirement in your project, you can use PIP:
```bash
pip install canonicalwebteam.flask-vite
```

### Update your Vite configuration
Set `build.manifest` to `true` in your Vite config.

### Configure
The extension reads the following values from the Flask `app.config` object:
  - `VITE_MODE: "development" | "production"` - type of environment in which the Vite integration will run. Defaults to `"production"`.
  - `VITE_PORT: int` - port where Vite's dev server is running. Defaults to `5173`.
  - `VITE_OUTDIR: str` - file system path where the Vite output is expected; the path can be absolute or relative to the Flask app's root directory. Defaults to `"static/dist"`.
  - `VITE_REACT: bool` - only needed for React projects; set to `True` to inject React HMR dev tools in dev mode. Defaults to `False`.

> Note: the extension does NOT manage the state of the Vite dev server nor produce the static builds, you are responsible for running the appropriate Vite commands *before* initializing the extension.

### Initialize
```python
from canonicalwebteam.flask_vite import FlaskVite
vite = FlaskVite()
vite.init_app(app)
```

### Import resources
The extension adds a new template global function named `vite_import`. To include a script or stylesheet, simply invoke this template function passing the path to the file you want to import, relative to the app's root directory.

#### Example
To import a script whose path is `< flask app directory >/js/app/main.ts`:
```html
{ vite_import("js/app/main.ts") }
```

> Note: when importing a file via `vite_import`, make sure it's also declared as an entry point in your Vite config (under `build.rollupOptions.input`); if this isn't the case, **the import will break in production mode**. This is because Vite's build won't contain the file you're trying to import, so `vite_import` will throw a `ManifestContentException` when attempting to resolve the filesystem path.


## Minimal usage example
```python
# app.py

# ...
app.config["VITE_MODE"] = "development" if app.debug else "production"

FlaskVite(app)

#...
```

```html
<!-- templates/index.html -->
<head>
  { vite_import("path/to/source/styles.scss") }
</head>
<body>
  { vite_import("path/to/source/file.tsx") }
</body>
```

For a more fleshed-out example check the `example` directory.

## Development
The package leverages [poetry](https://poetry.eustace.io/) for dependency management.

To set up the virtual env and install dependencies, run:
```bash
poetry install
```


## Testing
Unit tests can be run using:
```bash
poetry run python3 -m unittest discover tests
```
