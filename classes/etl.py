"""
Dieses Klassenmodul steuert die ETL-Pipeline und sorgt für die übergeordnete Logik des ETL-Prozess (Extrahieren, Transformieren, Laden)
"""

class ETL:

    @staticmethod
    def run_pipeline() -> None:
        """
        Diese übergeordnete Funktion steuert den Ablauf des ETL-Prozesses.
        """
        data = ETL.Extract.data()
        transformed = ETL.Transform.data(data)
        ETL.Load.data(transformed)

    class Extract:
        @staticmethod
        def data() -> list:
            """
            Übergeordnete Funktion zum Extrahieren der Daten aus dem Datenportal des Kantons.
            """
            from classes import Data
            from classes import read_json

            Data.download_geo_data()
            data = read_json("geo.json")
            if data:
                return data["results"]
            return []

    class Transform:
        @staticmethod
        def data(data: list) -> list:
            """
            Transformiert die Daten und gibt diese zurück.

            :params: `data` Das komplette Datenobjekt als Liste
            """
            return [
                {
                    "point"     :   [row["geo_point_2d"]["lat"], row["geo_point_2d"]["lon"]],
                    "geom"      :   row["geo_shape"]["geometry"]["coordinates"],
                    "name"      :   row["tourismusdestination"]
                } for row in data
            ]

    class Load:
        @staticmethod
        def data(data: list) -> None:
            """
            Übergeordnete Funktion zum Laden der Daten in Postgres

            :params: `data` Das komplette Datenobjekt als Liste
            """
            from classes import Postgres
            # Aufgrund der wenigen Daten wird die Tabelle bei jedem Lauf 
            # geleert und dann neu befüllt
            Postgres.truncate_geo_table()
            for record in data:
                Postgres.insert_geo_data(record)