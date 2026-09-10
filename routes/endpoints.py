from typing import Any
from flask import Blueprint, Flask, render_template

pages_blueprint = Blueprint("pages", __name__)

@pages_blueprint.get("/")
def index() -> Any:
    return render_template("index.html")

def register_page_routes(app: Flask) -> None:
    app.register_blueprint(pages_blueprint)