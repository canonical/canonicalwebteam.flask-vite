import flask
from flask_talisman import Talisman
from canonicalwebteam.flask_vite import FlaskVite

app = flask.Flask(__name__, template_folder="templates")

app.config["VITE_MODE"] = "development" if app.debug else "production"
app.config["VITE_PORT"] = 9999
app.config["VITE_OUTDIR"] = "static/vite/dist"

csp = {
    "default-src": ["'self'"],
    "script-src": ["'self'"],
}

if app.debug:
    csp["connect-src"] = ["'self'", "ws://localhost:9999"]

talisman = Talisman(
    app,
    content_security_policy=csp,
    content_security_policy_nonce_in=["script-src", "default-src"],
    force_https=False,
)

FlaskVite(app)


@app.route("/")
def index():
    return flask.render_template("index.html")
