from importlib import import_module

import streamlit as st

from modules.ui import encabezado, tarjetas_acciones, tarjetas_metricas


def ir_a(vista):
    st.session_state["reg_vista"] = vista


def ver_resumen():
    from database import traer_datos

    encabezado("Registro de participantes", "Administra a los participantes y docentes del proceso RAP.")
    tarjetas_acciones((
        ("Docentes evaluadores", "Consulta la lista y registra nuevos docentes.", "Gestionar docentes",
         ":material/school:", ir_a, ("docentes",)),
        ("Participantes", "Registra a una persona y vincula sus asignaturas.", "Gestionar participantes",
         ":material/group:", ir_a, ("estudiantes",)),
        ("Vista maestra", "Consulta el estado de las pruebas por participante.", "Abrir vista maestra",
         ":material/table_view:", ir_a, ("maestra",)),
    ))

    tot_est, tot_prof, tot_pend, tot_asig = traer_datos("""
        SELECT (SELECT COUNT(*) FROM estudiantes),
               (SELECT COUNT(*) FROM profesores),
               (SELECT COUNT(*) FROM maestro_pruebas
                WHERE lower(trim(estado)) IN ('en construcción', 'en construccion')),
               (SELECT COUNT(DISTINCT nullif(trim(alfa), '')) FROM asignaturas)
    """)[0]
    tarjetas_metricas((
        ("Participantes registrados", tot_est), ("Docentes evaluadores", tot_prof),
        ("Pruebas en construcción", tot_pend), ("Asignaturas activas", tot_asig),
    ))

    with st.container(border=True):
        st.subheader("Programaciones recientes", anchor=False)
        programaciones = traer_datos("""
            SELECT e.nombre_completo, p.alfa_asignatura, p.fecha_aplicacion
            FROM programacion_pruebas p
            JOIN estudiantes e ON e.id_banner = p.id_banner
            ORDER BY p.fecha_registro DESC NULLS LAST, p.id DESC
            LIMIT 3
        """)
        for nombre, codigo, fecha in programaciones:
            st.text(f"{nombre} · {codigo} · {fecha:%d/%m/%Y}" if fecha else f"{nombre} · {codigo}")
        if not programaciones:
            st.caption("Aún no hay pruebas programadas.")


def render():
    if message := st.session_state.pop("registro_guardado", None):
        st.success(message)

    vista = st.session_state.get("reg_vista", "dashboard")
    if vista == "dashboard":
        ver_resumen()
        return

    module = {
        "docentes": "gestion_docentes",
        "estudiantes": "gestion_estudiantes",
        "maestra": "vista_maestra",
        "nuevo_docente": "nuevo_docente",
    }[vista]
    import_module(f"modules.{module}").render()
