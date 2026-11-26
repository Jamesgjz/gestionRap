from importlib import import_module
from time import time

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

st.set_page_config(page_title="Gestión RAP - Uniminuto Virtual", page_icon="🔒", layout="wide")

# Retira parámetros de acceso que podrían venir de enlaces anteriores.
for param in ("u_auth", "p_auth", "auth_mode"):
    if param in st.query_params:
        del st.query_params[param]

try:
    oidc = st.secrets.get("auth", {})
    access = st.secrets.get("rap_access", {})
except StreamlitSecretNotFoundError:
    oidc, access = {}, {}

if not all(oidc.get(key) for key in (
    "redirect_uri", "cookie_secret", "client_id", "client_secret", "server_metadata_url"
)) or not access.get("admin_subjects"):
    st.title("Gestión RAP · UNIMINUTO Virtual")
    st.warning("El acceso institucional todavía no está configurado. Contacta al administrador.")
    st.stop()

if not st.user.is_logged_in:
    st.title("Gestión RAP · UNIMINUTO Virtual")
    st.write("Reconocimiento de Aprendizajes Previos")
    if st.button("Iniciar sesión", type="primary"):
        st.login()
    st.stop()

subject = st.user.get("sub")
expires = st.user.get("exp")
if not isinstance(expires, (int, float)) or expires <= time():
    st.warning("Tu sesión venció.")
    if st.button("Volver a iniciar sesión"):
        st.logout()
    st.stop()

role = None
for candidate, setting in (("admin", "admin_subjects"), ("publico", "consulta_subjects")):
    subjects = access.get(setting, [])
    if subject and isinstance(subjects, list) and subject in subjects:
        role = candidate
        break

if role is None:
    st.error("Tu cuenta no tiene acceso a Gestión RAP.")
    if st.button("Cerrar sesión"):
        st.logout()
    st.stop()

if st.session_state.get("identidad_rap") != (subject, role):
    st.session_state.clear()
    st.session_state["identidad_rap"] = (subject, role)

user_name = str(st.user.get("name") or st.user.get("email") or "Usuario")
st.session_state["usuario"] = user_name
st.session_state["rol"] = role
pages = {
    "Inicio": ("inicio", "Inicio", ":material/home:"),
    "Registro Estudiantes": ("registro", "Registro de Estudiantes", ":material/group:"),
    "Estado de Pruebas": ("estado_pruebas", "Estado de Pruebas", ":material/assignment:"),
    "Programación": ("programacion", "Programación", ":material/calendar_today:"),
    "Evaluación": ("evaluacion", "Evaluación", ":material/rate_review:"),
    "Dashboard / KPIs": ("dashboard", "Dashboard / KPIs", ":material/dashboard:"),
}
if role == "publico":
    pages = {"Dashboard / KPIs": pages["Dashboard / KPIs"]}


def navigate(page):
    st.session_state["opcion_menu"] = page


def logout():
    st.session_state.clear()
    st.logout()

with st.sidebar:
    st.markdown("**UNIMINUTO Virtual · RAP Digital**")
    st.text(user_name)
    st.caption("Administración" if role == "admin" else "Consulta")
    for page, (_, label, icon) in pages.items():
        st.button(label, icon=icon, width="stretch", on_click=navigate, args=(page,))
    st.button("Cerrar sesión", icon=":material/logout:", width="stretch", on_click=logout)

selected = st.session_state.get("opcion_menu")
if selected not in pages:
    selected = next(iter(pages))

from database import DatabaseError

try:
    import_module(f"modules.{pages[selected][0]}").render()
except DatabaseError:
    st.error("No se pudo completar la operación en la base de datos. Intenta de nuevo.")
