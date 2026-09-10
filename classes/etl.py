"""
Dieses Klassenmodul steuert die ETL-Pipeline und sorgt für die übergeordnete Logik des ETL-Prozess (Extrahieren, Transformieren, Laden)
"""

class ETL:

    @staticmethod
    def run_pipeline() -> None:
        """
        Diese übergeordnete Funktion 
        """
        data = ETL.Extract.data()
        transformed = ETL.Transform.data(data)
        ETL.Load.data(transformed)

    class Extract:
        @staticmethod
        def data() -> list:

            return []

    class Transform:
        @staticmethod
        def data(data: list) -> list:


            return []

    class Load:
        @staticmethod
        def data(data: list) -> None:
            ...