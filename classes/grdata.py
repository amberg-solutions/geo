import requests
from classes.helper import write_json

class Data:

    BASE_URL = "https://data.gr.ch/api/explore/v2.1/"

    @classmethod
    def download_dataset_catalogs(cls) -> None:
        """
        Ruft Informationen zu Datensets ab und lädt sie in `data/datasets.json` als .json runter.
        """

        url = cls.BASE_URL + "catalog/datasets"
        params = {
            "limit": 20,
        }

        response = requests.get(url, params=params).json()

        write_json("datasets.json", response)

    @classmethod
    def download_geo_data(cls, dataset_id = "dvs_awt_econ_202601260") -> None:
        """
        Lädt Geodaten herunter und speichert sie in `data/geo.json`

        :params: `dataset_id`: Die ID des Datensets, default Tourismusdestinationen Graubünden
        """
        url = cls.BASE_URL + f"catalog/datasets/{dataset_id}/records"
        params = {
            "limit"     :   100,
        }
        response = requests.get(url, params=params).json()

        write_json("geo.json", response)

