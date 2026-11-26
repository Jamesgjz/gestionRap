# Gestión RAP · UNIMINUTO Virtual

Aplicación Streamlit para registrar estudiantes, gestionar docentes, programar y evaluar pruebas de Reconocimiento de Aprendizajes Previos.

## Ejecutar en desarrollo

Instala Python 3.12, ejecuta `python -m pip install -r requirements.txt` y luego `python -m streamlit run main.py`.

### Cuentas de acceso

Gestión RAP valida cuentas administradas desde los secretos de Streamlit. Desde una terminal interactiva, crea tu primera cuenta:

```powershell
python crear_cuenta.py tu_usuario --nombre "Tu nombre" --rol admin
```

El asistente pide la contraseña sin mostrarla y devuelve un bloque TOML con su hash. Agrega todo ese bloque en **Settings → Secrets** de la app publicada o en `.streamlit/secrets.toml` para desarrollo. Conserva el bloque `[postgres]` existente. Evita guardar este bloque en Git o enviarlo por chat.

Agrega un bloque por usuario. El rol `admin` gestiona los registros y las evaluaciones. El rol `consulta_academica` puede consultar y exportar estados de pruebas, programaciones y resultados. El rol `consulta` se limita al Dashboard. Los Excel de resultados pueden incluir nombres, IDs y notas. Crea una cuenta individual por persona autorizada, usando `--rol consulta_academica` en el comando. Las vistas de consulta carecen de acciones de edición y las escrituras desde la aplicación web requieren el rol `admin`. Para cambiar una contraseña ejecuta el comando otra vez y reemplaza su bloque. Para retirar el acceso, quita el bloque del usuario. Agrega al menos un administrador antes de integrar los cambios a la rama desplegada.

Las sesiones expiran tras 30 minutos sin actividad o 8 horas desde el inicio. Recargar la página puede requerir entrar de nuevo. Los intentos de acceso se limitan en memoria por proceso y cuenta. Publica la app mediante HTTPS y usa contraseñas nuevas y exclusivas para Gestión RAP.

[Administrar secretos en Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/app-settings)

### PostgreSQL

Usa la base de Gestión RAP existente. Antes de desplegar, valida en una copia de pruebas el esquema, los tipos y las restricciones del entorno. `migrations/001_campos_registro.sql` añade los campos de registro de estudiantes y docentes que falten y conserva los datos existentes. El registro de docentes usa `programa`, `asignaturas` y `observaciones` como texto y `horas_dedicacion` como entero. El catálogo de asignaturas se carga desde las tablas existentes.

Los flujos de actualización requieren claves únicas para `maestro_pruebas.alfa_asignatura`, `programacion_pruebas (id_banner, alfa_asignatura)` y `notas.id_programacion`, como en las sentencias de actualización de la aplicación. Confirma que la cuenta de PostgreSQL tenga permisos de lectura y escritura para estas operaciones antes del despliegue.

Como alternativa local a `[postgres]`, se admiten `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_PORT` y `DB_SSLMODE` en un archivo `.env`. Los secretos de autenticación se configuran en Streamlit.
