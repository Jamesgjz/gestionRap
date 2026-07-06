import streamlit as st
import sqlite3
from streamlit_cookies_controller import CookieController
from modules import inicio, registro, estado_pruebas, programacion, evaluacion, dashboard

# 1. Configuración de la página en modo ancho total y limpio sin scrolls
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

# Inicialización obligatoria del controlador de cookies para evitar que F5 te saque
controller = CookieController()

# Intentar recuperar sesión de forma segura
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
        return {"solicitudes": 128, "pruebas": 56, "pendientes": 34, "cerrados": 245}

data_db = cargar_kpis_panel()

# --- ESCENARIO A: PANTALLA DE LOGIN PREMIUM CON REDISEÑO ESTÉTICO NATIVO ---
if not st.session_state['autenticado']:
    
    # 2. INYECCIÓN CSS TRANSFORMATIVA TOTAL: Reescribe la visual nativa de Streamlit a la de tu mockup
    st.markdown("""
        <style>
        /* Ocultar elementos nativos superiores de Streamlit en el Login */
        [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background-color: #f8fafc !important; overflow: hidden !important; }
        
        /* Ajustar contenedor principal */
        div.block-container { padding: 40px 80px !important; max-width: 1240px !important; margin: 0 auto !important; }
        
        /* Unificar st.columns como la tarjeta blanca flotante con sombra sutil */
        div[data-testid="stColumns"] {
            background: #ffffff !important;
            border-radius: 24px !important;
            box-shadow: 0 20px 40px rgba(15, 23, 42, 0.03) !important;
            overflow: hidden !important;
            border: 1px solid #e2e8f0 !important;
            margin-top: 15px !important;
        }
        div[data-testid="column"] { padding: 0 !important; margin: 0 !important; }
        
        /* Maquetación del Banner Azul Izquierdo (Idéntico a tu imagen de destino) */
        .banner-azul-premium {
            background: linear-gradient(180deg, #001737 0%, #00224f 100%);
            padding: 4.5rem 3.5rem;
            color: white;
            height: 610px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
            position: relative;
        }
        .banner-azul-premium::before {
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Logo_Uniminuto.png/640px-Logo_Uniminuto.png');
            background-position: bottom -10% right -25%; background-repeat: no-repeat; background-size: 85%; opacity: 0.03; pointer-events: none;
        }
        .banner-top-content { position: relative; z-index: 2; }
        .sub-marca { color: #38bdf8; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
        .main-logo-title { font-size: 2.3rem; font-weight: 800; line-height: 1.15; margin: 0 0 1.2rem 0; letter-spacing: -0.5px; }
        .main-description { font-size: 1.05rem; color: #94a3b8; line-height: 1.6; }
        
        /* Indicadores inferiores */
        .banner-features { display: flex; justify-content: space-between; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 1.8rem; gap: 10px; position: relative; z-index: 2; }
        .feature-box { text-align: center; flex: 1; display: flex; flex-direction: column; align-items: center; }
        .feature-icon-wrapper { background: rgba(255, 255, 255, 0.04); width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 10px; color: #38bdf8; font-size: 1.1rem; border: 1px solid rgba(255, 255, 255, 0.04); }
        .feature-box .f-title { font-weight: 600; font-size: 0.85rem; color: #f8fafc; }
        
        /* Contenedor del Formulario Derecho */
        .panel-formulario-real { padding: 4.5rem 4rem 1rem 4rem; font-family: 'Inter', sans-serif; box-sizing: border-box; }
        .f-access-title { color: #0f172a; font-size: 2.1rem; font-weight: 700; margin: 0 0 6px 0; letter-spacing: -0.5px; }
        .f-access-subtitle { color: #64748b; font-size: 0.95rem; margin: 0 0 0.5rem 0; }
        
        /* TRANSFORMACIÓN DE LA BARRA DE RADIO A PESTAÑAS RECTANGULARES CORPORATIVAS (Imagen 2) */
        div[data-testid="stRadio"] div[role="radiogroup"] { 
            background-color: #f1f5f9 !important; 
            padding: 6px !important; 
            border-radius: 12px !important; 
            gap: 5px !important; 
            display: flex !important;
            flex-direction: row !important;
            border: none !important;
        }
        div[data-testid="stRadio"] label[data-testid="stWidgetLabel"] { display: none !important; }
        
        /* Convertir los ítems circulares individuales en botones planos */
        div[data-testid="stRadio"] div[role="radiogroup"] > label {
            flex: 1 !important;
            background: transparent !important;
            padding: 10px 15px !important;
            border-radius: 8px !important;
            justify-content: center !important;
            align-items: center !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            border: none !important;
            margin: 0 !important;
        }
        /* Ocultar el círculo nativo de selección (Radio button dot) */
        div[data-testid="stRadio"] div[role="radiogroup"] input[type="radio"] { display: none !important; }
        div[data-testid="stRadio"] div[role="radiogroup"] div[data-testid="stMarkdownContainer"] p { 
            font-weight: 600 !important; 
            font-size: 0.95rem !important; 
            color: #64748b !important;
            margin: 0 !important;
        }
        
        /* Estilo para la pestaña seleccionada activa (Fondo blanco y sombra sutil) */
        div[data-testid="stRadio"] div[role="radiogroup"] div[data-checked="true"] {
            background-color: #ffffff !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03) !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] div[data-checked="true"] p {
            color: #0056b3 !important;
        }
        
        /* TRANSFORMACIÓN Y ABRAZO DE INPUTS NATIVOS */
        div[data-testid="stTextInput"] label { font-size: 0.95rem !important; font-weight: 600 !important; color: #334155 !important; margin-bottom: 0.4rem !important; }
        div[data-testid="stTextInput"] input { border-radius: 12px !important; padding: 0.8rem 1rem !important; border: 1px solid #cbd5e1 !important; font-size: 1rem !important; color: #0f172a !important; background-color: #ffffff !important; transition: all 0.2s !important; }
        div[data-testid="stTextInput"] input:focus { border-color: #0056b3 !important; box-shadow: 0 0 0 4px rgba(0, 86, 179, 0.08) !important; }
        
        /* Transformación del Botón de Ingreso a un Azul Rey de Bloque Completo */
        div.stButton > button {
            background-color: #0056b3 !important; color: white !important; width: 100% !important; padding: 0.95rem !important;
            border-radius: 12px !important; font-weight: 700 !important; font-size: 1.05rem !important; border: none !important;
            box-shadow: 0 4px 14px rgba(0, 86, 179, 0.15) !important; margin-top: 10px !important; transition: all 0.2s !important;
        }
        div.stButton > button:hover { background-color: #004494 !important; border: none !important; color: white !important; }
        div.stButton > button:focus { border: none !important; background-color: #004494 !important; color: white !important; }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)

    # Navbar Superior Estático Idéntico
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 15px; border-bottom: 1px solid #e2e8f0; margin-bottom: 20px; font-family: 'Inter', sans-serif;">
            <div style="display: flex; align-items: center; gap: 10px; font-weight: 800; color: #001f4d; font-size: 1.3rem;">
                <i class="fa-solid fa-graduation-cap" style="color:#0056b3;"></i>UNIMINUTO <span style="color:#0056b3;">VIRTUAL</span>
            </div>
            <div style="display: flex; align-items: center; gap: 25px; color: #1e293b;">
                <div style="position: relative; font-size: 1.25rem; color: #0056b3;"><i class="fa-regular fa-bell"></i><div style="position: absolute; top: -5px; right: -5px; background: #0056b3; color: white; border-radius: 50%; width: 16px; height: 16px; font-size: 0.65rem; display: flex; align-items: center; justify-content: center; font-weight: 700;">3</div></div>
                <div style="font-size: 1.25rem; color:#64748b;"><i class="fa-regular fa-circle-question"></i></div>
                <div style="color: #64748b; font-size: 0.9rem; font-weight: 500;"><i class="fa-regular fa-calendar"></i> 06 de Julio de 2026</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Distribución Simétrica en Columnas Nativas (Máxima velocidad de procesamiento)
    col_izq_banner, col_der_form = st.columns([1, 1.12])
    
    with col_izq_banner:
        st.markdown("""
            <div class="banner-azul-premium">
                <div class="banner-top-content">
                    <div style="font-size: 1.3rem; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 2.2rem; display: flex; align-items: center; gap: 8px;">
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
        """, unsafe_allow_html=True)
        
    with col_der_form:
        st.markdown("""
            <div class="panel-formulario-real">
                <div class="f-access-title">Acceso al sistema</div>
                <div class="f-access-subtitle">Inicia sesión para continuar con RAP Digital.</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div style="padding: 0 4rem 4rem 4rem; margin-top: -30px;">', unsafe_allow_html=True)
            
            # El radio nativo se convertirá automáticamente en las pestañas rectangulares por el CSS superior
            tab_selec = st.radio("Rol_Acceso", ["Administrativo", "Consulta pública"], horizontal=True)
            st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
            
            if tab_selec == "Administrativo":
                usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="usr_real")
                contrasena = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="pwd_real")
                
                # Botón nativo estable, procesado en memoria al instante
                if st.button("➡️ Ingresar al sistema", use_container_width=True):
                    if usuario == "admin" and contrasena == "admin123":
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
                        st.error("❌ Credenciales incorrectas.")
            else:
                st.markdown("""
                    <div style='text-align:center; padding: 35px 0; color:#64748b; font-family:\"Inter\",sans-serif;'>
                        <i class='fa-solid fa-circle-info' style='font-size:2.5rem; color:#0056b3; margin-bottom:15px;'></i><br>
                        <b>Consulta Pública Habilitada Abajo</b><br>
                        Por favor use el bloque inferior de la aplicación para revisar registros.
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
    # Restablecemos los scrolls y aplicamos el blindaje contra el hover oscuro del menú izquierdo
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
        
        /* Desactivar cajas opacas nativas en la barra lateral */
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
        
        /* Forzar tipografía blanca fija sin alteraciones */
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
        
        /* HOVER DE ALTA VISIBILIDAD: Al pasar el mouse cambia a azul corporativo sólido sin oscurecerse */
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
            st.session_state['opcion_menu'].select = "Programación"
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