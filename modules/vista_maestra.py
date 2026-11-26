import streamlit as st
from database import traer_datos
from modules.ui import tabla_con_estados
import math

def volver_a_registros():
    st.session_state["reg_vista"] = "dashboard"


def render():
    st.button("← Volver a registros", on_click=volver_a_registros)
    st.title("Vista maestra de asignaturas por participante")

    if 'pagina_actual' not in st.session_state:
        st.session_state['pagina_actual'] = 1

    materias_bd = [
        (alfa.strip(), (nombre or alfa).strip())
        for alfa, nombre in traer_datos(
            "SELECT DISTINCT alfa, nombre_materia FROM asignaturas ORDER BY alfa"
        ) if alfa
    ]
    estudiantes_bd = traer_datos(
        "SELECT id_banner, nombre_completo, alfa_asignatura, estado_matriz "
        "FROM estudiantes ORDER BY nombre_completo, id_banner"
    )
    estados = {
        alfa.strip().upper(): (estado or "").casefold()
        for alfa, estado in traer_datos("SELECT alfa_asignatura, estado FROM maestro_pruebas")
        if alfa
    }


    f_col1, f_col3, f_col4 = st.columns([1.5, 1.2, 1])
    with f_col1:
        search_query = st.text_input("Buscar participante", placeholder="Buscar por nombre o ID Banner...", label_visibility="collapsed")
        if search_query != st.session_state.get("maestra_busqueda"):
            st.session_state["pagina_actual"] = 1
            st.session_state["maestra_busqueda"] = search_query
    with f_col3:
        vista_compacta = st.toggle("Vista compacta (Ocultar columnas N/A)", value=True)
    with f_col4:
        limite_filas = st.selectbox("Registros por página", [10, 25, 50], index=0, label_visibility="collapsed")

    # 1. Aplicar filtro de búsqueda sobre la data real
    estudiantes_filtrados = []
    for est in estudiantes_bd:
        id_b, name, alfas, estado_matricula = est
        if search_query and (search_query.lower() not in str(name).lower() and search_query not in str(id_b)):
            continue
        estudiantes_filtrados.append(est)

    total = len(estudiantes_filtrados)
    if not total:
        st.info("No hay participantes que coincidan con la búsqueda.")
        return
    max_pages = math.ceil(total / limite_filas)
    page = min(st.session_state["pagina_actual"], max_pages)
    st.session_state["pagina_actual"] = page
    start = (page - 1) * limite_filas
    visible = estudiantes_filtrados[start:start + limite_filas]
    active_codes = {
        code.strip().upper()
        for _, _, courses, _ in visible for code in (courses or "").split(",")
    }
    courses = {
        code.upper(): f"{code} · {name}"
        for code, name in materias_bd if not vista_compacta or code.upper() in active_codes
    }
    rows = []
    for banner, name, registered, enrollment in visible:
        codes = {code.strip().upper() for code in (registered or "").split(",")}
        row = {"ID Banner": banner, "Participante": name, "Matrícula": enrollment}
        for code, label in courses.items():
            row[label] = (estados.get(code) or "sin construir").capitalize() if code in codes else "—"
        rows.append(row)
    if courses:
        import pandas as pd

        tabla_con_estados(pd.DataFrame(rows), courses.values())
    else:
        st.dataframe(rows, hide_index=True, width="stretch")

    def mover_pagina(offset):
        st.session_state["pagina_actual"] += offset

    left, center, right = st.columns(3)
    left.button("◀ Anterior", disabled=page == 1, on_click=mover_pagina, args=(-1,))
    center.caption(f"Página {page} de {max_pages} · {total} participantes")
    right.button("Siguiente ▶", disabled=page == max_pages, on_click=mover_pagina, args=(1,))
