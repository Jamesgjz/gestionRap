import streamlit as st
from database import ejecutar_query, traer_datos

def render():
    # --- ENRUTADOR INTERNO ---
    if 'reg_vista_actual' not in st.session_state:
        st.session_state['reg_vista_actual'] = "resumen"

    # --- INYECCIÓN DE ESTILOS CSS (DISEÑO FIDELIDAD TOTAL) ---
    st.markdown("""
<style>
/* Reset de fondo */
html, body, [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }

/* Cabecera */
.main-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.main-title { font-size: 2rem !important; font-weight: 800 !important; color: #0f172a; margin: 0; }

/* Tarjetas de Navegación Superiores (Centradas y Grandes) */
.card-nav-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 30px; }
.card-nav-premium { 
    background: white; border: 1px solid #e2e8f0; border-radius: 16px; 
    padding: 30px; display: flex; flex-direction: column; align-items: center; text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.03); 
}
.card-nav-icon { 
    width: 65px; height: 65px; border-radius: 50%; 
    display: flex; align-items: center; justify-content: center; 
    font-size: 1.8rem; margin-bottom: 20px; 
}
.card-title { font-weight: 700; font-size: 1.25rem; color: #0f172a; margin-bottom: 10px; }
.card-desc { font-size: 0.95rem; color: #64748b; line-height: 1.5; margin-bottom: 20px; }

/* Botones con estilo corporativo */
div.stButton > button { width: 100%; border-radius: 8px; font-weight: 600; padding: 12px; border: none; }
div.stButton > button[key*="doc"] { background-color: #0047ff !important; color: white !important; }
div.stButton > button[key*="est"] { background-color: #00875a !important; color: white !important; }
div.stButton > button[key*="mae"] { background-color: #6b21a8 !important; color: white !important; }

/* Métricas Ampliadas */
.metrics-box-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
.metric-box { background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 25px; position: relative; }
.metric-val { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin-top: 5px; }
.metric-lbl { font-size: 0.9rem; font-weight: 600; color: #64748b; }

/* Tablas y Estilos Generales */
.premium-data-table { width: 100%; border-collapse: collapse; font-size: 0.95rem; }
.premium-data-table th { background: #f8fafc; padding: 15px 10px; color: #475569; font-weight: 600; border-bottom: 2px solid #e2e8f0; }
.premium-data-table td { padding: 15px 10px; border-bottom: 1px solid #f1f5f9; color: #334155; }
</style>
""", unsafe_allow_html=True)

    # --- DATOS ---
    total_est = traer_datos("SELECT COUNT(*) FROM estudiantes")[0][0] or 1248
    
    # --- RENDER VISTA PRINCIPAL ---
    if st.session_state['reg_vista_actual'] == "resumen":
        st.markdown('<div class="main-header"><h1 class="main-title">Gestión de Registros</h1><div style="color:#64748b;">📅 21 de mayo de 2025</div></div>', unsafe_allow_html=True)
        
        # Tarjetas centradas y grandes
        st.markdown("""<div class="card-nav-grid">
            <div class="card-nav-premium">
                <div class="card-nav-icon" style="background:#edf5ff; color:#0047ff;"><i class="fa-solid fa-user-graduate"></i></div>
                <div class="card-title">Docentes evaluadores</div>
                <div class="card-desc">Registra, actualiza y gestiona los docentes que participan como evaluadores en el proceso RAP.</div>
            </div>
            <div class="card-nav-premium">
                <div class="card-nav-icon" style="background:#e6f4ea; color:#00875a;"><i class="fa-regular fa-user"></i></div>
                <div class="card-title">Estudiantes</div>
                <div class="card-desc">Registra, actualiza y gestiona los estudiantes del proceso RAP y consulta su estado.</div>
            </div>
            <div class="card-nav-premium">
                <div class="card-nav-icon" style="background:#f3e8ff; color:#6b21a8;"><i class="fa-regular fa-eye"></i></div>
                <div class="card-title">Vista maestra</div>
                <div class="card-desc">Consulta el estado de aplicación por estudiante, asignaturas y resultados del proceso RAP.</div>
            </div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        if c1.button("Gestionar docentes", key="doc"): st.session_state['reg_vista_actual'] = "docentes"; st.rerun()
        if c2.button("Gestionar estudiantes", key="est"): st.session_state['reg_vista_actual'] = "estudiantes"; st.rerun()
        if c3.button("Abrir vista maestra", key="mae"): st.session_state['reg_vista_actual'] = "maestra"; st.rerun()

        # Métricas grandes
        st.markdown(f"""<div class="metrics-box-grid">
            <div class="metric-box"><div class="metric-lbl">Total estudiantes</div><div class="metric-val">{total_est}</div></div>
            <div class="metric-box"><div class="metric-lbl">Docentes evaluadores</div><div class="metric-val">86</div></div>
            <div class="metric-box"><div class="metric-lbl">Pendientes</div><div class="metric-val">86</div></div>
            <div class="metric-box"><div class="metric-lbl">Asignaturas</div><div class="metric-val">64</div></div>
        </div>""", unsafe_allow_html=True)

    elif st.session_state['reg_vista_actual'] == "estudiantes":
        if st.button("← Volver", key="back"): st.session_state['reg_vista_actual'] = "resumen"; st.rerun()
        st.subheader("Registrar / Actualizar Estudiante")
        # Aquí continúa tu lógica de formulario...