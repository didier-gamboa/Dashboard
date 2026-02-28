"""
seed_db_postgres.py

Seed mínimo para PostgreSQL con 3 tablas:
- clients
- products
- sales

La idea es tener pocos registros y datos fáciles de entender para probar la API.
Lee credenciales desde .env:
DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

Uso:
  python scripts/seed_db_postgres.py --reset
  python scripts/seed_db_postgres.py
"""

from __future__ import annotations

import argparse
import os
from datetime import date, timedelta

import psycopg
from dotenv import load_dotenv

load_dotenv()


DDL_SQL = """
CREATE TABLE IF NOT EXISTS clients (
  client_id  SERIAL PRIMARY KEY,
  full_name  TEXT NOT NULL,
  email      TEXT UNIQUE,
  created_at DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
  product_id  SERIAL PRIMARY KEY,
  name        TEXT NOT NULL,
  category    TEXT NOT NULL,
  unit_price  NUMERIC(12,2) NOT NULL CHECK(unit_price >= 0)
);

CREATE TABLE IF NOT EXISTS sales (
  sale_id    SERIAL PRIMARY KEY,
  sale_date  DATE NOT NULL,
  status     TEXT NOT NULL CHECK(status IN ('PAID','PENDING','CANCELLED')),
  client_id  INT NOT NULL REFERENCES clients(client_id),
  product_id INT NOT NULL REFERENCES products(product_id),
  quantity   INT NOT NULL CHECK(quantity > 0),
  unit_price NUMERIC(12,2) NOT NULL CHECK(unit_price >= 0)
);

CREATE INDEX IF NOT EXISTS idx_sales_date   ON sales(sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_status ON sales(status);
"""

RESET_SQL = """
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS clients;
"""


def required(name: str) -> str:
    v = os.getenv(name)
    if v is None or v.strip() == "":
        raise RuntimeError(f"Missing environment variable: {name}")
    return v.strip()


def optional(name: str, default: str = "") -> str:
    v = os.getenv(name)
    return default if v is None else v.strip()


def conn_params() -> dict:
    return {
        "host": required("DB_HOST"),
        "port": int(required("DB_PORT")),
        "dbname": required("DB_NAME"),
        "user": required("DB_USER"),
        "password": optional("DB_PASSWORD", ""),
    }


def seed(reset: bool) -> None:
    """
    Inserta un set pequeño y fijo:
    - 5 clients
    - 6 products
    - 12 sales
    """
    today = date.today()

    clients = [
        ("Ana García", "ana.garcia@example.com", today - timedelta(days=120)),
        ("Luis Pérez", "luis.perez@example.com", today - timedelta(days=90)),
        ("María López", "maria.lopez@example.com", today - timedelta(days=60)),
        ("Carlos Sánchez", "carlos.sanchez@example.com", today - timedelta(days=30)),
        ("Sofía Ramírez", "sofia.ramirez@example.com", today - timedelta(days=15)),
    ]

    products = [
        ("Teclado Mecánico", "Electrónica", 899.00),
        ("Mouse Inalámbrico", "Electrónica", 399.00),
        ("Termo Acero", "Hogar", 249.00),
        ("Playera Deportiva", "Ropa", 299.00),
        ("Cuaderno A4", "Oficina", 79.00),
        ("Chocolate 70%", "Alimentos", 59.00),
    ]

    # Ventas: (sale_date, status, client_id, product_id, quantity, unit_price)
    # Nota: unit_price aquí es el precio "congelado" (lo copiamos del producto).
    sales = [
        (today - timedelta(days=10), "PAID",      1, 1, 1, 899.00),
        (today - timedelta(days=10), "PAID",      2, 2, 2, 399.00),
        (today - timedelta(days=9),  "PAID",      3, 3, 1, 249.00),
        (today - timedelta(days=9),  "PENDING",   4, 4, 1, 299.00),
        (today - timedelta(days=8),  "PAID",      5, 5, 3, 79.00),
        (today - timedelta(days=8),  "CANCELLED", 1, 6, 2, 59.00),
        (today - timedelta(days=7),  "PAID",      2, 1, 1, 899.00),
        (today - timedelta(days=7),  "PAID",      3, 2, 1, 399.00),
        (today - timedelta(days=6),  "PAID",      4, 4, 2, 299.00),
        (today - timedelta(days=5),  "PAID",      5, 3, 1, 249.00),
        (today - timedelta(days=4),  "PAID",      1, 5, 2, 79.00),
        (today - timedelta(days=3),  "PENDING",   2, 6, 5, 59.00),
    ]

    with psycopg.connect(**conn_params()) as con:
        with con.cursor() as cur:
            if reset:
                cur.execute(RESET_SQL)

            cur.execute(DDL_SQL)

            # Si ya hay datos y no es reset, no insertamos de nuevo.
            cur.execute("SELECT COUNT(*) FROM clients;")
            if cur.fetchone()[0] > 0 and not reset:
                print("Seed skipped: data already exists. Use --reset to recreate tables.")
                return

            cur.executemany(
                "INSERT INTO clients(full_name, email, created_at) VALUES (%s, %s, %s);",
                clients,
            )
            cur.executemany(
                "INSERT INTO products(name, category, unit_price) VALUES (%s, %s, %s);",
                products,
            )
            cur.executemany(
                """
                INSERT INTO sales(sale_date, status, client_id, product_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                sales,
            )

        con.commit()

    print("Seed completed.")
    print("Inserted: clients=5, products=6, sales=12")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Drop and recreate tables before inserting.")
    args = parser.parse_args()
    seed(reset=args.reset)


if __name__ == "__main__":
    main()