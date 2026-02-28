package demo.views;

import com.fasterxml.jackson.databind.ObjectMapper;
import demo.ApiClient;
import demo.models.Kpis;
import demo.models.Series;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.scene.chart.*;
import javafx.scene.control.*;
import javafx.scene.layout.*;

public class NativeDashboardView extends BorderPane {

    private final ApiClient api = new ApiClient();
    private final ObjectMapper mapper = new ObjectMapper();

    // KPI labels
    private final Label revenue = new Label("…");
    private final Label paidSales = new Label("…");
    private final Label avgTicket = new Label("…");
    private final Label activeClients = new Label("…");

    // Charts
    private final LineChart<String, Number> lineChart;
    private final BarChart<String, Number> barChart;

    public NativeDashboardView() {
        setPadding(new Insets(12));

        VBox root = new VBox(12);
        root.setPadding(new Insets(10));

        HBox kpiRow = new HBox(12,
                card("Revenue (PAID)", revenue),
                card("Paid sales", paidSales),
                card("Avg ticket", avgTicket),
                card("Active clients", activeClients)
        );

        CategoryAxis x1 = new CategoryAxis();
        NumberAxis y1 = new NumberAxis();
        lineChart = new LineChart<>(x1, y1);
        lineChart.setTitle("Nivel 2: Revenue by day (PAID)");

        CategoryAxis x2 = new CategoryAxis();
        NumberAxis y2 = new NumberAxis();
        barChart = new BarChart<>(x2, y2);
        barChart.setTitle("Nivel 3: Revenue by category (PAID)");

        Button refresh = new Button("Refresh");
        Label status = new Label(" ");
        ToolBar toolbar = new ToolBar(refresh, new Separator(), status);

        refresh.setOnAction(e -> loadAll(status));

        root.getChildren().addAll(toolbar, kpiRow, lineChart, barChart);
        setCenter(root);

        loadAll(status);
    }

    private VBox card(String title, Label valueLabel) {
        Label t = new Label(title);
        t.setStyle("-fx-font-weight: bold; -fx-font-size: 13;");
        valueLabel.setStyle("-fx-font-size: 20;");

        VBox box = new VBox(6, t, valueLabel);
        box.setPadding(new Insets(10));
        box.setMinWidth(200);
        box.setStyle("-fx-border-color: #ddd; -fx-border-radius: 10; -fx-background-radius: 10;");
        return box;
    }

    private void loadAll(Label status) {
        status.setText("Loading…");

        new Thread(() -> {
            try {
                // KPIs
                Kpis k = mapper.readValue(api.get("/kpis"), Kpis.class);

                // Main series
                Series s = mapper.readValue(api.get("/chart/sales_by_day?days=14&status=PAID"), Series.class);

                // Category series
                Series c = mapper.readValue(api.get("/chart/revenue_by_category?status=PAID"), Series.class);

                Platform.runLater(() -> {
                    revenue.setText(String.format("%.2f", k.revenue_paid));
                    paidSales.setText(String.valueOf(k.paid_sales));
                    avgTicket.setText(String.format("%.2f", k.avg_ticket_paid));
                    activeClients.setText(String.valueOf(k.active_clients));

                    // Line chart
                    XYChart.Series<String, Number> line = new XYChart.Series<>();
                    line.setName("Revenue");
                    lineChart.getData().clear();
                    for (int i = 0; i < s.labels.size(); i++) {
                        line.getData().add(new XYChart.Data<>(s.labels.get(i), s.values.get(i)));
                    }
                    lineChart.getData().add(line);

                    // Bar chart
                    XYChart.Series<String, Number> bars = new XYChart.Series<>();
                    bars.setName("Revenue");
                    barChart.getData().clear();
                    for (int i = 0; i < c.labels.size(); i++) {
                        bars.getData().add(new XYChart.Data<>(c.labels.get(i), c.values.get(i)));
                    }
                    barChart.getData().add(bars);

                    status.setText("OK");
                });

            } catch (Exception ex) {
                Platform.runLater(() -> status.setText("Error: " + ex.getMessage()));
            }
        }).start();
    }
}