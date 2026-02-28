package demo;

import java.io.InputStream;
import java.net.URI;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.util.Properties;

public class ApiClient {
    private final HttpClient http = HttpClient.newHttpClient();
    private final String baseUrl;

    public ApiClient() {
        this.baseUrl = loadProps().getProperty("api.baseUrl", "http://localhost:8000");
    }

    public String get(String path) throws Exception {
        HttpRequest req = HttpRequest.newBuilder()
                .uri(new URI(baseUrl + path))
                .GET()
                .build();
        return http.send(req, HttpResponse.BodyHandlers.ofString()).body();
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