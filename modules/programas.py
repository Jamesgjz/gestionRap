import pandas as pd
import streamlit as st

from database import ejecutar_query
from errors import DatabaseError
from modules.programas_datos import catalogo_asignaturas, listar_programas, preparar_esquema
from modules.ui import encabezado, panel


def render():
    encabezado("Programas académicos", "Crea programas y organiza las asignaturas que tienen pruebas RAP.")
    if not preparar_esquema():
        return
    if aviso := st.session_state.pop("programa_aviso", None):
        st.success(aviso)

    alta, relaciones = st.columns([1, 2], gap="medium")
    with alta, panel("crear-programa"):
        st.subheader("Nuevo programa", anchor=False)
        with st.form("form_rap_programa", clear_on_submit=True, border=False):
            nombre = st.text_input("Nombre del programa", max_chars=120)
            if st.form_submit_button("Crear programa", type="primary"):
                if not nombre.strip():
                    st.warning("Escribe el nombre del programa.")
                elif not ejecutar_query("""
                    INSERT INTO rap_programas (nombre) VALUES (%s)
                    ON CONFLICT DO NOTHING
                """, (nombre.strip(),)):
                    st.warning("Ya existe un programa con ese nombre.")
                else:
                    st.session_state["programa_aviso"] = "Programa creado."
                    st.rerun()

    with relaciones, panel("relacionar-programa"):
        st.subheader("Asignaturas y pruebas del programa", anchor=False)
        programas = dict(listar_programas())
        if not programas:
            st.info("Crea un programa para vincular sus asignaturas.")
            return
        programa_id = st.selectbox("Programa académico", list(programas), format_func=programas.__getitem__)
        catalogo = {codigo: nombre or codigo for codigo, nombre in catalogo_asignaturas()}
        actuales = catalogo_asignaturas(programa_id)
        with st.form(f"relaciones_programa_{programa_id}", border=False, clear_on_submit=True):
            disponibles = catalogo.keys() - {codigo for codigo, _ in actuales}
            seleccion = st.multiselect("Asignaturas para vincular", sorted(disponibles),
                                       format_func=lambda codigo: f"{codigo} · {catalogo[codigo]}")
            if st.form_submit_button("Vincular asignaturas", type="primary", disabled=not disponibles):
                if not seleccion:
                    st.warning("Selecciona al menos una asignatura.")
                else:
                    try:
                        cantidad = ejecutar_query("""
                            INSERT INTO rap_programa_asignaturas (programa_id, alfa)
                            SELECT %s, codigos.alfa FROM unnest(%s::text[]) AS codigos(alfa)
                            WHERE EXISTS (SELECT 1 FROM asignaturas a WHERE upper(trim(a.alfa)) = codigos.alfa)
                            ON CONFLICT DO NOTHING
                        """, (programa_id, seleccion))
                    except DatabaseError:
                        st.error("No se pudieron vincular las asignaturas.")
                    else:
                        st.session_state["programa_aviso"] = f"Asignaturas vinculadas: {cantidad}."
                        st.rerun()
        if actuales:
            st.dataframe(pd.DataFrame(actuales, columns=["Código", "Asignatura"]),
                         hide_index=True, width="stretch", height="content")
        else:
            st.caption("El programa aún no tiene asignaturas vinculadas.")
