import streamlit as st

from database import traer_datos
from modules.ui import encabezado, panel, tarjetas_metricas


def porcentaje(parte, total):
    return f"{parte / total:.0%}" if total else "—"


def resumen(titulo, categoria, filas, color):
    if not filas or not any(total for _, total in filas):
        st.info("Aún no hay datos para este indicador.")
        return

    import pandas as pd

    datos = pd.DataFrame(filas, columns=[categoria, "Cantidad"])
    grafico, tabla = st.columns([3, 2], gap="medium")
    with grafico, panel("indicador-grafico"):
        st.subheader(titulo, anchor=False)
        st.bar_chart(datos, x=categoria, y="Cantidad", horizontal=True, sort="-Cantidad", color=color)
    with tabla, panel("indicador-detalle"):
        st.subheader("Detalle", anchor=False)
        st.dataframe(datos, hide_index=True, width="stretch")


def banco_de_pruebas():
    filas = dict(traer_datos("""
        WITH catalogo AS (
            SELECT DISTINCT trim(alfa) AS codigo
            FROM asignaturas WHERE nullif(trim(alfa), '') IS NOT NULL
        ), estados AS (
            SELECT c.codigo,
                   CASE WHEN bool_or(lower(trim(m.estado)) IN
                       ('construida', 'construido', 'disponible', 'lista')) THEN 'Construida'
                        WHEN bool_or(lower(trim(m.estado)) IN
                       ('en construcción', 'en construccion')) THEN 'En construcción'
                        ELSE 'Sin construir' END AS estado
            FROM catalogo c
            LEFT JOIN maestro_pruebas m ON trim(m.alfa_asignatura) = c.codigo
            GROUP BY c.codigo
        )
        SELECT estado, COUNT(*) FROM estados GROUP BY estado
    """))
    orden = ("Construida", "En construcción", "Sin construir")
    datos = [(estado, filas.get(estado, 0)) for estado in orden]
    tarjetas_metricas(datos)
    resumen("Distribución del banco", "Estado", datos, "#1559D6")


def productividad():
    datos = traer_datos("""
        SELECT p.nombre_completo, COUNT(DISTINCT trim(m.alfa_asignatura)) AS total
        FROM profesores p
        JOIN maestro_pruebas m ON m.id_profesor::text = COALESCE(
            to_jsonb(p)->>'id_professor', to_jsonb(p)->>'id_profesor', to_jsonb(p)->>'id'
        )
        WHERE lower(trim(m.estado)) IN ('construida', 'construido', 'disponible', 'lista')
        GROUP BY p.nombre_completo
        ORDER BY total DESC, p.nombre_completo
    """)
    tarjetas_metricas((
        ("Docentes con pruebas listas", len(datos)),
        ("Pruebas construidas", sum(total for _, total in datos)),
    ))
    resumen("Pruebas listas por docente", "Docente", datos, "#7134B8")


def cobertura():
    solicitadas, programadas = traer_datos("""
        WITH solicitadas AS (
            SELECT DISTINCT trim(codigo) AS codigo
            FROM estudiantes e
            CROSS JOIN LATERAL unnest(string_to_array(e.alfa_asignatura, ',')) AS cursos(codigo)
            WHERE nullif(trim(codigo), '') IS NOT NULL
        ), programadas AS (
            SELECT DISTINCT trim(p.alfa_asignatura) AS codigo
            FROM programacion_pruebas p
            WHERE coalesce(lower(to_jsonb(p)->>'estado'), '') NOT IN ('cancelada', 'cancelado')
        )
        SELECT COUNT(*), COUNT(p.codigo)
        FROM solicitadas s LEFT JOIN programadas p USING (codigo)
    """)[0]
    tarjetas_metricas((
        ("Solicitadas", solicitadas), ("Con programación", programadas),
        ("Cobertura", porcentaje(programadas, solicitadas)),
    ))
    resumen("Cobertura de asignaturas solicitadas", "Estado",
            [("Con programación", programadas), ("Por programar", solicitadas - programadas)], "#1559D6")


def asistencia():
    presentes, ausentes = traer_datos("""
        SELECT COUNT(*) FILTER (WHERE asistencia IS TRUE),
               COUNT(*) FILTER (WHERE asistencia IS FALSE)
        FROM notas
    """)[0]
    tarjetas_metricas((
        ("Asistieron", presentes), ("No asistieron", ausentes),
        ("Tasa de asistencia", porcentaje(presentes, presentes + ausentes)),
    ))
    resumen("Asistencia a las pruebas evaluadas", "Asistencia",
            [("Asistió", presentes), ("No asistió", ausentes)], "#008461")


def aprobacion():
    aprobados, reprobados = traer_datos("""
        SELECT COUNT(*) FILTER (WHERE upper(trim(resultado)) = 'APROBÓ'),
               COUNT(*) FILTER (WHERE upper(trim(resultado)) = 'REPROBÓ')
        FROM notas
    """)[0]
    tarjetas_metricas((
        ("Aprobaron", aprobados), ("Reprobaron", reprobados),
        ("Tasa de aprobación", porcentaje(aprobados, aprobados + reprobados)),
    ))
    resumen("Resultados de quienes presentaron la prueba", "Resultado",
            [("Aprobó", aprobados), ("Reprobó", reprobados)], "#008461")


def render():
    encabezado("Dashboard / KPIs", "Consulta el avance de las pruebas, la asistencia y los resultados del proceso RAP.")
    indicadores = {
        "Banco de pruebas": banco_de_pruebas,
        "Cobertura de programación": cobertura,
        "Asistencia": asistencia,
        "Aprobación": aprobacion,
    }
    if st.session_state.get("rol") == "admin":
        indicadores["Pruebas por docente"] = productividad

    with panel("indicador-filtro"):
        indicador = st.selectbox("Indicador", indicadores)
    indicadores[indicador]()
