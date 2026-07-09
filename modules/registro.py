import streamlit as st
from database import traer_datos
# CAMBIO CLAVE: Usamos el punto (.) para importar desde la misma carpeta
from modules import gestion_docentes, gestion_estudiantes, vista_maestra

def render():
    # Inicializar estado de navegación
    if 'reg_vista' not in st.session_state:
        st.session_state['reg_vista'] = "dashboard"

    # Redirección según estado
    if st.session_state['reg_vista'] == "dashboard":
        render_dashboard()
    elif st.session_state['reg_vista'] == "docentes":
        gestion_docentes.render()
    elif st.session_state['reg_vista'] == "estudiantes":
        gestion_estudiantes.render()
    elif st.session_state['reg_vista'] == "maestra":
        vista_maestra.render()

def render_dashboard():
    # --- CSS DE ALTA FIDELIDAD ---
    st.markdown("""<style>
        .stApp { background-color: #f8fafc !important; }
        .dashboard-container { max-width: 1400px; margin: auto; padding: 20px; font-family: 'Inter', sans-serif; }
        .action-cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 30px; }
        .action-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 30px; display: flex; flex-direction: column; align-items: center; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.03); }
        .card-icon { font-size: 3.5rem; margin-bottom: 20px; }
        .card-title { font-weight: 800; font-size: 1.3rem; color: #0f172a; margin-bottom: 12px; }
        .card-desc { font-size: 0.95rem; color: #64748b; margin-bottom: 25px; line-height: 1.6; }
        .metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .metric-card { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 25px; }
        .metric-val { font-size: 2.5rem; font-weight: 800; color: #0f172a; margin-top: 5px; }
        .metric-lbl { font-size: 1rem; font-weight: 600; color: #64748b; }
        .bottom-split { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
        .card-box { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 25px; }
        .panel-card-title { font-size: 1.2rem; font-weight: 700; color: #0f172a; margin-bottom: 20px; }
        .timeline-wrapper { position: relative; padding-left: 10px; }
        .timeline-line { position: absolute; left: 16px; top: 10px; bottom: 10px; width: 2px; background: #e2e8f0; z-index: 0; }
        .timeline-item { position: relative; margin-bottom: 20px; display: flex; align-items: start; z-index: 1; }
        .timeline-dot { width: 12px; height: 12px; border-radius: 50%; margin-top: 5px; margin-right: 18px; flex-shrink: 0; }
    </style>""", unsafe_allow_html=True)

    # --- DATOS ---
    try:
        tot_est = traer_datos("SELECT COUNT(*) FROM estudiantes")[0][0]
        tot_prof = traer_datos("SELECT COUNT(*) FROM profesores")[0][0]
        tot_pend = traer_datos("SELECT COUNT(*) FROM estado_pruebas")[0][0]
        tot_asig = traer_datos("SELECT COUNT(*) FROM asignaturas")[0][0]
        actividades = traer_datos("SELECT tipo, fecha, descripcion FROM historial_actividad ORDER BY fecha DESC LIMIT 3")
    except:
        tot_est=tot_prof=tot_pend=tot_asig=0
        actividades = []

    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 2.2rem; font-weight: 800; color: #0f172a; margin-bottom: 25px;">Gestión de Registros</h1>', unsafe_allow_html=True)

    # --- TARJETAS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="action-card"><div class="card-icon">🎓</div><div class="card-title">Docentes evaluadores</div><div class="card-desc">Gestiona los docentes del proceso RAP.</div>', unsafe_allow_html=True)
        if st.button("Gestionar docentes", use_container_width=True, type="primary"):
            st.session_state['reg_vista'] = "docentes"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="action-card"><div class="card-icon">👤</div><div class="card-title">Estudiantes</div><div class="card-desc">Gestiona estudiantes del proceso RAP.</div>', unsafe_allow_html=True)
        if st.button("Gestionar estudiantes", use_container_width=True, type="primary"):
            st.session_state['reg_vista'] = "estudiantes"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="action-card"><div class="card-icon">👁️</div><div class="card-title">Vista maestra</div><div class="card-desc">Consulta resultados RAP.</div>', unsafe_allow_html=True)
        if st.button("Abrir vista maestra", use_container_width=True, type="primary"):
            st.session_state['reg_vista'] = "maestra"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- MÉTRICAS Y TIMELINE ---
    # ... (Aquí insertas el código de las métricas y la actividad como lo tenías)
    st.markdown('</div>', unsafe_allow_html=True)