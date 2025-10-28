import flask
from canonicalwebteam.flask_vite import FlaskVite

app = flask.Flask(__name__, template_folder="templates")

app.config["VITE_MODE"] = "development" if app.debug else "production"
app.config["VITE_PORT"] = 9999
app.config["VITE_OUTDIR"] = "static/vite/dist"

FlaskVite(app)


@app.route("/")
def index():
    return flask.render_template("index.html")
