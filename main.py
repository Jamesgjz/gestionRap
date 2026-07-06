import streamlit as st
import streamlit.components.v1 as components
from modules import inicio, registro, estado_pruebas, programacion, evaluacion, dashboard

# 1. Configuración de la página en modo ancho total y limpio
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

# Inicialización estricta del estado de la sesión
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if 'opcion_menu' not in st.session_state:
    st.session_state['opcion_menu'] = "Inicio"

# --- PROCESADOR DE LOGUEO NATIVO DE ALTO RENDIMIENTO ---
# Procesamos los datos de forma directa en el backend de Python
if not st.session_state['autenticado']:
    # Variables de control temporales
    if 'temp_user' not in st.session_state: st.session_state['temp_user'] = ""
    if 'temp_pass' not in st.session_state: st.session_state['temp_pass'] = ""

# --- ESCENARIO A: PANTALLA DE LOGIN ---
if not st.session_state['autenticado']:
    # Inyección de CSS de alta prioridad para ocultar barras nativas y posicionar el formulario nativo sobre el mockup
    st.markdown("""
        <style>
        /* Ocultar elementos de edición de Streamlit en el login */
        [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
        div.block-container { padding-top: 2rem !important; padding-bottom: 0rem !important; }
        
        /* Estilización de Inputs de Streamlit para acoplarlos al diseño premium */
        div[data-testid="stTextInput"] label {
            font-size: 0.9rem !important;
            font-weight: 600 !important;
            color: #334155 !important;
            margin-bottom: 4px !important;
        }
        div[data-testid="stTextInput"] input {
            border-radius: 10px !important;
            padding: 0.6rem 1rem !important;
            border: 1px solid #cbd5e1 !important;
            font-size: 0.95rem !important;
        }
        
        /* Botón de ingreso nativo corporativo */
        div.stButton > button {
            background-color: #0056b3 !important;
            color: white !important;
            width: 100% !important;
            padding: 0.8rem !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(0, 86, 179, 0.25) !important;
            margin-top: 10px !important;
            transition: all 0.2s !important;
        }
        div.stButton > button:hover {
            background-color: #004494 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Renderizado del cascarón visual estático del Mockup (Banner izquierdo y Top Bar)
    html_layout = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            html, body { margin: 0; padding: 0; width: 100%; height: 100%; background-color: #fcfdfe; font-family: 'Inter', sans-serif; box-sizing: border-box; overflow: hidden; }
            .page-wrapper { padding: 0px 40px; display: flex; flex-direction: column; height: 100vh; box-sizing: border-box; }
            .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #e2e8f0; width: 100%; height: 60px; }
            .top-logo { color: #001f4d; line-height: 1.2; }
            .top-logo .bold-md { font-weight: 800; font-size: 1.4rem; }
            .top-logo .text-uni { font-weight: 700; font-size: 1.2rem; letter-spacing: 1px; }
            .top-logo .sub-virtual { font-size: 0.85rem; font-weight: 400; color: #64748b; display: block; margin-top: -3px; }
            .top-date { color: #64748b; font-size: 0.9rem; }
            .center-container { display: flex; justify-content: center; align-items: center; flex-grow: 1; width: 100%; height: calc(100vh - 60px); padding-bottom: 20px; }
            .main-container { display: flex; width: 100%; max-width: 1150px; background: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 40px rgba(0, 31, 77, 0.07); min-height: 560px; }
            .banner-azul { flex: 1; background: linear-gradient(135deg, #001f4d 0%, #00112c 100%); padding: 3.5rem 3rem; color: white; display: flex; flex-direction: column; justify-content: space-between; }
            .logo-upload-zone { width: 100%; max-width: 220px; margin-bottom: 1.5rem; }
            .logo-upload-zone img { width: 100%; height: auto; filter: brightness(0) invert(1); }
            .banner-top .sub-marca { color: #38bdf8; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
            .banner-top .main-logo-title { font-size: 2.2rem; font-weight: 800; line-height: 1.1; margin-bottom: 1.2rem; }
            .banner-top .main-logo-title span { color: #f1c40f; }
            .banner-top .short-line { width: 50px; height: 3px; background-color: #38bdf8; margin-bottom: 1.5rem; }
            .banner-top .main-description { font-size: 1.1rem; color: #cbd5e1; line-height: 1.6; }
            .banner-features { display: flex; justify-content: space-between; border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 1.5rem; gap: 15px; }
            .feature-box { text-align: center; flex: 1; }
            .feature-icon-wrapper { background: rgba(255, 255, 255, 0.08); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 8px auto; color: #38bdf8; font-size: 1.1rem; }
            .feature-box .f-title { font-weight: 700; font-size: 0.9rem; color: white; margin-bottom: 3px; }
            .feature-box .f-desc { font-size: 0.75rem; color: #94a3b8; }
            .panel-formulario { flex: 1.1; padding: 3.5rem; display: flex; flex-direction: column; justify-content: center; background-color: #ffffff; }
            @media (max-width: 850px) { .main-container { flex-direction: column; } .banner-azul, .panel-formulario { width: 100%; padding: 2rem; } }
        </style>
    </head>
    <body>
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
                    <div class="panel-formulario">
                        <!-- El espacio del formulario se acopla dinámicamente desde Streamlit sin saltos de caja -->
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    # Desplegamos el cascarón estético de fondo
    components.html(html_layout, height=620)
    
    # Inyectamos milimétricamente el formulario real de Streamlit encima del espacio asignado
    col_vacio, col_central_form, col_vacio2 = st.columns([1.15, 1, 0.85])
    
    with col_central_form:
        st.markdown("<h2 style='color: #0f172a; margin-top: -555px; font-weight:700; font-size:1.8rem; font-family:\"Inter\", sans-serif;'>Acceso al sistema</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; font-size:0.95rem; font-family:\"Inter\", sans-serif; margin-bottom: 25px;'>Inicia sesión para continuar con RAP Digital.</p>", unsafe_allow_html=True)
        
        # Elemento selector nativo de pestañas adaptado
        tab_login = st.radio("Rol de acceso", ["Administrativo", "Consulta pública"], horizontal=True, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if tab_login == "Administrativo":
            usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="u_field")
            contrasena = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="p_field")
            
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
                <div style='text-align:center; padding: 30px 0; color:#64748b; font-family:\"Inter\", sans-serif;'>
                    <i class='fa-solid fa-circle-info' style='font-size:2.5rem; color:#0056b3; margin-bottom:15px;'></i><br>
                    <b>Formulario de Registro Habilitado Abajo</b><br>
                    Utilice el panel inferior de la plataforma para agregar estudiantes directamente al sistema.
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
            <div style="background-color: #f4f0ff; border: 1px solid #e0d4ff; border-radius: 10px; padding: 12px 20px; color: #4c1d95; font-size: 0.9rem; font-weight: 500; margin-top: 30px; display: flex; justify-content: space-between; align-items: center; font-family:\"Inter\", sans-serif;">
                <span><i class="fa-regular fa-circle-question" style="color:#7c3aed; margin-right:8px;"></i> Soporte académico RAP</span>
                <span>➔</span>
            </div>
        """, unsafe_allow_html=True)

    if tab_login == "Consulta pública":
        st.divider()
        st.subheader("📝 Formulario de Registro Público de Estudiantes")
        registro.render()

# --- ESCENARIO B: ENTORNO ADMINISTRATIVO (LOGUEADO) ---
else:
    # Filtro de CSS quirúrgico de alta especificidad para los botones de la barra lateral
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #001f4d 0%, #00112c 100%) !important;
        }
        [data-testid="stSidebarNav"] { display: none !important; }
        
        .sidebar-brand { padding: 20px 10px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
        .user-badge { background: rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.1); }
        
        /* Modificamos EXCLUSIVAMENTE los botones secundarios que estén contenidos en la barra lateral */
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            
            /* Ajustes exactos solicitados: padding interno y espaciado de 20px */
            padding: 20px !important;
            margin-bottom: 10px !important;
            
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            text-align: left !important;
            border-radius: 10px !important;
            transition: all 0.2s ease-in-out !important;
        }
        
        /* Forzar texto blanco en todo momento dentro del Sidebar (Reposo y Hover) */
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] p,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover p {
            color: #ffffff !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            margin: 0 !important;
            text-align: left !important;
            justify-content: flex-start !important;
        }
        
        /* Hover azul institucional sin alterar el texto */
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover {
            background: #0056b3 !important;
            background-color: #0056b3 !important;
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
        
        # Botones nativos estables, ahora controlados de forma limpia por el CSS sectorizado
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