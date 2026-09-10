import psycopg2
from config import PG_DB, PG_HOST, PG_PASS, PG_USER, BASE_DIR
import os

class Postgres:

    DATABASE_SCHEMA_SQL = os.path.join(BASE_DIR, "sql", "database.sql")

    @classmethod
    def connect(cls) -> None:
        cls.cnx = psycopg2.connect(
            dbname = PG_DB,
            user = PG_USER,
            password = PG_PASS,
            host = PG_HOST
        )

    @classmethod
    def ensure_connection(cls) -> None:
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
        cls.ensure_connection()

        sql = cls.read_sql_schema()

        with cls.cnx.cursor() as cursor:
            cursor.execute(sql)

    @classmethod
    def insert_geo_data(cls, record: dict) -> None:
        """
        Fügt die Daten aus dem Datenportal GR in die Postgres Datenbank ein.

        :params: `record`: Die transformierten Datensätze.
        """
        cls.ensure_connection()

        with cls.cnx.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.geodaten 
                (name, geom, zentrum)
                VALUES (
                    %s, 
                    ST_SetSRID(ST_GeomFromGeoJSON('{"type":{"Polygon","coordinates": %s}}')),
                    ST_SETSRID(ST_MakePoint(%s), 4326)
                )
                """, (record["name"], record["geom"], record["point"])
            )
            cls.cnx.commit()