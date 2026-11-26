from pathlib import Path

import streamlit as st

from database import ejecutar_query, traer_datos
from errors import DatabaseError


def esquema_listo():
    return traer_datos("SELECT to_regclass('rap_programa_asignaturas') IS NOT NULL")[0][0]


def preparar_esquema():
    if esquema_listo():
        return True
    st.info("Activa el catálogo de programas y el registro automático en la base de datos.")
    if not st.button("Activar funciones de registro", type="primary", icon=":material/database:"):
        return False
    migracion = Path(__file__).resolve().parents[1] / "migrations" / "002_programas_y_registros.sql"
    try:
        ejecutar_query(migracion.read_text(encoding="utf-8"))
    except DatabaseError as exc:
        if getattr(exc.__cause__, "pgcode", None) == "42501":
            st.error("La cuenta PostgreSQL de la app requiere permisos para crear tablas y modificar estudiantes y profesores.")
        else:
            st.error("La base de datos no pudo aplicar la actualización. Vuelve a intentarlo.")
        return False
    st.rerun()


def listar_programas():
    if not esquema_listo():
        return []
    return traer_datos("SELECT id, nombre FROM rap_programas ORDER BY lower(nombre), id")


def catalogo_asignaturas(programa_id=None):
    return traer_datos("""
        SELECT DISTINCT ON (upper(trim(a.alfa))) upper(trim(a.alfa)), a.nombre_materia
        FROM asignaturas a
        WHERE nullif(trim(a.alfa), '') IS NOT NULL
        ORDER BY upper(trim(a.alfa)), a.nombre_materia
    """) if programa_id is None else traer_datos("""
        SELECT DISTINCT ON (pa.alfa) pa.alfa, a.nombre_materia
        FROM rap_programa_asignaturas pa
        JOIN asignaturas a ON upper(trim(a.alfa)) = pa.alfa
        WHERE pa.programa_id = %s
        ORDER BY pa.alfa, a.nombre_materia
    """, (programa_id,))


def selector_programa(*, key=None):
    programas = dict(listar_programas())
    if not programas:
        return None
    return st.selectbox("Programa académico", [None, *programas],
                        format_func=lambda id_: programas.get(id_, "Sin asignar"), key=key)
