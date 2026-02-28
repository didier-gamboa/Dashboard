import requests
from dash import Dash, dcc, html
import plotly.graph_objects as go

API_BASE = "http://localhost:8000"

def get_json(path: str):
    r = requests.get(API_BASE + path, timeout=10)
    r.raise_for_status()
    return r.json()

def make_kpi_row(k):
    def card(title, value):
        return html.Div(
            [
                html.Div(title, style={"fontWeight": "600"}),
                html.Div(value, style={"fontSize": "22px"}),
            ],
            style={
                "border": "1px solid #ddd",
                "borderRadius": "10px",
                "padding": "12px",
                "minWidth": "180px",
            },
        )

    return html.Div(
        [
            card("Revenue (PAID)", f"{k['revenue_paid']:.2f}"),
            card("Paid sales", str(k["paid_sales"])),
            card("Avg ticket", f"{k['avg_ticket_paid']:.2f}"),
            card("Active clients", str(k["active_clients"])),
        ],
        style={"display": "flex", "gap": "12px", "flexWrap": "wrap"},
    )

app = Dash(__name__)
app.title = "Dash Dashboard (via API)"

# Fetch once at startup (demo simple). Luego podemos hacerlo reactivo con callbacks.
kpis = get_json("/kpis")
main = get_json("/chart/sales_by_day?days=14&status=PAID")
by_cat = get_json("/chart/revenue_by_category?status=PAID")

fig_main = go.Figure(
    data=[go.Scatter(x=main["labels"], y=main["values"], mode="lines+markers")]
)
fig_main.update_layout(title="Revenue by day (PAID)", margin=dict(l=30, r=30, t=50, b=30))

fig_cat = go.Figure(
    data=[go.Bar(x=by_cat["labels"], y=by_cat["values"])]
)
fig_cat.update_layout(title="Revenue by category (PAID)", margin=dict(l=30, r=30, t=50, b=30))

app.layout = html.Div(
    [
        html.H2("Dashboard (Plotly Dash consuming FastAPI)"),
        make_kpi_row(kpis),
        html.Div(style={"height": "12px"}),
        dcc.Graph(figure=fig_main),
        dcc.Graph(figure=fig_cat),
        html.Div("Data source: FastAPI JSON endpoints", style={"opacity": 0.6}),
    ],
    style={"maxWidth": "1100px", "margin": "0 auto", "padding": "16px"},
)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8050, debug=True)