import pandas as pd
import streamlit as st

from database import traer_datos


def ir_a(vista):
    st.session_state["reg_vista"] = vista


def render():
    st.button("← Volver a registros", on_click=ir_a, args=("dashboard",))
    st.title("Gestión de docentes evaluadores")
    st.button("+ Nuevo docente", type="primary", on_click=ir_a, args=("nuevo_docente",))

    docentes = traer_datos("""
        SELECT p.nombre_completo,
               coalesce(nullif(to_jsonb(p)->>'programa', ''), to_jsonb(p)->>'programa_academico'),
               to_jsonb(p)->>'asignaturas',
               to_jsonb(p)->>'horas_dedicacion',
               to_jsonb(p)->>'estado'
        FROM profesores p ORDER BY nombre_completo
    """)
    if not docentes:
        st.info("Aún no hay docentes registrados.")
        return

    col_search, col_programa, col_estado = st.columns([2, 1, 1])
    query = col_search.text_input("Buscar por nombre").strip().casefold()
    programa = col_programa.selectbox("Programa", ["Todos"] + sorted({r[1] for r in docentes if r[1]}))
    estado = col_estado.selectbox("Estado", ["Todos"] + sorted({r[4] for r in docentes if r[4]}))
    visible = [
        row for row in docentes
        if query in (row[0] or "").casefold()
        and (programa == "Todos" or row[1] == programa)
        and (estado == "Todos" or row[4] == estado)
    ]
    st.dataframe(
        pd.DataFrame(visible, columns=["Docente", "Programa", "Asignaturas RAP", "Horas asignadas", "Estado"]),
        hide_index=True, width="stretch", height="content",
    )
