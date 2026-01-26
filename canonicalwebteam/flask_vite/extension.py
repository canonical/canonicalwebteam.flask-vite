import flask
from markupsafe import Markup
from os import path
from urllib.parse import urljoin
from typing import Union

from canonicalwebteam.flask_vite.utils import EXTENSION_NAME, staticproperty
from canonicalwebteam.flask_vite.types import Config
from canonicalwebteam.flask_vite.exceptions import ExtensionNotInitialized
from canonicalwebteam.flask_vite.impl import (
    DevViteIntegration,
    ProdViteIntegration,
)


class FlaskVite:
    """
    Flask extension that implements the Vite integration
    """

    app: flask.Flask
    config: Config

    def __init__(self, app: flask.Flask | None = None):
        if app:
            self.init_app(app)

    @staticproperty  # type: ignore[arg-type]
    def instance() -> Union[DevViteIntegration, ProdViteIntegration, None]:
        try:
            return flask.current_app.extensions[EXTENSION_NAME]
        except KeyError:
            raise ExtensionNotInitialized(
                f"{EXTENSION_NAME}: can't use extension before initializing it"
            )

    def init_app(self, app: flask.Flask):
        FlaskVite.app = app
        FlaskVite.config = {
            "mode": app.config.get("VITE_MODE", "production"),
            "port": int(app.config.get("VITE_PORT", 5173)),
            "outdir": app.config.get("VITE_OUTDIR", "static/dist"),
            "react": bool(app.config.get("VITE_REACT", False)),
        }
        is_dev = "development" == FlaskVite.config["mode"]
        ViteIntegration = DevViteIntegration if is_dev else ProdViteIntegration

        if not app.extensions.get(EXTENSION_NAME):
            app.extensions[EXTENSION_NAME] = ViteIntegration(FlaskVite.config)

        app.template_global("vite_import")(vite_import)

        if is_dev:
            # add an after request handler to inject dev tools scripts
            app.after_request(_inject_vite_dev_tools)


def _csp_nonce():
    # Check if nonce has been set
    nonce = getattr(flask.request, "CSP_NONCE", "")
    if nonce:
        return f'nonce="{nonce}"'
    return ""


def vite_import(entrypoint: str):
    """
    Template function that takes a source file as an argument and returns
    the <script> or <link rel="stylesheet"> tags with the correct src URL
    based on Vite's config (a localhost URL in dev mode, or a static path
    in prod mode).
    If the file extension doesn't fall in one of these cases, the function
    will log an error and return an HTML comment, so the import will
    effectively fail silently.
    """
    _, ext = path.splitext(entrypoint)

    match ext:
        case ".css" | ".scss" | ".sass" | ".less" | ".styl":
            return _stylesheet_import(entrypoint)
        case ".js" | ".ts" | ".jsx" | ".tsx" | ".svelte" | ".vue":
            return _script_import(entrypoint)
        case _:
            return _unknown_import(entrypoint)


def _stylesheet_import(entrypoint):
    entry_url = FlaskVite.instance.get_asset_url(entrypoint)
    return Markup(
        f'<link rel="stylesheet" href="{entry_url}" {_csp_nonce()} />'
    )


def _script_import(entrypoint):
    entry_url = FlaskVite.instance.get_asset_url(entrypoint)

    entry_script = [
        f'<script type="module" src="{entry_url}" {_csp_nonce()}></script>'
    ]

    # a script might import stylesheets, which are treated as a dependency
    css_urls = FlaskVite.instance.get_imported_css(entrypoint)
    css_scripts = [
        f'<link rel="stylesheet" href="{c}" {_csp_nonce()} />'
        for c in css_urls
    ]

    # build the dependency tree of the imported script, so dependencies from
    # other modules can be fetched early, using `modulepreload` hints
    chunks_urls = FlaskVite.instance.get_imported_chunks(entrypoint)
    chunks_scripts = [
        f'<link rel="modulepreload" href="{c}" {_csp_nonce()} />'
        for c in chunks_urls
    ]

    return Markup("".join(entry_script + chunks_scripts + css_scripts))


def _unknown_import(entrypoint):
    flask.current_app.logger.error(
        f'{EXTENSION_NAME}: can\'t import file "{entrypoint}" with'
        " unknown file extension"
    )
    return Markup(
        "<!--"
        f"{EXTENSION_NAME}: unknown file extension for file {entrypoint} "
        "-->"
    )


def _inject_vite_dev_tools(res: flask.Response):
    """
    Patch text/html responses by injecting the <script> tags for Vite's dev
    server tools before closing the <head> tag
    """

    if not res.mimetype:
        # no idea what the response type is, send it unchanged
        return res

    if "text/html" not in res.mimetype:
        # response is not an HTML page, no need for Vite scripts
        return res

    body = res.get_data(as_text=True)
    if not body:
        # response doesn't have a body, no need for Vite scripts
        return res

    # build the dev tools scripts string
    port = FlaskVite.config["port"]
    baseurl = f"http://localhost:{port}/"
    dev_tools = f"""
    <!-- {EXTENSION_NAME}: start Vite dev tools -->
    <script
        type="module"
        src="{urljoin(baseurl, "@vite/client")}"
        {_csp_nonce()}>
    </script>
    <!-- {EXTENSION_NAME}: end Vite dev tools -->
    """

    react = FlaskVite.config["react"]
    if react:
        dev_tools += f"""
        <!-- {EXTENSION_NAME}: start React dev tools -->
        <script type="module" {_csp_nonce()}>
            import RefreshRuntime from "{urljoin(baseurl, "@react-refresh")}";
            RefreshRuntime.injectIntoGlobalHook(window);
            window.$RefreshReg$ = () => {{}};
            window.$RefreshSig$ = () => (type) => type;
            window.__vite_plugin_react_preamble_installed__ = true;
        </script>
        <!-- {EXTENSION_NAME}: end React dev tools -->
        """

    # inject the dev tools' scripts at the end of the <head> tag
    body = body.replace("</head>", f"{dev_tools}\n</head>")
    res.set_data(body)
    return res
