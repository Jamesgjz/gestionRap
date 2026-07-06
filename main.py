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

# --- ESCENARIO A: PANTALLA DE LOGIN IDÉNTICA AL MOCKUP ---
if not st.session_state['autenticado']:
    
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <!-- Librerías de Iconos vectoriales profesionales -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
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
                min-height: 580px;
            }

            /* PANEL IZQUIERDO: BANNER AZUL EXPANDIDO (45%) */
            .banner-azul {
                flex: 0.45;
                background: linear-gradient(135deg, #001f4d 0%, #00112c 100%);
                padding: 3.5rem 3rem;
                color: white;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            
            /* ESPACIO PARA SUBIR LA IMAGEN / LOGO */
            .logo-upload-zone {
                width: 100%;
                max-width: 220px;
                height: auto;
                min-height: 60px;
                margin-bottom: 2rem;
                display: flex;
                align-items: center;
            }
            .logo-upload-zone img {
                width: 100%;
                height: auto;
                object-fit: contain;
                /* Filtro opcional por si subes un logo negro y quieres que se vea blanco impecable */
                filter: brightness(0) invert(1); 
            }
            
            .banner-top .sub-marca {
                color: #38bdf8;
                font-size: 0.9rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 4px;
            }
            .banner-top .main-logo-title {
                font-size: 2.1rem;
                font-weight: 800;
                line-height: 1.1;
                margin-bottom: 1.2rem;
            }
            .banner-top .main-logo-title span { color: #f1c40f; }
            .banner-top .short-line {
                width: 50px;
                height: 3px;
                background-color: #38bdf8;
                margin-bottom: 1.8rem;
            }
            .banner-top .main-description {
                font-size: 1.1rem;
                color: #cbd5e1;
                line-height: 1.6;
            }
            
            /* CARACTERÍSTICAS INFERIORES CON ICONOS PREMIUM DEL MOCKUP */
            .banner-features {
                display: flex;
                justify-content: space-between;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                padding-top: 2rem;
                gap: 15px;
            }
            .feature-box {
                text-align: center;
                flex: 1;
            }
            .feature-icon-wrapper {
                background: rgba(255, 255, 255, 0.08);
                width: 42px;
                height: 42px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 10px auto;
                color: #38bdf8;
                font-size: 1.2rem;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
            .feature-box .f-title { font-weight: 700; font-size: 0.95rem; color: white; margin-bottom: 3px; }
            .feature-box .f-desc { font-size: 0.8rem; color: #94a3b8; display: block; line-height: 1.3; }

            /* PANEL DERECHO: FORMULARIO (55%) */
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
                gap: 10px;
            }
            .tab-item {
                padding: 10px 15px;
                font-size: 0.95rem;
                font-weight: 600;
                color: #64748b;
                border-bottom: 2px solid transparent;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .tab-item.active {
                color: #0056b3;
                border-bottom: 2px solid #0056b3;
            }

            /* CAMPOS DE ENTRADA */
            .form-group {
                margin-bottom: 1.5rem;
                position: relative;
            }
            .form-group label {
                display: block;
                font-size: 0.9rem;
                font-weight: 600;
                color: #334155;
                margin-bottom: 0.5rem;
            }
            .input-with-icon {
                position: relative;
                display: flex;
                align-items: center;
            }
            .input-with-icon i {
                position: absolute;
                left: 15px;
                color: #94a3b8;
                font-size: 1.1rem;
            }
            .form-group input {
                width: 100%;
                padding: 0.8rem 1rem 0.8rem 2.8rem;
                border-radius: 10px;
                border: 1px solid #cbd5e1;
                font-size: 0.95rem;
                color: #0f172a;
                background-color: #fff;
                box-sizing: border-box;
            }
            .form-group input:focus {
                outline: none;
                border-color: #0056b3;
                box-shadow: 0 0 0 3px rgba(0,86,179,0.08);
            }

            /* BOTÓN COMPLETO */
            .btn-submit-action {
                background-color: #0056b3;
                color: white;
                width: 100%;
                border: none;
                padding: 0.9rem;
                border-radius: 10px;
                font-size: 1rem;
                font-weight: 700;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0, 86, 179, 0.25);
                margin-top: 1rem;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }
            .btn-submit-action:hover { background-color: #004394; }

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
                    <!-- CONTENEDOR IMAGEN LOGO: Cambia src="assets/tu_logo.png" cuando lo tengas en tu carpeta -->
                    <div class="logo-upload-zone">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Logo_Uniminuto.png/640px-Logo_Uniminuto.png" onerror="this.style.display='none'; this.insertAdjacentHTML('afterend', '<div style=\'border:2px dashed rgba(255,255,255,0.3); padding:10px; border-radius:8px; font-size:0.8rem; color:#94a3b8; text-align:center;\'>[Espacio reservado para Logo de Uniminuto]</div>')">
                    </div>
                    
                    <div class="sub-marca">RAP Digital</div>
                    <div class="main-logo-title">MD UNIMINUTO<br><span>VIRTUAL</span></div>
                    <div class="short-line"></div>
                    <div class="main-description">
                        Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.
                    </div>
                </div>
                
                <!-- ICONOS VECTORIALES COMPLETA Y FIELMENTE ALINEADOS -->
                <div class="banner-features">
                    <div class="feature-box">
                        <div class="feature-icon-wrapper"><i class="fa-solid fa-chart-line"></i></div>
                        <div class="f-title">Seguimiento</div>
                        <span class="f-desc">Tiempo real</span>
                    </div>
                    <div class="feature-box">
                        <div class="feature-icon-wrapper"><i class="fa-regular fa-clipboard"></i></div>
                        <div class="f-title">Evaluación</div>
                        <span class="f-desc">Asignación ágil</span>
                    </div>
                    <div class="feature-box">
                        <div class="feature-icon-wrapper"><i class="fa-solid fa-shield-halved"></i></div>
                        <div class="f-title">Trazabilidad</div>
                        <span class="f-desc">Históricos seguros</span>
                    </div>
                </div>
            </div>
            
            <!-- PANEL DERECHO -->
            <div class="panel-formulario">
                <div class="form-header">
                    <h2 class="f-access-title">Acceso al sistema</h2>
                    <p class="f-access-subtitle">Inicia sesión para continuar con RAP Digital.</p>
                </div>
                
                <div class="mockup-tabs">
                    <div class="tab-item active"><i class="fa-regular fa-user"></i> Administrativo</div>
                    <div class="tab-item"><i class="fa-solid fa-globe"></i> Consulta pública</div>
                </div>
                
                <form action="/" method="GET">
                    <div class="form-group">
                        <label>Usuario</label>
                        <div class="input-with-icon">
                            <i class="fa-regular fa-user"></i>
                            <input type="text" name="form_usuario" placeholder="Ingresa tu usuario" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Contraseña</label>
                        <div class="input-with-icon">
                            <i class="fa-solid fa-lock"></i>
                            <input type="password" name="form_pass" placeholder="Ingresa tu contraseña" required>
                        </div>
                    </div>
                    <button type="submit" class="btn-submit-action">
                        <i class="fa-solid fa-right-to-bracket"></i> Ingresar al sistema
                    </button>
                </form>
                
                <div class="box-support-footer">
                    <span><i class="fa-regular fa-circle-question" style="color:#7c3aed; margin-right:8px;"></i> Soporte académico RAP</span>
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