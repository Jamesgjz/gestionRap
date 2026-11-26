# Gestión RAP · UNIMINUTO Virtual

Aplicación Streamlit para registrar estudiantes, gestionar docentes, programar y evaluar pruebas de Reconocimiento de Aprendizajes Previos.

## Ejecutar en desarrollo

Instala Python 3.12, ejecuta `python -m pip install -r requirements.txt` y luego `python -m streamlit run main.py`.

### Acceso institucional

1. Registra una aplicación web en el proveedor OpenID Connect de la institución. En el proveedor configura la URL de retorno del entorno, por ejemplo `http://localhost:8501/oauth2callback` para desarrollo o `https://tu-app.example/oauth2callback` para producción.
2. Guarda la configuración en `.streamlit/secrets.toml` o en los secretos de Streamlit Cloud. Genera `cookie_secret` con `python -c "import secrets; print(secrets.token_urlsafe(48))"`. Usa un secreto distinto para cada entorno.
3. Obtén de tu proveedor el identificador `sub` que emite **para este cliente OIDC** y agrega cada cuenta a su rol. Las cuentas en `admin_subjects` gestionan registros y evaluaciones. Las de `consulta_subjects` ven indicadores agregados. Un cambio de proveedor o tenant requiere actualizar las listas y rotar `cookie_secret`.

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "REEMPLAZAR"
client_id = "REEMPLAZAR"
client_secret = "REEMPLAZAR"
server_metadata_url = "https://proveedor.example/.well-known/openid-configuration"

[rap_access]
admin_subjects = ["IDENTIFICADOR_OIDC_ADMIN"]
consulta_subjects = []

[postgres]
host = "host-de-neon.example"
database = "neondb"
user = "usuario-de-aplicacion"
password = "REEMPLAZAR"
port = 5432
```

El despliegue requiere HTTPS. Usa un único emisor OIDC de confianza, con la URL de descubrimiento del tenant institucional. La aplicación verifica el vencimiento del token de identidad en cada ejecución.

[Configuración de OIDC en Streamlit](https://docs.streamlit.io/develop/concepts/connections/authentication)

### PostgreSQL

Usa la base de Gestión RAP existente. Antes de desplegar, valida en una copia de pruebas el esquema, los tipos y las restricciones del entorno. `migrations/001_campos_registro.sql` añade los campos de registro de estudiantes y docentes que falten y conserva los datos existentes. El registro de docentes usa `programa`, `asignaturas` y `observaciones` como texto y `horas_dedicacion` como entero. El catálogo de asignaturas se carga desde las tablas existentes.

Los flujos de actualización requieren claves únicas para `maestro_pruebas.alfa_asignatura`, `programacion_pruebas (id_banner, alfa_asignatura)` y `notas.id_programacion`, como en las sentencias de actualización de la aplicación. Confirma que la cuenta de PostgreSQL tenga permisos de lectura y escritura para estas operaciones antes del despliegue.

Como alternativa local a `[postgres]`, se admiten `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_PORT` y `DB_SSLMODE` en un archivo `.env`. Los secretos de autenticación se configuran en Streamlit.
