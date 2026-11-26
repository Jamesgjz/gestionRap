from importlib import import_module
from time import monotonic

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

from errors import DatabaseError
from local_auth import (
    MAX_PASSWORD_LENGTH,
    current_account,
    login_attempts,
    normalize_username,
    read_accounts,
    verify_password,
)
from modules.ui import acceso, aplicar_estilo, perfil_lateral

st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")
aplicar_estilo()

# Retira parámetros de acceso que podrían venir de enlaces anteriores.
for param in ("u_auth", "p_auth", "auth_mode"):
    if param in st.query_params:
        del st.query_params[param]

try:
    accounts = read_accounts(st.secrets.get("rap_accounts", {}))
except StreamlitSecretNotFoundError:
    accounts = {}

session = st.session_state.get("rap_session")
now = monotonic()
account = current_account(session, accounts, now)
if account is None:
    if session is not None:
        st.session_state.clear()

    with acceso():
        st.header("Acceso al sistema", anchor=False)
        st.caption("Inicia sesión para continuar con RAP Digital.")
        if not any(user.role == "admin" for user in accounts.values()):
            st.warning("El acceso a Gestión RAP aún no está configurado.")
            st.stop()
        if session is not None:
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
                    st.session_state["rap_session"] = (username, candidate.revision, signed_in_at, signed_in_at)
                    st.rerun()
    st.stop()

username, revision, started, _ = session
st.session_state["rap_session"] = (username, revision, started, now)
user_name = account.name
role = account.role
st.session_state["usuario"] = user_name
st.session_state["rol"] = role
pages = {
    "Inicio": ("inicio", "Inicio", ":material/home:"),
    "Registro de participantes": ("registro", "Registro de participantes", ":material/group:"),
    "Programas académicos": ("programas", "Programas académicos", ":material/account_tree:"),
    "Estado de Pruebas": ("estado_pruebas", "Estado de Pruebas", ":material/assignment:"),
    "Programación": ("programacion", "Programación", ":material/calendar_today:"),
    "Evaluación": ("evaluacion", "Evaluación", ":material/rate_review:"),
    "Dashboard / KPIs": ("dashboard", "Dashboard / KPIs", ":material/dashboard:"),
}
if role == "consulta_academica":
    pages = {
        "Estado de Pruebas": pages["Estado de Pruebas"],
        "Programación": pages["Programación"],
        "Resultados": ("evaluacion", "Resultados", ":material/assignment_turned_in:"),

    }
elif role == "consulta":
    pages = {"Dashboard / KPIs": pages["Dashboard / KPIs"]}


def navigate(page):
    st.session_state["opcion_menu"] = page


def logout():
    st.session_state.clear()

selected = st.session_state.get("opcion_menu")
if selected not in pages:
    selected = next(iter(pages))

with st.sidebar:
    perfil_lateral(user_name, role)
    for page, (_, label, icon) in pages.items():
        st.button(
            label, icon=icon, width="stretch", on_click=navigate, args=(page,),
            type="primary" if page == selected else "tertiary",
        )
    st.divider()
    st.button("Cerrar sesión", icon=":material/logout:", width="stretch", type="tertiary", on_click=logout)

try:
    module_name = pages[selected][0]
    module = import_module(f"modules.{module_name}")
    if role == "consulta_academica":
        module.render_consulta()
    else:
        module.render()
except DatabaseError:
    st.error("No se pudo completar la operación en la base de datos.")
    st.button("Reintentar conexión", icon=":material/refresh:")
