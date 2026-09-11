import json
import psycopg2
from config import PG_DB, PG_HOST, PG_PASS, PG_USER, BASE_DIR
from datetime import datetime
import os

class Postgres:

    DATABASE_SCHEMA_SQL = os.path.join(BASE_DIR, "sql", "database.sql")

    @classmethod
    def connect(cls) -> None:
        """
        Verbindung zur lokalen Postgres Datenbank.
        """
        cls.cnx = psycopg2.connect(
            dbname = PG_DB,
            user = PG_USER,
            password = PG_PASS,
            host = PG_HOST
        )

    @classmethod
    def close(cls) -> None:
        try: cls.cnx.close()
        except: pass

    @classmethod
    def ensure_connection(cls) -> None:
        """
        Sicherstellen dass die Verbindungen aufrecht erhalten bleiben.
        """
        try: 
            with cls.cnx.cursor() as cursor:
                cursor.execute("SELECT 1;")
        except:
            cls.connect()

    @classmethod
    def read_sql_schema(cls) -> str:
        with open(Postgres.DATABASE_SCHEMA_SQL, "r", encoding='utf-8') as f:
            return f.read()
        return ""

    @classmethod
    def build_db_schema(cls) -> None:
        """
        Funktion um das Schema gem. sql/database.sql zu bauen.
        """
        cls.ensure_connection()

        sql = cls.read_sql_schema()

        with cls.cnx.cursor() as cursor:
            cursor.execute(sql)
            cls.cnx.commit()

    @classmethod
    def insert_geo_data(cls, record: dict) -> None:
        """
        Fügt die Daten aus dem Datenportal GR in die Postgres Datenbank ein.

        :params: `record`: Die transformierten Datensätze.
        """
        cls.ensure_connection()

        geometry = json.dumps({
            "type": "Polygon",
            "coordinates": record["geom"]
        })
        longitude, latitude = record["point"]
        name = record["name"]

        with cls.cnx.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.geodaten 
                (name, geom, zentrum)
                VALUES (
                    %s, 
                    ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326),
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326)
                )
                """, (name, geometry, longitude, latitude)
            )
            cls.cnx.commit()

    @classmethod
    def truncate_geo_table(cls) -> None:
        """
        Leert die Tabelle und setzt sie zurück.
        """
        cls.ensure_connection()

        with cls.cnx.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE public.geodaten RESTART IDENTITY CASCADE")
            cls.cnx.commit()

    @classmethod
    def fetch_regions(cls) -> list:
        cls.ensure_connection()

        with cls.cnx.cursor() as cursor:
            cursor.execute(
                """
                SELECT DISTINCT(name) 
                FROM public.geodaten
                ORDER BY name;
                """
            )
            rows = cursor.fetchall()
            if rows:
                return [row[0] for row in rows]
            return []

    @classmethod
    def fetch_geo_data(cls, region: str = "all") -> list[dict]:
        cls.ensure_connection()

        with cls.cnx.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    name,
                    ST_AsGeoJSON(
                        ST_SimplifyPreserveTopology(geom, 0.001)
                    )::json AS geom,
                    ARRAY[ST_X(zentrum), ST_Y(zentrum)] AS point
                FROM public.geodaten
                WHERE %s = 'all' OR name = %s
                ORDER BY name
                """, (region, region)
            )
            rows = cursor.fetchall()

        return [
            {
                "name": row[0],
                "geom": row[1],
                "point": row[2]
            }
            for row in rows
        ]

    @classmethod
    def fetch_last_update_ts(cls) -> dict:
        cls.ensure_connection()

        with cls.cnx.cursor() as cursor:
            cursor.execute(
                """
                SELECT MAX(created_at)
                FROM public.geodaten 
                """
            )
            row = cursor.fetchone()
            if row:
                return {"ts" : f"{row[0].strftime("%d.%m.%Y - %H:%M")}"}

        return {}

    @classmethod
    def fetch_surface_area(cls, region: str = "all") -> dict:
        cls.ensure_connection()

        with cls.cnx.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    SUM(ST_Area(geom::geography)) / 1000000
                FROM public.geodaten
                WHERE %s = 'all' OR name = %s
                """, (region, region)
            )
            row = cursor.fetchone()
            if row and row[0] is not None:
                return {
                    "area": f"{round(float(row[0]), 2)} km²"
                }
        return {"area": "-"}

    @classmethod
    def fetch_region_count(cls) -> dict:
        cls.ensure_connection()

        with cls.cnx.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(DISTINCT(name))
                FROM public.geodaten
                """
            )
            row = cursor.fetchone()
            if row:
                return {
                    "count" : row[0]
                }
        return {}