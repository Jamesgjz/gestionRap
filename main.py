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

# --- PROCESADOR DE NAVEGACIÓN RECIENTE (MENÚ LATERAL) ---
query_params = st.query_params
menu_click = query_params.get("view", None)
if menu_click:
    if isinstance(menu_click, list) or isinstance(menu_click, tuple):
        menu_click = menu_click[0] if len(menu_click) > 0 else "Inicio"
    st.session_state['opcion_menu'] = menu_click
    st.query_params.clear()
    st.rerun()

# --- ESCENARIO A: PANTALLA DE LOGIN UNIFICADA Y SIN SCROLL ---
if not st.session_state['autenticado']:
    
    # 2. INYECCIÓN DE ESTILOS GLOBALES: Centra la tarjeta y estiliza inputs nativos
    st.markdown("""
        <style>
        /* Ocultar elementos nativos de edición superiores de Streamlit */
        [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
        html, body, [data-testid="stAppViewContainer"] { background-color: #fcfdfe !important; overflow: hidden !important; }
        
        /* Ajustar el contenedor general de la página */
        div.block-container { padding: 20px 60px !important; max-width: 1200px !important; margin: 0 auto !important; }
        
        /* DISEÑO DE LA TARJETA PRINCIPAL CONECTANDO LAS COLUMNAS NATIVAS */
        div[data-testid="stColumns"] {
            background: #ffffff !important;
            border-radius: 24px !important;
            box-shadow: 0 20px 40px rgba(0, 31, 77, 0.07) !important;
            overflow: hidden !important;
            border: 1px solid #e2e8f0 !important;
            margin-top: 25px !important;
        }
        
        /* Forzar que las columnas nativas no tengan espacios extraños */
        div[data-testid="column"] { padding: 0 !important; margin: 0 !important; }
        
        /* ESTILIZACIÓN DE ENTRADAS DE TEXTO NATIVAS */
        div[data-testid="stTextInput"] label { 
            font-size: 0.9rem !important; 
            font-weight: 600 !important; 
            color: #334155 !important; 
            font-family: 'Inter', sans-serif;
        }
        div[data-testid="stTextInput"] input { 
            border-radius: 10px !important; 
            padding: 0.65rem 1rem !important; 
            border: 1px solid #cbd5e1 !important; 
            font-size: 0.95rem !important; 
            color: #0f172a !important; 
            background-color: #ffffff !important; 
        }
        
        /* Botón de ingreso principal nativo corporativo */
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
            margin-top: 15px !important; 
            transition: all 0.2s !important;
        }
        div.stButton > button:hover { background-color: #004494 !important; }
        
        /* Personalizar la barra de radio pestañas */
        div[data-testid="stRadio"] div[role="radiogroup"] { gap: 20px !important; }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)

    # 3. Barra superior estática alineada con el contenedor
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #e2e8f0; font-family: 'Inter', sans-serif;">
            <div style="color: #001f4d; line-height: 1.2;">
                <span style="font-weight: 800; font-size: 1.4rem;">MD</span><span style="font-weight: 700; font-size: 1.2rem; letter-spacing: 1px;"> UNIMINUTO</span>
                <span style="font-size: 0.85rem; font-weight: 400; color: #64748b; display: block; margin-top: -3px;">VIRTUAL</span>
            </div>
            <div style="color: #64748b; font-size: 0.9rem;">📅 06 de Julio de 2026</div>
        </div>
    """, unsafe_allow_html=True)

    # 4. DISTRIBUCIÓN SIMÉTRICA EN COLUMNAS (Evita que el formulario se caiga abajo)
    col_izquierda_banner, col_derecha_formulario = st.columns([1, 1.15])
    
    with col_izquierda_banner:
        # Renderizado del Banner Azul Premium incluyendo la CDN de FontAwesome por dentro
        html_banner = """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <div style="background: linear-gradient(135deg, #001f4d 0%, #00112c 100%); padding: 3.5rem 3rem; color: white; height: 560px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; font-family: 'Inter', sans-serif;">
            <div class="banner-top">
                <div style="width: 100%; max-width: 220px; margin-bottom: 2rem;">
                    <!-- Logo Vectorial Alternativo de alta estabilidad corporativa -->
                    <img src="https://uniminuto.edu/sites/default/files/logo-uniminuto-header.png" style="width:100%; height:auto; filter: brightness(0) invert(1);" onerror="this.src='https://upload.wikimedia.org/wikipedia/commons/0/03/Logo_Uniminuto.png';">
                </div>
                <div style="color: #38bdf8; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">RAP Digital</div>
                <div style="font-size: 2.2rem; font-weight: 800; line-height: 1.1; margin-bottom: 1.2rem;">MD UNIMINUTO<br><span style="color: #f1c40f;">VIRTUAL</span></div>
                <div style="width: 50px; height: 3px; background-color: #38bdf8; margin-bottom: 1.5rem;"></div>
                <div style="font-size: 1.05rem; color: #cbd5e1; line-height: 1.6;">Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.</div>
            </div>
            <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 1.5rem; gap: 15px;">
                <div style="text-align: center; flex: 1;">
                    <div style="background: rgba(255, 255, 255, 0.08); width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 6px auto; color: #38bdf8;"><i class="fa-solid fa-chart-line"></i></div>
                    <span style="font-size:0.85rem; font-weight:600;">Seguimiento</span>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="background: rgba(255, 255, 255, 0.08); width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 6px auto; color: #38bdf8;"><i class="fa-regular fa-clipboard"></i></div>
                    <span style="font-size:0.85rem; font-weight:600;">Evaluación</span>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="background: rgba(255, 255, 255, 0.08); width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 6px auto; color: #38bdf8;"><i class="fa-solid fa-shield-halved"></i></div>
                    <span style="font-size:0.85rem; font-weight:600;">Trazabilidad</span>
                </div>
            </div>
        </div>
        """
        components.html(html_banner, height=560, scrolling=False)
        
    with col_derecha_formulario:
        st.markdown("""
            <div style="padding: 3.5rem 3.5rem 1rem 3.5rem; font-family: 'Inter', sans-serif;">
                <h2 style="color: #0f172a; font-weight: 700; font-size: 1.9rem; margin: 0 0 4px 0;">Acceso al sistema</h2>
                <p style="color: #64748b; font-size: 0.95rem; margin: 0 0 25px 0;">Inicia sesión para continuar con RAP Digital.</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div style="padding: 0 3.5rem;">', unsafe_allow_html=True)
            
            modo_seleccionado = st.radio("Rol", ["Administrativo", "Consulta pública"], horizontal=True, label_visibility="collapsed")
            st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
            
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
                    <div style='text-align:center; padding: 35px 0; color:#64748b; font-family:\"Inter\",sans-serif;'>
                        <i class='fa-solid fa-circle-info' style='font-size:2.5rem; color:#0056b3; margin-bottom:15px;'></i><br>
                        <b>Formulario de Registro Público Habilitado</b><br>
                        Por favor, use la pestaña de consulta pública para ver el estado de sus trámites académicos.
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("""
                <div style="background-color: #f4f0ff; border: 1px solid #e0d4ff; border-radius: 10px; padding: 12px 20px; color: #4c1d95; font-size: 0.9rem; font-weight: 500; margin-top: 30px; display: flex; justify-content: space-between; align-items: center; font-family:\"Inter\",sans-serif;">
                    <span><i class="fa-regular fa-circle-question" style="color:#7c3aed; margin-right:8px;"></i> Soporte académico RAP</span>
                    <span>➔</span>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- ESCENARIO B: ENTORNO ADMINISTRATIVO (LOGUEADO) ---
else:
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
        
        /* Ajuste estricto de botones secundarios de la barra lateral */
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