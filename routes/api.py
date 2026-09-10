from typing import Any
from flask import Blueprint, Flask, jsonify, request
from classes import Postgres, Map


api_blueprint = Blueprint("api", __name__, url_prefix="/api")

@api_blueprint.get("/get_map")
def get_map() -> Any:
    region = request.args.get("region", "all")
    geo_data = Postgres.fetch_geo_data(region)
    html_map = Map.build_html_map(geo_data, region)
    return jsonify({"map": html_map})

@api_blueprint.get("/fetch_regions")
def fetch_regions() -> Any:
    return jsonify({"regions": Postgres.fetch_regions()})

@api_blueprint.get("/fetch_last_update_ts")
def fetch_last_update_ts() -> Any:
    return jsonify(Postgres.fetch_last_update_ts())

@api_blueprint.get("/fetch_surface_area")
def fetch_surface_area() -> Any:
    region = request.args.get("region", "all")
    return jsonify(Postgres.fetch_surface_area(region))


def register_api_routes(app: Flask) -> None:
    app.register_blueprint(api_blueprint)