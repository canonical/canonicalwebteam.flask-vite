# Canonical Webteam Flask-Vite integration

A Flask extension that integrates with Vite, enabling use of Vite's dev server and static builds with as little configuration as possible.

To install this extension as a requirement in your project, you can use PIP:
```bash
pip install canonicalwebteam.flask-vite
```

## Features
- easy to configure configuration
- simple API
- supports custom Vite configurations
- supports multiple JS entry points
- supports all Vite-compatible JS frameworks
- supports all Vite-compatible stylesheet languages
- hot reloading in development mode
- `modulepreload` hints for JS chunks in production mode

## Configuration
The extension parses the following values from the Flask `app.config` object:
  - `VITE_MODE: "development" | "production"` - type of environment in which the Vite integration will run
  - `VITE_PORT: int` - port where Vite's dev server is running
  - `VITE_OUTDIR: str` - file system path where the Vite output is expected; the path can be absolute or relative to the Flask app's root directory


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

Run `poetry install` to set up the virtual env and install dependencies.

## Testing

Tests can be run with `poetry run python3 -m unittest discover tests`.
