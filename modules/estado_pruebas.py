import math

import pandas as pd
import streamlit as st

from database import ejecutar_query, traer_datos
from modules.exportacion import crear_excel
from modules.ui import encabezado, etiqueta_estado, panel, tabla_con_estados, tarjetas_metricas


ESTADOS = ("Construida", "En construcción", "Sin construir")


def estado_visible(value):
    state = (value or "").strip().casefold()
    if state in {"construida", "construido", "disponible", "lista"}:
        return ESTADOS[0]
    if state in {"en construcción", "en construccion"}:
        return ESTADOS[1]
    return ESTADOS[2]


def volver():
    st.session_state["opcion_menu"] = "Inicio"


def render():
    st.button("← Volver al Panel Principal", on_click=volver)
    encabezado("Estado de Pruebas", "Consulta el avance de cada asignatura y asigna docentes evaluadores.")
    if message := st.session_state.pop("estado_guardado", None):
        st.success(message)

    profesores = dict(traer_datos("""
        SELECT COALESCE(to_jsonb(p)->>'id_professor', to_jsonb(p)->>'id_profesor', to_jsonb(p)->>'id'),
               nombre_completo
        FROM profesores p ORDER BY nombre_completo
    """))
    profesores.pop(None, None)
    catalogo = traer_datos("""
        SELECT a.alfa, a.nombre_materia, m.estado, m.id_profesor::text
        FROM (
            SELECT DISTINCT ON (trim(alfa)) trim(alfa) AS alfa, nombre_materia
            FROM asignaturas WHERE nullif(trim(alfa), '') IS NOT NULL
            ORDER BY trim(alfa), nombre_materia
        ) a
        LEFT JOIN maestro_pruebas m ON a.alfa = trim(m.alfa_asignatura)
        ORDER BY a.alfa
    """)
    rows = [(code, name or code, estado_visible(state), teacher) for code, name, state, teacher in catalogo]
    metrics = (("Asignaturas", len(rows)), *((state, sum(r[2] == state for r in rows)) for state in ESTADOS))
    tarjetas_metricas(metrics, ("azul", "verde", "ambar", "gris"))

    listado_col, gestion_col = st.columns([2.2, 1], gap="medium")
    with listado_col, panel("listado-pruebas"):
        st.subheader("Listado de pruebas", anchor=False)
        search, status = st.columns([2, 1])
        query = search.text_input("Buscar por asignatura o código").strip().casefold()
        status = status.selectbox("Estado de prueba", ("Todos", *ESTADOS))
        filtradas = [
            row for row in rows
            if (query in row[0].casefold() or query in row[1].casefold())
            and (status == "Todos" or row[2] == status)
        ]
        if not filtradas:
            st.info("No se encontraron asignaturas con estos filtros.")
            return

        if (query, status) != st.session_state.get("mon_filtros"):
            st.session_state["mon_filtros"] = (query, status)
            st.session_state["mon_page"] = 1

        max_page = math.ceil(len(filtradas) / 10)
        page = min(st.session_state.get("mon_page", 1), max_page)
        st.session_state["mon_page"] = page

        headers = ("Código", "Asignatura", "Estado", "Docente")
        tabla = [(code, name, state, profesores.get(teacher, "Sin asignar"))
                 for code, name, state, teacher in filtradas]
        tabla_con_estados(pd.DataFrame(tabla[(page - 1) * 10:page * 10], columns=headers), ("Estado",))
        left, middle, right = st.columns(3)

        def move_page(offset):
            st.session_state["mon_page"] += offset

        left.button("◀ Anterior", disabled=page == 1, on_click=move_page, args=(-1,))
        middle.caption(f"Página {page} de {max_page} · {len(filtradas)} asignaturas")
        right.button("Siguiente ▶", disabled=page == max_page, on_click=move_page, args=(1,))
        st.download_button(
            "Exportar Excel", lambda: crear_excel(headers, tabla),
            "estado-pruebas.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            on_click="ignore",
        )

    with gestion_col, panel("gestionar-prueba"):
        st.subheader("Gestionar prueba", anchor=False)
        options = {row[0]: row for row in filtradas}
        code = st.selectbox("Asignatura", list(options), format_func=lambda key: f"{key} · {options[key][1]}")
        _, _, current_status, current_teacher = options[code]
        etiqueta_estado(current_status)
        teachers = [None, *profesores]
        with st.form(f"estado_prueba_{code}", border=False):
            teacher = st.selectbox(
                "Docente a cargo", teachers, format_func=lambda key: f"{profesores[key]} · {key}" if key else "Sin asignar",
                index=teachers.index(current_teacher) if current_teacher in teachers else 0,
            )
            new_status = st.selectbox("Nuevo estado", ESTADOS, index=ESTADOS.index(current_status))
            if st.form_submit_button("Guardar cambios", type="primary", width="stretch"):
                ejecutar_query("""
                    INSERT INTO maestro_pruebas (alfa_asignatura, estado, id_profesor)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (alfa_asignatura) DO UPDATE SET
                        estado = EXCLUDED.estado, id_profesor = EXCLUDED.id_profesor
                """, (code, new_status, teacher))
                st.session_state["estado_guardado"] = f"Se guardaron los cambios de {code}."
                st.rerun()
