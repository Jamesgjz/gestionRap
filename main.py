import streamlit as st
import streamlit.components.v1 as components
from modules import registro, estado_pruebas, programacion, evaluacion, dashboard

# Configuración de la página en modo ancho total
st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

# --- LÓGICA DE CAPTURA DE CREDENCIALES ---
query_params = st.query_params
if "form_usuario" in query_params and "form_pass" in query_params:
    u_ingresado = query_params["form_usuario"]
    p_ingresado = query_params["form_pass"]
    
    st.query_params.clear() 
    
    if u_ingresado == "admin" and p_ingresado == "admin123":
        st.session_state['autenticado'] = True
        st.session_state['usuario'] = "James Jaramillo"
        st.session_state['rol'] = "admin"
        st.rerun()
    else:
        st.sidebar.error("❌ Credenciales incorrectas. Intente nuevamente.")

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

# --- ESCENARIO A: PANTALLA DE LOGIN RESPONSIVA ---
if not st.session_state['autenticado']:
    
    # Aumentamos la altura del componente a 800 e inyectamos CSS adaptativo real
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            /* Reset básico para evitar scrolls y aprovechar espacio */
            html, body {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                background-color: #fcfdfe;
                font-family: 'Inter', sans-serif;
                box-sizing: border-box;
                overflow-x: hidden;
            }
            
            .page-wrapper {
                padding: 10px 40px;
                display: flex;
                flex-direction: column;
                min-height: 100vh;
                box-sizing: border-box;
            }
            
            /* BARRA SUPERIOR INSTITUCIONAL */
            .top-bar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 0;
                border-bottom: 1px solid #e2e8f0;
                margin-bottom: 20px;
            }
            .top-logo {
                color: #001f4d;
                line-height: 1.2;
            }
            .top-logo .bold-md { font-weight: 800; font-size: 1.4rem; }
            .top-logo .text-uni { font-weight: 700; font-size: 1.2rem; letter-spacing: 1px; }
            .top-logo .sub-virtual { font-size: 0.85rem; font-weight: 400; color: #64748b; display: block; margin-top: -3px; }
            .top-date { color: #64748b; font-size: 0.9rem; }

            /* CONTENEDOR PRINCIPAL AUTORESPONSIVO */
            .main-container {
                display: flex;
                width: 100%;
                max-width: 1350px; /* Expandido para aprovechar mejor los costados */
                margin: 0 auto flex-grow;
                background: #ffffff;
                border-radius: 24px;
                overflow: hidden;
                box-shadow: 0 15px 35px rgba(0, 31, 77, 0.06);
                min-height: 70vh; /* Altura proporcional a la pantalla */
            }

            /* PANEL IZQUIERDO: BANNER AZUL DINÁMICO */
            .banner-azul {
                flex: 1.1; /* Proporción balanceada y más ancha */
                background: linear-gradient(135deg, #001f4d 0%, #00112c 100%);
                padding: 4rem 3.5rem;
                color: white;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            
            .logo-upload-zone {
                width: 100%;
                max-width: 240px;
                margin-bottom: 2rem;
            }
            .logo-upload-zone img {
                width: 100%;
                height: auto;
                object-fit: contain;
                filter: brightness(0) invert(1); 
            }
            
            .banner-top .sub-marca {
                color: #38bdf8;
                font-size: 0.95rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 6px;
            }
            .banner-top .main-logo-title {
                font-size: 2.5rem;
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
                font-size: 1.2rem;
                color: #cbd5e1;
                line-height: 1.6;
            }
            
            /* PILARES INFERIORES */
            .banner-features {
                display: flex;
                justify-content: space-between;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                padding-top: 2rem;
                gap: 20px;
                margin-top: 3rem;
            }
            .feature-box { text-align: center; flex: 1; }
            .feature-icon-wrapper {
                background: rgba(255, 255, 255, 0.07);
                width: 46px;
                height: 46px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 12px auto;
                color: #38bdf8;
                font-size: 1.3rem;
            }
            .feature-box .f-title { font-weight: 700; font-size: 1rem; color: white; margin-bottom: 4px; }
            .feature-box .f-desc { font-size: 0.85rem; color: #94a3b8; }

            /* PANEL DERECHO: FORMULARIO FLEXIBLE */
            .panel-formulario {
                flex: 1.2;
                padding: 4.5rem;
                display: flex;
                flex-direction: column;
                justify-content: center;
                background-color: #ffffff;
            }
            .form-header .f-access-title {
                color: #0f172a;
                font-size: 2.2rem;
                font-weight: 700;
                margin: 0 0 6px 0;
            }
            .form-header .f-access-subtitle {
                color: #64748b;
                font-size: 1rem;
                margin: 0 0 2.5rem 0;
            }

            .mockup-tabs {
                display: flex;
                border-bottom: 1px solid #e2e8f0;
                margin-bottom: 2rem;
                gap: 15px;
            }
            .tab-item {
                padding: 12px 18px;
                font-size: 1rem;
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

            .form-group { margin-bottom: 1.6rem; }
            .form-group label {
                display: block;
                font-size: 0.95rem;
                font-weight: 600;
                color: #334155;
                margin-bottom: 0.6rem;
            }
            .input-with-icon {
                position: relative;
                display: flex;
                align-items: center;
            }
            .input-with-icon i {
                position: absolute;
                left: 16px;
                color: #94a3b8;
                font-size: 1.15rem;
            }
            .form-group input {
                width: 100%;
                padding: 0.9rem 1rem 0.9rem 3rem;
                border-radius: 10px;
                border: 1px solid #cbd5e1;
                font-size: 1rem;
                color: #0f172a;
                box-sizing: border-box;
            }
            .form-group input:focus {
                outline: none;
                border-color: #0056b3;
                box-shadow: 0 0 0 3px rgba(0,86,179,0.08);
            }

            .btn-submit-action {
                background-color: #0056b3;
                color: white;
                width: 100%;
                border: none;
                padding: 0.95rem;
                border-radius: 10px;
                font-size: 1.05rem;
                font-weight: 700;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0, 86, 179, 0.25);
                margin-top: 1.2rem;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }

            .box-support-footer {
                background-color: #f4f0ff;
                border: 1px solid #e0d4ff;
                border-radius: 10px;
                padding: 14px 20px;
                color: #4c1d95;
                font-size: 0.95rem;
                font-weight: 500;
                margin-top: 2.5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            /* --- DISPOSITIVOS MEDIANOS O PEQUEÑOS (RESPONSIVIDAD BREAKPOINT) --- */
            @media (max-width: 900px) {
                .main-container {
                    flex-direction: column;
                    min-height: auto;
                }
                .banner-azul, .panel-formulario {
                    flex: none;
                    width: 100%;
                    box-sizing: border-box;
                    padding: 2.5rem;
                }
                .banner-features {
                    margin-top: 2rem;
                }
            }
        </style>
    </head>
    <body>

        <div class="page-wrapper">
            <!-- CABECERA -->
            <div class="top-bar">
                <div class="top-logo">
                    <span class="bold-md">MD</span><span class="text-uni"> UNIMINUTO</span>
                    <span class="sub-virtual">VIRTUAL</span>
                </div>
                <div class="top-date">📅 06 de Julio de 2026</div>
            </div>

            <!-- TARJETA EN CONTENEDOR FLUIDO -->
            <div class="main-container">
                
                <!-- BANNER IZQUIERDO -->
                <div class="banner-azul">
                    <div class="banner-top">
                        <div class="logo-upload-zone">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Logo_Uniminuto.png/640px-Logo_Uniminuto.png" onerror="this.style.display='none';">
                        </div>
                        <div class="sub-marca">RAP Digital</div>
                        <div class="main-logo-title">MD UNIMINUTO<br><span>VIRTUAL</span></div>
                        <div class="short-line"></div>
                        <div class="main-description">
                            Gestión académica del proceso de Reconocimiento de Aprendizajes Previos.
                        </div>
                    </div>
                    
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
                
                <!-- FORMULARIO DERECHO -->
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
        </div>

    </body>
    </html>
    """, height=820)

# --- ESCENARIO B: PANEL ADMINISTRATIVO PRIVADO (MANTENIDO) ---
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