import os
from dotenv import load_dotenv

load_dotenv()


def required(name: str) -> str:
    v = os.getenv(name)
    if v is None or v.strip() == "":
        raise RuntimeError(f"Missing environment variable: {name}")
    return v.strip()


def optional(name: str, default: str = "") -> str:
    v = os.getenv(name)
    return default if v is None else v.strip()


APP_NAME = "simple-api"

DB_TYPE = optional("DB_TYPE", "postgres").lower()  # postgres | mysql

DB_HOST = required("DB_HOST")
DB_PORT = int(required("DB_PORT"))
DB_NAME = required("DB_NAME")
DB_USER = required("DB_USER")
DB_PASSWORD = optional("DB_PASSWORD", "")

IS_POSTGRES = DB_TYPE in ("postgres")
IS_MYSQL = DB_TYPE in ("mysql")

if not (IS_POSTGRES or IS_MYSQL):
    raise RuntimeError("DB_TYPE must be 'postgres' or 'mysql'")

# DSN para Postgres (psycopg3)
PSYCOPG_DSN = (
    f"host={DB_HOST} "
    f"port={DB_PORT} "
    f"dbname={DB_NAME} "
    f"user={DB_USER} "
    f"password={DB_PASSWORD}"
)