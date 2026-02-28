package demo.views;

import javafx.geometry.Insets;
import javafx.scene.control.Tab;
import javafx.scene.control.TabPane;
import javafx.scene.layout.BorderPane;

public class DashboardView extends BorderPane {

    public DashboardView() {
        setPadding(new Insets(12));

        TabPane tabs = new TabPane();

        Tab nativeTab = new Tab("Dashboard nativo (JavaFX)", new NativeDashboardView());
        nativeTab.setClosable(false);

        Tab dashTab = new Tab("Dashboard Dash (WebView)", new DashEmbeddedView());
        dashTab.setClosable(false);

        tabs.getTabs().addAll(nativeTab, dashTab);
        setCenter(tabs);
    }
}