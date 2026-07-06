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

# --- PROCESADOR DE LOGUEO LIMPIO (Previene que se sobreponga) ---
# --- PROCESADOR DE LOGUEO LIMPIO (Previene que se sobreponga y extrae el string) ---
query_params = st.query_params

if "form_usuario" in query_params and "form_pass" in query_params:
    # Obtenemos el primer elemento de la lista para asegurar que sea un string puro
    u_ingresado = query_params["form_usuario"]
    p_ingresado = query_params["form_pass"]
    
    # Si viene como lista o tupla por la URL, extraemos el primer índice
    if isinstance(u_ingresado, list) or isinstance(u_ingresado, tuple):
        u_ingresado = u_ingresado[0] if len(u_ingresado) > 0 else ""
    if isinstance(p_ingresado, list) or isinstance(p_ingresado, tuple):
        p_ingresado = p_ingresado[0] if len(p_ingresado) > 0 else ""

    if u_ingresado == "admin" and p_ingresado == "admin123":
        st.query_params.clear() # Limpiamos la URL para evitar bucles de sobreposición
        st.session_state['autenticado'] = True
        st.session_state['usuario'] = "James Jaramillo"
        st.session_state['rol'] = "admin"
        st.session_state['opcion_menu'] = "Inicio" 
        st.rerun()
    else:
        st.sidebar.error("❌ Credenciales incorrectas.")

# --- ESCENARIO A: PANTALLA DE LOGIN ---
if not st.session_state['autenticado']:
    modo_actual = query_params.get("modo", "admin")
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; background-color: #fcfdfe; font-family: 'Inter', sans-serif; box-sizing: border-box; overflow-x: hidden; }}
            .page-wrapper {{ padding: 10px 40px; display: flex; flex-direction: column; min-height: 100vh; box-sizing: border-box; }}
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 30px; width: 100%; }}
            .top-logo {{ color: #001f4d; line-height: 1.2; }}
            .top-logo .bold-md {{ font-weight: 800; font-size: 1.4rem; }}
            .top-logo .text-uni {{ font-weight: 700; font-size: 1.2rem; letter-spacing: 1px; }}
            .top-logo .sub-virtual {{ font-size: 0.85rem; font-weight: 400; color: #64748b; display: block; margin-top: -3px; }}
            .top-date {{ color: #64748b; font-size: 0.9rem; }}
            .center-container {{ display: flex; justify-content: center; align-items: center; flex-grow: 1; width: 100%; padding-bottom: 40px; }}
            .main-container {{ display: flex; width: 100%; max-width: 1150px; background: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 40px rgba(0, 31, 77, 0.07); min-height: 560px; }}
            .banner-azul {{ flex: 1; background: linear-gradient(135deg, #001f4d 0%, #00112c 100%); padding: 3.5rem 3rem; color: white; display: flex; flex-direction: column; justify-content: space-between; }}
            .logo-upload-zone {{ width: 100%; max-width: 220px; margin-bottom: 2rem; }}
            .logo-upload-zone img {{ width: 100%; height: auto; object-fit: contain; filter: brightness(0) invert(1); }}
            .banner-top .sub-marca {{ color: #38bdf8; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }}
            .banner-top .main-logo-title {{ font-size: 2.2rem; font-weight: 800; line-height: 1.1; margin-bottom: 1.2rem; }}
            .banner-top .main-logo-title span {{ color: #f1c40f; }}
            .banner-top .short-line {{ width: 50px; height: 3px; background-color: #38bdf8; margin-bottom: 1.8rem; }}
            .banner-top .main-description {{ font-size: 1.1rem; color: #cbd5e1; line-height: 1.6; }}
            .banner-features {{ display: flex; justify-content: space-between; border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 2rem; gap: 15px; }}
            .feature-box {{ text-align: center; flex: 1; }}
            .feature-icon-wrapper {{ background: rgba(255, 255, 255, 0.08); width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto; color: #38bdf8; font-size: 1.2rem; }}
            .feature-box .f-title {{ font-weight: 700; font-size: 0.95rem; color: white; margin-bottom: 3px; }}
            .feature-box .f-desc {{ font-size: 0.8rem; color: #94a3b8; }}
            .panel-formulario {{ flex: 1.1; padding: 4rem; display: flex; flex-direction: column; justify-content: center; background-color: #ffffff; }}
            .form-header .f-access-title {{ color: #0f172a; font-size: 2rem; font-weight: 700; margin: 0 0 5px 0; }}
            .form-header .f-access-subtitle {{ color: #64748b; font-size: 0.95rem; margin: 0 0 2.5rem 0; }}
            .mockup-tabs {{ display: flex; border-bottom: 1px solid #e2e8f0; margin-bottom: 2rem; gap: 5px; }}
            .tab-link {{ padding: 10px 18px; font-size: 0.95rem; font-weight: 600; color: #64748b; border: none; border-bottom: 2px solid transparent; background: none; cursor: pointer; display: flex; align-items: center; gap: 8px; text-decoration: none; transition: all 0.2s; }}
            .tab-link.active {{ color: #0056b3; border-bottom: 2px solid #0056b3; }}
            .form-group {{ margin-bottom: 1.5rem; }}
            .form-group label {{ display: block; font-size: 0.9rem; font-weight: 600; color: #334155; margin-bottom: 0.5rem; }}
            .input-with-icon {{ display: flex; align-items: center; position: relative; }}
            .input-with-icon i {{ position: absolute; left: 15px; color: #94a3b8; font-size: 1.1rem; }}
            .form-group input {{ width: 100%; padding: 0.8rem 1rem 0.8rem 2.8rem; border-radius: 10px; border: 1px solid #cbd5e1; font-size: 0.95rem; color: #0f172a; box-sizing: border-box; }}
            .form-group input:focus {{ outline: none; border-color: #0056b3; }}
            .btn-submit-action {{ background-color: #0056b3; color: white; width: 100%; border: none; padding: 0.9rem; border-radius: 10px; font-size: 1rem; font-weight: 700; cursor: pointer; box-shadow: 0 4px 12px rgba(0, 86, 179, 0.25); margin-top: 1rem; display: flex; align-items: center; justify-content: center; gap: 10px; }}
            .box-support-footer {{ background-color: #f4f0ff; border: 1px solid #e0d4ff; border-radius: 10px; padding: 14px 20px; color: #4c1d95; font-size: 0.9rem; font-weight: 500; margin-top: 2.5rem; display: flex; justify-content: space-between; align-items: center; }}
            @media (max-width: 850px) {{ .main-container {{ flex-direction: column; min-height: auto; }} .banner-azul, .panel-formulario {{ width: 100%; padding: 2.5rem; }} }}
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
                            <div class="logo-upload-zone"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Logo_Uniminuto.png/640px-Logo_Uniminuto.png" onerror="this.style.display='none';"></div>
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
                        <div class="form-header">
                            <h2 class="f-access-title">Acceso al sistema</h2>
                            <p class="f-access-subtitle">Inicia sesión para continuar con RAP Digital.</p>
                        </div>
                        <div class="mockup-tabs">
                            <a href="/?modo=admin" class="tab-link {cls_admin}"><i class="fa-regular fa-user"></i> Administrativo</a>
                            <a href="/?modo=publico" class="tab-link {cls_publico}"><i class="fa-solid fa-globe"></i> Consulta pública</a>
                        </div>
                        {dinamic_form}
                        <div class="box-support-footer"><span><i class="fa-regular fa-circle-question" style="color:#7c3aed; margin-right:8px;"></i> Soporte académico RAP</span><span>➔</span></div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    cls_admin = "active" if modo_actual == 'admin' else ""
    cls_publico = "active" if modo_actual == 'publico' else ""
    
    if modo_actual == "admin":
        dinamic_form = """
        <form action="/" method="GET" target="_parent">
            <div class="form-group">
                <label>Usuario</label>
                <div class="input-with-icon"><i class="fa-regular fa-user"></i><input type="text" name="form_usuario" placeholder="Ingresa tu usuario" required></div>
            </div>
            <div class="form-group">
                <label>Contraseña</label>
                <div class="input-with-icon"><i class="fa-solid fa-lock"></i><input type="password" name="form_pass" placeholder="Ingresa tu contraseña" required></div>
            </div>
            <button type="submit" class="btn-submit-action"><i class="fa-solid fa-right-to-bracket"></i> Ingresar al sistema</button>
        </form>
        """
    else:
        dinamic_form = """
        <div style='text-align:center; padding: 20px 0; color:#64748b;'>
            <i class='fa-solid fa-circle-info' style='font-size:2rem; color:#0056b3; margin-bottom:10px;'></i><br>
            <b>Formulario de Registro Habilitado Abajo</b><br>Utilice el panel inferior de la plataforma para agregar estudiantes directamente al sistema.</div>
        </div>
        """
    components.html(html_template.format(cls_admin=cls_admin, cls_publico=cls_publico, dinamic_form=dinamic_form), height=780)

    if modo_actual == "publico":
        st.divider()
        st.subheader("📝 Formulario de Registro Público de Estudiantes")
        registro.render()

# --- ESCENARIO B: ENTORNO ADMINISTRATIVO (LOGUEADO) ---
else:
    # FILTRO QUIRÚRGICO DE CSS: Corregimos la barra lateral sin tocar los botones del centro
    st.markdown("""
        <style>
        /* Fondo degradado corporativo de la barra lateral */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #001f4d 0%, #00112c 100%) !important;
        }
        [data-testid="stSidebarNav"] { display: none !important; }
        
        .sidebar-brand { padding: 20px 10px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }
        .user-badge { background: rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.1); }
        
        /* CORRECCIÓN MÉDICA: Modificamos EXCLUSIVAMENTE los botones de tipo secondary que estén dentro del Sidebar */
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            
            /* Ajustes exactos: alineación a la izquierda y padding de 20px */
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
        
        /* Forzar texto e iconos en color blanco puro de forma permanente sólo en el Sidebar */
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] p,
        [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover p {
            color: #ffffff !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            margin: 0 !important;
            text-align: left !important;
            justify-content: flex-start !important;
        }
        
        /* Efecto Hover en Azul Institucional sin alterar enunciados */
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
        
        # Botones nativos estables controlados quirúrgicamente
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