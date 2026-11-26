from collections import Counter
from datetime import date, datetime
from zoneinfo import ZoneInfo

import streamlit as st

from database import traer_datos
from modules.ui import panel


ZONA = ZoneInfo("America/Bogota")
MESES = ("Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")


def resumen_operativo():
    return traer_datos("""
        WITH agenda AS (
            SELECT count(*) AS agendadas,
                   count(*) FILTER (WHERE n.id_programacion IS NULL AND
                       p.fecha_aplicacion <= (CURRENT_TIMESTAMP AT TIME ZONE 'America/Bogota')::date) AS pendientes,
                   count(DISTINCT e.id_banner) AS con_programacion
            FROM programacion_pruebas p
            LEFT JOIN estudiantes e ON e.id_banner = p.id_banner
            LEFT JOIN notas n ON n.id_programacion = p.id
            WHERE coalesce(lower(trim(to_jsonb(p)->>'estado')), '') NOT IN ('cancelada', 'cancelado')
        ), resultados AS (
            SELECT count(*) AS registrados,
                   count(*) FILTER (WHERE upper(trim(resultado)) = 'APROBÓ') AS aprobados,
                   count(*) FILTER (WHERE upper(trim(resultado)) = 'REPROBÓ') AS reprobados
            FROM notas
        )
        SELECT (SELECT count(*) FROM estudiantes), agendadas, pendientes, registrados,
               con_programacion, aprobados, reprobados
        FROM agenda CROSS JOIN resultados
    """)[0]


def fecha_disponible(valores):
    for valor in valores:
        if not valor:
            continue
        try:
            fecha = datetime.fromisoformat(valor)
        except ValueError:
            continue
        return fecha.astimezone(ZONA).date() if fecha.tzinfo else fecha.date()
    return None


def registros_por_mes(fechas, hoy):
    ultimo = hoy.year * 12 + hoy.month - 1
    periodos = [date(anio, mes + 1, 1)
                for anio, mes in (divmod(i, 12) for i in range(ultimo - 11, ultimo + 1))]
    por_mes = Counter(date(fecha.year, fecha.month, 1) for fecha in fechas if fecha is not None and fecha <= hoy)
    return [(f"{MESES[mes.month - 1]} {mes.year}", por_mes[mes]) for mes in periodos]


def mostrar_registros_mensuales():
    with panel("registros-mensuales"):
        st.subheader("Registros por mes", anchor=False)
        fechas = [
            fecha_disponible(fila) for fila in traer_datos("""
                SELECT to_jsonb(e)->>'rap_registrado_en',
                       to_jsonb(e)->>'fecha_registro',
                       to_jsonb(e)->>'created_at'
                FROM estudiantes e
            """)
        ]
        hoy = datetime.now(ZONA).date()
        datos = registros_por_mes(fechas, hoy)
        sin_fecha = sum(fecha is None for fecha in fechas)
        if any(cantidad for _, cantidad in datos):
            import altair as alt
            import pandas as pd

            serie = pd.DataFrame(datos, columns=["Mes", "Participantes"])
            chart = alt.Chart(serie).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6,
                                               color="#087D86").encode(
                x=alt.X("Mes:N", sort=[mes for mes, _ in datos], title=None,
                        axis=alt.Axis(labelAngle=-35, labelFontSize=15)),
                y=alt.Y("Participantes:Q", axis=alt.Axis(tickMinStep=1, labelFontSize=15, titleFontSize=16)),
                tooltip=["Mes:N", "Participantes:Q"],
            ).properties(height=225)
            st.altair_chart(chart, width="stretch")
        else:
            st.info("Aún no hay registros fechados en los últimos 12 meses.")
        if sin_fecha:
            st.caption(f"Participantes sin fecha de registro: {sin_fecha}. La gráfica solo incluye fechas disponibles.")
