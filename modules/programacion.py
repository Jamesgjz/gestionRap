from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

from database import connection_pool, ejecutar_query, leer, traer_datos, traer_pagina
from modules.exportacion import crear_excel, descarga_autorizada
from modules.ui import encabezado, panel, tabla_con_estados


CATALOGO = """
    LEFT JOIN (
        SELECT DISTINCT ON (trim(alfa)) trim(alfa) AS alfa, nombre_materia
        FROM asignaturas ORDER BY trim(alfa), nombre_materia
    ) a ON a.alfa = trim(p.alfa_asignatura)
"""
QUERY_HISTORICO = f"""
    SELECT p.id_banner, e.nombre_completo, COALESCE(a.nombre_materia, p.alfa_asignatura) AS asignatura,
           p.fecha_registro, p.fecha_aplicacion, p.hora, p.alfa_asignatura,
           CASE WHEN lower(to_jsonb(p)->>'estado') IN ('cancelada', 'cancelado') THEN 'Cancelada'
                WHEN n.id_programacion IS NOT NULL THEN 'Completada'
                ELSE 'Programada' END AS estado, p.id
    FROM programacion_pruebas p
    JOIN estudiantes e ON e.id_banner = p.id_banner
    {CATALOGO}
    LEFT JOIN notas n ON n.id_programacion = p.id
"""
FILTROS_HISTORICO = f"""
    SELECT * FROM ({QUERY_HISTORICO}) registro
    WHERE (%s = '' OR strpos(id_banner::text, %s) > 0
        OR strpos(translate(lower(nombre_completo), 'ÁÉÍÓÚÜÑ', 'áéíóúüñ'), %s) > 0
        OR strpos(translate(lower(asignatura), 'ÁÉÍÓÚÜÑ', 'áéíóúüñ'), %s) > 0
        OR strpos(translate(lower(alfa_asignatura), 'ÁÉÍÓÚÜÑ', 'áéíóúüñ'), %s) > 0)
      AND (%s::date IS NULL OR fecha_aplicacion BETWEEN %s AND %s)
      AND (%s IS NULL OR asignatura = %s)
      AND (%s IS NULL OR estado = %s)
"""
ORDEN_HISTORICO = "fecha_aplicacion DESC, hora DESC, id DESC"
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
        SELECT e.nombre_completo, curso.alfa, a.nombre_materia, p.fecha_aplicacion, p.hora, p.id
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
        LEFT JOIN programacion_pruebas p ON p.id_banner = e.id_banner AND p.alfa_asignatura = curso.alfa
        WHERE e.id_banner = %s
        ORDER BY curso.alfa
    """, (banner_id,))
    if not rows:
        st.warning("No se encontró un estudiante con ese ID Banner.")
        return

    st.text(rows[0][0])
    courses = {alfa: (name or alfa, fecha, hora, id_) for _, alfa, name, fecha, hora, id_ in rows if alfa}
    if not courses:
        st.info("El estudiante no tiene asignaturas con una prueba lista para agendar.")
        return

    course = st.selectbox(
        "Asignatura disponible", list(courses),
        format_func=lambda alfa: f"{alfa} · {courses[alfa][0]}",
        key=f"agendar_curso_{banner_id}",
    )
    _, date, time, id_ = courses[course]
    if id_ is None:
        date, time = hoy, hora_actual

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
            st.session_state["agenda_guardada"] = True
            st.rerun()


def mover_pagina(offset):
    st.session_state["programacion_pagina"] += offset


def historico(hoy, *, gestionar=False):
    asignaturas = traer_datos(f"""
        SELECT DISTINCT COALESCE(a.nombre_materia, p.alfa_asignatura) AS asignatura
        FROM programacion_pruebas p JOIN estudiantes e ON e.id_banner = p.id_banner
        {CATALOGO}
        ORDER BY asignatura
    """)
    if not asignaturas:
        st.info("Aún no hay pruebas agendadas.")
        return

    st.subheader("Registro de pruebas")
    search, dates, courses, statuses = st.columns([2, 1, 1, 1])
    query = search.text_input("Estudiante, ID o asignatura").strip().casefold()
    dates = dates.selectbox("Rango de fechas", ["Todas", "Últimos 30 días", "Este mes"])
    course = courses.selectbox("Asignatura", [None, *(nombre for (nombre,) in asignaturas if nombre)],
                              format_func=lambda valor: valor or "Todas")
    status = statuses.selectbox("Estado", [None, "Programada", "Completada", "Cancelada"],
                                format_func=lambda valor: valor or "Todos")

    since, until = None, None
    if dates == "Últimos 30 días":
        since, until = hoy - timedelta(days=29), hoy
    elif dates == "Este mes":
        since = hoy.replace(day=1)
        until = (since + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    contador, cantidad = st.columns([3, 1])
    limite = cantidad.selectbox("Filas por página", (15, 25, 50), index=1)
    filtros = (query, dates, course, status, limite)
    if filtros != st.session_state.get("programacion_filtros"):
        st.session_state["programacion_filtros"] = filtros
        st.session_state["programacion_pagina"] = 0
    params = (query, query, query, query, query, since, since, until, course, course, status, status)
    total, pagina, filas = traer_pagina(
        FILTROS_HISTORICO, params, ORDEN_HISTORICO, st.session_state["programacion_pagina"], limite,
    )
    st.session_state["programacion_pagina"] = pagina
    if filas:
        inicio = pagina * limite
        contador.caption(f"Mostrando {inicio + 1}–{inicio + len(filas)} de {total} registros")
        tabla_con_estados(pd.DataFrame([fila[:8] for fila in filas], columns=COLUMNAS), ("Estado",), height="content")
        anterior, centro, siguiente = st.columns([1, 2, 1])
        anterior.button("Anterior", disabled=pagina == 0, icon=":material/chevron_left:",
                        on_click=mover_pagina, args=(-1,))
        centro.caption(f"Página {pagina + 1} de {(total - 1) // limite + 1}")
        siguiente.button("Siguiente", disabled=inicio + limite >= total, icon=":material/chevron_right:",
                         on_click=mover_pagina, args=(1,))
        pool = connection_pool()

        def descargar():
            filas_excel = leer(f"{FILTROS_HISTORICO} ORDER BY {ORDEN_HISTORICO}", params, pool=pool)
            return crear_excel(COLUMNAS, (fila[:8] for fila in filas_excel))

        st.download_button(
            "Exportar Excel", descarga_autorizada(descargar), "programacion.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", on_click="ignore",
        )
    else:
        st.info("No hay pruebas que coincidan con los filtros.")

    if not gestionar:
        return

    editor = st.expander("Eliminar programación", key="programacion_eliminar", on_change="rerun")
    if editor.open:
        with editor:
            rows = traer_datos(f"""
                SELECT p.id_banner, p.alfa_asignatura, e.nombre_completo,
                       COALESCE(a.nombre_materia, p.alfa_asignatura)
                FROM programacion_pruebas p JOIN estudiantes e ON e.id_banner = p.id_banner
                {CATALOGO}
                ORDER BY p.fecha_aplicacion DESC, p.hora DESC, p.id DESC
            """)
            if not rows:
                return
            options = {(banner, codigo): f"{banner} · {nombre} · {materia}"
                       for banner, codigo, nombre, materia in rows}
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
        if st.session_state.pop("agenda_guardada", False):
            st.success("Programación guardada.")
        agendar(now.date(), now.time().replace(second=0, microsecond=0))
    else:
        if "agenda_eliminada" in st.session_state:
            if st.session_state.pop("agenda_eliminada"):
                st.success("Programación eliminada.")
            else:
                st.warning("La programación ya no existe.")
        historico(now.date(), gestionar=True)


def render_consulta():
    encabezado("Programación", "Consulta y exporta el calendario de las pruebas RAP.")
    with panel("programacion-consulta"):
        historico(datetime.now(ZoneInfo("America/Bogota")).date())
