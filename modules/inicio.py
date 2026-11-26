import streamlit as st

from database import traer_datos


def abrir(page, registro=None):
    st.session_state["opcion_menu"] = page
    if registro:
        st.session_state["reg_vista"] = registro


def render():
    st.title("Panel de control")
    st.text(f"Bienvenido, {st.session_state['usuario']}")

    conteos = traer_datos("""
        SELECT (SELECT COUNT(*) FROM estudiantes),
               (SELECT COUNT(*) FROM programacion_pruebas),
               (SELECT COUNT(*) FROM programacion_pruebas p
                 WHERE p.fecha_aplicacion <= CURRENT_DATE
                   AND NOT EXISTS (SELECT 1 FROM notas n WHERE n.id_programacion = p.id)),
               (SELECT COUNT(*) FROM notas)
    """)[0]
    labels = ("Estudiantes registrados", "Pruebas agendadas", "Resultados pendientes", "Resultados registrados")
    for column, label, value in zip(st.columns(4), labels, conteos):
        column.metric(label, value)

    st.subheader("Acciones rápidas")
    links = (
        ("Registrar estudiante", "Registro Estudiantes", "estudiantes"),
        ("Programar prueba", "Programación", None),
        ("Registrar resultado", "Evaluación", None),
        ("Ver reportes", "Dashboard / KPIs", None),
    )
    for column, (label, page, registro) in zip(st.columns(4), links):
        column.button(label, width="stretch", on_click=abrir, args=(page, registro))
