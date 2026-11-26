import streamlit as st

from local_auth import MAX_PASSWORD_LENGTH
from modules.ui import acceso, aplicar_estilo, perfil_lateral
from rutas import PAGINAS, crear_pagina, enlace, ir_a, principal
from web_auth import COOKIE_NAME, cuentas, sesiones

st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")
aplicar_estilo()

paginas = {ruta: crear_pagina(ruta, config) for ruta, config in PAGINAS.items()}
pagina = st.navigation(list(paginas.values()), position="hidden")
ruta = pagina.url_path

for param in ("u_auth", "p_auth", "auth_mode"):
    if param in st.query_params:
        del st.query_params[param]

accounts = cuentas()
token = st.context.cookies.get(COOKIE_NAME)
account = sesiones.validar(token, accounts)
if account is None:
    st.session_state.clear()
    with acceso():
        st.header("Acceso al sistema", anchor=False)
        st.caption("Inicia sesión para continuar con RAP Digital.")
        if not any(user.role == "admin" for user in accounts.values()):
            st.warning("El acceso a Gestión RAP aún no está configurado.")
            st.stop()
        aviso = st.query_params.get("acceso")
        if aviso == "incorrecto":
            st.error("Usuario o contraseña incorrectos.")
        elif aviso == "intentos":
            st.error("Demasiados intentos. Vuelve a intentarlo en unos minutos.")
        elif aviso == "ocupado":
            st.error("Hay demasiadas sesiones activas. Vuelve a intentarlo en unos minutos.")
        elif token:
            st.info("Tu sesión terminó. Vuelve a iniciar sesión.")
        st.html(f"""
            <form class="rap-auth-form" method="post" action="./rap-iniciar">
                <input type="hidden" name="ruta" value="{ruta}">
                <label for="rap-usuario">Usuario</label>
                <input id="rap-usuario" name="usuario" autocomplete="username" maxlength="64" required>
                <label for="rap-password">Contraseña</label>
                <input id="rap-password" name="password" type="password" autocomplete="current-password"
                       maxlength="{MAX_PASSWORD_LENGTH}" required>
                <button type="submit">Iniciar sesión</button>
            </form>
        """)
    st.stop()

role = account.role
st.session_state["usuario"] = account.name
st.session_state["rol"] = role
st.session_state["_rap_paginas"] = paginas

if role not in PAGINAS[ruta][3]:
    ir_a(principal(role))

with st.sidebar:
    perfil_lateral(account.name, role)
    for destino, (_, _, _, roles, menu) in PAGINAS.items():
        if menu and role in roles:
            activa = ruta == destino or (destino == "registro" and not PAGINAS[ruta][4])
            with st.container(key="rap-menu-activo" if activa else None):
                enlace(destino, nueva_pestana=True)
    st.divider()
    st.html("""
        <form class="rap-salir" method="post" action="./rap-salir">
            <button type="submit">Cerrar sesión</button>
        </form>
    """)

pagina.run()
