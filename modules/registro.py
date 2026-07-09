import streamlit as st
from database import traer_datos
import os
import importlib.util

def render():
    # --- CARGA SEGURA POR RUTA FÍSICA PARA STREAMLIT CLOUD ---
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    
    def cargar_modulo_por_archivo(nombre_modulo, nombre_archivo):
        ruta_completa = os.path.join(dir_actual, nombre_archivo)
        if not os.path.exists(ruta_completa):
            st.error(f"❌ No se encontró el archivo '{nombre_archivo}' en la ruta: {dir_actual}.")
            st.stop()
        spec = importlib.util.spec_from_file_location(nombre_modulo, ruta_completa)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        return modulo

    # Carga dinámica de los módulos independientes
    gestion_docentes = cargar_modulo_por_archivo("gestion_docentes", "gestion_docentes.py")
    gestion_estudiantes = cargar_modulo_por_archivo("gestion_estudiantes", "gestion_estudiantes.py")
    vista_maestra = cargar_modulo_por_archivo("vista_maestra", "vista_maestra.py")

    # --- CSS DE ALTA FIDELIDAD: FUENTES INCREMENTADAS ---
    st.markdown("""
<style>
/* Reset de fondo */
.stApp { background-color: #f8fafc !important; }

/* Contenedor principal */
.dashboard-container { max-width: 1400px; margin: auto; padding: 20px; font-family: 'Inter', sans-serif; }

/* Tarjetas de acción superiores */
.action-card { 
    background: white; 
    border: 1px solid #e2e8f0; 
    border-top-left-radius: 16px; 
    border-top-right-radius: 16px; 
    padding: 35px 30px 25px 30px; 
    display: flex; 
    flex-direction: column; 
    align-items: center; 
    text-align: center; 
    border-bottom: none !important;
}
.card-icon { font-size: 3.8rem; margin-bottom: 20px; }
.card-title { font-weight: 800; font-size: 1.55rem !important; color: #0f172a; margin-bottom: 14px; }
.card-desc { font-size: 1.1rem !important; color: #64748b; line-height: 1.6; min-height: 85px; }

/* --- ESTILIZADO DE BOTONES NATIVOS CON FUENTE MÁS GRANDE (1.35rem) --- */
/* Columna 1: Gestión Docentes (Azul) */
[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton button {
    background-color: #0047ff !important;
    color: white !important;
    font-size: 1.35rem !important; /* Letra significativamente más grande */
    font-weight: 700 !important;
    padding: 18px !important; /* Botón con mayor altura */
    border-radius: 0px 0px 16px 16px !important;
    border: 1px solid #0047ff !important;
    border-top: none !important;
    width: 100% !important;
}
[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton button:hover {
    background-color: #0036d6 !important;
}

/* Columna 2: Gestión Estudiantes (Verde) */
[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton button {
    background-color: #00875a !important;
    color: white !important;
    font-size: 1.35rem !important; /* Letra significativamente más grande */
    font-weight: 700 !important;
    padding: 18px !important; /* Botón con mayor altura */
    border-radius: 0px 0px 16px 16px !important;
    border: 1px solid #00875a !important;
    border-top: none !important;
    width: 100% !important;
}
[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton button:hover {
    background-color: #006c48 !important;
}

/* Columna 3: Vista Maestra (Morado) */
[data-testid="stHorizontalBlock"] > div:nth-child(3) .stButton button {
    background-color: #6b21a8 !important;
    color: white !important;
    font-size: 1.35rem !important; /* Letra significativamente más grande */
    font-weight: 700 !important;
    padding: 18px !important; /* Botón con mayor altura */
    border-radius: 0px 0px 16px 16px !important;
    border: 1px solid #6b21a8 !important;
    border-top: none !important;
    width: 100% !important;
}
[data-testid="stHorizontalBlock"] > div:nth-child(3) .stButton button:hover {
    background-color: #551a87 !important;
}

[data-testid="stHorizontalBlock"] .stButton {
    margin-top: -1px;
}

/* Métricas Ampliadas */
.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 35px; margin-top: 40px; }
.metric-card { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 25px; }
.metric-val { font-size: 3rem; font-weight: 800; color: #0f172a; margin-top: 5px; }
.metric-lbl { font-size: 1.1rem; font-weight: 600; color: #64748b; }

/* Split inferior */
.bottom-split { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.card-box { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 28px; }
.panel-card-title { font-size: 1.35rem; font-weight: 700; color: #0f172a; margin-bottom: 22px; }

/* Línea de tiempo y accesos rápidos */
.timeline-wrapper { position: relative; padding-left: 10px; }
.timeline-line { position: absolute; left: 16px; top: 10px; bottom: 10px; width: 2px; background: #e2e8f0; z-index: 0; }
.timeline-item { position: relative; margin-bottom: 20px; display: flex; align-items: start; z-index: 1; }
.timeline-dot { width: 12px; height: 12px; border-radius: 50%; margin-top: 5px; margin-right: 18px; flex-shrink: 0; }
.timeline-content { font-size: 1.1rem; color: #334155; }
.acceso-rapido-item { border: 1px solid #e2e8f0; padding: 18px; border-radius: 10px; margin-bottom: 15px; font-weight: 500; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

    # Inicializar estado de navegación interna si no existe
    if 'reg_vista' not in st.session_state:
        st.session_state['reg_vista'] = "dashboard"

    # --- ENRUTADOR INTERNO RAP ---
    if st.session_state['reg_vista'] == "dashboard":
        
        # --- LÓGICA DE DATOS OPTIMIZADA ---
        tot_est = 0
        tot_prof = 0
        tot_pend = 0
        tot_asig = 0
        actividades = []

        try:
            db_est = traer_datos("SELECT COUNT(*) FROM estudiantes")
            if db_est: tot_est = db_est[0][0]
                
            db_prof = traer_datos("SELECT COUNT(*) FROM profesores")
            if db_prof: tot_prof = db_prof[0][0]
                
            db_pend = traer_datos("SELECT COUNT(*) FROM estado_pruebas")
            if db_pend: tot_pend = db_pend[0][0]
                
            db_asig = traer_datos("SELECT COUNT(*) FROM asignaturas")
            if db_asig: tot_asig = db_asig[0][0]
                
            actividades = traer_datos("SELECT tipo, fecha, descripcion FROM historial_actividad ORDER BY fecha DESC LIMIT 3")
        except Exception as db_error:
            st.sidebar.error(f"Aviso de Base de Datos: {db_error}")

        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<h1 style="font-size: 2.5rem; font-weight: 800; color: #0f172a; margin-bottom: 30px;">Gestión de Registros</h1>', unsafe_allow_html=True)

        # --- GRID DE TARJETAS CON BOTONES AMPLIADOS ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div class="action-card">
                <div class="card-icon">🎓</div>
                <div class="card-title">Docentes evaluadores</div>
                <div class="card-desc">Registra, actualiza y gestiona los docentes que participan en el proceso RAP.</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Gestionar docentes", use_container_width=True, key="nav_doc_btn"):
                st.session_state['reg_vista'] = "docentes"
                st.rerun()

        with col2:
            st.markdown("""<div class="action-card">
                <div class="card-icon">👤</div>
                <div class="card-title">Estudiantes</div>
                <div class="card-desc">Registra, actualiza y gestiona los estudiantes del proceso RAP y consulta su estado de aplicación.</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Gestionar estudiantes", use_container_width=True, key="nav_est_btn"):
                st.session_state['reg_vista'] = "estudiantes"
                st.rerun()

        with col3:
            st.markdown("""<div class="action-card">
                <div class="card-icon">👁️</div>
                <div class="card-title">Vista maestra</div>
                <div class="card-desc">Consulta el estado de aplicación por estudiante, asignaturas y resultados del proceso RAP.</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Abrir vista maestra", use_container_width=True, key="nav_mae_btn"):
                st.session_state['reg_vista'] = "maestra"
                st.rerun()

        # --- SECCIÓN DE MÉTRICAS ---
        st.markdown(f"""<div class="metrics-grid">
            <div class="metric-card"><div class="metric-lbl">Total estudiantes</div><div class="metric-val">{tot_est}</div></div>
            <div class="metric-card"><div class="metric-lbl">Docentes evaluadores</div><div class="metric-val">{tot_prof}</div></div>
            <div class="metric-card"><div class="metric-lbl">Pendientes de gestión</div><div class="metric-val">{tot_pend}</div></div>
            <div class="metric-card"><div class="metric-lbl">Asignaturas activas</div><div class="metric-val">{tot_asig}</div></div>
        </div>""", unsafe_allow_html=True)

        # --- SECCIÓN DE LÍNEA DE TIEMPO REAL ---
        html_timeline = ""
        if actividades:
            for tipo, fecha, desc in actividades:
                color = "#00875a" if "estudiante" in tipo.lower() else "#0047ff"
                html_timeline += f"""
                <div class="timeline-item">
                    <div class="timeline-dot" style="background:{color};"></div>
                    <div class="timeline-content"><b>{tipo}</b><br><small style="color:#64748b;">{fecha}</small><br>{desc}</div>
                </div>"""
        else:
            html_timeline = "<p style='color:#64748b; font-size:1.1rem;'>No hay actividad reciente registrada en la base de datos.</p>"

        st.markdown(f"""<div class="bottom-split">
            <div class="card-box">
                <div class="panel-card-title">Actividad reciente</div>
                <div class="timeline-wrapper">
                    <div class="timeline-line"></div>
                    {html_timeline}
                </div>
            </div>
            <div class="card-box">
                <div class="panel-card-title">Accesos rápidos</div>
                <div class="acceso-rapido-item">✅ Validar documentos de estudiantes</div>
                <div class="acceso-rapido-item">📅 Programar prueba por asignatura</div>
            </div>
        </div></div>""", unsafe_allow_html=True)

    # Redirecciones modulares nativas
    elif st.session_state['reg_vista'] == "docentes":
        gestion_docentes.render()
    elif st.session_state['reg_vista'] == "estudiantes":
        gestion_estudiantes.render()
    elif st.session_state['reg_vista'] == "maestra":
        vista_maestra.render()