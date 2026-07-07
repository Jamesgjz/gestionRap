import streamlit as st
from modules import inicio, registro, estado_pruebas, programacion, evaluacion, dashboard

# 1. Configuración de la página en modo ancho total y limpio
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if 'opcion_menu' not in st.session_state:
    st.session_state['opcion_menu'] = "Inicio"

if 'rol' not in st.session_state:
    st.session_state['rol'] = "admin"

# --- PROCESADOR DE NAVEGACIÓN ADMINISTRATIVA (MENÚ LATERAL) ---
query_params = st.query_params
menu_click = query_params.get("view", None)
if menu_click:
    if isinstance(menu_click, list) or isinstance(menu_click, tuple):
        menu_click = menu_click[0] if len(menu_click) > 0 else "Inicio"
    st.session_state['opcion_menu'] = menu_click
    st.query_params.clear()
    st.rerun()

# --- INTERCEPCIÓN DE LOGOUT O LOGIN EN URL ---
u_auth = query_params.get("u_auth", None)
p_auth = query_params.get("p_auth", None)
if u_auth and p_auth:
    if u_auth[0] == "admin" and p_auth[0] == "admin123":
        st.session_state['autenticado'] = True
        st.session_state['usuario'] = "James Jaramillo"
        st.session_state['opcion_menu'] = "Inicio"
        st.query_params.clear()
        st.rerun()

# --- ESCENARIO A: LOGIN (SI NO ESTÁ AUTENTICADO) ---
if not st.session_state['autenticado']:
    # Fuerza la redirección limpia interna para que use la sesión de James por defecto si ejecutas local
    st.session_state['autenticado'] = True
    st.session_state['usuario'] = "James Jaramillo"
    st.rerun()

# --- ESCENARIO B: ENTORNO ADMINISTRATIVO COMPLETO (LOGUEADO) ---
else:
    # Inyección de CSS quirúrgico para calcar la barra lateral de Panel de Control.png
    st.markdown("""
        <style>
        [data-testid="stHeader"], [data-testid="stToolbar"], footer, [data-testid="stDecoration"] { display: none !important; }
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background-color: #fcfdfe !important; font-family: 'Inter', sans-serif; }
        div.block-container { padding: 2rem 3.5rem !important; max-width: 100% !important; }
        
        /* Contenedor e Identidad de la Barra Lateral */
        [data-testid="stSidebar"] { background-color: #031430 !important; width: 280px !important; }
        [data-testid="stSidebarNav"] { display: none !important; }
        
        /* Estilización Estricta de los Botones de Menú */
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 14px 20px !important;
            margin-bottom: 6px !important;
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            text-align: left !important;
            border-radius: 12px !important;
            transition: all 0.2s ease !important;
        }
        
        /* Estilo de Texto por Defecto de los Botones */
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] p,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] span {
            color: #94a3b8 !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
        }
        
        /* Efecto Hover e Item Seleccionado Activo como la Imagen 2 */
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover {
            background-color: rgba(255, 255, 255, 0.05) !important;
        }
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover p {
            color: #ffffff !important;
        }
        
        /* Clase especial forzada por CSS para marcar el botón activo según el estado interno */
        .active-menu-btn p { color: #ffffff !important; font-weight: 600 !important; }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)

    with st.sidebar:
        # Cabecera Institucional Premium del Sidebar
        st.markdown("""
            <div style="padding: 10px 5px 25px 5px; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 25px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="font-size: 1.6rem; color: #f1c40f;"><i class="fa-solid fa-graduation-cap"></i></div>
                    <div>
                        <div style="color: #ffffff; font-weight: 800; font-size: 1.15rem; letter-spacing: -0.3px; line-height: 1.2;">UNIMINUTO</div>
                        <div style="color: #38bdf8; font-weight: 600; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px;">Virtual | RAP Digital</div>
                    </div>
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 16px; margin-bottom: 30px; border: 1px solid rgba(255,255,255,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="background: #0052cc; width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700;">JJ</div>
                    <div>
                        <div style="font-weight: 700; font-size: 0.95rem; color: white;">James Jaramillo</div>
                        <div style="font-size: 0.75rem; color: #64748b;">Administrador</div>
                    </div>
                </div>
                <div style="margin-top: 10px; font-size: 0.75rem; color: #22c55e; display: flex; align-items: center; gap: 6px;"><i class="fa-solid fa-circle" style="font-size: 0.5rem;"></i> En línea</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Renderizado de opciones usando íconos nativos y control de navegación estable
        if st.button("🏠 Inicio", use_container_width=True):
            st.session_state['opcion_menu'] = "Inicio"
            st.rerun()
        if st.button("👥 Registro de Estudiantes", use_container_width=True):
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
            
        st.markdown("""
            <div style="margin-top: 5rem; background: rgba(56, 189, 248, 0.05); padding: 14px; border-radius: 14px; border: 1px solid rgba(56, 189, 248, 0.1); text-align: center;">
                <div style="color: #38bdf8; font-size: 1.2rem; margin-bottom: 4px;"><i class="fa-regular fa-circle-question"></i></div>
                <div style="color: white; font-weight: 600; font-size: 0.85rem;">¿Necesitas ayuda?</div>
                <div style="color: #94a3b8; font-size: 0.75rem; margin-top: 2px;">Mesa de ayuda RAP</div>
            </div>
        """, unsafe_allow_html=True)

    # --- ENRUTADOR GENERAL DE MÓDULOS DE VISTA ---
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