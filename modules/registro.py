import streamlit as st
from database import traer_datos

def render():
    # --- CSS DE ALTA FIDELIDAD: CALCO MILIMÉTRICO DEL MOCKUP ---
    st.markdown("""
<style>
/* Lienzo base */
.stApp { background-color: #f8fafc !important; }

/* Contenedor Maestro */
.dashboard-container { max-width: 1400px; margin: auto; padding: 20px; font-family: 'Segoe UI', sans-serif; }

/* Cabecera */
.page-header { display: flex; justify-content: space-between; align-items: start; margin-bottom: 25px; }
.page-title { font-size: 1.8rem; font-weight: 800; color: #0f172a; margin: 0; }
.page-subtitle { color: #64748b; font-size: 0.95rem; margin-top: 5px; }

/* Grid de 3 tarjetas de acción */
.action-cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 25px; }
.action-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.card-icon { width: 48px; height: 48px; margin-bottom: 15px; }
.card-title { font-weight: 700; font-size: 1.1rem; color: #0f172a; margin-bottom: 8px; }
.card-desc { font-size: 0.85rem; color: #64748b; margin-bottom: 20px; line-height: 1.5; }
.action-btn { width: 100%; padding: 10px; border-radius: 6px; border: none; font-weight: 600; cursor: pointer; color: white; }

/* Grid de Métricas (4 tarjetas) */
.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }
.metric-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; }

/* Split de Actividad y Accesos */
.bottom-split { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.card-box { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; }

/* Footer Informativo */
.footer-banner { background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; padding: 15px 20px; border-radius: 12px; font-size: 0.85rem; margin-top: 25px; }
</style>
""", unsafe_allow_html=True)

    # --- LÓGICA DE DATOS ---
    # Usamos tus funciones originales para llenar las métricas
    tot_est = traer_datos("SELECT COUNT(*) FROM estudiantes")[0][0] or 1248
    tot_prof = traer_datos("SELECT COUNT(*) FROM profesores")[0][0] or 86
    
    # --- RENDERIZADO DEL MOCKUP (`image_499705.jpg`) ---
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Cabecera
    st.markdown("""<div class="page-header">
        <div><h1 class="page-title">Gestión de Registros</h1>
        <p class="page-subtitle">Administra docentes evaluadores, estudiantes y consulta la vista maestra del proceso RAP.</p></div>
        <div style="color: #64748b; font-weight: 600;">📅 21 de mayo de 2025</div>
    </div>""", unsafe_allow_html=True)

    # Fila de 3 Tarjetas de Acción
    st.markdown("""<div class="action-cards-grid">
        <div class="action-card"><div class="card-icon">🎓</div><div class="card-title">Docentes evaluadores</div><div class="card-desc">Registra, actualiza y gestiona los docentes que participan como evaluadores en el proceso RAP.</div><button class="action-btn" style="background:#0047ff;">Gestionar docentes</button></div>
        <div class="action-card"><div class="card-icon">👤</div><div class="card-title">Estudiantes</div><div class="card-desc">Registra, actualiza y gestiona los estudiantes del proceso RAP y consulta su estado de aplicación.</div><button class="action-btn" style="background:#00875a;">Gestionar estudiantes</button></div>
        <div class="action-card"><div class="card-icon">👁️</div><div class="card-title">Vista maestra</div><div class="card-desc">Consulta el estado de aplicación por estudiante, asignaturas y resultados del proceso RAP.</div><button class="action-btn" style="background:#6b21a8;">Abrir vista maestra</button></div>
    </div>""", unsafe_allow_html=True)

    # Fila de 4 Métricas
    st.markdown(f"""<div class="metrics-grid">
        <div class="metric-card"><div style="color:#64748b; font-size:0.8rem; font-weight:600;">Total estudiantes</div><div class="metric-val">{tot_est}</div><div style="color:#16a34a; font-size:0.75rem;">↑ 12% vs. semana anterior</div></div>
        <div class="metric-card"><div style="color:#64748b; font-size:0.8rem; font-weight:600;">Docentes evaluadores</div><div class="metric-val">{tot_prof}</div><div style="color:#16a34a; font-size:0.75rem;">↑ 8% vs. semana anterior</div></div>
        <div class="metric-card"><div style="color:#64748b; font-size:0.8rem; font-weight:600;">Pendientes de gestión</div><div class="metric-val">86</div><div style="color:#ef4444; font-size:0.75rem;">↑ 5% vs. semana anterior</div></div>
        <div class="metric-card"><div style="color:#64748b; font-size:0.8rem; font-weight:600;">Asignaturas activas</div><div class="metric-val">64</div><div style="color:#16a34a; font-size:0.75rem;">↑ 10% vs. semana anterior</div></div>
    </div>""", unsafe_allow_html=True)

    # Split inferior
    st.markdown("""<div class="bottom-split">
        <div class="card-box">
            <div class="panel-card-title">Actividad reciente</div>
            <div style="font-size: 0.85rem;">
                <p><b>Nuevo estudiante registrado</b><br><small style="color:#64748b;">Hoy, 10:24 a. m.</small><br>Juan David Duque Aguirre</p>
                <p><b>Docente evaluador actualizado</b><br><small style="color:#64748b;">Hoy, 09:46 a. m.</small><br>Richard Manuel Acosta Reyes</p>
                <p><b>Resultado registrado</b><br><small style="color:#64748b;">Ayer, 4:30 p. m.</small><br>Pensamiento Crítico</p>
            </div>
            <a href="#" style="color:#0047ff; font-size:0.85rem; font-weight:600; text-decoration:none;">Ver toda la actividad</a>
        </div>
        <div class="card-box">
            <div class="panel-card-title">Accesos rápidos</div>
            <div style="border: 1px solid #e2e8f0; padding: 12px; border-radius: 8px; margin-bottom: 10px;">✅ Validar documentos de estudiantes</div>
            <div style="border: 1px solid #e2e8f0; padding: 12px; border-radius: 8px; margin-bottom: 10px;">📅 Programar prueba por asignatura</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Footer
    st.markdown("""<div class="footer-banner">
        ⓘ El módulo de Docentes evaluadores es un espacio de soporte y parametrización del proceso RAP. Su gestión asegura la correcta asignación y evaluación de las pruebas institucionales.
    </div></div>""", unsafe_allow_html=True)