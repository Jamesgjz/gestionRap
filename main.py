import streamlit as st
from modules import inicio, registro, estado_pruebas, programacion, evaluacion, dashboard

# 1. Configuración de página
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

if 'autenticado' not in st.session_state: st.session_state['autenticado'] = False
if 'opcion_menu' not in st.session_state: st.session_state['opcion_menu'] = "Inicio"

# 2. CSS PREMIUM (Reemplaza al iFrame, sin sobreposiciones)
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    .stApp { background-color: #f8fafc !important; }
    div.block-container { padding: 0 !important; max-width: 100% !important; }
    
    .login-box {
        display: flex; width: 1100px; height: 600px; background: white;
        border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        margin: 50px auto; overflow: hidden; border: 1px solid #e2e8f0;
    }
    .left-panel { background: linear-gradient(180deg, #001737 0%, #00224f 100%); width: 450px; padding: 40px; color: white; }
    .right-panel { flex: 1; padding: 60px; background: white; }
    
    div.stButton > button { background-color: #0056b3 !important; color: white !important; width: 100% !important; padding: 12px !important; border-radius: 8px !important; font-weight: 700 !important; border: none !important; }
    
    /* Estilos del Sidebar */
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #001f4d 0%, #00112c 100%) !important; }
    </style>
""", unsafe_allow_html=True)

# --- ESCENARIO A: LOGIN PREMIUM NATIVO ---
if not st.session_state['autenticado']:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    c1, c2 = st.columns([0.4, 0.6])
    
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
        
        tab1, tab2 = st.tabs(["👤 Administrativo", "🌐 Consulta pública"])
        with tab1:
            user = st.text_input("Usuario")
            pwd = st.text_input("Contraseña", type="password")
            if st.button("Ingresar al sistema"):
                if user == "admin" and pwd == "admin123":
                    st.session_state['autenticado'] = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ESCENARIO B: PANEL ADMINISTRATIVO (COMPLETO) ---
else:
    with st.sidebar:
        st.title("RAP Digital")
        if st.button("🏠 Inicio"): st.session_state['opcion_menu'] = "Inicio"
        if st.button("🎓 Registro de Estudiantes"): st.session_state['opcion_menu'] = "Registro Estudiantes"
        if st.button("📋 Estado de Pruebas"): st.session_state['opcion_menu'] = "Estado de Pruebas"
        if st.button("📅 Programación"): st.session_state['opcion_menu'] = "Programación"
        if st.button("📝 Evaluación"): st.session_state['opcion_menu'] = "Evaluación"
        if st.button("📊 Dashboard / KPIs"): st.session_state['opcion_menu'] = "Dashboard / KPIs"
        st.divider()
        if st.button("🚪 Cerrar sesión"):
            st.session_state['autenticado'] = False
            st.rerun()

    # --- ENRUTADOR ---
    opcion = st.session_state['opcion_menu']
    if opcion == "Inicio": inicio.render()
    elif opcion == "Registro Estudiantes": registro.render()
    elif opcion == "Estado de Pruebas": estado_pruebas.render()
    elif opcion == "Programación": programacion.render()
    elif opcion == "Evaluación": evaluacion.render()
    elif opcion == "Dashboard / KPIs": dashboard.render()