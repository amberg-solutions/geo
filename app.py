from threading import Lock, Thread
from time import sleep
from flask import Flask
from classes import ETL, Postgres
from routes.api import register_api_routes
from routes.endpoints import register_page_routes

                                                                                                                
refresh_started = False                                                                                                                                        
refresh_lock = Lock()


def refresh_data() -> None:
    while True:
        try:
            ETL.run_pipeline()
        finally:
            Postgres.close()
        sleep(60 * 30) # Alle 30 Minuten aktualisieren


def start_refresh_job() -> None:
    global refresh_started

    with refresh_lock:
        if refresh_started:
            return

        Thread(target=refresh_data, daemon=True, name="geo-data-refresh").start()
        refresh_started = True


def create_app() -> Flask:
    app = Flask(__name__)
    register_page_routes(app)
    register_api_routes(app)

    @app.before_request
    def ensure_refresh_job_started() -> None:
        start_refresh_job()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=8000)