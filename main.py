import streamlit as st
import streamlit.components.v1 as components
import sqlite3
from streamlit_cookies_controller import CookieController
from modules import inicio, registro, estado_pruebas, programacion, evaluacion, dashboard

# 1. Configuración de la página en modo ancho total y limpio sin scrolls
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

# Inicialización obligatoria del controlador de cookies para evitar que F5 te saque
controller = CookieController()

# Intentar recuperar sesión persistente de la cookie de forma segura
try:
    cookie_auth = controller.get('rap_session_active')
    if cookie_auth == 'true' and 'autenticado' not in st.session_state:
        st.session_state['autenticado'] = True
        st.session_state['usuario'] = controller.get('rap_user_name') or "James Jaramillo"
        st.session_state['opcion_menu'] = "Inicio"
except Exception:
    pass

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if 'opcion_menu' not in st.session_state:
    st.session_state['opcion_menu'] = "Inicio"

# --- CONSULTA REAL DE LA BASE DE DATOS (Módulo SmartExam Manager) ---
def cargar_kpis_panel():
    try:
        conn = sqlite3.connect('smart_exam.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM solicitudes WHERE estado = 'activa'")
        solicitudes = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM pruebas WHERE estado = 'programada'")
        pruebas = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM evaluaciones WHERE estado = 'pendiente'")
        pendientes = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM casos WHERE estado = 'cerrado'")
        cerrados = cursor.fetchone()[0]
        conn.close()
        return {"solicitudes": solicitudes, "pruebas": pruebas, "pendientes": pendientes, "cerrados": cerrados}
    except Exception:
        # Datos exactos de tu mockup en caso de contingencia o si la BD está vacía
        return {"solicitudes": 128, "pruebas": 56, "pendientes": 34, "cerrados": 245}

data_db = cargar_kpis_panel()

# --- ESCENARIO A: PANTALLA DE LOGIN IDÉNTICA A IMAGEN 2 ---
if not st.session_state['autenticado']:
    
    st.markdown("""
        <style>
        [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
        div.block-container { padding: 0rem !important; max-width: 100% !important; }
        html, body, [data-testid="stAppViewContainer"] { overflow: hidden !important; background-color: #f8fafc !important; }
        </style>
    """, unsafe_allow_html=True)

    # API de escucha asíncrona para interconectar el formulario con Streamlit sin fallas
    js_bridge = """
    <script>
    window.addEventListener('message', function(e) {
        if (e.data.type === 'TRIGGER_LOGIN') {
            const currentUrl = window.location.origin + window.location.pathname;
            window.parent.location.href = currentUrl + '?user_token=' + encodeURIComponent(e.data.user) + '&pass_token=' + encodeURIComponent(e.data.pass);
        }
    });
    </script>
    """
    
    # Réplica exacta del diseño premium
    html_layout_premium = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            html, body { margin: 0; padding: 0; width: 100%; height: 100%; background-color: #f8fafc; font-family: 'Inter', sans-serif; display: flex; justify-content: center; align-items: center; box-sizing: border-box; }
            .page-wrapper { width: 100%; max-width: 1200px; padding: 0 40px; display: flex; flex-direction: column; justify-content: center; margin-top: 10px; }
            
            /* Navbar Superior */
            .top-bar { display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 1px solid #e2e8f0; margin-bottom: 25px; width: 100%; }
            .top-logo { display: flex; align-items: center; gap: 10px; font-weight: 800; color: #001f4d; font-size: 1.3rem; }
            .top-logo span { color: #0056b3; }
            .right-nav-items { display: flex; align-items: center; gap: 25px; color: #1e293b; }
            .icon-badge-container { position: relative; cursor: pointer; font-size: 1.25rem; color: #0056b3; }
            .icon-badge { position: absolute; top: -5px; right: -5px; background: #0056b3; color: white; border-radius: 50%; width: 16px; height: 16px; font-size: 0.65rem; display: flex; align-items: center; justify-content: center; font-weight: 700; }
            .top-date { color: #64748b; font-size: 0.9rem; font-weight: 500; display: flex; align-items: center; gap: 8px; }
            
            /* Tarjeta de Login Unificada con más aire vertical interno */
            .main-container { display: flex; width: 100%; background: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 40px rgba(15, 23, 42, 0.03); min-height: 600px; border: 1px solid #e2e8f0; }
            
            /* Banner Azul */
            .banner-azul { flex: 1; background: linear-gradient(180deg, #001737 0%, #00224f 100%); padding: 4.5rem 3.5rem; color: white; display: flex; flex-direction: column; justify-content: space-between; position: relative; box-sizing: border-box; }
            .banner-azul::before { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Logo_Uniminuto.png/640px-Logo_Uniminuto.png'); background-position: bottom -10% right -25%; background-repeat: no-repeat; background-size: 85%; opacity: 0.03; pointer-events: none; }
            .banner-top-content { position: relative; z-index: 2; }
            .sub-marca { color: #38bdf8; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
            .main-logo-title { font-size: 2.3rem; font-weight: 800; line-height: 1.15; margin: 0 0 1.2rem 0; letter-spacing: -0.5px; }
            .main-description { font-size: 1.05rem; color: #94a3b8; line-height: 1.6; }
            
            /* Indicadores Inferiores */
            .banner-features { display: flex; justify-content: space-between; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 2rem; gap: 10px; position: relative; z-index: 2; }
            .feature-box { text-align: center; flex: 1; display: flex; flex-direction: column; align-items: center; }
            .feature-icon-wrapper { background: rgba(255, 255, 255, 0.04); width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 10px; color: #38bdf8; font-size: 1.1rem; border: 1px solid rgba(255, 255, 255, 0.04); }
            .feature-box .f-title { font-weight: 600; font-size: 0.85rem; color: #f8fafc; }
            
            /* Panel Formulario */
            .panel-formulario { flex: 1.1; padding: 4.5rem; display: flex; flex-direction: column; justify-content: center; background-color: #ffffff; box-sizing: border-box; }
            .f-access-title { color: #0f172a; font-size: 2.1rem; font-weight: 700; margin: 0 0 6px 0; letter-spacing: -0.5px; }
            .f-access-subtitle { color: #64748b; font-size: 0.95rem; margin: 0 0 2.2rem 0; }
            
            /* Pestañas */
            .mockup-tabs { display: flex; background: #f1f5f9; padding: 6px; border-radius: 12px; margin-bottom: 2.2rem; gap: 5px; }
            .tab-link { flex: 1; padding: 12px; font-size: 0.95rem; font-weight: 600; color: #64748b; border: none; border-radius: 8px; background: none; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.2s; text-decoration: none; }
            .tab-link.active { color: #0056b3; background: #ffffff; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03); }
            
            /* Inputs */
            .form-group { margin-bottom: 1.6rem; }
            .form-group label { display: block; font-size: 0.95rem; font-weight: 600; color: #334155; margin-bottom: 0.6rem; }
            .input-with-icon { display: flex; align-items: center; position: relative; }
            .input-with-icon i { position: absolute; left: 16px; color: #94a3b8; font-size: 1.1rem; }
            .form-group input { width: 100%; padding: 0.85rem 1rem 0.85rem 3rem; border-radius: 12px; border: 1px solid #cbd5e1; font-size: 1rem; color: #0f172a; box-sizing: border-box; background-color: #ffffff; transition: all 0.2s; }
            .form-group input:focus { outline: none; border-color: #0056b3; box-shadow: 0 0 0 4px rgba(0, 86, 179, 0.08); }
            
            /* Botón de Ingreso */
            .btn-submit-action { background-color: #0056b3; color: white; width: 100%; border: none; padding: 1rem; border-radius: 12px; font-size: 1.05rem; font-weight: 700; cursor: pointer; box-shadow: 0 4px 14px rgba(0, 86, 179, 0.15); display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.2s; margin-top: 5px; }
            .btn-submit-action:hover { background-color: #004494; }
            
            /* Caja de Soporte Violeta */
            .box-support-footer { background-color: #f5f3ff; border: 1px solid #e9e3ff; border-radius: 12px; padding: 14px 20px; color: #5b21b6; font-size: 0.95rem; font-weight: 600; margin-top: 2.2rem; display: flex; justify-content: space-between; align-items: center; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="page-wrapper">
            <div class="top-bar">
                <div class="top-logo"><i class="fa-solid fa-graduation-cap" style="color:#0056b3; margin-right:8px;"></i>UNIMINUTO <span>VIRTUAL</span></div>
                <div class="right-nav-items">
                    <div class="icon-badge-container"><i class="fa-regular fa-bell"></i><div class="icon-badge">3</div></div>
                    <div style="font-size: 1.25rem; cursor:pointer; color:#64748b;"><i class="fa-regular fa-circle-question"></i></div>
                    <div class="top-date"><i class="fa-regular fa-calendar"></i> 06 de Julio de 2026</div>
                </div>
            </div>
            <div class="main-container">
                <div class="banner-azul">
                    <div class="banner-top-content">
                        <div style="font-size: 1.3rem; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 2rem; display: flex; align-items: center; gap: 8px;">
                            <i class="fa-solid fa-shield-halved" style="color:#38bdf8;"></i> RAP Digital
                        </div>
                        <div class="sub-marca">RAP Digital</div>
                        <h1 class="main-logo-title">UNIMINUTO<br><span style="color:#f1c40f;">VIRTUAL</span></h1>
                        <div style="width: 45px; height: 3px; background-color: #38bdf8; margin-bottom: 1.8rem; border-radius: 2px;"></div>
                        <p class="main-description">Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.</p>
                    </div>
                    <div class="banner-features">
                        <div class="feature-box"><div class="feature-icon-wrapper"><i class="fa-solid fa-chart-line"></i></div><span class="f-title">Seguimiento</span></div>
                        <div class="feature-box"><div class="feature-icon-wrapper"><i class="fa-regular fa-clipboard"></i></div><span class="f-title">Evaluación</span></div>
                        <div class="feature-box"><div class="feature-icon-wrapper"><i class="fa-regular fa-circle-check"></i></div><span class="f-title">Trazabilidad<br><span style="font-size:0.75rem; font-weight:400; color:#94a3b8;">académica</span></span></div>
                    </div>
                </div>
                <div class="panel-formulario">
                    <div class="form-header">
                        <h2 class="f-access-title">Acceso al sistema</h2>
                        <p class="f-access-subtitle">Inicia sesión para continuar con RAP Digital.</p>
                    </div>
                    <div class="mockup-tabs">
                        <a href="#" class="tab-link active"><i class="fa-regular fa-user"></i> Administrativo</a>
                        <a href="#" class="tab-link"><i class="fa-solid fa-globe"></i> Consulta pública</a>
                    </div>
                    <form onsubmit="event.preventDefault(); window.parent.postMessage({type: 'TRIGGER_LOGIN', user: document.getElementById('usr').value, pass: document.getElementById('pwd').value}, '*');">
                        <div class="form-group">
                            <label>Usuario</label>
                            <div class="input-with-icon">
                                <i class="fa-regular fa-user"></i>
                                <input type="text" id="usr" placeholder="Ingresa tu usuario" required>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Contraseña</label>
                            <div class="input-with-icon">
                                <i class="fa-solid fa-lock"></i>
                                <input type="password" id="pwd" placeholder="Ingresa tu contraseña" required>
                            </div>
                        </div>
                        <button type="submit" class="btn-submit-action"><i class="fa-solid fa-arrow-right-to-bracket"></i> Ingresar al sistema</button>
                    </form>
                    <div class="box-support-footer">
                        <span><i class="fa-regular fa-circle-question" style="color:#7c3aed; margin-right:8px; font-size:1.05rem;"></i> Soporte académico RAP</span>
                        <i class="fa-solid fa-chevron-right" style="font-size: 0.85rem;"></i>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    # CORRECCIÓN DE ALTURA: Pasamos a height=760 para darle el aire perfecto abajo y no recortar nada
    components.html(html_layout_premium + js_bridge, height=760, scrolling=False)


    # CORRECCIÓN DE PARÁMETROS SEGUROS: Conversión a diccionario puro de Python
    params_dict = st.query_params.to_dict()
    user_token = params_dict.get("user_token", None)
    pass_token = params_dict.get("pass_token", None)
            
    if user_token and pass_token:
        if user_token == "admin" and pass_token == "admin123":
            st.query_params.clear()
            try:
                controller.set('rap_session_active', 'true')
                controller.set('rap_user_name', "James Jaramillo")
            except Exception:
                pass
            st.session_state['autenticado'] = True
            st.session_state['usuario'] = "James Jaramillo"
            st.session_state['opcion_menu'] = "Inicio"
            st.rerun()
        else:
            st.sidebar.error("❌ Credenciales incorrectas.")

# --- ESCENARIO B: ENTORNO ADMINISTRATIVO (LOGUEADO) ---
else:
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
        
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
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
            transition: all 0.2s ease-in-out !important;
        }
        
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] p,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] span,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] div,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover p,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:focus p {
            color: #ffffff !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            margin: 0 !important;
            text-align: left !important;
        }
        
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:focus,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:active {
            background-color: #0056b3 !important;
            background: #0056b3 !important;
            color: #ffffff !important;
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
            try:
                controller.remove('rap_session_active')
                controller.remove('rap_user_name')
            except Exception:
                pass
            st.session_state['autenticado'] = False
            st.rerun()

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