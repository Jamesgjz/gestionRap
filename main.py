import streamlit as st
from modules import registro, estado_pruebas, programacion, evaluacion, dashboard

# Configuración de la página - Forzamos el diseño ancho para dar espacio al diseño dividido
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

# --- CSS AVANZADO: RECREANDO EL MOCKUP DE INICIO DE SESIÓN ---
st.markdown("""
    <style>
    /* Ocultar elementos nativos molestos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Configuración de fondo global */
    .stApp {
        background-color: #fcfdfe;
    }
    
    /* Contenedor Principal en Tabla para maquetación asimétrica rígida */
    .mockup-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-top: 10px;
    }
    
    /* BANNER IZQUIERDO (Azul Oscuro Institucional) */
    .panel-izquierdo {
        width: 42%;
        background: linear-gradient(135deg, #001f4d 0%, #001533 100%);
        padding: 4rem 3rem;
        border-radius: 20px;
        color: white;
        vertical-align: top;
        box-shadow: 0 12px 30px rgba(0,21,51,0.15);
    }
    
    .marca-txt {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 0.9rem;
        letter-spacing: 1.5px;
        color: #38bdf8;
        text-transform: uppercase;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .logo-placeholder {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.2;
        margin-bottom: 2rem;
    }
    
    .logo-placeholder span {
        color: #eab308; /* Amarillo Uniminuto */
    }
    
    .linea-separadora {
        width: 40px;
        height: 3px;
        background-color: #38bdf8;
        margin-bottom: 2rem;
    }
    
    .desc-principal {
        font-size: 1.2rem;
        color: #e2e8f0;
        line-height: 1.6;
        margin-bottom: 5rem;
    }
    
    /* Características inferiores del Banner */
    .feature-item {
        margin-bottom: 1.5rem;
    }
    .feature-title {
        font-weight: bold;
        font-size: 1rem;
        color: #ffffff;
    }
    .feature-desc {
        font-size: 0.85rem;
        color: #94a3b8;
    }
    
    /* ESPACIO DE SEPARACIÓN INTERMEDIO */
    .espaciador-celda {
        width: 4%;
    }
    
    /* PANEL DERECHO (Formulario de Acceso Blanco) */
    .panel-derecho {
        width: 54%;
        background-color: #ffffff;
        padding: 3rem 3.5rem;
        border-radius: 20px;
        vertical-align: top;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03);
    }
    
    /* Títulos del Formulario */
    .form-titulo {
        color: #0f172a;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    
    .form-subtitulo {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 2.5rem;
    }
    
    /* Botonera de Ingreso estilo Mockup */
    div.stButton > button:first-child {
        background: #0056b3 !important;
        color: white !important;
        width: 100% !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-size: 1rem !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,86,179,0.2) !important;
        transition: all 0.2s ease !important;
        margin-top: 10px;
    }
    
    /* Input adjustments */
    .stTextInput input {
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 0.55rem 0.75rem !important;
    }
    
    /* Enlace de soporte inferior */
    .soporte-box {
        background-color: #f4f0ff;
        border: 1px solid #e0d4ff;
        border-radius: 10px;
        padding: 12px 20px;
        margin-top: 2rem;
        color: #4c1d95;
        font-size: 0.9rem;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA SUPERIOR INSTITUCIONAL (Mockup Top Bar) ---
c_logo, c_fecha = st.columns([2, 1])
with c_logo:
    st.markdown("""
        <div style='padding: 10px 0;'>
            <span style='font-size:1.4rem; font-weight:800; color:#001f4d;'>MD</span>
            <span style='font-size:1.2rem; font-weight:700; color:#001f4d; letter-spacing: 1px;'> UNIMINUTO</span>
            <span style='font-size:0.9rem; font-weight:400; color:#475569; display:block; margin-top:-5px;'>VIRTUAL</span>
        </div>
    """, unsafe_allow_html=True)
with c_fecha:
    import datetime
    fecha_actual = datetime.date.today().strftime("%d de %B de %Y")
    st.markdown(f"<div style='text-align:right; color:#64748b; padding-top:20px; font-size:0.9rem;'>📅 {fecha_actual}</div>", unsafe_allow_html=True)

st.divider()

# --- LÓGICA DE NAVEGACIÓN INITIAL ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    
    # Maquetamos las dos columnas usando la tabla HTML inyectada de forma segura
    st.markdown("""
        <table class="mockup-table">
            <tr>
                <!-- COLUMNA IZQUIERDA: DISEÑO BANNER -->
                <td class="panel-izquierdo">
                    <div class="marca-txt">RAP Digital</div>
                    <div class="logo-placeholder">MD UNIMINUTO<br><span>VIRTUAL</span></div>
                    <div class="linea-separadora"></div>
                    <div class="desc-principal">
                        Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.
                    </div>
                    <div style="margin-top: 4rem;">
                        <div class="feature-item"><span class="feature-title">📈 Seguimiento</span><br><span class="feature-desc">Control analítico y métricas en tiempo real.</span></div>
                        <div class="feature-item"><span class="feature-title">📋 Evaluación</span><br><span class="feature-desc">Asignación ágil y transparente de notas.</span></div>
                        <div class="feature-item"><span class="feature-title">🛡️ Trazabilidad académica</span><br><span class="feature-desc">Históricos consolidados sin alteración.</span></div>
                    </div>
                </td>
                
                <!-- ESPACIADOR -->
                <td class="espaciador-celda"></td>
                
                <!-- COLUMNA DERECHA: FORMULARIO INTERACTIVO (Dejamos abierta la celda para inyectar los inputs de Streamlit) -->
                <td class="panel-derecho">
                    <div class="form-titulo">Acceso al sistema</div>
                    <div class="form-subtitulo">Inicia sesión para continuar con RAP Digital.</div>
    """, unsafe_allow_html=True)
    
    # Usamos st.tabs de forma limpia simulando el control de pestañas del mockup
    modo = st.tabs(["👤 Administrativo", "🌐 Consulta pública"])
    
    with modo[0]:
        usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="usr_input")
        contrasena = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="pass_input")
        
        if st.button("➔  Ingresar al sistema"):
            if usuario == "admin" and contrasena == "admin123":
                st.session_state['autenticado'] = True
                st.session_state['usuario'] = "James Jaramillo"
                st.session_state['rol'] = "admin"
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
                
    with modo[1]:
        st.info("Utilice este espacio alterno para registrar nuevos estudiantes al sistema.")
        registro.render()
        
    # Cerramos las celdas de la tabla HTML e inyectamos la sección de soporte inferior
    st.markdown("""
                    <div class="soporte-box">
                        ℹ️ Soporte académico RAP ➔
                    </div>
                </td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

else:
    # --- INTERFAZ ADMINISTRATIVA (MANTENIDA IDÉNTICA) ---
    st.sidebar.title(f"👨‍🏫 {st.session_state['usuario']}")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state['autenticado'] = False
        st.rerun()

    opcion = st.sidebar.radio("Menú Principal", [
        "Inicio", 
        "Registro Estudiantes", 
        "Estado de Pruebas", 
        "Programación", 
        "Evaluación",
        "Dashboard / KPIs"
    ])

    if opcion == "Inicio":
        st.subheader("Panel de Control Administrative")
        st.write(f"Bienvenido, {st.session_state['usuario']}. El sistema está listo para gestionar las pruebas RAP.")
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