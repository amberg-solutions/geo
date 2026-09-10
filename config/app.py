import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
FILE_DIR = os.path.join(BASE_DIR, "data")

if not os.path.exists(FILE_DIR):
    os.makedirs(FILE_DIR, exist_ok=True)

PG_HOST = "localhost"
PG_PORT = 5432
PG_USER = "postgres"
PG_PASS = os.getenv("PG_PASSWORD")
PG_DB = "geo"