from html import escape
from importlib import import_module

import streamlit as st

from errors import DatabaseError


ADMIN = "admin"
ACADEMICA = "consulta_academica"
INDICADORES = "consulta"

# El orden de las rutas principales define el menú de cada perfil.
PAGINAS = {
    "": ("Inicio", "inicio", ":material/home:", (ADMIN,), True),
    "registro": ("Registro de participantes", "registro", ":material/group:", (ADMIN,), True),
    "programas": ("Programas académicos", "programas", ":material/account_tree:", (ADMIN,), True),
    "estado-pruebas": ("Estado de Pruebas", "estado_pruebas", ":material/assignment:", (ADMIN, ACADEMICA), True),
    "programacion": ("Programación", "programacion", ":material/calendar_today:", (ADMIN, ACADEMICA), True),
    "evaluacion": ("Evaluación", "evaluacion", ":material/rate_review:", (ADMIN,), True),
    "resultados": ("Resultados", "evaluacion", ":material/assignment_turned_in:", (ACADEMICA,), True),
    "indicadores": ("Dashboard / KPIs", "dashboard", ":material/dashboard:", (ADMIN, INDICADORES), True),
    "docentes": ("Docentes evaluadores", "gestion_docentes", None, (ADMIN,), False),
    "nuevo-docente": ("Nuevo docente", "nuevo_docente", None, (ADMIN,), False),
    "participantes": ("Registrar participante", "gestion_estudiantes", None, (ADMIN,), False),
    "vista-maestra": ("Vista maestra", "vista_maestra", None, (ADMIN,), False),
    "registro-csv": ("Registro automático", "registro_automatico", None, (ADMIN,), False),
}


def ruta_valida(ruta):
    return ruta in PAGINAS


def principal(rol):
    return next(ruta for ruta, (_, _, _, roles, menu) in PAGINAS.items() if menu and rol in roles)


def crear_pagina(ruta, config):
    titulo, modulo, icono, roles, _ = config

    def render():
        rol = st.session_state.get("rol")
        if rol not in roles:
            return
        if ruta in {"registro", "docentes", "nuevo-docente", "participantes", "vista-maestra", "registro-csv"}:
            if mensaje := st.session_state.pop("registro_guardado", None):
                st.success(mensaje)
        try:
            module = import_module(f"modules.{modulo}")
            if rol == ACADEMICA:
                module.render_consulta()
            else:
                module.render()
        except DatabaseError:
            st.error("No se pudo completar la operación en la base de datos.")
            st.button("Reintentar conexión", icon=":material/refresh:")

    return st.Page(render, title=titulo, icon=icono, url_path=ruta, default=ruta == "")


def enlace(ruta, *, label=None, icon=None, nueva_pestana=False):
    pagina = st.session_state["_rap_paginas"][ruta]
    if not nueva_pestana:
        st.page_link(pagina, label=label, icon=icon, width="stretch")
        return

    nombre = escape(pagina.title)
    with st.container():
        st.page_link(pagina, label=label, icon=icon, width="stretch")
        st.html(f'<a class="rap-nueva-pestana" href="./{ruta}" target="_blank" '
                f'aria-label="Abrir {nombre} en otra pestaña" title="Abrir {nombre} en otra pestaña">↗</a>')


def ir_a(ruta):
    st.switch_page(st.session_state["_rap_paginas"][ruta])

