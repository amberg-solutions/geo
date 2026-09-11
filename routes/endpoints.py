from typing import Any
from flask import Blueprint, Flask, Response, render_template
from config import BASE_DIR
import os

pages_blueprint = Blueprint("pages", __name__)

@pages_blueprint.get("/")
def index() -> Any:
    return render_template("index.html")

@pages_blueprint.get("/api.py")
def api_file() -> Any:
    file_path = os.path.join(BASE_DIR, "routes", "api.py")
    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()
        return render_template("api.html", content=content)

@pages_blueprint.get("/robots.txt")
def robots() -> Response:
    return Response("User-agent: *\nDisallow: /\n", mimetype="text/plain")

def register_page_routes(app: Flask) -> None:
    app.register_blueprint(pages_blueprint)