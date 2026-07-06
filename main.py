import streamlit as st
import streamlit.components.v1 as components
from modules import registro, estado_pruebas, programacion, evaluacion, dashboard

# Configuración de la página en modo ancho para aprovechar todo el monitor
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

# --- LÓGICA DE CAPTURA DE CREDENCIALES DESDE EL COMPONENTE ---
query_params = st.query_params
if "form_usuario" in query_params and "form_pass" in query_params:
    u_ingresado = query_params["form_usuario"]
    p_ingresado = query_params["form_pass"]
    
    # Limpiamos los parámetros de la URL inmediatamente para evitar ciclos de recarga
    st.query_params.clear()
    
    if u_ingresado == "admin" and p_ingresado == "admin123":
        st.session_state['autenticado'] = True
        st.session_state['usuario'] = "James Jaramillo"
        st.session_state['rol'] = "admin"
        st.rerun()
    else:
        st.sidebar.error("❌ Credenciales incorrectas. Intente nuevamente.")

# --- INICIALIZACIÓN DEL ESTADO DE SESIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

# --- ESCENARIO A: USUARIO NO AUTENTICADO (PANTALLA DE LOGIN IDÉNTICA AL MOCKUP) ---
if not st.session_state['autenticado']:
    
    # Renderizado aislado mediante el componente HTML de Streamlit (Evita fugas de texto o deformaciones)
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: #fcfdfe;
                margin: 0;
                padding: 10px 40px;
                box-sizing: border-box;
            }
            
            /* BARRA SUPERIOR INSTITUCIONAL */
            .top-bar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 0;
                border-bottom: 1px solid #e2e8f0;
                margin-bottom: 25px;
            }
            .top-logo {
                color: #001f4d;
                line-height: 1.2;
            }
            .top-logo .bold-md { font-weight: 800; font-size: 1.4rem; }
            .top-logo .text-uni { font-weight: 700; font-size: 1.2rem; letter-spacing: 1px; }
            .top-logo .sub-virtual { font-size: 0.85rem; font-weight: 400; color: #64748b; display: block; margin-top: -3px; }
            .top-date { color: #64748b; font-size: 0.9rem; }

            /* CONTENEDOR PRINCIPAL DIVIDIDO (FLEXBOX) */
            .main-container {
                display: flex;
                max-width: 1200px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 24px;
                overflow: hidden;
                box-shadow: 0 15px 35px rgba(0, 31, 77, 0.08);
                min-height: 560px;
            }

            /* PANEL IZQUIERDO: BANNER AZUL EXPANDIDO (45% DEL CONTENEDOR) */
            .banner-azul {
                flex: 0.45;
                background: linear-gradient(135deg, #001f4d 0%, #00112c 100%);
                padding: 3.5rem 3rem;
                color: white;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                position: relative;
            }
            .banner-top .sub-marca {
                color: #38bdf8;
                font-size: 0.9rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 8px;
            }
            .banner-top .main-logo-title {
                font-size: 2.3rem;
                font-weight: 800;
                line-height: 1.1;
                margin-bottom: 1.5rem;
            }
            .banner-top .main-logo-title span { color: #f1c40f; }
            .banner-top .short-line {
                width: 60px;
                height: 4px;
                background-color: #38bdf8;
                margin-bottom: 2rem;
            }
            .banner-top .main-description {
                font-size: 1.15rem;
                color: #cbd5e1;
                line-height: 1.6;
            }
            
            /* CARACTERÍSTICAS INFERIORES DEL BANNER */
            .banner-features {
                display: flex;
                justify-content: space-between;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                padding-top: 2rem;
                gap: 10px;
            }
            .feature-box { text-align: center; flex: 1; }
            .feature-box .f-title { font-weight: 700; font-size: 0.95rem; color: white; margin-bottom: 4px; }
            .feature-box .f-desc { font-size: 0.8rem; color: #94a3b8; }

            /* PANEL DERECHO: FORMULARIO BLANCO INSTITUCIONAL (55% DEL CONTENEDOR) */
            .panel-formulario {
                flex: 0.55;
                padding: 4rem;
                display: flex;
                flex-direction: column;
                justify-content: center;
                background-color: #ffffff;
            }
            .form-header .f-access-title {
                color: #0f172a;
                font-size: 2rem;
                font-weight: 700;
                margin: 0 0 5px 0;
            }
            .form-header .f-access-subtitle {
                color: #64748b;
                font-size: 0.95rem;
                margin: 0 0 2.5rem 0;
            }

            /* SELECTOR DE PESTAÑAS DEL MOCKUP */
            .mockup-tabs {
                display: flex;
                border-bottom: 1px solid #e2e8f0;
                margin-bottom: 2rem;
            }
            .tab-item {
                padding: 10px 20px;
                font-size: 0.95rem;
                font-weight: 600;
                color: #64748b;
                border-bottom: 2px solid transparent;
                cursor: pointer;
            }
            .tab-item.active {
                color: #0056b3;
                border-bottom: 2px solid #0056b3;
            }

            /* CAMPOS DE ENTRADA HTML PUROS */
            .form-group {
                margin-bottom: 1.5rem;
            }
            .form-group label {
                display: block;
                font-size: 0.9rem;
                font-weight: 600;
                color: #334155;
                margin-bottom: 0.5rem;
            }
            .form-group input {
                width: 100%;
                padding: 0.8rem 1rem;
                border-radius: 10px;
                border: 1px solid #cbd5e1;
                font-size: 0.95rem;
                color: #0f172a;
                background-color: #fff;
                box-sizing: border-box;
                transition: border-color 0.2s;
            }
            .form-group input:focus {
                outline: none;
                border-color: #0056b3;
            }

            /* BOTÓN COMPLETO */
            .btn-submit-action {
                background-color: #0056b3;
                color: white;
                width: 100%;
                border: none;
                padding: 0.85rem;
                border-radius: 10px;
                font-size: 1rem;
                font-weight: 700;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0, 86, 179, 0.25);
                margin-top: 1rem;
                transition: background 0.2s;
            }
            .btn-submit-action:hover {
                background-color: #004394;
            }

            /* CAJA MORADA INFERIOR DE SOPORTE */
            .box-support-footer {
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
            }
        </style>
    </head>
    <body>

        <!-- CABECERA SUPERIOR -->
        <div class="top-bar">
            <div class="top-logo">
                <span class="bold-md">MD</span><span class="text-uni"> UNIMINUTO</span>
                <span class="sub-virtual">VIRTUAL</span>
            </div>
            <div class="top-date">📅 06 de Julio de 2026</div>
        </div>

        <!-- CONTENEDOR CENTRAL MAQUETADO -->
        <div class="main-container">
            
            <!-- PANEL IZQUIERDO (BANNER AZUL ANCHO) -->
            <div class="banner-azul">
                <div class="banner-top">
                    <div class="sub-marca">RAP Digital</div>
                    <div class="main-logo-title">MD UNIMINUTO<br><span>VIRTUAL</span></div>
                    <div class="short-line"></div>
                    <div class="main-description">
                        Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.
                    </div>
                </div>
                <div class="banner-features">
                    <div class="feature-box"><div class="f-title">📈 Seguimiento</div><span class="f-desc">Tiempo real</span></div>
                    <div class="feature-box"><div class="f-title">📋 Evaluación</div><span class="f-desc">Asignación ágil</div></div>
                    <div class="feature-box"><div class="f-title">🛡️ Trazabilidad</div><span class="f-desc">Históricos seguros</span></div>
                </div>
            </div>
            
            <!-- PANEL DERECHO (FORMULARIO SIN HUECOS EN BLANCO) -->
            <div class="panel-formulario">
                <div class="form-header">
                    <h2 class="f-access-title">Acceso al sistema</h2>
                    <p class="f-access-subtitle">Inicia sesión para continuar con RAP Digital.</p>
                </div>
                
                <div class="mockup-tabs">
                    <div class="tab-item active">👤 Administrativo</div>
                    <div class="tab-item">🌐 Consulta pública</div>
                </div>
                
                <!-- Target del formulario redirige los valores directo al backend de Streamlit -->
                <form action="/" method="GET">
                    <div class="form-group">
                        <label>Usuario</label>
                        <input type="text" name="form_usuario" placeholder="Ingresa tu usuario" required>
                    </div>
                    <div class="form-group">
                        <label>Contraseña</label>
                        <input type="password" name="form_pass" placeholder="Ingresa tu contraseña" required>
                    </div>
                    <button type="submit" class="btn-submit-action">➔ Ingresar al sistema</button>
                </form>
                
                <div class="box-support-footer">
                    <span>Soporte académico RAP</span>
                    <span>➔</span>
                </div>
            </div>
            
        </div>

    </body>
    </html>
    """, height=720)

# --- ESCENARIO B: PANEL ADMINISTRATIVO PRIVADO (USUARIO LOGUEADO) ---
else:
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