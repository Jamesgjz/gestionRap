import streamlit as st
from modules import registro, estado_pruebas, programacion, evaluacion

# Configuración de la página (Debe ser lo primero)
st.set_page_config(page_title="Gestión RAP", page_icon="🔒", layout="centered")

# --- CSS PERSONALIZADO PARA UNA INTERFAZ MODERNA ---
st.markdown("""
    <style>
    /* Fondo de la página */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Contenedor del Login */
    .login-container {
        background-color: white;
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Título Principal */
    .main-title {
        color: #1e3a8a;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        font-size: 3rem !important;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    /* Estilo del botón Ingresar */
    div.stButton > button:first-child {
        background-color: #0056b3;
        color: white;
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #003d82;
        border: none;
        color: white;
    }
    
    /* Quitar el menú de Streamlit arriba para que se vea más limpio */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE ACCESO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    # Centramos el contenido visualmente
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="main-title">Gestión RAP 🔒</h1>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            usuario = st.text_input("Usuario", placeholder="Ingrese su usuario")
            contrasena = st.text_input("Contraseña", type="password", placeholder="••••••••")
            
            if st.button("INGRESAR"):
                # Aquí van tus credenciales actuales
                if usuario == "James Jaramillo" and contrasena == "tu_password_segura":
                    st.session_state['autenticado'] = True
                    st.session_state['usuario'] = usuario
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- INTERFAZ PRINCIPAL UNA VEZ LOGUEADO ---
    st.sidebar.image("https://www.uniminuto.edu/sites/default/files/logo-uniminuto.png", width=200)
    st.sidebar.title(f"👨‍🏫 {st.session_state['usuario']}")
    
    opcion = st.sidebar.radio("Menú de Navegación", [
        "Inicio", 
        "Registro Estudiantes", 
        "Estado de Pruebas", 
        "Programación", 
        "Evaluación"
    ])

    if opcion == "Inicio":
        st.title("Bienvenido al Sistema de Gestión RAP")
        st.info("Seleccione una opción en el menú lateral para comenzar.")
        
    elif opcion == "Registro Estudiantes":
        registro.render()
    elif opcion == "Estado de Pruebas":
        estado_pruebas.render()
    elif opcion == "Programación":
        programacion.render()
    elif opcion == "Evaluación":
        evaluacion.render()