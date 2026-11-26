import streamlit as st

from modules.ui import encabezado, tarjetas_acciones, tarjetas_metricas


def abrir(page, registro=None):
    st.session_state["opcion_menu"] = page
    if registro:
        st.session_state["reg_vista"] = registro


def render():
    encabezado("Panel de control", f"Bienvenido, {st.session_state['usuario']}")
    resumen = st.container()
    st.subheader("Acciones rápidas", anchor=False)
    tarjetas_acciones((
        ("Participantes", "Inscribe a una persona en el proceso RAP.", "Registrar participante",
         ":material/person_add:", abrir, ("Registro de participantes", "estudiantes")),
        ("Programación", "Agenda o modifica la fecha de una prueba.", "Programar prueba",
         ":material/calendar_month:", abrir, ("Programación",)),
        ("Evaluación", "Registra asistencia y calificaciones.", "Registrar resultado",
         ":material/rate_review:", abrir, ("Evaluación",)),
        ("Indicadores", "Consulta el avance del proceso RAP.", "Ver reportes",
         ":material/monitoring:", abrir, ("Dashboard / KPIs",)),
    ))

    with resumen:
        from modules.indicadores_registro import resumen_operativo

        st.subheader("Indicadores generales", anchor=False)
        conteos = resumen_operativo()[:4]
        etiquetas = ("Participantes registrados", "Pruebas agendadas",
                     "Resultados pendientes", "Resultados registrados")
        tarjetas_metricas(tuple(zip(etiquetas, conteos)), ("azul", "morado", "ambar", "verde"))
