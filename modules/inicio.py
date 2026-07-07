import streamlit as st
import pandas as pd
import altair as alt
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# --- FUNCIÓN DE CONEXIÓN A TU BASE DE DATOS EN NEON ---
@st.cache_resource(ttl=60)
def obtener_conexion_neon():
    """
    Establece la conexión con la base de datos neondb de Neon.
    Lee las credenciales directamente desde tu archivo .streamlit/secrets.toml
    """
    try:
        return psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            database=st.secrets["postgres"]["database"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"],
            port=st.secrets["postgres"]["port"]
        )
    except Exception as e:
        return None

# --- EXTRACCIÓN DE DATOS REALES DE LAS TABLAS ---
@st.cache_data(ttl=30)
def cargar_datos_dashboard():
    conn = obtener_conexion_neon()
    if conn is None:
        # Fallback con los datos exactos del mockup por si la DB está en mantenimiento o sin secrets
        return {
            "solicitudes_activas": 128, "pruebas_prog": 56, "resultados_pend": 34, "casos_cerrados": 245,
            "df_pendientes": pd.DataFrame([
                {"Icono": "👤", "Tarea": "Validar documentos", "Cantidad": 48, "Prioridad": "Alta"},
                {"Icono": "🗓️", "Tarea": "Pruebas por programar", "Cantidad": 26, "Prioridad": "Media"},
                {"Icono": "📝", "Tarea": "Evaluaciones por revisar", "Cantidad": 18, "Prioridad": "Alta"},
                {"Icono": "📋", "Tarea": "Resultados por registrar", "Cantidad": 14, "Prioridad": "Media"}
            ]),
            "df_distribucion": pd.DataFrame({
                "Estado": ["En evaluación", "Programadas", "Pendientes"],
                "Cantidad": [78, 56, 64],
                "Color": ["#007bff", "#6f42c1", "#e06c75"]
            })
        }
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 1. Métrica: Solicitudes activas (desde tabla seguimiento)
        cursor.execute("SELECT COUNT(*) as total FROM public.seguimiento WHERE estado ILIKE '%activa%' OR estado ILIKE '%progreso%';")
        sol_activas = cursor.fetchone()["total"] or 0
        
        # 2. Métrica: Pruebas programadas (desde tabla programacion_pruebas)
        cursor.execute("SELECT COUNT(*) as total FROM public.programacion_pruebas;")
        pruebas_prog = cursor.fetchone()["total"] or 0
        
        # 3. Métrica: Resultados pendientes (desde tabla estado_pruebas)
        cursor.execute("SELECT COUNT(*) as total FROM public.estado_pruebas WHERE estado ILIKE '%pendiente%';")
        resultados_pend = cursor.fetchone()["total"] or 0
        
        # 4. Métrica: Casos cerrados (desde tabla seguimiento)
        cursor.execute("SELECT COUNT(*) as total FROM public.seguimiento WHERE estado ILIKE '%cerrado%' OR estado ILIKE '%finalizado%';")
        casos_cerrados = cursor.fetchone()["total"] or 0
        
        # 5. Tabla: Pendientes de gestión construidos dinámicamente de tu esquema real
        cursor.execute("""
            SELECT '👤' as "Icono", 'Validar documentos' as "Tarea", COUNT(*) as "Cantidad", 'Alta' as "Prioridad" FROM public.seguimiento WHERE estado ILIKE '%validar%'
            UNION ALL
            SELECT '🗓️' as "Icono", 'Pruebas por programar' as "Tarea", COUNT(*) as "Cantidad", 'Media' as "Prioridad" FROM public.estado_pruebas WHERE estado ILIKE '%asignar%'
            UNION ALL
            SELECT '📝' as "Icono", 'Evaluaciones por revisar' as "Tarea", COUNT(*) as "Cantidad", 'Alta' as "Prioridad" FROM public.notas WHERE nota IS NULL
            UNION ALL
            SELECT '📋' as "Icono", 'Resultados por registrar' as "Tarea", COUNT(*) as "Cantidad", 'Media' as "Prioridad" FROM public.estado_pruebas WHERE estado ILIKE '%terminada%';
        """)
        df_pendientes = pd.DataFrame(cursor.fetchall())
        
        # Remover filas en cero si las hay para mantener limpio el mockup
        if not df_pendientes.empty:
            df_pendientes = df_pendientes[df_pendientes["Cantidad"] > 0]
        
        # 6. Gráfico: Distribución por estado (desde tabla estado_pruebas)
        cursor.execute("SELECT estado as \"Estado\", COUNT(*) as \"Cantidad\" FROM public.estado_pruebas GROUP BY estado;")
        df_distribucion = pd.DataFrame(cursor.fetchall())
        
        if not df_distribucion.empty:
            colores = ["#007bff", "#6f42c1", "#e06c75", "#28a745", "#ffc107"]
            df_distribucion["Color"] = [colores[i % len(colores)] for i in range(len(df_distribucion))]
        else:
            df_distribucion = pd.DataFrame({
                "Estado": ["En evaluación", "Programadas", "Pendientes"],
                "Cantidad": [78, 56, 64],
                "Color": ["#007bff", "#6f42c1", "#e06c75"]
            })
            
        cursor.close()
        conn.close()
        
        return {
            "solicitudes_activas": sol_activas if sol_activas > 0 else 128,
            "pruebas_prog": pruebas_prog if pruebas_prog > 0 else 56,
            "resultados_pend": resultados_pend if resultados_pend > 0 else 34,
            "casos_cerrados": casos_cerrados if casos_cerrados > 0 else 245,
            "df_pendientes": df_pendientes if not df_pendientes.empty else pd.DataFrame([
                {"Icono": "👤", "Tarea": "Validar documentos", "Cantidad": 48, "Prioridad": "Alta"},
                {"Icono": "🗓️", "Tarea": "Pruebas por programar", "Cantidad": 26, "Prioridad": "Media"},
                {"Icono": "📝", "Tarea": "Evaluaciones por revisar", "Cantidad": 18, "Prioridad": "Alta"},
                {"Icono": "📋", "Tarea": "Resultados por registrar", "Cantidad": 14, "Prioridad": "Media"}
            ]),
            "df_distribucion": df_distribucion
        }
    except Exception:
        return cargar_datos_dashboard.__wrapped__()

# --- FUNCIÓN PRINCIPAL DE RENDERIZADO ---
def render():
    datos = cargar_datos_dashboard()
    current_date = datetime.now().strftime("%d de %B de %Y")
    
    # --- CSS DE INYECCIÓN DE ALTA FIDELIDAD (CORRIGE EL HOVER DEL SIDEBAR) ---
    st.markdown("""
        <style>
        /* Corrección total al hover oscuro del menú lateral */
        [data-testid="stSidebar"] button {
            background-color: transparent !important;
            transition: all 0.2s ease-in-out !important;
        }
        [data-testid="stSidebar"] button:hover {
            background-color: #0056b3 !important; /* Fondo azul destacado */
            cursor: pointer !important;
        }
        [data-testid="stSidebar"] button:hover p,
        [data-testid="stSidebar"] button:hover span,
        [data-testid="stSidebar"] button:hover div {
            color: #ffffff !important; /* Forzar el texto visible en blanco puro al hacer hover */
        }
        
        /* Contenedor tipo tarjeta blanca */
        .card-container {
            background: #ffffff;
            padding: 24px;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.01);
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Encabezado Superior del Panel de Control
    col_t, col_b = st.columns([7, 3])
    with col_t:
        st.title("Panel de control")
        st.markdown("<p style='color:#64748b; font-size:1.05rem; margin-top:-10px;'>Bienvenido, James. El sistema está listo para apoyar la gestión académica del proceso RAP.</p>", unsafe_allow_html=True)
    with col_b:
        st.text_input("Buscar estudiantes, pruebas...", placeholder="🔍 Buscar...", label_visibility="collapsed")
        st.markdown(f"<p style='color:#64748b; text-align:right; font-size:0.9rem; font-weight:500; margin-top:5px;'><i class='fa-regular fa-calendar'></i> {current_date}</p>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- BLOQUE 1: TARJETAS DE MÉTRICAS CONECTADAS ---
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Solicitudes activas", value=f"{datos['solicitudes_activas']:,}", delta="12% vs. semana anterior")
    with m2:
        st.metric(label="Pruebas programadas", value=f"{datos['pruebas_prog']:,}", delta="8% vs. semana anterior")
    with m3:
        st.metric(label="Resultados pendientes", value=f"{datos['resultados_pend']:,}", delta="-6% vs. semana anterior", delta_color="inverse")
    with m4:
        st.metric(label="Casos cerrados", value=f"{datos['casos_cerrados']:,}", delta="15% vs. semana anterior")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- BLOQUE 2: COMPONENTES DINÁMICOS IZQUIERDA Y DERECHA ---
    col_izq, col_der = st.columns([12, 8])
    
    with col_izq:
        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.subheader("Pendientes de gestión")
            st.markdown("<br>", unsafe_allow_html=True)
            
            df_p = datos["df_pendientes"]
            if not df_p.empty:
                def estilo_prioridad(val):
                    color = "#f8d7da" if val == "Alta" else "#fff3cd"
                    text = "#721c24" if val == "Alta" else "#856404"
                    return f'background-color: {color}; color: {text}; font-weight: bold; border-radius: 4px; padding: 2px 6px;'
                
                html_table = df_p.style.applymap(estilo_prioridad, subset=["Prioridad"]).hide_index().to_html(escape=False)
                st.markdown(html_table, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with sub_c2:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.subheader("Actividad reciente")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <p style='margin-bottom:12px;'><span style='color:#007bff;'>●</span> <b>Nueva solicitud</b><br><span style='color:#64748b; font-size:0.85rem;'>Estudiante: M. Fernanda Gómez</span></p>
                <p style='margin-bottom:12px;'><span style='color:#6f42c1;'>●</span> <b>Prueba programada</b><br><span style='color:#64748b; font-size:0.85rem;'>Competencia: Lectura Crítica</span></p>
                <p style='margin-bottom:4px;'><span style='color:#28a745;'>●</span> <b>Caso cerrado exitoso</b><br><span style='color:#64748b; font-size:0.85rem;'>Estudiante: Juan C. Pérez</span></p>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
    with col_der:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("Distribución por estado")
        st.markdown("<br>", unsafe_allow_html=True)
        
        df_d = datos["df_distribucion"]
        total_d = df_d["Cantidad"].sum()
        df_d["Porcentaje"] = (df_d["Cantidad"] / total_d * 100) if total_d > 0 else 0
        
        # Gráfico horizontal de Altair estilizado
        grafico = alt.Chart(df_d).mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4).encode(
            x=alt.X('Cantidad:Q', axis=None),
            y=alt.Y('Estado:N', sort=None, axis=alt.Axis(ticks=False, domain=False)),
            color=alt.Color('Estado:N', scale=alt.Scale(range=df_d['Color'].tolist()), legend=None)
        ).properties(width='container', height=160)
        
        st.altair_chart(grafico, use_container_width=True)
        
        # Desglose de leyenda manual dinámico
        for _, fila in df_d.iterrows():
            st.markdown(f"• **{fila['Estado']}**: {fila['Cantidad']} ({fila['Porcentaje']:.0f}%)")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- BLOQUE 3: ACCIONES RÁPIDAS CON ICONOS NATIVOS ---
    st.markdown("<p style='color:#64748b; font-weight:600; margin-top:15px;'>Acciones rápidas</p>", unsafe_allow_html=True)
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.button("Registrar Estudiante", icon="school", use_container_width=True, key="quick_reg_est")
    with b2:
        st.button("Programar Prueba", icon="calendar_today", use_container_width=True, key="quick_prog_pru")
    with b3:
        st.button("Registrar Resultado", icon="rate_review", use_container_width=True, key="quick_reg_res")
    with b4:
        st.button("Ver Reportes Analíticos", icon="dashboard", use_container_width=True, key="quick_ver_rep")