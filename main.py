from time import monotonic

import streamlit as st

from local_auth import (
    MAX_PASSWORD_LENGTH,
    current_account,
    login_attempts,
    normalize_username,
    verify_password,
)
from modules.ui import acceso, aplicar_estilo, perfil_lateral
from rutas import PAGINAS, crear_pagina, enlace, ir_a, principal
from sesion_navegador import cuentas_activas, inscribir, recuperar, sesiones

st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")
aplicar_estilo()

paginas = {ruta: crear_pagina(ruta, configuracion) for ruta, configuracion in PAGINAS.items()}
pagina = st.navigation(list(paginas.values()), position="hidden")
ruta = pagina.url_path

for param in ("u_auth", "p_auth", "auth_mode"):
    if param in st.query_params:
        del st.query_params[param]

accounts = cuentas_activas()
session = st.session_state.get("rap_session")
identificador = st.session_state.get("rap_id")
terminada = False
if identificador is not None:
    session = sesiones.validar(identificador, accounts)
    if session is None:
        st.session_state.clear()
        st.session_state["rap_recuperacion_intentada"] = True
        terminada = True

now = monotonic()
account = current_account(session, accounts, now)
if account is None:
    if session is not None:
        st.session_state.clear()
        st.session_state["rap_recuperacion_intentada"] = True
        terminada = True
    recuperar(accounts)
    with acceso():
        st.header("Acceso al sistema", anchor=False)
        st.caption("Inicia sesión para continuar con RAP Digital.")
        if not any(user.role == "admin" for user in accounts.values()):
            st.warning("El acceso a Gestión RAP aún no está configurado.")
            st.stop()
        if terminada:
            st.info("Tu sesión terminó. Vuelve a iniciar sesión.")

        with st.form("acceso_rap", clear_on_submit=True, border=False):
            username = st.text_input("Usuario", max_chars=64)
            password = st.text_input("Contraseña", type="password", max_chars=MAX_PASSWORD_LENGTH)
            if st.form_submit_button("Iniciar sesión", type="primary", width="stretch"):
                username = normalize_username(username)
                candidate = accounts.get(username)
                if not login_attempts.reserve(username):
                    st.error("Demasiados intentos. Vuelve a intentarlo en unos minutos.")
                elif not verify_password(password, candidate):
                    st.error("Usuario o contraseña incorrectos.")
                else:
                    login_attempts.reset_account(username)
                    st.session_state.clear()
                    signed_in_at = monotonic()
                    session = (username, candidate.revision, signed_in_at, signed_in_at)
                    st.session_state["rap_session"] = session
                    st.session_state["rap_id"] = sesiones.abrir(session)
                    st.rerun()
    st.stop()

username, revision, started, _ = session
st.session_state["rap_session"] = (username, revision, started, now)
inscribir(st.session_state.get("rap_id"))

role = account.role
st.session_state["usuario"] = account.name
st.session_state["rol"] = role
st.session_state["_rap_paginas"] = paginas

if role not in PAGINAS[ruta][3]:
    ir_a(principal(role))


def logout():
    identificador = st.session_state.get("rap_id")
    sesiones.cerrar(identificador)
    st.session_state.clear()
    st.session_state["rap_revocada"] = identificador
    st.session_state["rap_recuperacion_intentada"] = True


with st.sidebar:
    perfil_lateral(account.name, role)
    for destino, (_, _, _, roles, menu) in PAGINAS.items():
        if menu and role in roles:
            activa = ruta == destino or (destino == "registro" and not PAGINAS[ruta][4])
            with st.container(key="rap-menu-activo" if activa else None):
                enlace(destino, nueva_pestana=True)
    st.divider()
    with st.container(key="rap-menu-cerrar"):
        st.button("Cerrar sesión", icon=":material/logout:", width="stretch", type="tertiary", on_click=logout)

pagina.run()
