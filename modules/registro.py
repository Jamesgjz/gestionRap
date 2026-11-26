import streamlit as st

from modules.ui import encabezado, panel, tarjetas_acciones, tarjetas_metricas
from rutas import enlace


def render():
    from database import traer_datos
    from modules.indicadores_registro import mostrar_registros_mensuales, resumen_operativo

    encabezado("Registro de participantes", "Administra a los participantes y docentes del proceso RAP.")
    tarjetas_acciones((
        ("Docentes evaluadores", "Consulta la lista y registra nuevos docentes.", "Gestionar docentes",
         ":material/school:", "docentes"),
        ("Participantes", "Registra a una persona y vincula sus asignaturas.", "Gestionar participantes",
         ":material/group:", "participantes"),
        ("Vista maestra", "Consulta el estado de las pruebas por participante.", "Abrir vista maestra",
         ":material/table_view:", "vista-maestra"),
    ))

    enlace("registro-csv", label="Registro automático (CSV)", icon=":material/upload_file:",
           nueva_pestana=True)

    participantes, _, pendientes, _, con_programacion, aprobados, reprobados = resumen_operativo()
    docentes, en_construccion, asignaturas = traer_datos("""
        SELECT (SELECT COUNT(*) FROM profesores),
               (SELECT COUNT(*) FROM maestro_pruebas
                WHERE lower(trim(estado)) IN ('en construcción', 'en construccion')),
               (SELECT COUNT(DISTINCT nullif(trim(alfa), '')) FROM asignaturas)
    """)[0]
    evaluados = aprobados + reprobados
    tarjetas_metricas((
        ("Participantes registrados", participantes), ("Docentes evaluadores", docentes),
        ("Pruebas en construcción", en_construccion), ("Asignaturas activas", asignaturas),
    ), ("azul", "morado", "ambar", "turquesa"))
    tarjetas_metricas((
        ("Cobertura de programación", f"{con_programacion / participantes:.0%}" if participantes else "—"),
        ("Resultados pendientes", pendientes),
        ("Tasa de aprobación", f"{aprobados / evaluados:.0%}" if evaluados else "—"),
    ), ("turquesa", "ambar", "verde"))
    mostrar_registros_mensuales()

    with panel("programaciones-recientes"):
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
