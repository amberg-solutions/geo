from classes import Data, Postgres, ETL

#Data.download_dataset_data()
#Data.download_dataset_catalogs()

Postgres.connect()

#ETL.run_pipeline()
Data.download_dataset_data("dvs_awt_soci_2026061801", "new")

Postgres.close()