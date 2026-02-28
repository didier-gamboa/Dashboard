package demo;

import demo.views.DashboardView;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class App extends Application {
    @Override
    public void start(Stage stage) {
        stage.setTitle("JavaFX Dashboard (Native + Dash WebView)");
        stage.setScene(new Scene(new DashboardView(), 1100, 700));
        stage.show();
    }

    public static void main(String[] args) { launch(args); }
}