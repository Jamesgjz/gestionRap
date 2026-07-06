import streamlit as st
from modules import inicio, registro, estado_pruebas, programacion, evaluacion, dashboard

# 1. Configuración de la página en modo ancho total y limpio sin scrolls
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

# Inicialización estricta del estado de la sesión
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if 'opcion_menu' not in st.session_state:
    st.session_state['opcion_menu'] = "Inicio"

if 'modo_tabs' not in st.session_state:
    st.session_state['modo_tabs'] = "Administrativo"

# --- PROCESADOR DE NAVEGACIÓN ADMINISTRATIVA (MENÚ LATERAL) ---
query_params = st.query_params
menu_click = query_params.get("view", None)
if menu_click:
    if isinstance(menu_click, list) or isinstance(menu_click, tuple):
        menu_click = menu_click[0] if len(menu_click) > 0 else "Inicio"
    st.session_state['opcion_menu'] = menu_click
    st.query_params.clear()
    st.rerun()

# --- ESCENARIO A: PANTALLA DE LOGIN PREMIUM SIN IFRAMES (CASCARÓN ESTÁTICO) ---
if not st.session_state['autenticado']:
    
    # Inyección de CSS de alta prioridad para ocultar barras nativas y unificar el diseño gris/blanco
    st.markdown("""
        <style>
        /* Desactivar elementos nativos superiores de Streamlit para el Login */
        [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { overflow: hidden !important; background-color: #f8fafc !important; }
        div.block-container { padding: 25px 60px !important; max-width: 1200px !important; margin: 0 auto !important; }
        
        /* DISEÑO DE LA PLATAFORMA DE TRASFONDO (Idéntica a tu mockup) */
        .top-bar { display: flex; justify-content: space-between; align-items: center; padding-bottom: 15px; border-bottom: 1px solid #e2e8f0; margin-bottom: 25px; font-family: 'Inter', sans-serif; }
        .top-logo img { height: 35px; width: auto; }
        .right-nav-items { display: flex; align-items: center; gap: 20px; color: #64748b; font-size: 0.9rem; font-weight: 500; }
        .icon-badge-container { position: relative; font-size: 1.2rem; color: #0056b3; }
        .icon-badge { position: absolute; top: -5px; right: -5px; background: #0056b3; color: white; border-radius: 50%; width: 15px; height: 15px; font-size: 0.6rem; display: flex; align-items: center; justify-content: center; font-weight: 700; }
        
        /* ACABADO DE LA TARJETA PRINCIPAL CON COLUMNAS NATIVAS ENLOMADAS */
        div[data-testid="stColumns"] {
            background: #ffffff !important;
            border-radius: 24px !important;
            box-shadow: 0 20px 40px rgba(15, 23, 42, 0.05) !important;
            overflow: hidden !important;
            border: 1px solid #e2e8f0 !important;
        }
        div[data-testid="column"] { padding: 0 !important; margin: 0 !important; }
        
        /* Mitad Izquierda: Banner Azul Universitario con marca de agua sutil */
        .banner-azul-container {
            background: linear-gradient(180deg, #001737 0%, #00224f 100%);
            padding: 4rem 3.5rem;
            color: white;
            height: 570px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
            position: relative;
        }
        .banner-azul-container::before {
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Logo_Uniminuto.png/640px-Logo_Uniminuto.png');
            background-position: bottom -10% right -30%; background-repeat: no-repeat; background-size: 90%; opacity: 0.03; pointer-events: none;
        }
        .banner-top-content { position: relative; z-index: 2; }
        .sub-marca { color: #38bdf8; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
        .main-logo-title { font-size: 2.3rem; font-weight: 800; line-height: 1.15; margin: 0 0 1.2rem 0; letter-spacing: -0.5px; }
        .main-description { font-size: 1.05rem; color: #94a3b8; line-height: 1.6; }
        
        /* Indicadores vectoriales de la parte inferior */
        .banner-features { display: flex; justify-content: space-between; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 1.8rem; gap: 10px; position: relative; z-index: 2; }
        .feature-box { text-align: center; flex: 1; display: flex; flex-direction: column; align-items: center; }
        .feature-icon-wrapper { background: rgba(255, 255, 255, 0.04); width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 8px; color: #38bdf8; font-size: 1.1rem; border: 1px solid rgba(255, 255, 255, 0.04); }
        .feature-box .f-title { font-weight: 600; font-size: 0.85rem; color: #f8fafc; }
        
        /* ESTILIZACIÓN ULTRA-PROFESIONAL DE INPUTS DE STREAMLIT */
        div[data-testid="stTextInput"] label { font-size: 0.9rem !important; font-weight: 600 !important; color: #334155 !important; font-family: 'Inter', sans-serif; }
        div[data-testid="stTextInput"] input { border-radius: 12px !important; padding: 0.7rem 1rem !important; border: 1px solid #cbd5e1 !important; font-size: 0.95rem !important; color: #0f172a !important; background-color: #ffffff !important; }
        div[data-testid="stTextInput"] input:focus { border-color: #0056b3 !important; }
        
        /* Botón Ingresar Nativo Premium */
        div.stButton > button {
            background-color: #0056b3 !important; color: white !important; width: 100% !important; padding: 0.85rem !important;
            border-radius: 12px !important; font-weight: 700 !important; font-size: 1rem !important; border: none !important;
            box-shadow: 0 4px 14px rgba(0, 86, 179, 0.2) !important; margin-top: 10px !important; transition: all 0.2s !important;
        }
        div.stButton > button:hover { background-color: #004494 !important; }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)

    # Topbar Institucional limpia
    st.markdown("""
        <div class="top-bar">
            <div class="top-logo">
                <img src="https://www.uniminuto.edu/themes/custom/uniminuto/logo.png">
            </div>
            <div class="right-nav-items">
                <div class="icon-badge-container"><i class="fa-regular fa-bell"></i><div class="icon-badge">3</div></div>
                <div style="font-size: 1.2rem; cursor:pointer;"><i class="fa-regular fa-circle-question"></i></div>
                <div><i class="fa-regular fa-calendar"></i> 06 de Julio de 2026</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # RENDERIZADO SIMÉTRICO USANDO COLUMNAS NATIVAS (Funde la tarjeta en una sola pieza)
    col_izq, col_der = st.columns([1, 1.12])
    
    with col_izq:
        st.markdown("""
            <div class="banner-azul-container">
                <div class="banner-top-content">
                    <div style="font-size: 1.4rem; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 2.2rem; display: flex; align-items: center; gap: 8px;">
                        <i class="fa-solid fa-graduation-cap" style="color:#38bdf8;"></i> MD UNIMINUTO
                    </div>
                    <div class="sub-marca">RAP Digital</div>
                    <h1 class="main-logo-title">UNIMINUTO<br><span style="color:#f1c40f; font-size:1.8rem;">VIRTUAL</span></h1>
                    <div style="width: 45px; height: 3px; background-color: #38bdf8; margin-bottom: 1.5rem; border-radius: 2px;"></div>
                    <p class="main-description">Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.</p>
                </div>
                <div class="banner-features">
                    <div class="feature-box"><div class="feature-icon-wrapper"><i class="fa-solid fa-chart-line"></i></div><span class="f-title">Seguimiento</span></div>
                    <div class="feature-box"><div class="feature-icon-wrapper"><i class="fa-regular fa-clipboard"></i></div><span class="f-title">Evaluación</span></div>
                    <div class="feature-box"><div class="feature-icon-wrapper"><i class="fa-regular fa-circle-check"></i></div><span class="f-title">Trazabilidad<br><span style="font-size:0.75rem; font-weight:400; color:#94a3b8;">académica</span></span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_der:
        # Espaciado interno controlado
        st.markdown("""
            <div style="padding: 4rem 4rem 0rem 4rem; font-family: 'Inter', sans-serif;">
                <h2 style="color: #0f172a; font-weight: 700; font-size: 2rem; margin: 0 0 6px 0; letter-spacing: -0.5px;">Acceso al sistema</h2>
                <p style="color: #64748b; font-size: 0.95rem; margin: 0 0 25px 0;">Inicia sesión para continuar con RAP Digital.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Formulario encapsulado en aire interno nativo
        with st.container():
            st.markdown('<div style="padding: 0 4rem;">', unsafe_allow_html=True)
            
            # Conmutador de pestañas de alta velocidad
            tab_selec = st.radio("Selector_Rol", ["Administrativo", "Consulta pública"], horizontal=True, label_visibility="collapsed")
            st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
            
            if tab_selec == "Administrativo":
                usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="usr_field")
                contrasena = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="pwd_field")
                
                if st.button("➡️ Ingresar al sistema", use_container_width=True):
                    if usuario == "admin" and contrasena == "admin123":
                        st.session_state['autenticado'] = True
                        st.session_state['usuario'] = "James Jaramillo"
                        st.session_state['rol'] = "admin"
                        st.session_state['opcion_menu'] = "Inicio"
                        st.rerun()
                    else:
                        st.error("❌ Credenciales incorrectas.")
            else:
                st.markdown("""
                    <div style='text-align:center; padding: 35px 0; color:#64748b; font-family:\"Inter\",sans-serif;'>
                        <i class='fa-solid fa-circle-info' style='font-size:2.5rem; color:#0056b3; margin-bottom:15px;'></i><br>
                        <b>Formulario de Registro Habilitado Abajo</b><br>
                        Utilice el panel inferior de la plataforma para agregar estudiantes directamente al sistema.
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("""
                <div style="background-color: #f5f3ff; border: 1px solid #e9e3ff; border-radius: 12px; padding: 14px 20px; color: #5b21b6; font-size: 0.95rem; font-weight: 600; margin-top: 30px; display: flex; justify-content: space-between; align-items: center; font-family:\"Inter\",sans-serif;">
                    <span><i class="fa-regular fa-circle-question" style="color:#7c3aed; margin-right:8px; font-size:1.05rem;"></i> Soporte académico RAP</span>
                    <i class="fa-solid fa-chevron-right" style="font-size: 0.85rem;"></i>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- ESCENARIO B: ENTORNO ADMINISTRATIVO (LOGUEADO) ---
else:
    # Restablecemos scrolls globales y fijamos el CSS premium sectorizado para el menú izquierdo
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { overflow: auto !important; background-color: #fcfdfe !important; }
        div.block-container { padding: 2.5rem 4rem !important; max-width: 100% !important; }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #001f4d 0%, #00112c 100%) !important;
        }
        [data-testid="stSidebarNav"] { display: none !important; }
        
        .sidebar-brand { padding: 20px 10px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
        .user-badge { background: rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.1); }
        
        /* Ajuste estricto de botones secundarios de la barra lateral con tus espaciados de 20px */
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
        
        /* Blindaje de fuentes blancas permanente (Evita que el texto se tape en hover) */
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

    # --- ENRUTADOR GENERAL DE VISTAS ---
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