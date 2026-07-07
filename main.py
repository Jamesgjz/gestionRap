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

if 'rol' not in st.session_state:
    st.session_state['rol'] = None

# --- INTERCEPCIÓN DE CREDENCIALES DESDE EL FORMULARIO PREMIUM ---
query_params = st.query_params
u_auth = query_params.get("u_auth", None)
p_auth = query_params.get("p_auth", None)
auth_mode = query_params.get("auth_mode", "admin")

if u_auth and p_auth:
    if isinstance(u_auth, list) or isinstance(u_auth, tuple): u_auth = u_auth[0]
    if isinstance(p_auth, list) or isinstance(p_auth, tuple): p_auth = p_auth[0]
    if isinstance(auth_mode, list) or isinstance(auth_mode, tuple): auth_mode = auth_mode[0]
    
    # Validación dinámica según la pestaña seleccionada
    if auth_mode == "admin" and u_auth == "admin" and p_auth == "admin123":
        st.session_state['autenticado'] = True
        st.session_state['usuario'] = "James Jaramillo"
        st.session_state['rol'] = "admin"
        st.session_state['opcion_menu'] = "Inicio"
        st.query_params.clear()
        st.rerun()
    elif auth_mode == "publico" and u_auth == "publico" and p_auth == "publico123":
        st.session_state['autenticado'] = True
        st.session_state['usuario'] = "Consultor Ciudadano"
        st.session_state['rol'] = "publico"
        st.session_state['opcion_menu'] = "Inicio"
        st.query_params.clear()
        st.rerun()
    else:
        st.error("❌ Credenciales inválidas para el modo seleccionado.")
        st.query_params.clear()

# --- PROCESADOR DE NAVEGACIÓN ADMINISTRATIVA (MENÚ LATERAL) ---
menu_click = query_params.get("view", None)
if menu_click:
    if isinstance(menu_click, list) or isinstance(menu_click, tuple):
        menu_click = menu_click[0] if len(menu_click) > 0 else "Inicio"
    st.session_state['opcion_menu'] = menu_click
    st.query_params.clear()
    st.rerun()

# --- ESCENARIO A: PANTALLA DE LOGIN EN ALTA FIDELIDAD ---
if not st.session_state['autenticado']:
    
    # Ocultar cabeceras y forzar el lienzo limpio del navegador sin márgenes rotos
    st.markdown("""
        <style>
        [data-testid="stHeader"], [data-testid="stToolbar"], footer, [data-testid="stDecoration"] { display: none !important; }
        div.block-container { padding: 0rem !important; max-width: 100% !important; }
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background-color: #f8fafc !important; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        
        /* Contenedor Global Centrado */
        .page-wrapper { padding: 25px 50px; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }
        .top-bar { display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 1px solid #e2e8f0; margin-bottom: 30px; }
        .right-nav-items { display: flex; align-items: center; gap: 25px; color: #1e293b; }
        .icon-badge-container { position: relative; cursor: pointer; font-size: 1.3rem; color: #0056b3; }
        .icon-badge { position: absolute; top: -5px; right: -5px; background: #0056b3; color: white; border-radius: 50%; width: 16px; height: 16px; font-size: 0.65rem; display: flex; align-items: center; justify-content: center; font-weight: 700; }
        
        /* Tarjeta de Diseño Unificado */
        .center-container { display: flex; justify-content: center; align-items: center; flex-grow: 1; padding: 20px 0; }
        .main-container { display: flex; width: 100%; max-width: 1140px; height: 620px; background: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 50px rgba(15, 23, 42, 0.06); border: 1px solid #e2e8f0; }
        
        /* Mitad Izquierda: Banner Azul Premium */
        .banner-azul { flex: 1; background: linear-gradient(180deg, #001737 0%, #00224f 100%); padding: 3.5rem; color: white; display: flex; flex-direction: column; justify-content: space-between; position: relative; box-sizing: border-box; }
        
        /* Mitad Derecha: Formulario */
        .panel-formulario { flex: 1.1; padding: 4.5rem; display: flex; flex-direction: column; justify-content: center; background-color: #ffffff; box-sizing: border-box; }
        
        /* Pestañas de Selección Interactivas */
        .mockup-tabs { display: flex; background: #f1f5f9; padding: 6px; border-radius: 12px; margin-bottom: 2rem; gap: 5px; }
        .tab-link { flex: 1; padding: 12px; font-size: 0.95rem; font-weight: 600; color: #64748b; border: none; border-radius: 8px; background: none; text-align: center; display: flex; align-items: center; justify-content: center; gap: 10px; cursor: pointer; transition: all 0.2s; }
        .tab-link.active { color: #0056b3; background: #ffffff; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04); }
        
        /* Inputs Estilizados */
        .form-group { margin-bottom: 1.5rem; }
        .form-group label { display: block; font-size: 0.95rem; font-weight: 600; color: #334155; margin-bottom: 0.5rem; text-align: left; }
        .input-with-icon { display: flex; align-items: center; position: relative; }
        .input-with-icon i { position: absolute; left: 16px; color: #94a3b8; font-size: 1.1rem; }
        .form-group input { width: 100%; padding: 0.85rem 1rem 0.85rem 3rem; border-radius: 12px; border: 1px solid #cbd5e1; font-size: 1rem; color: #0f172a; box-sizing: border-box; outline: none; transition: all 0.2s; }
        .form-group input:focus { border-color: #0056b3; box-shadow: 0 0 0 4px rgba(0, 86, 179, 0.08); }
        
        /* Botón de Acción */
        .btn-submit-action { background-color: #0047ff; color: white; width: 100%; border: none; padding: 1rem; border-radius: 12px; font-size: 1.05rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: 0 4px 14px rgba(0, 71, 255, 0.2); }
        .btn-submit-action:hover { background-color: #0036d9; }
        
        /* Footer de Soporte */
        .box-support-footer { background-color: #f5f3ff; border: 1px solid #e9e3ff; border-radius: 12px; padding: 14px 20px; color: #5b21b6; font-size: 0.95rem; font-weight: 600; margin-top: 2rem; display: flex; justify-content: space-between; align-items: center; }
        
        .banner-features { display: flex; justify-content: space-between; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 1.5rem; gap: 10px; }
        .feature-box { text-align: center; flex: 1; display: flex; flex-direction: column; align-items: center; }
        .feature-icon-wrapper { background: rgba(255, 255, 255, 0.05); width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 8px; color: #38bdf8; font-size: 1.1rem; }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        
        <script>
        function seleccionarPestana(modo) {
            document.getElementById('auth_mode').value = mode;
            const btnAdmin = document.getElementById('btn-tab-admin');
            const btnPublic = document.getElementById('btn-tab-publico');
            
            if (modo === 'admin') {
                btnAdmin.classList.add('active');
                btnPublic.classList.remove('active');
            } else {
                btnPublic.classList.add('active');
                btnAdmin.classList.remove('active');
            }
        }
        </script>
    """, unsafe_allow_html=True)

    # Estructura del HTML Maquetado en una sola pieza limpia y reactiva
    st.markdown("""
<div class="page-wrapper">
<div class="top-bar">
<div style="display: flex; align-items: center; gap: 10px;">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Logo_Uniminuto.png/640px-Logo_Uniminuto.png" style="height:45px; width:auto;">
</div>
<div class="right-nav-items">
<div class="icon-badge-container"><i class="fa-regular fa-bell"></i><div class="icon-badge">3</div></div>
<div style="font-size: 1.3rem; cursor:pointer; color:#64748b;"><i class="fa-regular fa-circle-question"></i></div>
<div style="color: #64748b; font-size: 0.9rem; font-weight: 500;"><i class="fa-regular fa-calendar"></i> 21 de mayo de 2025</div>
</div>
</div>
<div class="center-container">
<div class="main-container">
<div class="banner-azul">
<div>
<div style="font-size: 1.4rem; font-weight: 800; letter-spacing: 0.5px; margin-bottom: 2rem; display: flex; align-items: center; gap: 8px;">
<i class="fa-solid fa-graduation-cap" style="color:#38bdf8;"></i> MD UNIMINUTO
</div>
<div style="color: #38bdf8; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">RAP Digital</div>
<h1 style="font-size: 2.3rem; font-weight: 800; line-height: 1.15; margin: 0 0 1.2rem 0;">UNIMINUTO<br><span style="color:#f1c40f; font-size:1.8rem;">VIRTUAL</span></h1>
<div style="width: 45px; height: 3px; background-color: #38bdf8; margin-bottom: 1.5rem; border-radius: 2px;"></div>
<p style="font-size: 1.05rem; color: #94a3b8; line-height: 1.6; margin: 0;">Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.</p>
</div>
<div class="banner-features">
<div class="feature-box"><div class="feature-icon-wrapper"><i class="fa-solid fa-chart-line"></i></div><span style="color:#f8fafc; font-size:0.85rem; font-weight:600;">Seguimiento</span></div>
<div class="feature-box"><div class="feature-icon-wrapper"><i class="fa-regular fa-clipboard"></i></div><span style="color:#f8fafc; font-size:0.85rem; font-weight:600;">Evaluación</span></div>
<div class="feature-box"><div class="feature-icon-wrapper"><i class="fa-regular fa-circle-check"></i></div><span style="color:#f8fafc; font-size:0.85rem; font-weight:600; text-align:center;">Trazabilidad<br><span style="font-size:0.75rem; color:#94a3b8; font-weight:400;">académica</span></span></div>
</div>
</div>
<div class="panel-formulario">
<div style="margin-bottom: 2rem;">
<h2 style="color: #0f172a; font-size: 2rem; font-weight: 700; margin: 0 0 6px 0;">Acceso al sistema</h2>
<p style="color: #64748b; font-size: 0.95rem; margin: 0;">Inicia sesión para continuar con RAP Digital.</p>
</div>
<div class="mockup-tabs">
<button type="button" id="btn-tab-admin" class="tab-link active" onclick="seleccionarPestana('admin')"><i class="fa-regular fa-user"></i> Administrativo</button>
<button type="button" id="btn-tab-publico" class="tab-link" onclick="seleccionarPestana('publico')"><i class="fa-solid fa-globe"></i> Consulta pública</button>
</div>
<form action="/" method="GET">
<input type="hidden" id="auth_mode" name="auth_mode" value="admin">
<div class="form-group">
<label>Usuario</label>
<div class="input-with-icon">
<i class="fa-regular fa-user"></i>
<input type="text" name="u_auth" placeholder="Ingresa tu usuario" required>
</div>
</div>
<div class="form-group">
<label>Contraseña</label>
<div class="input-with-icon">
<i class="fa-solid fa-lock"></i>
<input type="password" name="p_auth" placeholder="Ingresa tu contraseña" required>
</div>
</div>
<button type="submit" class="btn-submit-action"><i class="fa-solid fa-arrow-right-to-bracket"></i> Ingresar al sistema</button>
</form>
<div class="box-support-footer">
<span><i class="fa-regular fa-circle-question" style="color:#7c3aed; margin-right:8px;"></i> Soporte académico RAP</span>
<i class="fa-solid fa-chevron-right" style="font-size: 0.85rem;"></i>
</div>
</div>
</div>
</div>
</div>
    """, unsafe_allow_html=True)

# --- ESCENARIO B: ENTORNO ADMINISTRATIVO COMPLETO (LOGUEADO) ---
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
        
        # Etiqueta de rol dinámica en la tarjeta de perfil lateral
        badge_rol = "Administrador" if st.session_state.get('rol') == "admin" else "Consulta Pública"
        
        st.markdown(f"""
            <div class="user-badge">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="background:#38bdf8; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white;"><i class="fa-regular fa-user"></i></div>
                    <div>
                        <div style="font-weight:700; font-size:0.95rem; color:white;">{st.session_state['usuario']}</div>
                        <div style="font-size:0.75rem; color:#94a3b8;">{badge_rol}</div>
                    </div>
                </div>
                <div style="margin-top:10px; font-size:0.75rem; color:#22c55e;"><i class="fa-solid fa-circle" style="font-size:0.6rem; margin-right:5px;"></i> En línea</div>
            </div>
        """, unsafe_allow_html=True)
        
        # --- MENÚ LATERAL FILTRADO POR ROL ---
        if st.button("🏠 Inicio", use_container_width=True):
            st.session_state['opcion_menu'] = "Inicio"
            st.rerun()
            
        # Solo el Administrador tiene acceso a los módulos de gestión y parametrización académica
        if st.session_state.get('rol') == "admin":
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
                
        # El módulo de Dashboards y KPIs analíticos queda disponible para ambas opciones
        if st.button("📊 Dashboard / KPIs", use_container_width=True):
            st.session_state['opcion_menu'] = "Dashboard / KPIs"
            st.rerun()
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state['autenticado'] = False
            st.session_state['rol'] = None
            st.rerun()

    # --- ENRUTADOR GENERAL DE VISTAS MÓDULO POR MÓDULO ---
    opcion = st.session_state['opcion_menu']

    if opcion == "Inicio":
        inicio.render()
    elif opcion == "Registro Estudiantes" and st.session_state.get('rol') == "admin":
        registro.render()
    elif opcion == "Estado de Pruebas" and st.session_state.get('rol') == "admin":
        estado_pruebas.render()
    elif opcion == "Programación" and st.session_state.get('rol') == "admin":
        programacion.render()
    elif opcion == "Evaluación" and st.session_state.get('rol') == "admin":
        evaluacion.render()
    elif opcion == "Dashboard / KPIs":
        dashboard.render()