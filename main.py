import streamlit as st
from modules import registro, estado_pruebas, programacion, evaluacion  # Asegúrate de importar tus módulos aquí

# 1. Configuración de página (DEBE SER LA PRIMERA LÍNEA DE STREAMLIT)
st.set_page_config(page_title="AeroGrade - UNIMINUTO", layout="wide")

# 2. Inicialización del estado de sesión
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "rol" not in st.session_state:
    st.session_state["rol"] = "visitante"
if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""

# --- INTERFAZ DE LOGIN ---
if not st.session_state["autenticado"]:
    st.title("🔐 Acceso a AeroGrade")
    
    with st.form("login_form"):
        user = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Ingresar")
        
        if submit:
            if user == "admin" and password == "admin123":
                st.session_state["autenticado"] = True
                st.session_state["rol"] = "admin"
                st.session_state["usuario"] = "James Jaramillo"
                st.success("Acceso concedido")
                st.rerun()
            elif user == "visitante": # Opción para acceso limitado
                st.session_state["autenticado"] = True
                st.session_state["rol"] = "visitante"
                st.session_state["usuario"] = "Invitado"
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

# --- INTERFAZ PRINCIPAL (Solo si está autenticado) ---
else:
    # Barra lateral de navegación
    st.sidebar.title(f"Bienvenido, {st.session_state['usuario']}")
    st.sidebar.write(f"Rol: **{st.session_state['rol'].upper()}**")
    
    opcion = st.sidebar.radio(
        "Navegación Principal:",
        ["Registro", "Estado de Pruebas", "Programación", "Evaluación", "Dashboard"]
    )
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["autenticado"] = False
        st.session_state["rol"] = "visitante"
        st.rerun()

    # --- ENRUTAMIENTO DE MÓDULOS ---
    if opcion == "Registro":
        registro.render()
    elif opcion == "Estado de Pruebas":
        estado_pruebas.render()
    elif opcion =="Programación":
        programacion.render()
    elif opcion == "Evaluación":
        evaluacion.render()
    else:
        st.info(f"El módulo de {opcion} está en desarrollo.")