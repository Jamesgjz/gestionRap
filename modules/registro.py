import streamlit as st
from database import traer_datos

def render():
    # --- CSS DE ALTA FIDELIDAD ---
    st.markdown("""
<style>
/* Reset de fondo */
.stApp { background-color: #f8fafc !important; }

/* Contenedor principal */
.dashboard-container { max-width: 1400px; margin: auto; padding: 20px; font-family: 'Inter', sans-serif; }

/* Grid de tarjetas de acción */
.action-cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 30px; }
.action-card { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 30px; display: flex; flex-direction: column; align-items: center; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.03); }
.card-icon { font-size: 3.5rem; margin-bottom: 20px; }
.card-title { font-weight: 800; font-size: 1.3rem; color: #0f172a; margin-bottom: 12px; }
.card-desc { font-size: 0.95rem; color: #64748b; margin-bottom: 25px; line-height: 1.6; }

/* Botones */
.btn-docentes { background-color: #0047ff !important; color: white !important; width: 100%; padding: 14px; border-radius: 8px; border: none; font-weight: 700; font-size: 1rem; cursor: pointer; }
.btn-estudiantes { background-color: #00875a !important; color: white !important; width: 100%; padding: 14px; border-radius: 8px; border: none; font-weight: 700; font-size: 1rem; cursor: pointer; }
.btn-maestra { background-color: #6b21a8 !important; color: white !important; width: 100%; padding: 14px; border-radius: 8px; border: none; font-weight: 700; font-size: 1rem; cursor: pointer; }

/* Métricas */
.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
.metric-card { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 25px; }
.metric-val { font-size: 2.5rem; font-weight: 800; color: #0f172a; margin-top: 5px; }
.metric-lbl { font-size: 1rem; font-weight: 600; color: #64748b; }

/* Split inferior */
.bottom-split { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.card-box { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 25px; }
.panel-card-title { font-size: 1.2rem; font-weight: 700; color: #0f172a; margin-bottom: 20px; }

/* Línea de tiempo */
.timeline-wrapper { position: relative; padding-left: 10px; }
.timeline-line { position: absolute; left: 16px; top: 10px; bottom: 10px; width: 2px; background: #e2e8f0; z-index: 0; }
.timeline-item { position: relative; margin-bottom: 20px; display: flex; align-items: flex-start; z-index: 1; }
.timeline-dot { width: 12px; height: 12px; border-radius: 50%; margin-top: 5px; margin-right: 18px; flex-shrink: 0; }
</style>
""", unsafe_allow_html=True)

    # --- LÓGICA DE DATOS DINÁMICA ---
    try:
        tot_est = traer_datos("SELECT COUNT(*) FROM estudiantes")[0][0]
        tot_prof = traer_datos("SELECT COUNT(*) FROM profesores")[0][0]
        tot_pend = traer_datos("SELECT COUNT(*) FROM estado_pruebas")[0][0]
        tot_asig = traer_datos("SELECT COUNT(*) FROM asignaturas")[0][0]
        
        # Consulta de actividad reciente (Asegúrate de que la tabla 'historial_actividad' exista)
        actividades = traer_datos("SELECT tipo, fecha, descripcion FROM historial_actividad ORDER BY fecha DESC LIMIT 3")
    except:
        tot_est, tot_prof, tot_pend, tot_asig = 0, 0, 0, 0
        actividades = []

    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Cabecera
    st.markdown('<h1 style="font-size: 2.2rem; font-weight: 800; color: #0f172a; margin-bottom: 25px;">Gestión de Registros</h1>', unsafe_allow_html=True)

    # Tarjetas de Acción
    st.markdown("""<div class="action-cards-grid">
        <div class="action-card">
            <div class="card-icon">🎓</div>
            <div class="card-title">Docentes evaluadores</div>
            <div class="card-desc">Registra, actualiza y gestiona los docentes que participan en el proceso RAP.</div>
            <button class="btn-docentes">Gestionar docentes</button>
        </div>
        <div class="action-card">
            <div class="card-icon">👤</div>
            <div class="card-title">Estudiantes</div>
            <div class="card-desc">Registra, actualiza y gestiona los estudiantes del proceso RAP y consulta su estado de aplicación.</div>
            <button class="btn-estudiantes">Gestionar estudiantes</button>
        </div>
        <div class="action-card">
            <div class="card-icon">👁️</div>
            <div class="card-title">Vista maestra</div>
            <div class="card-desc">Consulta el estado de aplicación por estudiante, asignaturas y resultados del proceso RAP.</div>
            <button class="btn-maestra">Abrir vista maestra</button>
        </div>
    </div>""", unsafe_allow_html=True)

    # Métricas
    st.markdown(f"""<div class="metrics-grid">
        <div class="metric-card"><div class="metric-lbl">Total estudiantes</div><div class="metric-val">{tot_est}</div></div>
        <div class="metric-card"><div class="metric-lbl">Docentes evaluadores</div><div class="metric-val">{tot_prof}</div></div>
        <div class="metric-card"><div class="metric-lbl">Pendientes de gestión</div><div class="metric-val">{tot_pend}</div></div>
        <div class="metric-card"><div class="metric-lbl">Asignaturas activas</div><div class="metric-val">{tot_asig}</div></div>
    </div>""", unsafe_allow_html=True)

    # Actividad Reciente (Timeline Dinámico)
    html_timeline = ""
    for act in actividades:
        tipo, fecha, desc = act
        color = "#00875a" if tipo == "estudiante" else "#0047ff"
        html_timeline += f"""
        <div class="timeline-item">
            <div class="timeline-dot" style="background:{color};"></div>
            <div class="timeline-content"><b>{tipo.capitalize()}</b><br><small style="color:#64748b;">{fecha}</small><br>{desc}</div>
        </div>"""

    st.markdown(f"""<div class="bottom-split">
        <div class="card-box">
            <div class="panel-card-title">Actividad reciente</div>
            <div class="timeline-wrapper">
                <div class="timeline-line"></div>
                {html_timeline if html_timeline else "No hay actividad reciente."}
            </div>
        </div>
        <div class="card-box">
            <div class="panel-card-title">Accesos rápidos</div>
            <div style="border: 1px solid #e2e8f0; padding: 16px; border-radius: 10px; margin-bottom: 15px; font-weight:500;">✅ Validar documentos de estudiantes</div>
            <div style="border: 1px solid #e2e8f0; padding: 16px; border-radius: 10px; margin-bottom: 15px; font-weight:500;">📅 Programar prueba por asignatura</div>
        </div>
    </div>""", unsafe_allow_html=True)