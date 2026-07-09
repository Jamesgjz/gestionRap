import streamlit as st
from database import traer_datos
import sys
import os

def render():
    # --- INYECTOR DE RUTAS ABSOLUTAS PARA EVITAR FALLOS EN STREAMLIT CLOUD ---
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    if dir_actual not in sys.path:
        sys.path.append(dir_actual)
    
    # Importación directa asegurada por el entorno de ejecución
    import gestion_docentes
    import gestion_estudiantes
    import vista_maestra

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
.timeline-item { position: relative; margin-bottom: 20px; display: flex; align-items: start; z-index: 1; }
.timeline-dot { width: 12px; height: 12px; border-radius: 50%; margin-top: 5px; margin-right: 18px; flex-shrink: 0; }
.timeline-content { font-size: 1rem; color: #334155; }
</style>
""", unsafe_allow_html=True)

    # Inicializar estado de navegación interna si no existe
    if 'reg_vista' not in st.session_state:
        st.session_state['reg_vista'] = "dashboard"

    # --- ENRUTADOR INTERNO RAP ---
    if st.session_state['reg_vista'] == "dashboard":
        # Lógica de datos dinámica desde la base de datos
        try:
            tot_est = traer_datos("SELECT COUNT(*) FROM estudiantes")[0][0]
            tot_prof = traer_datos("SELECT COUNT(*) FROM profesores")[0][0]
            tot_pend = traer_datos("SELECT COUNT(*) FROM estado_pruebas")[0][0]
            tot_asig = traer_datos("SELECT COUNT(*) FROM asignaturas")[0][0]
            actividades = traer_datos("SELECT tipo, fecha, descripcion FROM historial_actividad ORDER BY fecha DESC LIMIT 3")
        except:
            tot_est = tot_prof = tot_pend = tot_asig = 0
            actividades = []

        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<h1 style="font-size: 2.2rem; font-weight: 800; color: #0f172a; margin-bottom: 25px;">Gestión de Registros</h1>', unsafe_allow_html=True)

        # Contenedores nativos seguros para los clics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="action-card"><div class="card-icon">🎓</div><div class="card-title">Docentes evaluadores</div><div class="card-desc">Registra, actualiza y gestiona los docentes que participan en el proceso RAP.</div>', unsafe_allow_html=True)
            if st.button("Gestionar docentes", use_container_width=True, key="nav_doc_btn"):
                st.session_state['reg_vista'] = "docentes"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="action-card"><div class="card-icon">👤</div><div class="card-title">Estudiantes</div><div class="card-desc">Registra, actualiza y gestiona los estudiantes del proceso RAP y consulta su estado de aplicación.</div>', unsafe_allow_html=True)
            if st.button("Gestionar estudiantes", use_container_width=True, key="nav_est_btn"):
                st.session_state['reg_vista'] = "estudiantes"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="action-card"><div class="card-icon">👁️</div><div class="card-title">Vista maestra</div><div class="card-desc">Consulta el estado de aplicación por estudiante, asignaturas y resultados del proceso RAP.</div>', unsafe_allow_html=True)
            if st.button("Abrir vista maestra", use_container_width=True, key="nav_mae_btn"):
                st.session_state['reg_vista'] = "maestra"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Mostrar métricas reales
        st.markdown(f"""<div class="metrics-grid">
            <div class="metric-card"><div class="metric-lbl">Total estudiantes</div><div class="metric-val">{tot_est}</div></div>
            <div class="metric-card"><div class="metric-lbl">Docentes evaluadores</div><div class="metric-val">{tot_prof}</div></div>
            <div class="metric-card"><div class="metric-lbl">Pendientes de gestión</div><div class="metric-val">{tot_pend}</div></div>
            <div class="metric-card"><div class="metric-lbl">Asignaturas activas</div><div class="metric-val">{tot_asig}</div></div>
        </div>""", unsafe_allow_html=True)

        # Renderizar línea de tiempo dinámica
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
            html_timeline = "<p style='color:#64748b;'>No hay actividad reciente para mostrar.</p>"

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
                <div style="border: 1px solid #e2e8f0; padding: 16px; border-radius: 10px; margin-bottom: 15px; font-weight:500;">✅ Validar documentos de estudiantes</div>
                <div style="border: 1px solid #e2e8f0; padding: 16px; border-radius: 10px; margin-bottom: 15px; font-weight:500;">📅 Programar prueba por asignatura</div>
            </div>
        </div></div>""", unsafe_allow_html=True)

    # Redirecciones nativas a los módulos independientes
    elif st.session_state['reg_vista'] == "docentes":
        gestion_docentes.render()
    elif st.session_state['reg_vista'] == "estudiantes":
        gestion_estudiantes.render()
    elif st.session_state['reg_vista'] == "maestra":
        vista_maestra.render()