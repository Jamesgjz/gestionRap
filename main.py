import streamlit as st
from modules import registro, estado_pruebas, programacion, evaluacion, dashboard

# Configuración de la página en modo ancho
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

# --- CSS DEFINITIVO (Usamos triple comilla limpia sin 'f' para evitar conflictos con las llaves de CSS) ---
st.markdown("""
    <style>
    /* Ocultar interfaces y barras nativas de la plataforma */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #fcfdfe;
    }
    
    /* MAQUETACIÓN EN CONTENEDOR FLEX PARA IGUALAR EL MOCKUP */
    .contenedor-mockup {
        display: flex;
        justify-content: space-between;
        align-items: stretch;
        width: 100%;
        max-width: 1200px;
        margin: 1rem auto;
        gap: 2rem;
    }
    
    /* BANNER AZUL IZQUIERDO */
    .banner-izquierdo-real {
        flex: 1;
        background: linear-gradient(135deg, #001f4d 0%, #00112c 100%);
        padding: 3.5rem 3rem;
        border-radius: 20px;
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 12px 30px rgba(0,31,77,0.15);
    }
    
    .marca-sub-txt {
        color: #38bdf8;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .logo-main-txt {
        font-size: 2.3rem;
        font-weight: 800;
        color: white;
        line-height: 1.1;
        margin-top: 10px;
        margin-bottom: 1.5rem;
    }
    
    .logo-main-txt span {
        color: #f1c40f;
    }
    
    .divisor-corto-real {
        width: 60px;
        height: 4px;
        background-color: #38bdf8;
        margin-bottom: 2rem;
    }
    
    .texto-desc-real {
        font-size: 1.15rem;
        color: #cbd5e1;
        line-height: 1.6;
    }
    
    .bloque-caracteristicas {
        display: flex;
        justify-content: space-between;
        margin-top: 5rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 2rem;
    }
    
    .item-carac {
        text-align: center;
        flex: 1;
    }
    
    .item-carac div {
        font-weight: bold;
        font-size: 0.95rem;
        color: white;
        margin-bottom: 4px;
    }
    
    .item-carac span {
        font-size: 0.8rem;
        color: #94a3b8;
    }
    
    /* TARJETA BLANCA FORMULARIO DERECHO */
    .tarjeta-login-real {
        flex: 1.1;
        background-color: #ffffff;
        padding: 3.5rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.02);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .titulo-acceso-real {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .sub-acceso-real {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 2.5rem;
    }
    
    /* Estilos para inputs HTML puros clonados del mockup */
    .input-html-grupo {
        margin-bottom: 1.5rem;
    }
    
    .input-html-label {
        display: block;
        font-size: 0.9rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 0.5rem;
    }
    
    .input-html-field {
        width: 100%;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        font-size: 0.95rem;
        color: #0f172a;
        background-color: #fff;
        box-sizing: border-box;
    }
    
    .input-html-field:focus {
        outline: none;
        border-color: #0056b3;
        box-shadow: 0 0 0 3px rgba(0,86,179,0.1);
    }
    
    /* Botón de envío que hereda el ancho completo */
    .btn-ingresar-real {
        background-color: #0056b3;
        color: white;
        width: 100%;
        border: none;
        padding: 0.8rem;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,86,179,0.25);
        transition: background 0.2s;
        margin-top: 1rem;
    }
    
    /* Enlace inferior de soporte */
    .soporte-footer {
        background-color: #f4f0ff;
        border: 1px solid #e0d4ff;
        border-radius: 10px;
        padding: 14px 20px;
        color: #4c1d95;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 2.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- TOP BAR (Cabecera Superior del Mockup) ---
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

# --- INSTANCIACIÓN DE SESIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    
    # Procesamos las variables que inyectará el formulario HTML nativo en la URL
    query_params = st.query_params
    if "form_usuario" in query_params and "form_pass" in query_params:
        u_ingresado = query_params["form_usuario"]
        p_ingresado = query_params["form_pass"]
        
        st.query_params.clear() # Limpiamos la barra de direcciones
        
        if u_ingresado == "admin" and p_ingresado == "admin123":
            st.session_state['autenticado'] = True
            st.session_state['usuario'] = "James Jaramillo"
            st.session_state['rol'] = "admin"
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    # RENDERIZADO COMPLETO REPARADO (Sin f-string, código HTML interpretado puro)
    st.markdown("""
        <div class="contenedor-mockup">
            <!-- PARTE IZQUIERDA: EL BANNER INSTITUCIONAL -->
            <div class="banner-izquierdo-real">
                <div>
                    <div class="marca-sub-txt">RAP Digital</div>
                    <div class="logo-main-txt">MD UNIMINUTO<br><span>VIRTUAL</span></div>
                    <div class="divisor-corto-real"></div>
                    <div class="texto-desc-real">
                        Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.
                    </div>
                </div>
                <div class="bloque-caracteristicas">
                    <div class="item-carac"><div>📈 Seguimiento</div><span>Métricas en tiempo real</span></div>
                    <div class="item-carac"><div>📋 Evaluación</div><span>Asignación ágil</span></div>
                    <div class="item-carac"><div>🛡️ Trazabilidad</div><span>Históricos seguros</span></div>
                </div>
            </div>
            
            <!-- PARTE DERECHA: LA TARJETA BLANCA DE ACCESO CON FORMULARIO DIRECTO -->
            <div class="tarjeta-login-real">
                <div class="titulo-acceso-real">Acceso al sistema</div>
                <div class="sub-acceso-real">Inicia sesión para continuar con RAP Digital.</div>
                
                <form action="/" method="get">
                    <div class="input-html-grupo">
                        <label class="input-html-label">Usuario</label>
                        <input type="text" name="form_usuario" class="input-html-field" placeholder="Ingresa tu usuario" required>
                    </div>
                    <div class="input-html-grupo">
                        <label class="input-html-label">Contraseña</label>
                        <input type="password" name="form_pass" class="input-html-field" placeholder="Ingresa tu contraseña" required>
                    </div>
                    <button type="submit" class="btn-ingresar-real">➔ Ingresar al sistema</button>
                </form>
                
                <div class="soporte-footer">
                    <span>Support técnico académico RAP</span>
                    <span>➔</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    # --- INTERFAZ ADMINISTRATIVA CONTROLADA ---
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