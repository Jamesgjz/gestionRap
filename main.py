import streamlit as st
from modules import inicio, registro, estado_pruebas, programacion, evaluacion, dashboard

# 1. Configuración de página ultra-limpia
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", layout="wide")

if 'autenticado' not in st.session_state: st.session_state['autenticado'] = False
if 'opcion_menu' not in st.session_state: st.session_state['opcion_menu'] = "Inicio"

# --- CSS BLINDADO Y FORZADO ---
# Este CSS destruye todos los elementos de Streamlit que causan la sobreposición y centra nuestra tarjeta
st.markdown("""
    <style>
    /* Ocultar todo lo nativo de Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer { display: none !important; }
    .stApp { background-color: #f8fafc !important; overflow: hidden !important; }
    div.block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
    
    /* El contenedor premium es ahora el único dueño del espacio */
    .premium-card {
        display: flex; width: 1100px; height: 650px; background: white;
        border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 5vh auto; overflow: hidden; border: 1px solid #e2e8f0;
    }
    .left-panel { background: #001737; width: 450px; padding: 40px; color: white; display: flex; flex-direction: column; justify-content: space-between; }
    .right-panel { flex: 1; padding: 60px; background: white; }
    
    /* Botón corporativo impecable */
    div.stButton > button { background-color: #0047ff !important; color: white !important; width: 100% !important; padding: 15px !important; border-radius: 8px !important; font-weight: 700 !important; border: none !important; font-size: 1.1rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN TOTALMENTE INTEGRADO ---
if not st.session_state['autenticado']:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([0.41, 0.59])
    
    with c1:
        st.markdown("""
            <div class="left-panel">
                <h2>MD UNIMINUTO</h2>
                <h3>RAP DIGITAL</h3>
                <p>Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="right-panel">', unsafe_allow_html=True)
        st.subheader("Acceso al sistema")
        st.write("Inicia sesión para continuar.")
        
        tab1, tab2 = st.tabs(["👤 Administrativo", "🌐 Consulta pública"])
        with tab1:
            user = st.text_input("Usuario", placeholder="Ingresa tu usuario")
            pwd = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
            if st.button("Ingresar al sistema"):
                if user == "admin" and pwd == "admin123":
                    st.session_state['autenticado'] = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- PANEL ADMINISTRATIVO ---
    with st.sidebar:
        st.title("RAP Digital")
        if st.button("🏠 Inicio"): st.session_state['opcion_menu'] = "Inicio"
        if st.button("🎓 Registro Estudiantes"): st.session_state['opcion_menu'] = "Registro Estudiantes"
        if st.button("📊 Dashboard"): st.session_state['opcion_menu'] = "Dashboard / KPIs"
        st.divider()
        if st.button("🚪 Cerrar sesión"):
            st.session_state['autenticado'] = False
            st.rerun()

    # --- ENRUTADOR ---
    opcion = st.session_state['opcion_menu']
    if opcion == "Inicio": inicio.render()
    elif opcion == "Registro Estudiantes": registro.render()
    elif opcion == "Dashboard / KPIs": dashboard.render()