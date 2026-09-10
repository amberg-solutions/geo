from classes import Data, Postgres, ETL

#Data.download_geo_data()
#Data.download_dataset_catalogs()

Postgres.connect()

ETL.run_pipeline()


Postgres.close()