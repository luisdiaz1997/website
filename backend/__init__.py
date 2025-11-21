from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS


BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "frontend" / "dist"

app = Flask(
    __name__,
    static_folder=str(DIST_DIR),
    static_url_path="/",
)
CORS(app)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue_app(path: str):
    """
    Serve built Vue assets, falling back to index.html for client-side routing.
    """
    if path and (DIST_DIR / path).is_file():
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")
