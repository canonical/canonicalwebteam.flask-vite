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


## How to use the extension

### Install
To install this extension as a requirement in your project, you can use PIP:
```bash
pip install canonicalwebteam.flask-vite
```

### Configure
The extension parses the following values from the Flask `app.config` object:
  - `VITE_MODE: "development" | "production"` - type of environment in which the Vite integration will run
  - `VITE_PORT: int` - port where Vite's dev server is running
  - `VITE_OUTDIR: str` - file system path where the Vite output is expected; the path can be absolute or relative to the Flask app's root directory

### Import
The extension adds a new template global function named `vite_import`.

> Note: all files imported via `vite_import` must be declared as entry points in your Vite config; if this isn't the case, the extension will NOT work in production mode.


## Minimal usage example

```python
# app.py
app = Flask()

app.config["VITE_MODE"] = "development" if app.debug else "production"
app.config["VITE_PORT"] = 9999
app.config["VITE_OUTDIR"] = "static/dist"

vite = FlaskVite()
vite.init_app(app)
```

```html
<!-- templates/base.html -->
<head>
  { vite_import("path/to/source/styles.scss") }
  { vite_import("path/to/source/file.tsx") }
</head>
```

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
