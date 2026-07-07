import streamlit as st
import json
from modules import inicio, registro, estado_pruebas, programacion, evaluacion, dashboard

# 1. Configuración de la página en modo ancho total e impecable
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

# Inicialización segura de los estados de sesión
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if 'opcion_menu' not in st.session_state:
    st.session_state['opcion_menu'] = "Inicio"

# --- PROCESADOR DE NAVEGACIÓN ADMINISTRATIVA (MENÚ LATERAL) ---
query_params = st.query_params
menu_click = query_params.get("view", None)
if menu_click:
    if isinstance(menu_click, list) or isinstance(menu_click, tuple):
        menu_click = menu_click[0] if len(menu_click) > 0 else "Inicio"
    st.session_state['opcion_menu'] = menu_click
    st.query_params.clear()
    st.rerun()

# --- ESCENARIO A: PANTALLA DE LOGIN DE ALTA FIDELIDAD (COMPONENTE NATIVO ESTILIZADO) ---
if not st.session_state['autenticado']:
    
    # Inyección de estilos globales avanzados para reescribir la interfaz nativa de Streamlit
    st.markdown("""
        <style>
        /* Ocultar cabeceras y elementos por defecto de Streamlit */
        [data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }
        div.block-container { padding: 25px 50px !important; max-width: 100% !important; }
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background-color: #f8fafc !important; font-family: 'Inter', sans-serif; }
        
        /* Contenedor unificado de la Tarjeta de Login */
        .premium-login-card {
            display: flex;
            width: 100%;
            max-width: 1180px;
            background: #ffffff;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(15, 23, 42, 0.04);
            min-height: 600px;
            margin: 0 auto;
            border: 1px solid #e2e8f0;
        }
        
        /* Personalización de las columnas nativas de Streamlit para simular la tarjeta */
        div[data-testid="stColumns"] { gap: 0px !important; }
        div[data-testid="column"]:first-child { background: linear-gradient(180deg, #001737 0%, #00224f 100%); padding: 4.5rem 3.5rem; color: white; display: flex; flex-direction: column; justify-content: space-between; border-top-left-radius: 24px; border-bottom-left-radius: 24px; }
        div[data-testid="column"]:last-child { padding: 4.5rem; background-color: #ffffff; display: flex; flex-direction: column; justify-content: center; border-top-right-radius: 24px; border-bottom-right-radius: 24px; }
        
        /* Estilización quirúrgica de Inputs Nativos de Streamlit */
        div[data-testid="stTextInput"] label { font-size: 0.95rem !important; font-weight: 600 !important; color: #334155 !important; margin-bottom: 0.6rem !important; }
        div[data-testid="stTextInput"] input { 
            width: 100% !important; 
            padding: 0.85rem 1rem 0.85rem 3rem !important; 
            border-radius: 12px !important; 
            border: 1px solid #cbd5e1 !important; 
            font-size: 1rem !important; 
            color: #0f172a !important; 
            background-color: #ffffff !important;
            font-family: 'Inter', sans-serif !important;
        }
        div[data-testid="stTextInput"] input:focus { border-color: #0056b3 !important; box-shadow: 0 0 0 4px rgba(0, 86, 179, 0.08) !important; }
        
        /* Inyección de Vectores de Iconos en los Inputs Nativos vía Data-URI */
        #usr_input {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394a3b8' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' /%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important; background-position: 14px center !important; background-size: 20px !important;
        }
        #pwd_input {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394a3b8' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z' /%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important; background-position: 14px center !important; background-size: 20px !important;
        }
        
        /* Transformación Absoluta de st.radio para recrear las Pestañas Rectangulares Premium */
        div[data-testid="stRadio"] > label { display: none !important; }
        div[data-testid="stRadio"] div[role="radiogroup"] { background-color: #f1f5f9 !important; padding: 6px !important; border-radius: 12px !important; gap: 5px !important; display: flex !important; flex-direction: row !important; border: none !important; }
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-testid="stRadioOption"] { flex: 1 !important; background: transparent !important; padding: 12px !important; border-radius: 8px !important; justify-content: center !important; display: flex !important; cursor: pointer !important; margin: 0 !important; }
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-testid="stRadioOption"] div:first-child { display: none !important; }
        div[data-testid="stRadio"] div[role="radiogroup"] div[data-testid="stMarkdownContainer"] p { font-weight: 600 !important; font-size: 0.95rem !important; color: #64748b !important; margin: 0 !important; }
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-testid="stRadioOption"]:has(input:checked) { background: #ffffff !important; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04) !important; }
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-testid="stRadioOption"]:has(input:checked) p { color: #0056b3 !important; }
        
        /* Botón de Envío Corporativo Expandido Completamente */
        div.stButton > button { background-color: #0056b3 !important; color: white !important; width: 100% !important; padding: 1rem !important; border-radius: 12px !important; font-size: 1.05rem !important; font-weight: 700 !important; border: none !important; box-shadow: 0 4px 14px rgba(0, 86, 179, 0.2) !important; transition: all 0.2s !important; }
        div.stButton > button:hover { background-color: #004494 !important; transform: translateY(-1px); }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)

    # Navbar Superior Institucional Idéntico al Mockup
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 1px solid #e2e8f0; margin-bottom: 40px; width:100%;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Logo_Uniminuto.png/640px-Logo_Uniminuto.png" style="height:45px; width:auto;">
            </div>
            <div style="display: flex; align-items: center; gap: 25px; color: #1e293b;">
                <div style="position: relative; cursor: pointer; font-size: 1.3rem; color: #0056b3;"><i class="fa-regular fa-bell"></i><div style="position: absolute; top: -5px; right: -5px; background: #0056b3; color: white; border-radius: 50%; width: 16px; height: 16px; font-size: 0.65rem; display: flex; align-items: center; justify-content: center; font-weight: 700;">3</div></div>
                <div style="font-size: 1.3rem; cursor:pointer; color:#64748b;"><i class="fa-regular fa-circle-question"></i></div>
                <div style="color: #64748b; font-size: 0.9rem; font-weight: 500; display: flex; align-items: center; gap: 8px;"><i class="fa-regular fa-calendar"></i> 21 de mayo de 2025</div>
            </div>
        </div>
        <div style="margin-top: 20px;"></div>
    """, unsafe_allow_html=True)

    # Renderizado Fluido de la Tarjeta de Login sin Contenedores Externos Rompibles
    st.markdown('<div class="premium-login-card">', unsafe_allow_html=True)
    col_izq_diseno, col_der_campos = st.columns([1, 1.12])
    
    with col_izq_diseno:
        st.markdown("""
            <div style="position: relative; z-index: 2; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.5rem; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 2rem; display: flex; align-items: center; gap: 8px;">
                        <i class="fa-solid fa-graduation-cap" style="color:#38bdf8;"></i> MD UNIMINUTO
                    </div>
                    <div style="color: #38bdf8; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">RAP Digital</div>
                    <h1 style="font-size: 2.4rem; font-weight: 800; line-height: 1.15; margin: 0 0 1.5rem 0; letter-spacing: -0.5px;">UNIMINUTO<br><span style="color:#f1c40f; font-size:1.9rem; font-weight:700;">VIRTUAL</span></h1>
                    <div style="width: 45px; height: 3px; background-color: #38bdf8; margin-bottom: 1.8rem; border-radius: 2px;"></div>
                    <p style="font-size: 1.1rem; color: #94a3b8; line-height: 1.6; font-weight: 400; margin: 0;">Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.</p>
                </div>
                <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 2rem; gap: 10px; margin-top: 4rem;">
                    <div class="feature-box" style="text-align: center; flex: 1; display: flex; flex-direction: column; align-items: center;"><div class="feature-icon-wrapper" style="background: rgba(255, 255, 255, 0.05); width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 10px; color: #38bdf8; font-size: 1.2rem; border: 1px solid rgba(255, 255, 255, 0.05);"><i class="fa-solid fa-chart-line"></i></div><span style="font-weight: 600; font-size: 0.9rem; color: #f8fafc;">Seguimiento</span></div>
                    <div class="feature-box" style="text-align: center; flex: 1; display: flex; flex-direction: column; align-items: center;"><div class="feature-icon-wrapper" style="background: rgba(255, 255, 255, 0.05); width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 10px; color: #38bdf8; font-size: 1.2rem; border: 1px solid rgba(255, 255, 255, 0.05);"><i class="fa-regular fa-clipboard"></i></div><span style="font-weight: 600; font-size: 0.9rem; color: #f8fafc;">Evaluación</span></div>
                    <div class="feature-box" style="text-align: center; flex: 1; display: flex; flex-direction: column; align-items: center;"><div class="feature-icon-wrapper" style="background: rgba(255, 255, 255, 0.05); width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 10px; color: #38bdf8; font-size: 1.2rem; border: 1px solid rgba(255, 255, 255, 0.05);"><i class="fa-regular fa-circle-check"></i></div><span style="font-weight: 600; font-size: 0.9rem; color: #f8fafc; text-align: center;">Trazabilidad<br><span style="font-size:0.75rem; font-weight:400; color:#94a3b8;">académica</span></span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_der_campos:
        st.markdown("""
            <div style="margin-bottom: 2rem;">
                <h2 style="color: #0f172a; font-size: 2.1rem; font-weight: 700; margin: 0 0 6px 0; letter-spacing: -0.5px;">Acceso al sistema</h2>
                <p style="color: #64748b; font-size: 1rem; margin: 0;">Inicia sesión para continuar con RAP Digital.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # El componente de selección estilizado impecablemente como las pestañas de la Imagen 5
        tab_selec = st.radio("Rol_Acceso", ["👤 Administrativo", "🌐 Consulta pública"], horizontal=True)
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        
        if "Administrativo" in tab_selec:
            # Inputs con identificadores estáticos capturados por las reglas CSS de Data-URI
            usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="usr_input")
            contrasena = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="pwd_input")
            
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            
            # Validación nativa, segura y de alta velocidad al primer clic
            if st.button("➡️ Ingresar al sistema", use_container_width=True):
                if usuario == "admin" and contrasena == "admin123":
                    st.session_state['autenticado'] = True
                    st.session_state['usuario'] = "James Jaramillo"
                    st.session_state['rol'] = "admin"
                    st.session_state['opcion_menu'] = "Inicio"
                    st.rerun()
                else:
                    st.error("❌ Credenciales inválidas.")
        else:
            st.markdown("""
                <div style='text-align:center; padding: 40px 0; color:#64748b;'>
                    <i class='fa-solid fa-circle-info' style='font-size:2.5rem; color:#0056b3; margin-bottom:15px;'></i><br>
                    <span style="font-weight:600; color:#0f172a;">Consulta Pública Habilitada</span><br>
                    Use los accesos institucionales para validar el estado de trámites RAP.
                </div>
            """, unsafe_allow_html=True)
            
        # Bloque inferior de soporte violeta idéntico al mockup
        st.markdown("""
            <div style="background-color: #f5f3ff; border: 1px solid #e9e3ff; border-radius: 12px; padding: 14px 20px; color: #5b21b6; font-size: 0.95rem; font-weight: 600; margin-top: 2.5rem; display: flex; justify-content: space-between; align-items: center; cursor: pointer;">
                <span><i class="fa-regular fa-circle-question" style="color:#7c3aed; margin-right:8px; font-size:1.05rem;"></i> Soporte académico RAP</span>
                <i class="fa-solid fa-chevron-right" style="font-size: 0.85rem;"></i>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- ESCENARIO B: ENTORNO ADMINISTRATIVO COMPLETO (LOGUEADO) ---
else:
    # Restablecemos los scrolls y configuramos el menú lateral administrativo premium con tus espaciados de 20px
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] { overflow: auto !important; background-color: #fcfdfe !important; }
        div.block-container { padding: 2.5rem 4rem !important; max-width: 100% !important; }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #001f4d 0%, #00112c 100%) !important;
        }
        [data-testid="stSidebarNav"] { display: none !important; }
        
        .sidebar-brand { padding: 20px 10px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
        .user-badge { background: rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.1); }
        
        /* Configuración de botones de la barra lateral con tus espaciados de 20px */
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"],
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:focus,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:active {
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 20px !important;
            margin-bottom: 10px !important;
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            text-align: left !important;
            border-radius: 10px !important;
        }
        
        /* Fuerza que el texto permanezca blanco y no sea tapado por el hover */
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] p,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] span,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] div,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover p {
            color: #ffffff !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            margin: 0 !important;
            text-align: left !important;
            justify-content: flex-start !important;
        }
        
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover {
            background: #0056b3 !important;
            background-color: #0056b3 !important;
            cursor: pointer !important;
        }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("""
            <div class="sidebar-brand">
                <div style="color:#38bdf8; font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:1px;">RAP Digital</div>
                <div style="font-size:1.3rem; font-weight:800; color:white; line-height:1.2;">MD UNIMINUTO<br><span style="color:#f1c40f; font-size:1rem;">VIRTUAL</span></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="user-badge">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="background:#38bdf8; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white;"><i class="fa-regular fa-user"></i></div>
                    <div>
                        <div style="font-weight:700; font-size:0.95rem; color:white;">{st.session_state['usuario']}</div>
                        <div style="font-size:0.75rem; color:#94a3b8;">Administrador</div>
                    </div>
                </div>
                <div style="margin-top:10px; font-size:0.75rem; color:#22c55e;"><i class="fa-solid fa-circle" style="font-size:0.6rem; margin-right:5px;"></i> En línea</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Inicio", use_container_width=True):
            st.session_state['opcion_menu'] = "Inicio"
            st.rerun()
        if st.button("🎓 Registro de Estudiantes", use_container_width=True):
            st.session_state['opcion_menu'] = "Registro Estudiantes"
            st.rerun()
        if st.button("📋 Estado de Pruebas", use_container_width=True):
            st.session_state['opcion_menu'] = "Estado de Pruebas"
            st.rerun()
        if st.button("📅 Programación", use_container_width=True):
            st.session_state['opcion_menu'] = "Programación"
            st.rerun()
        if st.button("📝 Evaluación", use_container_width=True):
            st.session_state['opcion_menu'] = "Evaluación"
            st.rerun()
        if st.button("📊 Dashboard / KPIs", use_container_width=True):
            st.session_state['opcion_menu'] = "Dashboard / KPIs"
            st.rerun()
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state['autenticado'] = False
            st.rerun()

    # --- ENRUTADOR GENERAL DE VISTAS (LÓGICA MODULAR COMERCIAL) ---
    opcion = st.session_state['opcion_menu']

    if opcion == "Inicio":
        inicio.render()
    elif opcion == "Registro Estudiantes":
        registro.render()
    elif opcion == "Estado de Pruebas":
        estado_pruebas.render()
    elif opcion == "Programación":
        programacion.render()
    elif opcion == "Evaluación":
        evaluacion.render()
    elif opcion == "Dashboard / KPIs":
        dashboard.render()