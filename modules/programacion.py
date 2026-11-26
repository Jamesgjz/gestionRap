from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

from database import ejecutar_query, traer_datos
from modules.exportacion import crear_excel


QUERY_HISTORICO = """
    SELECT p.id_banner, e.nombre_completo,
           COALESCE(a.nombre_materia, p.alfa_asignatura), p.fecha_registro,
           p.fecha_aplicacion, p.hora, p.alfa_asignatura,
           CASE WHEN lower(to_jsonb(p)->>'estado') IN ('cancelada', 'cancelado') THEN 'Cancelada'
                WHEN n.id_programacion IS NOT NULL THEN 'Completada'
                ELSE 'Programada' END
    FROM programacion_pruebas p
    JOIN estudiantes e ON e.id_banner = p.id_banner
    LEFT JOIN (
        SELECT DISTINCT ON (trim(alfa)) trim(alfa) AS alfa, nombre_materia
        FROM asignaturas ORDER BY trim(alfa), nombre_materia
    ) a ON a.alfa = trim(p.alfa_asignatura)
    LEFT JOIN notas n ON n.id_programacion = p.id
    ORDER BY p.fecha_aplicacion DESC, p.hora DESC, p.id DESC
"""
COLUMNAS = ["ID Banner", "Estudiante", "Asignatura", "Fecha de registro",
            "Fecha de aplicación", "Hora", "Código", "Estado"]


def agendar(hoy, hora_actual):
    st.subheader("Agendar o editar una prueba")
    with st.form("buscar_estudiante"):
        banner = st.text_input("ID Banner")
        buscar = st.form_submit_button("Buscar")
    if buscar:
        st.session_state.pop("agenda_banner", None)
        banner = banner.strip()
        if not (banner.isascii() and banner.isdecimal() and len(banner) <= 18):
            st.warning("Ingresa un ID Banner numérico válido.")
        else:
            st.session_state["agenda_banner"] = int(banner)

    banner_id = st.session_state.get("agenda_banner")
    if banner_id is None:
        return

    rows = traer_datos("""
        SELECT e.nombre_completo, curso.alfa, a.nombre_materia
        FROM estudiantes e
        LEFT JOIN LATERAL (
            SELECT DISTINCT trim(codigo) AS alfa
            FROM unnest(string_to_array(e.alfa_asignatura, ',')) AS codigos(codigo)
            WHERE EXISTS (
                SELECT 1 FROM maestro_pruebas m
                WHERE trim(m.alfa_asignatura) = trim(codigo)
                  AND lower(trim(m.estado)) IN ('disponible', 'construida', 'construido', 'lista')
            )
        ) curso ON true
        LEFT JOIN LATERAL (
            SELECT nombre_materia FROM asignaturas
            WHERE trim(alfa) = curso.alfa ORDER BY nombre_materia LIMIT 1
        ) a ON true
        WHERE e.id_banner = %s
        ORDER BY curso.alfa
    """, (banner_id,))
    if not rows:
        st.warning("No se encontró un estudiante con ese ID Banner.")
        return

    st.text(rows[0][0])
    courses = {alfa: name or alfa for _, alfa, name in rows if alfa}
    if not courses:
        st.info("El estudiante no tiene asignaturas con una prueba lista para agendar.")
        return

    course = st.selectbox(
        "Asignatura disponible", list(courses),
        format_func=lambda alfa: f"{alfa} · {courses[alfa]}",
        key=f"agendar_curso_{banner_id}",
    )
    previous = traer_datos("""
        SELECT fecha_aplicacion, hora FROM programacion_pruebas
        WHERE id_banner = %s AND alfa_asignatura = %s
    """, (banner_id, course))
    date, time = previous[0] if previous else (hoy, hora_actual)

    with st.form(f"programar_{banner_id}_{course}"):
        date = st.date_input("Fecha de aplicación", value=date)
        time = st.time_input("Hora de la prueba", value=time)
        if st.form_submit_button("Guardar programación", type="primary"):
            ejecutar_query("""
                INSERT INTO programacion_pruebas
                    (id_banner, alfa_asignatura, fecha_registro, fecha_aplicacion, hora)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id_banner, alfa_asignatura) DO UPDATE SET
                    fecha_aplicacion = EXCLUDED.fecha_aplicacion,
                    hora = EXCLUDED.hora
            """, (banner_id, course, hoy, date, time))
            st.success("Programación guardada.")


def historico(hoy):
    rows = traer_datos(QUERY_HISTORICO)
    if not rows:
        st.info("Aún no hay pruebas agendadas.")
        return

    st.subheader("Registro de pruebas")
    search, dates, courses, statuses = st.columns([2, 1, 1, 1])
    query = search.text_input("Estudiante, ID o asignatura").strip().casefold()
    dates = dates.selectbox("Rango de fechas", ["Todas", "Últimos 30 días", "Este mes"])
    course = courses.selectbox("Asignatura", ["Todas"] + sorted({r[2] for r in rows}))
    status = statuses.selectbox("Estado", ["Todos", "Programada", "Completada", "Cancelada"])

    since, until = None, None
    if dates == "Últimos 30 días":
        since, until = hoy - timedelta(days=29), hoy
    elif dates == "Este mes":
        since = hoy.replace(day=1)
        until = (since + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    visible = [
        row for row in rows
        if (not query or any(query in str(row[i]).casefold() for i in (0, 1, 2, 6)))
        and (since is None or (row[4] is not None and since <= row[4] <= until))
        and (course == "Todas" or row[2] == course)
        and (status == "Todos" or row[7] == status)
    ]
    if visible:
        st.dataframe(pd.DataFrame(visible, columns=COLUMNAS), hide_index=True, width="stretch")
        st.download_button(
            "Exportar Excel", lambda: crear_excel(COLUMNAS, visible),
            "programacion.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            on_click="ignore",
        )
    else:
        st.info("No hay pruebas que coincidan con los filtros.")

    with st.expander("Eliminar programación"):
        options = {(r[0], r[6]): f"{r[0]} · {r[1]} · {r[2]}" for r in rows}
        selected = st.selectbox("Prueba a eliminar", list(options), format_func=options.__getitem__)
        if st.button("Confirmar eliminación"):
            affected = ejecutar_query(
                "DELETE FROM programacion_pruebas WHERE id_banner = %s AND alfa_asignatura = %s",
                selected,
            )
            st.session_state["agenda_eliminada"] = affected
            st.rerun()


def render():
    st.title("Programación")
    now = datetime.now(ZoneInfo("America/Bogota"))
    view = st.radio("Vista de programación", ["Agendar y editar", "Registro de pruebas"], horizontal=True)
    if view == "Agendar y editar":
        agendar(now.date(), now.time().replace(second=0, microsecond=0))
    else:
        if "agenda_eliminada" in st.session_state:
            if st.session_state.pop("agenda_eliminada"):
                st.success("Programación eliminada.")
            else:
                st.warning("La programación ya no existe.")
        historico(now.date())
