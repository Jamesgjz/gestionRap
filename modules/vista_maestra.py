import math

import pandas as pd
import streamlit as st

from database import traer_datos, traer_pagina
from errors import DatabaseError
from modules.ui import encabezado, tabla_con_estados


def volver_a_registros():
    st.session_state["reg_vista"] = "dashboard"


def codigos(texto):
    return {codigo.strip().upper() for codigo in (texto or "").split(",") if codigo.strip()}


def catalogo_y_estados():
    try:
        catalogo = traer_datos("""
            SELECT DISTINCT alfa, nombre_materia
            FROM asignaturas WHERE nullif(trim(alfa), '') IS NOT NULL
            ORDER BY alfa, nombre_materia
        """)
    except DatabaseError:
        catalogo = []
        st.warning("No se pudieron cargar los nombres de las asignaturas. Se muestran sus códigos.")

    try:
        estados = {
            alfa.strip().upper(): estado.strip().capitalize()
            for alfa, estado in traer_datos("SELECT alfa_asignatura, estado FROM maestro_pruebas")
            if alfa and estado and estado.strip()
        }
    except DatabaseError:
        estados = None
        st.warning("No se pudieron cargar los estados de las pruebas.")
    return catalogo, estados


def render():
    st.button("← Volver a registros", on_click=volver_a_registros)
    encabezado("Vista maestra de asignaturas por participante", "Busca participantes y consulta el estado de sus pruebas.")

    buscar, compacta, cantidad = st.columns([1.5, 1.2, 1])
    consulta = buscar.text_input(
        "Buscar participante", placeholder="Buscar por nombre o ID Banner…",
        label_visibility="collapsed",
    ).strip().casefold()
    vista_compacta = compacta.toggle("Vista compacta (Ocultar columnas N/A)", value=True)
    limite = cantidad.selectbox("Registros por página", [10, 25, 50], index=1, label_visibility="collapsed")

    if (consulta, limite) != st.session_state.get("filtros_maestra"):
        st.session_state["pagina_actual"] = 1
        st.session_state["filtros_maestra"] = (consulta, limite)
    total, pagina, visibles = traer_pagina("""
        SELECT e.id_banner, e.nombre_completo, e.alfa_asignatura,
               COALESCE(NULLIF(trim(to_jsonb(e)->>'estado_matriz'), ''),
                        NULLIF(trim(to_jsonb(e)->>'estado_matricula'), ''))
        FROM estudiantes e
        WHERE %s = '' OR strpos(translate(lower(e.nombre_completo), 'ÁÉÍÓÚÜÑ', 'áéíóúüñ'), %s) > 0
                     OR strpos(e.id_banner::text, %s) > 0
    """, (consulta, consulta, consulta), "nombre_completo, id_banner",
        st.session_state["pagina_actual"] - 1, limite)
    if not visibles:
        st.info("No hay participantes que coincidan con la búsqueda." if consulta else "Aún no hay participantes registrados.")
        return

    max_pages = math.ceil(total / limite)
    page = pagina + 1
    st.session_state["pagina_actual"] = page
    catalogo, estados = catalogo_y_estados()
    activos = set().union(*(codigos(fila[2]) for fila in visibles))

    cursos = {}
    for alfa, nombre in catalogo:
        codigo = alfa.strip().upper()
        if not vista_compacta or codigo in activos:
            cursos.setdefault(codigo, f"{codigo} · {nombre.strip()}" if nombre else codigo)
    for codigo in sorted(activos - cursos.keys()):
        cursos[codigo] = codigo

    rows = []
    for banner, nombre, asignaturas, matricula in visibles:
        asignadas = codigos(asignaturas)
        row = {"ID Banner": banner, "Participante": nombre, "Matrícula": matricula or "—"}
        for codigo, label in cursos.items():
            if codigo not in asignadas:
                row[label] = "—"
            elif estados is None:
                row[label] = "Sin datos"
            else:
                row[label] = estados.get(codigo, "Sin construir")
        rows.append(row)
    if cursos:
        tabla_con_estados(pd.DataFrame(rows), cursos.values(), height="content")
    else:
        st.dataframe(rows, hide_index=True, width="stretch", height="content", row_height=36)

    def mover_pagina(offset):
        st.session_state["pagina_actual"] += offset

    anterior, centro, siguiente = st.columns(3)
    anterior.button("◀ Anterior", disabled=page == 1, on_click=mover_pagina, args=(-1,))
    participantes_label = "participante" if total == 1 else "participantes"
    centro.caption(f"Página {page} de {max_pages} · {total} {participantes_label}")
    siguiente.button("Siguiente ▶", disabled=page == max_pages, on_click=mover_pagina, args=(1,))
