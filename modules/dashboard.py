import streamlit as st
import pandas as pd
import plotly.express as px
from database import traer_datos

def render():
    st.title("📊 Tablero de Control - KPIs Gestión RAP")
    st.info("Seleccione un indicador del menú desplegable para evaluar el rendimiento del proceso en tiempo real.")

    # --- LISTA DESPLEGABLE DE KPIs ---
    kpi_seleccionado = st.selectbox(
        "🎯 Seleccione el KPI a visualizar:",
        [
            "1. Estado General de las Pruebas (Avance de Construcción)",
            "2. Productividad de Docentes (Pruebas Construidas)",
            "3. Cobertura: Asignaturas Solicitadas vs. Programadas",
            "4. Control de Asistencia a Pruebas Programadas",
            "5. Rendimiento Académico: Tasa de Aprobación (Sugerido)"
        ]
    )

    st.divider()

    # =========================================================================
    # KPI 1: ESTADO GENERAL DE LAS PRUEBAS
    # =========================================================================
    if kpi_seleccionado.startswith("1."):
        st.subheader("📌 Estado de Construcción de las Pruebas")
        
        # Consultamos el conteo directo desde maestro_pruebas
        # Mapeamos los estados posibles para no perder los que estén en cero
        query = "SELECT estado, COUNT(*) FROM maestro_pruebas GROUP BY estado"
        datos = traer_datos(query)
        
        # Estructuramos una base por defecto por si la tabla está vacía o faltan estados
        estados_base = {"Construida": 0, "En construcción": 0, "Sin construir": 0}
        if datos:
            for est, cant in datos:
                if est in estados_base:
                    estados_base[est] = cant
        
        # Añadimos las "Sin construir" contando las asignaturas que no están en maestro_pruebas
        total_asignaturas = traer_datos("SELECT COUNT(*) FROM asignaturas")
        total_en_maestro = traer_datos("SELECT COUNT(DISTINCT alfa_asignatura) FROM maestro_pruebas")
        
        cant_asignaturas = total_asignaturas[0][0] if total_asignaturas else 0
        cant_en_maestro = total_en_maestro[0][0] if total_en_maestro else 0
        estados_base["Sin construir"] = max(0, cant_asignaturas - cant_en_maestro)

        df_kpi1 = pd.DataFrame(list(estados_base.items()), columns=["Estado", "Cantidad"])

        # Renderizado en columnas: Gráfico + Tabla Resumen
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig1 = px.pie(df_kpi1, values="Cantidad", names="Estado", 
                          color="Estado",
                          color_discrete_map={
                              "Construida": "#28a745", 
                              "En construcción": "#ffc107", 
                              "Sin construir": "#dc3545"
                          },
                          hole=0.4, title="Distribución Porcentual")
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            st.markdown("#### Resumen Numérico")
            st.dataframe(df_kpi1, hide_index=True, use_container_width=True)
            total_pruebas = df_kpi1["Cantidad"].sum()
            st.metric("Total Banco de Pruebas", f"{total_pruebas} Materias")

    # =========================================================================
    # KPI 2: CANTIDAD DE PRUEBAS REALIZADAS POR DOCENTE
    # =========================================================================
    elif kpi_seleccionado.startswith("2."):
        st.subheader("📌 Pruebas Construidas por Docente")
        st.caption("Nota: Este indicador contabiliza únicamente las pruebas cuyo estado es 'Construida'.")

        # Query cruzando profesores con maestro_pruebas (asumiendo enlace por id_profesor)
        query = """
            SELECT p.nombre_completo, COUNT(m.alfa_asignatura) as total
            FROM profesores p
            LEFT JOIN maestro_pruebas m ON p.id_professor = m.id_profesor_programacion_pruebas
            WHERE m.estado = 'Construida'
            GROUP BY p.nombre_completo
            ORDER BY total DESC
        """
        # Nota: Ajusté provisionalmente el JOIN según las columnas comunes de tus capturas. 
        # Si arroja vacío o no encuentra relación, mostramos el aviso preventivo.
        try:
            datos = traer_datos(query)
        except:
            datos = None

        if datos:
            df_kpi2 = pd.DataFrame(datos, columns=["Docente", "Pruebas Listas"])
            
            fig2 = px.bar(df_kpi2, x="Docente", y="Pruebas Listas", 
                          text="Pruebas Listas", title="Ranking de Construcción",
                          color_discrete_sequence=["#0056b3"])
            st.plotly_chart(fig2, use_container_width=True)
            st.dataframe(df_kpi2, hide_index=True, use_container_width=True)
        else:
            st.warning("⚠️ Sin resultados acumulados. Actualmente no hay pruebas asociadas a docentes que hayan cambiado al estado de 'Construida'.")

    # =========================================================================
    # KPI 3: ASIGNATURAS SOLICITADAS VS PROGRAMADAS
    # =========================================================================
    elif kpi_seleccionado.startswith("3."):
        st.subheader("📌 Cobertura de Planificación Académica")
        
        # Solicitadas (Total de alfas únicas requeridas en la tabla estudiantes)
        res_solicitadas = traer_datos("SELECT alfa_asignatura FROM estudiantes")
        alfas_solicitadas = set()
        if res_solicitadas:
            for row in res_solicitadas:
                if row[0]:
                    alfas_solicitadas.update([a.strip() for a in row[0].split(",") if a.strip()])
        cant_solicitadas = len(alfas_solicitadas)

        # Programadas (Total de alfas únicas en programacion_pruebas)
        res_programadas = traer_datos("SELECT COUNT(DISTINCT alfa_asignatura) FROM programacion_pruebas")
        cant_programadas = res_programadas[0][0] if res_programadas else 0

        df_kpi3 = pd.DataFrame({
            "Métrica": ["Asignaturas Solicitadas", "Asignaturas Programadas"],
            "Cantidad": [cant_solicitadas, cant_programadas]
        })

        col1, col2 = st.columns([2, 1])
        with col1:
            fig3 = px.bar(df_kpi3, x="Métrica", y="Cantidad", color="Métrica",
                          text="Cantidad", color_discrete_sequence=["#17a2b8", "#6c757d"])
            st.plotly_chart(fig3, use_container_width=True)
        with col2:
            st.markdown("#### Brecha de Cobertura")
            st.dataframe(df_kpi3, hide_index=True, use_container_width=True)
            porcentaje_cobertura = int((cant_programadas / cant_solicitadas * 100)) if cant_solicitadas > 0 else 0
            st.metric("Índice de Cumplimiento", f"{porcentaje_cobertura}%")

    # =========================================================================
    # KPI 4: CONTROL DE ASISTENCIA A PRUEBAS
    # =========================================================================
    elif kpi_seleccionado.startswith("4."):
        st.subheader("📌 Balance de Asistencia en el Aula")
        
        query = "SELECT asistencia, COUNT(*) FROM notas GROUP BY asistencia"
        datos = traer_datos(query)
        
        asistencia_base = {"Asistió (SÍ)": 0, "No Asistió (NO)": 0}
        if datos:
            for asist, cant in datos:
                if asist == True:
                    asistencia_base["Asistió (SÍ)"] = cant
                elif asist == False:
                    asistencia_base["No Asistió (NO)"] = cant

        df_kpi4 = pd.DataFrame(list(asistencia_base.items()), columns=["Condición", "Estudiantes"])

        col1, col2 = st.columns([2, 1])
        with col1:
            fig4 = px.pie(df_kpi4, values="Estudiantes", names="Condición", 
                          color="Condición", color_discrete_map={"Asistió (SÍ)": "#20c997", "No Asistió (NO)": "#6c757d"},
                          title="Asistencia General")
            st.plotly_chart(fig4, use_container_width=True)
        with col2:
            st.markdown("#### Tabla de Control")
            st.dataframe(df_kpi4, hide_index=True, use_container_width=True)
            total_convocados = df_kpi4["Estudiantes"].sum()
            st.metric("Total Convocados Evaluados", f"{total_convocados} alumnos")

    # =========================================================================
    # KPI 5: SUGERIDO - TASA DE APROBACIÓN
    # =========================================================================
    elif kpi_seleccionado.startswith("5."):
        st.subheader("📌 Tasa de Rendimiento y Aprobación")
        st.caption("Sugerencia de Control Académico: Evalúa el éxito cuantitativo de las pruebas aplicadas.")

        query = "SELECT resultado, COUNT(*) FROM notas WHERE resultado != 'INASISTENCIA' GROUP BY resultado"
        datos = traer_datos(query)
        
        resultados_base = {"APROBÓ": 0, "REPROBÓ": 0}
        if datos:
            for res, cant in datos:
                if res in resultados_base:
                    resultados_base[res] = cant

        df_kpi5 = pd.DataFrame(list(resultados_base.items()), columns=["Dictamen", "Casos"])

        col1, col2 = st.columns([2, 1])
        with col1:
            fig5 = px.bar(df_kpi5, x="Dictamen", y="Casos", color="Dictamen",
                          text="Casos", color_discrete_map={"APROBÓ": "#28a745", "REPROBÓ": "#dc3545"})
            st.plotly_chart(fig5, use_container_width=True)
        with col2:
            st.markdown("#### Histórico de Notas")
            st.dataframe(df_kpi5, hide_index=True, use_container_width=True)
            total_presentados = df_kpi5["Casos"].sum()
            aprobados = resultados_base["APROBÓ"]
            
            tasa_exito = int((aprobados / total_presentados * 100)) if total_presentados > 0 else 0
            st.metric("Tasa de Éxito Académico", f"{tasa_exito}%")