import streamlit as st
from modules import inicio, registro, estado_pruebas, programacion, evaluacion, dashboard

# 1. Configuración limpia de la página en modo ancho total sin barras de scroll
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

# Inicialización estricta de variables de sesión
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if 'opcion_menu' not in st.session_state:
    st.session_state['opcion_menu'] = "Inicio"

if 'modo_login' not in st.session_state:
    st.session_state['modo_login'] = "admin"

# --- PROCESADOR DE NAVEGACIÓN RECIENTE (MENÚ LATERAL) ---
query_params = st.query_params
menu_click = query_params.get("view", None)
if menu_click:
    if isinstance(menu_click, list) or isinstance(menu_click, tuple):
        menu_click = menu_click[0] if len(menu_click) > 0 else "Inicio"
    st.session_state['opcion_menu'] = menu_click
    st.query_params.clear()
    st.rerun()

# --- ESCENARIO A: PANTALLA DE LOGIN PREMIUM SIN SCROLLS ---
if not st.session_state['autenticado']:
    
    # 2. INYECCIÓN CSS CORPORATIVA: Limpia cabeceras, elimina scrolls y maqueta la tarjeta centradora
    st.markdown("""
        <style>
        /* Desactivar elementos nativos superiores de Streamlit para el Login */
        [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
        html, body, [data-testid="stAppViewContainer"] { overflow: hidden !important; background-color: #fcfdfe !important; }
        .block-container { padding: 0 !important; max-width: 100% !important; }
        
        /* Contenedor Cascarón del Layout Principal */
        .page-wrapper { padding: 20px 40px; display: flex; flex-direction: column; height: 100vh; box-sizing: border-box; font-family: 'Inter', sans-serif; }
        .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #e2e8f0; height: 60px; box-sizing: border-box; }
        .top-logo { color: #001f4d; font-family: 'Inter', sans-serif; }
        .top-logo .bold-md { font-weight: 800; font-size: 1.4rem; }
        .top-logo .text-uni { font-weight: 700; font-size: 1.2rem; letter-spacing: 1px; }
        .top-logo .sub-virtual { font-size: 0.85rem; font-weight: 400; color: #64748b; display: block; margin-top: -3px; }
        .top-date { color: #64748b; font-size: 0.9rem; }
        
        .center-container { display: flex; justify-content: center; align-items: center; flex-grow: 1; height: calc(100vh - 80px); }
        .main-container { display: flex; width: 100%; max-width: 1150px; background: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 40px rgba(0, 31, 77, 0.07); height: 560px; }
        
        /* Mitad Izquierda: Banner Azul Universitario */
        .banner-azul { flex: 1; background: linear-gradient(135deg, #001f4d 0%, #00112c 100%); padding: 3.5rem 3rem; color: white; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; }
        .logo-upload-zone img { width: 100%; max-width: 220px; height: auto; filter: brightness(0) invert(1); }
        .banner-top .sub-marca { color: #38bdf8; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
        .banner-top .main-logo-title { font-size: 2.2rem; font-weight: 800; line-height: 1.1; margin-bottom: 1.2rem; }
        .banner-top .main-logo-title span { color: #f1c40f; }
        .banner-top .short-line { width: 50px; height: 3px; background-color: #38bdf8; margin-bottom: 1.5rem; }
        .banner-top .main-description { font-size: 1.05rem; color: #cbd5e1; line-height: 1.6; }
        .banner-features { display: flex; justify-content: space-between; border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 1.5rem; gap: 15px; }
        .feature-box { text-align: center; flex: 1; }
        .feature-icon-wrapper { background: rgba(255, 255, 255, 0.08); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 8px auto; color: #38bdf8; font-size: 1.1rem; }
        .feature-box .f-title { font-weight: 700; font-size: 0.9rem; color: white; margin-bottom: 2px; }
        .feature-box .f-desc { font-size: 0.75rem; color: #94a3b8; }
        
        /* Mitad Derecha: Espacio Base del Formulario */
        .panel-formulario-vacio { flex: 1.1; background-color: #ffffff; padding: 3.5rem; display: flex; flex-direction: column; justify-content: center; box-sizing: border-box; }
        
        /* ESTILIZACIÓN DE ENTRADAS NATIVAS DE PYTHON */
        div[data-testid="stTextInput"] label { font-size: 0.9rem !important; font-weight: 600 !important; color: #334155 !important; }
        div[data-testid="stTextInput"] input { border-radius: 10px !important; padding: 0.65rem 1rem !important; border: 1px solid #cbd5e1 !important; font-size: 0.95rem !important; color: #0f172a !important; }
        
        /* Botón de envío principal */
        div.stButton > button {
            background-color: #0056b3 !important; color: white !important; width: 100% !important; padding: 0.8rem !important;
            border-radius: 10px !important; font-weight: 700 !important; font-size: 1rem !important; border: none !important;
            box-shadow: 0 4px 12px rgba(0, 86, 179, 0.25) !important; margin-top: 15px !important; transition: all 0.2s !important;
        }
        div.stButton > button:hover { background-color: #004494 !important; }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)

    # 3. Estructura visual externa (Fondo y Banner Izquierdo)
    st.markdown("""
        <div class="page-wrapper">
            <div class="top-bar">
                <div class="top-logo"><span class="bold-md">MD</span><span class="text-uni"> UNIMINUTO</span><span class="sub-virtual">VIRTUAL</span></div>
                <div class="top-date">📅 06 de Julio de 2026</div>
            </div>
            <div class="center-container">
                <div class="main-container">
                    <div class="banner-azul">
                        <div class="banner-top">
                            <div class="logo-upload-zone"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Logo_Uniminuto.png/640px-Logo_Uniminuto.png"></div>
                            <div class="sub-marca">RAP Digital</div>
                            <div class="main-logo-title">MD UNIMINUTO<br><span>VIRTUAL</span></div>
                            <div class="short-line"></div>
                            <div class="main-description">Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.</div>
                        </div>
                        <div class="banner-features">
                            <div class="feature-box"><div class="feature-icon-wrapper"><i class="fa-solid fa-chart-line"></i></div><div class="f-title">Seguimiento</div><span class="f-desc">Tiempo real</span></div>
                            <div class="feature-box"><div class="feature-icon-wrapper"><i class="fa-regular fa-clipboard"></i></div><div class="f-title">Evaluación</div><span class="f-desc">Asignación ágil</span></div>
                            <div class="feature-box"><div class="feature-icon-wrapper"><i class="fa-solid fa-shield-halved"></i></div><div class="f-title">Trazabilidad</div><span class="f-desc">Históricos seguros</span></div>
                        </div>
                    </div>
                    <div class="panel-formulario-vacio">
                        <!-- Posicionador para los inputs nativos colgados abajo -->
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 4. Inyección matemática de los campos nativos de Python encima de la mitad derecha del contenedor
    col_vacio, col_formulario_real, col_vacio2 = st.columns([1.16, 1, 0.84])
    
    with col_formulario_real:
        st.markdown("<h2 style='color: #0f172a; margin-top: -555px; font-weight:700; font-size:1.9rem; font-family:\"Inter\",sans-serif; margin-bottom:4px;'>Acceso al sistema</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; font-size:0.95rem; font-family:\"Inter\",sans-serif; margin-bottom: 25px;'>Inicia sesión para continuar con RAP Digital.</p>", unsafe_allow_html=True)
        
        # Pestañas conmutadoras nativas con persistencia en el backend
        modo_seleccionado = st.radio("Rol", ["Administrativo", "Consulta pública"], horizontal=True, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if modo_seleccionado == "Administrativo":
            usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="usr_real")
            contrasena = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="pwd_real")
            
            if st.button("🚪 Ingresar al sistema", use_container_width=True):
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
                <div style='text-align:center; padding: 25px 0; color:#64748b; font-family:\"Inter\",sans-serif;'>
                    <i class='fa-solid fa-circle-info' style='font-size:2.5rem; color:#0056b3; margin-bottom:15px;'></i><br>
                    <b>Formulario de Registro Habilitado Abajo</b><br>
                    Utilice el panel inferior de la plataforma para agregar estudiantes directamente al sistema.
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
            <div style="background-color: #f4f0ff; border: 1px solid #e0d4ff; border-radius: 10px; padding: 12px 20px; color: #4c1d95; font-size: 0.9rem; font-weight: 500; margin-top: 25px; display: flex; justify-content: space-between; align-items: center; font-family:\"Inter\",sans-serif;">
                <span><i class="fa-regular fa-circle-question" style="color:#7c3aed; margin-right:8px;"></i> Soporte académico RAP</span>
                <span>➔</span>
            </div>
        """, unsafe_allow_html=True)

    if modo_seleccionado == "Consulta pública":
        st.markdown("<div style='margin-top: 80px;'></div>", unsafe_allow_html=True)
        st.divider()
        st.subheader("📝 Formulario de Registro Público de Estudiantes")
        registro.render()

# --- ESCENARIO B: ENTORNO ADMINISTRATIVO (LOGUEADO) ---
else:
    # Restablecemos las barras de scroll globales únicamente para el entorno de trabajo interno
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] { overflow: auto !important; background-color: #fcfdfe !important; }
        div.block-container { padding: 2.5rem 4rem !important; }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #001f4d 0%, #00112c 100%) !important;
        }
        [data-testid="stSidebarNav"] { display: none !important; }
        
        .sidebar-brand { padding: 20px 10px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
        .user-badge { background: rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.1); }
        
        /* Configuración estricta de botones secundarios de la barra lateral con tus espaciados */
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
        
        /* Blindaje de fuentes blancas permanente (Evita el bloqueo en hover) */
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
        
        # Botones estables de navegación
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