import streamlit as st
from database import traer_datos
from html import escape
from importlib import import_module


def ir_a(vista):
    st.session_state["reg_vista"] = vista


def render():
    # --- CSS DE ALTA FIDELIDAD ---
    st.markdown("""
<style>
.stApp { background-color: #f8fafc !important; }
.dashboard-container { max-width: 1400px; margin: auto; padding: 20px; font-family: 'Inter', sans-serif; }
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
.card-title { font-weight: 800; font-size: 1.55rem; color: #0f172a; margin-bottom: 14px; }
.card-desc { font-size: 1.1rem; color: #64748b; line-height: 1.6; min-height: 85px; }

/* Botones Maximizados (Texto 1.65rem y Padding 24px) */
[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton button {
    background-color: #0047ff !important; color: white !important; font-size: 1.65rem !important; font-weight: 700 !important; padding: 24px !important; border-radius: 0px 0px 16px 16px !important; border: 1px solid #0047ff !important; border-top: none !important; width: 100% !important;
}
[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton button {
    background-color: #00875a !important; color: white !important; font-size: 1.65rem !important; font-weight: 700 !important; padding: 24px !important; border-radius: 0px 0px 16px 16px !important; border: 1px solid #00875a !important; border-top: none !important; width: 100% !important;
}
[data-testid="stHorizontalBlock"] > div:nth-child(3) .stButton button {
    background-color: #6b21a8 !important; color: white !important; font-size: 1.65rem !important; font-weight: 700 !important; padding: 24px !important; border-radius: 0px 0px 16px 16px !important; border: 1px solid #6b21a8 !important; border-top: none !important; width: 100% !important;
}
[data-testid="stHorizontalBlock"] .stButton { margin-top: -1px; }
.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 35px; margin-top: 40px; }
.metric-card { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 25px; }
.metric-val { font-size: 3rem; font-weight: 800; color: #0f172a; margin-top: 5px; }
.metric-lbl { font-size: 1.1rem; font-weight: 600; color: #64748b; }
.bottom-split { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.card-box { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 28px; }
.panel-card-title { font-size: 1.35rem; font-weight: 700; color: #0f172a; margin-bottom: 22px; }
.timeline-wrapper { position: relative; padding-left: 10px; }
.timeline-line { position: absolute; left: 16px; top: 10px; bottom: 10px; width: 2px; background: #e2e8f0; z-index: 0; }
.timeline-item { position: relative; margin-bottom: 20px; display: flex; align-items: start; z-index: 1; }
.timeline-dot { width: 12px; height: 12px; border-radius: 50%; margin-top: 5px; margin-right: 18px; flex-shrink: 0; }
.timeline-content { font-size: 1.1rem; color: #334155; }
.acceso-rapido-item { border: 1px solid #e2e8f0; padding: 18px; border-radius: 10px; margin-bottom: 15px; font-weight: 500; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

    if 'reg_vista' not in st.session_state:
        st.session_state['reg_vista'] = "dashboard"

    if message := st.session_state.pop("registro_guardado", None):
        st.success(message)

    # --- ENRUTADOR INTERNO RAP ---
    if st.session_state['reg_vista'] == "dashboard":
        tot_est, tot_prof, tot_pend, tot_asig = traer_datos("""
            SELECT (SELECT COUNT(*) FROM estudiantes),
                   (SELECT COUNT(*) FROM profesores),
                   (SELECT COUNT(*) FROM maestro_pruebas WHERE lower(trim(estado)) IN ('en construcción', 'en construccion')),
                   (SELECT COUNT(*) FROM asignaturas)
        """)[0]
        actividades = []
        if traer_datos("SELECT to_regclass('historial_actividad')")[0][0]:
            actividades = traer_datos(
                "SELECT tipo, fecha, descripcion FROM historial_actividad ORDER BY fecha DESC LIMIT 3"
            )

        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<h1 style="font-size: 2.5rem; font-weight: 800; color: #0f172a; margin-bottom: 30px;">Gestión de Registros</h1>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="action-card"><div class="card-icon">🎓</div><div class="card-title">Docentes evaluadores</div><div class="card-desc">Registra, actualiza y gestiona los docentes que participan en el proceso RAP.</div></div>', unsafe_allow_html=True)
            st.button("Gestionar docentes", width="stretch", key="nav_doc_btn", on_click=ir_a, args=("docentes",))
        with col2:
            st.markdown('<div class="action-card"><div class="card-icon">👤</div><div class="card-title">Estudiantes</div><div class="card-desc">Registra, actualiza y gestiona los estudiantes del proceso RAP y consulta su estado de aplicación.</div></div>', unsafe_allow_html=True)
            st.button("Gestionar estudiantes", width="stretch", key="nav_est_btn", on_click=ir_a, args=("estudiantes",))
        with col3:
            st.markdown('<div class="action-card"><div class="card-icon">👁️</div><div class="card-title">Vista maestra</div><div class="card-desc">Consulta el estado de aplicación por estudiante, asignaturas y resultados del proceso RAP.</div></div>', unsafe_allow_html=True)
            st.button("Abrir vista maestra", width="stretch", key="nav_mae_btn", on_click=ir_a, args=("maestra",))

        # Métricas
        st.markdown(f"""<div class="metrics-grid">
            <div class="metric-card"><div class="metric-lbl">Total estudiantes</div><div class="metric-val">{tot_est}</div></div>
            <div class="metric-card"><div class="metric-lbl">Docentes evaluadores</div><div class="metric-val">{tot_prof}</div></div>
            <div class="metric-card"><div class="metric-lbl">Pendientes de gestión</div><div class="metric-val">{tot_pend}</div></div>
            <div class="metric-card"><div class="metric-lbl">Asignaturas activas</div><div class="metric-val">{tot_asig}</div></div>
        </div>""", unsafe_allow_html=True)

        # Timeline
        html_timeline = ""
        if actividades:
            for tipo, fecha, desc in actividades:
                color = "#00875a" if "estudiante" in str(tipo).lower() else "#0047ff"
                html_timeline += f'<div class="timeline-item"><div class="timeline-dot" style="background:{color};"></div><div class="timeline-content"><b>{escape(str(tipo))}</b><br><small style="color:#64748b;">{escape(str(fecha))}</small><br>{escape(str(desc))}</div></div>'
        else:
            html_timeline = "<p style='color:#64748b; font-size:1.1rem;'>No hay actividad reciente registrada en la base de datos.</p>"

        st.markdown(f"""<div class="bottom-split">
            <div class="card-box">
                <div class="panel-card-title">Actividad reciente</div>
                <div class="timeline-wrapper"><div class="timeline-line"></div>{html_timeline}</div>
            </div>
        </div></div>""", unsafe_allow_html=True)

    else:
        module = {
            "docentes": "gestion_docentes",
            "estudiantes": "gestion_estudiantes",
            "maestra": "vista_maestra",
            "nuevo_docente": "nuevo_docente",
        }[st.session_state["reg_vista"]]
        import_module(f"modules.{module}").render()
