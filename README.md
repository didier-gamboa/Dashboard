# Proyecto Dashboard — Despliegue

Este documento describe pasos mínimos para desplegar la aplicación en orden: primero el backend (API), luego la aplicación Dash y finalmente el cliente JavaFX.

**Estructura principal**
- `backend_api/` : API en Python (instalación y semillas de BD en `scripts/`).
- `dash_app/` : Interfaz web con Dash.
- `javafx_client/` : Cliente de escritorio JavaFX (con Maven).

**Requisitos (macOS)**
- Python 3.10+ y `pip`.
- Java 17+ y Maven.
- Base de datos: PostgreSQL o MySQL (según preferencia).
- Opcional: Docker si desea contenerizar servicios.

--------------------
**1) Backend (backend_api)**

1. Entrar al directorio del backend:

```bash
cd backend_api
```

2. Crear y activar un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno. El backend lee un archivo `.env` en el mismo directorio (`backend_api/.env`).
   Copie el ejemplo y ajuste los valores según su base de datos:

```ini
DB_TYPE=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=store_db
DB_USER=postgres
DB_PASSWORD=password     # cambiar por su contraseña
APP_NAME=Dashboard API
```

   Alternativamente puede exportar las variables en el shell:

```bash
export DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DBNAME"
export SECRET_KEY="cambiar_por_una_clave_segura"
```

5. Sembrar datos de ejemplo (opcional, elegir script según BD):

```bash
python scripts/seed_db_postgres.py
# o
python scripts/seed_db_mysql.py
```

6. Levantar la API (si usa FastAPI/uvicorn):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Si la aplicación usa otro comando para ejecutar la API, usarlo en su lugar (por ejemplo `python -m app.main`). Verifique `backend_api/app/main.py`.

--------------------
**2) Dash (dash_app)**

1. Abrir una nueva terminal e ir al directorio Dash:

```bash
cd dash_app
```

2. Crear/activar entorno virtual e instalar dependencias:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Asegurarse de que la API esté corriendo y que la URL base esté correcta (si la app consume la API, actualizar la configuración en `dash_app` si hace falta).

4. Ejecutar la app Dash:

```bash
python app.py
```

Por defecto la app suele escuchar en `http://127.0.0.1:8050`.

--------------------
**3) Cliente JavaFX (javafx_client)**

1. Requisitos: Java 17+ instalado y `mvn` disponible.

2. Revisar configuración de la API en:

```
src/main/resources/demo/app.properties
```

Editar la propiedad que señala la URL base de la API para que apunte a `http://localhost:8000` (o donde haya desplegado el backend).

3. Ejecutar con Maven:

```bash
cd javafx_client
mvn clean javafx:run
```

Si prefiere empaquetar un JAR, puede usar `mvn package` y ejecutar con la JVM adecuada.

--------------------
**Solución de problemas rápida**
- Si no se conecta el cliente JavaFX a la API: verificar `app.properties` y CORS en la API.
- Errores al instalar dependencias Python: active el entorno virtual antes de `pip install`.
- Conflicto de puertos: asegúrese de que `8000` (API) y `8050` (Dash) estén libres o cámbielos.

--------------------
**Notas finales**
- Esta guía da pasos mínimos para desarrollo y pruebas locales. Para producción considere usar: servir la API con un servidor ASGI en contenedor, configurar TLS, usar un proxy (nginx), y contenerizar servicios con Docker.
- Si desea, puedo añadir pasos de Docker Compose o CI/CD.

---
Archivo creado automáticamente: instrucciones básicas para despliegue local.
