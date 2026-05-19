import streamlit as st
from modules import registro, estado_pruebas, programacion, evaluacion, dashboard

# Configuración de la página
st.set_page_config(page_title="Gestión RAP", page_icon="🔒", layout="centered")

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .login-container {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .main-title {
        color: #1e3a8a;
        font-weight: 700;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 1rem;
    }
    div.stButton > button:first-child {
        background-color: #0056b3;
        color: white;
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN INICIAL ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    st.markdown('<h1 class="main-title">Gestión RAP</h1>', unsafe_allow_html=True)
    
    # Selector de modo para el usuario
    modo = st.tabs(["🔑 Acceso Administrativo", "📝 Registro Público"])
    
    with modo[0]:
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            usuario = st.text_input("Usuario", placeholder="Admin")
            contrasena = st.text_input("Contraseña", type="password", placeholder="••••••••")
            
            if st.button("INGRESAR AL PANEL"):
                if usuario == "admin" and contrasena == "admin123":
                    st.session_state['autenticado'] = True
                    st.session_state['usuario'] = "James Jaramillo"
                    st.session_state['rol'] = "admin"
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
            st.markdown('</div>', unsafe_allow_html=True)

    with modo[1]:
        st.info("Utilice este espacio para registrar nuevos estudiantes al sistema.")
        # Aquí llamamos al módulo de registro pero en modo "limitado"
        registro.render() 

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
        "Evaluación"
        "Dashboard / KPIs"
    ])

    if opcion == "Inicio":
        st.subheader("Panel de Control")
        st.write("Bienvenido, James. El sistema está listo para gestionar las pruebas RAP.")
    elif opcion == "Registro Estudiantes":
        registro.render()
    elif opcion == "Estado de Pruebas":
        estado_pruebas.render()
    elif opcion == "Programación":
        programacion.render()
    elif opcion == "Evaluación":
        evaluacion.render()
    elif opcion=="Dashboard / KPIs":
        dashboard.render()