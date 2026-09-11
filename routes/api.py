from typing import Any
from flask import Blueprint, Flask, jsonify, request
from classes import Postgres, Map


api_blueprint = Blueprint("api", __name__, url_prefix="/api")

@api_blueprint.get("/get_map")
def get_map() -> Any:
    """
    Endpunkt zum Erstellen der Folium Karte mit Parametern.
    """
    region = request.args.get("region", "all")
    geo_data = Postgres.fetch_geo_data(region)
    html_map = Map.build_html_map(geo_data, region)
    return jsonify({"map": html_map})

@api_blueprint.get("/fetch_regions")
def fetch_regions() -> Any:
    """
    Endpunkt zum Laden der eindeutigen Regionen.
    """
    return jsonify({"regions": Postgres.fetch_regions()})

@api_blueprint.get("/fetch_last_update_ts")
def fetch_last_update_ts() -> Any:
    """
    Endpunkt zum Laden der letzten Aktualisierung als Timestamp.
    """
    return jsonify(Postgres.fetch_last_update_ts())

@api_blueprint.get("/fetch_surface_area")
def fetch_surface_area() -> Any:
    """
    Endpunkt zum Laden der Fläche in Quadratkilometern gem. Parameter
    """
    region = request.args.get("region", "all")
    return jsonify(Postgres.fetch_surface_area(region))

@api_blueprint.get("/fetch_region_count")
def fetch_region_count() -> Any:
    """
    Endpunkt zum Laden der Anzahl Regionen.
    """
    return jsonify(Postgres.fetch_region_count())

def register_api_routes(app: Flask) -> None:
    app.register_blueprint(api_blueprint)