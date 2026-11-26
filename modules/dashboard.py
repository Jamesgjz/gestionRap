import streamlit as st

from database import traer_datos
from modules.colores import PALETA
from modules.ui import encabezado, panel, tabla_con_estados, tarjetas_metricas


def porcentaje(parte, total):
    return f"{parte / total:.0%}" if total else "—"


def resumen(titulo, categoria, filas, color, tonos=None):
    if not filas or not any(total for _, total in filas):
        st.info("Aún no hay datos para este indicador.")
        return

    import altair as alt
    import pandas as pd

    datos = pd.DataFrame(filas, columns=[categoria, "Cantidad"])
    barra = alt.Chart(datos).encode(
        x=alt.X(
            "Cantidad:Q", scale=alt.Scale(domain=[0, max(datos["Cantidad"]) * 1.2]),
            axis=alt.Axis(title=None, tickMinStep=1, grid=True),
        ),
        y=alt.Y(f"{categoria}:N", sort="-x", axis=alt.Axis(title=None, labelLimit=175)),
    )
    color_barra = alt.value(PALETA[color][0])
    if tonos:
        color_barra = alt.Color(
            f"{categoria}:N",
            scale=alt.Scale(domain=list(tonos), range=[PALETA[t][0] for t in tonos.values()]),
            legend=None,
        )

    barras = barra.mark_bar(cornerRadiusEnd=7, height=22).encode(
        color=color_barra,
        tooltip=[alt.Tooltip(f"{categoria}:N"), alt.Tooltip("Cantidad:Q", format="d")],
    )
    valores = barra.mark_text(align="left", dx=7, fontSize=18, fontWeight=700, color="#17304D").encode(
        text=alt.Text("Cantidad:Q", format="d"),
    )
    grafico_final = (barras + valores).properties(
        height=max(135, 36 * len(datos)),
        width="container", autosize=alt.AutoSizeParams(type="fit-x", contains="padding", resize=True),
    ).configure_axis(labelFontSize=16, labelColor="#34516E", gridColor="#E5EDF5").configure_view(strokeWidth=0)

    grafico, tabla = st.columns([3, 2], gap="medium")
    with grafico, panel("indicador-grafico"):
        st.subheader(titulo, anchor=False)
        st.altair_chart(grafico_final, width="stretch", theme=None)
    with tabla, panel("indicador-detalle"):
        st.subheader("Detalle", anchor=False)
        tabla_con_estados(datos, (categoria,))


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
    tonos = dict(zip(orden, ("verde", "ambar", "gris")))
    tarjetas_metricas(datos, tuple(tonos.values()))
    resumen("Distribución del banco", "Estado", datos, "azul", tonos)


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
    ), ("morado", "verde"))
    resumen("Pruebas listas por docente", "Docente", datos, "morado")


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
    ), ("azul", "turquesa", "morado"))
    resumen("Cobertura de asignaturas solicitadas", "Estado",
            [("Con programación", programadas), ("Por programar", solicitadas - programadas)],
            "azul", {"Con programación": "turquesa", "Por programar": "ambar"})


def asistencia():
    presentes, ausentes = traer_datos("""
        SELECT COUNT(*) FILTER (WHERE asistencia IS TRUE),
               COUNT(*) FILTER (WHERE asistencia IS FALSE)
        FROM notas
    """)[0]
    tarjetas_metricas((
        ("Asistieron", presentes), ("No asistieron", ausentes),
        ("Tasa de asistencia", porcentaje(presentes, presentes + ausentes)),
    ), ("verde", "ambar", "turquesa"))
    resumen("Asistencia a las pruebas evaluadas", "Asistencia",
            [("Asistió", presentes), ("No asistió", ausentes)], "verde", {"Asistió": "verde", "No asistió": "ambar"})


def aprobacion():
    aprobados, reprobados = traer_datos("""
        SELECT COUNT(*) FILTER (WHERE upper(trim(resultado)) = 'APROBÓ'),
               COUNT(*) FILTER (WHERE upper(trim(resultado)) = 'REPROBÓ')
        FROM notas
    """)[0]
    tarjetas_metricas((
        ("Aprobaron", aprobados), ("Reprobaron", reprobados),
        ("Tasa de aprobación", porcentaje(aprobados, aprobados + reprobados)),
    ), ("verde", "rojo", "azul"))
    resumen("Resultados de quienes presentaron la prueba", "Resultado",
            [("Aprobó", aprobados), ("Reprobó", reprobados)], "verde", {"Aprobó": "verde", "Reprobó": "rojo"})


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
