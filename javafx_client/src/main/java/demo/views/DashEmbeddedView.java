package demo.views;

import javafx.scene.layout.BorderPane;
import javafx.scene.web.WebView;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.Properties;

public class DashEmbeddedView extends BorderPane {

    public DashEmbeddedView() {
        Properties p = loadProps();
        String dashUrl = p.getProperty("dash.url", "http://localhost:8050");

        WebView web = new WebView();
        web.getEngine().load(dashUrl);
        setCenter(web);
    }

    private Properties loadProps() {
        try (InputStream in = getClass().getResourceAsStream("/demo/app.properties")) {
            Properties p = new Properties();
            if (in != null) p.load(new java.io.InputStreamReader(in, StandardCharsets.UTF_8));
            return p;
        } catch (Exception e) {
            return new Properties();
        }
    }
}