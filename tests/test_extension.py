from unittest import TestCase
import flask

from canonicalwebteam.flask_vite import (
    FlaskVite,
)
from tests.mocks import (
    MOCK_CONFIG,
)


class TestsExtension(TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)

        @self.app.route("/")
        def index():
            return """
            <!doctype html>
            <html>
                <head></head>
                <body></body>
            </html>
            """

        self.client = self.app.test_client()

        self.app.config["VITE_MODE"] = "development"
        self.app.config["VITE_PORT"] = MOCK_CONFIG["port"]
        self.app.config["VITE_OUTDIR"] = MOCK_CONFIG["outdir"]
        FlaskVite().init_app(self.app)

    def test_extension_init(self):
        self.assertEqual(self.app.config.get("VITE_MODE"), "development")
        self.assertEqual(self.app.config.get("VITE_PORT"), MOCK_CONFIG["port"])
        self.assertEqual(
            self.app.config.get("VITE_OUTDIR"), MOCK_CONFIG["outdir"]
        )

    def test_dev_tools(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        body = response.get_data(as_text=True)
        self.assertGreater(len(body), 0)
        self.assertIn(
            f'http://localhost:{MOCK_CONFIG["port"]}/@vite/client', body)
