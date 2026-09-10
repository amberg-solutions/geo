from flask import Flask

from routes.api import register_api_routes
from routes.endpoints import register_page_routes


def create_app() -> Flask:
    app = Flask(__name__)
    register_page_routes(app)
    register_api_routes(app)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=8000)