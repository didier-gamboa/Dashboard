from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.settings import APP_NAME, IS_MYSQL
from app.db import get_conn

app = FastAPI(title=APP_NAME)

# Dash corre en 8050 y consume la API en 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8050", "http://127.0.0.1:8050"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _cursor(conn):
    # MySQL necesita diccionarios; Postgres ya entrega dict_row
    return conn.cursor(dictionary=True) if IS_MYSQL else conn.cursor()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/clients")
def list_clients(conn=Depends(get_conn)):
    cur = _cursor(conn)
    try:
        cur.execute("""
            SELECT client_id, full_name, email, created_at
            FROM clients
            ORDER BY client_id
            LIMIT 50;
        """)
        return cur.fetchall()
    finally:
        cur.close()

@app.get("/kpis")
def kpis(conn=Depends(get_conn)):
    cur = _cursor(conn)
    try:
        # KPIs típicos con tu schema (clients, products, sales)
        cur.execute("""
            SELECT
              (SELECT COUNT(*) FROM clients) AS total_clients,
              (SELECT COUNT(*) FROM products) AS total_products,
              (SELECT COUNT(*) FROM sales) AS total_sales,
              (SELECT COUNT(*) FROM sales WHERE status = 'PAID') AS paid_sales,
              (SELECT COALESCE(SUM(quantity * unit_price), 0) FROM sales WHERE status = 'PAID') AS revenue_paid,
              (SELECT COALESCE(AVG(quantity * unit_price), 0) FROM sales WHERE status = 'PAID') AS avg_ticket_paid,
              (SELECT COUNT(DISTINCT client_id) FROM sales WHERE status = 'PAID') AS active_clients
        """)
        return cur.fetchone()
    finally:
        cur.close()

@app.get("/chart/sales_by_day")
def sales_by_day(conn=Depends(get_conn), days: int = 14, status: str = "PAID"):
    """
    Devuelve {labels:[...], values:[...]} con revenue por día.
    Demo-friendly: LIMIT por número de días disponibles.
    """
    cur = _cursor(conn)
    try:
        # Misma query funciona en MySQL y Postgres (LIMIT parametrizado).
        cur.execute("""
            SELECT sale_date AS d, COALESCE(SUM(quantity * unit_price), 0) AS revenue
            FROM sales
            WHERE status = %s
            GROUP BY sale_date
            ORDER BY sale_date DESC
            LIMIT %s
        """, (status, days))

        rows = cur.fetchall()
        rows = list(reversed(rows))  # ascendente para gráfica
        return {
            "labels": [str(r["d"]) for r in rows],
            "values": [float(r["revenue"]) for r in rows],
        }
    finally:
        cur.close()

@app.get("/chart/revenue_by_category")
def revenue_by_category(conn=Depends(get_conn), status: str = "PAID"):
    """
    Join sales+products, agrupa por category.
    """
    cur = _cursor(conn)
    try:
        cur.execute("""
            SELECT p.category AS category, COALESCE(SUM(s.quantity * s.unit_price), 0) AS revenue
            FROM sales s
            JOIN products p ON p.product_id = s.product_id
            WHERE s.status = %s
            GROUP BY p.category
            ORDER BY revenue DESC
        """, (status,))
        rows = cur.fetchall()
        return {
            "labels": [r["category"] for r in rows],
            "values": [float(r["revenue"]) for r in rows],
        }
    finally:
        cur.close()