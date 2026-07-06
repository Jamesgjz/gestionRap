import streamlit as st
from modules import registro, estado_pruebas, programacion, evaluacion, dashboard

# Configuración de la página en modo ancho
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

# --- CSS INTEGRADO CORREGIDO Y OPTIMIZADO ---
st.markdown("""
    <style>
    /* Ocultar barras por defecto */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Forzar fondo limpio y unificado */
    .stApp {
        background-color: #fcfdfe;
    }
    
    /* CONTENEDOR IZQUIERDO: Banner Azul Profundo */
    .banner-izquierdo {
        background: linear-gradient(135deg, #001f4d 0%, #00112c 100%);
        padding: 3.5rem 3rem;
        border-radius: 20px;
        color: white;
        height: auto;
        min-height: 520px;
        box-shadow: 0 12px 28px rgba(0,31,77,0.15);
    }
    
    .marca-sub {
        color: #38bdf8;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    
    .logo-main {
        font-size: 2.3rem;
        font-weight: 800;
        color: white;
        line-height: 1.1;
        margin-bottom: 1.5rem;
    }
    
    .logo-main span {
        color: #f1c40f;
    }
    
    .divisor-corto {
        width: 60px;
        height: 4px;
        background-color: #38bdf8;
        margin-bottom: 2.5rem;
    }
    
    .texto-desc {
        font-size: 1.15rem;
        color: #cbd5e1;
        line-height: 1.6;
        margin-bottom: 4rem;
    }
    
    /* Ajustes de las características */
    .item-caracteristica {
        margin-top: 1.8rem;
    }
    
    .titulo-caracteristica {
        font-weight: bold;
        font-size: 1.05rem;
        color: white;
    }
    
    .desc-caracteristica {
        font-size: 0.9rem;
        color: #94a3b8;
    }
    
    /* CONTENEDOR DERECHO: Tarjeta de Acceso Limpia */
    .tarjeta-login {
        background-color: #ffffff;
        padding: 2.5rem 3rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03);
        margin-top: 0px; /* Eliminamos cualquier margen que empuje el contenido */
    }
    
    .titulo-acceso {
        color: #0f172a;
        font-size: 1.9rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .sub-acceso {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    
    /* Ajuste estricto para los Inputs de Streamlit para que no dejen espacios muertos */
    .stTextInput {
        margin-top: -10px !important;
    }
    
    /* Ajuste de Botón de bloque completo */
    div.stButton > button:first-child {
        background-color: #0056b3 !important;
        color: white !important;
        width: 100% !important;
        border-radius: 8px !important;
        padding: 0.7rem 1rem !important;
        font-size: 1rem !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,86,179,0.2) !important;
        margin-top: 15px;
    }
    
    /* Caja Morada de Soporte en el extremo inferior */
    .caja-soporte {
        background-color: #f4f0ff;
        border: 1px solid #e0d4ff;
        border-radius: 8px;
        padding: 14px 20px;
        color: #4c1d95;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SUPERIOR (Alineación Horizontal) ---
col_logo_top, col_fecha_top = st.columns([2, 1])
with col_logo_top:
    st.markdown("""
        <div style='padding: 5px 0;'>
            <span style='font-size:1.4rem; font-weight:800; color:#001f4d;'>MD UNIMINUTO</span>
            <span style='font-size:0.85rem; font-weight:400; color:#64748b; display:block; margin-top:-5px;'>VIRTUAL</span>
        </div>
    """, unsafe_allow_html=True)
with col_fecha_top:
    import datetime
    fecha_hoy = datetime.date.today().strftime("%d de %B de %Y")
    st.markdown(f"<div style='text-align:right; color:#64748b; padding-top:15px; font-size:0.9rem;'>📅 {fecha_hoy}</div>", unsafe_allow_html=True)

st.divider()

# --- VALIDACIÓN DE SESIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    
    # Ajustamos la proporción a [5, 6] eliminando la columna vacía del medio para expandir todo horizontalmente
    col_banner, col_formulario = st.columns([5, 6])
    
    # PANEL IZQUIERDO: Renderizado directo del bloque visual
    with col_banner:
        st.markdown("""
            <div class="banner-izquierdo">
                <div class="marca-sub">RAP Digital</div>
                <div class="logo-main">MD UNIMINUTO<br><span>VIRTUAL</span></div>
                <div class="divisor-corto"></div>
                <div class="texto-desc">
                    Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.
                </div>
                <div style="margin-top: 1rem;">
                    <div class="item-caracteristica">
                        <span class="titulo-caracteristica">📈 Seguimiento</span><br>
                        <span class="desc-caracteristica">Control analítico y métricas en tiempo real.</span>
                    </div>
                    <div class="item-caracteristica">
                        <span class="titulo-caracteristica">📋 Evaluación</span><br>
                        <span class="desc-caracteristica">Asignación ágil y transparente de notas.</span>
                    </div>
                    <div class="item-caracteristica">
                        <span class="titulo-caracteristica">🛡️ Trazabilidad académica</span><br>
                        <span class="desc-caracteristica">Históricos consolidados sin alteración.</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    # PANEL DERECHO: Tarjeta de Acceso alineada arriba
    with col_formulario:
        st.markdown('<div class="tarjeta-login">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-acceso">Acceso al sistema</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-acceso">Inicia sesión para continuar con RAP Digital.</div>', unsafe_allow_html=True)
        
        # Pestañas limpias
        modo = st.tabs(["👤 Administrativo", "🌐 Consulta pública"])
        
        with modo[0]:
            usuario = st.text_input("Usuario", placeholder="Ingresa tu usuario", key="login_user")
            contrasena = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="login_pass")
            
            if st.button("Ingresar al sistema"):
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
            
        st.markdown("""
            <div class="caja-soporte">
                <span>ℹ️ Soporte académico RAP</span>
                <span>➔</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- INTERFAZ ADMINISTRATIVA (LOGUEADO) ---
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
        st.subheader("Panel de Control Administrativo")
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